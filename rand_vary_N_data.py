# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 23:50:01 2022

@author: whatf
"""

import Functions as fn
import numpy as np

m = 3

N = [int(i) for i in np.logspace(3, 5, 5)]

centres = []
means = []
stds = []

from tqdm import tqdm

import importlib
mod = importlib.import_module("logbin-2020")
scale = 1.1

for ni in N:
    max_bin = np.log(ni) + m
    min_bin = m
    dists = []
    for e in tqdm(range(200)):
        degrees = fn.dist_rand(m, ni)
        bin_centres, vals = mod.logbin(
            degrees, scale, min_bin, max_bin, zeros=True)
        
        dists.append(vals)
    centres.append(bin_centres)
    means.append(np.mean(dists, axis = 0))
    stds.append(np.std(dists, axis=0, ddof=1))
    
#%%
    
import pandas as pd

Data = pd.DataFrame(
    {ni:(c,av,err) for (ni, c, av, err) in zip(
        N, centres, means, stds)},
    index = ["Bin centres", "Log-binned data", "Associated errors"])

Data.to_pickle("rand_vary_N.pkl")