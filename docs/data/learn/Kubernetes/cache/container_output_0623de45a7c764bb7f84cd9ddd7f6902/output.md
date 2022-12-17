<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

If you already know about services, the `NodePort` service isn't the same thing as what's going on here. This is opening up a port on the node that the pod is running on and forwarding requests to the container. `NodePort` opens the same port on *all* nodes and forwards requests to a random pod (not necessarily the pod running on the same node that the request came in to).
</div>

