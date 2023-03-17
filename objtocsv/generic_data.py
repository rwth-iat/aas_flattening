class flattened_type:
    id: str = None  # hash+time
    parent_id: str = None
    attrib_map: dict = None  # <"attribute, values">
    children: list = None

    def add_child(self, child):
        if self.children is None:
            self.children = list()
        self.children.append(child)

    def append_attrib_val_pair(self, attrib_val: dict):
        if self.attrib_map is None:
            self.attrib_map = dict()
        self.attrib_map.update(attrib_val)
