<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

Why not just use a lambda instead of `std::bind()` / `std::bind_front()`? Probably because this is more terse. With a lambda, you likely will need `auto &&` for each parameter, `decltype(auto)` for the return, and `std::forward`s for each argument being pushed into the original function-like object.
</div>

