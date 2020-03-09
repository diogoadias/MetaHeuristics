from Util.TSPReader import TSPReader
from Util import PlotterResults
from Genetic.GA import GA
from Greedy.Greedy import Greedy
import collections
import time

def validateTSP(path):
    return [item for item, count in collections.Counter(path).items() if count > 1]

start = time.time()

cities = TSPReader.read_tsplib("Util/a280.xml")

gready = Greedy(cities)
path, total, stats = gready.run()

POPULATION_SIZE = len(cities)
N_ITERATIONS = 2000 # 2000 = 'min': 2685.585121077349
N_MATINGS = 50      # 50
    
ga = GA(POPULATION_SIZE, N_ITERATIONS, N_MATINGS, cities, path)
 
stats, population = ga.run()

end = time.time()

print("TIME SPEND:", (end - start))

print(stats[len(stats)-1])
print(population[len(population)-1])

PlotterResults.generatePlot(stats)