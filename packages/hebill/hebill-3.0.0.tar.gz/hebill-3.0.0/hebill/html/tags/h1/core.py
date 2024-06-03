from ...nodes import Tag


class H1(Tag):
    def __init__(self, senior, text=None):
        super().__init__(senior, 'h1')
        self.add_junior(text)
