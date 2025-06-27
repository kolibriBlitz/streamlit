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

"""Test compute_and_register_element_id error message behavior for button group widgets."""

from __future__ import annotations

import pytest

from streamlit.elements.lib.utils import compute_and_register_element_id
from streamlit.errors import StreamlitDuplicateElementId
from tests.delta_generator_test_case import DeltaGeneratorTestCase


class TestButtonGroupErrorMessages(DeltaGeneratorTestCase):
    """Test that button group widgets show correct command names in error messages."""


    def test_segmented_control_error_message_shows_correct_name(self) -> None:
        """Test that segmented_control style shows 'segmented_control' in error messages."""
        # Create element IDs with segmented_control style (no key to force element ID duplication)
        _ = compute_and_register_element_id(
            "button_group",

            user_key=None,
            form_id=None,
            style="segmented_control",
            options=("a", "b", "c"),
        )

        # Try to create another element with the same parameters - should raise error mentioning "segmented_control"
        with pytest.raises(StreamlitDuplicateElementId) as exc_info:
            compute_and_register_element_id(
                "button_group",
                user_key=None,
                form_id=None,
                style="segmented_control",
                options=("a", "b", "c"),
            )

        # Verify the error message contains "segmented_control" not "button_group"
        assert "segmented_control" in str(exc_info.value)
        assert "button_group" not in str(exc_info.value)

    def test_pills_error_message_shows_correct_name(self):
        """Test that pills style shows 'pills' in error messages."""
        # Create element IDs with pills style (no key to force element ID duplication)
        _ = compute_and_register_element_id(
            "button_group",
            user_key=None,
            form_id=None,
            style="pills",
            options=("option1", "option2"),
        )

        # Try to create another element with the same parameters - should raise error mentioning "pills"
        with pytest.raises(StreamlitDuplicateElementId) as exc_info:
            compute_and_register_element_id(
                "button_group",
                user_key=None,
                form_id=None,
                style="pills",
                options=("option1", "option2"),
            )

        # Verify the error message contains "pills" not "button_group"
        assert "pills" in str(exc_info.value)
        assert "button_group" not in str(exc_info.value)

    def test_feedback_error_message_shows_correct_name(self):
        """Test that borderless style (used by st.feedback) shows 'feedback' in error messages."""
        # Create element IDs with borderless style (no key to force element ID duplication)
        _ = compute_and_register_element_id(
            "button_group",
            user_key=None,
            form_id=None,
            style="borderless",
            options="thumbs",
        )

        # Try to create another element with the same parameters - should raise error mentioning "feedback"
        with pytest.raises(StreamlitDuplicateElementId) as exc_info:
            compute_and_register_element_id(
                "button_group",
                user_key=None,
                form_id=None,
                style="borderless",
                options="thumbs",
            )

        # Verify the error message contains "feedback" not "button_group" or "borderless"
        assert "feedback" in str(exc_info.value)
        assert "button_group" not in str(exc_info.value)
        assert "borderless" not in str(exc_info.value)

    def test_button_group_without_style_shows_button_group(self):
        """Test that button_group without style shows 'button_group' in error messages."""
        # Create element IDs without style parameter (no key to force element ID duplication)
        _ = compute_and_register_element_id(
            "button_group",
            user_key=None,
            form_id=None,
            options=("a", "b"),
        )

        # Try to create another element with the same parameters - should raise error mentioning "button_group"
        with pytest.raises(StreamlitDuplicateElementId) as exc_info:
            compute_and_register_element_id(
                "button_group",
                user_key=None,
                form_id=None,
                options=("a", "b"),
            )

        # Verify the error message contains "button_group"
        assert "button_group" in str(exc_info.value)
