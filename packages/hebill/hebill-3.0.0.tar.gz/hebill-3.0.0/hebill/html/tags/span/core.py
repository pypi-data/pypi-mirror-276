from ...nodes import Tag
from ...__extensions__.toggle.core import Toggle


class Span(Tag, Toggle):
    def __init__(self, senior, text=None):
        super().__init__(senior, 'span')
        self.add_junior(text)
