#!/bin/bash

set -e

# Step 1: Ask for new version
echo "Current version: $(cat version.txt)"
read -p "Enter new version (e.g. 0.1.1): " new_version

# Step 2: Update version.txt
echo $new_version > version.txt
echo "Updated version.txt to $new_version"

# Step 3: Clean previous builds
echo "Cleaning old builds..."
rm -rf build dist *.egg-info

# Step 4: Build the package
echo "Building package..."
python -m build

# Step 5: Upload to PyPI
echo "Uploading to PyPI..."
twine upload dist/*

echo "✅ Upload complete for version $new_version!"
