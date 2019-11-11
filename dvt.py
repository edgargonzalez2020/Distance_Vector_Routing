import sys
import csv
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
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
                if neighbor_table[x][y] < self.dvt[x][y] and neighbor_table[x][y] < 16:
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
        routing_label = Label(self.master, text="Routing Table").grid(row=0,columnspan=3)
        cols = ("Source", "Destination", "Weight")
        tree = ttk.Treeview(self.master, columns=cols, show="headings")
        for col in cols:
            tree.heading(col, text=col)
        tree.grid(row=1,column=0,columnspan=2)
        idx = 1
        for x in range(len(self.node.graph)):
            for y in range(len(self.node.graph[x])):
                source = x + 1
                dest = y + 1
                cost = self.node.graph[x][y]
                tree.insert("", "end", values=(source,dest,cost))
                idx += 1
        dvt_label = Label(self.master, text="Distance Vector Table").grid(row=idx + 1,columnspan=3)
        dvt_tree = ttk.Treeview(self.master, columns=cols, show="headings")
        for col in cols:
            dvt_tree.heading(col, text=col)
        dvt_tree.grid(row=idx+2,column=0, columnspan=2)
        for x in range(len(self.node.dvt)):
            for y in range(len(self.node.dvt[x])):
                source = x + 1
                dest = y + 1
                cost = self.node.dvt[x][y]
                dvt_tree.insert("", "end", values=(source,dest,cost))
def askopen(name):
    name.append(filedialog.askopenfilename())

def main():
    if len(sys.argv) < 2:
        print("usage: [path to file]")
    root = Tk()
    filename = []
    filebtn = Button(root, text="Open input file",command=askopen)
    filebtn.grid(row=0,column=0)
    routers = [x for x in csv.reader(open(filename[0]), delimiter=" ")]
    routers = [list(map(int, router)) for router in routers]
    topology = Network(routers, root)
    stable = True
    count = 0
    while stable:
        stable = topology.broadcast()
    topology.print()
    mainloop()
if __name__ == "__main__":
    main()


