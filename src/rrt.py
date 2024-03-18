import random
import copy
from common import *

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
