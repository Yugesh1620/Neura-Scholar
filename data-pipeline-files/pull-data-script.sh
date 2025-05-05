#!/bin/bash
while IFS= read -r line; do
  echo "Downloading : $line"
  base="arxiv_$(basename "$line")"
  mkdir "$base"
  gsutil -m rsync -d -r "$line" "$base"
  tar -cvf "$base.tar" "$base"
  rclone copy -vP "${base}.tar" "chi_tacc:${RCLONE_CONTAINER}/raw-data"
  rm -r "$base" "${base}.tar"
done < folders_list.txt

