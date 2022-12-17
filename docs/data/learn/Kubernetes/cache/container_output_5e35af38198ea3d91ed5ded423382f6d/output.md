<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

According to the book, most if not all implementations of ingress simply query the service for its endpoints and directly load balance across them vs forwarding the request through that service. Note that the port in the example above is still the port that the *service* is listening on, not the port of the pod is listening on.
</div>

