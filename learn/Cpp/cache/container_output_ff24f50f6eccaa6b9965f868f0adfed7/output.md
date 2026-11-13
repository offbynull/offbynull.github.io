<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

If you know what the `auto` keyword does:

For default implementations, sometimes people set the return type as `auto`. This is because the default implementation's ordering type is only going to be as "weak" as its weakest parent class / member variable, and you don't know the weakness of everything beforehand.

So for example, if your class has a bunch of member variables with `std::strong_ordering` and a single float member variable (`std::partial_ordering`), the return type of the spaceship operator will be `std::partial_ordering`.
</div>

