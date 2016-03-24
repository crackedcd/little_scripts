#!/bin/bash

cd $(dirname $0)
time=$(date +\%Y\%m\%d\%H\%M\%S)
log_file="logs/${time}.log"
script_file="jojo.sh"

cat ${script_file} | grep -Ev "^( )*#|^$" 2>&1 | tee -a ${log_file} 2>&1
echo 
echo '############################################################'
echo '############################################################'
echo 
python remoteExec.py ${script_file} 2>&1 | tee -a ${log_file} 2>&1

echo "see log at [${log_file}]."

