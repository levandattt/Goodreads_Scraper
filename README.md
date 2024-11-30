ERROR: Could not build wheels for psycopg2, which is required to install pyproject.toml-based projects
sudo apt-get install libpq-dev python3-dev


kubectl run curl-pod --image=radial/busyboxplus:curl -it --rm --restart=Never -- /bin/sh
kubectl run dns-test-pod --image=busybox:1.35 -it --rm --restart=Never -- sh

kubectl run debug-pod --image=busybox --restart=Never -- sleep 3600
kubectl -n kube-system edit configmap coredns
kubectl -n kube-system rollout restart deployment coredns
