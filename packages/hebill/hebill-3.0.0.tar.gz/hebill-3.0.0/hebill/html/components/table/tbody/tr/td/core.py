from ......tags.td.core import Td as TdParentClass


class Td(TdParentClass):
    def set_active(self):
        self.attributes.classes.append('table-active')
