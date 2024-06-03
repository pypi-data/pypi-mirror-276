from ...nodes import Tag
from ...__extensions__.toggle.core import Toggle


class Button(Tag, Toggle):
    def __init__(self, senior, text=None):
        super().__init__(senior, 'button')
        self.add_junior(text)
