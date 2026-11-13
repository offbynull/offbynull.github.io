<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

The following adapts the `std::tuple` approach documented [here](https://stackoverflow.com/a/24948381) to work with functors as well as functions.

```c++
template<typename Fn>
struct func_types; // unimplemented

// template specialization for functors
template<typename O, typename R, typename... Ps>
struct func_types<R (O::*)(Ps...)> {
    using ret_t = R;
    using params_as_tuple_t = std::tuple<Ps...>;

    template<std::size_t N>
    using param_t = std::tuple_element<N, params_as_tuple_t>::type;

    static constexpr std::size_t param_cnt { std::tuple_size<params_as_tuple_t>{} };
};



// manipulators to remove cv-type off functor's function call operator
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





struct my_functor {
    int operator() (long lval, short sval) const volatile {
        return 5;
    }
};

int main() {
    using functor_call_op_t = decltype(&my_functor::operator());
    using functor_call_op_t_without_cv = remove_cv_seq<functor_call_op_t>::type;
    using types = func_types<functor_call_op_t_without_cv>;
    std::cout << (std::is_same<types::ret_t, int>::value ? "true" : "false") << std::endl;         // prints "true"
    std::cout << (std::is_same<types::param_t<0u>, long>::value ? "true" : "false") << std::endl;  // prints "true"
    std::cout << (std::is_same<types::param_t<1u>, short>::value ? "true" : "false") << std::endl; // prints "true"
    std::cout << types::param_cnt;
    return 0;
}
```
</div>

