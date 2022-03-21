# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 15:24:00 2022

@author: whatf
"""

import Functions as fn
import numpy as np

N = [int(n) for n in np.logspace(3, 5, 5)]
m = 3 #nice and low

av = 100

scale = 1.1

centres = []
mean = []
err = []

import importlib
mod = importlib.import_module("logbin-2020")

from tqdm import tqdm

for n in N:
    degrees = []
    
    for i in tqdm(range(av)):
        dist = fn.dist_BA(m, n)
        bin_centres, vals = mod.logbin(
            dist, scale, m, 10*m*np.sqrt(n), zeros=True)
        
        degrees.append(vals)
        
    centres.append(bin_centres)
    mean.append(np.mean(degrees, axis=0))
    err.append(np.std(degrees, axis=0, ddof=1))

import pandas as pd

Data = pd.DataFrame(
    {n:(c,d,e) for (n,c,d,e) in zip(N, centres, mean, err)},
    index=["Bin centres", "Mean degree", "Error"])

Data.to_pickle("BA_N_vary_d1.1.pkl", compression=None)