from ..node.core import Node


class Group(Node):
    def __init__(self, sir):
        super().__init__(sir)
        self._juniors = {}
        self._create = None

    @property
    def juniors(self): return self._juniors

    def add_junior(self, jun=None):
        if jun is None:
            return False
        if isinstance(jun, str):
            return self.create.node.content(jun)
        if isinstance(jun, Node):
            jun.local_change_senior(self)
            self._juniors[jun.id] = jun
            return True
        return self.create.node.content(str(jun))

    def local_add_junior(self, jun: Node):
        self._juniors[jun.id] = jun

    def local_remove_junior(self, jun):
        if jun.id in self._juniors.keys():
            del self._juniors[jun.id]

    def has_juniors(self): return len(self._juniors) > 0

    @property
    def create(self):
        if self._create is None:
            from .create.core import Create
            self._create = Create(self)
        return self._create

    def output(self):
        s = ""
        if self.has_juniors():
            for key, value in self.juniors.items():
                s += value.output()
        return s
