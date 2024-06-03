from .color import Color


class ColorFore(Color):
    @property
    def background(self):
        return Color(self._terminal, False)
