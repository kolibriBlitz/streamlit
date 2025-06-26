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

"""toast unit tests."""

from __future__ import annotations

import pytest

import streamlit as st
from streamlit.errors import StreamlitAPIException
from tests.delta_generator_test_case import DeltaGeneratorTestCase


class ToastTest(DeltaGeneratorTestCase):
    def test_just_text(self):
        """Test that it can be called with just text."""
        st.toast("toast text")

        c = self.get_delta_from_queue().new_element.toast
        assert c.body == "toast text"
        assert c.icon == ""

    def test_no_text(self):
        """Test that an error is raised if no text is provided."""
        with pytest.raises(StreamlitAPIException) as e:
            st.toast("")
        assert str(e.value) == "Toast body cannot be blank - please provide a message."

    def test_valid_icon(self):
        """Test that it can be called passing a valid emoji as icon."""
        st.toast("toast text", icon="🦄")

        c = self.get_delta_from_queue().new_element.toast
        assert c.body == "toast text"
        assert c.icon == "🦄"

    def test_invalid_icon(self):
        """Test that an error is raised if an invalid icon is provided."""
        with pytest.raises(StreamlitAPIException) as e:
            st.toast("toast text", icon="invalid")
        assert str(e.value) == (
            'The value "invalid" is not a valid emoji. Shortcodes '
            "are not allowed, please use a single character instead."
        )

    def test_toast_from_dialog(self):
        """Test that toasts work correctly when called from within a dialog."""

        @st.dialog("Test Dialog")
        def my_dialog():
            st.toast("Toast from dialog")

        # Call the dialog function to trigger the toast
        my_dialog()

        # The toast should be enqueued to the main container
        # Try to get the toast directly first
        try:
            # Try direct approach first
            toast = self.get_delta_from_queue().new_element.toast
            assert toast.body == "Toast from dialog"
            assert toast.icon == ""
            return  # Test passed
        except (AttributeError, AssertionError):
            # If direct approach fails, search through all messages
            pass

        # Fallback: search through all messages
        messages = self.get_all_messages_from_queue()

        # Find the toast message
        toast_found = False
        for _i, msg in enumerate(messages):
            if hasattr(msg, "delta") and hasattr(msg.delta, "new_element"):  # noqa: SIM102
                if hasattr(msg.delta.new_element, "toast"):
                    c = msg.delta.new_element.toast
                    assert c.body == "Toast from dialog"
                    assert c.icon == ""
                    toast_found = True
                    break

        assert toast_found, (
            f"Toast message was not found in the queue. Found {len(messages)} messages."
        )
