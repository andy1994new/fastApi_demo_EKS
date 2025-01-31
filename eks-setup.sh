#!/bin/bash

set -e
set -o pipefail

echo "🔹 Switching to Terraform directory..."
cd terraform

echo "🔹 Initializing Terraform..."
terraform init

echo "🔹 Validating Terraform configuration..."
terraform validate

echo "🚀 Creating EKS cluster..."
terraform apply -target=module.eks -auto-approve

echo "🚀 Deploying remaining infrastructure..."
terraform apply -auto-approve

echo "✅ Deployment completed successfully!"

echo "🔹 Applying ArgoCD application configuration..."
kubectl apply -f ../argoApp.yaml

echo "🎉 Setup complete!"
