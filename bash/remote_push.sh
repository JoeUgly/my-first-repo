#!/usr/bin/env bash

# Desc: Copy code dir to remote server using SSH key auth and tarball compression


# To do:
# include this in backup.sh?
# delete previous data? rm -r /home/joe/.backup/code; cat | tar --overwrite -xz -C /home/joe/.backup



set -e


cd /home/joepers/


# Create tarball, pv for progress, login to remote host, copy to hidden backup dir
tar -czv code/ | pv | ssh -p 17589 -i /home/joepers/.ssh/id_rsa root@134.122.12.32 'cat | tar --overwrite -xz -C /home/joe/.backup'


