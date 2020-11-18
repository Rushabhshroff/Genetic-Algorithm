from random import randint
import random as rd


def NumToBinArray(num, l=4):
    # using format() + list comprehension
    # decimal to binary number conversion
    bi = [int(i) for i in bin(num)[2:].zfill(l)]
    return bi


def BinArrayToNum(arr):
    # join array of bits and convert it to its decimal using int
    return int(''.join([str(el) for el in arr]), 2)

def EvaluateFitnessHistory(history,overPriod = 4):
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

class Genetics:
    def __init__(self, values, weights, weightLimit, maxGenerations=50, populationSize=8):
        self.values = values
        self.weights = weights
        self.weightLimit = weightLimit
        self.maxGenerations = maxGenerations
        self.populationSize = populationSize
        self.Population = [NumToBinArray(
            randint(1, len(self.values)),len(self.values)) for _ in range(self.populationSize)]

    def calculateFitness(self):
        fitness = [0]*len(self.Population)
        for i in range(len(self.Population)):
            s1 = sum([self.Population[i][j] * self.values[j] for j in range(len(self.Population[i]))])
            s2 = sum([self.Population[i][j] * self.weights[j] for j in range(len(self.Population[i]))])
            if(s2 < self.weightLimit):
                fitness[i] = s1
        return fitness

    def selectFitParents(self,fitness):
        numOfParent = int(self.populationSize/2)
        fitnesses = list(fitness)
        selectedParents = []
        for _ in range(numOfParent):
            maxFitIndex = fitnesses.index(max(fitnesses))
            selectedParents.append(self.Population[maxFitIndex])
            fitness[maxFitIndex] = -99999
        return selectedParents

    def performCrossOver(self, parents):
        numOfOffsprings = self.populationSize - len(parents)
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
            rnd = randint(0,len(offsprings[i])-1)
            offsprings[i][rnd] = 1 - offsprings[i][rnd]
        return offsprings
    
    def EvaluateResult(self,fitness):
        maxFitnessIndex = fitness.index(max(fitness))
        population = self.Population[maxFitnessIndex]
        return population

    def runKnapSack(self):
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


values = [12,5,10,7]
weights = [5,3,7,2]

gen = Genetics(values,weights,13)
op = gen.runKnapSack()
print(op)

