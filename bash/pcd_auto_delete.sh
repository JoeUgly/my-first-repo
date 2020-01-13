#!/usr/bin/env bash

# Desc: Delete all duplicate movies created by pcd.sh


# To do:
# some filenames have been altered by fuck_all. run fuck_all on tor dir and delete_these?
# delete the directory, not just the video. +
# always use abs path +




# For safety
cd /mnt/a0b51b49-88e3-43bc-8c48-d5d49f4ae5b3/tors/


# This is the only way I know how to list files with whitespace
IFS=$'\n'


the_files=$(cat ~/code/bash/pcd_delete_these)


# List the files and warning prompt
echo
for i in $the_files; do echo -e \\n "$i"; done
echo -e \\n\\n ========== \ Warning \ ========== \\n\\n All of these files will be deleted. Continue? \\n y/n

read resp

# Exit if response is not yes
if [[ "$resp" != 'yes' ]] && [[ "$resp" != 'y' ]]
then
echo Exiting ...
exit
fi


# Loop through each file in the pcd_delete_these text file
for i in $the_files
    do
    echo -e \\n\\n

    # Delete each file or dir
    rm -rv "$i"
    e_c=$?

        # Don't remove entry if error occured
        if [[ $e_c == 0 ]]
        then

        # Remove entry from pcd_delete_these text file using inverse search
        grep -Fv "$i" ~/code/bash/pcd_delete_these > filename2; mv filename2 ~/code/bash/pcd_delete_these
        echo -e \\n "$i" removed from pcd_delete_these
        fi

    

done


echo -e \\n\\n All operations complete.



















