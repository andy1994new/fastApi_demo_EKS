#!/bin/bash

set -e

new_ver=$1

echo "new version: $new_ver"

# # Simulate release of the new docker images
# docker tag test:latest andy2025/test:$new_ver

# # Push new version to dockerhub
# docker push andy2025/test:$new_ver

# Create temporary folder
tmp_dir=$(mktemp -d)
echo $tmp_dir

# Clone GitHub repo
git clone https://github.com/andy1994new/argo.git $tmp_dir

# Update image tag

sed -i '' -e "s/andy2025\/test:.*/andy2025\/test:$new_ver/g" $tmp_dir/test.yaml

# Commit and push
cd $tmp_dir
git add .
git commit -m "Update image to $new_ver"
git push

# Optionally on build agents - remove folder
rm -rf $tmp_dir
