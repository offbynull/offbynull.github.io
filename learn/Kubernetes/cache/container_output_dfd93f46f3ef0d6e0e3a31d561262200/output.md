<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

A service decides which pods it routes to based key-value pairs in on `spec.selector`. What happens if the key-value pairs identify a set of pod instances where some of those instances don't have a port named `my-http-port`. For example, a service may be forwarding to two applications rather than a single application which just could be sharing the same set of key-value labels (pod instances are heterogenous).

Maybe this isn't possible with Kubernetes?
</div>

