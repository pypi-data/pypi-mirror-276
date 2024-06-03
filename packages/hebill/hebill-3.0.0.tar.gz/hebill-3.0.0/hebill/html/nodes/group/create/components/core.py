class Components:
    def __init__(self, sir):
        self.senior = sir

    def alert(self, text):
        from .....components import Alert
        return Alert(self.senior, text)

    def breadcrumb(self):
        from .....components import Breadcrumb
        return Breadcrumb(self.senior)

    def button(self, text):
        from .....components import Button
        return Button(self.senior, text)

    def container(self):
        from .....components import Container
        return Container(self.senior)

    def pagination(self):
        from .....components import Pagination
        return Pagination(self.senior)

    def table(self):
        from .....components import Table
        return Table(self.senior)
