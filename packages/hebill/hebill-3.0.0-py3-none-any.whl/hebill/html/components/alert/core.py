from ...tags.div.core import Div


class Alert(Div):
    def __init__(self, senior, text=None):
        super().__init__(senior, text)
        self.attributes.classes.set('alert')

        self._color = None

    @property
    def color(self):
        if self._color is None:
            from .color import Color
            self._color = Color(self)
        return self._color
