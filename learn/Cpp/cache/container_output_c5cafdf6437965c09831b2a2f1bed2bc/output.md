<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

There's a special function in the C++ standard library called `std::is_constant_evaluated()` that you can use in a `constexpr` function to determine if / ensure that the code is being executed at compile-time or at run-time. This is useful if you want the code to do something different when evaluated at compile-time vs run-time (e.g. use a look-up table if evaluated at run-time vs do the full calculation if evaluated at compile-time).

Here's the example from the book...

```c++
constexpr double power(double b, int x) {
    if (std::is_constant_evaluated() && !(b == 0.0 && x < 0)) {       
        if (x == 0)
            return 1.0;
        double r = 1.0, p = x > 0 ? b : 1.0 / b;
        auto u = unsigned(x > 0 ? x : -x);
        while (u != 0) {
            if (u & 1) r *= p;
            u /= 2;
            p *= p;
        }
        return r;
    } else {
        return std::pow(b, double(x));
    }
}
```

Technically, `std::is_constant_evaluated()` can be used anywhere. If you use it ...

 * in a `consteval`, it will always evaluate to true
 * in a `constexpr`, it may evaluate to true or false depending on where it was called
 * in a normal run-time evaluated function, it will always evaluate to false
</div>

