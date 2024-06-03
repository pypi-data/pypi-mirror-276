from ...__templates__.styles import Styles


class Color(Styles):
    def __init__(self, senior):
        super().__init__(senior, [
            'alert-primary',
            'alert-secondary',
            'alert-success',
            'alert-danger',
            'alert-warning',
            'alert-info',
            'alert-light',
            'alert-dark',
        ])

    def set_primary(self): return self.set('alert-primary')

    def set_secondary(self): return self.set('alert-secondary')

    def set_success(self): return self.set('alert-success')

    def set_danger(self): return self.set('alert-danger')

    def set_warning(self): return self.set('alert-warning')

    def set_info(self): return self.set('alert-info')

    def set_light(self): return self.set('alert-light')

    def set_dark(self): return self.set('alert-dark')
