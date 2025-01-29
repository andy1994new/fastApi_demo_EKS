#!/bin/bash

set -e

new_ver=$1
service_name=$2

image_name="${service_name}_service"
yaml_name="${service_name}-service.yaml"

echo "new version: $new_ver"

# Build the Docker image
docker build -t andy2025/$image_name:$new_ver docker/$image_name

# Tag the image
docker tag andy2025/$image_name:$new_ver andy2025/$image_name:latest

# Push the new version and latest tag to DockerHub
docker push andy2025/$image_name:$new_ver
docker push andy2025/$image_name:latest