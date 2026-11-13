<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

The book mentions that, if you're going to use `decltype(auto)`, don't wrap the expression in brackets. The reason is that `decltype()`, for whatever reason, will end up interpreting it different than what it is.

```c++ 
// Example from the book
decltype(auto) f1() {
  int x = 0;
  return x;        // decltype(x) is int, so f1 returns int
}

decltype(auto) f2() {
  int x = 0;
  return (x);      // decltype((x)) is int&, so f2 returns int&
}
```
</div>

