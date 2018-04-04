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
        import IPython; IPython.embed()
        return(-1)

    else:
        m = A.shape[1]

        # initialize the w vector to hold all weights i=0:m (n.b): A has columns
        # ranging from 1:m, no 0th column.
        w = np.zeros((m+1))

        # add 1, for the base case w(0) = 1
        w[0] = 1

        for i in range(0, m):
            vals = np.zeros((2))
            idx_1 = int(A[0, i])
            idx_2 = int(A[1, i])
            vals[0] = w[idx_1]
            vals[1] = w[idx_2]
            w[i+1] = np.sum(vals) # shift iterator here to align length of w & A

        return(int(w[-1]))


def find_m(w):
    """given a weight, find the smallest abacus"""
    # first, note that the maximum weight of an abacus is (2*n!)+1
    # so we can first easily find the minimum size of the abacus by
    m, max_weight = 0, 0

    while max_weight < w:
        m += 1
        max_weight = calc_weight(make_abacus(m, maxval=True))

    print('w={}, m={}'.format(w, m))
    return(m)


def increment(i, j):
    """moves rightword through matrix, down columns"""
    j += 1 # move down in column
    if j == 2:
        j = 0  # goto top of next column
        i += 1 #

    return(i, j)


def deccrement(i, j):
    """moves leftword through matrix, up column"""
    j -= 1 # move up in column
    if j == -1:
        j = 1  # gotob bottom of previous column
        i -= 1 #

    return(i, j)


def fill_abacus(A, w, i=0, j=0):
    """Fills abacus such that it is legal and has the expected weight"""
    curr_weight = calc_weight(A) # intialize current_weight
    #print('A={}\nc={}/{}, i={}, j={}\n'.format(A, curr_weight, w, i, j))

    m = A.shape[1]

    curr_val = i # the maximum value allowed in index=i (because python uses
                 # 0-based indexing

    # terminate this branch -- impossible case
    if i >= m:
        return(A)

    while curr_weight < w and curr_val >= 0:
        curr_weight = calc_weight(A) # needed to break out of while loop
        #print('adding {} at [{},{}]'.format(curr_val, i, j))

        A[j, i] = curr_val
        curr_weight = calc_weight(A) # updates value

        #print(chr(27) + "[2J")
        print(A)
        print('c={}/{}, i={}, j={}\n'.format(curr_weight, w, i, j))

        # FAILED: went over w, reset value at [j, i] and try again
        if curr_weight > w:
            A[j, i] = 0
            return(A)

        # SUCCESS: exactly correct, just return
        elif curr_weight == w:
            return(A)

        # WE NEED TO GO DEEPERER
        else:
            next_i, next_j = increment(i, j)
            A = fill_abacus(A, w, i=next_i, j=next_j)
            curr_val -= 1

    # FAILED: ran out of i to test
    #A[j, i] = 0
    return(np.hstack((A, np.zeros((2, 1)))))


# 3a
A = make_abacus(20)
w = calc_weight(A)

# 3b
w = 70
m = find_m(w)
A = np.zeros((2, m))
A = fill_abacus(A, w, i=1, j=0)

import IPython; IPython.embed()

