<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

Be careful when making use of concept_TEMPLATEs like this. When `const auto` is involved, it'll break compilation. 

```c++
std::integral const auto f() {
    return 0;
}
```

The above function won't compile because there's something before the `const`. When a `const` is the left-most thing, it can't have anything further left of it. You need to move the `const` after `auto` (`const auto` is the exact same as `auto const`, having `const` as left-most thing is just a syntactical convenience thing).

```c++
std::integral auto const f() {
    return 0;
}
```
</div>

