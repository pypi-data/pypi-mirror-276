from ...tags.table.core import Table as TableParentClass
from .thead.core import Thead
from .tbody.core import Tbody


class Table(TableParentClass):
    def __init__(self, senior):
        super().__init__(senior)
        self._head_wrap = self.create.node.group()
        self._head = None
        self._body = None
        self.attributes.classes.set('table')

        self._style = None

    @property
    def head(self) -> Thead:
        if self._head is None:
            self._head = Thead(self._head_wrap)
        return self._head

    @property
    def head_rows(self): return self.head.rows

    @property
    def head_row(self): return self.head.row

    def add_head_row(self, data: list = None): return self.head.add_row(data)

    @property
    def head_cells(self): return self.head.cells

    @property
    def head_cell(self): return self.head.cell

    def add_head_cell(self, text=None): return self.head.add_cell(text)

    @property
    def body(self) -> Tbody:
        if self._body is None:
            self._body = Tbody(self)
        return self._body

    @property
    def body_rows(self): return self.body.rows

    @property
    def body_row(self): return self.body.row

    def add_body_row(self, data: list = None): return self.body.add_row(data)

    @property
    def body_cells(self): return self.body.cells

    @property
    def body_cell(self): return self.body.cell

    def add_body_cell(self, text=None): return self.body.add_cell(text)

    @property
    def color(self):
        if self._style is None:
            from .__templates__.color import Color
            self._style = Color(self)
        return self._style

    def set_striped(self):
        return self.attributes.classes.set('table-striped')

    def set_striped_columns(self):
        return self.attributes.classes.set('table-striped-columns')

    def set_hover(self):
        return self.attributes.classes.set('table-hover')

    def set_bordered(self):
        self.attributes.classes.unset('table-borderless')
        return self.attributes.classes.set('table-bordered')

    def set_borderless(self):
        self.attributes.classes.unset('table-bordered')
        return self.attributes.classes.set('table-borderless')

    def set_small(self):
        return self.attributes.classes.set('table-sm')
