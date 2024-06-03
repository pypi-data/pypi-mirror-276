from .color import Color


class ColorBack(Color):
    @property
    def color(self):
        return Color(self._terminal)
    