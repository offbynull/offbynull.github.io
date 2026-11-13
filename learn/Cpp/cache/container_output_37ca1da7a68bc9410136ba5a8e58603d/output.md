<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

According to documentation online: "Compilers are not required to diagnose or do anything meaningful when undefined behaviour is present. Correct C++ programs are free of undefined behaviour". Not exactly sure how to fix some scenarios to be "free" of undefined behaviour. Specifically, there are a lot of cases where signed integer overflow (described below) happens, but that's undefined behaviour. I read online that the way to handle these cases is to test at the beginning of the function if overflow is possible and bail out if it is, but there's no built-in C++ mechanism to do that.

The statement and the examples below, were lifted from [here](https://en.cppreference.com/w/cpp/language/ub).
</div>

