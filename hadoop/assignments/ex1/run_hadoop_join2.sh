#!/bin/bash

hdfs dfs -rm -r /user/cloudera/output_join2

hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
    -input /user/cloudera/input \
    -output /user/cloudera/output_join2 \
    -mapper /home/cloudera/ex1/join2_mapper.py \
    -reducer /home/cloudera/ex1/join2_reducer.py \
    -numReduceTasks 1

hdfs dfs -cat /user/cloudera/output_join2/part-00000 > total_viewer_counts.txt

