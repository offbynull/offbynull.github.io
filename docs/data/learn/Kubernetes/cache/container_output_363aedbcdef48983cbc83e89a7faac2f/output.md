<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

Persistent volumes themselves aren't are cluster-level resources while persistent volume claims are namespace-level resources. All volumes are available for claims regardless of the namespace that claim is in. Maybe you can limit which volumes can be claimed by using labels / label selectors?
</div>

