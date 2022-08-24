<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

The following adapts the `std::tuple` approach documented [here](https://stackoverflow.com/a/24948381) to work with functors as well as functions.

```c++
// manipulators to remove cv-type off functor's function call operator AND free functions
//  don't know if any of this is even valid for free functions
template<typename T>
struct remove_cv_seq;

template<typename R, typename... Ps>
struct remove_cv_seq<R (Ps...) const> {
    using type = R (Ps...);
};

template<typename R, typename... Ps>
struct remove_cv_seq<R (Ps...) volatile> {
    using type = R (Ps...);
};

template<typename R, typename... Ps>
struct remove_cv_seq<R (Ps...) const volatile> {
    using type = R (Ps...);
};

template<typename R, typename... Ps>
struct remove_cv_seq<R (Ps...)> {
    using type = R (Ps...);
};

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




// function type breakers
//
template<typename Fn>
struct func_types; // unimplemented

// template specialization for functions
template<typename R, typename... Ps>
struct func_types<R(Ps...)> {
    using ret_t = R;
    using params_as_tuple_t = std::tuple<Ps...>;

    template<std::size_t N>
    using param_t = std::tuple_element<N, params_as_tuple_t>::type;

    static constexpr std::size_t param_cnt { std::tuple_size<params_as_tuple_t>{} };
};

// template specialization for functors
template<typename O, typename R, typename... Ps>
struct func_types<R (O::*)(Ps...)> {
    using ret_t = R;
    using params_as_tuple_t = std::tuple<Ps...>;

    template<std::size_t N>
    using param_t = std::tuple_element<N, params_as_tuple_t>::type;

    static constexpr std::size_t param_cnt { std::tuple_size<params_as_tuple_t>{} };
};

// unify template specializations
template<typename T>
struct unified_func_types {
private:
    static auto _fake() {
        if constexpr (!std::is_function<T>::value) {
            using functor_call_op_t = decltype(&T::operator());
            using functor_call_op_t_without_cv = remove_cv_seq<functor_call_op_t>::type;
            return func_types<functor_call_op_t_without_cv> {};
        } else {
            using function_without_cv = remove_cv_seq<T>::type;
            return func_types<function_without_cv> {};
        }
    }
public:
    using types = decltype(unified_func_types<T>::_fake());
};






int my_func(long lval, short sval) {
    return 5;
}

struct my_functor {
    int operator() (long lval, short sval) {
        return 5;
    }
};

int main() {
    // using types = unified_func_types<decltype(my_func)>::types;
    using types = unified_func_types<my_functor>::types;
    std::cout << (std::is_same<types::ret_t, int>::value ? "true" : "false") << std::endl;         // prints "true"
    std::cout << (std::is_same<types::param_t<0u>, long>::value ? "true" : "false") << std::endl;  // prints "true"
    std::cout << (std::is_same<types::param_t<1u>, short>::value ? "true" : "false") << std::endl; // prints "true"
    std::cout << types::param_cnt;
    return 0;
}
```
</div>

