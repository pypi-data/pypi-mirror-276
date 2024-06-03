from ...nodes import Tag


class H3(Tag):
    def __init__(self, senior, text=None):
        super().__init__(senior, 'h3')
        self.add_junior(text)
