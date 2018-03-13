## MapReduce (single machine) -- relational join ##

import MapReduce
import json
import sys

mr = MapReduce.MapReduce()

# Part 2
def mapper(record):
    # key: document identifier
    # value: document contents
    value = record[1]
    mr.emit_intermediate(value, record)

# Part 3
def reducer(key, list_of_values):
    for firstVal in list_of_values:
        for secondVal in list_of_values:
            if firstVal[0] == 'order' and secondVal[0] == 'line_item':
                mr.emit(firstVal + secondVal)

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
