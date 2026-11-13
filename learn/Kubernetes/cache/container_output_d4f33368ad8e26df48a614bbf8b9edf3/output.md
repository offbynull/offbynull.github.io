<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

Part of the reasoning for doing it like this is decoupling: volumes are independent from pods and a volume can be shared access across pods.

Another reason is that a developer should only be responsible for claiming a volume while the cluster administrator should be responsible for setting up those volumes and dealing with backend details like the specifics of the volume type and how large each volume is. As a developer, you only have to make a "claim" while the administrator is responsible for ensuring those resources exist.
</div>

