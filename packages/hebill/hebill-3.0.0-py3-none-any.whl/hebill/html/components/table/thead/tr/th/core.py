from ......tags.th.core import Th as ThParentClass


class Th(ThParentClass):
    def set_active(self):
        self.attributes.classes.append('table-active')
