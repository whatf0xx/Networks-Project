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