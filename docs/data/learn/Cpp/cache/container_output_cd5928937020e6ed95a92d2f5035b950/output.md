<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

The C++ standard library separates the idea of equality and equivalence by assuming the equality operator (==) only tests for equality.

* Equality: `a == b`
* Equivalence: `!(a < b) && !(b < a)` (or `!(a > b) && !(b > a)`, or some other relation that doesn't use `==`)

See [here](https://en.cppreference.com/w/cpp/named_req/EqualityComparable).
</div>

