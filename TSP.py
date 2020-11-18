from random import randint
import random as rd


def RandomPermutation(x):
    vals = x[:]
    perm = []
    while len(vals) > 1:
        y = rd.choice(vals)
        perm.append(y)
        vals.remove(y)
    perm.append(vals[0])
    return perm


def EvaluateFitnessHistory(history, overPriod=4):
    historyLength = len(history)
    if(historyLength < overPriod):
        return False
    lastCheckedHistory = []
    similarHistoryCount = 0
    for i in range(overPriod):
        if(history[historyLength-1-i] != lastCheckedHistory):
            lastCheckedHistory = history[historyLength-1-i]
            similarHistoryCount = 0
        else:
            similarHistoryCount += 1
    if(similarHistoryCount == overPriod):
        return True
    else:
        return False


def getDistance(l, graph):
    start = l[0]
    dist = 0
    for k in range(1, len(l)):
        dist += graph[start][l[k]]
        start = l[k]
    return dist + graph[start][l[0]]


class Genetics:
    def __init__(self, places, distanceGraph, maxGenerations=10):
        self.places = places
        self.distanceGraph = distanceGraph
        self.maxGenerations = maxGenerations
        self.populationSize = len(places)
        self.Population = [RandomPermutation(places) for _ in range(self.maxGenerations)]

    def calculateFitness(self):
        fitness = [0]*len(self.Population)
        for i in range(len(self.Population)):
            s = getDistance(self.Population[i],self.distanceGraph)
            fitness[i] = s
        return fitness

    def selectFitParents(self,fitness):
        numOfParent = int(self.populationSize/2)
        fitnesses = list(fitness)
        selectedParents = []
        for _ in range(numOfParent):
            minFitIndex = fitnesses.index(min(fitnesses))
            selectedParents.append(self.Population[minFitIndex])
            fitness[minFitIndex] = 99999
        return selectedParents

    def performCrossOver(self, parents):
        numOfOffsprings = self.populationSize - len(parents)-1
        offsprings = [[0]*len(parents[0])]*numOfOffsprings
        crossoverpoint = randint(1, len(parents[0]))
        crossover_rate = 0.8
        for i in range(0, numOfOffsprings, 2):
            x = rd.random()
            if(x > crossover_rate):
                continue
            firstParent = parents[i]
            secondParent = parents[i+1]
            offsprings[i][0:crossoverpoint] = firstParent[0:crossoverpoint]
            offsprings[i][crossoverpoint:] = secondParent[crossoverpoint:]
        return offsprings

    def mutateOffspiring(self, offsprings):
        mutationRate = 0.4
        for i in range(len(offsprings)):
            x = rd.random()
            if(x > mutationRate):
                continue
            rnd1 = randint(0,len(offsprings[i])-1)
            rnd2 = randint(0,len(offsprings[i])-1)
            offsprings[i][rnd1],offsprings[i][rnd2] = offsprings[i][rnd2],offsprings[i][rnd1]
        return offsprings
    
    def EvaluateResult(self,fitness):
        minFitnessIndex = fitness.index(min(fitness))
        population = self.Population[minFitnessIndex]
        return population

    def runTSP(self):
        fitness_history = []
        for _ in range(self.maxGenerations):
            fitness = self.calculateFitness()
            fitness_history.append(fitness)
            if(EvaluateFitnessHistory(fitness_history,4)):
                return self.EvaluateResult(fitness)
            parents = self.selectFitParents(fitness)
            offsprings = self.performCrossOver(parents)
            mutants = self.mutateOffspiring(offsprings)
            self.Population[0:len(parents)] = parents
            self.Population[len(parents):] = mutants
        return self.EvaluateResult(fitness)

places = [0, 1, 2, 3, 4]
distanceGraph = [
    [float('inf'), 3, 6, 2, 3],
    [3, float('inf'), 5, 2, 3],
    [6, 5, float('inf'), 6, 4],
    [2, 2, 6, float('inf'), 6],
    [3, 3, 4, 6, float('inf')]
]
gen = Genetics(places,distanceGraph)
r = gen.runTSP()
print(r)
print(getDistance(r,distanceGraph))