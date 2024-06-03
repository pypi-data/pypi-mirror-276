from ...nodes import Tag


class Html(Tag):
    def __init__(self, senior, lang: str = None):
        super().__init__(senior, 'html')
        if lang is not None:
            self.attributes["lang"] = lang

    def set_attribute_lang(self, lang: str):
        self.attributes["lang"] = lang
