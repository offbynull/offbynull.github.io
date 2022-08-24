<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

Cleverly using templates as shown above is the most robust way to check a parameter's type. But, if your requirements aren't overly complex, there may be simpler ways.

**SCENARIO 1: Testing for a known concrete types**

In this scenario, the requirement is that a callable's parameter type be a concrete type that's known beforehand (e.g. `int`). The concept_TEMPLATE for the callable itself can simply use a parameter list `requires` clause.

```c++
// concept for a function that takes in a single argument of type int
template <typename Fn>
concept MySpecialFunction = requires(Fn f, int t) {
            { f(t) } -> std::same_as<int>;
        };
```

**SCENARIO 2: Testing for a set of known concrete types**

In this scenario, the requirement is that a callable's parameter be one of a set of concrete types that's known beforehand (e.g. `int` or `long`). The concept_TEMPLATE for the callable can be exploded out into several sub-concept_TEMPLATEs: Each sub-concept_TEMPLATE checks that the callable's parameter type match a specific concrete type, then those sub-concept_TEMPLATEs combine to form the full concept_TEMPLATE.

```c++
// concept that combines the two sub-concepts: checks for a function has a single parameter of type int or long
template<typename Fn>
concept MySpecialFunction1 = requires(Fn f, int i) {   // sub-concept1: func that has a single parameter of type int
    { f(i) } -> std::same_as<decltype(i)>;
};

template<typename Fn>
concept MySpecialFunction2 = requires(Fn f, long l) {  // sub-concept2: func that has a single parameter of type long
    { f(l) } -> std::same_as<decltype(l)>;
};

template<typename Fn>
concept MySpecialFunction = MySpecialFunction1<Fn> || MySpecialFunction2<Fn>;  // final concept: func that has a single parameter of type int or long


// usage
template<MySpecialFunction Fn>
decltype(auto) call(Fn f) {
    return f(2);
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

The problem with exploding out to sub-concept_TEMPLATEs is that the number of sub-concept_TEMPLATEs can get very large. For example, if the callable should have 4 parameters and each of those parameters should be of type `int`, `long`, `short`, or `void*`, that's 256 different sub-concept_TEMPLATEs to list out.

```c++
// sub-concepts for function that takes in 4 params:
// param1: int|long|short|void*
// param2: int|long|short|void*
// param2: int|long|short|void*
// param3: int|long|short|void*
//
// 4^4=256 sub-concepts required, not really feasible to code something like this out
template<typename Fn>
concept MySpecialFunction1 = requires(Fn f, int p1, int p2, int p3, int p4) {
    { f(p1, p2, p3, p4) } -> std::same_as<long>;
};

template<typename Fn>
concept MySpecialFunction2 = requires(Fn f, int p1, int p2, int p3, long p4) {
    { f(p1, p2, p3, p4) } -> std::same_as<long>;
};

template<typename Fn>
concept MySpecialFunction3 = requires(Fn f, int p1, int p2, int p3, short p4) {
    { f(p1, p2, p3, p4) } -> std::same_as<long>;
};

template<typename Fn>
concept MySpecialFunction4 = requires(Fn f, int p1, int p2, int p3, void* p4) {
    { f(p1, p2, p3, p4) } -> std::same_as<long>;
};

template<typename Fn>
concept MySpecialFunction5 = requires(Fn f, int p1, int p2, long p3, int p4) {
    { f(p1, p2, p3, p4) } -> std::same_as<long>;
};

template<typename Fn>
concept MySpecialFunction6 = requires(Fn f, int p1, int p2, long p3, long p4) {
    { f(p1, p2, p3, p4) } -> std::same_as<long>;
};

...

template<typename Fn>
concept MySpecialFunction256 = requires(Fn f, void* p1, void* p2, void* p3, void* p4) {
    { f(p1, p2, p3, p4) } -> std::same_as<long>;
};

// combine sub-concepts together into final concept
template<typename Fn>
concept MySpecialFunction =
    MySpecialFunction1<Fn>
    || MySpecialFunction2<Fn>
    || MySpecialFunction3<Fn>
    || MySpecialFunction4<Fn>
    || MySpecialFunction5<Fn>
    || MySpecialFunction6<Fn>
    || ...
    || MySpecialFunction256<Fn>;



// usage
template<typename Fn>
    requires MySpecialFunction<Fn>
decltype(auto) call(Fn fn) {
    return fn(1, 2, 3, 4);
}

long multiply(int num1, long num2, short num3, long num4) {
    return num1 * num2 * num3 * num4;
}

int main() {
    std::cout << call(multiply) << std::endl;
    return 0;
}
```

One potential workaround to the sub-concept_TEMPLATE explosion problem shown in the example above is to use a parameter list `requires` clause: Each of the 4 parameter types gets fed into the top-level concept_TEMPLATE as a template parameter and requirements are individually tested on each of those template parameters.

```c++
// function that takes in 4 params:
// param1: int|long|short|void*
// param2: int|long|short|void*
// param2: int|long|short|void*
// param3: int|long|short|void*
template<typename Fn, typename P1, typename P2, typename P3, typename P4>
concept MySpecialFunction =
    (std::same_as<P1, int> || std::same_as<P1, long> || std::same_as<P1, short> || std::same_as<P1, void*>)
    && (std::same_as<P2, int> || std::same_as<P2, long> || std::same_as<P2, short> || std::same_as<P2, void*>)
    && (std::same_as<P3, int> || std::same_as<P3, long> || std::same_as<P3, short> || std::same_as<P3, void*>)
    && (std::same_as<P4, int> || std::same_as<P4, long> || std::same_as<P4, short> || std::same_as<P4, void*>)
    && requires(Fn f, P1 p1, P2 p2, P3 p3, P4 p4) {
        { f(p1, p2, p3, p4) } -> std::same_as<long>;
    };
```

Doing this removes the sub-concept_TEMPLATE explosion problem, but it introduces a new problem of the compiler losing the ability to infer template parameters from usage. In the example below, the concept_TEMPLATE for the callable is concise, but usages of `call()` now need to explicitly specify what each template argument is because the C++ compiler is no longer able to infer them on its own.

```c++
// function that takes in 4 params:
// param1: int|long|short|void*
// param2: int|long|short|void*
// param2: int|long|short|void*
// param3: int|long|short|void*
template<typename Fn, typename P1, typename P2, typename P3, typename P4>
concept MySpecialFunction =
    (std::same_as<P1, int> || std::same_as<P1, long> || std::same_as<P1, short> || std::same_as<P1, void*>)
    && (std::same_as<P2, int> || std::same_as<P2, long> || std::same_as<P2, short> || std::same_as<P2, void*>)
    && (std::same_as<P3, int> || std::same_as<P3, long> || std::same_as<P3, short> || std::same_as<P3, void*>)
    && (std::same_as<P4, int> || std::same_as<P4, long> || std::same_as<P4, short> || std::same_as<P4, void*>)
    && requires(Fn f, P1 p1, P2 p2, P3 p3, P4 p4) {
        { f(p1, p2, p3, p4) } -> std::same_as<long>;
    };


// usage
template<typename Fn, typename P1, typename P2, typename P3, typename P4>
    requires MySpecialFunction<Fn, P1, P2, P3, P4>
decltype(auto) call(Fn fn) {
    return fn(1, 2, 3, 4);
}

long multiply(int num1, long num2, short num3, long num4) {
    return num1 * num2 * num3 * num4;
}

int main() {
    // std::cout << call(multiply) << std::endl; // <--- WON'T COMPILE because template parameters can't be inferred by the compiler
    std::cout << call<decltype(multiply), int, long, short, long>(multiply) << std::endl; // <--- WILL COMPILE because template parameters explicitly listed,
    return 0;
}
```
</div>

