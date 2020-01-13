
# Description: Start vsftpd and prerequisites



echo -e \\n Starting vsftpd ... \\n\\n

# Exit on any non-zero status
set -e

# Ignore error if already mounted
sudo mount -v /dev/sdb2 || [ "$?" -eq 32 ]
echo
sudo systemctl start vsftpd
sudo ufw allow 21/tcp
sudo ufw allow 13061/tcp


# Add user IP address to /etc/hosts.allow
echo -e \\n\\n Enter the IPv4 address to allow
read resp

# Omit empty responses
if [[ -n "$resp" ]]
then

# Append response with root
echo vsftpd : "$resp" | sudo tee -a /etc/hosts.allow
echo -e \\n "$resp" appended to /etc/hosts.allow
else
echo -e \\n No changes made to /etc/hosts.allow
fi

# Display public and local IP addresses
public_ip=$(dig @ns1-1.akamaitech.net ANY whoami.akamai.net +short)
local_ip=$(ifconfig | awk '/inet 192.168./ {print $2;}')
pw=$(cat /etc/vsftpd.email_passwords)

echo -e \\n\\n Local address: $local_ip \\n Public address: $public_ip \\n Password: $pw \\n\\n

echo -e ~~~ VSFTPD is now running. ~~~\\n





