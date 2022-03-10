# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 19:22:27 2022

@author: whatf
"""

import networkx as nx

"""
Return a complete graph with degree distribution m:
"""

def seed(m):
    return nx.complete_graph(m)

