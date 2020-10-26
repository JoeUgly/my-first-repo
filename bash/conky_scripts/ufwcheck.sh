#!/usr/bin/env bash

# Desc: Used by Conky to check if firewall is up


stat=$(/sbin/lsmod | awk '/ip_tables/{print $3;}' | head -n 1)



#Ubuntu
#if [[ $stat -eq 1 ]]
#then
#echo '${color3}'inactive
#else
#echo '${color3}'active
#fi


# Manjaro
if [[ $stat -eq 4 ]]
then
echo '${color3}'inactive
else
echo '${color3}'active
fi
