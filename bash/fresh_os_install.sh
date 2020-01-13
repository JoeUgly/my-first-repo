#!/usr/bin/env bash

# Description: Get a new Ubuntu OS set up the way you like it


# To do:
# download PIA client +
# copy most recent backup dir to home dir +
# mount drive 2 to backup dir +


# Later version:
# install docker
# copy non one timers to appropriate locations. all items in backup.sh
# keyboard shortcuts -



# Copy backups to primary drive
# Create drive 1 backup dir
mkdir -v /home/joepers/backup/

## make drive_2 dir first?
# Set mount point for drive 2 in backup dir
sudo mount -v --target /home/joepers/backup/drive_2/ /dev/sdb1

# use drive_1 and drive_2 dirs in backup dir?
# Copy one timers backups from drive 2 to drive 1
sudo cp -rv /home/joepers/backup/drive_2/one_timers/ /home/joepers/backup/

# Select most recent monthly dir in drive 2 by name
mon_path=$(ls /mnt/1886dad6-7316-45dd-9d7c-6d1a90312619/ | sort | head -n1)

# Copy monthly dir from drive 2 to drive 1
sudo cp -rv "$mon_path" /home/joepers/backup/

## check make sure everything worked so far
echo -e \\n\\n pause
read


# Install software from repos
sudo add-apt-repository universe
sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get -y install cinnamon-desktop-environment lightdm conky-all deluge vsftpd keepassxc exfat-utils exfat-fuse ffmpeg curl vlc mkvtoolnix


# Enable firewall
sudo ufw enable


# Copy Conky files. Must use "cat <> | sudo tee <>" to write to root files
cat "$mon_path"/other/conky.conf | sudo tee /etc/conky/conky.conf

# Allow Conky to read HDD temperature
sudo chmod u+s /usr/sbin/hddtemp


# Remove Amazon app
sudo rm /usr/share/applications/amazon


# Install HTTP server and allow CGI scripts for Joes Jorbs
sudo apt-get -y install apache2
sudo a2enmod cgi
sudo systemctl restart apache2
# copy cgi to /usr/lib/cgi-bin/<index.py> 
# copy html files to /var/www/html/<ttt.html>

# Install PIA VPN client
# Get HTML for recent PIA installers
pia_html=$(curl -sL "https://www.privateinternetaccess.com/pages/changelog")

# Select most recent Linux installer
pia_installer=$(echo "$pia_html" | grep -Po pia-linux-.*?\.run | sort -r | head -n 1)

# Install VPN client
cd /home/joepers/Downloads/
sh "$pia_installer"


# Copy Desktop files
cp -v "$mon_path"/other/info /home/joepers/Desktop/
cp -v "$mon_path"/other/python3_notes /home/joepers/Desktop/
cp -v "$mon_path"/other/ubuntu_notes /home/joepers/Desktop/
cp -v "$mon_path"/other/words.txt /home/joepers/Desktop/


# Copy bash aliases
cat "$mon_path"/other/.bash_aliases | sudo tee /home/joepers/.bash_aliases


# Copy VSFTPD files
cat "$mon_path"/other/vsftpd/vsftpd.conf | sudo tee /etc/vsftpd.conf
cat "$mon_path"/other/vsftpd/vsftpd.chroot_list | sudo tee /etc/vsftpd.chroot_list
cat "$mon_path"/other/vsftpd/vsftpd.email_passwords | sudo tee /etc/vsftpd.email_passwords
cat "$mon_path"/other/vsftpd/vsftpd.userlist | sudo tee /etc/vsftpd.userlist


# Python dependencies
sudo apt-get -y install python3-pip
python3 -m pip install --upgrade pip
sudo python3 -m pip install bs4 selenium html5lib docker pandas xlrd


# Docker
#sudo docker pull scrapinghub/splash















