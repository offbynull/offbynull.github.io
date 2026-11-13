<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

Not using `std::forward<T>()` will force the argument to get moved forward as a lvalue reference. You must use `std::forward<T>()` to maintain the type of reference.
</div>

