import random
import heapq
import copy
import tqdm
from common import *

class Individual:
    def __init__(self):
        self.movement = []
        self.path = []
        self.fitness = 0
        self.reached = False

    def __repr__(self):
        ans = ""
        for points in self.path:
            ans += str(points)
        return ans
    
    def __ge__(self, other):
        return self.fitness >= other.fitness
    
    def __gt__(self, other):
        return self.fitness > other.fitness

    def __le__(self, other):
        return self.fitness <= other.fitness
    
    def __lt__(self, other):
        return self.fitness < other.fitness

def createPopulation(size: int, length: int, newPositionList):
    populationList = []
    # create a population with completely random moves
    for i in range(size):
        individual = Individual()

        for j in range(length):
            individual.movement.append(newPositionList[random.randrange(0, len(newPositionList))])

        populationList.append(individual)
    return populationList

def findFitness(populationList, world):
    for indv in populationList:
        blocked = 0
        valid = 0
        backtrack = 0

        pos = world.robot
        indv.path = []
        indv.path.append(pos)
        for direction in indv.movement:
            newPos = GridCell(pos.x + direction.x, pos.y + direction.y)
            if not checkValid(newPos, world):
                valid += 1
            elif world.grid[newPos.x][newPos.y] == OBSTACLE:
                blocked += 1
            elif newPos == world._goal:
                if newPos in indv.path:
                    backtrack += 1
                indv.path.append(newPos)
                indv.reached = True
                break
            else:
                if newPos in indv.path:
                    backtrack += 1
                indv.path.append(newPos)
                pos = newPos

        distanceReward = 0
        for node in indv.path:
            distanceReward += euclideanDist(node.x, node.y, world._goal.x, world._goal.y)
        penalty = valid + blocked + backtrack
        endReward = euclideanDist(indv.path[-1].x, indv.path[-1].y, world._goal.x, world._goal.y)
        
        if not indv.reached:
            indv.fitness = distanceReward/len(indv.path) + penalty * 40 + len(indv.path) * 10 + endReward   
            # print(indv.fitness, distanceReward / len(indv.path), penalty, len(indv.path), endReward)
        else:
            indv.fitness = distanceReward/len(indv.path) + penalty * 40 + len(indv.path) * 10 + endReward - 400
        
        if (indv.fitness < 0):
            indv.fitness = 1
        # print(indv, indv.fitness)

def mutate(indv: Individual, length: int, mutateProb: int, newPositionList):
    individual = Individual()

    for i in range(length):
        prob = random.randint(0,100)
        if prob <= mutateProb:
            # mutate
            direction = GridCell(0,0)
            while direction != indv.movement[i]:
                direction = newPositionList[random.randrange(0, len(newPositionList))]
        else:
            # take wholesale
            direction = indv.movement[i]

        individual.movement.append(direction)
    return individual

def dropOffMutate(indv: Individual):
    individual = Individual()  
    drop = random.randrange(0, len(indv.movement))
    for i in range(len(indv.movement)):
        if i != drop:
            individual.movement.append(indv.movement[i])
    individual.movement.append(indv.movement[drop])
    return individual

def crossover(left: Individual, newPositionList, length: int):
    individual = Individual()
    loc = random.randrange(0, length)
    for i in range(loc):
        individual.movement.append(left.movement[i])
    for j in range(loc, length):
        individual.movement.append(newPositionList[random.randrange(0, len(newPositionList))])

    return individual

def geneticPlanner(world, iterations: int = 500):
    populationSize = 1000
    mutationProb = 50
    dropOffMutationProb = 90
    maxLength = max(world._width, world._height)*4
    newPositionList = generateNewPositionList(world._allowDiagonal)
    populationList = createPopulation(populationSize, maxLength, newPositionList)
    bestIndividual = Individual()

    for iter in tqdm.tqdm(range(iterations)):
        findFitness(populationList, world)
        heapq.heapify(populationList)
        
        elite = []
        for j in range(random.randrange(100, int(populationSize/2))):
            ind = heapq.heappop(populationList)
            elite.append(ind)
        bestIndividual = elite[0]
        # print("cycle: ", iter, "fitness: ", bestIndividual.fitness)

        # for vis
        grid = copy.deepcopy(world.grid)
        for node in bestIndividual.path[1:-1]:
            if grid[node.x][node.y] != ROBOT and grid[node.x][node.y] != GOAL:
                grid[node.x][node.y] = PATH
        grid[bestIndividual.path[-1].x][bestIndividual.path[-1].y] = PLANNER_PATH_1
        world.frames.append(grid)           

        # generate the new population
        newPopulation = []
        for k in range(populationSize):
            mutateProb = random.randint(1, 100)         
            chosenElite = elite[random.randrange(0, len(elite))]
            indv = Individual()
            if mutateProb <= mutationProb:
                # mutate
                indv = mutate(chosenElite, maxLength, mutationProb, newPositionList)
                newPopulation.append(indv)
            elif mutateProb >= 90:
                indv = dropOffMutate(chosenElite)
                newPopulation.append(indv)
            else:     
                # crossover         
                indv = crossover(chosenElite, newPositionList, maxLength)
                newPopulation.append(indv)
        populationList = newPopulation

    if bestIndividual.reached == True:
        print("gen path found")
        
        # for vis
        grid = copy.deepcopy(world.grid)
        for node in bestIndividual.path[1:-1]:
            if grid[node.x][node.y] != ROBOT and grid[node.x][node.y] != GOAL:
                grid[node.x][node.y] = PATH
        world.frames.append(grid)   

        # for path
        path = bestIndividual.path[1:-1]
        return path