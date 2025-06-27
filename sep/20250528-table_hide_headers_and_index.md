## Summary

This proposal suggests adding `hide_headers` and `hide_index` parameters to the `st.table` command to allow developers to hide the table's column headers and/or index column.

## Motivation

The `st.table` command is designed for displaying **small, static tables**. It is often used for simple visualisations like confusion matrices or leaderboards. Developers may wish to hide the column headers or the index column to achieve a more compact visual display or when integrating the table into a dashboard or report where column labels or index information is provided elsewhere in the app. The `st.dataframe` and `st.data_editor` commands already support a `hide_index` parameter, so adding a similar option to `st.table` would provide some **consistency** and offer finer control for these smaller, static table use cases.

## Proposal

Add two new optional boolean parameters to the `st.table` command signature:
`st.table(data=None, hide_headers=False, hide_index=False)`

* **`hide_headers: bool = False`** [Proposed]: If set to `True`, the row containing the column headers will not be displayed.
* **`hide_index: bool = False`** [Proposed, analogous to `st.dataframe`/`st.data_editor`]: If set to `True`, the index column of the table will not be displayed.

Both parameters should default to `False` to maintain the current default behavior of showing headers and the index.

## Alternatives

* **Pre-process the data:** Developers can already achieve a similar effect by modifying the input data (e.g., removing the index in pandas) before passing it to `st.table`. To hide headers, one could potentially add a dummy row before the actual data and remove the original headers. However, this approach requires data manipulation outside of Streamlit's display functions and can be less intuitive and maintainable than a dedicated display parameter.
* **Custom CSS/HTML:** Users could potentially use `st.markdown(..., unsafe_allow_html=True)` or `st.html` to try and hide parts of the rendered table using CSS. This is discouraged due to safety, styling, and maintainability concerns. The proposed parameters offer a simple, officially supported method.

## Unresolved questions

None immediately apparent.

## Checklist

*Provide more information in case any of the items cannot be checked*

* [X] Backwards compatible - Adding new parameters with default values does not change the behavior for existing apps.
* [X] No new frontend dependencies - Hiding existing rendered elements should not require new dependencies.
* [X] No new backend dependencies - Hiding existing rendered elements should not require new dependencies.
* [X] No known risks or drawbacks - Risks appear minimal. The primary drawback might be reduced discoverability compared to data pre-processing, but the feature serves a common UI need directly.
