while IFS= read -r file; do
  echo "Moving - $file to current directory"
  cp /mnt/object/raw-data/$file .
  echo "Untar $file"
  tar -xvf $file
  dirname="${file%.tar}"
  echo "Dir name: $dirname"
  mkdir "text_$dirname"
  echo "Processing the pdfs in the $dirname folder"
  python3 pdf-to-text-from-folder.py /home/cc/Neura-Scholar/data-pipeline-files/$dirname /home/cc/Neura-Scholar/data-pipeline-files/"text_$dirname" 16
  tar -cvf "text_${dirname}.tar" "text_$dirname"
  rclone copy -vP "text_${dirname}.tar" "chi_tacc:${RCLONE_CONTAINER}/text-files-data"
  rm -rf arxiv_* text_*
done < tar_files_list.txt
