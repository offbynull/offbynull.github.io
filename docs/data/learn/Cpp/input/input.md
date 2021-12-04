`{title} C++`

```{toc}
```


# TODOs

TODO: Set prereqs



TODO: https://github.com/AnthonyCalandra/modern-cpp-features



TODO:  https://stackoverflow.com/questions/57363324/ramifications-of-c20-requiring-twos-complement



TODO:  https://www.reddit.com/r/cpp/comments/r3pmw2/writing_portable_c_code_and_undefined_unspecified/  + evaluation order of isn't defined (**SEE CH7 -- EXECUTION ORDER SECTION**)

`{bm-disable-all}`
> Evaluation order determines the execution sequence of operators in an expression. A common misconception is that precedence and evaluation order are equivalent: they are not. Precedence is a compile time concept that drives how operators bind to operands. Evaluation order is a runtime concept that drives the scheduling of operator execution.
> 
> In general, C++ has no clearly specified execution order for operands. Although operators bind to operands in the well-defined way explained in the preceding sections, those operands evaluate in an undefined order. The compiler can order operand evaluation however it likes.

the last few paragraphs list out exceptions

SEE https://stackoverflow.com/a/5473530
`{bm-enable-all}`

worth putting in associtivity and operator precedence in operator section????
implementaiton-specific behaviour with implict casts (see implicit casts section -- AVOIDABLE USING BRACED INITIALIZATION)

UNDEFINED OVERFLOW/UNDERFLOW: talk about how this can be used.
```c++
#include <limits>
try {
    auto c = a + std::numeric_limits<unsigned int>::max(); ➌
} catch(const std::overflow_error& e) {
    printf("(a + max) Exception: %s\n", e.what());
}
```



TODO: `static_assert`



TODO: what is the spaceship operator?




TODO: put in a section for user-defined literals? it's used by the chrono header a lot.


TODO: organize constant sections under a common "Constant" section and volatile sections under a common "Volatile" section.


TODO: continue from ch 8

# Operators

**Bitwise Logical Operators**

| Name                       | Example            | Note                                             |
|----------------------------|--------------------|--------------------------------------------------|
| Bitwise AND         (`&`)  | `0b1011 & 0b0110`  |                                                  |
| Bitwise OR          (`\|`) | `0b1011 \| 0b0110` |                                                  |
| Bitwise XOR         (`^`)  | `0b1011 ^ 0b0110`  |                                                  |
| Bitwise NOT         (`~`)  | `~0b1011`          |                                                  |
| Bitwise left-shift  (`<<`) | `0b1011 << 2`      |                                                  |
| Bitwise right-shift (`>>`) | `0b1011 >> 2`      | Result on signed may be different than unsigned. |

**Boolean Logical Operators**

| Name                 | Example           | Note |
|----------------------|-------------------|------|
| Logical AND (`&&`)   | `true && true`    |      |
| Logical OR  (`\|\|`) | `true \|\| false` |      |
| Logical NOT (`!`)    | `!true`           |      |

**Arithmetic Operators**

| Name                   | Example | Note |
|------------------------|---------|------|
| Unary Plus      (`+`)  | `+10`   |      |
| Unary Minus     (`-`)  | `-10`   |      |
| Addition        (`+`)  | `1 + 2` |      |
| Subtraction     (`-`)  | `2 - 1` |      |
| Multiplication  (`*`)  | `2 * 3` |      |
| Division        (`/`)  | `6 / 2` |      |
| Modulo          (`%`)  | `6 % 4` |      |

There are implicit rules for how fundamental types get promoted. The general rule of thumb is that the result of the operator is promoted to the operand with the "greater" type. For example, if an `int` is added to a `float`, the result will be a `float`.

These rules are similar to those in other languages (e.g. Java and Python).

```{note}
If confused, use type deduction via the `auto` keyword: `auto x = 5 + y`, then check to see what the type of `y` is in the IDE or using `typeid`.
```

**Assignment Operators**

| Name                                   | Example        | Note                                                                                                                             |
|----------------------------------------|----------------|----------------------------------------------------------------------------------------------------------------------------------|
| Assignment                     (`=`)   | `x = 5`        |                                                                                                                                  |
| Assignment Bitwise AND         (`&=`)  | `x &= 0b0110`  |                                                                                                                                  |
| Assignment Bitwise OR          (`\|=`) | `x \|= 0b0110` |                                                                                                                                  |
| Assignment Bitwise XOR         (`^=`)  | `x ^= 0b0110`  |                                                                                                                                  |
| Assignment Bitwise left-shift  (`<<=`) | `x <<= 2`      |                                                                                                                                  |
| Assignment Bitwise right-shift (`>>=`) | `x >>= 2`      | Result on signed may be different than unsigned.                                                                                 |
| Assignment Addition            (`+=`)  | `x += 2`       |                                                                                                                                  |
| Assignment Subtraction         (`-=`)  | `x -= 1`       |                                                                                                                                  |
| Assignment Multiplication      (`*=`)  | `x *= 3`       |                                                                                                                                  |
| Assignment Division            (`/=`)  | `x /= 2`       |                                                                                                                                  |
| Assignment Modulo              (`%=`)  | `x %= 4`       |                                                                                                                                  |
| Increment                      (`++`)  | `x++`          | Applicable BEFORE or AFTER the operand: `++x` returns the value AFTER modification, `x++` returns the value BEFORE modification. |
| Decrement                      (`--`)  | `x--`          | Applicable BEFORE or AFTER the operand: `--x` returns the value AFTER modification, `x--` returns the value BEFORE modification. |

All assignment operators work similar to those in Java except for the increment and decrement operators. Due to the confusion it causes, Java disallows the increment / decrement from returning a value, meaning that it can't be used in an expression. Not so in C++. In addition to modifying the variable passed as the operand, in C++ these operators also return a result, meaning that it's okay to an increment / decrement operator within some larger expression. 

```c++
int x = 3;
int y = (x++) + 2;
// at this point, x is 4, y is 5
int a = 3;
int b = (++a) + 2;
// at this point, a is 4, b is 6
```

**Comparison Operator**

| Name                            | Example  | Note |
|---------------------------------|----------|------|
| Equal To                 (`==`) | `5 == 7` |      |
| Not Equal To             (`!=`) | `5 != 7` |      |
| Less Than                (`<`)  | `5 < 7`  |      |
| Less Than Or Equal To    (`<=`) | `5 <= 7` |      |
| Greater Than             (`>`)  | `5 > 7`  |      |
| Greater Than Or Equal To (`>=`) | `5 >= 7` |      |

**Ternary Conditional Operator**

The ternary conditional operator is a pseudo operator that takes in 3 operands similar to those found in other high-level languages: `CONDITION ? EXPRESSION_IF_TRUE : EXPRESSION_IF_FALSE`. It's essentially a shorthand if-else block. 

```c++
int x = n % 7 == 1 ? 1000 : -1000;
// equiv to...
if (n % 7 == 1) {
    x = 1000;
} else {
    x = -1000;
}
```

**Member Access Operators**

| Name                     | Example     | Note                                                                                       |
|--------------------------|-------------|--------------------------------------------------------------------------------------------|
| Subscript         (`[]`) | `x[0]`      |                                                                                            |
| Indirection       (`*`)  | `*x`        | Doesn't conflict with arithmetic multiplication operator because this is a unary operator. |
| Address Of        (`&`)  | `&x`        |                                                                                            |
| Member Of Object  (`.`)  | `x.member`  |                                                                                            |
| Member Of Pointer (`->`) | `x->member` |                                                                                            |

There operators are used in scenarios that deal with accessing the members of an object (e.g. element in an array, field of a class) or dealing with memory addresses / pointers. The subscript and and member of object operators are similar to their counterparts in other high-level languages (e.g. Java, Python, C#, etc..). The others are unique to languages with support for lower-level programming like C++. Their usage is detailed in other sections.

**Dynamic Object Operators**

| Name                                | Example       | Note |
|-------------------------------------|---------------|------|
| Create Dynamic Object       (`new`) | `new int`     |      |
| Create Dynamic Array      (`new[]`) | `new int[50]` |      |
| Destroy Dynamic Object   (`delete`) | `delete x`    |      |
| Destroy Dynamic Array  (`delete[]`) | `delete[] x`  |      |

```{note}
If you already know about dynamic objects and arrays and constructors/destructors, make sure you delete an array using `delete[]`. It makes sure to call the destructor for each element of the array.
```

**Size Operator**

| Name            | Example     | Note |
|-----------------|-------------|------|
| Size (`sizeof`) | `sizeof x]` |      |

This operator gets the size of an object in bytes. Note that an object's byte size may not be indicative of the da may include padding required by the platform (e.g. an object requiring 5 bytes may get expanded to 8 bytes because the platform requires 8 byte boundary alignments).

**Other Operators**

C++ provides a set of other operators such as the ...

 * comma operator (`,`).
 * function call operator (`()`).
 * conversion operator (e.g. casting).

While it isn't worth going into them in detail here, the reason the language explicitly lists them as operators is because they're overload-able (e.g. operator overloading). Overloading these operators is heavily discouraged since doing so causes confusion.

````{note}
The book mentions the comma operator specifically. It doesn't look this is used for much and the book recommends against using it for anything (e.g. operator overloading) due to the confusion it causes. This gives off similar vibes to Python's tuple syntax, where you can pass an unenclosed tuple as a subscript to something. When I was learning Python, that also came off as very confusing.

```python
x = obj['column name', 100]
```
````

# Types

## Core Integer Types

C++'s core integer types are as follows...

1. `short int`
1. `int`
1. `long int`
1. `long long int`

The above integer types come in two forms: signed and unsigned. Tha range of ...

* unsigned integers starts at 0 and ends at a positive integer.
* signed integers starts at a negative integer and positive integer.

By default, the integer types above are signed (speculation). Signed-ness can be explicitly stated by prefixing either `signed` or `unsigned` to the type, but if the type is signed the prefix is usually omitted.

| signed                                   | unsigned                 |
|------------------------------------------|--------------------------|
| `short int`     / `signed short int`     | `unsigned short int`     |
| `int`           / `signed int`           | `unsigned int`           |
| `long int`      / `signed long int`      | `unsigned long int`      |
| `long long int` / `signed long long int` | `unsigned long long int` |

Integer types `char int`, `short int`, `long int`, and `long long int` can optionally omit the `int` keyword.

| signed                           | unsigned             |
|----------------------------------|----------------------|
| `short`     / `signed short`     | `unsigned short`     |
| `int`       / `signed int`       | `unsigned int`       |
| `long`      / `signed long`      | `unsigned long`      |
| `long long` / `signed long long` | `unsigned long long` |

The only guarantees for core integer types are that ...

 * each integer type tier must be able to cover the same range as the tier before it (e.g. range of `short` >= range of `int`).
 * unsigned integer types start at 0. 
 * unsigned integer types overflow behaviour is to wrap to 0.

All other specifics are platform-dependent. Specifically, ...

 * range is undefined.
 * bit length is undefined (e.g. 8, 16, etc..).
 * endian-ness is undefined (e.g. big-endian vs little-endian).
 * encoding scheme is undefined (e.g. one's complement, two's complement, etc..).
 * overflow behaviour of _signed_ types is undefined (e.g. crash, stay at boundary, wrap back around, etc..).

Integer ranges, although platform-specific, are queryable in the climits header.

| type                 | min           | max          |
|----------------------|---------------|--------------|
| `signed short`       | `SHRT_MIN`    | `SHRT_MAX`   |
| `signed int`         | `INT_MIN`     | `INT_MAX`    |
| `signed long`        | `LONG_MIN`    | `LONG_MAX`   |
| `signed long long`   | `LLONG_MIN`   | `LLONG_MAX`  |
| `unsigned short`     | `0`           | `USHRT_MAX`  |
| `unsigned int`       | `0`           | `UINT_MAX`   |
| `unsigned long`      | `0`           | `ULONG_MAX`  |
| `unsigned long long` | `0`           | `ULLONG_MAX` |

By default, literals are represented using base10. Literals may be presented in different bases via the prefix.

| base         | literal prefix | example  |
|--------------|----------------|----------|
| 2 (binary)   | 0b             | `0b1111` |
| 8 (octal)    | 0              | `016`    |
| 10 (decimal) |                | `15`     |
| 16 (hex)     | 0x             | `0xF`    |

Integer literals are targeted to specific integer types by their suffix.

| type                 | literal suffix | example |
|----------------------|----------------|---------|
| `signed short`       |                |         |
| `signed int`         |                |         |
| `signed long`        | L              | `2L`    |
| `signed long long`   | LL             | `2LL`   |
| `unsigned short`     |                |         |
| `unsigned int`       | U              | `2U`    |
| `unsigned long`      | UL             | `2UL`   |
| `unsigned long long` | ULL            | `2ULL`  |

```{note}
Notice that `int`, `short`, and `unsigned short` don't have explicit suffixes. If no suffix is present, it's an int (speculation). To get it to a short, the easiest way is to cast it: `(short) 2`.
```

```{note}
See also `std::numeric_limits` in the limits header. This seems to also provide platform-specific definitions that are queryable via functions..
```

## Sized Integer Types

Integer types with standardized bit lengths are defined in the cstdlib header.

| signed          | unsigned         | description                                                            |
|-----------------|------------------|------------------------------------------------------------------------|
| `intmax_t`      | `uintmax_t`      | widest possible bit length                                             |
| `int8_t`        | `uint8_t`        | exactly 8 bits                                                         |
| `int16_t`       | `uint16_t`       | exactly 16 bits                                                        |
| `int32_t`       | `uint32_t`       | exactly 32 bits                                                        |
| `int64_t`       | `uint64_t`       | exactly 64 bits                                                        |
| `int_least8_t`  | `uint_least8_t`  | 8 bits  or greater                                                     |
| `int_least16_t` | `uint_least16_t` | 16 bits or greater                                                     |
| `int_least32_t` | `uint_least32_t` | 32 bits or greater                                                     |
| `int_least64_t` | `uint_least64_t` | 64 bits or greater                                                     |
| `int_fast8_t`   | `uint_fast8_t`   | 8 bits  or greater                                                     |
| `int_fast16_t`  | `uint_fast16_t`  | 16 bits or greater                                                     |
| `int_fast32_t`  | `uint_fast32_t`  | 32 bits or greater                                                     |
| `int_fast64_t`  | `uint_fast64_t`  | 64 bits or greater                                                     |
| `intptr_t`      | `uintptr_t`      | wide enough to hold a void *                                           |
|                 | `size_t`         | wide enough to hold the maximum number of bytes of something in memory |

The minimum and maximum extents of each type are defined in `{TYPE}_MIN` and `{TYPE}_MAX`, where `{TYPE}` doesn't include the `_t` suffix. For example the maximum value an `uint64_t` can be is `UINT64_MAX`.

```{note}
Not all types guaranteed to be present (e.g. 64-bit types may be missing if platform can't support it). Unsigned types don't have a minimum extent defined because a minimum of any unsigned integer type is always 0 (e.g. uint64_t can't go any lower than 0).
```

To expand any integer __literal__ to a ...

 * `intmax_t`, use the macro `INTMAX_C(...)`.
 * `uintmax_t`, use the macro `UINTMAX_C(...)`.
 * `int{N}_t`, use the macro `INT{N}_C(...)` (where `{N}` is the bit length).
 * `uint{N}_t`, use the macro `UINT{N}_C(...)` (where `{N}` is the bit length).

```{note}
What's the point of the above? You don't know what internal integer type each standardized type maps to. For example, `uint64_t` may map to `unsigned long long`, which means when you want to assign a literal to a variable of that type you need to add a `ULL` suffix...

`uint64_t test = 9999999999999999999ULL`

The macros above make it so that you don't need to know the underlying mapping...

`uint64_t test = UINT64_C(9999999999999999999)`
```

```{note}
See also `std::numeric_limits` in the limits. This seems to also provide platform-specific definitions that are queryable via functions..
```

## Floating Point Types

C++'s core floating point types are as follows...

| type          | description        | literal suffix | example  |
|---------------|--------------------|----------------|----------|
| `float`       | single precision   | `f`            | `123.0f` |
| `double`      | double precision   |                | `123.0`  |
| `long double` | extended precision | `L`            | `123.0L` |

The specifics of each type are platform-dependent. The only guarantee is that each each type has to hold at least the same range as the type before it (e.g. `double`'s range should cover `float`'s range). Other than that, ...

* rounding mode is undefined.
* exponent bit length is undefined.
* mantissa bit length is undefined.
* subnormal number support is undefined.

Floating point characteristics, although platform-specific, are queryable in the cfloat header.

| type          | min        | max        | min exponent   | max exponent   | mantissa digits | radix        | epsilon        |
|---------------|------------|------------|----------------|----------------|-----------------|--------------|----------------|
| `float`       | `FLT_MIN`  | `FLT_MAX`  | `FLT_MIN_EXP`  | `FLT_MAX_EXP`  | `FLT_MANT_DIG`  | `FLT_RADIX`  | `FLT_EPSILON`  |
| `double`      | `DBL_MIN`  | `DBL_MAX`  | `DBL_MIN_EXP`  | `DBL_MAX_EXP`  | `DBL_MANT_DIG`  | `DBL_RADIX`  | `DBL_EPSILON`  |
| `long double` | `LDBL_MIN` | `LDBL_MAX` | `LDBL_MIN_EXP` | `LDBL_MAX_EXP` | `LDBL_MANT_DIG` | `LDBL_RADIX` | `LDBL_EPSILON` |

```{note}
Mantissa digits is the number of digits (of the base specified in radix) that the floating point type uses (speculation).

Epsilon is the difference between 1 and the floating point number just before 1.
```

```{note}
The sizeof operator should NOT be used to infer limits / characteristics of a floating point type. For example, a `sizeof(long double)` 16 doesn't necessarily mean that the type is a quadruple precision float (128-bit). Rather, it's likely that the floating point type has less precision but the platform requires padding.
```

The rounding behaviour of all floating point types is queryable via `FLT_ROUNDS`, where a ...

 * -1 means undetermined.
 * 0 means toward zero.
 * 1 means toward nearest.
 * 2 means toward positive infinity.
 * 3 means toward negative infinity.

The floating point evaluation behaviour is queryable via `FLT_EVAL_METHOD`, where a ...

 * -1 means undetermined.
 * 0 means evaluate just to the range and precision of the type.
 * 1 means evaluate float and double as double, and long double as long double.
 * 2 means evaluate all as long double
 * negative value other than -1 means platform-specific behavior.

```{note}
Unsure about the last point. How's the last point any different than -1?
```

```{note}
I see online that `FLT_DIG`, `DBL_DIG`, `LDBL_DIG`, and `DECIMAL_DIG` define the number of "decimal digits" that can be converted to floating point and back without a loss in precision. I'm assuming that just means the max number of digits that can be represented in a float where exp is 1?
```

```{note}
See also `std::numeric_limits` in the limits header. This seems to also provide platform-specific definitions that are queryable via functions..
```

## Character Types

Core C++ strings are represented as an array of characters, where that array ends with a null character to signify its end. This is in contrast to other major platforms that typically structure strings a size integer along with the array (no null terminator).

Individual characters all map to integer types, where literals are defined by wrapping the character in single quotes. Even though they're integers, the signed-ness of each of the types below isn't guaranteed.

| type       | bits | literal prefix | example | description                                                 |
|------------|------|----------------|---------|-------------------------------------------------------------|
| `char`     | >= 8 |                | `'T'`   | >= 8-bit wide character (smallest unit of memory -- 1 byte) |
| `char16_t` | 16   | `u`            | `u'T'`  | 16-bit wide character (e.g. UTF-16)                         |
| `char32_t` | 32   | `U`            | `U'T'`  | 32-bit wide character (e.g. UTF-32)                         |
| `wchar_t`  |      | `L`            | `L'T'`  | at least as wide as `char`                                  |

Note that `char` and `wchar_t` don't have predefined bit lengths. They are platform-dependent. The bit length for...

* `char` is defined in `CHAR_BIT` of climits and must be at least 8 bits.
* `wchar_t` must be equal to or greater than that of `char`.

```{note}
`char` literals can also be integers, but the signed-ness of the `char` type isn't defined by default (speculation). It can specifically be made to signed / unsigned by prefixing it as such: `signed char` / `unsigned char`.
```

Strings literals are wrapped in double quotes instead of single quotes, where they get transformed into an array terminated by a null character.

| type         | literal prefix | example     | description                           |
|--------------|----------------|-------------|---------------------------------------|
| `char *`     |                | `"hello"`   | unknown encoding (platform specific?) |
| `wchar_t *`  | `L`            | `L"hello"`  | unknown encoding (platform specific?) |
| `char16_t *` | `u`            | `u"hello"`  | encoded as UTF-16                     |
| `char32_t *` | `U`            | `U"hello"`  | encoded as UTF-32                     |
| `char8_t *`  | `u8`           | `u8"hello"` | encoded as UTF-8                      |

Typically escaping rules apply to string literals. Unescaped string literals are allowed by adding an `R` at the end of the literal prefix, which make it so that the ...

 1. starting quote requires a custom delimiter immediately after it.
 2. finishing quote requires a custom delimited immediately before it.
 
These delimiter characters are characters that aren't encountered in the contents of the string itself. For example, in `u8R"|hello|"`, the delimiter is `|` and isn't included in the resulting UTF-8 string.

## Void Type

`void` is a type that represents an empty set of values. Since it can't hold a value, C++ won't allow you to declare an object of type void. However, you can use it to declare that a function ...

* returns no value (`void` return).
* accepts no arguments (`void` parameter list).

## Enumeration Types

C++ enumerations are be declared using `enum class`.

```c++
enum class MyEnum {
   OptionA,
   OptionB,
   OptionC
};

MyEnum x = MyEnum::OptionC;
```

Under the hood, an enum is represented as an integer data type where each of its options is a particular integer constant (speculation -- is it guaranteed to be an int or is it something that's platform-specific?).

Enumerations may be used with `switch` statements as well.

```c++
switch (x) {
    case MyEnum::OptionA:
        ...
        break;
    case MyEnum::OptionB:
        ...
        break;
    case MyEnum::OptionC:
        ...
        break;
    default:
        break;
}
```

````{note}
It's possible to remove the `class` from `enum class`, which heavily loosens type-safety and scope. By removing `class`, the options within have their values implicitly converted to integers and you don't need the resolution scope operator (their options are accessible at the same level as an enum).

```c++
enum MyEnum { // no class keywrod
   OptionA,
   OptionB,
   OptionC
};

MyEnum x = OptionC; // this is okay -- don't have to use MyEnum::OptionC
int y = OptionC;    // this is okay -- options are integers
```

You should prefer `enum class`.
````

## Array Types

C++ allows for the creation of arrays of constant length (size of the array must be known at compile-time). Elements of an array are guaranteed to be a contiguous in memory (speculation).

* `int x[100]` - Creates an array of 100 ints where those 100 ints are junk values (data previously at that memory location is not zero'd out).
* `int x[] { 5, 5, 5 }` - Creates an array of 3 ints where each of those ints have been initialized to 5 (braced initialization).
* `int x[] = { 5, 5, 5 }` - Equivalent to above (assignment does not do any extra work).
* `int x[3] {}` - Creates an array of 3 ints where each of those ints are 0 (memory zero'd out -- braced initialization).
* `int x[3] = {}` - Equivalent to above (assignment does not do any extra work).
* `int x[n]` - Disallowed by C++ if n isn't a constant. These types of arrays are allowed in C (called variable length arrays / VLA), but not in C++ because C++ has collection classes that allow for sizes not known at compile-time.

Accessing arrays is done similarly to how it is in most other languages, by subscripting (e.g. `x[0] = 5`). The only difference is that array access isn't bounds-checked and array length information isn't automatically maintained at run-time. For example, if an array has 100 elements, C++ won't stop you from trying to access element 250 -- out-of-bounds array access is undefined behaviour.

One way to think of an arrays is as pointer to a contiguous block of elements of the array type. In fact, if an array type gets used where it isn't expected, that array type automatically decays to a pointer type.

```c++
int test(int *x) {
   return x[0] + x[1];
}

void run() {
   int x[3] = { 1, 2, 3 };
   int y = test(x);
}
```

````{note}
My understanding is that arrays are typically passed to functions as pointers + array length. This is because the array length information is only available at compile-time, meaning that if you have a function that takes in an array, how would it know the size of the array it's working with (it isn't the one who declared it). It looks like you can for the function to an array type of fixed size, but apparently that doesn't mean anything? The compiler doesn't enforce that a caller use an array of that fixed size, and using sizeof on the array will produce a warning saying that it's decaying into a pointer.

```c++
size_t test(int x[10]) {
   return sizeof(x); // compiler warning that this is returning sizeof(int *)
}

int main() {
   int x[3] = { 1, 2, 3 };
   size_t y = test(x); // compiler doesn't complain that test() expects int[10] but this is int[3]
   cout << y;
   return 0;
}
```
````


Be careful when using the `sizeof` operator on an array. If the type is the original array type, `sizeof` will return the number of bytes taken up by the elements of that array (known at compile-time). However, if the type has decayed to a pointer type, `sizeof` will return the number of bytes to hold on to a pointer.

```c++
int x[3];
int *y = x;  // equiv to setting to &(x[0]);
cout << sizeof x;  // should be the size of 3 ints
cout << sizeof y;  // should be the size of a pointer
```

Similarly, range-based for loops won't work if the type has decayed to a pointer type because the array size of that pointer isn't known at compile-time.

```c++
int x[3] = {1,2,3};
int *y = x;
for (int i = 0; i < 3; i++) { // OK
   cout << y[i] << endl;
}
for (int v : x) { // OK
   cout << v << endl;
}
for (int v : y) { // ERROR
   cout << v << endl;
}
```

You may be tempted to use `sizeof(array) / sizeof(type)` to determine the number of elements within an array. It's a better idea to use `std::size(array)` instead (found in the iterator header) because it should have logic to workaround and platform-specific behaviours that might cause inconsistent results / unexpected behaviour (speculation).

## Pointer Types

C++ provides types that reference a memory address, called pointers. Variables of these types can point to different memory addresses / objects.

Adding an asterisk (\*) to the end of any type makes it a pointer type (e.g. `int *` is a type that can contain a pointer to an `int`). A pointer to any object can be retrieved using the address-of unary operator (&). Similarly, the value in any pointer can be retrieved using the deference unary operator (\*).

```c++
int w {5};
int *x { &w }; // x points to w
int *y { &w }; // y points to w
int z = *x;    // z is a copy of whatever x points to, which is w, which means it gets set to 5
*x = 7;        // w is set to 5 through x

int **a { &x }; // a points to x, which points to w (a pointer to a pointer to an int)
```

As shown in the example above, it's perfectly valid to use the deference operator on the left-side of the equals. It defines where the result of the right side should go.

```c++
int w {5};
int *x { &w };  // x points to w
int **y { &x }; // y point to x, which points to w

**y = 7;        // y dereferenced twice and set to 7 -- w should now be 7 
```

The notation is confusing because asterisk (*) has different meanings. In the context of a ...

 * type declaration, an asterisk means that the type is a "pointer to" some other type.
 * unary operator in an expression, an asterisk means the object being pointed to should be accessed.
 * binary operator in an expression, an asterisk means multiplication.

```{note}
See also: member-of-pointer operator.
```

In addition, a pointer can optionally be set to nothing via the `nullptr` literal. `nullptr` is actually of type `std::nullptr_t`, but the compiler will implicit conversion to/from other pointer types when required.

```c++
int *y = nullptr; // implicit conversion
if (y == nullptr) {
    // report error
}
```

```{note}
It seems like there's some implicit conversions to boolean that are possible with pointers. If whatever the pointer is going to expects a boolean, its implicitly converted to `ptr != nullptr`? So in if / while/ for conditions, you can just use the pointer as is without explicitly writing out a condition?
```

```{note}
How is this different than the NULL macro? I guess because it's a distance type, you can have a function overload that takes in param of type `std::nullptr_t`? But why would you ever want to do that?
```

### Pointer Arithmetic

Certain arithmetic operators are allowed on pointers, called pointer arithmetic. Adding or subtracting integer types on a pointer will move that pointer by the number of bytes that makes up its underlying type.

```c++
int []x = {1, 5, 7};
int *ptrA = &(x[1]);  // points to idx 1 of x (5)
int *ptrB = ptrA + 1; // points to idx 2 of x (7)
```

This is similar to array access via the subscript operator. In fact, both arrays and pointers can be accessed in the same way using the subscript operator and pointer arithmetic.

```c++
int x[] { 1, 2, 3, 4, 5, 6, 7, 8, 9 };
int *y = x;
*(y+1) = 99;  // equivalent to x[1] = 99
x[2] = 101;   // equivalent to *(y+2) = 101;
```

```{note}
An array guarantees that its elements appear contiguously and in order within memory (I think?), so if the pointer is from a decay'd array, using pointer arithmetic to access its elements is perfectly fine.
```

### Void Pointer

A pointer to the void type means that the type being pointed to is unknown. Since the type is unknown, dereferencing a void pointer isn't possible. In otherwords, it isn't possible to read or write to the data pointed to by a void * because the underlying type is void / unknown.

```c++
int x[] { 1, 2, 3, 4, 5, 6, 7, 8, 9 };
void *y = x;
*y = 2; // fails
```

Since the underlying type of the pointer is unknown, pointer arithmetic isn't allowed either.

```c++
int x[] { 1, 2, 3, 4, 5, 6, 7, 8, 9 };
void *y = x;
y = y + 2; // fails
```

```{note}
If you have a `void *` and you want to do raw memory manipulation at that address, use a `std::byte *` instead. Why not just use `char *` instead? Is a `char` guaranteed to be 1 byte (I think it is)? According to [this](https://stackoverflow.com/a/46151026), it's because certain assumptions about `char`s may not hold with bytes? I don't know. Just remember `std::byte *` if you're working with raw data.
``` 

## Reference Types

C++ provides a more sanitized version of pointers called references. A reference type is declared by adding an ampersand (&) after the type rather than an asterisk (*), and it implicitly takes the address of whatever is passed into it when its created.

```c++
int w {5};

int *x { &w }; // x points to w
int &y { w };  // y references to w (note address-of operator not used here)
```

The main difference is between pointer types and reference types is that a reference type doesn't need to explicitly dereference to access the object pointed to. The object pointed to by the reference type is accessed as if it were the object itself.

```c++
*x = 10;       // x explicitly dereferenced to w and set to 10
y = 15;        // y implicitly dereferenced to w and set to 15
```

As shown in the example above, assignment to a reference type is assignment on the underlying object being referenced. As such, having the reference type point a different object isn't possible (reseating).

```{note}
One way to think of this is that it's implicitly `const` -- the compiler won't let explicitly set a reference to be `const`.
```

Similarly, it's not possible to have a reference to a reference.

```c++
int &&z { y }; // this isn't a thing -- fail
```

## Rvalue Reference Type

An rvalue reference is similar to a reference except that it tells the compiler that it's working with is an rvalue. Rvalue references are declared by adding two ampersands (&&) after the type rather than just one. It's initialized using the `std::move()` function within the utility header, which casts its input into an rvalue reference.

Rvalue references are typically used for moving objects (not copying, but actually moving the guts of one object into another). This is typically done through something called a move constructor, which will be explained further on.

```c++
MyObject a {};
MyObject &&b = std::move(a);  // get rvalue reference
MyObject c {b};               // move a into c (gut it into c) via the move constructor
// b is in an invalid state
```

```{note}
Once an object is moved, it's in an invalid state. The only two reliable operations you can perform on it is to either destroy or re-assign it to something else (assignments are discussed elsewhere).
```

## Union Types

C++ unions are a set of variables that point to the same underlying memory. Each union takes up only as much memory as its largest member.

```c++
union MyUnion {
   char raw[100];
   short num_int;
   double num_dbl;
}

MyUnion x;
// set all bytes of raw to 0
for (int i = 0; i < sizeof(x.raw); i++) {
   x.raw[i] = 0;
}
// since all members of the union start at the same memory location, these
// will by likely both be 0 (unless short or double has a byte size of over
// 100).
cout << x.num_int << endl;
cout << x.num_dbl << endl;
```

```
Consider using std::variant instead of unions.
```

## Class Types

C++ classes are declared using either the `struct` keyword or `class` keyword. When ...

 * `struct` is used, the default visibility of class members is public.
 * `class` is used, the default visibility of class members is private.

Public and private visibility are the same as in most other languages: private members aren't accessible outside the class while public members are.

```c++
class MyStruct {
    private:
    int count;
    bool flag;

    public:
    char name[256];
    void add() {
        count += 1;
        flag = false;
    }
};
```

C++ classes that contain only data are called plain-old-data classes (POD), and they're typically created using the `struct` keyword so as their members are all accessible by default.

```c++
struct MyStruct {
   int count;
   char name[256];
   bool flag;
};
```

```{note}
C++ guarantees that a class's fields will be sequentially stored in memory, but they may be padded / aligned based on the platform. Be aware when using the sizeof operator. 
```

### This Pointer

Non-static methods of a class have access to an implicit pointer called `this`, which allows for accessing that instance's members. As long as the class member doesn't conflict with a parameter name of the method invoked, the usage of that name will implicitly reference the `this` pointer.

The member-of-pointer operator (->) allows for dereferencing a pointer and accessing a member on the result in a more concise form.

```c++
class MyStruct {
    private:
    int count;
    bool flag;

    public:
    f1(int count) {
        this->count = count;  // equivalent to (*this).count = count
        flag = false;
    }

    f2(int count, bool flag) {
        this->count = count;  // equivalent to (*this).count = count
        this->flag = flag;    // equivalent to (*this).flag = flag
    }
}
```

### Construction

C++ classes are allowed one or more constructors that initialize the object. Similar to Java, each constructor should have the same name as the class itself, no return type, and a unique parameter list.

```c++
class MyStruct {
    private:
    int count;
    bool flag;

    public:
    MyStruct() {
        count = 0;
        flag = false;
    }

    MyStruct(int initialCount, bool initialFlag) {
        this->count = initialCount;
        this->flag = initialFlag;
    }
}
```

The above constructors are using the member-of-pointer operator (->) to access the `this` pointer. Non-static methods of a class have access to an implicit pointer called `this`, which allows for accessing that instance's members. The member-of-pointer operator allows for dereferencing a pointer and accessing a member on the result in a more concise form.

```c++
this->count = 0;  // equivalent to (*this).member = 0
```

If a class offers constructors, the least error-prone way to invoke it is to use braced initialization: `MyStruct x { 5, true }`. The reason is that C++ has so many object initialization foot-guns that, while simpler methods may work (e.g. `MyStruct x(5, true)`), those methods may end up being interpreted by the compiler as something else that's entirely different (e.g. function declaration).

```{note}
This ambiguity is often referred to as the "most vexing parse" problem.
```

Classes that don't have any constructors declared get an implicit zero-arg constructor that zeros out the memory of that class (speculation). If the class is a POD, a braced initialization that is ...

 * empty will zero out the memory for all fields, (implicit default constructor).
 * non-empty will set the individual fields, in the order they're declared in.

```c++
struct MyStruct {
   int count;
   char name[256];
   bool flag;
};

MyStruct a;                    // initialized to zero'd out memory (via implicit constructor)
MyStruct b {};                 // initialized to zero'd out memory (via implicit constructor)
MyStruct b {5, "steve", true}; // initialized to supplied arguments
```

```{note}
See [here](https://stackoverflow.com/a/49802943) for more information. The = operator won't result in a copy or anything like that (meaning performance won't suffer).
```

If a class does explicitly declare constructors, the implicit zero-arg constructor won't be generated. If desired, a zero-arg constructor may be declared with the default behaviour of the implicit zero arg constructor by adding `= default` instead of a method body.

```c++
class MyStruct {
    private:
    int count;
    bool flag;

    public:
    MyStruct() = default;
    MyStruct(int initialCount, bool initialFlag) {
        this->count = initialCount;
        this->flag = initialFlag;
    }
}
```

A field may be initialized to a value either through default member initializations or the member initializer list. For default member initializations, the initialization is done directly in the field's declaration.

```c++
struct MyStruct {
   int count {5};
   char name[256] {"steve"};
   bool flag {true};
};
```

In contrast, a member initializer list is a comma separated list of braced initializations for the fields of a class. It's specified just before a constructor's body.

```c++
struct MyStruct {
    int count;
    bool flag;

    MyStruct(): count{0}, flag{false} {
    }
}
```

Each item in the comma separated list is called a member initializer.


```{note}
How is this better than default member initialization, where initialization is done directly after the field declaration? According to [this](https://stackoverflow.com/a/48098997), it's more-or-less the same?
```

### Destruction

C++ classes are allowed an explicit cleanup function called a destructor (e.g. closing an open file handle, zeroing out memory for security purposes, etc..). A destructor is declared similarly to a constructor, the only differences being ...

 1. a tilde must appear just before the class / function name.
 2. it doesn't take in any arguments.

```c++
class MyStruct {
    private:
    int count {5};
    bool flag {true};

    public:
    ~MyStruct() {
        // do some cleanup here
    }
};
```

Destructors must never be called directly by the user, nor should an exception ever be thrown in a destructor.

If a destructor isn't declared, an empty one is implicitly generated.

### Copying

There are two built-in mechanisms for copying in C++: the copy constructor and copy assignment.

A copy constructor is a constructor that has a single parameter, a reference to a `const` object of the same type. By default, classes are implicitly provided with a default copy constructor if one hasn't been explicitly declared by the user. The copy semantics of this default copy constructor is to copy each field individually, called a member-wise copy.

Member-wise copying may not be the correct way to copy in certain cases, in which case a copy constructor should be explicitly provided with the correct copy semantics.

```c++
class MyStruct {
    ...

    MyStruct(const MyStruct &orig) {
        this->db = DatabaseConnection {orig.db.host, orig.db.port}; // make a new db connection instead of using orig's
        this->max = orig.max;
    }
}


MyStruct x {host, port};
MyStruct y {x}; // both x and y are independent and equal, but y has its own DatabaseConnection
```

Similarly, copy assignment is a method invoked when the assignment operator is used, called an operator overload. Unlike copy constructors, copy assignment is required to clean up any resources in the destination object prior to copying. By default, classes are implicitly provided with a copy assignment method if one hasn't been explicitly declared by the user. The copy semantics of this default method is to assign each field individually, called a member-wise copy.

```c++
class MyStruct {
    ...

    MyStruct& operator=(const MyStruct &orig) {
        if (this != &other) { // only do if assigning to self
            this->db.close(); // close existing db connection
            this->db = DatabaseConnection {orig.db.host, orig.db.port}; // make a new db connection
            this->max = orig.max;
        }
        return *this; // return self -- this should always be the case??
    }
}
```

To suppress the compiler from allowing copying or assignment of an object, add ` = delete` after both signatures instead of specifying a body. This is important if the object holds on to an un-copyable resource such as a lock.

```c++
class MyStruct {
    ...

    MyStruct(const MyStruct &orig) = delete;
    MyStruct& operator=(const MyStruct &orig) = delete;
}
```

````{note}
If using the defaults, the book recommends explicitly declaring the methods but adding ` = default` after both signatures instead of specifying a body. The reason is that the default is almost always wrong, so if you tack this on it makes it explicit to other that you intended this.

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
````

### Moving

There are two built-in mechanisms for moving in C++: the move constructor and move assignment. Moving is different from copying in that moving actually guts the insides (data) of one object and transfers it into another, leaving that object in an invalid state. If the scenario allows for it, moving is often times more efficient than copying.

A move constructor is a constructor that has a single parameter, an rvalue reference to an object of the same type. By default, classes are implicitly provided with a default move constructor if one hasn't been explicitly declared by the user. The move semantics of this default move constructor is to _copy_ each field rather than actually move anything, called a member-wise copy.

```c++
class MyStruct {
    ...

    MyStruct(MyStruct &&orig) noexcept {
        this->str_ptr = orig.str_ptr;
        this->max = orig.max;
        orig.str_ptr = nullptr; // mark orig object as invalid
        orig.max = -1; // mark orig object as invalid
    }
}

MyStruct a {};
MyStruct &&b = std::move(a);  // get rvalue reference for a
MyStruct c {b};               // move a into c (gut it into c) via the move constructor
// b is in an invalid state
```

In the example above, the move constructor has `noexcept` set to indicate that it will never throws an exception. Move constructors that can throw exceptions are problematic for the compiler to use. If a move constructor throws an exception, the source object will likely enter into an inconsistent state, meaning the program will likely be in an inconsistent state. As such, if the compiler sees that the move constructor can throw an exception, it'll prefer to copy it instead.

Similarly to the move constructor, move assignment is a method invoked when the assignment operator is used, called an operator overload. It has the same parameter list and it shouldn't throw exceptions either (`noexcept`), the only difference is that it return a reference to itself at the end.

```c++
class MyStruct {
    ...

    MyStruct& operator=(MyStruct &&orig) {
        if (this != &other) { // only do if assigning to self
            this->str_ptr = orig.str_ptr;
            this->max = orig.max;
            orig.str_ptr = nullptr; // mark orig object as invalid
            orig.max = -1; // mark orig object as invalid
        }
        return *this; // return self -- this should always be the case??
    }
}
```

````{note}
There's ambiguity around when the compiler generates default move/copy/destructor methods. It might be compiler specific. The book recommends that if you're using the defaults, always set them to `= default` (or do `= delete` to disallow them).

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
````

### Inheritance

In C++, a class inherits another class by, just after its name, appending a colon (:) followed by the name of the parent class.

```c++
class MyChild : MyParent {
};
```

Like in most other object oriented languages, a child class...

 * can access the non-private members of any of the classes it inherits.
 * is assignable to the type of any of the classes it inherits.

```c++
MyChild c {};
MyParent p {x}; // MyChild inherits from MyParent, meaning that it's assignable to MyParent
```

Unlike most other object oriented languages, methods aren't overridable by default. To be able to override a method in a child class, the base class declaring it needs to prepend `virtual` to the declaration, making it a virtual method. Similarly, any method that overrides a virtual method should append `override` before the body.

```{note}
Appending `override` isn't strictly required, but it's a hint that the compiler can use to prevent you from making a mistake (e.g. it sees `override` but what's being overridden isn't `virtual`). It's similar to Java's `@Override` annotation.
```

```c++
struct MyParent {
    virtual int virt_method() { ... }
    int non_virt_method() { ... }
};

struct MyChild : MyParent {
    virtual int virt_method() override { ... }
};
```

If the base class and child class have the exact same non-virtual method, which method gets called depends the type of the variable.

```c++
struct MyParent {
    virtual int virt_method() { ... }
    int non_virt_method(int a) { ... }
};

struct MyChild : MyParent {
    virtual int virt_method() override { ... }
    int non_virt_method(int a) { ... }
};


MyChild c {};
MyChild  &cref {x};
MyParent &pref {x};
cref.non_virt_method(0);  // calls MyChild::non_virt_method()
pref.non_virt_method(0);  // calls MyParent::non_virt_method() even though object is a MyChild
```

C++ chains constructor and destructor invocations appropriately as expected. The one caveat is that destructor, if not a virtual method, will use the method resolution mechanism described above: If the type of the variable doesn't match the object (variable type is the base class but object is not), the wrong destructor gets invoked, resulting in object potentially not cleaning up resources (e.g. closing file handles).

```c++
struct MyParent {
    virtual int v1() { ... };
    ~MyParent() { ... };
};

struct MyChild : MyParent {
    virtual int v1() { ... };
    ~MyChild() { ... };
};


MyParent *c = new MyChild{};
delete c;  // calls MyParent's destructor instead of MyChild's destructor
```

When inheritance is involved, it's almost always a good idea to enforce a virtual destructor. Since not having a virtual destructor sometimes makes sense (e.g. user determined that it's safe to omit it and as such omitted it to improve performance), the compiler won't produce a warning if it isn't virtual.

```c++
struct MyParent {
    virtual int v1() { ... };
    virtual ~MyParent() { ... };
};
```

### Interfaces

Interfaces and abstract classes are supported in C++, but not in the same way as other high-level languages. The C++ approach to interfaces is to explicitly mark certain methods as requiring an implementation. This is done by appending `= 0` to the method declaration.

```c++
struct MyParent {
    virtual int virt_method() = 0;
    int non_virt_method() = 0;
};
```

A method that is both a virtual method and requires an implementation is called a pure virtual method. A class that contains all pure virtual methods is called a pure virtual class.

```c++
struct MyParent {
    virtual int v1() = 0;
    virtual int v2() = 0;
    virtual ~MyParent() {};  // also okay to do   "virtual ~MyParent() = default"
};
```

As shown in the example above, a pure virtual class should have a virtual destructor. While not required, failing to do so means that the wrong destructor may get invoked if the type of the variable doesn't match the object (variable type is the base class but object is not), resulting in class resources being left open (e.g. file handles).

```{note}
See inheritance section for a more thorough explanation.
```

### Operator Overloading

C++ classes support operator overloading.

Operators are overload-able in two ways. To overload an operator the first way, introduce a method but instead of naming it, add the `operator` keyword followed by the operator being overloaded. The parameters and return type of the method need to match whatever types the operator is intended to deal with.

```c++
struct MyClass {
    ...

    // MyClass + int -- notice whitespace between 'operator' keyword and operator -- this is okay.
    MyClass operator +(int rhs) const {
        MyClass ret { this->value + x };
        return ret;
    };

    // MyClass + MyClass
    MyClass operator+(const MyClass &rhs) const {
        MyClass ret { this->value + rhs.value };
        return ret;
    }

    // MyClass += MyClass
    MyClass& operator+=(const MyClass &rhs) {
        this->value += x->value;
        return *this;
    }
};
```

To overload an operator the second way, introduce a function (not a method) using the `operator` keyword followed by the operator being overloaded. In the examples above, the left-hand side was the `this` pointer. When using this second way, a left-hand side needs to be explicitly provided as the first parameter while the right-hand side is the second argument.

```c++
// MyClass + int
MyClass operator+(const MyClass &lhs, int rhs) const {
    MyClass ret { lhs.value + x };
    return ret;
};

// MyClass + MyClass
MyClass operator+(const MyClass &lhs, const MyClass &rhs) const {
    MyClass ret { lhs.value + rhs.value };
    return ret;
}

// MyClass += MyClass
MyClass & operator+=(MyClass &rhs, const MyClass &rhs) {
    lhs.value += rhs.value;
    return lhs;
}
```

```{note}
Evidently the two ways described above aren't equivalent. The second way has some added benefits. See [here](https://stackoverflow.com/a/10958716).
```

Note how the `const` keyword is added to the method in cases where the operator shouldn't modify itself. Similarly, when the argument for a parameter shouldn't be changed, `const` is used on that parameter. `const`-ness depends on the scenario. For example, the second `operator+` requires two references to `const` types.

```c++
MyClass operator+(const MyClass &lhs, const MyClass &rhs) const {
    MyClass ret { lhs.value + rhs.value };
    return ret;
}
```

Those `const`s ensures that the operands aren't changed in the method. Imagine that you're performing `x = y + z`. It doesn't make sense for `y` or `z` to get modified.

The signature could have just as well been modified to be the types themselves rather than `const` references, in which case both the left-hand side and right-hand side would get copied on invocation of the method (modifications to copies don't matter).

```c++
MyClass operator+(MyClass lhs, MyClass rhs) const {
    MyClass ret { lhs.value + rhs.value };
    return ret;
}
```

```{note}
See [here](https://gist.github.com/beached/38a4ae52fcadfab68cb6de05403fa393) for a list of operators and their signatures (still incomplete).

There's also the option to create operators that allow for implicit type casting and explicit type casting. See the type casting section for more information.
```

# Templates

Templates are loosely similar to generics in other high-level languages such as Java. A template defines a class or function where some of the types and code are unknown, called template parameters. Each template parameter in a template either maps to a ...

 * a type (e.g. `int`).
 * an integral value available at compile-time (e.g. `5`).
 * floating point value available at compile-time (e.g. `5.5f`).
 * an enumeration value available at compile-time (e.g. `MyEnum::Value`).
 * object pointer type value available at compile-time (e.g. `&MyClass::MyStaticField`).
 * function pointer type value available at compile-time (e.g. `&MyClass::MyStaticMember`).
 * `std::nullptr_t` value available at compile-time (e.g. `nullptr`).

Templates are created using the `template` keyword, where the template parameters are a comma separated list sandwiched within angle brackets. When the user makes use of a template, its template parameters get substituted with what the user specified.

```c++
template <typename X, typename Y, typename Z, int N>
struct MyClass {
    X perform(Y &var1, Z &var2) {
        return (var1 + var2) * N;
    }
};
```

As shown above, each template parameter for a ...

* type substitution is prefixed with the keyword `typename`. The keyword `class` may be used instead of `typename`. The meaning is exactly the same (`typename` should be preferred).
* value substitution is prefixed with the type name.

To use a template, use it just as you would a non-template but provide substitutions (template instantiation). To instantiate a class template, use the class as if it were a normal class but immediately after the class name add in a comma separated list of template parameter substitutions sandwiched within angle brackets. These substitutions should be in the same order as the template parameters.

```c++
MyClass<float, int, int, 2> obj {}; // X = float, Y = int, Z = int, N = 2
float x = obj.perform(5, 3);
```

Declaring templated functions is done in the same manner as templated classes, and using templated functions is done similarly to templated classes: Use the function as if it were a normal function but immediately after the function name add in a common separated list of substitutions sandwiched within angle brackets.

```c++
// declare
template <typename X, typename Y, typename Z, int N>
X perform(Y &var1, Z &var2) {
    return (var1 + var2) * N;
}

// use
float x = perform<float, int, int, 2>(5, 3);
```

When the template parameters are for types only (not values), it's possible to leave out substitutions during usage. The compiler will deduce the types from the argument you pass in and substitute them automatically.

```c++
// declare
template <typename X, typename Y, typename Z>
X perform(Y &var1, Z &var2) {
    return var1 + var2;
}

// use
float x = perform(5, 3);  // template arguments omitted, deduced by compiler
```

It's possible to supply a default substitution for a template parameter by appending it with `=` followed by the substitution, called default template argument.

```c++
template <typename X, typename Y = long, typename Z = long>
X perform(Y &var1, Z &var2) {
    return var1 + var2;
}
```

```{note}
You would think that once a default is supplied, all other template parameters after it need a default as well. For whatever reason the compiler isn't erroring out when I do this.
```

Normally, C++ code is split into two files: a header file that contains declarations (e.g. function signatures) and a C++ file that contains definitions (e.g. function signatures with their bodies). When accessing C++ code that isn't local, typically only the declarations of that non-local code need to be included. The linker binds those non-local declarations to their definitions when it comes time to build the executable.

Templates work differently from Java generics in that the C++ compiler generates a new code for each unique set of substitutions it sees used (template instantiation). Doing so produces more code than if there was only one copy, but also ensures any performance optimizations unique to that specific set of substitutions. Also, because each usage of a template may result in newly generated code, that usage typically needs access to both the declaration and definition. The simplest way to handle this is to put the entirety of the template (both definition and declaration) into a header, which gets included into the same file as the usage.

## Concepts

In certain cases, a set of types substituted in for a template won't produce working code.

```c++
// declare
template <typename X, typename Y, typename Z>
X perform(Y &var1, Z &var2) {
    return var1 + var2;
}
```

In the example above, `X perform(Y &var1, Z &var2) { ... }` needs `Y` and `Z` to be types that support the plus operator (+) on each other (e.g. `int` and `short`). Setting them to types that don't support the plus operator typically causes cryptic compilation error, especially if the user is only making use of the template and isn't familiar with its innards.

To mitigate this problems, concept_TEMPLATEs may be provided within a template: A concept_TEMPLATE is a predicate, evaluated at compile-time (not runtime), to determine if the substituted types on some template have the properties needed to be used within it. Concept_TEMPLATEs themselves are templates where the `concept` keyword is used followed by a named expression that return a `bool`.

```c++
template <typename T1, typename T2, typename TR>
concept MyConcept = std::is_default_constructible<T1>::value
        && std::is_default_constructible<T2>::value
        && requires(T1 a, T2 b) {
            { a + b } -> std::same_as<TR>;
            { a * b } -> std::same_as<TR>;
            { std::hash<T1>{}(a) } -> std::convertible_to<std::size_t>;
            { std::hash<T2>{}(a) } -> std::convertible_to<std::size_t>;
        };
```

The concept_TEMPLATE above checks a combination of three types: `T1`, `T2`, and `TR`. The first two checks are done through functionality provided by the type_traits header. In the example above, `std::is_default_constructible` provides a compile-time check to ensure the types `T1` and `T2` both have a default initializer (e.g. default constructor). Examples of other checks baked provided by the type_traits header (and concept_NORMs header):

 * `std::is_signed` - ensures a type is signed.
 * `std::is_unsigned` - ensures a type is unsigned.
 * `std::is_integral` - ensures a type is an integer (e.g. `short int`, `int`, `unsigned long long int`, etc..)
 * `std::is_pod` - ensures a type is a POD.
 * `std::is_fundamental` - ensures a type is a fundamental type.
 * `std::is_abstract` - ensures a type is an abstract class (has at least one pure virtual function).
 * `std::is_copy_constructible` - ensures type has a copy constructor.
 * `std::is_copy_assignable` - ensures type has copy assignment.
 * `std::is_move_constructible` - ensures type has a move constructor.
 * `std::is_nothrow_move_constructible` - ensures type has a move constructor that never throws an exception (`noexcept`).
 * `std::is_move_assignable` - ensures type has move assignment.

The remaining checks are done through a `requires` clause, which lists out the required set of expressions the substituted types must support and the resulting type of each of those expressions. The example above lists that types `T1` and `T2` are ...

 1. addable, returning an object of type `TR`.
 1. multiply-able, returning an object of type `TR`.
 1. hashable (when passed into `std::hash()`, returns an object that's convertible to `size_t`).

Each item in the list has the syntax `{ EXPRESSION } -> RESULT`, where the result is wrapped with functionality from the concept_NORMs header. This functionality describes how the result of the expression should behave. In the example above, ...

 * `std::same_as<TR>` means that the expression should return the exact type as specified by `TR`.
 * `std::convertible_to<std::size_t>` means that the expression should return a type can implicitly convert to `std::size_t` (e.g. a `short` can implicitly convert to an `int` without requiring any kind of casting).

```{note}
The book says that these are / are related to "type functions". I can't find much information on this or how to create new "type functions".
```

Use the `requires` keyword immediately after the template to target a set of template parameters to a concept_TEMPLATE.

```c++
template <typename T1, typename T2>
    requires MyConcept<T1, T2, T1>  // refers to the concept defined in the example above
T1 add_and_multiply(T1 &var1, T2 &var2) {
    return (var1 + var2) * var2;
}
```

Concept_TEMPLATE may also be directly embedded into the template itself. 

```c++
template <typename T1, typename T2>
    requires std::is_default_constructible<T1>::value   // same as above, but "MyConcept<T1, T2, T1>" has been embedded
            && std::is_default_constructible<T2>::value
            && requires(T1 a, T2 b) {
                { a + b } -> std::same_as<T1>;
                { a * b } -> std::same_as<T!>;
                { std::hash<T1>{}(a) } -> std::convertible_to<std::size_t>;
                { std::hash<T2>{}(a) } -> std::convertible_to<std::size_t>;
            };
T1 add_and_multiply(T1 &var1, T2 &var2) {
    return (var1 + var2) * var2;
}
```

If a concept_TEMPLATE only checks a single type, it's possible to use it just by substituting its name in place of the `typename` / `class` for the template parameter that requires it (as opposed to using `requires` shown above).

```c++
// concept
template <typename T>
concept SingleTypeConcept = requires(T a, T b) {
            { a + b } -> std::same_as<T>;
            { a * b } -> std::same_as<T>;
        };

// usage of concept
template <SingleTypeConcept X>  // this line is updated -- "typename T" replaced with "SingleTypeConcept T"
X add_and_multiply(X &var1, X &var2) {
    return (var1 + var2) * var2;
}
```

## Variadic

A variadic function is one that takes in a variable number of arguments, sometimes called varargs in other languages. A template can be made variadic by placing a final template parameter with `...` preceding the name, where this template parameter is referred to as parameter pack.

One common use-case for parameter packs is invoking functions where the parameter list isn't known beforehand.

```c++
template <typename X, typename... R>
X create(R... args) {
    return X {args...};
}
```

Another less common use-case is specifying the base classes to inherit from (multiple inheritance).

```c++
template <typename X, typename... R>
struct X : R... {
    X(const R&... args) : R(args)... { // member initializer list calls constructors of base class
    }
}
```

Another less common use-case is to apply an repeatedly apply some operator or function.

```c++
template<typename T>
T sum(T t) {
    return t;
}

template<typename T, typename... R>
T sum(const T& first, R... rest) {
    return sum(first) + sum(rest...);
}
```

Parameter packs are used internally within C++'s implementation of analogues to Python's tuples and zip: `std::pair`, `std::tuple`, and `std::zip`.

```{note}
Examples adapted from [here](https://crascit.com/2015/03/21/practical-uses-for-variadic-templates/).
```

## Specialization

Given a specific set of substitutions for the template parameters of a template, a template specialization is code that overrides the template generated code. Often times template specializations are introduced because they're more memory or computationally efficient than the standard template generated code. The classic example is a template that holds on to an array. Most C++ implementations represent a `bool` as a single byte, however it's more compact to store an array of `bool`s as a set of bits.

Declare a template specialization with the `template` keyword but without any template parameters (empty angle brackets). The class or function that follows should list out substitutions after its name and the code within it should be real (non-templated).

```c++
// template
template<typename T>
T sum(T a, T b) {
    return a + b;
}

// template specialization for bool: bit-wise or
template<>
bool sum<bool>(bool a, bool b) {
    return a | b;
}
```

Template specialization doesn't have to substitute all template parameters. When a template specialization only provides substitutes some of its template parameters, leaving other template parameters as-is or partially refined, it's called a partial template specialization.

```c++
// template
template<typename R, typename T>
struct MyClass {
    R sum(T a, T b) {
        return a + b;
    }
};

// template specialization for pointers of unknown type: already return false
template<typename X>
struct MyClass<bool, X*> {
    bool sum(X * a, X* b) {
        return false;
    }
};
```

```{note}
Partial template specializations for functions isn't supported (yet?). See [here](https://stackoverflow.com/a/8061522).
```

In certain cases, the compiler is able to deduce the types for a specialization from its usage, meaning explicitly listing substitutions after the name may not be required.

```c++
// first example without explicitly listing out substitutions
template<>
bool sum(bool a, bool b) {  // type removed after name: "sum<bool>" to just "sum"
    return a | b;
}
```

# Constant Types

For types, any part of that type can be made unmodifiable by adding a `const` immediately after it.

```c++
int a {5};                // a is changeable   -- set to 5
int const x {a};          // x is unchangeable -- set to 5 (value in a)
int * const y {&a};       // y is an unchangeable pointer to a changeable int -- set to a (points to a)
int const * const z {&x}; // z is an unchangeable pointer to a unchangeable int -- set to x (points to x)
```

The simplest way to interpret `const`-ness of a type is to read it from right-to-left.

```{svgbob}
 "int const"   "*"   "* const"
'-----+-----' '-+-' '----+----'
      |         |        |
      |         |        '-- "an unmodifiable pointer to"
      |         '----------- "a pointer to"
      '--------------------- "an unmodifiable int"
                  
"int const * * const = An unmodifiable pointer to a pointer to an unmodifiable int" 
```

One caveat to the above is that a type beginning with `const` is equivalent to the first part of that type having `const` applied on it.

```c++
const int x {5};  // equivalent to int const x {5}
```

All of the examples above were for fundamental types. Appending a `const` on a class type works exactly the same way: None of its fields are modifiable ever, even by its own methods.

```c++
struct MyStruct {
    int x {5}
};

MyStruct const inst {};
inst.x = 5;  // compiler error
```

# Constant Expressions

A constant expression is an expression that gets evaluated at compile-time, such that any invocation of it gets swapped out for the result computed at compile-time. It comes in two forms: variable and function.

A constant expression variable requires using `constexpr` instead of `const`. The difference between a `const` variable and `constexpr` variable is that the former only guarantees the variable is unmodifiable. It doesn't actually guarantee that the expression within is evaluated at compile-time.

```c++
const int x {5 + 5};      // COULD BE evaluated at run-time or compule-time, but guaranteed to be unmodifiable
constexpr int y {5 + 5};  // MUST BE evaluated at compile-time and guaranteed to be unmodifiable
```

Similarly, a constant expression function requires prefixing `constexpr` to a function.

```c++
constexpr unsigned int fibonacci(unsigned int n) {
    if (n == 0) {
        return 0;
    } else if (n == 1 || n == 2) {
        return 1;
    } else {
        return fibonacci(n-1) + fibonacci(n-2);
    }
}

int x {fibonacci(7)}; // at compile-time, fibonacci(7) is executed and its return value substituted into the initializer
```

The restrictions on constant expressions are vast. At a high-level, a constant expression is only allowed inputs and outputs that are literal types:

 * **Scalar**: Floating point types, integral types, pointer types, enumeration types, `std::nullptr_t`, etc..
 * **Reference**
 * **Array**: Every element must be a literal.
 * **Class**: Constructor must be a constant expression. Non-static fields initializers using braced initialization, equals initialization, or brace-plus-equals initialization must use constant expressions. The destructor must be a trivial destructor (non-virtual, does nothing, and all base class destructors do nothing).
 * **Union**: Must have at least one non-static member that is a literal type.

```{note}
The rules here are vast and complicated. The above might not be entirely correct, may be missing some conditions, or may not cover certain aspects. In the type_traits header, there's a function called `std::is_literal_type` that can be used to test if a type is a literal type.
```

Constant expressions help with reducing the use of hard coded numbers whose origins are obtuse, called magic numbers. A constant expression uses the computation to get to that obtuse magic number rather than the number itself, meaning its easier to understand and requires less effort to tweak (via the parameters of the constant expression).

# Constant Methods

For methods of a class, a `const` after the declaration indicates that the class's fields won't be modified (read-only). This is a deep check rather than a shallow check, meaning that the entire call graph is considered when checking for modification.

```c++
struct Inner {
    int x = 5;
    int y = 6;
    void change(int n) {
        x = n;
    }
};

struct X {
    int a = 0;
    Inner inner;
    void test1() const {
        a = 5;  // NOT okay -- no mutation allowed
    }
    void test2() const {
        inner.x = 15; // NOT okay -- no mutation allowed, even though this is deeper down
    }
    void test3() const {
        inner.change(15); // NOT okay -- method being invoked must be const (otherwise mutation might happen)
    }
};
```

# Volatile Types

```{note}
Unlike in Java, The `volatile` keyword in C++ is _not_ used for thread-safety.
```

Adding the keyword `volatile` before a type makes it immune to compiler optimizations such as operation re-ordering and removal. Mutations and accesses, no matter how irrelevant they may seem, are kept in-place and in-order by the compiler.

```c++
int f(int a) {
    int x {a};
    x = 6;
    int y {x};
    int x {y};
    return x; // at this point, x is always 6
}
```

A compiler might be able to deduce that the function above always returns 6, and as such may replace the operations it performs with simply just returning 6. Adding `volatile` to the type of the variable prevents this from happening.

```c++
int f(int a) {
    volatile int x {a};  // marked as volatile
    x = 6;
    int y {x};
    int x {y};
    return x;
}
```

Using `volatile` is important when working with embedded devices, where platform-specific memory locations often need to be accessed in a specific order / at specific intervals in seemingly useless ways (e.g. kicking a watchdog by writing 0 to a memory location but never reading that memory location).

# Volatile Methods

For methods of a class, a `volatile` after the declaration indicates that all fields should be treated as `volatile` (access won't be optimized away or re-ordered). This is a deep check rather than a shallow check, meaning that the entire call graph requires `volatile`.

```c++
struct Inner {
    int x {5};
    int y {6};
    void change(int n) volatile {
        x = n;
        x = n;
        x = n;
    }
};

struct X {
    int a {0};
    int b {0};
    void test() volatile {
        a = b;
        b = a;
        inner.change(15); 
    }
};
```

# Type Conversions

Similar to most other languages (e.g. Java and Python), C++ offers ways of type casting: implicit and explicit.

 * An implicit type conversion is when an object of a certain type is converted (cast) to another type automatically based on its usage.

   ```c++
   int x {5};
   long y {x};  // int to long
   ```

 * An explicit type conversion is when an object of a certain type is converted (cast) to another type explicitly in code.

   ```c++
   long x {5L};
   int y {static_cast<int>(x)};   // long to int
   ```

Unlike those other languages, ...

 * implicit type conversions are more involved and error-prone.
 * explicit type conversions are done through multiple mechanisms.

The following subsections detail the type conversions.

## Implicit Type Conversions

An implicit type conversion is when an object of a certain type is converted (cast) automatically, without code explicitly changing the object to a different type. For example, `long x {1}` implicitly converts the `int` literal in the initializer to a `long`.

The most common types of implicit conversions are ...

 * when a pointer of a certain type gets implicitly converted to a void pointer (e.g. `int *` to `void *`).
 * when a numeric type gets converted to another numeric type via promotion rules (e.g. `int` to `float`).
 * when a numeric type gets converted to a bool type (e.g. `0` to `false`)

Depending on the operation performed or how an object is initialized, the results of an implicit conversion may do something specific to that platform and/or compiler implementation.

| Source Type    | Destination Type | Behaviour                                                                                                                                         |
|----------------|------------------|---------------------------------------------------------------------------------------------------------------------------------------------------|
| Integer        | Floating Point   | Implementation-specific behaviour if can't fit in destination (speculation).                                                                      |
| Floating Point | Integer          | Rounded to integer (speculation - how?), implementation-specific behaviour if can't fit in destination (speculation).                             |
| Integer        | Integer          | Signed destination and value can't fit, implementation-specific behaviour. Unsigned destination and value can't fit, truncates higher-order bits. |
| Floating Point | Floating Point   | Implementation-specific behaviour if value can't fit in destination.                                                                              |
| Any Numeric    | Boolean          | 0 converts to `false`, otherwise `true`.                                                                                                          |
| Any Pointer    | Boolean          | `nullptr` converts to `false`, otherwise `true`.                                                                                                  |

```{note}
The book recommends to always use braced initialization because when you do, the compiler produces warnings about types not fitting. However, those warnings don't seem to cover everything, at least that's the impression I get from what I've tried.
```

## Explicit Type Conversions

An explicit type conversion is the opposite of an implicit type conversion. It's when an object of a certain type is explicitly converted (cast) to another type in code. Explicit type conversions come in two forms:

 * Named conversions are the official way to cast in C++.
 * C-style casts are the legacy way to cast in C++.

Named conversions should be preferred over C-style casts. Any C-style cast can be performed through a named conversion.

### Named Conversions

Named conversion functions are a set of (seemingly templated) functions to convert an object's types. These functions provides safety mechanisms that aren't available in other older ways of casting.

 * `const_cast` removes the `const` modifier from an object's type.
   
   ```c++
   void func(const MyType &t) {
       T &moddable_t = const_cast<MyType &>(t);
   }
   ```

   Performing this type of conversion should only be done in extreme situations since it breaks contracts.

 * `static_cast` forces the reverse of an implicit conversion.

   ```c++
   int a[] {1,2,3,4};
   int *b = a;  // ok, implicit conversion (decay to pointer)
   void *c = b; // ok, implicit conversion
   int *d = c;  // error, can't go in reverse
   int *e = static_cast<int *>(c); // ok
   ```

   In the above example, a `uint32_t *` implicitly converts to `void *`, but not the reverse. A `static_cast` makes going in reverse possible. However, that doesn't mean it's always safe to do. For example, `uint32_t` reads may need to be aligned to 4 byte boundaries on certain platforms. If the `void *` was arbitrary data (e.g. coming in over a network), it might cause a crash to just treat it as a `uint32_t *` and start reading.

   ```{note}
   Why does a `uint32_t*` implicitly convert to a `void *`? Recall that `void *` just means "pointer to something unknown", which is something the language is okay automatically / implicitly converting.
   ```

 * `reinterpret_cast` forces a reinterpretation of an object into an entirely different type.

   ```c++
   int a[] {1,2,3,4};
   int *b = a;   // ok, implicit conversion (decay to pointer)
   short *c = b; // error, you can't convert from an int* to a short* (not even with a static_cast because it's not an implicit conversion)
   short *d = reinterpret_cast<int *>;  // ok
   ```

 * `narrow_cast` is similar to `static_cast` for numerics, except it ensures that no information loss occurred.

   ```c++
   uint32_t a = 70000;                     // ok
   uint16_t b = static_cast<uint16_t>(a);  // ok, but since uint16_t has a max of65535, this object is mangled
   uint16_t c = narrow_cast<uint16_t>(a);  // runtime exception, narrow_cast sees that the object will be mangled
   ```

   ```{note}
   Is this part of the standard? The book seems to give the code for `narrow_cast` and looking online it looks like people have their own implementations?
   ```

### C-style Casts

C-style casts are similar to casts seen in Java. The type is bracketed before whatever is being evaluated.

```c++
int x = (int) 9999999999L;
```

The problem with C-style casts are that they don't provide the same safety mechanisms as named conversions do (e.g. inadvertently strip the `const`-ness). Named conversions provide these safety mechanisms and as such should be preferred over C-style casts. Any C-style cast can be performed using a named conversion.

## Custom Type Conversions

C++ classes support both implicit type conversions and explicit type conversions via operator overloading. Implicit type conversions are represented as operator overload methods where the name of the operator being overloaded is the destination type and the return type is omitted.

```c++
struct MyClass {
    ...
    operator int() const {
        return this-> value / 42;
    }
};
...
MyClass cls {};
int x = cls; // triggers operator overload method
```

Explicit type conversions are enabled the same way as implicit type conversions, except the overload method is preceded by the `explicit` keyword. The `explicit` keyword makes it so that conversion to that type requires a `static_cast`

```c++
struct MyClass {
    ...
    explicit operator int() const {
        return this-> value / 42;
    }
};
...
MyClass cls {};
int x = static_cast<int>(cls);  // static_cast required to trigger operator overload method
```

```{note}
The book recommends not preferring explicit over implicit because implicit is a source for confusion.

Do these still qualify as operator overloads? Return types should be there.
```

# Type Deduction

The keyword `auto` may be used during a variable declaration to deduce the resulting type of that variable from whatever it's being initialized with.

```c++
auto a { 1 };  // int
auto b { 1L }; // long
auto c { &a }; // int *
auto d { *c }; // int
auto &e { a }; // int &  <-- THIS IS A SPECIAL CASE. YOU ALWAYS NEED TO USE auto& FOR REFERENCES
```

Note that the last variable in the example above explicitly the ampersand (&) to declare e as a reference type. This is required because reference initialization works the same way as normal initialization (`auto` can't disambiguate).

# Object Lifecycle

In C++, an object is a region of memory that has a type and a value (e.g. a class instance, an integer, a pointer to an integer, etc..). Contrary to other more high-level languages (e.g. Java), C++ objects aren't exclusive to classes (e.g. an boolean is an object).

An object's life cycle passes through the following stages:

1. memory allocated
2. constructor invoked
3. destructor invoked
4. memory deallocated

The storage duration of an object starts from when its memory is allocated and ends when that memory is deallocated. An object's lifetime, on the other hand, starts when its constructor _completes_ (meaning the constructor finishes) and ends when its destructor is _invoked_ (meaning when the destructor starts).

```{svgbob}
.------------------------------------------------.
|           "OBJECT STORAGE DURATION"            |
|                                                |
| "1. allocation"                                |
|                                                |
| "2. constructor invocation started"            |
|                                                |
|  .----------------------------------------.    |
|  |           "OBJECT LIFETIME"            |    |
|  |                                        |    |
|  | "3. constructor invocation finished"   |    |
|  |                                        |    |
|  | "4. destructor invocation started"     |    |
|  |                                        |    |
|  | "5. destructor invocation finished"    |    |
|  '----------------------------------------'    |
|                                                |
| "6. deallocation"                              |
|                                                |
'------------------------------------------------'
```

Since C++ doesn't have a garbage collector performing cleanup like other high-level languages, it's the user's responsibility to ensure how object lifetimes. The user is responsible for knowing when objects should be destroyed and ensuring that objects are only accessed within their lifetime.

The typical storage durations supported by C++ are...

 * automatic storage duration - scoped to duration of some function within the program.
 * static storage duration - scoped to the entire duration of the program.
 * thread storage duration - scoped to the entire duration of a thread in the program.
 * dynamic storage duration - allocated and deallocated on request of the user.

# Static Objects

By default, an object declared within a function is said to be an automatic object. Automatic objects have automatic storage durations: start at the beginning of the block and finish at the end of the block. When the keyword `static` (or `extern` in some cases) is added to the declaration, the storage duration of the function changes.

At global scope, if an object is declared as `static` or `extern`, storage duration of the object spans the entire duration of the program. The difference between the two is essentially just visibility:

 * `static` makes it so it's accessible to only the translation unit it's declared in.
 * `extern` makes it so it's accessible to other translation units as well as the translation unit it's declared in.

```c++
static int a = 0; // static variable
extern int b = 1; // static variable (accessible outside translation unit)
```

At function scope, the storage duration of objects declared as `static` starts at the first invocation of that function and ends when the program exits.

```c++
int f1() {
    static int z = 0; // static variable
    z += 1;
    return z;
}
```

At class level, the storage duration of a member (field or method) declared as `static` is essentially the same as if it were declared at global scope (they aren't bound to an individual instance of the class the same way a normal field or method is). The only differences are that the static member is accessed on the class itself using the scoped resolution operator (::) and that static members that are fields must be initialized at global scope.

```c++
struct X {
    static int m;         // static member (field initialized at end)
    static int f1() {     // static member (method)
        m += 1;
        return m;
    }
};

X::m = 0;                // initialize static member
```

If the `thread_local` modifier is added before `static` (or `extern`), each thread gets its own copy of the object. That is, the storage duration essentially gets changed to when the thread starts and ends.

`thread_local static` can be shortened to just `thread_local` (it's assumed to be static).

```c++
static int a = 0;
thread_local static int b = 1;
thread_local extern int c = 2;
```

# Dynamic Objects

An object can be created in an ad-hoc manner, such that its storage duration is entirely controlled by the user. The operator ...

 * `new` allocates a new object and calling its the constructor.
 * `delete` calls the destructor of some object and deallocates it.

Both keywords work with pointers: `new` returns a pointer while `delete` requires a pointer. To create a new object, use `new` followed by the type.

```c++
int * ptr = new int;
*ptr = 0;
delete ptr;
```

Objects may be initialized directly within the `new` invocation just as if it were an automatic object initialization. The only caveat is that equals initialization and brace-plus-equals initialization won't work because the equal sign is already being used during `new` (speculation -- it doesn't work but I don't know the exact reason). As such, braced initialization is the best way to initialize a dynamic object.

```c++
int * ptr = new int {0}; // initialize to 0
delete ptr;
```

The same process can be used to create an array of objects. Unlike automatic object arrays, dynamic arrays don't have a constant size array lengths restriction.. However, the return value `new` will decay from an array type to a pointer type.

When deleting a dynamic object array, square brackets need to be appended to `delete` operator: `delete[]`. Doing so ensures that the destructor for each object in the array gets invoked before deallocation.

```c++
int * ptr = new int[len];  // len is some non-constant positive integer, decayed to pointer type because array length can be non-constant.
delete[] ptr;
```

Braced initialization may be used when declaring dynamic arrays so long as the size of the array is at least the size of the initialization list.

```c++
int * ptr1 = new int[10] {1,2,3};  // initialize the first 3 elems of a 10 elem array
int * ptr2 = new int[2] {1,2,3};   // throws exception  (size too small for initializer list)
int * ptr3 = new int[n] {1,2,3};   // okay -- so long as n >= 3
delete[] ptr1;
delete[] ptr2;
delete[] ptr3;
```

By default, dynamic objects are stored on a block of memory called the heap, also sometimes referred to as the free store.

```{note}
See operator overloading section to see how the `new` and `delete` operators may be overridden to customize where and how a specific type gets stored.

The `new` and `delete` operators may also be overridden globally rather than per-type. See the new header.
```

# Object Size

`sizeof` is a _unary operator_ that returns the size of its operand in bytes as a `size_t` type. If the operand is a ...

* data type or a variable, it'll return the number of bytes needed to hold that type. For example, ...

  * `sizeof char` is guaranteed to be 1.
  * `sizeof (char &)` is guaranteed to be 1.
  * `sizeof (char *)` is platform dependant, typically either 4 or 8.
  * `char * x = "hi"; sizeof x` is equivalent to `sizeof (char *)` (see above).

* an expression such as a struct literal, array literal, or string literal, it'll return the number of bytes needed to hold it. For example, ...

 * `sizeof "hi"` is 3 (added 1 for the null terminator at the end)
 * `sizeof { 5, 5, 4 }` is platform dependent, typically either 12 or 24.
 * `sizeof (int[3])` is platform dependent, typically either 12 or 24.
 * `x = int[n]; sizeof x` is invalid C++ (variable length arrays allocated on stack are not allowed in C++).

In other words, `sizeof` returns the size of things known at compile-time. If a variable is passed in, it outputs the size of the data type. For example, if the data type is a struct of type `MyStruct`, it'll return the number of bytes used to store a `MyStruct`. However, if the data type is a pointer to `MyStruct`, it'll return the number of bytes to hold that pointer. That is, you can't use it to get the size of something like a dynamically allocated array of integers.

In certain cases, the compiler may add padding to objects (e.g. byte boundary alignments or performance reasons), meaning that the size returned by `sizeof` for an object shouldn't be used to make inferences about the characteristics of that object. For example, a `long double` may get reported as being 16 bytes, but that doesn't necessarily mean that a `long double` is a 128-bit quad floating point. It could be that only 12 of those bytes are used to represent the floating point number while the remainder is just padding for alignment reasons. 

```{note}
As shown in the examples above, the `sizeof` a C++ reference is equivalent to the raw size. For example, `sizeof char == sizeof (char &)`.
```

```{note}
The last example is valid in C99 (called a VLA -- variable length array) but not C++. The reason is C++ has std::vector and std::array that give you basically the same thing as variable arrays.

In C, where VLAs are allowed, doing a `sizeof` on a VLA is undefined.
```

Remember that `sizeof` is a _unary operator_, similar to how the negative sign is a unary operator that negates whatever is to the right of it. People usually structure its usage in code as if it were a function (e.g. `sizeof(x)` vs `sizeof x`). This sometimes causes confusion for people coming from other languages.

# Exceptions

C++ exceptions work similarly to exceptions in other languages, except that there is no `finally` block. The idea behind this is that resources should be bound to an object's lifetime (destructor). As the call stack unwinds and the automatic objects that each function owns are destroyed, the destructors of those objects should be cleaning up any resources that would have been cleaned up by the `finally` block. This concept_NORM is referred to as resource acquisition is initialization (RAII).

```{note}
What does accordingly mean? For example, wrap the dynamically allocated object in a class where allocation happens in the constructor / deallocation happens in the destructor. An automatic object of that class type will cleanup properly when the function exits.
```

To throw an exception, use the `throw` keyword followed by the object to throw. Most object types are throwable, but thrown objects are typically limited to types either in or derived from those in the stdexcept header.

```c++
void no_negatives_check(int x) {
    if (x < 0) {
        throw std::runtime_error { "no negatives" };
    }
}
```

Similar to Java and Python, C++ provides a standard set of exceptions in stdexcept complete with a hierarchy.

```{svgbob}
"std:exception"
     |
     +-- "std:bad_alloc"
     |
     +-- "std:bad_cast"
     |
     +-- "std:bad_typeid"
     |
     +-- "std:bad_exception"
     |
     +-- "std:logic_failure"
     |        |
     |        +------------------------------+-- "std:domain_error"
     |                                       |
     +-- "std:runtime_error"                 +-- "std:invalid_argument"
              |                              |
              +-- "std:overflow_error"       +-- "std:length_error"
              |                              |
              +-- "std:range_error"          +-- "std:out_of_range"
              |
              +-- "std:underflow_error"
```

To catch a exception potentially being thrown, wrap code in a try-catch block. Typical inheritance rules apply when catching an exception. For example, catching a `std:runtime_error` type will also catch anything that extends from it as well (e.g. `std:overflow_error`).

```c++
try {
    no_negatives_check(55);
    no_negatives_check(0);
    no_negatives_check(-1); // will throw an exception
} catch (const std::runtime_error &e) {
    // do something
}
```

To catch any exception regardless of type, use `...`.

```c++
try {
    no_negatives_check(-1); // will throw an exception
} catch (...) {
    // do something, note the exception object is not accessible here
}
```

Multiple catches may exist in the same try-catch block.

```c++
try {
    no_negatives_check(-1); // will throw an exception
} catch (const std::range_error &e) {
    // do something
} catch (const std::runtime_error &e) {
    // do something -- this block will get chosen
} catch (const std::exception &e) {
    // do something
} catch (...) {
    // do something, note the exception object is not accessible here
}
```

In certain cases, it'll be impossible for a function to throw an exception. Either the function (and the functions it calls into) never throws an exception or the conditions imposed by the function make it impossible for any exception to be thrown. In such cases, a function may be marked with the `noexcept` keyword. This keyword allows the compiler to perform certain optimizations that it otherwise wouldn't have been able to, but it doesn't necessarily mean that the compiler will check to ensure an exception can't be thrown.

```c++
int add(int a, int b) noexcept {
    return a + b;
}
```

```{note}
The book mentions this is documented in "Item 16 of Effective Modern C++ by Scott Meyers". It goes on to say that, unless specified otherwise, the compiler assumes move constructors / move-assignment operators can thrown an exception if they try to allocate memory but the system doesn't have any. This prevents it from making certain optimizations.
```

Treat any destructor as if it were marked with `noexcept`. That is, an exception should never be thrown in a destructor. When an exception gets thrown, the call stack unwinds. As each function exits, the destructors for automatic variables of that function get invoked. Another exception getting thrown while one is already in flight means two exceptions would be in flight, which isn't supported.

# Unpacking

Structured binding declaration is a C++ language feature similar to Python's unpacking of lists and tuples. Given an array or a class, the values contained within are unpackable to individual variables.

```c++
// array example
int x[] = {1,2};
auto [a, b] = x;  // a is a copy of x[0], b is a copy of x[1]
auto &[c, d] = x; // c is a REFERENCE to a[0], d is a REFERENCE to a[1]

// class example
struct MyStruct {
    int count;
    bool flag;
};
MyStruct y {5,true};
auto [i, j] = y;  // i is a copy of y.count, b is a copy of y.flag
auto &[k, l] = y; // k is a REFERENCE to y.count, l is a REFERENCE to y.flag
```

# Expression Categories

Value categories are a classification of expressions in C++. At their core, these categories are used for determining when objects get _moved_ vs copied, where a move means that the guts of the object and scooped out and transferred to another object.

```{svgbob}
          lvalue
        /
glvalue 
        \
          xvalue
        /
 rvalue
        \
          prvalue

" * glvalue is either an lvalue or an xvalue"
" * rvalue is either a prvalue or an xvalue"
```

This is explicitly categorizing expressions, not objects, variables or types. Each expression is categorized as either an lvalue, xvalue, or prvalue.

A prvalue is an expression that generates some transient result, where that result is typically either used for assignment or passed into a function invocation by _moving_ it.

```c++
int a = 0; // move -- 0 is being generated and MOVED into a (the expression 0 is a prvalue)
//      ^
//      |
//   rvalue

int b = a; // copy -- a already exists and its being COPIED into b (the expression a is NOT a prvalue)
```

In essence, the way to think of a prvalue is that its an expression that meets the following 3 conditions ...

1. can't have the address-of operator used on it.

   ```c++
   MyStruct* a = &MyStruct(true); // error -- right-hand expression is transient, not a var that you can get the address of   
   int* b = &(5)                  // error -- right-hand expression is a literal, not a var that you can get the address of
   int* c = &get_int()            // error -- right-hand expression is the return val of function, not a var that you can get the address of
   ```   

2. can have its guts be scooped out and moved into something else.

   ```c++
   x = 55 + y;  // expression 55 + y is evaluated and the result is MOVED into x (its guts are scooped out and moved into x)
   ```

3. doesn't persist once the expression has been executed.

   ```c++
   x = 55 + y;  // expression 55 + y is a prvalue -- doesn't persist after this line (its not something you can access)
   x = c;       // expression c is NOT a prvalue -- DOES persist after this line (it IS something you can keep accessing)
   ```

```{note}
The name prvalue is short for pure right value. It's called that because prvalue expressions are usually found on the right side of an assignment.
```

An lvalue is an expression is the opposite of a prvalue. An lvalue expression CAN use the address-of operator (opposite of point 1 above), it CANNOT have guts scooped out and moved into something else (opposite of point 2 above), and it DOES persist (opposite of point 3 above). The typical example of an lvalue is an expression that's solely a variable name or function name.

```c++
x = y;  // both x and y are lvalue
x = 0;  // x is an lvalue while 0 is a prvalue
```

The key takeaway with lvalues is that you might be able to _copy_ over its contents to something else, but you can't scoop out its guts and _move_ it over to something different. Doing so would make whatever that lvalue points to no longer usable.

```{note}
The name xvalue is short for left value. It's called that because lvalue expressions are usually found on the left side of an assignment.
```

An xvalue is an expression which can have the address-of operator used on it but also _can be moved_. The general idea with an xvalue expression is that the object it represents is nearing the end of its lifetime and as such moving its guts is fine. There are a very limited number of cases where this happens or is required.

```c++
MyObject a {};
MyObject &&b = std::move(a);  // get rvalue reference
MyObject c {b};               // move a into c (gut it into c) via the move constructor
// b is in an invalid state
```

```{note}
The example above is using features that haven't been introduced yet (std::move, rvalue references, move constructor). Just ignore it if you don't know those pieces yet. They're explained in other sections.
```

This is in contrast to lvalue expressions, which the address-of operator is usable on but _CANNOT be moved_. If the address-of operator works on it, regardless of if it's moveable (xvalue) or not (lvalue), it's called a glvalue.

```{svgbob}
          lvalue "(addressable but CAN'T be gutted)"
         /
        /
glvalue "(addressable)" 
        \
         \
          xvalue "(addressable and can be gutted)"
```

Similarly, if it's an expression that can be _moved_ (gutted), its called an rvalue regardless of if the address-of operator can be used on it or not.

```{svgbob}
          xvalue   "(can be gutted and addressable)"
        /
       /
 rvalue "(can be gutted)"
       \
        \
          prvalue  "(can be gutted but NOT addressable)"
```

```{note}
See [here](http://zhaoyan.website/xinzhi/cpp/html/cppsu32.html) for what I used to clarify what's going on here.
```

# Terminology

 * `{bm} processor/(preprocessor|translation unit)/i` - A tool that takes in a C++ source file and performs basic manipulation on it to produce what's called a translation unit.

   ```{svgbob}
   .--------------------.
   |  "C++ source file" +--+
   '--------------------'  |
                           | "preprocessor (1 to 1)"
                           |  .--------------------.
                           +--+ "translation unit" +--+
                              '--------------------'  |
                                                      | "compiler (1 to 1)"
                                                      |  .---------------.
                                                      +--+ "object file" +--+
                                                         '---------------'  |
                                                                            | "linker (1+ to 1)"
                                                                            |  .--------------.
                                                                            +--+ "executable" |
                                                                               '--------------'
   ```

 * `{bm} compiler/(compiler|object file|object code)/i` - A tool that takes in a translation unit to produce an intermediary format called an object file.

   ```{svgbob}
   .--------------------.
   |  "C++ source file" +--+
   '--------------------'  |
                           | "preprocessor (1 to 1)"
                           |  .--------------------.
                           +--+ "translation unit" +--+
                              '--------------------'  |
                                                      | "compiler (1 to 1)"
                                                      |  .---------------.
                                                      +--+ "object file" +--+
                                                         '---------------'  |
                                                                            | "linker (1+ to 1)"
                                                                            |  .--------------.
                                                                            +--+ "executable" |
                                                                               '--------------'
   ```

 * `{bm} linker/(linker|executable)/i` - A tool that takes multiple object files to produce an executable. Linkers are are also responsible for finding libraries used by the program and integrating them into the executable.

   ```{svgbob}
   .--------------------.
   |  "C++ source file" +--+
   '--------------------'  |
                           | "preprocessor (1 to 1)"
                           |  .--------------------.
                           +--+ "translation unit" +--+
                              '--------------------'  |
                                                      | "compiler (1 to 1)"
                                                      |  .---------------.
                                                      +--+ "object file" +--+
                                                         '---------------'  |
                                                                            | "linker (1+ to 1)"
                                                                            |  .--------------.
                                                                            +--+ "executable" |
                                                                               '--------------'
   ```

 * `{bm} enumeration/(enumeration|enum)/i` - A user-defined type that can be set to one of a set of possibilities.

 * `{bm} class/(class|struct)/i` - A user-defined type that pairs together data and the functions that operate on that data.

 * `{bm} union` - A user-defined type where all members share the same memory location (different representations of the same data).

 * `{bm} plain-old-data class/(plain-old-data class|plain-old data class|plain old data class|plain-old-data structure|plain-old data structure|plain old data structure|plain-old-data struct|plain-old data struct|plain old data struct)/i` `{bm} /(POD)/` - A class that contains only data, not functions.

 * `{bm} member/\b(member)/i` - Data or function belonging to a class.

 * `{bm} method` - Function belonging to a class (class member that is a function).

 * `{bm} field` - Data belonging to a class (class member that is a variable).

 * `{bm} class invariant` - When using some class, a class invariant is a feature of that class that is always true (never varies). For example, if a class is used to hold on to an IP and port combination, and it ensures that the port can never be 0, that's a class invariant.

 * `{bm} fundamental type/(fundamental type|built-in type)/i` - C++ type that's built into the compiler itself rather than being declared through code. Examples include `void`, `bool`, `int`, `char`, etc..

 * `{bm} object initialization` - The process by which a C++ program initializes an object (e.g. an `int`, array of `int`s, object of a class type, etc..).

 * `{bm} braced initialization/(brace initialization|braced initialization|uniform initialization)/i` - A form of object initialization where braces are used to set values (e.g. `MyStruct x = { 1, true }`, `MyStruct x{ 1, true }`, etc..). Braced initialization is often the least error-prone form of object initialization, where other forms may introduce ambiguity.

   ```c++
   MyStruct x{int(a), int(b)};  // call the constructor taking in two ints
   MyStruct x(int(a), int(b));  // possibly interpreted as function declaration -- equiv to MyStruct(int a, int b)

   float a{1}, b{2};
   int b (a/b); // no compiler warning generated about narrowing (why? -- book doesn't say)
   int b {a/b}; // compiler warning generated about narrowing
   ```

   ```{note}
   This is also called uniform initialization.
   ```

 * `{bm} equals initialization/(equals? initialization)/i` - A form of object initialization where the equals sign is used (e.g. `int x { 5 }`).

 * `{bm} braces-plus-equals initialization/(brace[sd]?[\-\s]plus[\-\s]equals? initialization)/i` - A form of object initialization where both the equals sign and braces are used for initialization (e.g. `MyStruct x = { 1, true }`). This is mostly equivalent to braced initialization.

   ```{note}
   See [here](https://stackoverflow.com/a/20733537). No copying/moving is done by the assignment.
   ```

 * `{bm} constructor` - A function used for initializing an object.

 * `{bm} destructor` - A function used for cleanup when an object is destroyed.

 * `{bm} pointer` - A data type used to point to a different piece of memory (e.g. `int yPtr { &y }`).

 * `{bm} reference` - A data type used to point to a different piece of memory, but in a more sanitized / less confusing manner (e.g. `int &yRef { y };`).

 * `{bm} sizeof` - An operator that returns the size of a type or object (known at compile-time).

 * `{bm} address-of (&)/(address[\-\s]of)/i` - A unary operator used to obtain the memory address of an object (pointer) (e.g. `int *ptr {&x}`).

 * `{bm} dereference (*)/(dereference|dereferencing)/i` - A unary operator used to obtain the object at some memory address (e.g. `int x {*ptr}`).

 * `{bm} member-of-pointer (->)/(member[\-\s]of[\-\s]pointer)/i` - An operator that dereferences a pointer and access a member of the object pointed to (e.g. `ptr->x`).

 * `{bm} member-of-object (.)/(member[\-\s]of[\-\s]object)/i` - An operator that accesses a member of an object to (e.g. `obj.x`).

 * `{bm} pointer arithmetic` - Adding or subtracting integer types to a pointer will move that pointer by the number of bytes that makes up its underlying type (e.g. `uint32_t *ptrB = ptrA + 1` will set `ptrB` to 4 bytes ahead of ptrA).

 * `{bm} reseating/(reseat)/i` - The concept_NORM of a variable that points to something updating to point to something else. Pointers can be reseated, but references cannot.

 * `{bm} member initializer list/(member initializer list|member initialization list|member initializer)/i` - A comma separated list of object initializations for the fields of a class appearing just before a constructor's body.

 * `{bm} default member initialization/(default member initializer|default member initialization)/i` - The object initialization of a field directly where that field is declared.

 * `{bm} object/(object|instance)/i` - A region of memory that has a type and a value (e.g. class, an integer, a pointer to an integer, etc..).

 * `{bm} allocation/(allocation|allocate)/i` - The act of reserving memory for an object.

 * `{bm} deallocation/(deallocation|deallocate)/i` - The act of releasing the memory used by an object.

 * `{bm} storage duration` - The duration between an object's allocation and deallocation.

 * `{bm} lifetime` - The duration between when an object's constructor _completes_ (meaning the constructor finishes) and when its destructor is _invoked_ (meaning when the destructor starts).

 * `{bm} automatic object/(automatic object|automatic variable|automatic storage duration)/i` - An object that's declared within an enclosing code block. The storage duration of these objects start at the beginning of the block and finish at the end of the block.

 * `{bm} static object/(static object|static variable|static storage duration)/i` - An object that's declared using `static` or `extern`. The storage duration of these objects start at the beginning of the program and finish at the end of the program.

 * `{bm} local static object/(local static object|local static variable|local static storage duration)/i` - A static object but declared at function scope. The storage duration of these objects start at the first invocation of the function and finish at the end of the program.

 * `{bm} static member/(static field|static member)/i` - An object that's a member of a class but bound globally rather than on an instance of the class. A static field is essentially a static object that's accessible through the class itself (not an instance of the class). Similarly, a static method is essentially a global function that's accessed through the class (not an instance of the class).

 * `{bm} thread local object/(thread[\-\s]local object|thread[\-\s]local variable|thread[\-\s]local storage duration|thread storage duration)/i` - An object where each thread has access to its own copy. The storage duration of these objects start at the beginning of the thread and finish when the thread ends.

 * `{bm} dynamically allocated object/(dynamic object|dynamic array|dynamically allocated object|dynamically allocated array|dynamic storage duration)/i` - An object that's allocated and deallocated at the user's behest, meaning that it's storage duration is also controlled by the user.

 * `{bm} internal linkage` - A variable only visible to the translation unit it's in.

 * `{bm} external linkage` - A variable visible to the translation units that it's in as well as other translation units.

 * `{bm} scope resolution (::)/(scope resolution)/i` - A operator that's used to access static members (e.g. `MyStruct::static_func()`).

 * `{bm} extend/(extend|subclass)/i` - Another way of expressing class inheritance (e.g. B extends A is equivalent to saying B is a child of A).

 * `{bm} exception/(exception|try[\-\s]catch)/i` - An exception operation accepts an object and unwinds the call stack until reaching a special region specifically intended to stop the unwinding for objects of that type, called a try-catch block. Exceptions are a way for code to signal that something unexpected / exceptional happened.

 * `{bm} structured binding` - A language feature that allows for unpacking an object's members / array's elements into a set of variables (e.g. `auto [x, y] = two_elem_array`).

 * `{bm} copy semantics` - The rules used for making copies of objects of some type. A copy, once made, should be equivalent to its source. A modification on the copy shouldn't modify the source as well.

 * `{bm} member-wise copy/(member[\-\s]wise copy)/i` - The default copy semantics for classes. Each individual field is copied.

 * `{bm} copy constructor` - A constructor with a single parameter that takes in a reference to an object of the same type (e.g. `T(const T &) { ... }`). A copy constructor is used to specify the copy semantics for that class.

 * `{bm} copy assignment` - An assignment operator overload that copies one object into another (e.g. `x = y`). Copy assignment requires that resources in the destination object be cleaned up prior to performing the copy.

 * `{bm} RAII/(RAII|CADRe)/` - Short for resource acquisition is initialization, the concept_NORM that the life cycle of some resource (e.g. open file, database object, etc..) is bound to an object's lifetime via it's constructor and destructor.

   Sometimes also referred to constructor acquires destructor releases (CADRe).

 * `{bm} moved-from object/(moved[\-\s]from object|moved[\-\s]from state)/i` - When an object is moved to another object, that object enters a special state where the only possible operation allowed on it is either destruction or re-assignment.

 * `{bm} move constructor` - A constructor with a single parameter that takes in an rvalue reference to an object of the same type (e.g. `T(T &&) { ... }`). A move constructor is used to specify the move semantics for that class.

 * `{bm} move assignment` - An assignment operator overload that moves one object into another (e.g. `x = y`).

 * `{bm} value categories/(value categories|value category|prvalue|lvalue|xvalue|rvalue|glvalue)/i` - A classification hierarchy for C++ expressions. Any C++ expression falls into one of the following categories: lvalue, xvalue, or prvalue.

   The intent of this hierarchy is to enable the _moving_ of objects. In this case, moving doesn't mean copying. It means gutting out the contents of one object and moving it into another object.

   ```{svgbob}
             lvalue "(YES addressable + NO movable)"
            /
           /
   glvalue  "(YES addressable)" 
           \
            \
             xvalue "(YES addressable + YES movable)"
            /
           /
    rvalue  "(YES movable)"
           \
            \
             prvalue "(NO addressable + YES movable)"
   ```

   * prvalue - An expression that, once evaluated, is a transient / temporary object.

     ```c++
     (x + 51) / n    // this is a prvalue      (the result is temporary, needing to go somewhere)
     x               // this is NOT a prvalue  (the result of x is just x -- it's an exist object)
     ```

   * lvalue - An expression that, once evaluated, is an addressable object (NOT transient / NOT temporary / the address-of operator is usable on it).

      ```c++
      (x + 51) / n    // this is NOT an lvalue (the result is temporary, needing to go somewhere)
      x               // this is a lvalue      (the result of x is just x -- it's an exist object)
      ```
    
   * xvalue - An expression that, similar to lvalue, is an addressable object. But, unlike lvalue, the object is marked as being near the end of its lifetime.

   ```{note}
   See the expression categories for more information.
   ```

 * `{bm} variable length array` `{bm} /(VLA)/` - A feature of C99 that allows for declaring an automatic storage duration array whose length is determined at runtime (non-constant length). This feature is not available in C++ because C++ provides higher-level abstractions for collections of objects in its STL (speculation).

   ```c++
   void test(int n) {
       int x[] = int[n];  // okay in C99, but not in C++
   }
   ```

 * `{bm} rvalue reference` - A data type that's more-or-less the same as a reference but conveys to the compiler that the data its pointing to is an rvalue (e.g. `MyType &&rref { y }`).

 * `{bm} virtual method/(virtual method|virtual function)/i` - A method in a base class that is overridable by any class that inherits from that base class.

 * `{bm} pure virtual method/(pure[\-\s]virtual method|pure[\-\s]virtual function)/i` - A virtual method that requires an implementation (no implementation has been provided by the base class that declares it). For a class to be instantiable, it cannot have any pure virtual methods (similar to an abstract class in Java).

 * `{bm} pure virtual class/(pure[\-\s]virtual class)/i` - A class that only contains pure virtual methods.

 * `{bm} virtual destructor` - A destructor that's a virtual method.

 * `{bm} vtable` - A table of pointers to virtual functions, generated by the compiler. When a virtual function gets invoked (runtime) vtables are used to determining which method implementation to use.

 * `{bm} template` - A class or function where parts of the code are intended for substitution (by other code). At compile-time, a user supplies a set of substitutions for each usage of a template, customizing it for the specific use-case that user is dealing with.

 * `{bm} template parameter` - An identifier within the template. At compile time, any time a template is used its template parameters are substituted with code that the usage supplies.
 
   A template parameter may be used multiple times throughout the template. At compile-time, each usage is substituted with the same piece of code.

 * `{bm} template instantiation` - The process of substituting the template parameters in a template with real code.

 * `{bm} named conversion/(named conversion function|named conversion|const[_\s]cast|static[_\s]cast|reinterpret[_\s]cast|narrow[_\s]cast)/i` - A set of language features / functions used for converting types (casting): `const_cast`, `static_cast`, `reinterpret_cast`, and `narrow_cast`.

 * `{bm} concept/(concept)_TEMPLATE/i` - A compile-time check to ensure that the type substituted for a template parameter matches a set of requirements (e.g. the type support certain operators).

 * `{bm} compile-time` - Used in reference to something that happens during the compilation process.

 * `{bm} runtime` - Used in reference to something that happens when the compiled program is running.

 * `{bm} zero-arg/\b(zero-arg|no-arg)\b/i` - Short for zero argument. A function with zero parameters.

 * `{bm} parameter pack` - In the context of templates, a parameter pack is a single template parameter declaration that can take in zero or more substitutions (variadic).

 * `{bm} variadic/(variadic|vararg)/i` - A function that takes in a variable number of arguments, sometimes also called varargs.

 * `{bm} template specialization` - Given a specific substitutions set substitutions for the template parameters of a template, a template specialization is code that overrides the template generated code. Often times template specializations are introduced because they're more memory or computationally efficient than the standard template generated code.

 * `{bm} partial template specialization/(partial template specialization | template partial specialization)/i` - A template specialization where not all of the template parameters have been removed.

 * `{bm} default template argument` - The default substitute in use for a template parameter.

 * `{bm} heap/(heap|free store)/i` - An implementation-specific block of memory used for dynamic objects. Also called the free store.

 * `{bm} implicit type conversion` - When an object of a certain type is converted automatically, without code explicitly changing the object to a different type (e.g. `long x {1}` implicitly converts the `int` literal in the initializer to the `long` type).

 * `{bm} explicit type conversion` - When an object of a certain type is explicitly converted to another type: casting and named conversions.

 * `{bm} promotion rule` - An implicit type conversion that may occur when an operator's operands are of differing integral and floating point types. For example, adding an integral type with a smaller integral type will cause the result to be of the same type as the larger type.

 * `{bm} narrowing conversion` - When an object of a certain type is truncated to a lesser type (e.g. `int` to `short`). 

   Narrowing conversions may be implicit during object initialization. To erroneous cases of narrowing, use braced initialization to force the compiler to generate a warning.

 * `{bm} constant expression` - A function that gets evaluated at compile-time, such that at run-time any invocation of it simply returns the result computed at compile-time. Constant expressions are represented as functions prefixed with the `constexpr` keyword.

 * `{bm} literal type` - A type that's usable in a constant expression (for parameters and return), meaning that objects of this type can have a value that's knowable at compile-time.

 * `{bm} volatile` - A volatile variable's usage in code is immune to compiler optimizations such as operation re-ordering and removal. Mutations and accesses, no matter how irrelevant they may seem, are kept in-place and in-order by the compiler.

`{bm-ignore} (classification)/i`
`{bm-ignore} (structure)/i`
`{bm-error} Did you mean variadic?/(vardic)/i`
`{bm-error} Did you mean template parameter?/(type parameter)/i`

`{bm-error} Add the suffix _NORM or _TEMPLATE/(concept)/i`
`{bm-ignore} (concept)_NORM/i`