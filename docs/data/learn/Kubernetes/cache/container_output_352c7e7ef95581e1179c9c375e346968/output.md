<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

For individual files/directories mounted from a volume, one workaround to receiving updates is to use symlinks. Essentially, mount the whole volume to a path that doesn't conflict with an existing path in the container. Then, as a part of the container's start-up process, add symlinks to the whole volume mount wherever needed.

For example, if the application requires a configuration file at /etc/my_config.conf, you can mount all configurations to /config and then symlink /etc/my_config.conf to /config/my_config.conf. That way, you can still receive updates.
</div>

