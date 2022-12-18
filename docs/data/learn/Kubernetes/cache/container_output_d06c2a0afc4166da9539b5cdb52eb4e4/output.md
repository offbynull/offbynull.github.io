<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

Note that `requiredDuringSchedulingIgnoredDuringExecution` and `preferredDuringSchedulingIgnoredDuringExecution` both end with "ignored during execution". This basically says that a pod won't get scheduled on a node but it also won't get evicted if that pod is already running on that node. This is in contrast to node taints, where a taint having an effect of `NoExecute` will force evictions of running pods.

The book hints that the ability to evict running pods may be added sometime in the future.
</div>

