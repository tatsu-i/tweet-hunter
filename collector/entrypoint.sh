#!/bin/bash
/wait-for-it.sh elasticsearch:9200
sleep 10

python -u /scripts/run.py
