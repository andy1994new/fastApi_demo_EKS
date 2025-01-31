# FastAPI Microservices on AWS EKS

## Overview
This project demonstrates microservices communication using FastAPI. It consists of three services that are built into Docker images and deployed to AWS EKS automatically. The infrastructure, including the EKS cluster and all required components, is provisioned using Terraform.

## Features
- **Microservices Architecture**: Three FastAPI services communicate with each other.
- **Fully Automated Deployment**: 
  - Infrastructure as Code (IaC) using Terraform.
  - Continuous Integration (CI) with GitHub Actions.
  - Continuous Deployment (CD) using ArgoCD.
- **CI/CD Pipeline**:
  - Runs automated tests.
  - Builds Docker images and pushes them to Docker Hub.
  - Updates Kubernetes manifests, triggering ArgoCD to deploy new versions.
- **Kubernetes Components**:
  - Autoscaler for dynamic scaling.
  - AWS Load Balancer Controller for managing external traffic.
  - ArgoCD for GitOps-based deployment management.

## Prerequisites
Before starting, ensure you have:
1. An **AWS account** with an **Access Key ID** and **Secret Access Key**.
2. **Docker Hub** account for storing built images.
3. **GitHub repository** for storing the project and triggering CI/CD workflows.
4. **VS Code** (or another IDE) with necessary extensions.

## Setup & Deployment
### 1️⃣ Clone the Repository and Create a GitHub Repository
1. Create a new **GitHub repository** for your project.
2. Clone the repository locally:
   ```sh
   git clone https://github.com/andy1994new/fastApi_demo_EKS.git
   cd fastApi_demo_EKS
   ```
3. Add the following **GitHub Action secrets** under **Settings → Secrets and variables → Actions**:
   - `DOCKERHUB_USERNAME` → Your Docker Hub username
   - `DOCKERHUB_TOKEN` → Your Docker Hub token
   - `GH_TOKEN` → Your GitHub token
4. Push your code to this repository.

### 2️⃣ Create a GitHub Repository for ArgoCD
1. Create a new repository on GitHub named `argo`.
2. Push all files under `/k8s` to this repository:
   ```sh
   cd k8s
   git init
   git remote add origin https://github.com/your-username/argo.git
   git add .
   git commit -m "Initial commit for ArgoCD manifests"
   git push -u origin main
   cd ..
   ```

### 3️⃣ Modify Configuration Files
Before deploying, update the following files:
- **terraform/argoApp.yaml**: Update `repoURL:` to point to your ArgoCD GitHub repository.
- **terraform/local.tf**: Update any AWS-related configurations as needed.
- **update.sh**: Replace with your Docker Hub username.

After making these changes, push the modified code to your repository. GitHub Actions will automatically:
- Run tests.
- Build new Docker images and push them to Docker Hub.
- Update the Kubernetes YAML files in the ArgoCD repository.

### 4️⃣ Run Local Setup
```sh
make local_setup
```
> **Note:** Homebrew is required for macOS. Modify the script if you are using Windows.

This will configure your local environment and AWS credentials.

### 5️⃣ Run AWS Setup
```sh
make AWS_setup
```
This initializes the AWS infrastructure, including the EKS cluster, ArgoCD, and other dependencies. The services will be automatically deployed on the EKS cluster.

To check the status of the services:
```sh
kubectl get svc
```
After a few minutes, once the **Load Balancer** is activated, use tools like **Postman** to test the services using the obtained URLs.

### 6️⃣ Access the ArgoCD Console
Run the script to open the ArgoCD console:
```sh
sh argocd-console.sh
```
From here, you can monitor the deployment status of your three services.

## CI/CD Workflow
### GitHub Actions (CI)
1. **Runs Tests** → Ensures the FastAPI services work correctly.
2. **Builds Docker Images** → Pushes to Docker Hub.
3. **Updates Kubernetes YAML** → Triggers ArgoCD to deploy the new version.

### ArgoCD (CD)
- Monitors changes in the Kubernetes manifests.
- Automatically applies updates to the EKS cluster.

## Monitoring & Scaling
- **Horizontal Pod Autoscaler (HPA)** ensures services scale based on demand.
- **AWS Load Balancer Controller** manages incoming traffic.

## Cleanup
To delete all resources created by Terraform:
```sh
cd terraform
terraform destroy -auto-approve
```

## Conclusion
This project automates the deployment of FastAPI microservices on AWS EKS, integrating Terraform, GitHub Actions, and ArgoCD for a complete CI/CD pipeline. 🚀

