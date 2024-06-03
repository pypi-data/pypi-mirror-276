from ...tags import Html as HtmlParentClass
from .head.core import Head
from .body.core import Body


class Html(HtmlParentClass):
    def __init__(self, senior, title: str = 'Untitled', lang: str = None):
        super().__init__(senior, lang)
        self._head = Head(self)
        self._body = Body(self)
        self._library_files = []
        self.title = title
        self.add_meta().set_attribute_charset('utf-8')
        css = self.add_head_css_link('https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css')
        css.attributes.set('rel', 'stylesheet')
        css.attributes.set('integrity', 'sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH')
        css.attributes.set('crossorigin', 'anonymous')
        css = self.add_head_css_link('https://cdn.jsdelivr.net/gh/hebill/hebill_lib/hebill.css')
        # css = self.add_head_css_link('https://cdn.jsdelivr.net/gh/hebill/hebill_lib/hebill.css')
        css.attributes.set('rel', 'stylesheet')
        # css.attributes.set('integrity', 'sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH')
        # https://cdn.jsdelivr.net/gh/hebill/hebill_lib@releases/tag/1.0.0
        css.attributes.set('crossorigin', 'anonymous')
        js = self.add_library_js_link_to_body(
            'https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js')
        js.attributes.set('integrity', 'sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz')
        js.attributes.set('crossorigin', 'anonymous')

    @property
    def head(self):
        return self._head

    @property
    def title(self):
        return self.head.title

    @title.setter
    def title(self, title):
        self.head.title = title

    @property
    def body(self):
        return self._body

    ##################################################
    @property
    def library_files(self):
        return self._library_files

    def is_library_file_added(self, url):
        return url in self._library_files

    def add_library_js_link_to_head(self, url):
        if self.is_library_file_added(url):
            return True
        self._library_files.append(url)
        return self.head.libraries.create.tag.script(url)

    def add_library_js_link_to_body(self, url):
        if self.is_library_file_added(url):
            return True
        self._library_files.append(url)
        return self.body.libraries.create.tag.script(url)

    def add_head_css_link(self, url):
        if self.is_library_file_added(url):
            return True
        self._library_files.append(url)
        return self.head.libraries.create.tag.link(url)

    def add_meta(self):
        return self.head.libraries.create.tag.meta()
