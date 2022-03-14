# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 00:26:18 2022

@author: whatf
"""

import Functions as fn

m = 34
N = int(1e3)

nodes, edges, norm, k_predict, k_meas = fn.test_BA(m, N)

#%%

import matplotlib

matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
matplotlib.rcParams['font.size'] = 12

import matplotlib.pyplot as plt

fig = plt.figure()
ax = plt.axes()

ax.plot(nodes[::20],
        'o', color="blue", markersize=2.6, label="Nodes")
ax.plot(edges[::20],
        'o', color="green", markersize=2.6, label="Edges")

ax.set_xlabel("Time")
ax.set_ylabel("Number")
ax.legend()

#%%

import Functions as fn
import numpy as np

m = [int(mi) for mi in np.logspace(1, 4, 4, base=2)]
N = int(1e4)

nodes = []
edges = []
norm =  []

for mi in m:
    n, e, nm, k_predict, k_meas = fn.test_BA(mi, N)
    nodes.append(n)
    edges.append(e)
    norm.append(nm)

#%%

m = [int(mi) for mi in np.logspace(1, 4, 4, base=2)]
N = int(1e4)

import matplotlib

matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
matplotlib.rcParams['font.size'] = 12

import matplotlib.pyplot as plt

fig, ax = plt.subplots(2, 2, figsize=(6.2, 3.6))

ms = 2.2
skips = 300

from numpy.polynomial import Polynomial

for e, me in enumerate(m):
    i = int(e/2)
    j = e%2

    t = np.arange(0, N-me, 1)

    ax[i][j].plot(t[::skips], nodes[e][::skips],
            'o', color="blue", markersize=ms, label="Nodes")
    ax[i][j].plot(t[::skips], edges[e][::skips],
            'o', color="green", markersize=ms, label="Edges")
    
    nodes_fit = Polynomial.fit(t, nodes[e], 1).convert()
    ax[i][j].plot(nodes_fit(t),
                  color="grey", linestyle="-")
    
    edges_fit = Polynomial.fit(t, edges[e], 1).convert()
    ax[i][j].plot(edges_fit(t),
                  color="grey", linestyle="-")
    
    #ax[i][j].legend()
    ax[i][j].set_title(f"$m = {me}$")
    
    ax2=ax[i][j].twinx()
    ax2.plot(t[::skips], norm[e][::skips],
             'o', color="#cc5500", markersize=ms, label="Summed distribution")
    
    
    t = np.arange(0, N-me-1, 1)
    norm_fit = Polynomial.fit(t, norm[e], 1).convert()
    ax2.plot(norm_fit(t),
                  color="grey", linestyle="-")
    
    ax2.set_ylim(0, 1.1)
    
fig.text(0.5, 0.01, "Time", ha='center')
fig.text(0.01, 0.35, "Number", va='center',
         rotation='vertical')
fig.text(0.01, 0.5, "(nodes)", va='center',
         rotation='vertical', color="blue")
fig.text(0.01, 0.64, "(edges)", va='center',
         rotation='vertical', color="green")

fig.text(0.94, 0.5, "Summed probability", va='center',
         rotation='vertical', color="#cc5500")

fig.tight_layout(pad=0.4, rect=(0.03,0.02,0.94,1.0))

fig.savefig("tests1.eps")

#%%

fig = plt.figure()
ax = plt.axes()

ax.plot(k_predict,
        'o', color="blue", markersize=0.8, label="Prediction")
ax.plot(k_meas,
        'o', color="green", markersize=0.8, label="Measured")

#ax.set_xscale("log")
#ax.set_yscale("log")

ax.set_xlabel("Time")
ax.set_ylabel("Degree of chosen nodes")
ax.legend()

"""
k_predict significantly overestimates the degree of the chosen nodes. This is
because k_predict does not take into account that a node can only be picked
once, which lowers the degree of the average chosen node in practice, but not
in the overly simply model presented here.
"""

#%%

fig = plt.figure()
ax = plt.axes()

ax.plot(norm,
        'o', color="grey", markersize=1.0, label="Summed probabilities")

ax.set_xlabel("Time")
ax.set_ylabel("Probability")
ax.legend()

#%%

import Functions as fn
import numpy as np

m = 32
N = int(1e4)

mu_k = fn.test2_BA(m, N)

#%%

fig = plt.figure()
ax = plt.axes()

ax.plot(np.array(mu_k)/(2*m),
        'o', color="grey", markersize=1.0, label="Measured value")
ax.hlines(1+np.zeros_like(mu_k), 0, len(mu_k)+50,
          color="blue", linestyle="dashed", linewidth=0.9,
          label="Mean-field limit prediction")

ax.set_xlabel("Time")
ax.set_ylabel("$\\langle k \\rangle / 2m$")
ax.legend()

#%%

import Functions as fn
import numpy as np

m = [int(n) for n in np.logspace(2, 5, 4, base=2)]
N = int(1e4)

mu_k = []

for i in m:
    mu_k.append(fn.test2_BA(i, N))
    
#%%

fig, ax = plt.subplots(2, 2)
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

for e, M in enumerate(mu_k):
    i = int(e/2)
    j = e%2
    ax[i][j].plot(np.array(M)/(2*m[e]),
            'o', color=colors[e], markersize=1.0, label=f"m = {m[e]}")
    ax[i][j].hlines(1+np.zeros_like(M), 0, len(M)+50,
              color="grey", linestyle="dashed", linewidth=0.9)
    
fig.text(0.5, 0.01, "Time", ha='center')
fig.text(0.01, 0.5, "$\\langle k \\rangle / 2m$", va='center',
         rotation='vertical')

fig.legend(loc=(0.72, 0.54))

fig.savefig("k_mean_convergence_visual.eps")

#%%

m = [int(n) for n in np.logspace(2, 5, 4, base=2)]
N = int(1e4)

fig, ax = plt.subplots(2, 2, figsize=(6.2, 4.0))
diffs = []
skip = 2
for e, M in enumerate(m):
    diffs.append(1 - np.array(mu_k[e])/(2*M))
    
from numpy.polynomial import Polynomial

for e, D in enumerate(diffs):
    i = int(e/2)
    j = e%2
    
    t = np.arange(0, N-m[e]-1, 1)
    
    ax[i][j].plot(t[::skip], D[::skip],
            'x', color=colors[e], markersize=1.0, label=f"m = {m[e]}")
    ax[i][j].set_yscale("log")
    ax[i][j].set_xscale("log")
    ax[i][j].set_title(f"m = {m[e]}")
    #ax[i][j].legend()
    
    
    fit = Polynomial.fit(np.log(t[500:]), np.log(D[500:]), 1).convert()
    
    ax[i][j].plot(t[1:], np.exp(fit(np.log(t[1:]))),
                  color="grey", linestyle="dashed")
    
    
    
fig.text(0.5, 0.01, "Time", ha='center')
fig.text(0.01, 0.5, "Deviation from theoretical value", va='center',
         rotation='vertical')

fig.tight_layout(pad=0.2, rect=(0.03, 0.02, 0.98, 0.98))

fig.savefig("tests2.eps")