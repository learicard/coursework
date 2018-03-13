#!/usr/bin/env python
"""
Determines if a is a permutation of b. O(log n)
"""

import sys

def main(a, b):
    # simple case
    if len(a) != len(b):
        return(False)

    a = ''.join(sorted(a))
    b = ''.join(sorted(b))

    if a == b:
        return(True)
    else:
        return(False)

if __name__ == '__main__':
    if main(sys.argv[1], sys.argv[2]):
        print('same')

