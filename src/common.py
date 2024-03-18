class GridCell:
    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return "[" + str(self.x) + ", " + str(self.y) + "]"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
class Node:
    def __init__(self, parent, position: GridCell):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __repr__(self):
        return "[" + str(self.position.x) + ", " + str(self.position.y) + "]"

    def __eq__(self, other):
        return self.position == other.position