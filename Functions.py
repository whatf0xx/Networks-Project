# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 19:22:27 2022

@author: whatf
"""

import networkx as nx
import numpy as np
import random

"""
Returns a complete graph with m+1 nodes.
"""

def seed(m: int):
    return nx.complete_graph(m+1)

"""
Set-up the list from which to randomly pick nodes for the BA algorithm steps,
taking as inputs:
    N - the eventual size of the BA graph.
    m - the standard constant for adding new edges at each time step.
This assumes that the seed graph for the BA model is given as above.
N.B. when calling from this list the slicing is very important - the array is
initialised to full length in order to stop memory re-allocation as the
algorithm runs, which means during the run the last half of the array is full
of 0s, which will corrupt how the code runs if they are left in the sliced
bin, while it is being used to calculate the preferential attachment.
"""

def make_list(N: int, m: int):
    length = m*(m+1) + 2*m*(N-m-1)
    node_list = np.zeros(length, dtype=np.uint32)
    for i in range(m+1):
        for j in range(m):
            node_list[i*(m)+j] = i
    
    return node_list

"""
The BA algorithm, iterated for one step. Takes a graph G, and the associated
degree bin, and performs a step, adding a node and m edges to the graph,
assigned by preferential attachment, and adding nodes which get edges added to
them to the degree bin.
"""

def BA_step(G, degree_bin, m, t):
    new_node = m+t+1 #new node is the (m+t+1)th, starting from t=0
    used_posns = m*(m+1) + 2*m*t
    G.add_node(new_node) 
    
    # bin_positions = [random.randint(0, used_posns) for i in range(m)]
    # #this step seems to do what it should for t=0
    
    # lucky_nodes = [int(degree_bin[b]) for b in bin_positions]
    # print(f"bin positions: {bin_positions}")
    # print(f"corresponding nodes: {lucky_nodes}")
    lucky_nodes = []
    trimmed_bin = degree_bin[:used_posns].copy()
    
    for i in range(m):
        node = random.choice(trimmed_bin)
        lucky_nodes.append(node)
        trimmed_bin = trimmed_bin[trimmed_bin != node]
    
    for i, l in enumerate(lucky_nodes):
        G.add_edge(new_node, l) #add edges to the lucky nodes
        degree_bin[used_posns + i] = l
        
    for i in range(m):
        degree_bin[used_posns + m + i] = new_node
        
"""
A neatly wrapped-up function to generate a BA graph with characteristic m and 
size N. If dist == True, also returns the degree for each node.
"""

def gen_BA(m, N, dist=False):
    
    G = seed(m)
    degree_bin = make_list(N, m)

    for t in range(N-m-1):
        BA_step(G, degree_bin, m, t)
        
    if dist:
        d = np.bincount(degree_bin)
        return G, d
        
    return G

"""
A neatly wrapped-up function to generate a BA graph with characteristic m and 
size N. Only returns the degree distribution list
"""

def dist_BA(m, N, dist=False):
    
    G = seed(m)
    degree_bin = make_list(N, m)

    for t in range(N-m-1):
        BA_step(G, degree_bin, m, t)
        
    d = np.bincount(degree_bin)
    return d

"""
Same as above, but with some breaks in to output useful data to test the
algorithm is running correctly.
"""

def test_BA(m, N):
    
    G = seed(m)
    degree_bin = make_list(N, m)
    
    nodes = []                      #the number of nodes the graph has
    edges = []                      #the number of edges the graph has
    norm = []
    k_predict = []                  #calculated degree of picked nodes
    k_meas = []                     #actual average degree of picked nodes
    
    nodes.append(len(G.nodes))
    edges.append(len(G.edges))

    for t in range(N-m-1):
        used_posns = m*(m+1) + 2*m*t
        trimmed_bin = degree_bin[:used_posns].copy()
        d = np.bincount(trimmed_bin)
        norm.append(np.sum([k for k in d])/(2*len(G.edges)))
        k_squared = np.sum([k**2 for k in d])
        k_predict.append(k_squared/(2*len(G.edges)))
        lucky_nodes = BA_test_step(G, degree_bin, m, t)
        t = list(trimmed_bin)
        lucky_degrees = [t.count(l) for l in lucky_nodes]
        k_meas.append(np.mean(lucky_degrees))
        nodes.append(len(G.nodes))
        edges.append(len(G.edges))
        
    return nodes, edges, norm, k_predict, k_meas

"""
Another slightly modified function to lend itself to being used for testing.
"""

def BA_test_step(G, degree_bin, m, t):
    new_node = m+t+1 #new node is the (m+t+1)th, starting from t=0
    used_posns = m*(m+1) + 2*m*t
    G.add_node(new_node) 
    
    # bin_positions = [random.randint(0, used_posns) for i in range(m)]
    # #this step seems to do what it should for t=0
    
    # lucky_nodes = [int(degree_bin[b]) for b in bin_positions]
    # print(f"bin positions: {bin_positions}")
    # print(f"corresponding nodes: {lucky_nodes}")
    lucky_nodes = []
    trimmed_bin = degree_bin[:used_posns].copy()
    
    for i in range(m):
        node = random.choice(trimmed_bin)
        lucky_nodes.append(node)
        trimmed_bin = trimmed_bin[trimmed_bin != node]
    
    for i, l in enumerate(lucky_nodes):
        G.add_edge(new_node, l) #add edges to the lucky nodes
        degree_bin[used_posns + i] = l
        
    for i in range(m):
        degree_bin[used_posns + m + i] = new_node
        
    return lucky_nodes

"""
A test for the BA model based on the average degree at each time step.
"""

def test2_BA(m, N):
    
    mu_k = []
    G = seed(m)
    degree_bin = make_list(N, m)

    for t in range(N-m-1):
        used_posns = m*(m+1) + 2*m*t
        trimmed_bin = degree_bin[:used_posns].copy()
        degrees = np.bincount(trimmed_bin)
        mu_k.append(np.mean(degrees))
        BA_step(G, degree_bin, m, t)
    
    return mu_k

"""
For finding the k1 behaviour as N varies
"""

def BA_k1(m, N):
    
    G = seed(m)
    degree_bin = make_list(N, m)
    
    k1 = np.zeros(N-m-1)

    for t in range(N-m-1):
        BA_step(G, degree_bin, m, t)
        used_posns = m*(m+1) + 2*m*t
        k1[t] = np.max(np.bincount(degree_bin[:used_posns]))
        
    return k1

"""
A step wherein you pick m random nodes from an initial graph to connect a new
node to. No fancy list needed, just grab the current list of nodes, and pick
m distinct elements from it. Random.sample() handles this nicely.
    m - the number of connections to make.
    G - the graph to start off of.
"""

def rand_step(m, G):
    node_list = list(G.nodes())
    t = len(node_list)
    G.add_node(t+1)
    
    lucky_nodes = random.sample(node_list, m)
    for l in lucky_nodes:
        G.add_edge(t+1, l)
        
"""
A neatly wrapped-up function to generate a random graph with characteristic m
and size N. If dist == True, also returns the degree for each node.
"""

def gen_rand(m, N, dist=False):
    
    G = seed(m)

    for t in range(N-m-1):
        rand_step(m, G)
        
    if dist:
        degrees = [val for (node, val) in G.degree()]
        return G, degrees
        
    return G

"""
A neatly wrapped-up function to generate a random graph with characteristic m 
and size N. Only returns the degree distribution list
"""

def dist_rand(m, N, dist=False):
    
    G = seed(m)

    for t in range(N-m-1):
        rand_step(m, G)
        
    degrees = [val for (node, val) in G.degree()]
    return degrees

"""
For finding the k1 behaviour as N varies (random attachment)
"""

def rand_k1(m, N):
    
    G = seed(m)
    
    k1 = np.zeros(N-m-1)

    for t in range(N-m-1):
        rand_step(m, G)
        degrees = [val for (node, val) in G.degree()]
        k1[t] = np.max(degrees)
        
    return k1

"""
The dad mixed existing attachment. Do preferential first and then random, use
random.sample() to pick nodes to be attached to and then for each generate a
unique neighbour.
"""

def exist_step(G, degree_bin, r, t):
    m = 2*r
    node_list = list(G.nodes())
    new_node = m+t+1 #new node is the (m+t+1)th, starting from t=0
    used_posns = m*(m+1) + 2*m*t
    G.add_node(new_node)
    
    lucky_nodes = []
    trimmed_bin = degree_bin[:used_posns].copy()
    
    for i in range(r):
        node = random.choice(trimmed_bin)
        lucky_nodes.append(node)
        trimmed_bin = trimmed_bin[trimmed_bin != node]
    
    for i, l in enumerate(lucky_nodes):
        G.add_edge(new_node, l) #add edges to the lucky nodes
        degree_bin[used_posns + i] = l
        
    for i in range(r):
        degree_bin[used_posns + r + i] = new_node
        
    #now for the random attachment bit
    lucky_nodes2 = random.sample(node_list, r)
    for i, l in enumerate(lucky_nodes2):
        nbs = list(set(node_list) & set(list(G.neighbors(l))))
        nb = random.choice(nbs)
        G.add_edge(l, nb)
        degree_bin[used_posns + m + 2*i] = l
        degree_bin[used_posns + m + 2*i+1] = nb
        
"""
A neatly wrapped-up function to generate a exist graph with characteristic m 
and size N. If dist == True, also returns the degree for each node.
"""

def gen_exist(r, N, dist=False):
    m=2*r
    G = seed(m)
    degree_bin = make_list(N, m)

    for t in range(N-m-1):
        exist_step(G, degree_bin, r, t)
        
    d = np.bincount(degree_bin)
    return d