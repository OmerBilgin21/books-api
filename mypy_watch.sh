#!/bin/bash

# Check if entr is installed
if ! dpkg -l | grep -q entr; then
	echo "entr package is used to watch the files for changes."
	echo "However, it is not found on your system. Installing..."
	sudo apt-get install -y entr
	echo "Installation done."
fi

# Get the current directory
current_dir=$(pwd)

# Function to find Python files in the v2 directory
file_find() {
	find src -name "*.py"
}

# Activate the virtual environment
source venv/bin/activate

echo "Starting mypy with entr"
# Use file_find function with entr to run mypy
file_find | entr -c mypy . --config-file="$current_dir"/pyproject.toml --follow-imports=silent
