class Edge:
    def __init__(self,origin, destinaton, weight=0):
        self._origin = origin
        self._dest = destinaton
        self._weight = weight

    @property
    def origin(self):
        return self._origin

    @property
    def destination(self):
        return self._dest

    @property
    def weight(self):
        return self._weight

    def __eq__(self, other):
        return self.origin == other.origin and self.destination == other.destination

    def __hash__(self):
        return hash(str(self.origin)+str(self.destination))

    def __str__(self):
        return "(" + str(self.origin) + ", " + str(self.destination) + ")" + " weight: " + str(self.weight)

