<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

It turns out that, if you pass in an invalid `{bm-skip} specifier` for whatever type it is you're trying to parse to, it doesn't barf by default. It may be that you need to check `fail()` or you need to explicitly tell the stream to throw an exception via `exceptions()`? For example, parsing `"Aug 2021"` using `"%b %Y"` into `std::chrono::year` doesn't work because `std::chrono::year` can only contain a year.
</div>

