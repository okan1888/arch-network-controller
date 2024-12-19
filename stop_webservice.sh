#!/bin/bash

# Pattern to search for
PATTERN="uvicorn"

# Check if the pattern is provided
if [[ -z "$PATTERN" ]]; then
    echo "Usage: $0 <process_pattern>"
    exit 1
fi

# Find the PID(s) of the process matching the pattern
PIDS=$(ps aux | grep "$PATTERN" | grep -v grep | awk '{print $2}')

# Check if any PIDs were found
if [[ -z "$PIDS" ]]; then
    echo "No process found matching pattern '$PATTERN'."
    exit 0
fi

# Kill the process(es)
echo "Killing process(es) matching pattern '$PATTERN': $PIDS"
for PID in $PIDS; do
    kill -9 "$PID"
    echo "Killed process with PID: $PID"
done

