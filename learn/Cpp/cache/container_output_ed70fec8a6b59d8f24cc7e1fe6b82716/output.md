<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

Another option is to go ahead and use pointers, but rather than specifying `std::hash<K>` / `std::equal_to<K>` / `std::less_than<K>` in the template parameters, create custom functor that access data on the object being pointed to.

```c++
struct custom_less_functo {
    constexpr bool operator()(const MyObject* & lhs, const MyObject* & rhs) const {
        return lhs->val1 < rhs->val1 || lhs->val2 < rhs->val2;
    }
}
std::ordered_set<MyObject*, custom_less_functor_for> s { ... }
```
</div>

