<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

You may be wondering why the bullet point for *b* says "appeared twice" even though `last_tallies[5]['b'] = 3`. Remember that `last_tallies[5]` is giving the tallies up until index 5, not just *before* index 5. Since `last[5] = 'b'`, `last_tallies[5]['b']` needs to be subtracted by 1 to give the tallies just before reaching index 5.
</div>

