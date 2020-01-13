#!/usr/bin/env bash

# Description: Automatically download Jeopardy episode torrents.


# Features:
# Start VPN
# Find most recent episode online using proxy
# Allow only approved uploaders
# Edit config file to allow port forwarding
# Start torrent client and add episode




# To do:
# bypass DDoS protection
# connect VPN if it is already running
# must connect to VPN region that suppports port forwarding
# Error detection and resolution
# Run at specified time
# Allow for user-defined search term -
# remove proxy check?




# Get date of most recent episode in tor dir
file_date=$(ls /mnt/a0b51b49-88e3-43bc-8c48-d5d49f4ae5b3/tors | grep -iP Jeopardy\\.\\d{4} | sort -r | head -n 1 | cut -d \. -f2-4)
echo -e \\n Most recent episode on disk: $file_date

# Check date format
date_check=$(echo $file_date | grep -E ^[0-9]{4}\.[0-9]{2}\.[0-9]{2}$)
if [[ -z $date_check ]]
then
echo -e \\n File date check failed. Exiting ...
#exit
fi



# Check VPN
echo -e \\n Checking VPN connection ...
vpn_state=$(piactl get connectionstate)

# Check VPN status
if [[ $vpn_state != 'Connected' ]]
then

    # Check if VPN client is running but disconnected or if client is not running.
    if [[ -n $(pgrep pia-client) ]]
    then
    echo Connecting VPN ...
    piactl connect

    # Start VPN client, redirect stdout and stderr, and detach
    else
    /opt/piavpn/bin/pia-client > /dev/null 2>&1 &
    echo Turning on VPN ...
    fi


    # Wait for VPN to start
    for i in {1..10}
    do
    echo Please wait ...
    sleep 2
    vpn_state=$(piactl get connectionstate)

        # VPN has started
        if [[ $vpn_state == 'Connected' ]]
        then
        echo VPN has been started
        break
        fi

    done

    # Exit if loop is exhausted
    if [[ $vpn_state != 'Connected' ]]
    then    
    echo VPN failed to start. Exiting ...
    exit
    fi
    

# VPN was already on
else
echo VPN is on
fi


: '
# Proxy check
echo -e \\n Checking proxy ...

sec_check=$(curl --proxy-user x4929043:HbXeY7u7cZ --socks5-hostname proxy-nl.privateinternetaccess.com:1080 --max-time 15 --retry 1 -sL "ifconfig.me")

if [[ $sec_check == 46\.166\.* ]] || [[ $sec_check == 109\.201\.* ]]
then
echo Proxy check success: $sec_check
else
echo -e Proxy check failure: $sec_check \\n error code = "$?" \\n Exiting ...
exit
fi
'


# Get HTML with SOCKS5 proxy
echo -e \\n Requesting HTML ...

#html=$(curl --user-agent 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0' --proxy-user x4929043:HbXeY7u7cZ --socks5-hostname proxy-nl.privateinternetaccess.com:1080 --max-time 15 --retry 1 -sL 'https://pirateproxy.llc/search/jeopardy/0/3/0')

html=$(curl --user-agent 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0' --max-time 15 --retry 1 -sL 'https://pirateproxy.llc/search/jeopardy/0/3/0')
err=$?


# Catch request errors
if [[ $err -ne 0 ]]
then
echo -e \\n HTML request error detected: $err \\n Exiting ...
exit

else
echo -e HTML received \\nExit code: $err
fi



# I don't know why this must be done. Don't delete.
html=$(echo $html)


# Check HTML
if [[ -z $(echo $html | grep Jeopardy) ]]
then
echo -e \\n Failed HTML check. Exiting ...

if [[ -n $(echo $html | grep 'DDoS protection by Cloudflare') ]]
then
echo -e \\n DDoS splash screen detected \\n
exit
fi

fi


# This is needed to seperate each block of torrent info. All HTML must be one line.
oldifs=$IFS
IFS=$'\n'

# Form array of torrent info based on <td> elements
tor_arr=($(echo "$html" | grep -Po \<td\>.*?\ \</td\>))


# Loop through each torrent in the array starting with the most recently uploaded
for each_tor in "${tor_arr[@]}"
do


# Get name of torrent. Not really necessary
name=$(echo "$each_tor" | grep -iPo \>Jeopardy.*?\< | cut -c 2- | rev | cut -c 2- | rev)
echo -e \\n\\n\\n ~~~~~~~~~~~~~~~~~~~~~ \\n Name: $name
## Alternative way to get date
# online_date=$(echo $name | cut -d . -f2-4)

# Get date of torrent
online_date=$(echo "$each_tor" | grep -Po href=\"/torrent/.*?\" | cut -d \. -f2-4)
echo -e \\n \ Disk date: $file_date
echo Online date: "$online_date"

# Get magnet URL
mag_link=$(echo "$each_tor" | grep -o "<a href=\"magnet.*title" | grep -oE '".*?"' | cut -d \" -f2)
#echo -e \\n Magnet link: "$mag_link"

# Get name of uploader
uploader=$(echo "$each_tor" | grep -Po href=\"/user/.*?\" | cut -d / -f3)
#echo -e \\n Uploader:  "$uploader"



# Compare file and online dates
if [[ "$file_date" < "$online_date" ]]
then
echo -e \\n ~~~ More recent episode found online

# Check date format
date_check=$(echo $online_date | grep -E ^[0-9]{4}\.[0-9]{2}\.[0-9]{2}$)
if [[ -z $date_check ]]
then
echo -e \\n Online date check failed. Skipping ...
continue
fi

# Compare uploaders
if [[ "$uploader" == cptnkirk ]] || [[ "$uploader" == mwoz ]]
then
echo -e \\n Uploader check passed: "$uploader"




# Forward a port and start Deluge only if it is not already running
del_check=$(pidof deluge-gtk)

if [[ -z $del_check ]]
then

    # Get VPN forwarded port
    port=$(piactl get portforward)

    # Make sure port var is a number
    port_check=$(echo $port | grep -E [0-9]{5})

    # Check port number
    if [[ -z $port_check ]]
    then
        echo -e \\n ~~~ Unable to retrieve forwarded port from VPN
        
    else
        echo -e \\n Forwarding port: $port
        


        ## Previous method attempts
        #sed "s/\"listen_ports\".*\],/\"listen_ports\": \[$port, $port\],/g" core.conf > t.txt
        #sed "s/\"outgoing_ports\".*\],/\"outgoing_ports\": \[$port, $port\],/g" t.txt > core.conf

        #aaa=$(cat n.txt | sed "s/\"outgoing_ports\".*\],/\"outgoing_ports\": \[$port, $port\],/g")
        #aaa=$(echo $aaa | sed "s/\"listen_ports\".*\],/\"listen_ports\": \[$port, $port\],/g")

        # Replace all 5 digit numbers in config file with new port value. Dangerous?
        #aaa=$(cat n.txt | sed "s/[0-9]\{5\}/$port/g")

        # Port forward by editing Deluge config file
        cd /home/joepers/.config/deluge/
        
        # Restore original IFS
        IFS=$oldifs

        # Find port key and value lists using regex. Replace with key and new port value lists. eg:
        # Orignal: "outgoing_ports": [ 11111, 11111 ],
        # Becomes: "outgoing_ports": [ 12345, 12345 ],
        ## Convert newlines to spaces?
        temp_conf=$(cat core.conf)
        temp_conf=$(echo $temp_conf | sed "s/\"outgoing_ports\": \[ [0-9]\{5\}, [0-9]\{5\}/\"outgoing_ports\": \[ $port, $port/")

        # Same but use previously created var instead of text file
        temp_conf=$(echo $temp_conf | sed "s/\"listen_ports\": \[ [0-9]\{5\}, [0-9]\{5\}/\"listen_ports\": \[ $port, $port/")

        # Read conf var then write changes to config file using jq to preserve original pretty formatting
        jq . <<< $temp_conf > core.conf

        # Check if port was written to conf file
        core_check=$(grep $port, ~/.config/deluge/core.conf)
        if [[ -z $core_check ]]
        then
        echo -e \\n ~~~ Port forwarding failed to write to conf file
        fi

        # Restore IFS to newline
        IFS=$'\n'

        # Start Deluge and detach
        deluge-gtk > /dev/null 2>&1 &
        sleep 2

    fi

# Deluge is already running
else
    echo -e \\n Deluge is already running: $del_check

fi


# Add torrent to Deluge
echo -e \\n Adding to Deluge: \\n$name
deluge-gtk "$mag_link" &

# Skip if unapproved uploader is detected
else
echo -e \\n Uploader check failed: "$uploader"
fi

# Exit when disk episode is as recent as online date
else
echo -e \\n Most recent episode already on disk. Exiting ...
exit
fi



echo -e \\n\\n Checking next online episode ...

done


      















