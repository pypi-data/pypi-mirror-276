from ...nodes import Tag


class H2(Tag):
    def __init__(self, senior, text=None):
        super().__init__(senior, 'h2')
        self.add_junior(text)
