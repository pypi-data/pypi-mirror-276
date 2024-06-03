from ...__templates__.styles import Styles


class Flex(Styles):
    def __init__(self, senior):
        super().__init__(senior, [
            'd-flex',
            'd-inline-flex',
            'd-sm-flex',
            'd-sm-inline-flex',
            'd-md-flex',
            'd-md-inline-flex',
            'd-lg-flex',
            'd-lg-inline-flex',
            'd-xl-flex',
            'd-xl-inline-flex',
            'd-xxl-flex',
            'd-xxl-inline-flex',
        ])

    def set_d_flex(self): self.set('d-flex')
    def set_d_inline_flex(self): self.set('d-inline-flex')
    def set_d_sm_flex(self): self.set('d-sm-flex')
    def set_d_sm_inline_flex(self): self.set('d-sm-inline-flex')
    def set_d_md_flex(self): self.set('d-md-flex')
    def set_d_md_inline_flex(self): self.set('d-md-inline-flex')
    def set_d_lg_flex(self): self.set('d-md-lg-flex')
    def set_d_lg_inline_flex(self): self.set('d-lg-inline-flex')
    def set_d_xl_flex(self): self.set('d-md-xl-flex')
    def set_d_xl_inline_flex(self): self.set('d-xl-inline-flex')
    def set_d_xxl_flex(self): self.set('d-md-xxl-flex')
    def set_d_xxl_inline_flex(self): self.set('d-xxl-inline-flex')
