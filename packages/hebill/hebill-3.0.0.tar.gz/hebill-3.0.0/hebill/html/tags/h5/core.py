from ...nodes import Tag


class H5(Tag):
    def __init__(self, senior, text=None):
        super().__init__(senior, 'h5')
        self.add_junior(text)
