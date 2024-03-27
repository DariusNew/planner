import random
import heapq
import copy
import tqdm
from common import *

class Chromosome:
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
        chromosome = Chromosome()

        for j in range(length):
            chromosome.movement.append(newPositionList[random.randrange(0, len(newPositionList))])

        populationList.append(chromosome)
    return populationList

def findFitness(populationList, world):
    for chromo in populationList:
        blocked = 0
        valid = 0
        backtrack = 0

        pos = world.robot
        chromo.path = []
        chromo.path.append(pos)
        for direction in chromo.movement:
            newPos = GridCell(pos.x + direction.x, pos.y + direction.y)
            if not checkValid(newPos, world):
                valid += 1
            elif world.grid[newPos.x][newPos.y] == OBSTACLE:
                blocked += 1
            elif newPos == world._goal:
                if newPos in chromo.path:
                    backtrack += 1
                chromo.path.append(newPos)
                chromo.reached = True
                break
            else:
                if newPos in chromo.path:
                    backtrack += 1
                chromo.path.append(newPos)
                pos = newPos

        distanceReward = 0
        for node in chromo.path:
            distanceReward += euclideanDist(node.x, node.y, world._goal.x, world._goal.y)
        penalty = valid + blocked + backtrack
        endReward = euclideanDist(chromo.path[-1].x, chromo.path[-1].y, world._goal.x, world._goal.y)
        
        if not chromo.reached:
            chromo.fitness = distanceReward/len(chromo.path) + penalty * 40 + len(chromo.path) * 10 + endReward   
            # print(chromo.fitness, distanceReward / len(chromo.path), penalty, len(chromo.path), endReward)
        else:
            chromo.fitness = distanceReward/len(chromo.path) + penalty * 40 + len(chromo.path) * 10 + endReward - 400
        
        if (chromo.fitness < 0):
            chromo.fitness = 1
        # print(chromo, chromo.fitness)

def mutate(chromo: Chromosome, length: int, mutateProb: int, newPositionList):
    chromosome = Chromosome()

    for i in range(length):
        prob = random.randint(0,100)
        if prob <= mutateProb:
            # mutate
            direction = GridCell(0,0)
            while direction != chromo.movement[i]:
                direction = newPositionList[random.randrange(0, len(newPositionList))]
        else:
            # take wholesale
            direction = chromo.movement[i]

        chromosome.movement.append(direction)
    return chromosome

def dropOffMutate(chromo: Chromosome):
    chromosome = Chromosome()  
    drop = random.randrange(0, len(chromo.movement))
    for i in range(len(chromo.movement)):
        if i != drop:
            chromosome.movement.append(chromo.movement[i])
    chromosome.movement.append(chromo.movement[drop])
    return chromosome

def crossover(left: Chromosome, newPositionList, length: int):
    chromosome = Chromosome()
    loc = random.randrange(0, length)
    for i in range(loc):
        chromosome.movement.append(left.movement[i])
    for j in range(loc, length):
        chromosome.movement.append(newPositionList[random.randrange(0, len(newPositionList))])

    return chromosome

def geneticPlanner(world, iterations: int = 500):
    populationSize = 1000
    mutationProb = 50
    dropOffMutationProb = 85
    maxLength = max(world._width, world._height)*4
    newPositionList = generateNewPositionList(world._allowDiagonal)
    populationList = createPopulation(populationSize, maxLength, newPositionList)
    bestChromosome = Chromosome()

    for iter in tqdm.tqdm(range(iterations)):
        findFitness(populationList, world)
        heapq.heapify(populationList)
        
        elite = []
        for j in range(random.randrange(100, int(populationSize/2))):
            chromosome = heapq.heappop(populationList)
            elite.append(chromosome)
        bestChromosome = elite[0]
        # print("cycle: ", iter, "fitness: ", bestChromosome.fitness)

        # for vis
        grid = copy.deepcopy(world.grid)
        for node in bestChromosome.path[1:-1]:
            if grid[node.x][node.y] != ROBOT and grid[node.x][node.y] != GOAL:
                grid[node.x][node.y] = PATH
        grid[bestChromosome.path[-1].x][bestChromosome.path[-1].y] = PLANNER_PATH_1
        world.frames.append(grid)           

        # generate the new population
        newPopulation = []
        for k in range(populationSize):
            mutateProb = random.randint(1, 100)         
            chosenElite = elite[random.randrange(0, len(elite))]
            chromo = Chromosome()
            if mutateProb <= mutationProb:
                # mutate
                chromo = mutate(chosenElite, maxLength, mutationProb, newPositionList)
                newPopulation.append(chromo)
            elif mutateProb >= dropOffMutationProb:
                chromo = dropOffMutate(chosenElite)
                newPopulation.append(chromo)
            else:     
                # crossover         
                chromo = crossover(chosenElite, newPositionList, maxLength)
                newPopulation.append(chromo)
        populationList = newPopulation

    if bestChromosome.reached == True:
        print("gen path found")
        
        # for vis
        grid = copy.deepcopy(world.grid)
        for node in bestChromosome.path[1:-1]:
            if grid[node.x][node.y] != ROBOT and grid[node.x][node.y] != GOAL:
                grid[node.x][node.y] = PATH
        world.frames.append(grid)   

        # for path
        path = bestChromosome.path[1:-1]
        return path