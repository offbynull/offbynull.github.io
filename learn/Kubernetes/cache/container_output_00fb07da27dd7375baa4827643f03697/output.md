<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

Since these persistent volumes are being dynamically provisioned, it doesn't make sense to have `Recycle`. You can just `Delete` and if a new claim comes in it'll automatically provision a new volume. It's essentially the same thing as `Recycle`.
</div>

