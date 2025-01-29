#!/bin/bash

set -e

new_ver=$1  # First argument: new version
service_name=$2  # Second argument: service name

if [[ -z "$new_ver" || -z "$service_name" ]]; then
    echo "Usage: $0 <new_version> <service_name>"
    exit 1
fi

echo "Building and pushing $service_name with version: $new_ver"

# Build the Docker image
docker build -t andy2025/$service_name:$new_ver docker/$service_name

# Tag the image
docker tag andy2025/$service_name:$new_ver andy2025/$service_name:latest

# Push the new version and latest tag to DockerHub
docker push andy2025/$service_name:$new_ver
docker push andy2025/$service_name:latest

# Create a temporary folder
tmp_dir=$(mktemp -d)
echo "Temporary directory: $tmp_dir"

# Clone GitHub repo
git clone https://github.com/andy1994new/argo.git $tmp_dir

# Update image tag in deployment YAML
sed -i -e "s|andy2025/$service_name:.*|andy2025/$service_name:$new_ver|g" $tmp_dir/$service_name.yaml

# Commit and push changes
cd $tmp_dir
git add .
git commit -m "Update $service_name image to $new_ver"
git push

# Cleanup
rm -rf $tmp_dir

echo "Successfully updated $service_name to version $new_ver"
