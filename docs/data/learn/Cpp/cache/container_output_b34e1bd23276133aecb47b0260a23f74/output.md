<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

If you're aware of the type traits library, you might be tempted to use `std::remove_cv<T>::type`. That won't actually remove the `const` / `volatile` off of a function. See [here](https://stackoverflow.com/a/38768590). The most you can do is build your own version of `std::remove_cv` for this usecase, as is done in the link. The full version of what's in the link is below.

```c++
template<typename T>
struct remove_cv_seq;

template<typename O, typename R, typename... Ps>
struct remove_cv_seq<R (O::*)(Ps...) const> {
    using type = R (O::*)(Ps...);
};

template<typename O, typename R, typename... Ps>
struct remove_cv_seq<R (O::*)(Ps...) volatile> {
    using type = R (O::*)(Ps...);
};

template<typename O, typename R, typename... Ps>
struct remove_cv_seq<R (O::*)(Ps...) const volatile> {
    using type = R (O::*)(Ps...);
};

template<typename O, typename R, typename... Ps>
struct remove_cv_seq<R (O::*)(Ps...)> {
    using type = R (O::*)(Ps...);
};
```

I think these are only required for functors and lambdas, not free functions. It doesn't make sense for a free function to be `const` or `volatile?
</div>

