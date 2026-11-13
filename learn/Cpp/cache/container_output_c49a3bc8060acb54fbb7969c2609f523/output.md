<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

The book mentions that, before `decltype(auto)`, you needed to use the trailing return type syntax to get similar behaviour when the return type depended on the parameter types.

```c++
template<typename T>
auto f1(T x) -> decltype(x + 5) {
    return x + 5;
}
```

You can't do something similar with the original return type syntax because the compiler doesn't know what's in the parameter list -- it hasn't parsed that part yet.

```c++
template<typename T>
decltype(x + 5) f1(T x) { // THIS WON'T WORK: x used in decltype() before it's encountered in parameter list
    return x + 5;
}
```
</div>

