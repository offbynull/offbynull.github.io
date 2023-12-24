<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

To determine how effectively you're using EBS volumes, you can use CloudWatch. Specifically, ...

* `EBSIOBalance%` shows number of credits remaining for EBS volumes
* `EBSByteBalance%` shows amount of throughput left for EBS volumes

Higher numbers mean better performance: If it's ...

* consistently high, you should downgrade
* consistently low, you should upgrade
</div>

