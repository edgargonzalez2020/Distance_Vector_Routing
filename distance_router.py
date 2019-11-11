from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
import csv
import sys
class Network:
    def __init__(self, routers):
        self.routers = routers
        self.network = self.load_network()
        self.nodes = [Node(self.routers, x) for x in range(1,self.uniq + 1)]
    def load_network(self):
        unique_nodes = set()
        for x in self.routers:
            for y in x[:-1]:
                unique_nodes.add(y)
        self.uniq = len(unique_nodes)
        self.graph = [[16 for _ in range(self.uniq)] for _ in range(self.uniq)]
        for x in self.routers:
            a = int(x[0]) - 1
            b = int(x[1]) - 1
            cost = int(x[2])
            self.graph[a][b] = cost
            self.graph[b][a] = cost
    def broadcast(self):
        is_stable_state = False
        temp = 0
        while( not is_stable_state ):
            for x in self.nodes:
                neighbor_table = x.get_neighbors()
                for i,y in enumerate(neighbor_table):
                    if y > 0:
                        dvt = self.nodes[i].dvt
                        is_stable_state = x.updateDVT(dvt)
                        if not is_stable_state:
                            temp += 1
            is_stable_state = True if temp == 0 else False
class Node:
    def __init__(self, routers, router_id):
        self.routers = routers
        self.router_id= router_id
        unique_nodes = set()
        for x in self.routers:
            for y in x[:-1]:
                unique_nodes.add(y)
        self.uniq = len(unique_nodes)
        self.graph = [[16 for _ in range(self.uniq)] for _ in range(self.uniq)]
        for x in range(len(self.routers)):
            for y in range(len(self.routers[int(y)]) - 1):
                if self.router_id == int(self.routers[int(x)][int(y)]):
                    a = int(self.routers[int(x)][0])
                    b = int(self.routers[int(x)][1])
                    cost = int(self.routers[int(x)][2])
                    self.graph[a - 1][b - 1] = cost
                    self.graph[b - 1][a - 1] = cost
        self.graph[self.router_id - 1][self.router_id - 1] = 0
        self.dvt = self.graph
    def get_neighbors(self):
        packet = [0 for _ in range(len(self.dvt[0]))]
        for i,x in enumerate(self.dvt[self.router_id - 1]):
            if x < 16:
                packet[i] = x
        return packet
    def updateDVT(self, table):
        temp = 0
        for x in range(len(self.dvt)):
            for y in range(len(self.dvt[x])):
                if self.dvt[x][y] > table[x][y] and table[x][y] < 16:
                    print("DVT updated")
                    self.dvt[x][y] = table[x][y]
                    temp += 1
        return False if temp > 0 else True
def main():
    routers = [x for x in csv.reader(open("input.txt"), delimiter=" ")]
    topology = Network(routers).broadcast()
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: [path_to_file]")
    else:
        main()
