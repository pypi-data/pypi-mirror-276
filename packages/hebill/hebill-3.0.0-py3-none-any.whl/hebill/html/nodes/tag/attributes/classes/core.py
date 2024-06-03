class Classes(list):
    def reset(self, classes: str | list = None) -> bool:
        self.clear()
        if classes is None:
            return True
        return self.set(classes)

    def set(self, classes: str | list = None) -> bool:
        if isinstance(classes, str):
            if ' ' in classes:
                self.set(classes.split(' '))
            else:
                if classes not in self:
                    self.append(classes)
            return True
        elif isinstance(classes, list):
            for c in classes:
                self.set(c)
            return True
        return False

    def unset(self, classes: str | list = None) -> bool:
        if isinstance(classes, str):
            if ' ' in classes:
                self.unset(classes.split(' '))
            else:
                if classes in self:
                    self.remove(classes)
            return True
        elif isinstance(classes, list):
            for c in classes:
                self.unset(c)
            return True
        return False

    @property
    def is_empty(self) -> bool: return len(self) <= 0

    def __str__(self): return ' '.join(self)

    def output(self) -> str: return self.__str__()
