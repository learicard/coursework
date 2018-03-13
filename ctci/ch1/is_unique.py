#!/usr/bin/env python
"""
Implement an algo to determine is a string has all unique characters. Completes
in O(n log n) time. log n = sort, n for iteration through string.
"""
import sys

def main(string):

    # assume ASCII
    if len(string) > 256:
        return False

    # sort: log n time
    string = ''.join(sorted(string))

    # iterate: n time
    for i in range(len(string)-1):
        if string[i] == string[i+1]:
            return False
        else:
            pass
    return True

if __name__ == '__main__':
    if main(sys.argv[1]):
        print('all unique')
