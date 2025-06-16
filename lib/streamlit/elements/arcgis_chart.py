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

"""Streamlit support for ArcGIS maps."""

from __future__ import annotations

import json
from typing import (
    TYPE_CHECKING,
    Any,
    cast,
)

from streamlit import type_util
from streamlit.elements.lib.utils import Key, compute_and_register_element_id, to_key
from streamlit.errors import StreamlitAPIException
from streamlit.proto.ArcgisChart_pb2 import ArcgisChart as ArcgisChartProto
from streamlit.runtime.metrics_util import gather_metrics

if TYPE_CHECKING:
    from arcgis.widgets import Map

    from streamlit.delta_generator import DeltaGenerator


def extract_map_data(map_object: Map) -> dict[str, Any]:
    """Extract map configuration and data from ArcGIS map object."""

    if type_util.is_arcgis_version_less_than("2.4.0"):

        raise StreamlitAPIException(
            "Streamlit does not currently support Arcgis version "
            "older than 2.4. Please upgrade to Version 2.4"

        )

    return json.dumps(map_object._webmap_dict)


class ArcgisMixin:
    @gather_metrics("arcgis_chart")
    def arcgis_chart(
        self,
        map_object: Map,
        *,
        height: int | None = None,
        key: Key | None = None,
        **kwargs: Any,
    ) -> DeltaGenerator:
        """Display an interactive ArcGIS map.

        `ArcGIS <https://developers.arcgis.com/python/>`_ is a comprehensive
        mapping and spatial analytics platform. This function displays ArcGIS
        maps in Streamlit applications.

        .. Important::
            You must install ``arcgis`` to use this command and have appropriate
            ArcGIS credentials configured.

        Parameters
        ----------
        map_object : arcgis.mapping.WebMap, dict, or ArcGIS map widget
            The ArcGIS map object to render. This can be:

            - A WebMap object from arcgis.mapping
            - A map widget obtained from gis.map()
            - A dictionary containing map configuration

        height : int or None
            The height of the map in pixels. If ``None``, a default height will be used.

        key : str
            An optional string to use for giving this element a stable
            identity. If ``key`` is ``None`` (default), this element's identity
            will be determined based on the values of the other parameters.

        **kwargs
            Additional arguments for map configuration.

        Returns
        -------
        DeltaGenerator
            An internal placeholder for the map element.

        Example
        -------
        Basic usage with an ArcGIS map:

        >>> import streamlit as st
        >>> from arcgis.gis import GIS
        >>>
        >>> # Connect to ArcGIS Online
        >>> gis = GIS(profile="your_online_profile")
        >>>
        >>> # Create a map
        >>> map = gis.map("USA")
        >>> map.zoom = 4
        >>>
        >>> # Display the map
        >>> st.arcgis_chart(map)

        Example with custom height:

        >>> import streamlit as st
        >>> from arcgis.gis import GIS
        >>>
        >>> gis = GIS(profile="your_online_profile")
        >>> map = gis.map("New York")
        >>>
        >>> # Display map with custom height
        >>> st.arcgis_chart(map, height=600)

        """

        key = to_key(key)

        # Extract map data from the ArcGIS map object
        map_data = extract_map_data(map_object)

        arcgis_chart_proto = ArcgisChartProto()

        if height is not None:
            arcgis_chart_proto.height = height

        # Serialize the map data
        arcgis_chart_proto.spec = map_data

        # Add any additional config from kwargs
        config = dict(kwargs)
        arcgis_chart_proto.config = json.dumps(config)

        # Compute the element id for state persistence
        # when the frontend component gets unmounted and remounted.
        arcgis_chart_proto.id = compute_and_register_element_id(
            "arcgis_chart",
            form_id=None,
            user_key=key,
            dg=self.dg,
            arcgis_spec=arcgis_chart_proto.spec,
            arcgis_config=arcgis_chart_proto.config,
            height=height,
        )

        return self.dg._enqueue("arcgis_chart", arcgis_chart_proto)

    @property
    def dg(self) -> DeltaGenerator:
        """Get our DeltaGenerator."""
        return cast("DeltaGenerator", self)
