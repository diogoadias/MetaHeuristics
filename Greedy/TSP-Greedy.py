import sys
sys.path.append(".")

from Util.TSPReader import TSPReader
from Greedy import Greedy
import time

start = time.time()

cities = TSPReader.read_tsplib("Util/berlin52.xml")

gready = Greedy(cities)
path, total, stats = gready.run()


print("DISTANCE:", total)
print(path)

end = time.time()

print("TIME SPEND:", (end - start))

#PlotterResults.generatePlot(stats)
#PlotterResults.routePlot(path)