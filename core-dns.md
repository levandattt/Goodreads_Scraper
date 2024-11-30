export KUBE_EDITOR="nano"
kubectl -n kube-system edit configmap coredns
forward . 8.8.8.8 8.8.4.4
kubectl -n kube-system rollout restart deployment coredns