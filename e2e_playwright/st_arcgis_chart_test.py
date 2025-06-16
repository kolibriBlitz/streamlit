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

from playwright.sync_api import Page

from e2e_playwright.conftest import ImageCompareFunction


def test_chart(themed_app: Page, assert_snapshot: ImageCompareFunction):
    """Check that the arcgis chart is displaying a map correctly."""
    import time

    time.sleep(10)  # Arcgis maps take a bit to load

    chart = themed_app.get_by_test_id("stArcgisChart").first
    assert_snapshot(chart, name="st_arcgis_chart")
