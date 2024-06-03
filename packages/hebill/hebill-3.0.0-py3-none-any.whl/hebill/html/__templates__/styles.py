class Styles:
    def __init__(self, senior, styles: list):
        self._senior = senior
        self._styles = styles

    def set(self, style: str | int) -> bool:
        if isinstance(style, int):
            if not 0 <= style < len(self._styles):
                return False
            style = self._styles[style]
        if style not in self._styles:
            return False
        self._senior.attributes.classes.unset(self._styles)
        return self._senior.attributes.classes.set(style)
