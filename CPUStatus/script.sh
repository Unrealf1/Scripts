#!/bin/bash

echo "Temperature:"
sensors | grep 'Core'

echo "Frequency:"
core_number=0
cat /proc/cpuinfo | grep 'cpu MHz' 2>&1 | while read line
do
echo "Core $core_number: $line"
core_number=$((core_number + 1))
done

