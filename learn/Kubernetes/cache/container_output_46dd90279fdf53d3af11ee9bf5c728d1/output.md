<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

According to the book, it's difficult to tell if / why a hook failed. Its output doesn't go anywhere. You'll just see something like `FailedPostStartHook` / `FailedPreStopHook` somewhere in the pod's event log.

According to the book, many applications use pre-stop hook to manually send a `SIGTERM` to their app because, even though `SIGTERM` is being sent by Kubernetes, it's getting gobbled up and discarded by some parent process (e.g. running your app via `sh`).
</div>

