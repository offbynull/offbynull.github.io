<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

This is how C++ provides its version of Java's `Object.toString()`. For each class that you want to be able to print as a string, you implement a templated friend function of the left-shift operator overload (<<) that targets the class `ostream`, making it usable in something like `std::cout`.

```c++
ostream& operator<<(ostream &os, const MyClass &obj) {
    os << obj.x << "\n";
    return os;
}
```

It seems like a convoluted way to do it.
</div>

