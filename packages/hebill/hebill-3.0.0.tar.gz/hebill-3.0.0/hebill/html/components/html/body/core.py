from ....tags.body.core import Body as BodyParentClass


class Body(BodyParentClass):
    def __init__(self, senior):
        super().__init__(senior)
        self._top = self.create.node.group()
        self._upper = self.create.node.group()
        self._middle = self.create.node.group()
        self._lower = self.create.node.group()
        self._footer = self.create.node.group()
        self._bottom = self.create.node.group()
        self._libraries = self.create.node.group()

    @property
    def top(self):
        return self._top

    @property
    def upper(self):
        return self._upper

    @property
    def middle(self):
        return self._middle

    @property
    def lower(self):
        return self._lower

    @property
    def footer(self):
        return self._footer

    @property
    def bottom(self):
        return self._bottom

    @property
    def libraries(self):
        return self._libraries
