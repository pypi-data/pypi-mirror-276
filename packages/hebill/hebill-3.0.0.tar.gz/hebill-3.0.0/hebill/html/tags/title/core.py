from ...nodes import Tag


class Title(Tag):
    def __init__(self, senior, text: str = None):
        super().__init__(senior, 'title')
        self.output_break_inner = False
        self._content = self.create.node.content()
        self.add_junior(text)

    @property
    def content(self):
        return self._content.text

    @content.setter
    def content(self, content):
        self._content.text = content
