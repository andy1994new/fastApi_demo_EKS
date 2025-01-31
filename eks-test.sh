# only for test stage
set -e
set -o pipefail

cd k8s
echo "setting up kubectl"
aws eks --region eu-west-1 update-kubeconfig --name fastapi
kubectl get all
echo "applying nginx.yaml"
kubectl apply -f nginx.yaml
kubectl get pod
kubectl get svc
cd ..