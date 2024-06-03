from ...nodes import Tag
from ...__extensions__.toggle.core import Toggle


class Div(Tag, Toggle):
    def __init__(self, senior, text=None):
        super().__init__(senior, 'div')
        self.add_junior(text)
