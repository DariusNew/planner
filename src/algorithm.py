import numpy as np
from common import GridCell
import sys
sys.setrecursionlimit(10000)

def depthFirstSearch(height: int, width: int, goal: GridCell, pos: GridCell, grid, visited, init = False):
    if init:
        global reached
        reached = False

    if pos == goal:
        reached = True
        print("path found")
    else:
        visited[pos.x][pos.y] = 1
        
        # check left right up down
        for direction in range(4):
            if direction == 0:
                newPos = GridCell(pos.x - 1, pos.y)
            elif direction == 1:
                newPos = GridCell(pos.x + 1, pos.y)
            elif direction == 2:
                newPos = GridCell(pos.x, pos.y - 1)
            elif direction == 3:
                newPos = GridCell(pos.x, pos.y + 1)

            if newPos.x >= 0 and newPos.x < width and newPos.y >= 0 and newPos.y < height and grid[newPos.x][newPos.y] != 1 and visited[newPos.x][newPos.y] == 0:
                depthFirstSearch(height, width, goal, newPos, grid, visited)
                visited[newPos.x][newPos.y] = 1

    if reached:
        return True
    else:
        return False