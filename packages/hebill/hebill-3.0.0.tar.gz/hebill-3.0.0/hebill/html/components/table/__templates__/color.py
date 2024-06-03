from ....__templates__.styles import Styles


class Color(Styles):
    def __init__(self, senior):
        super().__init__(senior, [
            'table-primary',
            'table-secondary',
            'table-success',
            'table-danger',
            'table-warning',
            'table-info',
            'table-light',
            'table-dark',
        ])

    def set_primary(self): return self.set('table-primary')

    def set_secondary(self): return self.set('table-secondary')

    def set_success(self): return self.set('table-success')

    def set_danger(self): return self.set('table-danger')

    def set_warning(self): return self.set('table-warning')

    def set_info(self): return self.set('table-info')

    def set_light(self): return self.set('table-light')

    def set_dark(self): return self.set('table-dark')
