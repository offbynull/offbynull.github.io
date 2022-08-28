<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

To keep things efficient-ish, the code below actually splits out `last_tallies` into it a dictionary of index to tallies. Otherwise, you end up with a bunch of `None` entries under `last_tallies` and that actually ends up taking space.

You could also make it a list where each index maps to a multiple of the original index (e.g. 0 maps to 0*3, 1 maps to 1*3, 2 maps to 2*3, ...).
</div>

