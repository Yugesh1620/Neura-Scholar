#!/bin/bash

# Set the parent folder (you can also use `.` if running from that folder)
PARENT_DIR="/Users/riyagarg/Neura-Scholar/arxiv-data/arxiv/pdf"

# Move into parent directory
cd "$PARENT_DIR" || exit 1

# Loop through each subfolder
for dir in */ ; do
    # Check if it's a directory
    if [ -d "$dir" ]; then
        echo "Moving contents of $dir to $PARENT_DIR"
        mv "$dir"* "$PARENT_DIR" 2>/dev/null
        rmdir "$dir"
    fi
done

echo "Done. All subfolder contents moved to $PARENT_DIR."

