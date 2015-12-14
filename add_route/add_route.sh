#!/bin/bash

function bin2dec() {
    echo $((2#$1)) | bc
}

function dec2bin() {
    binary_num=$(echo "obase=2; $1" | bc)
    printf "%08d" ${binary_num}
}

function get_net() {
    /sbin/ip r | awk '{if(($2 != "via") && ($0 ~ /eth1/)) print $1}'
}

function get_mask_bin() {
    local mask_bin=''
    for i in $(seq 1 $1)
    do 
        mask_bin+='1'
    done
    for i in $(seq $(($1 + 1)) 32)
    do 
        mask_bin+='0'
    done
    echo ${mask_bin}
}

function get_net_bin() {
    local net_name_arr[0]=$(get_net | awk -F'[.|/]+' '{print $1}')
    local net_name_arr[1]=$(get_net | awk -F'[.|/]+' '{print $2}')
    local net_name_arr[2]=$(get_net | awk -F'[.|/]+' '{print $3}')
    local net_name_arr[3]=$(get_net | awk -F'[.|/]+' '{print $4}')
    local mask_name=$(get_net | awk -F'[.|/]+' '{print $5}')
    local net_name_bin=''
    for net_name in ${net_name_arr[@]}
    do
        net_name_bin+=$(dec2bin ${net_name})
    done
    mask_name_bin=$(get_mask_bin ${mask_name})

    #echo ${net_name_bin}
    #echo ${mask_name_bin}

    local and_result=''
    for i in $(seq 0 31)
    do
        net_pos=${net_name_bin:${i}:1}
        mask_pos=${mask_name_bin:${i}:1}
        pos_and_result=$((${net_pos}&${mask_pos}))
        and_result+=${pos_and_result}
    done
    echo ${and_result}
}
    
function get_first_ip() {
    local result_bin=$(get_net_bin)
    #echo ${result_bin}

    local ip=''
    cut_result_bin=${result_bin:0:8}
    local ip_1=$(bin2dec ${cut_result_bin})
    cut_result_bin=${result_bin:8:8}
    local ip_2=$(bin2dec ${cut_result_bin})
    cut_result_bin=${result_bin:16:8}
    local ip_3=$(bin2dec ${cut_result_bin})
    cut_result_bin=${result_bin:24:8}
    local ip_4=$(bin2dec ${cut_result_bin})
    ip_4=$((${ip_4} + 1))
    local ip="${ip_1}.${ip_2}.${ip_3}.${ip_4}"
    echo ${ip}
}

function add_route() {
    local gate_way=$(get_first_ip)
    local net_list=$*
    for nets in ${net_list}
    do
        net=$(echo ${nets} | awk -F'|' '{print $1}')
        mask=$(echo ${nets} | awk -F'|' '{print $2}')
        if [ $(/sbin/route -n | grep ${net} -c) -lt 1 ]
        then
            echo /sbin/route add net ${net} netmask ${mask} gw ${gate_way}
            # do real route add.
        fi
    done
}

function main() {
    local net_list="100.64.0.0/10|255.192.0.0  1.2.3.4/10|255.255.0.0"
    add_route ${net_list}
}

main

