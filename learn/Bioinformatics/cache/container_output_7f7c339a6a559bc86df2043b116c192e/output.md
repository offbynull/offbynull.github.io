<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

The algorithm above is serial, but it can be made parallel to get even more speed:

 1. Parallelized prefix sum (e.g. Hillis-Steele / Blelloch).
 2. Parallelized iteration instead of nested for-loops.
 3. Parallelized sorting (e.g. Parallel merge sort / Parallel brick sort / Bitonic sort).
</div>

