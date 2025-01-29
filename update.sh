#!/bin/bash

set -e

new_ver=$1  # First argument: new version
service_name=$2  # Second argument: service name (e.g., user, order, product)

# Convert service_name to match Docker image naming convention (underscore)
image_name="${service_name}_service"

# Convert service_name to match YAML file naming convention (dash)
yaml_name="${service_name}-service.yaml"

# echo "Building and pushing $image_name with version: $new_ver"

# # Build the Docker image
# docker build -t andy2025/$image_name:$new_ver docker/$image_name

# # Tag the image
# docker tag andy2025/$image_name:$new_ver andy2025/$image_name:latest

# # Push the new version and latest tag to DockerHub
# docker push andy2025/$image_name:$new_ver
# docker push andy2025/$image_name:latest

# Create a temporary folder
tmp_dir=$(mktemp -d)
echo "Temporary directory: $tmp_dir"

# Clone GitHub repo
git clone https://github.com/andy1994new/argo.git $tmp_dir

# Print before and after sed for debugging
echo "Before sed:"
cat $tmp_dir/$yaml_name

# Update image tag in deployment YAML
sed -i -e "s|andy2025/$image_name:.*|andy2025/$image_name:$new_ver|g" $tmp_dir/$yaml_name

# Navigate to repo
cd $tmp_dir

echo "befor indentity:"
git status

# Set Git user identity for CI/CD (Fixes "Author identity unknown" error)
git config --global user.email "ci-bot@example.com"
git config --global user.name "CI Bot"

echo "after indentity:"
git status

# Commit and push changes if there are any
git add .
if git diff --quiet; then
    echo "No changes to commit."
else
    git commit -m "Update $service_name-service image to $new_ver"
    git push
fi

# Cleanup
rm -rf $tmp_dir

echo "Successfully updated $service_name-service to version $new_ver"
