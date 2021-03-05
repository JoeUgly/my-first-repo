#!/usr/bin/env bash

# Desc: Start Nordvpn for torrenting


# to do:
# check new ip
#dig @resolver4.opendns.com myip.opendns.com +short
#curl ipinfo.io/ip
#wget -qO- ipinfo.io/ip
# open browser? -


set -e


## based on location or load?
# Get recommended server using a filter for P2P servers (group code = 15)
resp=$(curl --silent --max-time 15 --retry 1 'https://nordvpn.com/wp-admin/admin-ajax.php?action=servers_recommendations&filters=\%22servers_groups%22:\[15\]')


# Use json to select server number
server_num=$(echo $resp | jq --tab .[0]."name" | cut -d \# -f2 | cut -d \" -f1)

# Select load
load=$(echo $resp | jq --tab .[0]."load")


echo -e \\nUsing server: $server_num
echo load: $load


# Connect to VPN
nordvpn connect us$server_num
nordvpn set killswitch enable


# Check IP
nord_ip=$(nordvpn status | grep 'new IP:' | cut -d \  -f4)
dns_ip=$(dig @resolver4.opendns.com myip.opendns.com +short)

echo -e \\nNord IP: $nord_ip
echo -e \ DNS IP: $dns_ip \\n

# Ignore part after last decimal
short_n=$(echo $nord_ip | cut -d . -f1-3)
short_d=$(echo $dns_ip | cut -d . -f1-3)

if [[ $short_n != $short_d ]]
then
echo -e \\n\\n IP address mismatch \\n\\n Do not proceed \\n\\n
fi


# Check IP against original
if [[ $nord_ip =~ 74.76. ]]
then
echo -e \\n\\n IP address may be unchanged \\n\\n Do not proceed \\n\\n
fi















