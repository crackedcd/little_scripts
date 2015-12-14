#!/bin/bash

ifconfig eth1 | awk -F'[ :]+' 'NR==2{print $4}'
df -Th

