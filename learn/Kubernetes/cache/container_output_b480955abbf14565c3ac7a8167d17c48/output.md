<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

The manifest is using label selectors are being used to identify pods. How does it know what the replica count is for the replica set / deployment / or stateful set? According to the docs:

> The "intended" number of pods is computed from the spec.replicas of the workload resource that is managing those pods. The control plane discovers the owning workload resource by examining the metadata.ownerReferences of the Pod.
</div>

