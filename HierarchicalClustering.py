import csv
import math
from itertools import combinations

COUNT = 0

def increment():
    global COUNT
    COUNT = COUNT+5

def decrement():
    global COUNT
    COUNT = COUNT-5

def average(lst):
    return sum(lst) / len(lst)

def iterFlatten(root):
    if isinstance(root, (list, tuple)):
        for element in root:
            for e in iterFlatten(element):
                yield e
    else:
        yield root

def izris(lst):
    if len(lst) != 1:
        increment()
        izris(lst[0])
        for space in range(COUNT-5):
            print(" ", end="")
        print("----|")
        izris(lst[1])
        decrement()
    else:
        for space in range(COUNT):
            print(" ", end="")
        print("---- " + lst[0])


class HierarchicalClustering:
    def __init__(self, filename):
        f = open(filename, "r", encoding="latin1")

        self.values = {}
        self.countries = []

        for line in csv.reader(f):
            if not line[0].isdigit():
                temp = line[16:]
                countries1 = [val.rstrip() for val in temp]
                self.values = {country: [] for country in countries1 if country is not ''}
            else:
                self.countries.append(line[1])
                points = line[16:]
                index = 0
                for point in points:
                    if countries1[index] is not '':
                        self.values[countries1[index]].append(point)
                        index = index + 1

        self.clusters = [[name] for name in self.values.keys()]

    def __call__(self):
        while (len(self.clusters) != 1):
            closestPair = hc.closest_cluster()
            self.clusters.append([closestPair[0], closestPair[1]])
            self.clusters.remove(closestPair[0])
            self.clusters.remove(closestPair[1])
        print(self.clusters)
        izris(self.clusters[0])

    def row_distance(self, r1, r2):
        N = 0
        for i, j in zip(self.values[r1], self.values[r2]):
            if i and j is not '':
                N = N + 1
        if N is 0:
            return None

        return math.sqrt(sum((float(a) - float(b)) ** 2
                             for a, b in zip(self.values[r1], self.values[r2]) if (a is not '') and (b is not '')) / N)

    def cluster_distance(self, c1, c2):
        y = []
        for a in c1:
            for b in c2:
                val = self.row_distance(a, b)
                if val != None:
                    y.append(val)
        if len(y) == 0:
            return None
        return average(y)

    def closest_cluster(self):
        x = []
        for c1, c2 in combinations(self.clusters, 2):
            d = self.cluster_distance(iterFlatten(c1), iterFlatten(c2))
            if d != None:
                x.append((d, (c1, c2)))
        dis, pair = min(x)
        return pair


if __name__ == "__main__":
    hc = HierarchicalClustering("inputfiles/eurovision-final.csv")
    hc()
