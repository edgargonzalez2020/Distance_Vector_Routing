import sys
import csv
from tkinter import *
class Network:
    def __init__(self, routers, root):
        self.routers = routers
        self.initialize_network()
        self.nodes = [Node(routers,self.uniq,x, root) for x in range(1, self.uniq + 1)]
    def initialize_network(self):
        unique_nodes = set()
        for x in self.routers:
            for y in x[:-1]:
                unique_nodes.add(y)
        self.uniq = len(unique_nodes)
        self.graph = [[16 for _ in range(self.uniq)] for _ in range(self.uniq)]
    def broadcast(self):
        count = 0
        for i, x in enumerate(self.nodes):
            neighbors = x.get_neighbors()
            for j, y in enumerate(neighbors):
                if y > 0:
                    dvt = self.nodes[j].dvt
                    did_change = self.nodes[i].update_dvt(dvt)
                    if did_change:
                        count += 1
        return True if count > 0 else False
    def print(self):
        for i,x in enumerate(self.nodes):
            print(f'Node {i + 1}')
            x.print()
class Node:
    def __init__(self, routers, uniq,router_id, root):
        self.graph = [[16 for _ in range(uniq)] for _ in range(uniq)]
        self.router_id = router_id
        for x in range(len(routers)):
            for y in range(len(routers[x]) - 1):
                if routers[x][y] == self.router_id:
                    a = routers[x][0] - 1
                    b = routers[x][1] - 1
                    cost = routers[x][2]
                    self.graph[a][b] = cost
                    self.graph[b][a] = cost
        self.graph[self.router_id - 1][self.router_id - 1] = 0
        self.dvt = self.graph
        self.gui = GUI(f"Node {self.router_id}", self, root)
    def print(self):
        for x in self.dvt:
            print(x)
    def get_neighbors(self):
        neighbors = [0 for x in range(len(self.dvt[0]))]
        for i,x in enumerate(self.dvt[self.router_id - 1]):
            if x < 16:
                neighbors[i] = x
        return neighbors
    def update_dvt(self, neighbor_table):
        did_change = False
        count = 0
        for x in range(len(neighbor_table)):
            for y in range(len(neighbor_table[x])):
                if neighbor_table[x][y] < self.dvt[x][y] and neighbor_table[x][y] < 16 and neighbor_table[x][y] != 0:
                    self.dvt[x][y] = neighbor_table[x][y]
                    self.dvt[y][x] = neighbor_table[y][x]
                    did_change = True
                    if did_change:
                        count += 1
        return True if count > 0 else False

class GUI:
    def __init__(self, title, node, master = None):
        self.master = Toplevel(master)
        self.node = node
        self.master.title(title)
        h = 250
        w = 400
        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()

        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)

        self.master.geometry(f"{w}x{h}+{int(x)}+{int(y)}")
        dvt_label = Label(self.master, text="Distance Vector Table")
        dvt_label.grid(row=0, column=0)
        height = 12
        width = 6
        for i in range(1,height + 1):
            if i == 6:
                routing_label = Label(self.master, text="Routing Table")
                routing_label.grid(row=i,column=0)
                continue
            for j in range(width + 1):
                b = Entry(self.master, width=10)
                b.grid(row=i,column=j)


def main():
    if len(sys.argv) < 2:
        print("usage: [path to file]")
    root = Tk()
    routers = [x for x in csv.reader(open("input.txt"), delimiter=" ")]
    routers = [list(map(int, router)) for router in routers]
    topology = Network(routers, root)
    stable = True
    count = 0
    while stable:
        stable = topology.broadcast()
    topology.print()
    #mainloop()
if __name__ == "__main__":
    main()

