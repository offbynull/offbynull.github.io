<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

If using the defaults, the book recommends explicitly declaring the methods but adding ` = default` after both signatures instead of specifying a body. The reason is that the default is almost always wrong, so if you tack this on it makes it explicit to others that you intended this.

```c++
class MyStruct {
    ...

    MyStruct(const MyStruct &orig) = default;
    MyStruct& operator=(const MyStruct &orig) = default;
}
```

ALSO, there's ambiguity around when the compiler generates default move/copy/destructor methods. It might be compiler specific. The book recommends that if you're using the defaults, always set them to `= default` (or do `= delete` to disallow them).

class MyStruct {
    ...

    // copy
    MyStruct(MyStruct &&orig) = default;
    MyStruct& operator=(MyStruct &&orig) = default;
    // move
    MyStruct(MyStruct &&orig) = default;
    MyStruct& operator=(MyStruct &&orig) = default;
    // destructor
    ~MyStruct() = default;
}
```
</div>

