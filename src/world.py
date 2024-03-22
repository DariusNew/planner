import random
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
from common import *

class World:
    def __init__(self, height: int = 25, width: int = 25):
        self._allowDiagonal = False
        self._prob = 0.35
        self._height = height
        self._width = width
        self.robot = GridCell(0, 0)
        self.goal = GridCell(self._width - 1, self._height - 1)
        self.grid = np.zeros((self._width, self._height))
        self.generateObstacles()
        self.frames = [self.grid]

    def generateObstacles(self):
        for i in range(self._width):
            for j in range(self._height):
                prob = random.randint(0,100)/100
                if prob <= self._prob:
                    self.grid[i][j] = OBSTACLE
                else:
                    self.grid[i][j] = FREE
        
        self.grid[self.robot.x][self.robot.y] = ROBOT
        self.grid[self.goal.x][self.goal.y] = GOAL

        count = 0
        reached = False
        while count < 10:
            visited = np.zeros((self._width, self._height))
            reached = depthFirstSearch(self._height, self._width, self.goal, self.robot, self.grid, visited, self._allowDiagonal, init = True)
            if reached:
                break
            count += 1
            # print(count, reached)
            for i in range(self._width):
                for j in range(self._height):
                    if self.grid[i][j] == FREE:
                        ## down left
                        if not self._allowDiagonal:
                            for direction in range(2):
                                prob = random.randint(0,100)/100                  
                                if direction == 0 and i-1 >= 0 and i-1 < self._width and prob <= self._prob: 
                                    self.grid[i-1][j] = FREE
                                elif direction == 1 and j-1 >= 0 and j-1 < self._height and prob <= self._prob:
                                    self.grid[i][j-1] = FREE    

                        else: 
                            for direction in range(3):
                                prob = random.randint(0,100)/100                  
                                if direction == 0 and i-1 >= 0 and i-1 < self._width and prob <= self._prob: 
                                    self.grid[i-1][j] = FREE
                                elif direction == 1 and j-1 >= 0 and j-1 < self._height and prob <= self._prob:
                                    self.grid[i][j-1] = FREE 
                                elif direction == 2 and i-1 >= 0 and i-1 < self._width and j-1 >= 0 and j-1 < self._height and prob <= self._prob:
                                    self.grid[i-1][j-1] = FREE      
                    elif self.grid[i][j] == ROBOT:
                        self.grid[i+1][j] = FREE
                        self.grid[i][j+1] = FREE
                    elif self.grid[i][j] == GOAL:
                        self.grid[i-1][j] = FREE
                        self.grid[i][j-1] = FREE

    def vis(self):
        cmap = ListedColormap(['w', 'k', 'r', 'b', 'y', 'c' ,'g'])
        self.grid[self.robot.x][self.robot.y] = ROBOT
        self.grid[self.goal.x][self.goal.y] = GOAL

        fig, ax = plt.subplots()
        ax.matshow(self.grid, cmap=cmap)
        ax.set_xlabel('x')
        ax.set_ylabel('y')

        plt.show()

