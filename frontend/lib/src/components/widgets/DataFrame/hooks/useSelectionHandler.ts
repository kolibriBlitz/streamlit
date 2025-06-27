/**
 * Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022-2025)
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import { useCallback, useState } from "react"

import { CompactSelection, GridSelection } from "@glideapps/glide-data-grid"
import isEqual from "lodash/isEqual"

import { Arrow as ArrowProto } from "@streamlit/protobuf"

import { BaseColumn } from "~lib/components/widgets/DataFrame/columns"

export type SelectionHandlerReturn = {
  // The current selection state
  gridSelection: GridSelection
  // True, if row selection is activated
  isRowSelectionActivated: boolean
  // True, if multi row selection is activated
  isMultiRowSelectionActivated: boolean
  // True, if column selection is activated
  isColumnSelectionActivated: boolean
  // True, if multi column selections is activated
  isMultiColumnSelectionActivated: boolean
  // True, if cell selection is activated
  isCellSelectionActivated: boolean
  // True, if multi cell selection is activated
  isMultiCellSelectionActivated: boolean
  // True, if at least one row is selected
  isRowSelected: boolean
  // True, if at least one column is selected
  isColumnSelected: boolean
  // True, if at least one cell is selected
  isCellSelected: boolean
  // Callback to clear selections
  clearSelection: (keepRows?: boolean, keepColumns?: boolean) => void
  // Callback to process selection changes from the grid
  processSelectionChange: (newSelection: GridSelection) => void
}

/**
 * Custom hook that handles all selection capabilities for the interactive data table.
 *
 * @param element - The Arrow proto message
 * @param isEmptyTable - Whether the table is empty
 * @param isDisabled - Whether the table is disabled
 * @param columns - The columns of the table.
 * @param syncSelectionState - The callback to sync the selection state
 *
 * @returns the selection handler return object
 */
function useSelectionHandler(
  element: ArrowProto,
  isEmptyTable: boolean,
  isDisabled: boolean,
  columns: BaseColumn[],
  syncSelectionState: (newSelection: GridSelection) => void
): SelectionHandlerReturn {
  const [gridSelection, setGridSelection] = useState<GridSelection>({
    columns: CompactSelection.empty(),
    rows: CompactSelection.empty(),
    current: undefined,
  })

  const isRowSelectionActivated =
    !isEmptyTable &&
    !isDisabled &&
    (element.selectionMode.includes(ArrowProto.SelectionMode.MULTI_ROW) ||
      element.selectionMode.includes(ArrowProto.SelectionMode.SINGLE_ROW))
  const isMultiRowSelectionActivated =
    isRowSelectionActivated &&
    element.selectionMode.includes(ArrowProto.SelectionMode.MULTI_ROW)

  const isColumnSelectionActivated =
    !isEmptyTable &&
    !isDisabled &&
    (element.selectionMode.includes(ArrowProto.SelectionMode.SINGLE_COLUMN) ||
      element.selectionMode.includes(ArrowProto.SelectionMode.MULTI_COLUMN))
  const isMultiColumnSelectionActivated =
    isColumnSelectionActivated &&
    element.selectionMode.includes(ArrowProto.SelectionMode.MULTI_COLUMN)

  const isCellSelectionActivated =
    !isEmptyTable &&
    !isDisabled &&
    (element.selectionMode.includes(ArrowProto.SelectionMode.SINGLE_CELL) ||
      element.selectionMode.includes(ArrowProto.SelectionMode.MULTI_CELL))

  const isMultiCellSelectionActivated =
    isCellSelectionActivated &&
    element.selectionMode.includes(ArrowProto.SelectionMode.MULTI_CELL)

  const isRowSelected = gridSelection.rows.length > 0
  const isColumnSelected = gridSelection.columns.length > 0
  const isCellSelected = gridSelection.current !== undefined

  /**
   * This callback is used to process selection changes and - if activated -
   * trigger a sync of the state with the widget state
   */
  const processSelectionChange = useCallback(
    (newSelection: GridSelection) => {
      const rowSelectionChanged = !isEqual(
        newSelection.rows.toArray(),
        gridSelection.rows.toArray()
      )
      const columnSelectionChanged = !isEqual(
        newSelection.columns.toArray(),
        gridSelection.columns.toArray()
      )
      const cellSelectionChanged = !isEqual(
        newSelection.current,
        gridSelection.current
      )

      const shouldSync =
        (isRowSelectionActivated && rowSelectionChanged) ||
        (isColumnSelectionActivated && columnSelectionChanged) ||
        (isCellSelectionActivated && cellSelectionChanged)

      let finalSelection = newSelection // Start with what the grid gave us

      // Ensure index columns are not part of a column selection sent to Python
      if (
        isColumnSelectionActivated &&
        columnSelectionChanged &&
        finalSelection.columns.length >= 0
      ) {
        let cleanedColumns = finalSelection.columns
        columns.forEach((column, idx) => {
          if (column.isIndex) {
            cleanedColumns = cleanedColumns.remove(idx)
          }
        })
        if (cleanedColumns.length < finalSelection.columns.length) {
          finalSelection = {
            ...finalSelection,
            columns: cleanedColumns,
          }
        }
      }

      setGridSelection(finalSelection) // Update UI with the (potentially column-cleaned) selection from grid

      if (shouldSync) {
        syncSelectionState(finalSelection) // Sync this selection
      }
    },
    [
      gridSelection, // Need old gridSelection for changed checks
      isRowSelectionActivated,
      isColumnSelectionActivated,
      isCellSelectionActivated,
      syncSelectionState,
      columns,
    ]
  )

  /**
   * This callback is used to selections (row/column/cell)
   * and sync the state with the widget state if column or row selections
   * are activated and the selection has changed.
   *
   * @param keepRows - Whether to keep the row selection (default: false)
   * @param keepColumns - Whether to keep the column selection (default: false)
   */
  const clearSelection = useCallback(
    (keepRows = false, keepColumns = false) => {
      const oldCellSelectionExisted = gridSelection.current !== undefined
      const emptySelection: GridSelection = {
        columns: keepColumns
          ? gridSelection.columns
          : CompactSelection.empty(),
        rows: keepRows ? gridSelection.rows : CompactSelection.empty(),
        current: undefined,
      }
      setGridSelection(emptySelection)

      const cellSelectionCleared =
        isCellSelectionActivated && oldCellSelectionExisted
      const rowSelectionCleared =
        !keepRows && isRowSelectionActivated && gridSelection.rows.length > 0
      const columnSelectionCleared =
        !keepColumns &&
        isColumnSelectionActivated &&
        gridSelection.columns.length > 0

      if (
        cellSelectionCleared ||
        rowSelectionCleared ||
        columnSelectionCleared
      ) {
        syncSelectionState(emptySelection)
      }
    },
    [
      gridSelection,
      isRowSelectionActivated,
      isColumnSelectionActivated,
      isCellSelectionActivated,
      syncSelectionState,
    ]
  )

  return {
    gridSelection,
    isRowSelectionActivated,
    isMultiRowSelectionActivated,
    isColumnSelectionActivated,
    isMultiColumnSelectionActivated,
    isCellSelectionActivated,
    isMultiCellSelectionActivated,
    isRowSelected,
    isColumnSelected,
    isCellSelected,
    clearSelection,
    processSelectionChange,
  }
}

export default useSelectionHandler
