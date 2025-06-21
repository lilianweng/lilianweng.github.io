#!/usr/bin/env bash
# Clean LaTeX auxiliary files recursively in the current directory and all subdirectories

EXTS=("aux" "bbl" "bcf" "blg" "log" "nav" "out" "snm" "toc" "run.xml" "synctex.gz")

DIR="."  # Set to current directory

for ext in "${EXTS[@]}"; do
    find "$DIR" -type f -name "*.$ext" -exec rm -f {} +
done

echo "LaTeX auxiliary files in current directory and all subdirectories deleted."