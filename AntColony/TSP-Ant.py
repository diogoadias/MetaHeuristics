import sys
sys.path.append(".")

from ant import AntColony
from Util.TSPReader import TSPReader
from Greedy.Greedy import Greedy
import numpy as np
import time

start = time.time()

cities = TSPReader.read_tsplib("Util/berlin52.xml")
c = np.asarray(cities) 

# distances, n_ants, n_best, n_iterations, evaporation
ant = AntColony(c, len(c), 1, 1000, 0.5)

result = ant.run()
print(result)

end = time.time()

print("TEMPO: ", end - start)