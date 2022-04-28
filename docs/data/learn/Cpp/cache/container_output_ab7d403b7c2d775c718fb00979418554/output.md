<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

The book mentions that, if you're going to use `decltype()`, don't wrap the expression in brackets. The reason is that `decltype()`, for whatever reason, will end up interpreting it different than what it is.

```c++
int x { 5 };

decltype(x)    // will be an int
decltype((x))  // will be an int &
```
</div>

