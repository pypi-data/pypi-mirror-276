from ...__templates__.styles import Styles


class Size(Styles):
    def __init__(self, senior):
        super().__init__(senior, [
            'container',
            'container-sm',
            'container-md',
            'container-lg',
            'container-xl',
            'container-xxl',
            'container-fluid',
        ])

    def set_container(self): return self.set('container')

    def set_container_small(self): return self.set('container-sm')

    def set_container_middle(self): return self.set('container-md')

    def set_container_large(self): return self.set('container-lg')

    def set_container_x_large(self): return self.set('container-xl')

    def set_container_xx_large(self): return self.set('container-xxl')

    def set_container_fluid(self): return self.set('container-fluid')
