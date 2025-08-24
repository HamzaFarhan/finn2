#!/bin/bash
# Create the required directories
mkdir -p /data/workspaces

# Run the original command
exec "$@"