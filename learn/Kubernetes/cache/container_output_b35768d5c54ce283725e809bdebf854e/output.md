<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

What about shrinking a volume? I imagine what you need to do is, starting with the last ordinal to the first (current pod denoted N), ...

1. delete stateful set without deleting its pods (`kubectl delete sts --cascade=orphan <name>`).
1. delete pod N.
1. create a temporary volume with the new desired size.
1. create a temporary pod with both the pod N's volume and the temporary volume attached.
1. use the temporary pod to copy pod N's volume to the temporary volume.
1. delete the temporary pod.
1. delete pod N's volume.
1. re-create pod N's volume with the new desired size (same name).
1. create a temporary pod with both the pod N's volume and the temporary volume attached.
1. use the temporary pod to copy the temporary volume to pod N's volume.
1. re-create the stateful set (`kubectl apply -f <name>`).
1. trigger the stateful set to restart pods one at a time (`kubectl rollout restart sts <name>`).

The last step should restart the deleted pod, and that deleted pod will attach the updated volume.

These same steps may work for expanding volumes when `allowVolumeExpansion` isn't set to `true`.
</div>

