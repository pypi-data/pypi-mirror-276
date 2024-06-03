from ...__templates__.styles import Styles


class Color(Styles):
    def __init__(self, senior):
        super().__init__(senior, [
            'btn-outline-primary',
            'btn-outline-secondary',
            'btn-outline-success',
            'btn-outline-danger',
            'btn-outline-warning',
            'btn-outline-info',
            'btn-outline-light',
            'btn-outline-dark',
        ])

    def set_primary(self): return self.set('btn-outline-primary')

    def set_secondary(self): return self.set('btn-outline-secondary')

    def set_success(self): return self.set('btn-outline-success')

    def set_danger(self): return self.set('btn-outline-danger')

    def set_warning(self): return self.set('btn-outline-warning')

    def set_info(self): return self.set('btn-outline-info')

    def set_light(self): return self.set('btn-outline-light')

    def set_dark(self): return self.set('btn-outline-dark')
