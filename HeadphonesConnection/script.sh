#!/bin/bash

plug="jack/headphone HEADPHONE plug"
unplug="jack/headphone HEADPHONE unplug"

while true
do
    read event
    if [ "$event" == "$plug" ]; then
        amixer set Front 0
    fi
    if [ "$event" == "$unplug" ]; then
        amixer set Front 100
    fi
done
