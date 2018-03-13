#!/usr/bin/env python
import sys

last_key = None
viewers = 0
channel = 'ABC'
is_channel = False

for line in sys.stdin:
    line = line.strip()
    key = line.split('\t')[0]
    value = line.split('\t')[1]

    # ensure input digits are integer
    if value.isdigit():
        value = int(value)

    if last_key != key:
        if is_channel:
            # emit data and reset variables
            print('{0} {1}'.format(last_key, viewers))
            is_channel = False
            viewers = 0
        elif value != channel:
            # first count of viewers for this show
            viewers = value
    elif last_key == key:
        if type(value) == int:
            viewers += value

    # flag that tells us whether to emit data (b/c this is the correct channel)
    if value == channel:
        is_channel = True

    last_key = key

# emit the final show
if is_channel:
    print('{0} {1}'.format(last_key, viewers))

