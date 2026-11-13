<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

There is no macro `SIZE_C(...)` for `size_t`. Best to just assign a `size_t to one of the other types's literals and hope the compiler warns about any narrowing conversions that might happen.
</div>

