import heapq
import copy
from common import *

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
            grid[currentNode.position.x][currentNode.position.y] = PATH
            for node in openList:
                grid[node.position.x][node.position.y] = PLANNER_PATH_1
            world.frames.append(grid)
            # for path
            curr = currentNode
            path = []
            while (curr != startNode):
                path.append(curr)
                curr = curr.parent
            path.append(startNode)
            for node in path[1:-1]:
                world.grid[node.position.x][node.position.y] = PATH
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
        grid[currentNode.position.x][currentNode.position.y] = PATH
        for node in openList:
            grid[node.position.x][node.position.y] = PLANNER_PATH_1
        world.frames.append(grid)