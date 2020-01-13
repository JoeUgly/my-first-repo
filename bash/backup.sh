#!/usr/bin/env bash

# Description: Copy certain directories and files to monthly directory in backup drive.
# Certain dirs = ~/code/, ~/code/bash/, ~/Documents/
# Certain files = words.txt, info, How_to_do_things_in_Ubuntu, python, vsftpd, conky, .bash_aliases
# if orig file is deleted this program will not delete the backup file

# Use manual backups for: keepass, photos, Downloads, taxes, crypto, torrents, converted vids, old anarcho texts, diaro, 




# To do:
# verify with checksum
# determine what needs rolling backups vs one copy



# Exit on any non-zero status
set -e


# Set the date
dater=$(date +%-m_%y)
echo -e \\nDate code = \"$dater\"


# Mount backup drive, set mount_check if already mounted
sudo mount -v /dev/sdb1 || if [[ "$?" -eq 32 ]]; then mount_check=True; fi


# Check if backup drive is accessible
if [[ -n $(ls /home/joepers/backup/drive_2/) ]]; then 
cd /home/joepers/backup/drive_2

# Create monthly directory if it doesn't exist
mkdir -pv "$dater/code/bash" "$dater/other/Documents" "$dater/other/vsftpd"

# Exit if drive is not mounted
else echo \"/home/joepers/backup/drive_2/\" cannot be accessed. Exiting ...
exit
fi

# Set absolute path to monthly destination directory
if [[ -d /home/joepers/backup/drive_2/$dater ]]; then
    mon_dir_dest=/home/joepers/backup/drive_2/$dater

else echo Absolute backup location cannot be found. Exiting ...
exit
fi

echo -e Destination = \"$mon_dir_dest\" \\n

## fix
# Copy files in ~/code/ dir
#find ~/code/ -type f -not -path "*.git*" -exec cp -ruv {} $mon_dir_dest/code/ \;
#cp -uvr ~/code/ $mon_dir_dest/code/

# Copy code dir without git dirs
rsync -ruv /home/joepers/code/ $mon_dir_dest/code/ --exclude .git


# Copy files in ~/code/bash/ dir
#find ~/code/bash/ -maxdepth 1 -type f -exec cp -uv {} $mon_dir_dest/code/bash/ \;

## why max depth?
## why find?
# Copy files in ~/Documents/ dir
find /home/joepers/Documents/ -maxdepth 1 -type f -exec cp -uv {} $mon_dir_dest/other/Documents/ \;


# Copy ~/Desktop/ files
cd /home/joepers/Desktop/
cp -uv info words.txt ubuntu_notes python3_notes $mon_dir_dest/other/


# Copy vsftpd files
find /etc/vsftpd.* -maxdepth 1 -type f -exec cp -uv {} $mon_dir_dest/other/vsftpd/ \;


# Copy conky file
find /etc/conky/conky.conf -maxdepth 1 -type f -exec cp -uv {} $mon_dir_dest/other/ \;


# Copy .bash_aliases
cp -uv /home/joepers/.bash_aliases $mon_dir_dest/other/

# Copy webpage and cgi
cp -ruv /var/www/html/ $mon_dir_dest/code/
cp -ruv /usr/lib/cgi-bin/ $mon_dir_dest/code/

# Unmount if backup drive started unmounted
if [[ -z $mount_check ]]
then
echo
sudo umount -v /dev/sdb1
fi


echo -e \\n\\n ~~~  All operations complete.  ~~~ \\n

















