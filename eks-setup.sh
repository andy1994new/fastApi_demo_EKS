set -e
set -o pipefail

cd tf

echo "Initializing Terraform..."
terraform init

echo "Creating VPC and networking resources..."
terraform apply -target=module.vpc -auto-approve

echo "Creating EKS cluster..."
terraform apply -target=module.eks -auto-approve

echo "Creating remaining resources..."
terraform apply -auto-approve

echo "Deployment completed successfully!"