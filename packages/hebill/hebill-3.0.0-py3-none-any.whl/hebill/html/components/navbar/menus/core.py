from ....tags import Ul


class Navbar(Ul):
    def __init__(self, senior):
        super().__init__(senior)
        self.attributes.classes.set('navbar')
        self._div = self.create.tag.div()
        self._div.attributes.classes.set('container-fluid')
        self._brand_wrap = self._div.create.node.group()
        self._brand = None