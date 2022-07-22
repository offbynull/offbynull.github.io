<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

Why must `spec.storageClassName` be an empty string instead of being removed entirely? Being removed entirely would cause Kubernetes to use a default storage class name (if one exists), which is not what you want. Storage classes are described in the next few paragraphs below.
</div>

