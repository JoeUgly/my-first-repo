#!/usr/bin/env bash

# Description: Start vsftpd server

# Features:
# Mounts Joerassic Park partition
# Punches holes in firewall for FTP auth and transfer
# Whitelists specific IP addresses
# Retrieves server's public IP address
# Start server


# To do:
# use uuid not device blocks +
# allow "all" option for IP whitelist +
# hosts.deny is deprecated. use ufw +
# update off_vsfptd +
# display public IP +
# display login password? +



echo -e \\n Starting vsftpd ... \\n\\n

# Exit on any non-zero status
set -e

# Mount partition, ignore error if already mounted
sudo mount -v UUID=1b0cbce9-8df4-4119-ad94-23a6641519f9 || [ "$?" -eq 32 ]
echo


# Prompt for client IP address to whitelist
echo -e \\n\\n Enter the IPv4 address to allow. Leave blank to allow all.
read resp

# Edit firewall with specific IP address
if [[ -n "$resp" ]]
then
sudo ufw allow 21/tcp from "$resp"
sudo ufw allow 13061/tcp from "$resp"

# Edit firewall allowing all IP addresses
else
sudo ufw allow 21/tcp
sudo ufw allow 13061/tcp
fi


# Display public and local IP addresses and login password
public_ip=$(dig @ns1-1.akamaitech.net ANY whoami.akamai.net +short)
local_ip=$(ifconfig | awk '/inet 192.168./ {print $2;}')
pw=$(cat /etc/vsftpd.email_passwords)

echo -e \\n\\n Local address:\\n$local_ip\\n\\n Public address:\\n$public_ip\\n\\n Password:\\n$pw\\n\\n


# Start vsftpd
sudo systemctl start vsftpd

echo -e ~~~ vsftpd is now running. ~~~\\n





