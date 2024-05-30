# pgpyui 0.1.1

pgpyui is an add-on module for pygame to create a user interface.

## Installation

```
pip install pgpyui
```

## Usage

### Button

Imports
```python
from pgpyui import button
import pygame
```

Creating a button
```python
button = button.Button((100, 100), (200, 100), "Some text", func, sprites=["sprites/sprite1.png", "sprites/sprite2.png"])
```

Event handling
```python
button.check_events(event)
```

Drawing
```python
button.draw(window)
```
#
### Text Area

Imports
```python
from pgpyui import textarea
import pygame
```

Creating a text area
```python
textarea = textarea.TextArea((200, 100), (100, 100), 20, 15, is_enter=False, font="Arial")
```

Event handling
```python
textarea.check_events(event)
```

Drawing
```python
textarea.draw(window)
```

Information output
```python
text: list[str] = textarea.data_return()
```

#
### Slider

Imports
```python
from pgpyui import slider
import pygame
```

Creating a slider
```python
slider = slider.Slider((200, 100), (100, 100), 100, orientation="True")
```

Event handling
```python
slider.check_events(event)
```

Drawing
```python
slider.draw(window)
```

Information output
```python
prgrs: int = slider.data_return()
```

#
### CheckBox

Imports
```python
from pgpyui import checkbox
import pygame
```

Creating a checkbox
```python
chkbox = checkbox.CheckBox((100, 100), (50, 50), 3, 75, color=(0, 0, 0), ["passive.png", "active.png"])
```

Event handling
```python
chkbox.check_events(event)
```

Drawing
```python
chkbox.draw(window)
```

Information output
```python
prgrs: list = chkbox.data_return()
```

#
### Radio-button

Imports
```python
from pgpyui import radio
import pygame
```

Creating a radio-button
```python
radiob = radio.Radio((100, 100), 25, 10, 100)
```

Event handling
```python
radiob.check_events(event)
```

Drawing
```python
radiob.draw(window)
```

Information output
```python
rt: list = radiob.data_return()
```

## Documentation

### Button

**Parameters:**

* `position`: The position of the button.
* `size`: The size of the button.
* `text`: The text on the button.
* `function`: The function to be called when the button is clicked.
* `sprite`: A sprite to use for the button (optional).

### TextArea

**Parameters:**

* `position`: The position of the text area.
* `size`: The size of the text area.
* `font_size`: The size of the font.
* `max_symbols`: The maximum number of symbols that can be entered.
* `is_enter`: Whether or not the enter key should be allowed.
* `font`: The name of the font to use (optional).

### Slider

**Parameters:**

* `position`: The position of the slider.
* `size_block`: The size of the block slider.
* `len`: Length of slide.
* `max_symbols`: The maximum number of symbols that can be entered.
* `orientation`: Horisontal or vertical slider. (optional)

### CheckBox

**Parameters:**

* `position`: The position of the CheckBox.
* `size`: The size of the block Checkbox.
* `num_boxes`: The num of CheckBoxes.
* `step`: The distance between the boxes.
* `color`: Color of the box. (optional)
* `sprites`: Two sprites - the first without a check mark, the second with a check mark. (optional)

### Radio-button

**Parameters:**

* `position`: The position of the radio-button.
* `radius`: Radius of radio-button.
* `num_rb`: The num of radio-buttons.
* `step`: The distance between the buttons.
* `color`: Color of the box. (optional)


## License

MIT

## Author mail

mixail.vilyukov@icloud.com
