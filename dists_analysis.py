# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 16:08:02 2022

@author: whatf
"""

import pandas as pd
import numpy as np

Data = pd.read_pickle("./BA_distributions1.pkl")

m = list(Data.keys())
raw = np.array([Data[i]["Raw data"] for i in m])
dists = [Data[i]["Degree distribution"] for i in m]

import importlib

mod = importlib.import_module("logbin-2020")

log_bins = []

for r in raw:
    log_bins.append(mod.logbin(r, 1.1))

import matplotlib.pyplot as plt

plt.plot(log_bins[1][0], log_bins[1][1], '.')
plt.xscale("log")
plt.yscale("log")