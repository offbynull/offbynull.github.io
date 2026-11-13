<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

Cleverly using templates as shown above is the most robust way to check a callable's return type. But, if your requirements aren't overly complex, it may be feasible to use simpler checks such as those discussed in the parameter types section before this section. For example, if the scenario allows for it, a concept_TEMPLATE check can be reduced to just a set of parameter list `requires` clauses being logically or'd together.

```c++
// concept for a function whose return type is an integral type
template<typename Fn>
concept MySpecialFunction =
    requires(Fn f, int i) {
        { f(i) } -> std::same_as<int>;
    }
    || requires(Fn f, long l) {
        { f(l) } -> std::same_as<long>;
    };


// usage
template<MySpecialFunction Fn>
decltype(auto) call(Fn fn) {
    return fn(2);
}

int square_int(int num) {
    return num * num;
}

long square_long(long num) {
    return num * num;
}

int main() {
    std::cout << call(square_int) << std::endl;
    std::cout << call(square_long) << std::endl;
    return 0;
}
```
</div>

