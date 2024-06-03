class Styles(dict):
    def reset(self, styles: str | list = None) -> bool:
        self.clear()
        if styles is None:
            return True
        return self.sets(styles)

    def set(self, name: str, style: str):
        self[name.strip()] = style.strip()

    def sets(self, styles: dict | str = None) -> bool:
        if isinstance(styles, str):
            if styles.strip() == '':
                return True
            if ';' not in styles:
                styles += ';'
            x = styles.split(';')
            for style in x:
                if ':' in style:
                    n, v = style.split(':')
                    self.set(n, v)
            return True
        elif isinstance(styles, dict):
            for n, v in styles.items():
                self.set(n, v)
            return True
        return False

    @property
    def is_empty(self) -> bool:
        return len(self) <= 0

    def __str__(self):
        return ''.join(f'{n}:{v};' for n, v in self.items())

    def output(self) -> str:
        return self.__str__()
