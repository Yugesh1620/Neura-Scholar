find /mnt/object/text-files-data/ -name "*.tar" | \
  xargs -n 1 -P 16 -I{} sh -c 'tar -tf "{}" | grep -v "/$" | xargs -n 1 basename' > all_files_list.txt

