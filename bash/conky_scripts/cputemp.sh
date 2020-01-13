#!/usr/bin/env bash

# Desc: Used by Conky to get CPU temperature


cputemp=$(sensors | awk '/Tdie/ {print $2;}' | cut -c 2-3)
if [[ $cputemp -ge 75 ]]
then 
echo '${color red}'$cputemp
fi

if [[ $cputemp -ge 65 ]] && [[ $cputemp -lt 75 ]]
then 
echo '${color yellow}'$cputemp
fi

if [[ $cputemp -lt 65 ]]
then 
echo '${color darkgrey}'$cputemp
fi
