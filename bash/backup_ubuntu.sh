#!/usr/bin/env bash

# Description: Copy files to monthly directory in backup drive


# if orig file is deleted, this program will not delete the backup file
# uses UUID to address backup disk and mount point

# Use manual backups for: keepass, photos, Downloads, taxes, crypto, torrents, converted vids, old anarcho texts, diaro, PS4


# To do:
# determine what needs rolling backups vs one copy
# merge taxes and financials







# Exit on any non-zero status
set -e


# Set the date
dater=$(date +%-m_%y)
echo -e \\n Date code = \"$dater\" \\n


# Mount backup drive. Save original mount state
sudo mount -v UUID=1886dad6-7316-45dd-9d7c-6d1a90312619 || if [[ "$?" -eq 32 ]]; then was_unmounted=True; fi




# Create monthly dir and subdirs if they doesn't exist already
mon_dir_dest=/home/joepers/backup/drive_2/$dater
mkdir -pv "$mon_dir_dest/vsftpd" "$mon_dir_dest/Desktop"


# Set absolute path to monthly destination directory
if [[ -d $mon_dir_dest ]]; then
    echo -e \\n Destination = $mon_dir_dest \\n\\n

# Exit if mount point is invalid
else
    echo Absolute backup location cannot be found. Exiting ...
    exit
fi





# Copy code dir
#sudo cp -ruv /home/joepers/code/ $mon_dir_dest/

# Copy code dir without git dirs
rsync -ruv /home/joepers/code/ $mon_dir_dest/code/ --exclude .git


# Copy files in Documents dir
sudo cp -ruv /home/joepers/Documents/ $mon_dir_dest/


# Copy Desktop files
cd /home/joepers/Desktop/
sudo cp -uv info words.txt ubuntu_notes python3_notes workout.ods $mon_dir_dest/Desktop


# Copy conky file
sudo cp -uv /etc/conky/conky.conf $mon_dir_dest/


# Copy bash aliases
sudo cp -uv /home/joepers/.bashrc $mon_dir_dest/

# Copy SSH keys
sudo cp -ruv /home/joepers/.ssh $mon_dir_dest/


# Unmount if backup drive was originally unmounted
if [[ -z $was_unmounted ]]
then
echo
sudo umount -v UUID=1886dad6-7316-45dd-9d7c-6d1a90312619
fi


echo -e \\n\\n ~~~  All operations complete.  ~~~ \\n

















