## MapReduce (single machine) -- find asymmetric friendships ##

import MapReduce
import sys

mr = MapReduce.MapReduce()

def mapper(record):
    # emit every combo of friends
    mr.emit_intermediate(record[0], record[1])
    mr.emit_intermediate(record[1], record[0])

def reducer(key, list_of_values):
    friends = {}
    for value in list_of_values:
        if value in friends:
          del friends[value]
        else:
          friends[value] = 'symmetric'
    for friend in friends:
        mr.emit((key, friend))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)