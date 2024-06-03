from ...nodes import Tag


class Meta(Tag):
    def __init__(self, senior):
        super().__init__(senior, 'meta')
        self.output_paired = False

    def set_attribute_charset(self, charset):
        self.attributes['charset'] = charset

    def set_attribute_name(self, name):
        self.attributes['name'] = name

    def set_attribute_content(self, content):
        self.attributes['content'] = content
