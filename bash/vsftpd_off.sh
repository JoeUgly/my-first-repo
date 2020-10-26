#!/usr/bin/env bash

# Description: Stop vsftpd server, unmount partition, and reset firewall



echo -e \\n Stopping vsftpd ... \\n\\n

# Exit on any non-zero status
set -e


# Stop vsftpd server
sudo systemctl stop vsftpd

echo -e \\n\\n ~~~ vsftpd has been shut down. ~~~ \\n

# Check if vsfptd is enabled at startup
if [[ $(systemctl is-enabled vsftpd) != 'disabled' ]]
then
echo -e vsftpd is enabled at startup. Disable? \\ny/n
read en_resp

    # Disable vsftpd at startup
    if [[ "$en_resp" =~ ^('yes'|'y')$ ]]
    then
    sudo systemctl disable vsftpd
    echo -e vsftpd disabled at startup
    fi
fi


# Unmount partition, ignore error if already unmounted
sudo umount -v UUID=1b0cbce9-8df4-4119-ad94-23a6641519f9 || [ $? -eq 32 ]
echo -e \\n


# Display all firewall rules
sudo ufw status numbered

# Prompt to delete all firewall rules
echo -e \\n\\n Delete all firewall rules? \\ny/n
read resp

if [[ "$resp" =~ ^('yes'|'y')$ ]]
then
sudo ufw --force reset
else
echo -e \\n No changes made to firewall
fi






















