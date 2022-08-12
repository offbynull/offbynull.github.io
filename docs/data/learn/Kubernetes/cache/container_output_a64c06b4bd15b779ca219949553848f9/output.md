<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

The DNS server runs as an internal Kubernetes application called 'coredns` or `kube-dns`. This is usually in the `kube-system` namespace. Recall that the IP of a service is stable for the entire lifetime of the service, meaning that service restarts and DNS caching by the application and / or OS isn't an issue here.
</div>

