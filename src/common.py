import sys
sys.setrecursionlimit(10000)

FREE = 0
OBSTACLE = 1
ROBOT = 2
PATH = 3
PLANNER_PATH_1 = 4
PLANNER_PATH_2 = 5
GOAL = 6

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
    
    def __ge__(self, other):
        return self.f >= other.f
    
    def __gt__(self, other):
        return self.f > other.f

    def __le__(self, other):
        return self.f <= other.f
    
    def __lt__(self, other):
        return self.f < other.f

def inWorld(pos: GridCell, width: int, height: int):
    status = False
    if pos.x >= 0 and pos.x < width and pos.y >= 0 and pos.y < height:
        status = True
    return status

def checkValid(pos: GridCell, world):
    cont = True

    # check new position valid
    if not inWorld(pos, world._width, world._height):
        cont = False

    # check new position is not an obstacle
    if cont and world.grid[pos.x][pos.y] == OBSTACLE:
        cont = False

    return cont

def euclideanDist(x1, y1, x2, y2):
    return (x1 - x2) **2 + (y1 - y2)**2

def generateNewPositionList(allowDiag: bool):
    ls = []
    if not allowDiag:
        ls = [GridCell(-1, 0), GridCell(0, -1), GridCell(1, 0), GridCell(0, 1)]
    else:
        ls = [GridCell(-1, 1), GridCell(-1, 0), GridCell(-1, -1), GridCell(0, -1), GridCell(1, -1), GridCell(1, 0), GridCell(1, 1), GridCell(0, 1)]

    return ls

def depthFirstSearch(height: int, width: int, goal: GridCell, pos: GridCell, grid, visited, allowDiagonal, init = False):
    if init:
        global reached
        reached = False

    if pos == goal:
        reached = True
    else:
        visited[pos.x][pos.y] = 1
        
        # check left right up down
        newPositionList = generateNewPositionList(allowDiagonal)
        for newPosition in newPositionList:
            newPos = GridCell(pos.x + newPosition.x, pos.y + newPosition.y)

            if inWorld(newPos, width, height) and grid[newPos.x][newPos.y] != OBSTACLE and visited[newPos.x][newPos.y] == 0:
                    depthFirstSearch(height, width, goal, newPos, grid, visited, allowDiagonal)
                    visited[newPos.x][newPos.y] = 1
 
    if reached:
        return True
    else:
        return False