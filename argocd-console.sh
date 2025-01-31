kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 --decode; echo
kubectl port-forward svc/argocd-server -n argocd 8080:443
# console url: http://localhost:8080
# user name: admin
# password: see the output