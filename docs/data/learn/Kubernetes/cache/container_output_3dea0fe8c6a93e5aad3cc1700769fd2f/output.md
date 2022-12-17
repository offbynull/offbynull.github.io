<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

What exactly is the `system:authenticated` group in the examples above? According to the book, there are several groups internal to Kubernetes that help identify an account:

 * `system:unauthenticated` - Group assigned when authentication failed.
 * `system:authenticated` - Group assigned when authentication succeeded.
 * `system:serviceaccounts` - Group assigned to service accounts.
 * `system:serviceaccounts:<NAMESPACE>` - Group assigned to service accounts under a specific namespace.
</div>

