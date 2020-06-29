import sys
sys.path.append(".")

from ant import AntColony
from Util.TSPReader import TSPReader
from Greedy.Greedy import Greedy
import numpy as np
import time

start = time.time()

cities = TSPReader.read_tsplib("Util/a280.xml") # get distances for all cities
c = np.asarray(cities) # transform in numpy array

# distances, n_ants, n_best, n_iterations, evaporation
ant = AntColony(c, 10, 1, 100, 0.1) # R: 9705.55 T: 73.23 seg
#ant = AntColony(c, 10, 1, 100, 0.5) # R: 10345.60 T: 78.09 seg
#ant = AntColony(c, 10, 1, 1000, 0.1) # R: 8677.13 T: 728.56 seg
#ant = AntColony(c, 10, 1, 1000, 0.5) # R: 8280.19 T: 822.73 seg

#ant = AntColony(c, round(len(c)/2), 1, 100, 0.1) # R: 9652.22 T: 219.24 seg
#ant = AntColony(c, round(len(c)/2), 1, 100, 0.5) # R: 9635.15 T: 219.94 seg
#ant = AntColony(c, round(len(c)/2), 1, 1000, 0.1) # R: 8311.52 T: 2182.55 seg 
#ant = AntColony(c, round(len(c)/2), 1, 1000, 0.5) # R: 7848.23 T: 1965.01 seg 

#ant = AntColony(c, len(c), 1, 100, 0.1) # R: 9205.52 T: 449.39 seg
#ant = AntColony(c, len(c), 1, 100, 0.5) # R: 9390.97 T: 373.73 seg
#ant = AntColony(c, len(c), 1, 1000, 0.1) # R: 8280.19 T: 3870.20 seg 
#ant = AntColony(c, len(c), 1, 1000, 0.5) # R: 7933.30 T: 4485.96 seg 
           

result = ant.run()
print(result)

end = time.time()

print("TEMPO: ", end - start)