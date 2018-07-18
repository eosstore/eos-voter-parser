#!/usr/bin/env bash

from=1
range=1000
is_more=true
count=1
timestamp=`date "+%Y-%m-%d-%H:%M:%S"`
dir=/root/voters/vote-data-${timestamp}
mkdir ${dir}

while [ ${is_more} == true ]
do
    echo ${from} ${count}
    res=`/usr/local/bin/cleos -u http://127.0.0.1:8889 get table eosio eosio voters -L " "${from} -l ${range}`
    echo ${res} |jq .rows >>  ${dir}/list${count}.txt
    sleep 0.5
    count=$(( ${count} + 1 ))
    is_more=`echo ${res} | jq .more`
    from=`echo ${res} | jq .rows[$(( $range -1 ))].owner |cut -c 2-13`
done

echo "Done!"
