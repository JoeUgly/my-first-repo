#!/usr/bin/env bash

# Desc: Only run Deluge if VPN is active



status=$(nordvpn status | grep Status: | cut -d : -f2)

if [[ $status = ' Connected' ]]
then
deluge-gtk %U &
else
echo VPN: $status
fi















