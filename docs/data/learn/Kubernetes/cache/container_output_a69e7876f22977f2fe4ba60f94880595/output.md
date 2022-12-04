<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

You can inspect previous versions via `kubectl rollout history deployment my-deployment`. For each update, it's good practice to set the `kubernetes.io/change-cause` annotation a custom message describing what was updated / why it was updated -- this shows up in the history.

You can a rollback via `kubectl rollout undo deployments my-deployment --to-revision=12345`.
</div>

