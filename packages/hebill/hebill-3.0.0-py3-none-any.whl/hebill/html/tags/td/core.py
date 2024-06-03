from ...nodes import Tag


class Td(Tag):
    def __init__(self, senior, text=None):
        super().__init__(senior, 'td')
        self.add_junior(text)
        