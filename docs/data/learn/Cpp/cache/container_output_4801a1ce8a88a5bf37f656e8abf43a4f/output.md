<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

There's also `std::partial_sum()`, which is like `std::inclusive_scan()` but guarantees the operation goes from left-to-right (left-fold). The scan functions don't guarantee which elements get operated on first, meaning multiple runs of o the same scan function with the same inputs may return different result if the type isn't commutative.
</div>

