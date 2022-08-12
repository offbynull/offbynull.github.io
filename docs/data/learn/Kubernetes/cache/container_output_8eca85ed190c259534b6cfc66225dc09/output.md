<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

These are also typically created via command-line: `kubectl create configmap my-config --from-file=my-config.ini=myconfig.init --from-literal=param1=another-value --from-literal=param2=extra-value`

The option `--from-file` can also point to a directory, in which case an entry will get created for each file in the directory provided that the filenames don't have any disalowed characters.
</div>

