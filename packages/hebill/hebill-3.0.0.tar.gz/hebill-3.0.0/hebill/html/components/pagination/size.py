from ...__templates__.styles import Styles


class Size(Styles):
    def __init__(self, senior):
        super().__init__(senior, [
            'pagination-lg',
            'pagination-sm',
        ])

    def set_large(self): return self.set('pagination-lg')

    def set_small(self): return self.set('pagination-sm')
