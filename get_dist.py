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

m = [int(i) for i in np.logspace(1, 5, 5, base=2)]

N = int(1e4) #smaller, average over more runs to get better statistics in tail.

scale = 1.3 #should be good. go to 1.1 for more points, 1.3 for smoother curve

from tqdm import tqdm
import pandas as pd

#Now, we are only interested in the log-binned data.

import importlib
mod = importlib.import_module("logbin-2020")

full_dists = []
dist_errs = []
entries = []
centres = []

average_over = 200

for i, mi in enumerate(m):
    max_bin = np.sqrt(N) * 10 * mi
    min_bin = mi
    dists = []
    for e in tqdm(range(average_over)):
        degrees = fn.dist_BA(mi, N)
        bin_centres, vals = mod.logbin(
            degrees, scale, min_bin, max_bin, zeros=True)
        
        dists.append(vals)
    centres.append(bin_centres)
    full_dists.append(np.mean(dists, axis = 0))
    dist_errs.append(np.std(dists, axis=0, ddof=1))
    
Data = pd.DataFrame(
    {mi:(c,av,err) for (mi, c, av, err) in zip(
        m, centres, full_dists, dist_errs)},
    index = ["Bin centres", "Log-binned data", "Associated errors"])

Data.to_pickle("BA_10_4_av_vary_m.pkl")

#%% raw data so we can do KS test

import Functions as fn
import numpy as np

m = [int(i) for i in np.logspace(1, 5, 5, base=2)]

N = int(1e4) #smaller, average over more runs to get better statistics in tail.
av_over = 100

degrees = []

from tqdm import tqdm

for mi in tqdm(m):
    degs = []
    for e in range(av_over):
        degs.append(fn.dist_BA(mi, N))
    degs = np.array(degs)
    degs = degs.flatten('C')
    degrees.append(degs)
    
import pandas as pd

Data = pd.DataFrame(
    {mi:[di] for (mi, di) in zip(m, degrees)},
    index=["Raw data"])

Data.to_pickle("Raw_data_for_KS.pkl", compression=None)