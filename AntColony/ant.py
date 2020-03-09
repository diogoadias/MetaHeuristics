import sys
sys.path.append(".")

import numpy as np
from random import randint
from Greedy.Greedy import Greedy

class AntColony(object):

    def __init__(self, city_distances, n_ants, n_best, n_iterations, evaporation, alpha=1, beta=1):
       
        self.distances  = city_distances
        self.pheromone = np.zeros(self.distances.shape) / len(city_distances)       
        #self.all_itens = range(len(distances))
        self.n_ants = n_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.evaporation = evaporation
        self.alpha = alpha
        self.beta = beta
        self.best_all_times = (None, np.inf)

    def path_distances(self, path):
        total_distance = 0
        start = path[0]
        for i in range(1, len(path)):
            end = path[i]
            total_distance += self.distances[start][end]
            start = end
        return total_distance
    
    def ants_paths(self):
        paths = []
        for _ in range(self.n_ants):
            ant_path = self.generate_path()
            total_distance = self.path_distances(ant_path)            
            paths.append((ant_path, total_distance))

        self.spread_pheromone(paths)
        return paths
    
    def generate_path(self):
        path = []
        initial_city = randint(0, len(self.distances) -1)
        path.append(initial_city)

        for _ in range(len(self.distances) -1):
            next_city = self.move_to_next_city(path)
            path.append(next_city)
        return path

    def move_to_next_city(self, path):
        probs = self.calculate_probability(path)
        next_city = np.random.choice(len(self.distances), p=probs )

        return next_city

    def calculate_probability(self, path):
        probs = []
        actual_city = path[-1]
        for j in range(0, len(self.distances)):
            if j not in path:
                value = 1.0 / self.distances[actual_city][j]
                probs.append(value)
            else:
               probs.append(0.0)                

        #total_probs = sum(probs)
        
        for i in range(0, len(self.distances)):
            if i not in path:
                
                tax_pheromone = self.pheromone[actual_city][i] 
                distance = (1.0 / self.distances[actual_city][i])
                total_pheromone = sum(self.pheromone[actual_city])
                total_distances = sum(self.distances[actual_city]) - self.path_distances(path)

                value1 = (tax_pheromone ** self.alpha) * (distance ** self.beta)
                value2 = (total_pheromone ** self.alpha) * (total_distances ** self.beta)

                if value1 == 0 and value2 == 0:
                    final_value = 0.0
                else:
                    final_value = value1 / value2
                
                probs[i] = final_value
                
        return probs        

    def spread_pheromone(self, paths):
        q = 1.0 #quantity of pheromone spread
        sorted_paths = sorted(paths, key=lambda x: x[1])
        for path, distance in sorted_paths[:self.n_best]:
            for i, j in zip(path[0::1], path[1::1]):               
                self.pheromone[i][j] += ((1.0 - self.evaporation) * q) + (1.0 / distance)

    def run(self):
        best_path = []

        # gready = Greedy(self.distances.tolist())
        # greedy_path, greedy_total, stats = gready.run()

        # best_path.append((greedy_path, greedy_total))
        # self.spread_pheromone(best_path)

        for i in range(self.n_iterations):
            all_paths = self.ants_paths()
            self.spread_pheromone(all_paths)
            best_path = min(all_paths, key=lambda x: x[1])
            if best_path[1] < self.best_all_times[1]:
                self.best_all_times = best_path
           
        
        return self.best_all_times
