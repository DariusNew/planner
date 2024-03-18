import heapq
import copy
import random
import numpy as np
from common import GridCell
from common import Node
import sys
sys.setrecursionlimit(10000)

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
    if cont and world.grid[pos.x][pos.y] == 1:
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
            # for vis
            grid = copy.deepcopy(world.grid)
            grid[currentNode.position.x][currentNode.position.y] = 3
            for node in openList:
                grid[node.position.x][node.position.y] = 4
            world.frames.append(grid)
            # for path
            curr = currentNode
            path = []
            while (curr != startNode):
                path.append(curr)
                curr = curr.parent
            path.append(startNode)
            for node in path[1:-1]:
                world.grid[node.position.x][node.position.y] = 3
            return path[::-1]
        
        # if not yet found the goal, we generate the search space and calculate all their f
        searchSpace = []
        newPositionList = generateNewPositionList(world._allowDiagonal)
    
        for newPosition in newPositionList:
            newPos = GridCell(currentNode.position.x + newPosition.x, currentNode.position.y + newPosition.y)
            cont = checkValid(newPos, world)

            if cont:
                newNode = Node(currentNode, newPos)
                searchSpace.append(newNode)
        
        for node in searchSpace:
            cont = True
            if node in closedList:
                cont = False

            if cont:
                node.g = currentNode.g + 1
                node.h = euclideanDist(node.position.x, node.position.y, endNode.position.x, endNode.position.y)
                node.f = node.g + node.h
            
                for openNode in openList:    
                    if node == openNode and node.g >= openNode.g:
                        cont = False
                    elif node == openNode and node.g < openNode.g:
                        openList.remove(openNode)
                        cont = True
            
            if cont:
                heapq.heappush(openList, node)

        # for vis
        grid = copy.deepcopy(world.grid)
        grid[currentNode.position.x][currentNode.position.y] = 3
        for node in openList:
            grid[node.position.x][node.position.y] = 4
        world.frames.append(grid)

def rrtPlanner(world):
    startNode = Node(None, world.robot)
    endNode = Node(None, world._goal)
    stepSize = int(min(world._height, world._width) / 2)
    forwardTree = [startNode]
    reverseTree = [endNode]
    pathFound = False
    midNode = startNode
    forwardOnly = False
    reverseOnly = False
    while not pathFound:
        randPos = GridCell(random.randrange(0, world._width), random.randrange(0, world._height))
        # print ("random position: ", randPos)

        if checkValid(randPos, world):
            minForwardDist = float("inf")
            minReverseDist = float("inf")
            closestForwardNode = forwardTree[0]
            closestReverseNode = reverseTree[0]
            for node in forwardTree:           
                dist = euclideanDist(randPos.x, randPos.y, node.position.x, node.position.y)
                if dist < minForwardDist: 
                    minForwardDist = dist
                    closestForwardNode = node
            for node in reverseTree:
                dist = euclideanDist(randPos.x, randPos.y, node.position.x, node.position.y)
                if dist < minReverseDist:
                    minReverseDist = dist
                    closestReverseNode = node
            # print("closest node: ", closestForwardNode)

            # if possible try taking n steps in any direction towards the node
            prevForwardNode = closestForwardNode
            prevReverseNode = closestReverseNode

            for step in range(min(stepSize, min(int(minForwardDist), int(minReverseDist)))):
                cont = True
                forwardPos = copy.deepcopy(prevForwardNode.position)
                reversePos = copy.deepcopy(prevReverseNode.position)
                forwardNode = Node(prevForwardNode, forwardPos)
                reverseNode = Node(prevReverseNode, reversePos)

                # Forward x or y     
                xForwardDiff = randPos.x - forwardNode.position.x
                yForwardDiff = randPos.y - forwardNode.position.y
                if (abs(xForwardDiff) > abs(yForwardDiff)):
                    if xForwardDiff >= 0:
                        forwardNode.position.x += 1
                    else:
                        forwardNode.position.x -= 1
                else:
                    if yForwardDiff >= 0:
                        forwardNode.position.y += 1
                    else:
                        forwardNode.position.y -= 1
                
                # Reverse x or y   
                xReverseDiff = randPos.x - reverseNode.position.x
                yReverseDiff = randPos.y - reverseNode.position.y
                if (abs(xReverseDiff) > abs(yReverseDiff)):
                    if xReverseDiff >= 0:
                        reverseNode.position.x += 1
                    else:
                        reverseNode.position.x -= 1
                else:
                    if yReverseDiff >= 0:
                        reverseNode.position.y += 1
                    else:
                        reverseNode.position.y -= 1

                if checkValid(forwardNode.position, world):
                    prevForwardNode = copy.deepcopy(forwardNode)
                    if prevForwardNode not in forwardTree:
                        forwardTree.append(prevForwardNode)
                    if forwardNode.position == world._goal:
                        print("rrt path found")
                        forwardOnly = True
                        pathFound = True
                    elif forwardNode in reverseTree:
                        print("rrt path found")
                        midNode = forwardNode
                        pathFound = True
                else:
                    cont = False

                if checkValid(reverseNode.position, world):
                    prevReverseNode = copy.deepcopy(reverseNode)
                    if prevReverseNode not in reverseTree:
                        reverseTree.append(prevReverseNode)
                    if reverseNode.position == world.robot:
                        print("rrt path found")
                        reverseOnly = True
                        pathFound = True
                    elif reverseNode in forwardTree:
                        print("rrt path found")
                        midNode = reverseNode
                        pathFound = True
                else:
                    cont = False

                if not cont:
                    break

                if pathFound:
                    # for vis
                    grid = copy.deepcopy(world.grid)
                    for node in forwardTree[1:]:
                        grid[node.position.x][node.position.y] = 4
                    for node in reverseTree[:-1]:
                        grid[node.position.x][node.position.y] = 5
                    grid[randPos.x][randPos.y] = 3
                    world.frames.append(grid)

                    if forwardOnly:
                        # for path
                        curr = forwardNode
                        path = []
                        while curr != startNode:
                            path.append(curr)
                            curr = curr.parent
                        path.append(startNode)
                        for node in path[1:-1]:
                            world.grid[node.position.x][node.position.y] = 3
                        return path[::-1]
                    elif reverseOnly:
                        # for path
                        curr = reverseNode
                        path = []
                        while curr != endNode:
                            path.append(curr)
                            curr = curr.parent
                        path.append(endNode)
                        for node in path[1:-1]:
                            world.grid[node.position.x][node.position.y] = 3
                        return path
                    else:
                        currForward = forwardTree[forwardTree.index(midNode)]
                        currReverse = reverseTree[reverseTree.index(midNode)]
                        currReverse = currReverse.parent
                        path = []
                        while currForward != startNode:
                            path.append(currForward)
                            currForward = currForward.parent
                        path.append(startNode)
                        path = path[::-1]
                        while currReverse != endNode:
                            path.append(currReverse)
                            currReverse = currReverse.parent
                        path.append(endNode)
                        for node in path[1:-1]:
                            world.grid[node.position.x][node.position.y] = 3
                        return path
                
                    
            # for vis
            grid = copy.deepcopy(world.grid)
            for node in forwardTree[1:]:
                grid[node.position.x][node.position.y] = 4
            for node in reverseTree[:-1]:
                grid[node.position.x][node.position.y] = 5
            grid[randPos.x][randPos.y] = 3
            world.frames.append(grid)

            
