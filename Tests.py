# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 00:26:18 2022

@author: whatf
"""

import Functions as fn

m = 4
N = int(1e4)

nodes, edges, k_predict, k_meas = fn.test_BA(m, N)

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