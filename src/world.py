import random
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
from common import GridCell
from algorithm import depthFirstSearch

class World:
    def __init__(self, height: int = 50, width: int = 50):
        self._height = height
        self._width = width
        self.robot = GridCell(0, 0)
        self._goal = GridCell(self._width - 1, self._height - 1)
        self.grid = np.zeros((self._width, self._height))
        self.visited = np.zeros((self._width, self._height))
        self.generateObstacles()

    def generateObstacles(self):
        for i in range(self._width):
            for j in range(self._height):
                prob = random.randint(0,100)/100
                if prob <= 0.35:
                    self.grid[i][j] = 1
                else:
                    self.grid[i][j] = 0
        
        self.grid[self.robot.x][self.robot.y] = 2
        self.grid[self._goal.x][self._goal.y] = 3

        count = 0
        reached = False
        while count < 10:
            self.visited = np.zeros((self._width, self._height))
            self.vis()
            reached = depthFirstSearch(self._height, self._width, self._goal, self.robot, self.grid, self.visited, init = True)
            if reached:
                break
            count += 1
            print(count, reached)

            # need a better way to remove obstacles from the map
            for i in range(self._width):
                for j in range(self._height):
                    if self.grid[i][j] == 0:
                        ## up down left right
                        for direction in range(2):
                            if direction == 0 and i-1 >= 0 and i-1 < self._width:  
                                self.grid[i-1][j] = 0
                            elif direction == 1 and j-1 >= 0 and j-1 < self._height:
                                self.grid[i][j-1] = 0
                    elif self.grid[i][j] == 2:
                        self.grid[i+1][j] = 0
                        self.grid[i][j+1] = 0
                    elif self.grid[i][j] == 3:
                        self.grid[i-1][j] = 0
                        self.grid[i][j-1] = 0

    def vis(self):
        cmap = ListedColormap(['w', 'k', 'r', 'b'])
        self.grid[self.robot.x][self.robot.y] = 2
        self.grid[self._goal.x][self._goal.y] = 3

        fig, ax = plt.subplots()
        ax.matshow(self.grid, cmap=cmap)
        ax.set_xlabel('x')
        ax.set_ylabel('y')

        plt.show()

world = World()
# world.vis()