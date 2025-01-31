# only for test stage
set -e
set -o pipefail

cd k8s
kubectl apply -f user-service.yaml
kubectl apply -f product-service.yaml
kubectl apply -f order-service.yaml

kubectl get all
cd ..