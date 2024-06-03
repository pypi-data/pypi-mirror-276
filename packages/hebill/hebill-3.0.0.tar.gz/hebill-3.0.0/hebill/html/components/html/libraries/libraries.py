

class Libraries:
    def __init__(self, htm):
        from ....components.html.core import Html
        self._htm: Html = htm
        self._files = []

    def add_link_js(self, url):
        if url not in self._files:
            self._files.append(url)
        pass

    def add_link_css(self, url):
        if url not in self._files:
            self._files.append(url)
        pass

    def add_meta(self):
        pass

