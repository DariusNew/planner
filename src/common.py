class GridCell:
    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return "[" + str(self.x) + ", " + str(self.y) + "]"
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y