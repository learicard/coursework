#!/bin/bash


hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
    -input /user/cloudera/input \
    -output /user/cloudera/output_new_2 \
    -mapper /home/cloudera/ex1/wordcount_mapper.py \
    -reducer /home/cloudera/ex1/wordcount_reducer.py \
    -numReduceTasks 2
    
