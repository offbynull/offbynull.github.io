<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

C++20 / C++23 has nothing in the standard library for this except for `std::span<T>`, and AFAIK type erasure isn't what it was intended for. You should use ranges-v3. Future versions of C++ might provide something.
</div>

