<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

This seems to mesh with how certain classes work. For example, to create a `std::vector<int>`, you can pass in an `std::initializer_list<int>` via its constructor to prime it with a set of values. That `std::initializer_list<int>` is typically created using the curly brace syntax.

```c++
std::vector<int> v ( {1, 2, 3, 4, 5} );
```

**However**, when you use `auto` as the return type of a function OR `auto` for parameters in a lambda, the curly-brace to `std::initializer<T>` conversion discussed below doesn't happen. The compiler will fail to deduce the type if you use supply a list in curly braces.
</div>

