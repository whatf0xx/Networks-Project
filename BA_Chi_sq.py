# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 01:20:34 2022

@author: whatf
"""

import pandas as pd

Data = pd.read_pickle("Raw_data_for_KS.pkl")

def p_inf(m,k):
    return 2*m*(m+1)/k/(k+1)/(k+2)

m = 16

data = Data[m]["Raw data"]
normalisation = 1e6

import numpy as np

binned_data = np.bincount(data)[m:]/normalisation
points = np.arange(m, len(binned_data)+m, 1)
theory = p_inf(m,points)

import matplotlib

matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
matplotlib.rcParams['font.size'] = 12

import matplotlib.pyplot as plt

plt.plot(points, binned_data, 'b.')
plt.plot(points, theory)
plt.xscale("log")
plt.yscale("log")