#!/bin/bash

beep_time="3"
sleep_time="0"
prev_volume="30"
max_volume="55"
min_volume="0"

if [ ! -z "$1" ]
  then
    sleep_time="$1"
fi

echo "Set timer for $sleep_time seconds"

sleep $sleep_time
cur_volume="$min_volume"

echo "Time has come!"

sleep $sleep_time
cur_volume="$min_volume"

while [ 1 ]; do
    amixer set Master "$cur_volume%" &> /dev/null
    timeout -s $beep_time $beep_time speaker-test -t sine -f 1000 -l 1 &> /dev/null
    amixer set Master "$prev_volume%" &> /dev/null
    cur_volume="$(($cur_volume + 7))"
    if [ $cur_volume -ge $max_volume ]
     then
        cur_volume="$min_volume"
    fi
    sleep 10
done

