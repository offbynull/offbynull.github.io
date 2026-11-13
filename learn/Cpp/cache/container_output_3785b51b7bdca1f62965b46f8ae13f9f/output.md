<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

Recall that, with concept_TEMPLATE function overloading, you can add a constrained function overload (overload using concrete types in the parameters) and the compiler will always default to that if there's ambiguity in which unconstrained function overload it should use. The same doesn't seem to apply with template specializations. I added the following template specialization and the compiler still complained about ambiguity when I did `multiply(3, 5)`:

```c++
template<>
int multiply<int>(int a, int b) {
    return a * b;
}
```
</div>

