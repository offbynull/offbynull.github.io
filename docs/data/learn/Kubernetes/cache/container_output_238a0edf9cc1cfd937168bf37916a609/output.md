<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

By default, network access is allowed to all pods within the cluster. You can change this using a special kind of pod called `NetworkPolicy` (as long as your Kubernetes environment supports it -- may or may not depending on the container networking interface used). `NetworkPolicy` lets you limit network access such that only pods that should talk togetehr can talk together (a pod can't send a request to another random pod in the system). This is done via label selectors.

If you're aware of endpoints, service, and ingress kinds, I'm not sure how this network policy stuff plays with those kinds.
</div>

