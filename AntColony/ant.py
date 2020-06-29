import numpy as np
from random import randint
from Greedy.Greedy import Greedy
from Util import Plot


class AntColony(object):

    def __init__(self, city_distances, n_ants, n_best, n_iterations, evaporation, alpha=1, beta=1):
       
        self.distances  = city_distances #matrix of distances between cities
        self.pheromone = np.ones(self.distances.shape) / len(city_distances) # create pheromone matrix       
        self.n_ants = n_ants # number of ants 
        self.n_best = n_best # quantity of best ants
        self.n_iterations = n_iterations # number of interactions
        self.evaporation = evaporation # evaporation tax
        self.alpha = alpha
        self.beta = beta
        self.best_all_times = (None, np.inf) # tuple of path and total distance

    #calculate distances between cities. Run to all cities to calculate total distance for a path
    def path_distances(self, path):
        total_distance = 0
        start = path[0]
        for i in range(1, len(path)):
            end = path[i]
            total_distance += self.distances[start][end]
            start = end
        return total_distance
    
    #define a path for an ant
    def ants_paths(self):
        paths = []
        for _ in range(self.n_ants):
            ant_path = self.generate_path() # generate a path for an ant
            total_distance = self.path_distances(ant_path) # calculate ant path            
            paths.append((ant_path, total_distance))

        return paths
    
    def generate_path(self):
        path = []
        initial_city = randint(0, len(self.distances) -1) # randomly define a initial city 
        path.append(initial_city) # add the city to an path

        for _ in range(len(self.distances) -1): # loop until quantity of cities -1 (because initial city is in path) 
            next_city = self.move_to_next_city(path) # select the next city to visit
            path.append(next_city)
        return path

    #decide what is the next city to visit
    def move_to_next_city(self, path):
        probs = self.calculate_probability(path) # define a probability to visit each city in a path
        next_city = np.random.choice(len(self.distances), p=probs) #select a city randomly using a probability of choice

        return next_city

    def calculate_probability(self, path):
        probs = []
        actual_city = path[-1] # get the last value of a list
        for j in range(0, len(self.distances)):
            if j not in path: # if city is not in path
                value = 1.0 / self.distances[actual_city][j] # distance between actual city and neighboor city
                probs.append(value)
            else:
               probs.append(0.0) # if in path do not used to calculate the probability                
        
        #total = sum(probs)

        for j in range(0, len(self.distances)):
            if j not in path:
                #probs[j] = (1.0 * probs[j]) / total
                total_pheromone = 0.0
                for i in range(0, len(self.pheromone[actual_city])):
                    if i not in path:
                        total_pheromone += self.pheromone[actual_city][i] # sum the total pheromone deposited in a  complete path
                
                tax_pheromone = self.pheromone[actual_city][j] # get the actual pheromone tax between two cities 
                distance = (1.0 / self.distances[actual_city][j])
                total_distances = sum(self.distances[actual_city]) - self.path_distances(path) # remove the sum of distances that are in path 
                value1 = (tax_pheromone ** self.alpha) * (distance ** self.beta)
                value2 = (total_pheromone ** self.alpha) * (total_distances ** self.beta)

                final_value = value1 / value2 # probability to choose this city from actual city                
                probs[j] = final_value # add to
                        
        print(sum(probs))
        return probs / sum(probs) # normalize small probababilities in a path

    def spread_pheromone(self, paths):
        q = 1.0 #quantity of pheromone spread
        sorted_paths = sorted(paths, key=lambda x: x[1]) #ordering paths 
        for path, distance in sorted_paths[:self.n_best]: # select the n_best paths
            for i, j in zip(path[0::1], path[1::1]):               
                self.pheromone[i][j] += ((1.0 - self.evaporation) * q) + (1.0 / distance) #update pheromone in the path

    def run(self):
        best_path = []
        #best_gready_path = []
        #all_gready_path = []
        
        # for i in range(self.n_iterations):
        #     for i in range(0, len(self.distances)):
        #         initial_city = randint(0, len(self.distances) -1)
        #         gready = Greedy(self.distances.tolist(), initial_city)
        #         gready_path, gready_total, stats = gready.run()
        #         all_gready_path.append((gready_path, gready_total))
                

        #     self.spread_pheromone(all_gready_path)    
        #     best_gready_path = min(all_gready_path, key=lambda x: x[1])
        #     self.best_all_times = best_gready_path
            #self.spread_pheromone(self.best_all_times)

        # print("BEST SO FAR:", self.best_all_times)
        # print("ITERATION:", "GREADY")   
        for i in range(self.n_iterations): #define number of interactions
            all_paths = self.ants_paths() # all paths define for each ant
            self.spread_pheromone(all_paths) # update pheromone spread in a path
            best_path = min(all_paths, key=lambda x: x[1]) # select the best path
            if best_path[1] < self.best_all_times[1]: # compare with the best of all times path
                self.best_all_times = best_path
                print("BEST SO FAR:", self.best_all_times)
                print("ITERATION:", i)
        
        
        return self.best_all_times
