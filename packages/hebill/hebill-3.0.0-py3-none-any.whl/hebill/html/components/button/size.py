from ...__templates__.styles import Styles


class Size(Styles):
    def __init__(self, senior):
        super().__init__(senior, [
            'btn-sm',
            'btn-lg',
        ])

    def set_small(self): return self.set('btn-sm')

    def set_large(self): return self.set('btn-lg')
