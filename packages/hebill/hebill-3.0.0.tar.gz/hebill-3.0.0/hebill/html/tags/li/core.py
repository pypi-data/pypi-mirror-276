from ...nodes import Tag


class Li(Tag):
    def __init__(self, senior, text=None):
        super().__init__(senior, 'li')
        self.add_junior(text)
