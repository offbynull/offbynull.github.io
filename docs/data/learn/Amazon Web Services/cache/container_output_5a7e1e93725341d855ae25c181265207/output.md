<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

Recall that when there are multiple policies for the same resource and action (e.g. an IAM user could be both in IAM group A and IAM group B, both of which have a policy for reading an S3 bucket), denials always take precedence.

`NotResource` and `NotAction` are commonly used with `Deny`.
</div>

