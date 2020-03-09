import collections
import numpy as np
from random import randint

class Greedy:
    def __init__(self, cities, initial_city=None):
        self.cities = cities
        self.initial_city = initial_city
        self.path = []
        self.total_lenght = 0.0
   
    def validateTSP(self, path):
        return [item for item, count in collections.Counter(path).items() if count > 1]

    def run(self):
        stats = []
        if(self.initial_city == None):
            initial_city = randint(0, len(self.cities) -1)
            self.path.append(initial_city)
        else:
            self.path.append(self.initial_city)
               
        for i in range(0, len(self.cities)-1):        
            city_lenght = min(k for k in self.cities[i] if k > 0)
            index = self.cities[i].index(city_lenght)       
            if index in self.path:
                while index in self.path:
                    self.cities[i][index] = 0
                    city_lenght = min(k for k in self.cities[i] if k > 0)
                    index = self.cities[i].index(city_lenght)
            
            self.total_lenght += city_lenght
            self.path.append(index)
            stats.append(Greedy.pull_stats(self.total_lenght, i))

        return self.path, self.total_lenght, stats

    @staticmethod
    def pull_stats(cities, iteration=1):
        #fitnesses = [ individual.fitness.values[0] for individual in population ]
        return {
        'i': iteration,
        'mu': np.mean(cities),
        'std': np.std(cities),
        'max': np.max(cities),
        'min': np.min(cities)
        }