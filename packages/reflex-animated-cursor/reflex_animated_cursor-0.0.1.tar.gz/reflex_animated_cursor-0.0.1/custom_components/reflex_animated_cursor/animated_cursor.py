"""Reflex custom component AnimatedCursor."""

# For wrapping react guide, visit https://reflex.dev/docs/wrapping-react/overview/

import reflex as rx

# Some libraries you want to wrap may require dynamic imports.
# This is because they they may not be compatible with Server-Side Rendering (SSR).
# To handle this in Reflex, all you need to do is subclass `NoSSRComponent` instead.
# For example:
# from reflex.components.component import NoSSRComponent
# class AnimatedCursor(NoSSRComponent):
#     pass


class AnimatedCursor(rx.Component):
    """AnimatedCursor component."""

    # The React library to wrap.
    library = "react-animated-cursor"
    is_default = True
    # The React component tag.
    tag = "AnimatedCursor"

    # The props of the React component.
    color: rx.Var[str] = "110, 224, 194" # RGB
    inner_scale: rx.Var[float] = 1
    outer_scale: rx.Var[float] = 2
    outer_alpha: rx.Var[float] = 0
    inner_size: rx.Var[int] = 8
    outer_size: rx.Var[int] = 35
    inner_style: rx.Var[dict] = {'background_color': 'transparent'}
    outer_style: rx.Var[dict] = {'border': '3px solid #FFC145'}
    clickables: rx.Var[list] = [
        'a',
        'input[type="text"]',
        'input[type="email"]',
        'input[type="number"]',
        'input[type="submit"]',
        'input[type="image"]',
        'label[for]',
        'select',
        'textarea',
        'button',
        '.link'
    ]
    show_system_cursor: rx.Var[bool] = False
    trailing_speed: rx.Var[int] = 8

    # Additional libraries required for the component.
    lib_dependencies: list[str] = ["react-animated-cursor"]

    # To add custom code to your component.
    def _get_custom_code(self) -> str:
        return """
            // Custom client-side JavaScript if needed
        """
    
animated_cursor = AnimatedCursor.create