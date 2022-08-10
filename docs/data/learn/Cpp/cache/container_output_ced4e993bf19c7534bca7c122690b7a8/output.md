<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

Technically, `std::is_constant_evaluated()` can be used anywhere. If you use it ...

 * in a `consteval`, it will always evaluate to true
 * in a `constexpr`, it may evaluate to true or false depending on where it was called
 * in a normal run-time evaluated function, it will always evaluate to false
</div>

