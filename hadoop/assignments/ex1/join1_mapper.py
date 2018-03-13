#!/usr/bin/env python

import sys

for line in sys.stdin:
    line = line.strip()
    key_value = line.split(',')
    key_in = key_value[0].split(' ')
    value_in = key_value[1]

    # date word case
    if len(key_in) >= 2:
        date = key_in[0]
        word = key_in[1]
        value_out = date + ' ' + value_in # concatenate date
        print('{0}\t{1}'.format(word, value_out))
    else:
        print('{0}\t{1}'.format(key_in[0], value_in))

