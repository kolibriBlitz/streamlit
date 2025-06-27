# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022-2025)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from playwright.sync_api import Page, expect

from e2e_playwright.conftest import ImageCompareFunction
from e2e_playwright.shared.app_utils import check_top_level_class

TOTAL_TABLE_ELEMENTS = 41


def test_table_rendering(app: Page, assert_snapshot: ImageCompareFunction):
    """Test that st.table renders correctly via snapshot testing."""
    table_elements = app.get_by_test_id("stTable")
    expect(table_elements).to_have_count(TOTAL_TABLE_ELEMENTS)

    for i, element in enumerate(table_elements.all()):
        assert_snapshot(element, name=f"st_table-{i}")


def test_themed_table_rendering(
    themed_app: Page, assert_snapshot: ImageCompareFunction
):
    """Test that st.table renders correctly with different theming."""
    table_elements = themed_app.get_by_test_id("stTable")
    expect(table_elements).to_have_count(TOTAL_TABLE_ELEMENTS)

    # Only test a single table element to ensure theming is applied correctly:
    assert_snapshot(table_elements.nth(30), name="st_table-themed")


def test_pandas_styler_tooltips(app: Page, assert_snapshot: ImageCompareFunction):
    """Test that pandas styler tooltips render correctly."""
    styled_table = app.get_by_test_id("stTable").nth(31)
    table_cell = styled_table.locator("td", has_text="38").first
    table_cell.hover()
    expect(table_cell.locator(".pd-t")).to_have_css("visibility", "visible")
    assert_snapshot(styled_table, name="st_table-styler_tooltip")


def test_check_top_level_class(app: Page):
    """Check that the top level class is correctly set."""
    check_top_level_class(app, "stTable")


def test_hide_headers_and_index(app: Page):
    """Test that tables correctly hide headers and/or index when requested."""
    # Regular table
    regular_table = app.get_by_test_id("stTable").nth(34)
    expect(regular_table).to_be_visible()
    # Should have headers and index visible
    expect(regular_table.locator("thead")).to_be_visible()
    expect(regular_table.locator("th[scope='row']").first).to_be_visible()

    # Table with hidden headers
    hidden_headers_table = app.get_by_test_id("stTable").nth(35)
    expect(hidden_headers_table).to_be_visible()
    # Should NOT have headers visible
    expect(hidden_headers_table.locator("thead")).not_to_be_visible()
    # Should still have index visible
    expect(hidden_headers_table.locator("th[scope='row']").first).to_be_visible()

    # Table with hidden index
    hidden_index_table = app.get_by_test_id("stTable").nth(36)
    expect(hidden_index_table).to_be_visible()
    # Should have headers visible
    expect(hidden_index_table.locator("thead")).to_be_visible()
    # Should NOT have index visible
    expect(hidden_index_table.locator("th[scope='row']")).to_have_count(0)

    # Table with both hidden
    both_hidden_table = app.get_by_test_id("stTable").nth(37)
    expect(both_hidden_table).to_be_visible()
    # Should NOT have headers visible
    expect(both_hidden_table.locator("thead")).not_to_be_visible()
    # Should NOT have index visible
    expect(both_hidden_table.locator("th[scope='row']")).to_have_count(0)

    # MultiIndex table with hidden index
    multi_hidden_index = app.get_by_test_id("stTable").nth(38)
    expect(multi_hidden_index).to_be_visible()
    # Should have headers but no index columns
    expect(multi_hidden_index.locator("thead")).to_be_visible()
    expect(multi_hidden_index.locator("th[scope='row']")).to_have_count(0)

    # Styled table with hidden headers
    styled_hidden_headers = app.get_by_test_id("stTable").nth(39)
    expect(styled_hidden_headers).to_be_visible()
    # Should NOT have headers visible but should have index
    expect(styled_hidden_headers.locator("thead")).not_to_be_visible()
    expect(styled_hidden_headers.locator("th[scope='row']").first).to_be_visible()

    # Markdown table with hidden index
    markdown_hidden_index = app.get_by_test_id("stTable").nth(40)
    expect(markdown_hidden_index).to_be_visible()
    # Should have headers but no index
    expect(markdown_hidden_index.locator("thead")).to_be_visible()
    expect(markdown_hidden_index.locator("th[scope='row']")).to_have_count(0)


def test_hide_headers_and_index_visual(app: Page, assert_snapshot):
    """Visual test for tables with hidden headers and/or index."""
    # Capture the entire section
    hide_section = (
        app.locator("h2").filter(has_text="Hide Headers and Index").locator("..")
    )

    # Wait for tables to be fully rendered
    app.wait_for_timeout(500)

    assert_snapshot(hide_section, name="st_table-hide_headers_and_index")
