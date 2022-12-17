<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

Recall that it's also possible to disable auto-mounting on individual pods. Auto-mounting can't be disabled on individual containers, but it is possible to override the `/var/run/secrets/kubernetes.io/serviceaccount` mount on those containers with something like tmpfs (empty directory).
</div>

