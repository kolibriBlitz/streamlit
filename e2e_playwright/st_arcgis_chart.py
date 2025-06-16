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

from arcgis.features import FeatureLayer
from arcgis.gis import GIS

import streamlit as st

gis = GIS()
usa_map = gis.map("USA")
layer_url = "https://services2.arcgis.com/ZQgQTuoyBrtmoGdP/arcgis/rest/services/SF_311_Incidents/FeatureServer/0"
layer = FeatureLayer(layer_url)
usa_map.content.add(layer)

# Display in Streamlit (if you have a Streamlit ArcGIS component)
st.arcgis_chart(usa_map, height=500)
