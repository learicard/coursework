## MapReduce (single machine) -- inverted index ##

import MapReduce
import json
import sys

mr = MapReduce.MapReduce()

# Part 2
def mapper(record):
    # key: document identifier
    # value: document contents
    used = []

    key = record[0]
    value = record[1]
    words = value.split()
    for w in words:
      if w not in used:
        mr.emit_intermediate(w, key)
        used.append(w)


# Part 3
def reducer(key, list_of_values):
    # key: word
    # value: list of documents
    # docList = []
    # for doc in list_of_values:
    #  total += v
    mr.emit((key, list_of_values))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
