<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

I think (not sure) if you create a `std::hash<T>` implementation for the element type, the `std::unordered_set` should automatically pick it without having to specify the template parameter + directly passing it in as an argument (as done above). It should work so long as the implementation is visible (e.g. whatever file its in has been `#include`-ed) when the container is created.
</div>

