import heapq
import copy
from common import *

class AStarPlanner():
    def __init__(self, world):
        self.world = world
        self.originalGrid = copy.deepcopy(world.grid)
        self.startNode = Node(None, world.robot)
        self.endNode = Node(None, world.goal)
        self.directionList = generateNewPositionList(world._allowDiagonal)
        self.solved = False
        self.openList = []
        self.closedList = []
        self.frames = [self.originalGrid]
        heapq.heappush(self.openList, self.startNode)

    def saveFrame(self, current: Node):
        grid = copy.deepcopy(self.originalGrid)
        grid[current.position.x][current.position.y] = PATH
        for node in self.openList:
            grid[node.position.x][node.position.y] = PLANNER_PATH_1
        self.frames.append(grid)

    def savePathFrame(self, current: Node):
        path = []
        while (current != self.startNode):
            path.append(current)
            current = current.parent
        grid = copy.deepcopy(self.originalGrid)
        for node in path[1:]:
            grid[node.position.x][node.position.y] = PATH
        self.frames.append(grid)            

    def search(self, current: Node):
        searchSpace = []
        for direction in self.directionList:
            newPos = GridCell(current.position.x + direction.x, current.position.y + direction.y)
            if checkValid(newPos, self.world):
                searchSpace.append(Node(current, newPos))
        
        if searchSpace:
            for node in searchSpace:
                if node in self.closedList:
                    pass
                else:
                    node.g = current.g + 1
                    node.h = euclideanDist(node.position.x, node.position.y, self.endNode.position.x, self.endNode.position.y)
                    node.f = node.g + node.h
                    
                    cont = True
                    for openNode in self.openList:
                        if node == openNode and node.g >= openNode.g:
                            cont = False
                        elif node == openNode and node.g < openNode.g:
                            self.openList.remove(openNode)

                    if cont: 
                        heapq.heappush(self.openList, node)

    def solve(self):
        while len(self.openList) > 0:
            current = heapq.heappop(self.openList)
            self.closedList.append(current)
        
            if current == self.endNode:
                print("a star path found")
                self.savePathFrame(current)
                return self.frames
            else:
                self.search(current)
                self.saveFrame(current)