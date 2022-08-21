<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

This algorithm focuses on a different way of testing the first and last column of a BWT matrix for a substring. It specifically requires that the first and last columns of a BWT matrix were generated using the deserialization algorithm, because that algorithm has some special properties with how symbol instances get numbered (sorted / ordered).

Ultimately, it seems to be testing in a similar way as before but it doesn't try to test each potential substring instance by drilling down. Instead, it limits the span / range of options at each step to values that it knows are correct. In a way, it should be a faster way to test because of the memory layouts and principle of locality (e.g. subsequent memory access to a location that's closer to the original memory access is faster vs a location that's farther, due to caching and stuff like that).
</div>

