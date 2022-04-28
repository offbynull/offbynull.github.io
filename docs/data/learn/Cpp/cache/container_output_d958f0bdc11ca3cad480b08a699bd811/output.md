<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

A quick-and-dirty way to determine what a type is deduced is to use `typeid()` in combination with querying type traits.

```c++
template<typename T>
void test(T p) {  // T or T& or const T or const T& or ...
    using P = decltype(p);
    using T_ref_removed = std::remove_reference<T>::type;
    using P_ref_removed = std::remove_reference<P>::type;
    using T_ref_and_cv_removed = std::remove_cv<T_ref_removed>::type;
    using P_ref_and_cv_removed = std::remove_cv<P_ref_removed>::type;
    // is_const/is_volatile must have ref removed for test to work: https://en.cppreference.com/w/cpp/types/is_const
    std::cout
        << "p: "
        << (std::is_const<P_ref_removed>::value ? "[const]" : "")
        << (std::is_volatile<P_ref_removed>::value ? "[volatile]" : "")
        << (std::is_lvalue_reference<P>::value ? "[&]" : "")
        << (std::is_rvalue_reference<P>::value ? "[&&]" : "")
        << typeid(P_ref_and_cv_removed).name()
        << "  /  "
        << "T:"
        << (std::is_const<T_ref_removed>::value ? "[const]" : "")
        << (std::is_volatile<T_ref_removed>::value ? "[volatile]" : "")
        << (std::is_lvalue_reference<T>::value ? "[&]" : "")
        << (std::is_rvalue_reference<T>::value ? "[&&]" : "")
        << typeid(T_ref_and_cv_removed).name()
        << std::endl;
}
```

`typeid()` by itself has a couple of issue:

 1. In certain cases, it won't output specifics of the type (see https://stackoverflow.com/q/37412265). I've tried to work around this by using type traits in the code above.
 
 2. The mains are mangled in G++ and clang (MSVC produces full type names). To de-mangle, you can use a command-line tool (that comes with most Linux g++/clang setups) called "c++-filt". For example, if `typeid().name()` outputs "PKi", ...

    ```
    user@localhost$ c++filt -t Pki
    int const*
    ```
</div>

