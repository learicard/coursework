#!/bin/bash

cat join1_File*.txt | ./join1_mapper.py | sort | ./join1_reducer.py
