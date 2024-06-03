from ...nodes import Tag


class H4(Tag):
    def __init__(self, senior, text=None):
        super().__init__(senior, 'h4')
        self.add_junior(text)
