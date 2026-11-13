<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

In most cases, you shouldn't have to write out templates like `is_same<>` yourself. The C++ standard library provides the `type_traits` header library which contains `std::is_same<>` and several other type checks. The C++ standard library also provides a set of pre-built concept_TEMPLATEs that make use of check that a type has specific type traits. For example, `std::is_same<>` is exposed as the concept_TEMPLATE `std::same_as<>`.

Likewise, the C++ standard library provides a more elaborate version of `integral_check<>` as `std::integral<>`.
</div>

