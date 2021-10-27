class Vertex:
    def __init__(self, label):
        self._label = label

    @property
    def label(self):
        return self._label

    def __eq__(self, other):
        return self.label == other.label

    def __hash__(self):
        return hash(str(self._label))

    def __str__(self):
        return str(self.label)

