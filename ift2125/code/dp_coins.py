#!/usr/bin/env python

import numpy as np

import sys

def get_ways(n, c):
    """ """
    n_change = n + 1  # add a base case of required change = 0
    n_coins = len(c) + 1

    T = np.zeros((n_change, n_coins))

    # initialize boundary values to inf, so they never win the min (below)
    for i in range(1, n_change, 1):
        T[i, 0] = np.inf

    # i is the amount of money we need to make change for
    for i in range(1, n_change, 1):
        for j in range(1, n_coins, 1):

            if i == 1:
                # smallest denomination case, just counts up in units of c[0]
                T[i, j] = 1 + T[0, j-c[0]]

            elif i < c[j-1]:
                #print('increment')
                # this value is smaller than the next largest denomination
                # so we add one to the previous value
                T[i, j] = 1 + T[i-1, j]

            else:
                # take the minimum of adding one of the previous denominations
                # or using one new denomination
                T[i, j] = min(T[i, j-1], 1+T[i-c[j-1], j])

            #print('change={}, denom={}\n{}\n'.format(i, c[j-1], T))


    # find coins used
    i = n_change-1
    j = n_coins-1
    coins_used = []

    while i != 0:

        if T[i, j] == T[i, j-1]:
            j -= 1
        elif T[i, j] != T[i, j-1]:
            coins_used.append(c[j-1])
            i -= c[j-1]

    return(T, coins_used, T[-1, -1])

n = 8
c = [1, 4, 6]
T, coins, answer = get_ways(n, c)

print('problem: change for {}, using coins={}'.format(n, c))
print('solution:\n{}\n\nusing {} coins: {}'.format(T, answer, coins))

