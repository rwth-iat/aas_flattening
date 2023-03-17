class HeaderList(list):
    def __init__(self, *args):
        super().__init__(*args)

    def append(self, item):
        if item not in self:
            super().append(str(item))
