from __future__ import annotations

import random
from typing import Any, Callable

from gradio_client.documentation import document

from gradio.components.base import FormComponent
from gradio.events import Events


class CategoricalSlider(FormComponent):
    """
    Creates a slider that uses categories with associated values.
    """

    EVENTS = [Events.change, Events.input, Events.release]

    def __init__(
        self,
        categories: list[tuple[str, Any]] = [],
        value: float | Callable | None = None,
        *,
        label: str | None = None,
        info: str | None = None,
        every: float | None = None,
        show_label: bool | None = None,
        container: bool = True,
        scale: int | None = None,
        min_width: int = 160,
        interactive: bool | None = True,
        visible: bool = True,
        elem_id: str | None = None,
        elem_classes: list[str] | str | None = None,
        render: bool = True,
        key: int | str | None = None,
        randomize: bool = False,
    ):
        """
        Parameters:
            categories: List of tuples containing category and value.
            value: default value. If callable, the function will be called whenever the app loads to set the initial value of the component. Ignored if randomized=True.
            label: The label for this component. Appears above the component and is also used as the header if there are a table of examples for this component. If None and used in a `gr.Interface`, the label will be the name of the parameter this component is assigned to.
            info: additional component description.
            every: If `value` is a callable, run the function 'every' number of seconds while the client connection is open. Has no effect otherwise. The event can be accessed (e.g. to cancel it) via this component's .load_event attribute.
            show_label: if True, will display label.
            container: If True, will place the component in a container - providing some extra padding around the border.
            scale: relative size compared to adjacent Components. For example if Components A and B are in a Row, and A has scale=2, and B has scale=1, A will be twice as wide as B. Should be an integer. scale applies in Rows, and to top-level Components in Blocks where fill_height=True.
            min_width: minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain scale value results in this Component being narrower than min_width, the min_width parameter will be respected first.
            interactive: if True, slider will be adjustable; if False, adjusting will be disabled. If not provided, this is inferred based on whether the component is used as an input or output.
            visible: If False, component will be hidden.
            elem_id: An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.
            elem_classes: An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.
            render: If False, component will not render be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.
            key: if assigned, will be used to assume identity across a re-render. Components that have the same key across a re-render will have their value preserved.
            randomize: If True, the value of the slider when the app loads is taken uniformly at random from the list of categories.
        """
        self.categories = categories
        if randomize:
            value = self.get_random_value

        assert len(categories) > 0, "Categories must have at least one element."
        assert all(
            len(cat) == 2 for cat in categories
        ), "Each category must be a tuple of length 2."

        if value is None:
            value = categories[0][1]
        else:
            assert value in [cat[1] for cat in categories], "Value must be in category values."

        super().__init__(
            label=label,
            info=info,
            every=every,
            show_label=show_label,
            container=container,
            scale=scale,
            min_width=min_width,
            interactive=interactive,
            visible=visible,
            elem_id=elem_id,
            elem_classes=elem_classes,
            render=render,
            key=key,
            value=value,
        )

    def api_info(self) -> dict[str, Any]:
        return {
            "type": "number",
            "description": f"categorical value from {self.categories}",
        }

    def example_payload(self) -> Any:
        return self.categories[0][1]

    def example_value(self) -> Any:
        return self.categories[0][1]

    def get_random_value(self):
        return random.choice(self.categories)[1]

    def postprocess(self, value: float | None) -> float:
        """
        Parameters:
            value: Expects a float or None returned from function and sets slider value to it as long as it is within the category values.
        Returns:
            The value of the slider within the category values.
        """
        category_values = [cat[1] for cat in self.categories]
        return category_values[0][1] if value not in category_values else value

    def preprocess(self, payload: str) -> str:
        """
        Parameters:
            payload: slider category
        Returns:
            Passes slider category as a str into the function.
        """
        return payload
