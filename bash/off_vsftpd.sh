#!/usr/bin/env bash

# Description: Shutdown vsftpd and prerequisites



echo -e \\n Stopping vsftpd ... \\n\\n

# Exit on any non-zero status
set -e

# Ignore error if already unmounted
sudo umount -v /dev/sdb2 || [ $? -eq 32 ]
echo
sudo systemctl stop vsftpd

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


sudo ufw delete allow 21/tcp
sudo ufw delete allow 13061/tcp

# Check for any other ufw rules
ufw_check=$(sudo ufw status)
if [[ "$ufw_check" != 'Status: active' ]]
then
echo -e \\n\\n\\n "$ufw_check"
echo -e \\n\\n ~~~~~~  ufw has additional rules. Check it out.  ~~~~~~
fi


# Edit /etc/hosts.allow to remove IP address
echo -e \\n\\n Edit /etc/hosts.allow in Nano? \\ny/n
read resp

if [[ "$resp" =~ ^('yes'|'y')$ ]]
then
sudo nano /etc/hosts.allow
else
echo -e \\n No changes made to /etc/hosts.allow
fi


echo -e \\n\\n ~~~ VSFTPD has been shut down. ~~~ \\n



: '
# Remove user IP address from /etc/hosts.allow
echo -e \\n\\n Enter the IPv4 address to remove
read resp

# Omit empty responses
if [[ -n $resp ]]
then
echo vsftpd : $resp >> /etc/hosts.allow
echo -e \\n $resp appended to /etc/hosts.allow
else
echo -e \\n No changes made to /etc/hosts.allow
fi
'
