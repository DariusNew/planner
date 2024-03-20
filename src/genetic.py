import random
import heapq
import copy
from common import *

class Individual:
    def __init__(self):
        self.path = []
        self.movement = []
        self.fitness = 0

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

def createPopulation(size: int, length: int, startPos: GridCell, newPositionList):
    populationList = []
    # create a population with completely random moves
    for i in range(size):
        individual = Individual()
        pos = startPos
        individual.path.append(pos)

        for j in range(length):
            direction = newPositionList[random.randrange(0, len(newPositionList))]
            newPos = GridCell(pos.x + direction.x, pos.y + direction.y)
            # we want to prevent back tracking.
            if newPos not in individual.path:
                individual.path.append(newPos)
                pos = newPos
            individual.movement.append(direction)

        populationList.append(individual)
    return populationList

def findFitness(populationList, length: int, world):
    for indv in populationList:
        blocked = False
        valid = True
        reached = False
        lastPointIndex = -1
        for point in indv.path:
            if not checkValid(point, world):
                valid = False
                break
            elif world.grid[point.x][point.y] == 1:
                blocked = True
                break
            elif point == world._goal:
                reached = True
                lastPointIndex += 1
                break
            else:
                lastPointIndex += 1
        
        lastPoint = indv.path[lastPointIndex]
        # exit proximity reward
        distanceReward = euclideanDist(lastPoint.x, lastPoint.y, world._goal.x, world._goal.y) ## smaller is better
        # exploration reward
        lengthReward = length - lastPointIndex ## smaller is better
        # not valid penalty
        penalty = 0
        if not valid:
            penalty += lengthReward * 10 ## penalise over where the last point index is along the path.
        # dead end penalty
        if blocked:
            penalty += lengthReward * 20 ## penalise over where the last point index is along the path.
        # reward if reached the goal
        if reached:
            indv.fitness = 0
        else:
            indv.fitness = distanceReward + lengthReward + penalty     
        
def mutate(indv: Individual, length: int, mutateProb: int, newPositionList):
    individual = Individual()
    pos = indv.path[0]
    for i in range(length):
        prob = random.randint(0,100)
        if prob <= mutateProb:
            # mutate
            direction = newPositionList[random.randrange(0, len(newPositionList))]
        else:
            # take wholesale
            direction = indv.movement[i]

        newPos = GridCell(pos.x + direction.x, pos.y + direction.y)
        # we want to prevent back tracking.
        if newPos not in individual.path:
            individual.path.append(newPos)
            pos = newPos
        individual.movement.append(direction)
        
    return individual

def crossover(left: Individual, right: Individual, length: int):
    individual = Individual()
    loc = random.randrange(0, length)
    for i in range(loc):
        individual.movement.append(left.movement[i])
    for j in range(loc, length):
        individual.movement.append(right.movement[j])
    
    pos = left.path[0]
    for direction in range(individual.movement):
        newPos = GridCell(pos.x + direction.x, pos.y + direction.y)
        if newPos not in individual.path:
            individual.path.append(newPos)
            pos = newPos

    return individual

def geneticPlanner(world, iterations: int = 5000):
    populationSize = 100
    mutationProb = 30 
    eliteProb = 20 
    maxLength = max(world._width, world._height)*2
    newPositionList = generateNewPositionList(world._allowDiagonal)
    populationList = createPopulation(populationSize, maxLength, world.robot, newPositionList)

    for i in range(iterations):
        findFitness(populationList, populationSize, world)
        heapq.heapify(populationList)

        bestIndividual = heapq.heap[0]
        print("cycle: ", i, "fitness: ", bestIndividual.fitness)
        if bestIndividual.fitness == 0:
            print("path found")
            return print(bestIndividual)       

        elite = [] # we try to keep some of the better ones for better crossover, but definitely we keep the best best for comparison
        for j in range(random.randrange(1, 25)):
            elite.append(heapq.heap[j])
        eliteCounter = 0
        # generate the new population
        newPopulation = []
        for k in range(populationSize):
            mutateEliteProb = random.randint(0, 100)
            crossoverEliteProb = random.randint(0,100)

            if mutateEliteProb <= mutationProb:
                # mutate
                indv = mutate(populationList[k], maxLength, mutationProb, newPositionList)
                newPopulation.append(indv)
            elif mutateEliteProb >= 100 - eliteProb:
                # add elite
                newPopulation.append(elite[eliteCounter])
                eliteCounter += 1
            elif crossoverEliteProb <= eliteProb:     
                # crossover with elite
                left = elite[random.randrange(0, len(elite))]
                right = populationList[k]
                indv = crossover(left, right, maxLength)
                newPopulation.append(indv)
            else:
                # 2 random selection and crossover
                left = populationList[random.randrange(0, len(populationList))]
                right = populationList[k]
                indv = crossover(left, right, maxLength)
                newPopulation.append(indv)