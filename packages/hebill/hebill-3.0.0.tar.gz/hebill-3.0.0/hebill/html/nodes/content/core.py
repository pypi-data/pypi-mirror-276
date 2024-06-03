from ..node.core import Node


class Content(Node):
    def __init__(self, sir, text: str = None):
        super().__init__(sir)
        self._text = text if text is not None else ''

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text

    def output(self):
        self.document.output_next_breakable = False
        return self.text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
