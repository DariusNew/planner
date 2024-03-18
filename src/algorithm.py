import heapq
import copy
from common import GridCell
from common import Node
import sys
sys.setrecursionlimit(10000)

def inWorld(pos: GridCell, width: int, height: int):
    status = False
    if pos.x >= 0 and pos.x < width and pos.y >= 0 and pos.y < height:
        status = True
    return status

def euclideanDist(x1, y1, x2, y2):
    return (x1 - x2) **2 + (y1 - y2)**2

def depthFirstSearch(height: int, width: int, goal: GridCell, pos: GridCell, grid, visited, allowDiagonal, init = False):
    if init:
        global reached
        reached = False

    if pos == goal:
        reached = True
    else:
        visited[pos.x][pos.y] = 1
        
        # check left right up down
        newPositionList = []
        if not allowDiagonal:
            newPositionList = [GridCell(-1, 0), GridCell(0, -1), GridCell(1, 0), GridCell(0, 1)]
        else:
            newPositionList = [GridCell(-1, 1), GridCell(-1, 0), GridCell(-1, -1), GridCell(0, -1), GridCell(1, -1), GridCell(1, 0), GridCell(1, 1), GridCell(0, 1)]

        for newPosition in newPositionList:
            newPos = GridCell(pos.x + newPosition.x, pos.y + newPosition.y)

            if inWorld(newPos, width, height) and grid[newPos.x][newPos.y] != 1 and visited[newPos.x][newPos.y] == 0:
                    depthFirstSearch(height, width, goal, newPos, grid, visited, allowDiagonal)
                    visited[newPos.x][newPos.y] = 1
 
    if reached:
        return True
    else:
        return False
    
def aStarPlanner(world):
    startNode = Node(None, world.robot)
    endNode = Node(None, world._goal)

    openList = []
    closedList = []
    heapq.heappush(openList, startNode)

    # Loop till we find the end node 
    while(len(openList) > 0):
    # for i in range(10):
        currentNode = heapq.heappop(openList)
        closedList.append(currentNode)
        # if we found the goal, back track through all the parents and reverse this path
        if currentNode == endNode:
            print("a star path found")
            current = currentNode
            path = []
            while (current != startNode):
                path.append(current)
                current = current.parent
            path.append(startNode)
            for node in path[1:-1]:
                world.grid[node.position.x][node.position.y] = 3
            return path[::-1]
        
        # if not yet found the goal, we generate the children and calculate all their f
        children = []
        newPositionList = []
        if not world._allowDiagonal:
            newPositionList = [GridCell(-1, 0), GridCell(0, -1), GridCell(1, 0), GridCell(0, 1)]
        else:
            newPositionList = [GridCell(-1, 1), GridCell(-1, 0), GridCell(-1, -1), GridCell(0, -1), GridCell(1, -1), GridCell(1, 0), GridCell(1, 1), GridCell(0, 1)]

        for newPosition in newPositionList:
            cont = True
            newPos = GridCell(currentNode.position.x + newPosition.x, currentNode.position.y + newPosition.y)

            if not inWorld(newPos, world._width, world._height):
                cont = False

            if cont and world.grid[newPos.x][newPos.y] == 1:
                cont = False
        
            if cont:
                newNode = Node(currentNode, newPos)
                children.append(newNode)
        
        for child in children:
            cont = True
            if child in closedList:
                cont = False

            if cont:
                child.g = currentNode.g + 1
                child.h = euclideanDist(child.position.x, child.position.y, endNode.position.x, endNode.position.y)
                child.f = child.g + child.h
            
            for openNode in openList:    
                if child == openNode and child.g >= openNode.g:
                    cont = False
                elif child == openNode and child.g < openNode.g:
                    openList.remove(openNode)
                    cont = True
            
            if cont:
                heapq.heappush(openList, child)

        # for vis
        grid = copy.deepcopy(world.grid)
        grid[currentNode.position.x][currentNode.position.y] = 3
        for node in openList:
            grid[node.position.x][node.position.y] = 4
        world.frames.append(grid)