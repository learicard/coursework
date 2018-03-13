#!/bin/bash


hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
    -input /user/cloudera/input \
    -output /user/cloudera/output_join \
    -mapper /home/cloudera/ex1/wordcount_mapper.py \
    -reducer /home/cloudera/ex1/wordcount_reducer.py
    
