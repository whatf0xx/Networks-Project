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

G = nx.barabasi_albert_graph(1000, 3)

nx.write_graphml(G, f"built-in_BA.graphml")

#%%

import Functions as fn

m = 4
G = fn.seed(m)
#nx.draw(G)

degree_bin = fn.make_list(100, m)
fn.BA_step(G, degree_bin, m, 0)
#it works for the first step!!

#%%

import Functions as fn

m = 4
N = 10
G = fn.seed(m)
degree_bin = fn.make_list(N, m)

for t in range(N-m-1):
    fn.BA_step(G, degree_bin, m, t)
    
#%%

import Functions as fn

m = 5
N = int(1e4)

G, degrees = fn.gen_BA(m, N, dist=True)

#%%

import Functions as fn
import time
import numpy as np

m = 3
N = [int(n) for n in np.logspace(2, 5, 16)]

times = []

for n in N:
    t0 = time.perf_counter()
    G, degrees = fn.gen_BA(m, n, dist=True)
    t1 = time.perf_counter()
    
    times.append(t1-t0)
    del(G)
    del(degrees)
    
#%%

import matplotlib

matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
matplotlib.rcParams['font.size'] = 12

import matplotlib.pyplot as plt

fig = plt.figure()
ax = plt.axes()

ax.plot(N, times, 'bx')

ax.set_yscale("log")
ax.set_xscale("log")

ax.set_title("Time complexity for generating a BA network, $m = 3$")
ax.set_xlabel("System size $N$")
ax.set_ylabel("Runtime (seconds)")

fig.tight_layout(rect=(0, 0, 0.95, 1))
fig.savefig("./time_complexity_m3.eps")