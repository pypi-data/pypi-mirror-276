from ...tags.button.core import Button as ButtonTag


class Button(ButtonTag):
    def __init__(self, senior, text=None):
        super().__init__(senior, text)
        self.attributes.classes.set("btn")
        self._color = None
        self._color_outline = None
        self._size = None

    @property
    def color(self):
        if self._color is None:
            from .color import Color
            self._color = Color(self)
        return self._color

    @property
    def color_outline(self):
        if self._color_outline is None:
            from .color_outline import Color
            self._color_outline = Color(self)
        return self._color_outline

    @property
    def size(self):
        if self._size is None:
            from .size import Size
            self._size = Size(self)
        return self._size
