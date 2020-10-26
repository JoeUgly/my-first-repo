#!/usr/bin/env bash

# Desc: Used by Conky to get hard drive temperature


hddtemp=$(hddtemp -n /dev/sda)
if [[ $hddtemp -ge 50 ]]
then 
echo '${color red}'$hddtemp
fi
if [[ $hddtemp -gt 40 ]] && [[ $hddtemp -lt 50 ]]
then 
echo '${color yellow}'$hddtemp
fi
if [[ $hddtemp -le 40 ]]
then 
echo '${color darkgrey}'$hddtemp
fi

