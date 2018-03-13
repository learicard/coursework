## MapReduce (single machine) -- matrix multiply ##

import MapReduce
import sys

mr = MapReduce.MapReduce()

def mapper(record):
    mat = record[0]
    row = record[1]
    col = record[2]
    val = record[3]
    
    if mat == 'a':
        for iterator in range(5):
            mr.emit_intermediate((row, iterator), record)

    elif mat == 'b':
        for iterator in range(5):
            mr.emit_intermediate((iterator, col), record)

def reducer(key, list_of_values):
    aVals={}
    bVals={}

    for value in list_of_values:
        
        if value[0] == 'a':
            aVals[value[2]] = value[3]
        
        elif value[0] == "b":
            bVals[value[1]] = value[3]

    dotProduct = 0
    for iterator in range(5):
        if iterator in aVals and iterator in bVals:
            dotProduct += aVals[iterator] * bVals[iterator]

    n=[]
    n.append(key[0])
    n.append(key[1])
    n.append(dotProduct)
    mr.emit(tuple(n))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)