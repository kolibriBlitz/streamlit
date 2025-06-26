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

import streamlit as st

# Background content
st.title("Main App Content")
st.write("This content should remain visible behind the dialog")
st.info("Background info box")


# Dialog with toast
@st.dialog("Test Dialog")
def show_dialog():
    st.write("Dialog content")
    if st.button("Show Toast"):
        st.toast("Hello from dialog!")
    if st.button("Close Dialog"):
        st.rerun()


# Button to open dialog
if st.button("Open Dialog"):
    show_dialog()

# More background content
st.write("More background content that should stay visible")
st.success("This should also remain visible")
