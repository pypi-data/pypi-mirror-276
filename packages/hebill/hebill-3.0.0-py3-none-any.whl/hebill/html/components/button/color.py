from ...__templates__.styles import Styles


class Color(Styles):
    def __init__(self, senior):
        super().__init__(senior, [
            'btn-primary',
            'btn-secondary',
            'btn-success',
            'btn-danger',
            'btn-warning',
            'btn-info',
            'btn-light',
            'btn-dark',
        ])

    def set_primary(self): return self.set('btn-primary')

    def set_secondary(self): return self.set('btn-secondary')

    def set_success(self): return self.set('btn-success')

    def set_danger(self): return self.set('btn-danger')

    def set_warning(self): return self.set('btn-warning')

    def set_info(self): return self.set('btn-info')

    def set_light(self): return self.set('btn-light')

    def set_dark(self): return self.set('btn-dark')
