#!/usr/bin/env python

import sys

for line in sys.stdin:
    line = line.strip()
    key = line.split(',')[0]
    value = line.split(',')[1]
    if value == 'ABC' or value.isdigit():
        print('{0}\t{1}'.format(key, value))

