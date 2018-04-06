#!/usr/bin/env python

import numpy as np

def charge(j):
    """charge is a exponential function of j"""
    return(j**2)

def optimize(k):

    schedule = np.zeros((k+1, k+1)) # k+1 set to zero for base case
    times = []

    # contains the number of chefs available at each i
    n = np.random.randint(0, 10, k)

    for i in range(k-1 , -1, -1):
        for j in range(i+1):
            use_this_cell = min(charge(j), n[i]) + schedule[0, i+1]
            print('i={}, j={}, charge(j)={}, n[i]={}'.format(i, j, charge(j), n[i]))
            use_next_cell = schedule[j+1, i+1]
            schedule[j, i] = max(use_this_cell, use_next_cell)
            print(schedule[j, i])

            if schedule[j, i] == use_this_cell:
                times.append(i)

    import IPython; IPython.embed()
    return(schedule[0,0], times)


value, times = optimize(10)

import IPython; IPython.embed()

