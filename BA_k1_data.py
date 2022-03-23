# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 22:47:20 2022

@author: whatf
"""

import Functions as fn
import numpy as np
from tqdm import tqdm

k1 = np.zeros((100, 9997))

for i in tqdm(range(100)):
    k1[i] = fn.BA_k1(2, int(1e4))

#%%

mean = np.mean(k1, axis=0)
std = np.std(k1, axis=0)

#%%

N = np.arange(3,1e4, 1)

import matplotlib

matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
matplotlib.rcParams['font.size'] = 12

colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
          '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

import matplotlib.pyplot as plt

fig, ax = plt.subplots(1,2, figsize=(6.0, 2.8))

ax[0].errorbar(N, mean, yerr=std,
               marker='.', linewidth=0, markersize=1.8, color=colors[0], 
               elinewidth=0.01, ecolor=colors[2])

ax[1].errorbar(N, mean, yerr=std,
               marker='.', linewidth=0, markersize=1.8, color=colors[3],
               elinewidth=1/N**0.6, ecolor=colors[4],
               label="Numerical data")

ax[1].set_xscale("log")
ax[1].set_yscale("log")

fig.text(0.5, 0.01, "Degree distribution $k$", ha='center')
fig.text(0.01, 0.5, "Largest degree $k_1$", va='center',
         rotation='vertical')

from numpy.polynomial import Polynomial

fit = Polynomial.fit(np.log(N[200:]), np.log(mean[200:]), 1, full=True)

lin = fit[0].convert()

ax[1].plot(N, np.exp(lin(np.log(N))), 
           color="#222222", linestyle="dashed", zorder=10,
           label="Least squares fit")

ax[1].legend()

fig.tight_layout(pad=0.2, rect=(0.04,0.04,0.98,0.98))

fig.savefig("BA_k1.eps")