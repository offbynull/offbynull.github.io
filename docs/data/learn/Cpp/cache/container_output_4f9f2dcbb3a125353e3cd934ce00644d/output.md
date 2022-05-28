<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

Unlike Java streams, the current implementation of ranges (C++20) are missing some major functionality:

* type-erasures (e.g. `std::vector<int> {0, 1, 2} | std::views::transform([](int x) { return x * 2; })` and `std::vector<int> {0, 1, 2} | std::views::filter([](int x) { return x != 0; })` don't have the same type)
* parallel algorithms (e.g. transform using multiple cores)
* actions (e.g. missing things like `forEach()` in Java streams)
</div>

