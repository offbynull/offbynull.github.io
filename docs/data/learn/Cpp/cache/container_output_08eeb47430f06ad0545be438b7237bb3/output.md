<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

There's also `std::accumulate()`, which is like `std::reduce()` but guarantees the operation goes from left-to-right (left-fold). `std::reduce()` doesn't guarantee which elements get operated on first, meaning multiple runs of `std::reduce()` with the same inputs may return different result if the type isn't commutative.
</div>

