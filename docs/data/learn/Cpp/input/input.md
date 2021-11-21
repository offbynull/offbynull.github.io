`{title} C++`

```{toc}
```

# Core Integer Types

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

Integer ranges, although platform-specific, are queryable in climits of the C++ standard library.

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
See also `std::numeric_limits` in limits of the C++ standard library. This seems to also provide platform-specific definitions that are queryable via functions..
```

# Sized Integer Types

Integer types with standardized bit lengths are defined in cstdlib of the C++ standard library.

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
See also `std::numeric_limits` in limits of the C++ standard library. This seems to also provide platform-specific definitions that are queryable via functions..
```

# Floating Point Types

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

Floating point characteristics, although platform-specific, are queryable in cfloat of the C++ standard library.

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

```{note}
I see online that `FLT_DIG`, `DBL_DIG`, `LDBL_DIG`, and `DECIMAL_DIG` define the number of "decimal digits" that can be converted to floating point and back without a loss in precision. I'm assuming that just means the max number of digits that can be represented in a float where exp is 1?
```

```{note}
See also `std::numeric_limits` in limits of the C++ standard library. This seems to also provide platform-specific definitions that are queryable via functions..
```

# String Types

Core C++ strings are represented as an array of characters, where that array ends with a null character to signify its end. This is in contrast to other major platforms that typically structure strings a size integer along with the array (no null terminator).

Individual characters all map to integer types, where literals are defined by wrapping the character in single quotes. Even though they're integers, the signed-ness of each of the types below isn't guaranteed.

| type       | bits | literal prefix | example | description                                                 |
|------------|------|----------------|---------|-------------------------------------------------------------|
| `char`     | >= 8 |                | `'T'`   | >= 8-bit wide character (smallest unit of memory -- 1 byte) |
| `char16_t` | 16   | `L`            | `L'T'`  | 16-bit wide character (e.g. UTF-16)                         |
| `char32_t` | 32   | `u`            | `u'T'`  | 32-bit wide character (e.g. UTF-32)                         |
| `wchar_t`  |      | `U`            | `U'T'`  | at least as wide as `char`                                  |

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

# sizeof

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

In other words, `sizeof` returns the size of things known at compile-time. If a variable is passed in, it outputs the size of the data type. For example, if the data type is a struct of type MyStruct, it'll return the number of bytes used to store a MyStruct. However, if the data type is a pointer to MyStruct, it'll return the number of bytes to hold that pointer. That is, you can't use it to get the size of something like a dynamically allocated array of integers.

```{note}
As shown in the examples above, the `sizeof` a C++ reference is equivalent to the raw size. For example, `sizeof char == sizeof (char &)`.
```

```{note}
The last example is valid in C99 (called a VLA -- variable length array) but not C++. The reason is C++ has std::vector and std::array that give you basically the same thing as variable arrays.

In C, where VLAs are allowed, doing a `sizeof` on a VLA is undefined.
```

Remember that `sizeof` is a _unary operator_, similar to how the negative sign is a unary operator that negates whatever is to the right of it. People usually structure its usage in code as if it were a function (e.g. `sizeof(x)` vs `sizeof x`). This sometimes causes confusion for people coming from other languages.

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

 * `{bm} linker/(linker|binary|executable)/i` - A tool that takes multiple object files to produce an executable. Linkers are are also responsible for finding libraries used by the program and integrating them into the executable.

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