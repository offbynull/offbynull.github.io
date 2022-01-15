<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

An alternate version of constant expression functions, called immediate functions, have the restriction that they must produce a compile-time constant. An immediate function requires prefixing `consteval` to a function instead of `constexpr`.

What's the point of this? According to [here](https://stackoverflow.com/a/53347377)...

> constexpr functions may be evaluated at compile time or run time, and need not produce a constant in all cases.

Here's an example from [here](https://github.com/AnthonyCalandra/modern-cpp-features)...

```c++
consteval int sqr(int n) {
  return n * n;
}

constexpr int r {sqr(100)}; // OK
int x {100};
int r2 {sqr(x)}; // ERROR: the value of 'x' is not usable in a constant expression
                 // OK if `sqr` were a `constexpr` function
```
</div>

