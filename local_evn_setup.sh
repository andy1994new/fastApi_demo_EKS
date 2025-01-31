#!/bin/bash

set -e

echo "🔹 Installing required tools using Homebrew..."

brew install terraform awscli kubectl eksctl

echo "✅ Terraform version: $(terraform -v)"
echo "✅ AWS CLI version: $(aws --version)"
echo "✅ kubectl version: $(kubectl version --client --output=yaml | grep gitVersion)"
echo "✅ eksctl version: $(eksctl version)"

echo "🔹 Configuring AWS credentials"
aws configure