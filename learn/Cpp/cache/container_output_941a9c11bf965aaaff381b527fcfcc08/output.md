<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

Do these functions actually call into the `std::less<>()` to compare, or is it just using the less than operator (<) directly? cppreference doesn't seem to say?

For `std::stable_sort()`, it says it maintains the order of elements that are the same, but cppreference doesn't say how "sameness" is determined? Does it use equal operator (==), `std::equal_to()`, or is it doing `!(a < b) && !(b < a)`?

How are they moving values around? Are these using `std::swap()` or `std::move()` or assignment (=)?
</div>

