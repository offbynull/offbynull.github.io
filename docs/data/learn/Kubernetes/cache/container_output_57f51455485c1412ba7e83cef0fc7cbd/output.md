<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

You can distinguish a pod created by a replica set vs one created manually by checking the annotation key `kubernetes.io/create-by` on the pod.

If deleting a replica set, use `--cascade=false` in `kubectl` if you don't want the pods created by the replica set to get deleted as well.
</div>

