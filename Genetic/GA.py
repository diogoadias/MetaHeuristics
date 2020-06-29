import random
import numpy as np
from deap import base, creator, tools

class GA:
    def __init__(self, population_size, iterations, n_matings, cities, path):
        self.population = population_size # size of population
        self.iterations = iterations # number of interactions
        self.matings = n_matings # quantity of matings to be realize
        self.cities = cities #matrix of instance distance between cities
        self.greedy = path # gready path
       
        self.initConfig()

    def initConfig(self):
        #Min
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,)) # set min fitness
        creator.create("Individual", list, fitness=creator.FitnessMin) #create a list of individuals

        self.toolbox = base.Toolbox()

        #permutation setup for individual
        self.toolbox.register("indices", random.sample, range(self.population), self.population)
        self.toolbox.register("individual", tools.initIterate, creator.Individual, self.toolbox.indices)
        
        #population setup
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

        self.toolbox.register("evaluate", self.evaluateGA)
        self.toolbox.register("mate", tools.cxOrdered)
        self.toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.01)
        self.toolbox.register("select", tools.selTournament, tournsize=10)     
        
    def fitness(self, population):
        fitnesses = [(individual, self.toolbox.evaluate(individual)) for individual in population]
        
        for indivivual, fitness in fitnesses:
            indivivual.fitness.values = (fitness,)

    def offspring(self, population):
        n = len(population)
        for _ in range(self.matings):
            ind1, ind2 = np.random.choice(range(n), size=2, replace=False)

            offspring1, offspring2 = self.toolbox.mate(population[ind1], population[ind2])

            yield self.toolbox.mutate(offspring1)[0]
            yield self.toolbox.mutate(offspring2)[0]

    @staticmethod
    def pull_stats(population, iteration=1):
        fitnesses = [ individual.fitness.values[0] for individual in population ]
        return {
            'i': iteration,
            'mu': np.mean(fitnesses),
            'std': np.std(fitnesses),
            'max': np.max(fitnesses),
            'min': np.min(fitnesses)
        }  

    def evaluateGA(self, individual):
        distances = 0
        start = individual[0]
        for i in range(1, len(individual)):
            end = individual[i]
            distances += self.cities[start][end]
            start = end
        return distances
        
    def run(self):
        population = self.toolbox.population(n=self.population) # generate a population
       
        greedy = creator.Individual(self.greedy)    
        for i in range(0, 2):
            population[i] = greedy  

        self.fitness(population)

        stats = []
        for iteration in list(range(1, self.iterations)):
            current_population = list(map(self.toolbox.clone, population))
            offspring = list(self.offspring(current_population))
            for child in offspring:
                current_population.append(child)

            #reset fitness
            self.fitness(current_population)

            population[:] = self.toolbox.select(current_population, len(population)) # get the bests N of all population and remove others
            stats.append(GA.pull_stats(population, iteration))
        
        return stats, population