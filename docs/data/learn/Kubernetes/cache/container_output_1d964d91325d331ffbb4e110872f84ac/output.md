<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

According to the k8s docs, it may be a parent-child relationship. Apparently looking for labels is just a initial step to permanently bringing pods under the control of a specific replica set:

> A ReplicaSet is linked to its Pods via the Pods' metadata.ownerReferences field, which specifies what resource the current object is owned by. All Pods acquired by a ReplicaSet have their owning ReplicaSet's identifying information within their ownerReferences field. It's through this link that the ReplicaSet knows of the state of the Pods it is maintaining and plans accordingly.

What happens when two replica sets try "owning" the same pod?
</div>

