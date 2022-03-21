# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 12:51:08 2022

@author: whatf
"""

import pandas as pd

Data = pd.read_pickle("./BA_10_4_av_vary_m_d1.1.pkl")

m = Data.keys()

def p_inf(m, k):
    return 2*m*(m+1)/k/(k+1)/(k+2)

import matplotlib

matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
matplotlib.rcParams['font.size'] = 12

import matplotlib.pyplot as plt

fig, ax = plt.subplots(2, 3, figsize=(6.2, 3.8))

colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
          '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

for e, mi in enumerate(m):
    centres = Data[mi]["Bin centres"]
    
    data = Data[mi]["Log-binned data"][:len(centres)]
    errors = Data[mi]["Associated errors"][:len(centres)]
    
    centres = centres[data != 0]
    errors = errors[data != 0]
    data = data[data != 0]
    
    theory = p_inf(mi, centres)
    
    
    i = int(e/3)
    j = e%3

    ax[i][j].set_xscale("log")
    ax[i][j].set_yscale("log")

    ax[i][j].errorbar(centres, data, yerr = errors,
            color=colors[e], marker='.', linewidth=0, 
            elinewidth=1.0,
            zorder = 1, label=f"$m={mi}$")
    
    if e == 0:
        label = "Theoretical value"
    else:
        label = "__nolegend__"
    
    ax[i][j].plot(centres, theory,
                  zorder = 2, linestyle="dashed", color="#444444",
                  label = label)

ax[1][2].set_visible(False)

fig.text(0.5, 0.01, "Degree distribution $k$", ha='center')
fig.text(0.01, 0.5, "Probability density $p_\\infty(k)$", va='center',
         rotation='vertical')
fig.legend(loc=(0.7, 0.11))

fig.tight_layout(pad=0.2, rect=(0.04,0.04,0.98,0.98))

fig.savefig("varying_m.eps")

#%%

fig, ax = plt.subplots(2, 3, figsize=(7.2, 4.8))

for e, mi in enumerate(m):
    
    centres = Data[mi]["Bin centres"]
    
    data = Data[mi]["Log-binned data"][:len(centres)]
    errors = Data[mi]["Associated errors"][:len(centres)]
    
    centres = centres[data != 0]
    errors = errors[data != 0]
    data = data[data != 0]
    
    
    i = int(e/3)
    j = e%3

    ax[i][j].set_xscale("log")
    ax[i][j].set_yscale("log")

    ax[i][j].errorbar(centres, data*centres*(centres+1)*(centres+2),
                      yerr = errors*centres*(centres+1)*(centres+2),
            color=colors[e], marker='.', linewidth=0, 
            elinewidth=1.0, label=f"$m={mi}$")

ax[1][2].set_visible(False)

fig.text(0.5, 0.01, "Degree distribution $k$", ha='center')
mt = "Modified probability $p_\\infty(k) \\cdot k \\cdot (k+1) \\cdot (K+2)$"
fig.text(0.01, 0.5, mt, va='center',
         rotation='vertical')
fig.legend(loc=(0.72, 0.11))

fig.tight_layout(pad=0.4, rect=(0.04,0.04,0.96,0.96))

#%%

fig = plt.figure(figsize = (7.2,4.8))
ax = plt.axes()

ax.set_xscale("log")
ax.set_yscale("log")

for e, mi in enumerate(m):
    
    centres = Data[mi]["Bin centres"]
    
    data = Data[mi]["Log-binned data"][:len(centres)]
    errors = Data[mi]["Associated errors"][:len(centres)]
    
    centres = centres[data != 0]
    errors = errors[data != 0]
    data = data[data != 0]
    
    theory = p_inf(mi, centres)
    
    ax.errorbar(centres, data, yerr = errors,
            color=colors[e], marker='.', linewidth=0, 
            elinewidth=1.0,
            zorder = 1, label=f"$m={mi}$")
    
    if e == 0:
        label = "Theoretical value"
    else:
        label = "__nolegend__"
    
    ax.plot(centres, theory,
                  zorder = 2, linestyle="dashed", color="#444444",
                  label = label)
    
ax.set_xlabel("Degree distribution $k$", ha='center')
ax.set_ylabel("Probability density $p_\\infty(k)$")
ax.legend()