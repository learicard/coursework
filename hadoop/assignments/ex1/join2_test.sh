#!/bin/bash

cat join2*.txt | ./join2_mapper.py | sort  | ./join2_reducer.py
