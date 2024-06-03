from ...nodes import Tag


class Body(Tag):
    def __init__(self, senior, text=None):
        super().__init__(senior, 'body')
        self.add_junior(text)
