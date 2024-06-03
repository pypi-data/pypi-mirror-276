from ....html.tags import Nav, A


class Breadcrumb(Nav):
    def __init__(self, senior):
        super().__init__(senior)
        self.attributes.set('aria-label', 'breadcrumb')
        self._ol = self.create.tag.ol()
        self._ol.attributes.classes.set('breadcrumb')

    def add_item(self, title=None, url=None, active=False):
        li = self._ol.create.tag.li()
        li.attributes.classes.set('breadcrumb-item')
        if not active:
            li.create.tag.a(title, url)
        else:
            li.create.node.content(title)
            li.attributes.classes.set('active')
            li.attributes.set('aria-current', 'page')

    def set_divider(self, divider: str):
        self.attributes.styles.set('--bs-breadcrumb-divider', f'\'{divider}\'')
