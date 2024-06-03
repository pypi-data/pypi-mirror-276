from ...nodes import Tag


class H6(Tag):
    def __init__(self, senior, text=None):
        super().__init__(senior, 'h6')
        self.add_junior(text)
