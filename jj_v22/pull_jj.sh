#!/usr/bin/env bash

# Desc: Copy files from remote host using SSH key auth and port


# to do:
# include apache config files +




# Where to save the files
loc_dir=/home/joepers/code/jj_v22/current

# Dir and files to copy
rem_index=/var/www/html/index.html
rem_help=/var/www/html/help.html
rem_res=/usr/lib/cgi-bin/results.py

rem_conf=/etc/apache2/apache2.conf


# Copy dir and files to local host
scp -rP 17589 root@134.122.12.32:"$rem_index $rem_help $rem_res $rem_conf" $loc_dir




# One liner
#scp -rP 17589 root@134.122.12.32:"/var/www/html/ /usr/lib/cgi-bin/results.py" /home/joepers/code/jj_v2/current/











