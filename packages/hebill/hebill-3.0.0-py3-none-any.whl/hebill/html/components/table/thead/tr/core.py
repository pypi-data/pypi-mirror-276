from .....tags.tr.core import Tr as TrParentClass
from .th.core import Th


class Tr(TrParentClass):
    def __init__(self, senior):
        super().__init__(senior)
        self._cells = []
        self._cell = None

        self._style = None

    @property
    def cells(self) -> list:
        return self._cells

    @property
    def cell(self) -> Th:
        if self._cell is None:
            self.add_cell()
        return self._cell

    def add_cell(self, text=None) -> Th:
        self._cell = Th(self, text)
        self._cells.append(self._cell)
        return self._cell

    @property
    def color(self):
        if self._style is None:
            from ...__templates__.color import Color
            self._style = Color(self)
        return self._style

    def set_active(self):
        self.attributes.classes.append('table-active')
