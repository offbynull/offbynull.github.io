<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

**WARNING**: Once `v` above gets destroyed (e.g. goes out of scope), `range` becomes invalid. `v` is _referenced_ by `range`, it isn't _copied_ / _moved_ into `range`. See the subsection on owning views to workaround this problem.
</div>

