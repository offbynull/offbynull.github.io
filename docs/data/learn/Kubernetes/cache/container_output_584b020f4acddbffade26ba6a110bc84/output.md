<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

Looking at the k8s code, it looks like for a service port needs to be named for it as an environment variable. Service ports that don't have a name won't show up as environment variables. See [here](https://github.com/kubernetes/kubernetes/blob/master/pkg/kubelet/envvars/envvars.go#L51-L55).
</div>

