#!/usr/bin/env bash

from=1
range=1000
is_more=true
count=1
timestamp=`date "+%Y-%m-%d-%H:%M:%S"`
dir=vote-data-${timestamp}
mkdir ${dir}

while [ ${is_more} == true ]
do
    echo ${from} ${count}
    res=`cleos get table eosio eosio voters -L " "${from} -l ${range}`
    echo ${res} |jq .rows >>  ${dir}/list${count}.txt
    count=$(( ${count} + 1 ))
    is_more=`echo ${res} | jq .more`
    from=`echo ${res} | jq .rows[$(( $range -1 ))].owner |cut -c 2-13`
done

echo "Done!"