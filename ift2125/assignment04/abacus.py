#!/usr/bin/env python

import numpy as np

def make_abacus(m, maxval=False):
    """ makes a 2xm-sized abacus """
    abacus = np.zeros((2, m)) # initalize array

    # 1 <= i <= m, A(1, i) < i and A(2, i) < i, therefore 0 when i = 1.
    for i in range(1, m):
        # add 1 to i because we convert 0 index to 1 index for problem

        if maxval:
            abacus[:, i] = i
        else:
            abacus[:, i] = np.random.randint(0, i+1, (1, 2))

    return(abacus)


def is_abacus(A):
    """ """
    # abacus must be 2xm
    dims = np.shape(A)
    if len(dims) > 2:
        return(False)

    n, m = dims
    if n != 2:
        return(False)

    # ensures all entries [:, i] in A are < i
    test =  make_abacus(m, maxval=True)
    if np.sum(A[:, 1:] > test[:, 1:]):
        return(False)

    # finally ensure [:, 0] is 0
    if np.sum(A[:,0]):
        return(False)

    return(True)


def calc_weight(A):
    if not is_abacus(A):
        return(-1)

    else:
        # first, calculate all A[1,:] + A[2,:]
        weights = np.sum(A, axis=0)

        # remove the first entry (techinically unnessicary since the first entry
        # is always = 0), and add 1, for the base case w(0) = 1
        w = np.sum(weights[1:]) + 1

        return(int(w))


def find_m(w):
    """given a weight, find the smallest abacus"""
    # first, note that the maximum weight of an abacus is (2*n!)+1
    # so we can first easily find the minimum size of the abacus by
    m = 1
    test_val =  1 # base case

    while test_val < w:
        test_val += (2*m)
        m += 1

    print('w={}, m={}'.format(w, m))
    return(m)


def increment(i, j):
    """moves leftword through matrix, column-wise"""

    # move down in column
    j += 1
    if j == 2:
        j = 0

        # move back one column
        if i > 0:
            i -= 1

    return(i, j)


def fill_abacus(A, w, i=1, j=0):
    """Fills abacus such that it is legal and has the expected weight"""

    curr_weight = calc_weight(A)
    if curr_weight < w:
        if w - curr_weight >= i:
            print('adding {}'.format(i))
            A[j, i] = i

        else:
            print('adding {}'.format(np.abs(curr_weight - w)))
            A[j, i] = w - curr_weight

        i, j = increment(i, j)

        print('A={}\nc={}/{}, i={}, j={}'.format(A, curr_weight, w, i, j))
        A = fill_abacus(A, w, i=i, j=j)

    elif curr_weight == w:
        print('SUCCESS\nA={}\nc={}/{}, i={}, j={}'.format(A, curr_weight, w, i, j))
        return(A)
    else:
        print('FAILED\nA={}\nc={}/{}, i={}, j={}'.format(A, curr_weight, w, i, j))
        A[i, j] = 0
        return(A)

    # filled_A will be returned to process that spawned call if we don't go over
    # the limit
    return(A)


# 3a
A = make_abacus(20)
w = calc_weight(A)

# 3b
w = 70
m = find_m(w)
A = np.zeros((2, m))
A = fill_abacus(A, w, i=m-1, j=0)

import IPython; IPython.embed()

