from ...tags import Nav


class Navbar(Nav):
    def __init__(self, senior):
        super().__init__(senior)
        self.attributes.classes.set('navbar')
        self._div = self.create.tag.div()
        self._div.attributes.classes.set('container-fluid')
        self._brand_wrap = self._div.create.node.group()
        self._brand = None
        btn = self._div.create.tag.div()
        btn.attributes.classes.set('navbar-toggler')
        btn.attributes.set('tyre', 'button')
        btn.attributes.set('data-bs-toggle', 'collapse')

    @property
    def brand(self): return self._brand

    @brand.setter
    def brand(self, text: str): self._brand = text

    def output(self):
        if self.brand:
            pass
        super().output()
