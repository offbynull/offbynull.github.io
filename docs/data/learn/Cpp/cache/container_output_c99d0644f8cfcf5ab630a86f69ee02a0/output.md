<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

Concept_TEMPLATEs can be used to ensure that the underlying type of a universal reference is correct. In the example above, it's expected that the underlying type is `int`.

```c++
// VERSION 1: Accept only int, int &, or int &&
template<typename T>
  requires std::same_as<T, int> || std::same_as<T, int &> || std::same_as<T, int &&>
void test(T && x) {
    ...
}

// VERSION 2: Must be the same as int once you strip the reference and const/volatile off
template<typename T>
  requires std::is_same_v<std::remove_cv_t<std::remove_reference_t<T>>, int>
void test(T && x) {
    ...
}
```
</div>

