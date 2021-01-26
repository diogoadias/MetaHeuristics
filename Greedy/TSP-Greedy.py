import sys
sys.path.append(".")

from Util.TSPReader import TSPReader
from Greedy import Greedy
import time

start = time.time()

cities = TSPReader.read_tsplib("Util/berlin52.xml")

best = float("inf")
best_path = None

for i in range(0, len(cities)):
    gready = Greedy(cities, i)
    path, total, stats = gready.run()

    if best > total:
        best = total
        best_path = path
    
    print("At interaction {} the best value is: {}", i, best)

print("DISTANCE:", best)
print(best_path)

end = time.time()

print("TIME SPEND:", (end - start))

#PlotterResults.generatePlot(stats)
#PlotterResults.routePlot(path)