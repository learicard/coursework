## MapReduce (single machine) -- count friends ##

import MapReduce
import sys

mr = MapReduce.MapReduce()

# Part 2
def mapper(record):
    # key: document identifier
    # value: document contents
    mr.emit_intermediate(record[0], 1)

# Part 3
def reducer(key, list_of_values):
    mr.emit((key, sum(list_of_values)))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
