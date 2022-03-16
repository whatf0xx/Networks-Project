# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 16:08:02 2022

@author: whatf
"""

import pandas as pd
import numpy as np

raw = []
dists = []





for i in range(5):
    Data = pd.read_pickle(f"./BA_distributions{i+1}.pkl")
    m = list(Data.keys())
    raw.append(np.array([Data[i]["Raw data"] for i in m]))
    dists.append([Data[i]["Degree distribution"] for i in m])

import importlib

mod = importlib.import_module("logbin-2020")

raw_log_binned = []

for r in raw:    
    log_bins = []
    
    for ri in r:
        log_bins.append(mod.logbin(ri, 1.2))
        
    raw_log_binned.append(log_bins)

import matplotlib

matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
matplotlib.rcParams['font.size'] = 12

import matplotlib.pyplot as plt

fig, ax = plt.subplots(2, 3, figsize=(7.2, 4.8))

for e, mi in enumerate(m):
    i = int(e/3)
    j = e%3

    ax[i][j].set_xscale("log")
    ax[i][j].set_yscale("log")

    ax[i][j].set_title(f"m = {mi}")

    for k in range(5):
        ax[i][j].plot(raw_log_binned[k][1][0], raw_log_binned[k][1][1],
                '.')

ax[1][2].set_visible(False)

fig.text(0.5, 0.01, "Degree distribution $k$", ha='center')
fig.text(0.01, 0.5, "Probability density $p_\\infty(k)$", va='center',
         rotation='vertical')

fig.tight_layout(pad=0.4, rect=(0.04,0.04,0.96,0.96))