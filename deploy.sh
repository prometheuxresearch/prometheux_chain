#!/bin/bash

set -e

echo "Current version: $(cat version.txt)"
read -p "Enter new version (e.g. 0.1.1): " new_version
# write the new version to version.txt
if [[ -z "$new_version" ]]; then
    echo "Version cannot be empty. Exiting."
    exit 1
fi
echo "Updating version to $new_version..."
echo "$new_version" > version.txt

echo "Cleaning old builds..."
rm -rf build dist *.egg-info

echo "Building package..."
python -m build

echo "Uploading to PyPI..."
twine upload dist/*

echo "✅ Upload complete for version $new_version!"

echo $new_version > version.txt
echo "Updated version.txt to $new_version"
