# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 23:39:58 2022

@author: whatf
"""

import Functions as fn
import numpy as np

N = int(1e4)

m = [int(i) for i in np.logspace(1, 6, 6, base=2)]

centres = []
means = []
stds = []

from tqdm import tqdm

import importlib
mod = importlib.import_module("logbin-2020")
scale = 1.05

for mi in m:
    max_bin = mi*np.log(N) + mi
    min_bin = mi
    dists = []
    for e in tqdm(range(200)):
        degrees = fn.dist_rand(mi, N)
        bin_centres, vals = mod.logbin(
            degrees, scale, min_bin, max_bin, zeros=True)
        
        dists.append(vals)
    centres.append(bin_centres)
    means.append(np.mean(dists, axis = 0))
    stds.append(np.std(dists, axis=0, ddof=1))
    


import pandas as pd

Data = pd.DataFrame(
    {mi:(c,av,err) for (mi, c, av, err) in zip(
        m, centres, means, stds)},
    index = ["Bin centres", "Log-binned data", "Associated errors"])

Data.to_pickle("rand_vary_m.pkl")