<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

The same gotchas with replica sets also apply to deployments: all pods will use the same persistent volume claim and IPs / hosts aren't retained when pods are replaced.

Like with replica set, you might have to use `--cascade=false` in `kubectl` if you don't want the pods created by the deployment to get deleted as well (unsure about this).
</div>

