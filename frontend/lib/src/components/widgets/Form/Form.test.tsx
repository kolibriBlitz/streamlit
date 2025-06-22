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

import React from "react"

import { screen } from "@testing-library/react"

import { renderWithContexts } from "~lib/test_util"
import {
  createFormsData,
  FormsData,
  WidgetStateManager,
} from "~lib/WidgetStateManager"

import Form, { Props } from "./Form"

describe("Form", () => {
  function getProps(props: Partial<Props> = {}): Props {
    return {
      formId: "mockFormId",
      scriptNotRunning: false,
      clearOnSubmit: false,
      enterToSubmit: true,
      widgetMgr: new WidgetStateManager({
        sendRerunBackMsg: vi.fn(),
        formsDataChanged: vi.fn(),
      }),
      border: false,
      ...props,
    }
  }

  const defaultFormsData = (
    formsDataOverrides: Partial<FormsData> = {}
  ): FormsData => {
    return {
      ...createFormsData(),
      ...formsDataOverrides,
    }
  }

  it("renders without crashing", () => {
    renderWithContexts(
      <Form {...getProps()} />,
      {},
      {
        formsData: defaultFormsData(),
      }
    )
    const formElement = screen.getByTestId("stForm")
    expect(formElement).toBeInTheDocument()
    expect(formElement).toHaveClass("stForm")
  })

  it("shows error if !hasSubmitButton && scriptRunState==NOT_RUNNING", () => {
    const props = getProps()
    const { rerender, unmount } = renderWithContexts(
      <Form {...props} />,
      {},
      {
        // default formsData has no submit buttons
        formsData: defaultFormsData(),
      }
    )

    // We have no Submit Button, but the app is still running
    expect(screen.queryByTestId("stFormSubmitButton")).not.toBeInTheDocument()

    // When the app stops running, we show an error if the submit button
    // is still missing.
    rerender(<Form {...getProps({ scriptNotRunning: true })} />)
    expect(screen.getByText("Missing Submit Button")).toBeInTheDocument()

    // If the app restarts, we continue to show the error...
    rerender(<Form {...getProps({ scriptNotRunning: false })} />)
    expect(screen.getByText("Missing Submit Button")).toBeInTheDocument()

    // Until we get a submit button, and the error is removed immediately,
    // regardless of ScriptRunState.
    // Need to unmount first and render with a new context since rerender doesn't update contexts
    unmount()
    renderWithContexts(
      <Form {...getProps()} />,
      {},
      {
        formsData: defaultFormsData(),
      }
    )
    expect(screen.getByTestId("stForm")).toBeInTheDocument()
    expect(screen.queryByText("Missing Submit Button")).not.toBeInTheDocument()
  })
})
