#!/bin/bash

cd $(dirname $0)
time=$(date +\%Y\%m\%d\%H\%M\%S)
log_file="logs/${time}.log"
script_file="jojo.sh"

cat giogio.sh | grep -Ev "^( )*#|^$" 2>&1 | tee ${log_file}
python remoteExec.py ${script_file} 2>&1 | tee ${log_file}
