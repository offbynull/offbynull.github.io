<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

`std::visit()` can take in multiple `std::variant` objects. The callable unit passed in needs to have overloads for the cartesian product of the variant types (param at index n covers the types of the variant at index n). For example, calling `std::visit()` with `std::variant<int, float>` amd `std::variant<char, long>` requires that the callable unit have overloads for (int, char), (int, long), (float, char), and (float, long).

See [here](https://www.cppstories.com/2018/09/visit-variants/) and [here](https://dev.to/tmr232/that-overloaded-trick-overloading-lambdas-in-c17).
</div>

