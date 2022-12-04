<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

It doesn't look like it's possible to prevent these authentication details from being mounted to a single container within a pod, but it is possible to override it by mounting something else to `/var/run/secrets/kubernetes.io/serviceaccount` (e.g. maybe a tmp file system).
</div>

