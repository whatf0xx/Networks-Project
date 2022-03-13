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

ax.plot(nodes,
        'o', color="blue", markersize=0.8, label="Nodes")
ax.plot(edges,
        'o', color="green", markersize=0.8, label="Edges")

ax.set_xlabel("Time")
ax.set_ylabel("Number")
ax.legend()

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

m = [int(n) for n in np.logspace(3, 5, 4, base=2)]
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

fig, ax = plt.subplots(2, 2)
diffs = []

for e, M in enumerate(m):
    diffs.append(1 - np.array(mu_k[e])/(2*M))
    
from numpy.polynomial import Polynomial

for e, D in enumerate(diffs):
    i = int(e/2)
    j = e%2
    ax[i][j].plot(D,
            'x', color=colors[e], markersize=1.0, label=f"m = {m[e]}")
    ax[i][j].set_yscale("log")
    ax[i][j].set_xscale("log")
    ax[i][j].legend()
    
    
    
fig.text(0.5, 0.01, "Time", ha='center')
fig.text(0.01, 0.5, "$\\langle k \\rangle / 2m$", va='center',
         rotation='vertical')