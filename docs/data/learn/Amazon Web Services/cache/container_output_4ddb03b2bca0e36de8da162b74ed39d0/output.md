<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

While not enforced, AWS recommends ...

* stopping an EC2 instance before taking a snapshot of the root EBS volume.
* unmounting a non-root volume before taking a snapshot of that volume.

This is probably recommended because of data consistency issues. For example, the operating system's file IO cache not have flushed to disk before taking the snapshot.
</div>

