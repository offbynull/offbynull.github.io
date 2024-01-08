<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

Auto-mounting an EFS volume may be done by updated `/etc/fstab` to include the line `filesystem-id:/ mount-target efs default,_netdev 0 0`. You can do this either manually or through a "cloud-init"  you use to initialize your EC2 instance on creation.
</div>

