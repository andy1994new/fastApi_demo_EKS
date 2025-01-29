#!/bin/bash

set -e

new_ver=$1
service_name=$2

image_name="${service_name}_service"
yaml_name="${service_name}-service.yaml"

echo "new version: $new_ver"

# # Build the Docker image
# docker build -t andy2025/$image_name:$new_ver docker/$image_name

# # Tag the image
# docker tag andy2025/$image_name:$new_ver andy2025/$image_name:latest

# # Push the new version and latest tag to DockerHub
# docker push andy2025/$image_name:$new_ver
# docker push andy2025/$image_name:latest

# Create temporary folder
tmp_dir=$(mktemp -d)
echo $tmp_dir

# Clone GitHub repo
git clone https://github.com/andy1994new/argo.git $tmp_dir

# Update image tag

sed -i -e "s/andy2025\/$image_name:.*/andy2025\/$image_name:$new_ver/g" $tmp_dir/$yaml_name


# Commit and push
cd $tmp_dir

# Set Git user identity for CI/CD (Fixes "Author identity unknown" error)
git config --global user.email "ci-bot@example.com"
git config --global user.name "CI Bot"

git add .
git commit -m "Update image to $new_ver"
git push https://x-access-token:${GH_TOKEN}@github.com/andy1994new/argo.git

# Optionally on build agents - remove folder
rm -rf $tmp_dir