<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

What's the point of the above? You don't know what internal integer type each standardized type maps to. For example, `uint64_t` may map to `unsigned long long`, which means when you want to assign a literal to a variable of that type you need to add a `ULL` suffix...

`uint64_t test = 9999999999999999999ULL`

The macros above make it so that you don't need to know the underlying mapping...

`uint64_t test = UINT64_C(9999999999999999999)`
</div>

