#!/bin/bash

echo "Temperature:"
sensors | grep 'Core'

echo "Frequency:"
core_number=0
cpufreq-info | grep 'current CPU' 2>&1 | while read line
do
echo "Core $core_number: $line"
core_number=$((core_number + 1))
done

