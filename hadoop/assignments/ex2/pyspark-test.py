#!/usr/bin/env python

def split_fileA(line):
    l = line.split(',')[0]
    v = line.split(',')[1]
    v = int(v)
    return(l, v)
def split_fileB(line):
    l = line.split(' ')[0]
    v = line.split(' ')[1]
    word = v.split(',')[0]
    count = v.split(',')[1]
    return(word, l + ' ' + count)
fileA = sc.textFile("input/join1_FileA.txt")
fileB = sc.textFile("input/join1_FileB.txt")
fileA_data = fileA.map(split_fileA)
fileB_data = fileB.map(split_fileB)

b_join_a = fileB_data.join(fileA_data)

