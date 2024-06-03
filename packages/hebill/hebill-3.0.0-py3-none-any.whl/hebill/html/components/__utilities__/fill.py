from ...__templates__.styles import Styles


class Justify(Styles):
    def __init__(self, senior):
        super().__init__(senior, [
            'flex_fill',
            'flex_sm_fill',
            'flex_md_fill',
            'flex_lg_fill',
            'flex_xl_fill',
            'flex_xxl_fill',

        ])

    def flex_fill(self): self.set('flex-fill')

    def flex_sm_fill(self): self.set('flex-sm-fill')

    def flex_md_fill(self): self.set('flex-md-fill')

    def flex_lg_fill(self): self.set('flex-lg-fill')

    def flex_xl_fill(self): self.set('flex-xl-fill')

    def flex_xxl_fill(self): self.set('flex-xxl-fill')
