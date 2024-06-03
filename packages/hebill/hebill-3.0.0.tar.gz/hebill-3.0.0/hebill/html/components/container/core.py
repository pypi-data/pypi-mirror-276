from ...tags.div.core import Div


class Container(Div):
    def __init__(self, senior):
        super().__init__(senior)
        self.attributes.classes.set("container")
        self._size = None

    @property
    def size(self):
        if self._size is None:
            from .size import Size
            self._size = Size(self)
        return self._size
