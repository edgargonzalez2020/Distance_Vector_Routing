import time
import sys
import csv
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

#wrapper class, responsible for network initailization paramaters and running the dvt algorith
class Network:
    #constructor, takes in a list of src,dest,cost arrays and a root paramater for the gui
    def __init__(self, routers, root):
        self.routers = routers
        #initialize all network paramaters
        self.initialize_network()
        #populate nodes list this is gonna be an array with as many unique nodes in the networl
        self.nodes = [Node(routers,self.uniq,x, root) for x in range(1, self.uniq + 1)]
    def initialize_network(self):
        #count the amount of unique nodes in the set not including the cost of course
        unique_nodes = set()
        for x in self.routers:
            for y in x[:-1]:
                unique_nodes.add(y)
        self.uniq = len(unique_nodes)
    #the backbone of the algorithm returns True if the system is not stable and False if it is
    def broadcast(self):
        count = 0
        #loop through the neigbors
        for i, x in enumerate(self.nodes):
            neighbors = x.get_neighbors()
            for j, y in enumerate(neighbors):
                #if the distance is greater than 0 check their Distance Vector Table(DVT)
                if y > 0:
                    dvt = self.nodes[j].dvt
                    #calculate if the current nodes DVT has been changed
                    #used to check if the system is stable
                    did_change = self.nodes[i].update_dvt(dvt)
                    if did_change:
                        count += 1
        return True if count > 0 else False
    #helper function to print the system
    def print(self):
        for i,x in enumerate(self.nodes):
            print(f'Node {i + 1}')
            x.print()
    #this is to start the gui after the network has achieved equilibrium
    def init_gui(self):
        for x in self.nodes:
            x.init_gui()
#Wrapper class that describes a router
class Node:
    #Takes in a list of src,des,cost arrays as well as the node id starting at 1
    #also the root for the gui
    def __init__(self, routers, uniq,router_id, root):
        self.root = root
        #initialize the router table
        self.graph = [[16 for _ in range(uniq)] for _ in range(uniq)]
        self.router_id = router_id
        #loop through array and update links
        for x in range(len(routers)):
            for y in range(len(routers[x]) - 1):
                if routers[x][y] == self.router_id:
                    a = routers[x][0] - 1
                    b = routers[x][1] - 1
                    cost = routers[x][2]
                    self.graph[a][b] = cost
                    self.graph[b][a] = cost
        #initialize the cost of the current nodes self to 0
        self.graph[self.router_id - 1][self.router_id - 1] = 0
        self.dvt = self.graph
    #helper function to print the system
    def print(self):
        for x in self.dvt:
            print(x)
    def get_neighbors(self):
        #loops through the graph array and finds the distance to the neighbors
        neighbors = [0 for x in range(len(self.dvt[0]))]
        for i,x in enumerate(self.dvt[self.router_id - 1]):
            if x < 16:
                neighbors[i] = x
        return neighbors
    #initialized the gui
    def init_gui(self):
        self.gui = GUI(f"Node {self.router_id}", self, self.root)
    def update_dvt(self, neighbor_table):
        #loops through the neighbor table and checks to see if there is any nodes whose cost is lower than the
        #current cost
        did_change = False
        count = 0
        for x in range(len(neighbor_table)):
            for y in range(len(neighbor_table[x])):
                if neighbor_table[x][y] < self.dvt[x][y] and neighbor_table[x][y] < 16:
                    #make the graph bi-directional
                    self.dvt[x][y] = neighbor_table[x][y]
                    self.dvt[y][x] = neighbor_table[y][x]
                    did_change = True
                    if did_change:
                        count += 1
        return True if count > 0 else False

#gui class to hanfle gui stuff
class GUI:
    def __init__(self, title, node, master = None):
        #we need this line in order to have multiple windows
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

def main():
    if len(sys.argv) < 2:
        print("usage: [path to input]")
        return
    root = Tk()
    # read in routers from file
    routers = [x for x in csv.reader(open(sys.argv[1]), delimiter=" ")]
    # cast them all to ints
    routers = [list(map(int, router)) for router in routers]
    #initialize the the network with the values from the file
    topology = Network(routers, root)
    stable = True
    count = 0
    start = time.time()
    #boradcast neighbor dvt's until the system reaches equilibirum
    while stable:
        stable = topology.broadcast()
    end = time.time()
    topology.init_gui()
    time_label = Label(root, text=f"Time elapased: {(end-start) * 1000:.4f}ms")
    time_label.grid(row=0,column=0)
    stable_label = Label(root, text="Stable", fg="red")
    stable_label.grid(row=2,column=0)
    topology.print()
    mainloop()
if __name__ == "__main__":
    main()
