#!/usr/bin/env bash

# Description: Get a new Ubuntu install set up the way you like it


# To do:
# copy non one timers to appropriate locations. all items in backup.sh
# use drive_1 and drive_2 dirs in backup dir?
# determine sudo usage
# vsftpd needs dedicated user eg sammy
# update fstab section with joerassic park partition
# fstab uuids change after formatting during installation
# exclude old phone photos
# remove verbose. use echo descriptions instead
# bash aliases
# skip section if it is complete already
# ums is broken
# code dir and others are saved as root + dont use sudo with copy
# copy .ssh dir +
# install retroarch

# ip checking torrents:
#https://ipleak.net/
#magnet:?xt=urn:btih:523fc51cdb15f70ce55890f0321975d29b7a828e&tr=https://ipleak.net/announce.php%3Fh%3D523fc51cdb15f70ce55890f0321975d29b7a828e&dn=ipleak.net+torrent+detection

#https://torguard.net/checkmytorrentipaddress.php
#magnet:?xt=urn:btih:4bd780c15ec11e860446a35bd15880e211640260&dn=checkmyiptorrent+Tracking+Link&tr=http%3A%2F%2F34.204.227.31%2F


# Do we need?:
# apache
# ufw


# Do manually
# prompt color
# bash history length
# keyboard shortcuts
# wide panel icons: right click app panel icon, pref, config: (general tab for ungrouping) (panel tab, button label:window title for icon size)

# docker rootless
#curl -fsSL https://get.docker.com/rootless | sh
#uidmap
#pull as nonroot
#
#
#




# Exit on non-zero status
set -e


# Write fstab file
: '
cat >/etc/fstab <<EOL
# <file system> <dir> <type> <options> <dump> <pass>

# Swap
UUID=6fac9b36-2b2a-43aa-99eb-29c2b712d9fc	none      	swap      	defaults  	0 0

# Root
UUID=3ddc9818-ddfa-41aa-a0c8-cd03b388ef5e	/         	ext4      	rw,relatime	0 1

# Video
UUID=a0b51b49-88e3-43bc-8c48-d5d49f4ae5b3 /home/joepers/Videos ext4 defaults 0 0


# Backup
UUID=1886dad6-7316-45dd-9d7c-6d1a90312619 /home/joepers/backup/drive_2 ext4 nosuid,nodev,nofail,comment=x-gvfs-show 0 2
EOL
'



# Create drive 2 backup dir
mkdir -pv /home/joepers/backup/drive_2/

# Mount backup drive
sudo mount -v UUID=1886dad6-7316-45dd-9d7c-6d1a90312619 /home/joepers/backup/drive_2 || if [[ "$?" -eq 32 ]]; then echo Backup drive already mounted; fi

# Copy one timers backups from drive 2 to drive 1
cp -ruv /home/joepers/backup/drive_2/one_timers/ /home/joepers/backup/

# Select most recent monthly dir in drive 2 by name. Exclude non-monthly dirs
mon_path=/home/joepers/backup/drive_2/$(ls /home/joepers/backup/drive_2/ | sort -r | grep ^[0-9] | head -n 1)
echo -e \\n\\n Using monthly directory: $mon_path \\n\\n

# Copy monthly dir from drive 2 to drive 1
cp -ruv "$mon_path" /home/joepers/backup/

# Copy code dir to drive 1
cp -ruv "$mon_path"/code/ /home/joepers/

# Copy ssh dir
cp -ruv "$mon_path"/.ssh /home/joepers/



# Install software from repos
#sudo add-apt-repository universe # 'universe' distribution component is already enabled for all sources.
echo -e \\n\\n Begin repo
sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get -y install cinnamon-desktop-environment lightdm conky-all deluge vsftpd keepassxc exfat-utils exfat-fuse ffmpeg curl vlc mkvtoolnix docker.io mediainfo dcraw mplayer mencoder kdenlive wmctrl pv jq # apache2 blender



# Copy Conky files. Must use "cat <> | sudo tee <>" to write to root files
echo -e \\n\\n Begin Conky
cat "$mon_path"/other/conky.conf | sudo tee /etc/conky/conky.conf

# Allow Conky to read HDD temperature
sudo chmod u+s /usr/sbin/hddtemp



# Install PIA VPN client
echo -e \\n\\n Begin PIA

# Get HTML for recent PIA installers
pia_html=$(curl -sL "https://www.privateinternetaccess.com/pages/changelog")

# Select most recent Linux installer
pia_installer=$(echo "$pia_html" | grep -Po pia-linux-.*?\.run | sort -r | head -n 1)
echo Using: $pia_installer

# Download installer
cd /home/joepers/Downloads/
wget https://installers.privateinternetaccess.com/download/"$pia_installer"

# Install VPN client
echo Running installer ...
sh "$pia_installer"


# Copy Desktop files
echo -e \\n\\n Begin copy desktop files
cp -v "$mon_path"/other/info /home/joepers/Desktop/
cp -v "$mon_path"/other/python3_notes /home/joepers/Desktop/
cp -v "$mon_path"/other/ubuntu_notes /home/joepers/Desktop/
cp -v "$mon_path"/other/words.txt /home/joepers/Desktop/




# Copy vsftpd files
echo -e \\n\\n Begin copy vsftpd files
cat "$mon_path"/other/vsftpd/vsftpd.conf | sudo tee /etc/vsftpd.conf
cat "$mon_path"/other/vsftpd/vsftpd.chroot_list | sudo tee /etc/vsftpd.chroot_list
cat "$mon_path"/other/vsftpd/vsftpd.email_passwords | sudo tee /etc/vsftpd.email_passwords
cat "$mon_path"/other/vsftpd/vsftpd.userlist | sudo tee /etc/vsftpd.userlist


# Install Python packages
echo -e \\n\\n Begin Python packages
sudo apt-get -y install python3-pip ## move up there?
python3 -m pip install --upgrade pip
sudo python3 -m pip install bs4 selenium html5lib docker pandas xlrd regex fuzzyquzzy


# Install Splash Docker container
echo -e \\n\\n Begin Splash Docker container
sudo docker pull scrapinghub/splash




: '
# Get HTML for recent UMS installers
echo -e \\n\\n Begin UMS
ums_html=$(curl -sL 'https://www.fosshub.com/Universal-Media-Server.html')

# Select most recent Linux x86_64 installer
ums_installer=$(echo "$ums_html" | grep -oP href=.*?x86_64.tgz | head -n 1 | cut -d \" -f 2)

# Download installer
cd /home/joepers/Downloads/
wget $ums_installer

# Extract installer into home dir
ums_installer=$(echo $ums_installer | cut -d = -f 2)
tar xzvf $ums_installer -C /home/joepers/

## Run at startup
'



# Remove preinstalled apps
sudo apt-get -y purge brasero blueman thunderbird transmission-common transmission-gtk
sudo apt-get -y autoremove


# Detect sensors
sudo sensors-detect




# Enable firewall
#sudo ufw enable


# Allow CGI scripts for Joes Jorbs
#sudo a2enmod cgi
#sudo systemctl restart apache2

# Copy HTML files to Apache default location
#cp -uv "$mon_path"/code/jj_v2/current/*.html /var/www/html/

# Copy CGI scripts to Apache default location
#cp -uv "$mon_path"/code/jj_v2/current/results.py /usr/lib/cgi-bin/













