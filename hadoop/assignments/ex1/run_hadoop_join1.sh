#!/bin/bash

hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
    -input /user/cloudera/input \
    -output /user/cloudera/output_join1 \
    -mapper /home/cloudera/ex1/join1_mapper.py \
    -reducer /home/cloudera/ex1/join1_reducer.py

