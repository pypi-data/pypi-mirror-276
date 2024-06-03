from ...__templates__.styles import Styles


class FlexRow(Styles):
    def __init__(self, senior):
        super().__init__(senior, [
            'flex-column',
            'flex-column-reverse',
            'flex-sm-column',
            'flex-sm-column-reverse',
            'flex-md-column',
            'flex-md-column-reverse',
            'flex-lg-column',
            'flex-lg-column-reverse',
            'flex-xl-column',
            'flex-xl-column-reverse',
            'flex-xxl-column',
            'flex-xxl-column-reverse',
            'flex-row',
            'flex-row-reverse',
            'flex-sm-row',
            'flex-sm-row-reverse',
            'flex-md-row',
            'flex-md-row-reverse',
            'flex-lg-row',
            'flex-lg-row-reverse',
            'flex-xl-row',
            'flex-xl-row-reverse',
            'flex-xxl-row',
            'flex-xxl-row-reverse',
        ])

    def set_flex_column(self): self.set('flex-column')
    def set_flex_column_reverse(self): self.set('d-flex-column-reverse')
    def set_flex_sm_column(self): self.set('flex-sm-column')
    def set_flex_sm_column_reverse(self): self.set('d-flex-sm-column-reverse')
    def set_flex_md_column(self): self.set('flex-md-column')
    def set_flex_md_column_reverse(self): self.set('d-flex-md-column-reverse')
    def set_flex_lg_column(self): self.set('flex-lg-column')
    def set_flex_lg_column_reverse(self): self.set('d-flex-lg-column-reverse')
    def set_flex_xl_column(self): self.set('flex-xl-column')
    def set_flex_xl_column_reverse(self): self.set('d-flex-xl-column-reverse')
    def set_flex_xxl_column(self): self.set('flex-xxl-column')
    def set_flex_xxl_column_reverse(self): self.set('d-flex-xxl-column-reverse')
    def set_flex_row(self): self.set('flex-row')
    def set_flex_row_reverse(self): self.set('d-flex-row-reverse')
    def set_flex_sm_row(self): self.set('flex-sm-row')
    def set_flex_sm_row_reverse(self): self.set('d-flex-sm-row-reverse')
    def set_flex_md_row(self): self.set('flex-md-row')
    def set_flex_md_row_reverse(self): self.set('d-flex-md-row-reverse')
    def set_flex_lg_row(self): self.set('flex-lg-row')
    def set_flex_lg_row_reverse(self): self.set('d-flex-lg-row-reverse')
    def set_flex_xl_row(self): self.set('flex-xl-row')
    def set_flex_xl_row_reverse(self): self.set('d-flex-xl-row-reverse')
    def set_flex_xxl_row(self): self.set('flex-xxl-row')
    def set_flex_xxl_row_reverse(self): self.set('d-flex-xxl-row-reverse')
