from collections import Counter


class HashableCounter(Counter):
    def __init__(self, v=None):
        if v is None:
            super().__init__()
        else:
            super().__init__(v)

    def __hash__(self):
        return hash(tuple(sorted(self.items())))


class HashableList(list):
    def __init__(self, v=None):
        if v is None:
            super().__init__()
        else:
            super().__init__(v)

    def __hash__(self):
        return hash(tuple(self))


class HashableSet(set):
    def __init__(self, v=None):
        if v is None:
            super().__init__()
        else:
            super().__init__(v)

    def __hash__(self):
        return hash(tuple(self))


class HashableDict(dict):
    def __init__(self, v=None):
        if v is None:
            super().__init__()
        else:
            super().__init__(v)

    def __hash__(self):
        return hash(tuple(sorted(self.items())))