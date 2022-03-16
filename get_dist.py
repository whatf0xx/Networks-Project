# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 15:42:57 2022

@author: whatf
"""

import Functions as fn
import numpy as np

m = [int(i) for i in np.logspace(1, 5, 5, base=2)]
N = int(1e5)

degs = []
dists = []

from tqdm import tqdm

for mi in tqdm(m):
    degrees = fn.dist_BA(mi, N)
    degs.append(degrees)
    dist = np.bincount(degrees)
    index = np.arange(0, max(dist)+1, 1)
    dists.append({i:d for (i,d) in zip(index, dist)})
    
#%%

import pandas as pd

Data = pd.DataFrame(
    {mi:(ri, di) for (mi, ri, di) in zip(
        m, degs, dists)},
    index=["Raw data", "Degree distribution"])

Data.to_pickle("./BA_distributions1.pkl", compression=None)

#%%

import Functions as fn
import numpy as np

m = [int(i) for i in np.logspace(1, 5, 5, base=2)]
N = int(1e5)

from tqdm import tqdm
import pandas as pd

for i in range(2, 8):
    degs = []
    dists = []
    
    for mi in tqdm(m):
        degrees = fn.dist_BA(mi, N)
        degs.append(degrees)
        dist = np.bincount(degrees)
        index = np.arange(0, max(dist)+1, 1)
        dists.append({i:d for (i,d) in zip(index, dist)})
        
    Data = pd.DataFrame(
        {mi:(ri, di) for (mi, ri, di) in zip(
            m, degs, dists)},
        index=["Raw data", "Degree distribution"])

    Data.to_pickle(f"./BA_distributions{i}.pkl", compression=None)
    
#%%

import Functions as fn
import numpy as np

m = [int(i) for i in np.logspace(2, 6, 5, base=2)]

N = int(1e4) #smaller, average over more runs to get better statistics in tail.
max_bin = np.sqrt(N) * 5 #probably an overestimate
scale = 1.2 #should be good. go to 1.1 for more points, 1.3 for smoother curve

from tqdm import tqdm
import pandas as pd

#Now, we are only interested in the log-binned data.

import importlib
mod = importlib.import_module("logbin-2020")

full_dists = []
dist_errs = []

for i, mi in tqdm(m):
    for e in range(100):
        degrees = fn.dist_BA(mi, N)
        bin_centres, vals = mod.logbin(degrees, scale, max_bin, zeros=True)
        
        