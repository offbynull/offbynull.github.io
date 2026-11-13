<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

This warning is from the book, and seems important:

> When you change the size of the underlying contiguous range, the contiguous range may be reallocated, and the std::span refers to stale data. Only a std::span with dynamic extent can have a resizable underlying contiguous range and can, therefore, be a victim of this subtle issue.

I think what this is saying is that, a `std::span` may be holding on to the actual pointer to the data of the contiguous range, not the contiguous range object itself. A contiguous range has `data()` function that gives you a pointer to the data and if that's what the `std::span` implementation is using, that pointer and the data within it changes on modification. That's why you may end up with a `std::span` that points to stale data?

A resizable contiguous range (e.g. `std::vector`) requires a dynamic extent `std::span`, but that dynamic extent `std::span` won't update if that contiguous range resizes / reallocates its data to another piece of contiguous memory.
</div>

