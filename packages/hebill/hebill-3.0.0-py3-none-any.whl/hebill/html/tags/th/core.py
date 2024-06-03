from ...nodes import Tag


class Th(Tag):
    def __init__(self, senior, text=None):
        super().__init__(senior, 'th')
        self.add_junior(text)
        