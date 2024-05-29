from __future__ import annotations

import warnings
from typing import Literal, overload

from shiny import App, Inputs, Outputs, Session, ui
from shiny._deprecated import ShinyDeprecationWarning
from shiny.render.transformer import (
    TransformerMetadata,
    ValueFn,
    output_transformer,
    resolve_value_fn,
)

warnings.filterwarnings("ignore", category=ShinyDeprecationWarning)

#######
# Package authors can create their own output transformer methods by leveraging
# `output_transformer` decorator.
#
# The transformer is kept simple for demonstration purposes, but it can be much more
# complex (e.g. shiny.render.plotly)
#######


@output_transformer()
async def CapitalizeTransformer(
    # Contains information about the render call: `name` and `session`
    _meta: TransformerMetadata,
    # The app-supplied output value function
    _fn: ValueFn[str | None],
    *,
    # Extra parameters that app authors can supply to the render decorator
    # (e.g. `@render_capitalize(to="upper")`)
    to: Literal["upper", "lower"] = "upper",
) -> str | None:
    # Get the value
    value = await resolve_value_fn(_fn)
    # Equvalent to:
    # if shiny.render.transformer.is_async_callable(_fn):
    #     value = await _fn()
    # else:
    #     value = _fn()

    # Render nothing if `value` is `None`
    if value is None:
        return None

    if to == "upper":
        return value.upper()
    if to == "lower":
        return value.lower()
    raise ValueError(f"Invalid value for `to`: {to}")


# First, create an overload where users can supply the extra parameters.
# Example of usage:
# ```
# @render_capitalize(to="upper")
# def value():
#     return input.caption()
# ```
# Note: Return type is `OutputRendererDecorator`
@overload
def render_capitalize(
    *,
    to: Literal["upper", "lower"] = "upper",
) -> CapitalizeTransformer.OutputRendererDecorator: ...


# Second, create an overload where users are not using parentheses to the method.
# While it doesn't look necessary, it is needed for the type checker.
# Example of usage:
# ```
# @render_capitalize
# def value():
#     return input.caption()
# ```
# Note: `_fn` type is the transformer's `ValueFn`
# Note: Return type is the transformer's `OutputRenderer`
@overload
def render_capitalize(
    _fn: CapitalizeTransformer.ValueFn,
) -> CapitalizeTransformer.OutputRenderer: ...


# Lastly, implement the renderer.
# Note: `_fn` type is the transformer's `ValueFn` or `None`
# Note: Return type is the transformer's `OutputRenderer` or `OutputRendererDecorator`
def render_capitalize(
    _fn: CapitalizeTransformer.ValueFn | None = None,
    *,
    to: Literal["upper", "lower"] = "upper",
) -> (
    CapitalizeTransformer.OutputRenderer | CapitalizeTransformer.OutputRendererDecorator
):
    return CapitalizeTransformer(
        _fn,
        CapitalizeTransformer.params(to=to),
    )


#######
# End of package author code
#######

app_ui = ui.page_fluid(
    ui.h1("Capitalization renderer"),
    ui.input_text("caption", "Caption:", "Data summary"),
    "Renderer called with out parentheses:",
    ui.output_text_verbatim("no_output", placeholder=True),
    ui.output_text_verbatim("no_parens", placeholder=True),
    "To upper:",
    ui.output_text_verbatim("to_upper", placeholder=True),
    "To lower:",
    ui.output_text_verbatim("to_lower", placeholder=True),
)


def server(input: Inputs, output: Outputs, session: Session):
    # Without parentheses
    @render_capitalize
    def no_output():
        return input.caption()

    @output
    # Without parentheses
    @render_capitalize
    def no_parens():
        return input.caption()

    # @output # Do not include to make sure auto registration works
    # With parentheses. Equivalent to `@render_capitalize()`
    @render_capitalize(to="upper")
    def to_upper():
        return input.caption()

    # provide a custom name to make sure the name can be overridden
    @output(id="to_lower")
    @render_capitalize(to="lower")
    # Works with async output value functions
    async def _():
        return input.caption()


app = App(app_ui, server)
