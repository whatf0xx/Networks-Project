# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import networkx as nx

G = nx.Graph()

#nx.draw(G)
n = 20
G.add_nodes_from(i for i in range(n))

for i in range(n-1):
    for j in range(n-1-i):
        G.add_edge(i, i+j+1)
        
nx.draw(G)
nx.write_graphml(G, "./simple_connected_20.graphml")

#%%

import random

G = nx.Graph()
p = 0.3
n = 200

G.add_nodes_from(i for i in range(10))

for i in range(n-1):
    for j in range(n-1-i):
        if p > random.random():
            G.add_edge(i, i+j+1)
        
#nx.draw(G)
nx.write_graphml(G, f"./ER_{n}_{p}.graphml")

#%%

import random

G = nx.barabasi_albert_graph(10000, 3)

nx.write_graphml(G, f"built-in_BA.graphml")
