# Implementation Plan: Add hide_headers and hide_index to st.table

## Overview
Add two new optional boolean parameters to `st.table` to allow hiding column headers and/or the index column, providing consistency with `st.dataframe` and `st.data_editor` which already support `hide_index`.

## Implementation Steps

### 1. Update Protobuf Definition (Arrow.proto)
- Add two new optional boolean fields to the Arrow message:
  - `hide_headers`: Controls visibility of column headers
  - `hide_index`: Controls visibility of index column(s)

### 2. Backend Implementation (arrow.py)
- Update the `table()` method signature to accept the new parameters:
  - `hide_headers: bool = False`
  - `hide_index: bool = False`
- Pass these parameters to the Arrow protobuf when marshalling the table
- Ensure backward compatibility by using default values of `False`

### 3. Frontend Implementation (ArrowTable.tsx)
- Read the new `hideHeaders` and `hideIndex` properties from the protobuf
- Conditionally render:
  - The `<thead>` section based on `hideHeaders`
  - Index columns based on `hideIndex` (filter them out in `generateTableRow`)
- Update the column count calculation when index is hidden

### 4. Testing

#### Python Unit Tests (arrow_table_test.py)
- Test that `hide_headers=True` sets the proto field correctly
- Test that `hide_index=True` sets the proto field correctly
- Test default behavior (both False)
- Test combinations of both parameters

#### E2E Tests (st_table.py and st_table_test.py)
- Add visual tests for tables with headers hidden
- Add visual tests for tables with index hidden
- Add visual tests for tables with both headers and index hidden
- Test with different data types (regular DataFrame, MultiIndex, styled tables)
- Test that the feature works with Markdown content

### 5. Edge Cases to Consider
- Tables with MultiIndex (both row and column)
- Empty tables
- Single-cell tables
- Pandas Styler objects
- Tables with Markdown content
- Interaction with caption display

## Order of Implementation
1. Protobuf changes (requires `make protobuf`)
2. Backend implementation
3. Python unit tests
4. Frontend implementation
5. E2E tests

