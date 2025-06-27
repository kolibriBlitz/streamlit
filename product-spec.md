## Product Specification: Cell Selections in `st.dataframe`

**1. Goal**

Enable developers to allow users to select single or multiple cells in an `st.dataframe` and retrieve information about these selected cells in Python.

**2. Python API (`st.dataframe`)**

*   **New `selection_mode` options:**
    *   `"single-cell"`: Allows users to select only one cell at a time. Clicking a new cell deselects the previous one.
    *   `"multi-cell"`: Allows users to select a rectangular range of cells. Clicking and dragging will define the range.
*   **Combination with existing modes:**
    *   Cell selection modes (`"single-cell"`, `"multi-cell"`) can be combined with row selection modes (`"single-row"`, `"multi-row"`) and column selection modes (`"single-column"`, `"multi-column"`).
    *   For example, `selection_mode=["multi-row", "single-cell"]` would allow the user to select multiple rows *and* a single cell independently. The returned selection state will reflect all active selections.
    *   The following combinations will raise an error due to inherent conflict:
        *   `{"single-row", "multi-row"}`
        *   `{"single-column", "multi-column"}`
        *   `{"single-cell", "multi-cell"}`
*   **Return Value (`DataframeState`)**:
    *   When `on_select` is set to `"rerun"` or a callable, and a cell selection mode is active, the `st.dataframe` function will return a `DataframeState` dictionary. This dictionary will be extended to include information about selected cells.
    *   A new key, `"cells"`, will be added to the `selection` dictionary within `DataframeState`.
    *   `DataframeState.selection.cells`: A list of dictionaries, where each dictionary represents a selected cell and contains:
        *   `row`: The original integer index of the selected cell's row.
        *   `column`: The string name of the selected cell's column.

    **Python Type Definitions:**

    ```python
    class DataframeCellPosition(TypedDict):
        row: int
        column: str

    class DataframeSelectionState(TypedDict, total=False):
        rows: list[int]
        columns: list[str]
        cells: list[DataframeCellPosition]  # New field for cell selections

    class DataframeState(TypedDict, total=False):
        selection: DataframeSelectionState
    ```
*   **`on_select` Behavior:**
    *   This parameter will continue to function as it currently does (`"ignore"`, `"rerun"`, or a `callable`).
    *   If a cell selection mode is enabled, any change to the cell selection will trigger a rerun or the callback, and the `st.dataframe` call will return the updated `DataframeState` including the `cells` data.

**3. Frontend Behavior (GlideDataEditor)**

*   **Selection Mechanism:**
    *   The underlying GlideDataEditor's `rangeSelect` prop will likely be maintained as `"rect"` (or `"cell"` for touch devices) to support rectangular selections.
    *   The distinction between `"single-cell"` and `"multi-cell"` will be handled by how the frontend processes the selection event from GlideDataEditor:
        *   For `"single-cell"`: Even if the user drags to select a range, only the primary cell of the interaction (e.g., where the mouse button was pressed) will be reported as selected.
        *   For `"multi-cell"`: All cells within the selected rectangle will be reported.
*   **Visual Indication:**
    *   Selected cells will be visually highlighted using GlideDataEditor's default cell/range selection appearance. This should be distinct enough, especially if combined with row/column selection highlights.
*   **Toolbar Interaction:**
    *   The "Clear selection" button in the toolbar will clear all types of selections, including cell selections.
*   **State Management:**
    *   The `gridSelection.current` object from GlideDataEditor, which contains `cell: GridCellPosition` and `range: Rectangle`, will be the primary source for cell selection information.
    *   The `useSelectionHandler` hook and the `DataFrame.tsx` component will be updated to interpret this information based on the active cell selection mode and translate it into the format expected by the Python backend (original row indices and column names).

**4. Protobuf Definition (`proto/streamlit/proto/Arrow.proto`)**

*   New enum values will be added to `Arrow.SelectionMode`:

    ```protobuf
    enum SelectionMode {
      SINGLE_ROW = 0;
      MULTI_ROW = 1;
      SINGLE_COLUMN = 2;
      MULTI_COLUMN = 3;
      SINGLE_CELL = 4; // New: Only one cell can be selected.
      MULTI_CELL = 5;  // New: Multiple cells (contiguous range) can be selected.
    }
    ```
*   The existing `repeated SelectionMode selection_mode = 12;` field in the `Arrow` message will be used to transmit these new modes.

**5. Backend Implementation (`lib/streamlit/elements/arrow.py`)**

*   **`parse_selection_mode` function:**
    *   This function will be updated to recognize `"single-cell"` and `"multi-cell"`.
    *   It will enforce the rule that `"single-cell"` and `"multi-cell"` cannot be used simultaneously.
    *   It will map these new string modes to the corresponding `ArrowProto.SelectionMode` enum values.
*   **`DataframeSelectionSerde` class:**
    *   The `deserialize` method will be updated to look for the `"cells"` key within the `"selection"` part of the JSON string received from the frontend. It will then reconstruct the list of `DataframeCellPosition` objects.
*   **Widget State Processing:**
    *   The backend will receive the selection state (including cell selections) as a JSON string. The primary change here is enabling the frontend to correctly construct this JSON string.

**6. Frontend Implementation**

*   **`useSelectionHandler.ts` (`frontend/lib/src/components/widgets/DataFrame/hooks/useSelectionHandler.ts`):**
    *   New boolean flags will be derived from `element.selectionMode`:
        *   `isCellSelectionActivated`
        *   `isMultiCellSelectionActivated` (distinct from just cell selection being active)
    *   These flags will be returned by the hook for use in `DataFrame.tsx`.
    *   The logic within `processSelectionChange` related to `syncSelection` will be reviewed to ensure it correctly triggers updates when cell selections change and are active.
*   **`DataFrame.tsx` (`frontend/lib/src/components/widgets/DataFrame/DataFrame.tsx`):**
    *   The `innerSyncSelectionState` callback (debounced into `syncSelectionState`) will be the main place for constructing the `selection.cells` array.
    *   It will use `gridSelection.current.cell` (for single-cell mode) or `gridSelection.current.range` (for multi-cell mode).
    *   It will iterate through the selected cell(s) based on the active mode.
    *   For each selected cell, it will:
        *   Convert the displayed row index to the original row index using `getOriginalIndex`.
        *   Convert the displayed column index to the column name using `getColumnName` (from `EditingState.ts`) and the `columns` array.
        *   Ensure that index columns are not reported as part of cell selections.
        *   Populate the `selectionState.selection.cells` array with `{row: originalRowIdx, column: columnName}` objects.
    *   This `selectionState` (now including `cells`) will then be stringified and sent to the backend via `widgetMgr.setStringValue`.
*   **GlideDataEditor Configuration:**
    *   The `rangeSelect` prop will likely remain `"rect"` or `"cell"`. The logic for handling single vs. multi-cell selection will reside in how `gridSelection.current` is interpreted, not by changing `rangeSelect` dynamically based on these specific modes.
