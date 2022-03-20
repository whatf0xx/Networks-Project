################################################################################
# Max Falkenberg McGillivray
# mff113@ic.ac.uk
# 2019 Complexity & Networks course
#
# logbin230119.py v2.0
# 23/01/2019
# Email me if you find any bugs!
#
# For details on data binning see Appendix E from
# K. Christensen and N.R. Moloney, Complexity and Criticality,
# Imperial College Press (2005).
################################################################################

import numpy as np

def logbin(data, scale = 1., min_bin=1, max_bin=-1, zeros = False):
    """
    logbin(data, scale = 1., zeros = False)

    Log-bin frequency of unique integer values in data. Returns probabilities
    for each bin.

    Array, data, is a 1-d array containing full set of event sizes for a
    given process in no particular order. For instance, in the Oslo Model
    the array may contain the avalanche size recorded at each time step. For
    a complex network, the array may contain the degree of each node in the
    network. The logbin function finds the frequency of each unique value in
    the data array. The function then bins these frequencies in logarithmically
    increasing bin sizes controlled by the scale parameter.

    Minimum binsize is always 1. Bin edges are lowered to nearest integer. Bins
    are always unique, i.e. two different float bin edges corresponding to the
    same integer interval will not be included twice. Note, rounding to integer
    values results in noise at small event sizes.

    Parameters
    ----------

    data: array_like, 1 dimensional, non-negative integers
          Input array. (e.g. Raw avalanche size data in Oslo model.)

    scale: float, greater or equal to 1.
          Scale parameter controlling the growth of bin sizes.
          If scale = 1., function will return frequency of each unique integer
          value in data with no binning.
          
    min_bin: float. The lowest bin edge to use.
          
    max_bin: float. set the final bin edge manually, instead of taking it from
            the data. Useful for averaging lots of logbins, but don't forget
            to normalise afterwards! Leave as -1 in order to use smax instead.

    zeros: boolean
          Set zeros = True if you want binning function to consider events of
          size 0.
          Note that output cannot be plotted on log-log scale if data contains
          zeros. If zeros = False, events of size 0 will be removed from data.

    Returns
    -------

    x: array_like, 1 dimensional
          Array of coordinates for bin centres calculated using geometric mean
          of bin edges. Bins with a count of 0 will not be returned.
    y: array_like, 1 dimensional
          Array of normalised frequency counts within each bin. Bins with a
          count of 0 will not be returned.
    """
    if scale < 1:
        raise ValueError('Function requires scale >= 1.')
    count = np.bincount(data)
    tot = np.sum(count)
    smax = np.max(data)
    if scale > 1:
        if max_bin == -1:
            jmax = np.ceil(np.log(smax)/np.log(scale))
        else:
            jmax = np.ceil(np.log(max_bin)/np.log(scale))
        if zeros:
            binedges = min_bin * scale ** np.arange(jmax + 1)
            #binedges[0] = 0
        else:
            binedges = min_bin * scale ** np.arange(1,jmax + 1)
            # count = count[1:]
        binedges = np.unique(binedges.astype('uint64'))
        x = (binedges[:-1] * (binedges[1:]-1)) ** 0.5
        y = np.zeros_like(x)
        count = count.astype('float')
        for i in range(len(y)):
            y[i] = np.sum(count[binedges[i]:binedges[i+1]]/(binedges[i+1] - binedges[i]))
            # print(binedges[i],binedges[i+1])
        # print(smax,jmax,binedges,x)
        # print(x,y)
    else:
        x = np.nonzero(count)[0]
        y = count[count != 0].astype('float')
    if zeros != True and x[0] == 0:
        x = x[1:]
        y = y[1:]
    if zeros != True:
        x = x[y!=0]
        y = y[y!=0]
    y /= tot
    return x,y
