# animated-cursor

A Reflex custom component animated-cursor.

## Installation

```bash
pip install reflex-animated-cursor
```

- **`color`**: `str` - RGB value for the cursor color.
- **`inner_scale`**: `float` - Scale factor for the inner cursor.
- **`outer_scale`**: `float` - Scale factor for the outer cursor.
- **`outer_alpha`**: `float` - Alpha transparency for the outer cursor.
- **`inner_size`**: `int` - Size (px) of the inner cursor dot.
- **`outer_size`**: `int` - Size (px) of the outer cursor outline.
- **`inner_style`**: `dict` - Custom styles for the inner cursor.
- **`outer_style`**: `dict` - Custom styles for the outer cursor.
- **`clickables`**: `list` - Collection of selectors that trigger cursor interaction.
- **`show_system_cursor`**: `bool` - Show or hide the system cursor.
- **`trailing_speed`**: `int` - Speed of the outer cursor's trailing animation.
