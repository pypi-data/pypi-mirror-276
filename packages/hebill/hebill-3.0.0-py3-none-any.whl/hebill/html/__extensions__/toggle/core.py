class Toggle:
    def set_toggle_target_by_id(self, tag, show=False):
        self.attributes.set('data-bs-toggle', 'collapse')
        self.attributes.set('aria-expanded', 'true' if show else 'false')
        self.attributes.set('data-bs-target', f'#{tag.attributes.get_id(True)}')
        self.attributes.set('aria-controls', tag.attributes.get_id())
        tag.attributes.classes.set('collapse')

    def set_toggle_target_by_class(self, tag, show=False):
        self.attributes.set('data-bs-toggle', 'collapse')
        self.attributes.set('aria-expanded', 'true' if show else 'false')
        self.attributes.set('data-bs-target', f'#{tag.attributes.get_id(True)}')
        self.attributes.set('aria-controls', tag.attributes.get_id())
        tag.attributes.classes.set('collapse')
