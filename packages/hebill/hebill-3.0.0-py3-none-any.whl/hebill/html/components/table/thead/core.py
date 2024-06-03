from ....tags.thead.core import Thead as TheadParentClass
from .tr.core import Tr


class Thead(TheadParentClass):
    def __init__(self, senior):
        super().__init__(senior)
        self._rows = []
        self._row = None

        self._style = None

    @property
    def rows(self) -> list:
        return self._rows

    @property
    def row(self) -> Tr:
        if self._row is None:
            self.add_row()
        return self._row

    @property
    def cells(self): return self.row.cells

    @property
    def cell(self): return self.row.cell

    def add_cell(self, text=None): return self.row.add_cell(text)

    def add_row(self, data: list = None) -> Tr:
        self._row = Tr(self)
        self._rows.append(self._row)
        if data:
            for d in data:
                self.row.add_cell(d)
        return self._row

    @property
    def color(self):
        if self._style is None:
            from ..__templates__.color import Color
            self._style = Color(self)
        return self._style
