<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

For retain specifically, once the existing persistent volume claim is released, the persistent volume itself goes into "Released" status. If it were available for reclamation, it would go into "Available" status. The book mentions that there is no way to "recycle" a persistent volume that's in "Released" status without destroying and recreating it.

According to the k8s docs, this is the way it is so that users have a chance to manually pull out data considered precious before it gets destroyed.
</div>

