## MapReduce (single machine) -- find asymmetric friendships ##

import MapReduce
import sys

mr = MapReduce.MapReduce()

def mapper(record):
    # seqID: sequence name
    # value: a string containing nucleotides
    seqID = record[0]
    nucTs = record[1]

    mr.emit_intermediate(nucTs[:-10], seqID)

def reducer(key, list_of_values):
    mr.emit(key)

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
