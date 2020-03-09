from Util.TSPReader import TSPReader

cities = TSPReader.read_tsplib("Util/berlin52.xml")

c = [1,49,32,45,19,41,8,9,10,43,33,51,11,52,14,13,47,26,27,28,12,25,4,6,15,5,24,
48,38,37,40,39,36,35,34,44,46,16,29,50,20,23,30,2,7,42,21,17,3,18,31,22]

total = 0.0
for i in range(0, len(cities)-1):
  total += cities[i][i+1]

print(total)