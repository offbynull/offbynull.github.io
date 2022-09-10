<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

Do these functions actually call into the `std::less<>()` to compare, or is it just using the less than operator (<) directly? cppreference doesn't seem to say?

How are they moving values around? Are these using `std::swap()` or `std::move()` or assignment (=)?
</div>

