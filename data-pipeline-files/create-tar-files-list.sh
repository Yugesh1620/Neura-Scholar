#!/usr/bin/env bash


sudo mkdir -p /mnt/object
sudo chown -R cc /mnt/object
sudo chgrp -R cc /mnt/object
rclone mount chi_tacc:object-persist-project-22 /mnt/object --read-only --allow-other --daemon
ls /mnt/object
ls /mnt/object/raw-data/ > tar_files_list.txt
cat tar_files_list.txt
