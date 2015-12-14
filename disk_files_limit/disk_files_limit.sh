#!/bin/bash

work_path=$(dirname $0)
log_path="${work_path}/log"
time_now=$(date +\%Y\%m\%d\%H\%M)
log_file="${log_path}/${time_now}.log"
unique_ip=$(/sbin/ifconfig eth1 | awk -F'[ |:]+' 'NR==2{gsub(/\./, "", $0); print $4}')
unique_id=$((584360 + ${unique_ip}))

scan_dirs="/usr/local/middle/  /data/cft_msg_forwarder/data/"
limit_count=100

function count_files() {
    # params:
    #    dir_name - lookup directory name.
    local dir_name=$1
    /usr/bin/find ${dir_name} -maxdepth 1 -type f | wc -l
}

function count_exceed_limit() {
    # judge if the count out of limit or not.
    # params:
    #    count - number of file counts in this directory. 
    local counts=$1
    if [[ ${counts} -gt ${limit_count} ]]
    then
        echo 1
    else
        echo 0
    fi
}

function list_all_dirs() {
    # params:
    #   dir_name - name of parent directory.
    local dir_name=$1
    /usr/bin/find ${dir_name} -type d
}

function is_leaf_dir() {
    # params:
    #   dir_name - name of directory.
    # returns:
    #   1 - is leaf.
    #   0 - not a leaf.
    local dir_name=$1
    sub_dirs=$(/usr/bin/find ${dir_name} -maxdepth 1 -type d)
    if [[ ${sub_dirs} == ${dir_name} ]]
    then
        echo 1
    else
        echo 0
    fi
}

function alarm() {
    # log and send alarm.
    # params:
    #   dir_name.
    #   counts.
    local dir_name=$1
    local counts=$2
    echo -e "${dir_name} : ${counts}" >> ${log_file}
    ./LogClient 10.128.128.20 file_limit warning ${unique_id} "${dir_name}下文件数量是${counts}, 超过${limit_count}的限制."
}

function lookup_dirs() {
    # traversal dirs and find the leaf dirs and their inner files.
    # params:
    #   dir_name - name of root directory.
    local dir_names=$1
    for dir in ${dir_names}
    do
        sub_dirs=$(list_all_dirs ${dir})
        for sub in ${sub_dirs}
        do
            if [[ $(is_leaf_dir ${sub}) -eq 1 ]]
            then
                local counts=$(count_files ${sub})
                if [[ $(count_exceed_limit ${counts}) -eq 1 ]]
                then
                    alarm ${sub} ${counts}
                fi
            fi
        done
    done
}

function main() {
    cd ${work_path}
    if [ ! -d ${log_path} ]
    then
        mkdir -p ${log_path}
    fi
    lookup_dirs ${scan_dirs} 
}

main

