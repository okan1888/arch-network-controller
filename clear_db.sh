#!/bin/bash

# Input file
FILE="/SRL-DEV-LAB/ARCH_NW_CONTROLLER/configDB.csv"

# Check if file exists
if [[ ! -f "$FILE" ]]; then
    echo "Error: File '$FILE' does not exist."
    exit 1
fi

# Count the number of lines in the file
LINE_COUNT=$(wc -l < "$FILE")

# If line count is greater than 1, keep only the first line
if [[ $LINE_COUNT -gt 1 ]]; then
    # Use sed to delete all lines except the first line
    sed -i '2,$d' "$FILE"
    echo "All lines except the first line have been deleted."
else
    echo "File '$FILE' has 1 or no lines. No changes made."
fi

