<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

There's a much simpler way to do all of this if you're already familiar with `std::tuple` from the C++ standard library, documented [here](https://stackoverflow.com/a/24948381). Basically, wrap the parameter types within a `std::tuple`'s type, and then use `std::tuple`'s type access functions to pull out individual types within that tuple type / number of types nested in that tuple type.

```c++
template<typename Fn>
struct func_types; // unimplemented

template<typename R, typename... Ps>
struct func_types<R(Ps...)> {
    using ret_t = R;
    using params_as_tuple_t = std::tuple<Ps...>;

    template<std::size_t N>
    using param_t = std::tuple_element<N, params_as_tuple_t>::type;

    static const constexpr std::size_t param_cnt { std::tuple_size<params_as_tuple_t>{} };
};




int my_func(long lval, short sval) {
    return 5;
}

int main() {
    using types = func_types<decltype(my_func)>;
    std::cout << (std::is_same<types::ret_t, int>::value ? "true" : "false") << std::endl;         // prints "true"
    std::cout << (std::is_same<types::param_t<0u>, long>::value ? "true" : "false") << std::endl;  // prints "true"
    std::cout << (std::is_same<types::param_t<1u>, short>::value ? "true" : "false") << std::endl; // prints "true"
    std::cout << types::param_cnt;
    return 0;
}
```

There's also [Boost's type traits library](https://www.boost.org/doc/libs/1_79_0/libs/type_traits/doc/html/boost_typetraits/reference/function_traits.html), which provides a simple `function_traits<>` template that pulls out all the types and other type related information within a function: `function_traits<my_func>::result_type`, `function_traits<my_func>::argN_type`, `function_traits<my_func>::arity`, etc...
</div>

