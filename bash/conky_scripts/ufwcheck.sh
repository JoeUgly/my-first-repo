#!/usr/bin/env bash

# Desc: Used by Conky to check if firewall is up


stat=$(/sbin/lsmod | awk '/ip_tables/{print $3;}' | head -n 1)

if [[ $stat -eq 1 ]]
then
echo '${color orange}'inactive
else
echo '${color6}'active
fi
