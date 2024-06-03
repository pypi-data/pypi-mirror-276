from ...tags import Nav


class Pagination(Nav):
    def __init__(self, senior):
        super().__init__(senior)
        self.attributes.set('aria-label', 'pagination')
        self._ul = self.create.tag.ul()
        self._ul.attributes.classes.set('pagination')
        self._size = None

    def add_item(self, title=None, url=None, active=False):
        li = self._ul.create.tag.li()
        li.attributes.classes.set('page-item')
        a = li.create.tag.a(title, url)
        a.attributes.classes.set('page-link')
        if active:
            li.attributes.classes.set('active')
            li.attributes.set('aria-current', 'page')
        return self

    @property
    def size(self):
        if self._size is None:
            from .size import Size
            self._size = Size(self._ul)
        return self._size
