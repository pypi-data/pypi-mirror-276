import sys
from colorama import Style


class Terminal:
    def __init__(self):
        self._color = ''
        self._background = ''

    def set_color(self, color: str):
        self._color = color

    def set_background(self, color: str):
        self._background = color

    def input(self, content: str):
        try:
            inputs = input(self._background + self._color + content + Style.RESET_ALL)
            sys.stdout.flush()
            return inputs
        except UnicodeDecodeError as e:
            print(f"编码错误：{e}")

    def print(self, content: str, line_break=True):
        print(self._background + self._color + content + Style.RESET_ALL, end='\n' if line_break else '')
        sys.stdout.flush()

    @property
    def color(self):
        from .color_fore import ColorFore
        return ColorFore(self, True)

    @property
    def background(self):
        from .color_back import ColorBack
        return ColorBack(self)
