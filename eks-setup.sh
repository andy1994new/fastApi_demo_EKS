set -e
set -o pipefail

cd terraform

echo "Initializing Terraform..."
terraform init

echo "Creating EKS cluster..."
terraform apply -target=module.eks -auto-approve

echo "Creating remaining resources..."
terraform apply -auto-approve

echo "Deployment completed successfully!"

cd ..