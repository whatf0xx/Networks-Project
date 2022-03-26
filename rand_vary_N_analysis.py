# -*- coding: utf-8 -*-
"""
Created on Sun Mar 20 14:59:23 2022

@author: whatf
"""

import pandas as pd

Data = pd.read_pickle("./rand_vary_N.pkl")
m = 3

import numpy as np

N = np.array(list(Data.keys()))

centres = []
val = []
err =[]

for n in N:

    v = Data[n]["Log-binned data"]
    c = Data[n]["Bin centres"]
    e = Data[n]["Associated errors"]
    
    centres.append(c[v != 0])
    err.append(e[v != 0])
    val.append(v[v != 0])


def p_inf(k):
    return 2*m*(m+1)/k/(k+1)/(k+2)

theory = p_inf(centres[-1])

import matplotlib

matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
matplotlib.rcParams['font.size'] = 12

colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
          '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

import matplotlib.pyplot as plt

fig = plt.figure(figsize=(6.0, 4.4))
ax = plt.axes()

ax.set_xscale("log")
ax.set_yscale("log")

for i, n in enumerate(N):

    ax.errorbar(centres[i], val[i], yerr=err[i],
            color = colors[i], marker = '.', linewidth = 0,
            elinewidth = 0.6, label=f"N = {n}")
    
ax.plot(centres[-1], theory, color='#222222', linestyle='dashed',
        label="Theoretical $p_\\infty(k)$")

ax.set_xlabel("$k$")
ax.set_ylabel("Probability $p(k)$")


ax.legend()

fig.savefig("./rand_vary_N.eps")

#%%
fig = plt.figure(figsize=(6.0, 4.4))
ax = plt.axes()

ax.set_xscale("log")
ax.set_yscale("log")

for i, n in enumerate(N):

    ax.errorbar(centres[i]/np.sqrt(n),
                val[i]*centres[i]*(centres[i]+1)*(centres[i]+2), 
                yerr=err[i]*centres[i]*(centres[i]+1)*(centres[i]+2),
            color = colors[i], marker = '.', linewidth = 0,
            elinewidth = 0, label=f"N = {n}")
    
ax.vlines(np.sqrt(12), 0, 60, color="#222222", linestyle="dashed",
          label="$\\sqrt{{m(m+1)}}$")

ax.set_xlabel("$k$ / $\\sqrt{{N}}$")
ax.set_ylabel("Modified probability $p(k) \\cdot k \\cdot (k+1) \\cdot (k+2)$")

ax.legend()

fig.tight_layout(rect=(-0.02,-0.04,0.98,0.98))

fig.savefig("rand_data_collapse.eps")