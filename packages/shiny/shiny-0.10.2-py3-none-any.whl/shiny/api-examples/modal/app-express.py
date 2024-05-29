from shiny import reactive
from shiny.express import input, ui

ui.input_action_button("show", "Show modal dialog")


@reactive.effect
@reactive.event(input.show)
def _():
    m = ui.modal(
        "This is a somewhat important message.",
        title="Somewhat important message",
        easy_close=True,
        footer=None,
    )
    ui.modal_show(m)
