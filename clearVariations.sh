#!/bin/bash
# Loop through directories that start with a number in the current directory
for dir in [0-9]*/; do
    if [ -d "$dir" ]; then
        rm -rf "$dir"
    fi
done