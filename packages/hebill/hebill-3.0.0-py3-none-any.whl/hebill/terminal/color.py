from colorama import Fore, Back


class Color:
    def __init__(self, terminal, fore=False):
        from .core import Terminal
        self._terminal: Terminal = terminal
        self._fore = fore
        self._FB = Fore if fore else Back

    def _set(self, color):
        if self._fore:
            self._terminal.set_color(color)
        else:
            self._terminal.set_background(color)
        return self._terminal

    @property
    def black(self): return self._set(self._FB.BLACK)

    @property
    def blue(self): return self._set(self._FB.BLUE)

    @property
    def cyan(self): return self._set(self._FB.BLUE)

    @property
    def green(self): return self._set(self._FB.GREEN)

    @property
    def magenta(self): return self._set(self._FB.MAGENTA)

    @property
    def red(self): return self._set(self._FB.RED)

    @property
    def yellow(self): return self._set(self._FB.YELLOW)

    @property
    def white(self): return self._set(self._FB.WHITE)

    @property
    def light_black(self): return self._set(self._FB.LIGHTBLACK_EX)

    @property
    def light_blue(self): return self._set(self._FB.LIGHTBLUE_EX)

    @property
    def light_cyan(self): return self._set(self._FB.LIGHTCYAN_EX)

    @property
    def light_green(self): return self._set(self._FB.LIGHTGREEN_EX)

    @property
    def light_magenta(self): return self._set(self._FB.LIGHTMAGENTA_EX)

    @property
    def light_red(self): return self._set(self._FB.LIGHTRED_EX)

    @property
    def light_yellow(self): return self._set(self._FB.LIGHTYELLOW_EX)
