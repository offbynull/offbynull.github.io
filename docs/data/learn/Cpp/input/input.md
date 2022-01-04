`{title} C++`

```{toc}
```

# TODOs

TODO: Set prereqs

TODO: ch 9 at std::function / std::callable

TODO: C++20 coroutines section needs to be fleshed out better (no good source for this)

TODO: add section on equals/hashcode/tostring equivalents
      -- operator== overload
      -- std::hash template overload: https://en.cppreference.com/w/cpp/utility/hash
      -- friend function to ostringstream

TODO: smart pointers

TODO: add terminology for declarations and definitions + add more example code into terminology

# Essentials

The following document is my attempt at charting out the various pieces of the modern C++ landscape, focusing on the 80% of features that gets used most of the time rather than the 20% of highly esoteric / confusing features. It isn't comprehensive and some of the information may not be entirely correct / may be missing large portions.

The key points of similarity to remember:

1. Scope in C++ is similar to Java/C# (e.g. function scope, class scope, etc...). Variables, classes, etc.. come into and leave out of scopes in similar ways.
1. Compound statements in C++ are similar Java/C#. They create a scope, and things declared in that scope are gone once the scope is exited.
1. Control flow statements in C++ are similar to Java/C#. All the basics are there: for loops, for-each loops, while loops, if-else, switch, etc...
1. Data can exist on the heap or stack similar to Java/C#.

The key point of dissimilarity to remember:

1. **C++ does not come with a garbage collector**. You are responsible for releasing memory, although the C++ standard library has a lot of pieces to help with this.
1. C++ has a lot of legacy baggage and many edge cases. Compared to Java/C#, the language is powerful but also deeply convoluted with many foot-guns and esoteric syntax / semantics.
1. C++ has a lot of ambiguous behaviour. Compared to Java/C#, the language specifically carves out pieces of the spec and leaves it as platform-specific behaviour, undefined behaviour, etc.. so that compilers have more room to optimize code. 

## Language Basics

The following are a base set of language constructs required for understanding the rest of the document.

1. The general purpose integral type is `int`.

2. Variables use the format `modifiers type name initializer`.

   ```c++
   int a = 0;
   int b (0); // parenthesis
   int c {0}; // curly braces
   ```
 
   C++ provides a bewildering number of ways to initialize a variable, each with its own set of edge cases. For best results, stick to the curly braces.

3. Functions use the format `modifiers return-type name(param-type1 arg-name1, param-type2 arg-name2, ...) modifiers { body }`.
 
   ```c++
   int myFunction(int a) {
       return x + a;
   }
   ```
 
   C++ functions don't necessarily have to be methods (members of a class).

4. Classes use either `struct` or `class`.

   `struct` makes all members of the class public by default, while `class` makes them all private by default. Members need to be grouped together by visibility, where a visibility (e.g. `private`) is a label within the class.

   ```c++
   class MyClass {
      int myFunction(int a) {
         return x + a;
      }
   private: // everything under this label is private
      int x {0};
   };
   ```

5. Source code often comes in pairs: A header file usually contains declarations (e.g. just the function's signature / prototype) while a C++ file usually contains definitions (e.g. the function implementation).

   ```c++
   // MyCode.hpp (header file w/ declarations)
   int myFunction(int a);
 
   // MyCode.cpp (source file w/ definitions)
   #include "MyCode.hpp"
   int myFunction(int a) {
       return x + a;
   }
   ```

   This isn't required. Source files may contain declarations and / or header files may contain definitions, but the split is typically done for a variety of reasons: faster compile times, sharing the same object across multiple source files, compiling when there are cyclical references, etc..

```{note}
The above points aren't entirely correct or complete. They're generalizations that help set up a base for the explanations in the rest of the document.
```

## Example Program

The following is an example C++ program that prints "hello world" to stdout.

```c++
// hello.cpp file
#include <iostream>
int main() {
    std::cout << "hello world\n";
    return 0;
}
```

The ...

 * `#include <iostream>` pulls in a library that lets you interface with stdout, stderr, and stdin.
 * `int main() { ... }` is the entry point of the program.
 * `std:cout << ...` is what prints to stdout.
 * `return 0` returns from the `main()` function, ending the program with an exit code of 0.

Pretty much any modern C++ compiler will compile the above code. The output below uses the GNU C++ compiler to compile the example, then runs the executable.

```
$ g++ hello.cpp
$ ./a.out
hello world
```

## Compilation

Several C++ compilers exist, the most popular of which are the GNU C++ compiler and LLVM clang. C++ compilers generally follow the same set of steps to go from C++ code to an executable.

1. C++ source files get fed into a preprocessor to generate translation units. A translation unit is the C++ source file after going through modifications based compiler specifics, platform specifics, libraries used, compile options / library options, etc..
1. Translation unit files get fed into a compiler to generate object files. An object file is the intermediary compiled form of each individual translation unit.
1. Object files get fed into a linker to generate the executable. All object files come together and linkages between them are made to form the final executable.

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

The C++ language has a lot of legacy baggage, edge cases, and ambiguous behaviour. Regardless of the compiler chosen, at least some of the following warning options should be enabled:

* `-Wall` - Warns about questionable but easily avoidable constructs.
* `-Wextra` - Warns about other questionable constructs not covered by `-Wall`. 
* `-Wpedantic` - Warns about ISO conformance.
* `-Weverything` - Turns on all warnings.

Most compilers support some or all of the flags above.

```{note}
A good online tool to try things in is [cppinsights](https://cppinsights.io/), which breaks down C++ code and allows you some visibility into what the compiler is doing / what the compiler sees.
```

## Header Files

For each source code file that gets compiled, the compiler needs to know that the entities (variables, functions, classes, etc..) accessed within that file actually exist. The scope at which the compiler keeps track of these entities is per source code file. For example, imagine a source code file that defines a function named `myFunction` (definition). There are 5 other source code files that call `myFunction` at some point. Each of those 5 other files is required to tell the compiler what `myFunction` is (declaration) before it can invoke it.

One way to handle this scenario is to put `myFunction`'s declaration in each source code file that calls it.

```c++
OtherClass myFunction(int a);
```

The problem with doing this is that ...

1. you're duplicating something 5 times, meaning you need to update 5 different places should anything change with the class.
2. you need a declaration for more than just `myFunction` (e.g. `myFunction` requires `OtherClass`, which may require even more entities). 
3. as a result of 1 and 2, source code file sizes explode and quickly becomes unmanageable.

The preferred way to handle this scenario is to put `myFunction`'s declaration into a header file. Then, any file that needs to know about `myFunction` can use the `#include` directive.,,

```c++
// MyFunction.hpp
#include "OtherClass.hpp"
OtherClass myFunction(int a);

// UsageFile1.cpp
#include "MyFunction.hpp"
myFunction(44);
```

If an entity is declared once already by an `#include`, it shouldn't be declared again.  For example, imagine that the file `Main.cpp` includes `ParentA.hpp` and `ParentB.hpp`. Both `ParentA.hpp` and `ParentB.hpp` then go on to include `Child.hpp`....

```{svgbob}
Main.cpp
  |
  +----> ParentA.hpp ------+
  |                        +----> Child.hpp
  +----> ParentB.hpp ------+
```

The problem the above example scenario creates is that `Child.hpp` gets `#include`'d twice, meaning that everything in it is declared twice. To mitigate this problem, an include guard is typically provided in each header file.

```c++
// MyFunction.hpp
#ifndef MY_FUNCTION_H // include guard
#define MY_FUNCTION_H

#include "OtherClass.hpp"
OtherClass myFunction(int a);

#endif
```

```{note}
`#ifdef`, `#define`, and `#endif` are preprocessor macros that aren't covered here. Look them up online if you need to. 
```

You may notice that sometimes `#include` puts quotes around the files and sometimes angle brackets. Use quotes when the files are in the same directory structure, angle brackets when the files are coming from some external library.

```c++
#include <vector>          // library header
#include "OtherClass.hpp"  // local header
```

# Operators

The following subsections provide the list of operators available in C++. Some operators are obvious, while others are explained in other sections.

## Bitwise Logical Operators

| Name                       | Example            | Note                                             |
|----------------------------|--------------------|--------------------------------------------------|
| Bitwise AND         (`&`)  | `0b1011 & 0b0110`  |                                                  |
| Bitwise OR          (`\|`) | `0b1011 \| 0b0110` |                                                  |
| Bitwise XOR         (`^`)  | `0b1011 ^ 0b0110`  |                                                  |
| Bitwise NOT         (`~`)  | `~0b1011`          |                                                  |
| Bitwise left-shift  (`<<`) | `0b1011 << 2`      |                                                  |
| Bitwise right-shift (`>>`) | `0b1011 >> 2`      | Result on signed may be different than unsigned. |

## Boolean Logical Operators

| Name                 | Example           | Note |
|----------------------|-------------------|------|
| Logical AND (`&&`)   | `true && true`    |      |
| Logical OR  (`\|\|`) | `true \|\| false` |      |
| Logical NOT (`!`)    | `!true`           |      |

## Arithmetic Operators

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
If confused, use type deduction via the `auto` keyword: `auto x {5 + y}`, then check to see what the type of `y` is in the IDE or using `typeid`.
```

## Assignment Operators

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
int x {3};
int y {(x++) + 2};
// at this point, x is 4, y is 5
int a {3};
int b {(++a) + 2};
// at this point, a is 4, b is 6
```

## Comparison Operator

| Name                             | Example   | Note                                                                                    |
|----------------------------------|-----------|-----------------------------------------------------------------------------------------|
| Equal To                 (`==`)  | `5 == 7`  |                                                                                         |
| Not Equal To             (`!=`)  | `5 != 7`  |                                                                                         |
| Less Than                (`<`)   | `5 < 7`   |                                                                                         |
| Less Than Or Equal To    (`<=`)  | `5 <= 7`  |                                                                                         |
| Greater Than             (`>`)   | `5 > 7`   |                                                                                         |
| Greater Than Or Equal To (`>=`)  | `5 >= 7`  |                                                                                         |
| Three-way Comparison     (`<=>`) | `5 <=> 7` | Returns a special ordering type, not boolean (discussed in spaceship operator section). |

In addition, the ternary conditional operator is a pseudo operator that takes in 3 operands similar to those found in other high-level languages: `CONDITION ? EXPRESSION_IF_TRUE : EXPRESSION_IF_FALSE`. It's essentially a shorthand if-else block. 

```c++
int x {n % 7 == 1 ? 1000 : -1000};
// equiv to...
if (n % 7 == 1) {
    x = 1000;
} else {
    x = -1000;
}
```

## Member Access Operators

| Name                     | Example     | Note                                                                                       |
|--------------------------|-------------|--------------------------------------------------------------------------------------------|
| Subscript         (`[]`) | `x[0]`      |                                                                                            |
| Indirection       (`*`)  | `*x`        | Doesn't conflict with arithmetic multiplication operator because this is a unary operator. |
| Address Of        (`&`)  | `&x`        |                                                                                            |
| Member Of Object  (`.`)  | `x.member`  |                                                                                            |
| Member Of Pointer (`->`) | `x->member` |                                                                                            |

There operators are used in scenarios that deal with accessing the members of an object (e.g. element in an array, field of a class) or dealing with memory addresses / pointers. The subscript and and member of object operators are similar to their counterparts in other high-level languages (e.g. Java, Python, C#, etc..). The others are unique to languages with support for lower-level programming like C++. Their usage is detailed in other sections.

## Dynamic Object Operators

| Name                                | Example       | Note |
|-------------------------------------|---------------|------|
| Create Dynamic Object       (`new`) | `new int`     |      |
| Create Dynamic Array      (`new[]`) | `new int[50]` |      |
| Destroy Dynamic Object   (`delete`) | `delete x`    |      |
| Destroy Dynamic Array  (`delete[]`) | `delete[] x`  |      |

```{note}
If you already know about dynamic objects and arrays and constructors/destructors, make sure you delete an array using `delete[]`. It makes sure to call the destructor for each element of the array.
```

## Size Operator

| Name            | Example     | Note |
|-----------------|-------------|------|
| Size (`sizeof`) | `sizeof x]` |      |

This operator gets the size of an object in bytes. Note that an object's byte size may not be indicative of the da may include padding required by the platform (e.g. an object requiring 5 bytes may get expanded to 8 bytes because the platform requires 8 byte boundary alignments).

## Other Operators 

C++ provides a set of other operators such as the ...

 * comma operator (`,`).
 * function call operator (`()`).
 * conversion operator (e.g. casting).
 * user-defined literal operator (e.g. `_`)

While it isn't worth going into them in detail here, the reason the language explicitly lists them as operators is because they're overload-able (e.g. operator overloading). Overloading these operators is heavily discouraged since doing so causes confusion.

````{note}
The book mentions the comma operator specifically. It doesn't look this is used for much and the book recommends against using it for anything (e.g. operator overloading) due to the confusion it causes. This gives off similar vibes to Python's tuple syntax, where you can pass an unenclosed tuple as a subscript to something. When I was learning Python, that also came off as very confusing.

```python
x = obj['column name', 100]
```
````

# Variables

C++ variable declarations have the following form: `modifiers type name initializer`.

 * **type** (required) - Type of variable.

 * **name**: (required) - Name of variable.

 * **initializer**: (optional) - Initial value to assign (object initialization).

   There are multiple ways to initialize a variable, each with their own advantages and disadvantages.

   * braced initialization / uniform initialization: braces used for initialization (e.g. `int x {a + b}`).
   * equals initialization: equals sign used for initialization (e.g. `int x = 5`).
   * brace-plus-equals initialization: equals sign and braces used for initialization (e.g. `int x = { a + b }`).
   * etc..

   ```{note}
   The above is an over-simplification. The ways to initialize are vast and complex. See [here](https://en.cppreference.com/w/cpp/language/initialization) for a full accounting and [here](https://youtu.be/7DTlWPgX6zs) for an hour long talk about the edge cases.
   
   It seems like the safest bet is to always use brace initialization where possible. Just use the braces as if they were parenthesis or braces in Java (specific to the context). The others have surprising behaviour (e.g. they won't warn about narrowing conversions).
   ```

 * **modifiers** (optional) - Markers controlling the behaviour / properties of a variable.

   (e.g. `const`, `volatile`, `constexpr`, `inline`, ...)

```c++
int a;     // no initializer -- garbage possibly contained at memory location
int b {};  // empty initializer -- zeros out the memory for the int
int c {0}; // assign to constant 0
int d {c}; // assign to value in c
```

In C++, variables that are fields (assigned to a class) are called member variables. This section deals with non-member variables (e.g. scoped somewhere other than a class -- global, inside a function, etc..).

## Core Types

The following sections list out core C++ types and their analogs. These include numeric types, character types, and string types.

### Integral

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
 * encoding scheme of _signed_ types is two's complement (as of C++20), but underflow/overflow behaviour of _signed_ types is undefined (e.g. crash, stay at boundary, wrap back around, etc..).

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
There is no macro `SIZE_C(...)` for `size_t`. Best to just assign a `size_t to one of the other types's literals and hope the compiler warns about any narrowing conversions that might happen.
```

```{note}
What's the point of the above? You don't know what internal integer type each standardized type maps to. For example, `uint64_t` may map to `unsigned long long`, which means when you want to assign a literal to a variable of that type you need to add a `ULL` suffix...

`uint64_t test {9999999999999999999ULL}`

The macros above make it so that you don't need to know the underlying mapping...

`uint64_t test {UINT64_C(9999999999999999999)}`
```

```{note}
See also `std::numeric_limits` in the limits. This seems to also provide platform-specific definitions that are queryable via functions..
```

### Floating Point

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

### Character String

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

### Void

`void` is a type that represents an empty set of values. Since it can't hold a value, C++ won't allow you to declare an object of type void. However, you can use it to declare that a function ...

* returns no value (`void` return).
* accepts no arguments (`void` parameter list).

## Arrays

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
   int y { test(x) };
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
   size_t y { test(x) }; // compiler doesn't complain that test() expects int[10] but this is int[3]
   cout << y;
   return 0;
}
```
````


Be careful when using the `sizeof` operator on an array. If the type is the original array type, `sizeof` will return the number of bytes taken up by the elements of that array (known at compile-time). However, if the type has decayed to a pointer type, `sizeof` will return the number of bytes to hold on to a pointer.

```c++
int x[3];
int *y {x};  // equiv to setting to &(x[0]);
cout << sizeof x;  // should be the size of 3 ints
cout << sizeof y;  // should be the size of a pointer
```

Similarly, range-based for loops won't work if the type has decayed to a pointer type because the array size of that pointer isn't known at compile-time.

```c++
int x[3] = {1,2,3};
int *y {x};
for (int i {0}; i < 3; i++) { // OK
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

## Pointers

C++ provides types that reference a memory address, called pointers. Variables of these types can point to different memory addresses / objects.

Adding an asterisk (\*) to the end of any type makes it a pointer type (e.g. `int *` is a type that can contain a pointer to an `int`). A pointer to any object can be retrieved using the address-of unary operator (&). Similarly, the value in any pointer can be retrieved using the deference unary operator (\*).

```c++
int w {5};
int *x { &w }; // x points to w
int *y { &w }; // y points to w
int z { *x };   // z is a copy of whatever x points to, which is w, which means it gets set to 5
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
int *y { nullptr }; // implicit conversion
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
int *ptrA { &(x[1]) };  // points to idx 1 of x (5)
int *ptrB { ptrA + 1 }; // points to idx 2 of x (7)
```

This is similar to array access via the subscript operator. In fact, both arrays and pointers can be accessed in the same way using the subscript operator and pointer arithmetic.

```c++
int x[] { 1, 2, 3, 4, 5, 6, 7, 8, 9 };
int *y {x};
*(y+1) = 99;  // equivalent to x[1] = 99
x[2] = 101;   // equivalent to *(y+2) = 101;
```

```{note}
An array guarantees that its elements appear contiguously and in order within memory (I think?), so if the pointer is from a decay'd array, using pointer arithmetic to access its elements is perfectly fine.
```

### Void Pointer

A pointer to the void type means that the type being pointed to is unknown. Since the type is unknown, dereferencing a void pointer isn't possible. In other words, it isn't possible to read or write to the data pointed to by a void * because the underlying type is void / unknown.

```c++
int x[] { 1, 2, 3, 4, 5, 6, 7, 8, 9 };
void *y { x };
*y = 2; // fails
```

Since the underlying type of the pointer is unknown, pointer arithmetic isn't allowed either.

```c++
int x[] { 1, 2, 3, 4, 5, 6, 7, 8, 9 };
void *y { x };
y = y + 2; // fails
```

```{note}
If you have a `void *` and you want to do raw memory manipulation at that address, use a `std::byte *` instead. Why not just use `char *` instead? Is a `char` guaranteed to be 1 byte (I think it is)? According to [this](https://stackoverflow.com/a/46151026), it's because certain assumptions about `char`s may not hold with bytes? I don't know. Just remember `std::byte *` if you're working with raw data.
``` 

### Function Pointer

A pointer to a function means the type being pointed to is a function with some specific structure. All functions have a type associated with them, defined by their return type, parameter type, and owning class if the function is a method.

```c++
// type is: int (int, int)
int add(int a, int b) {
    return a + b;
}
```

To declare a function pointer to a free function or a static class method, write out the function type (return type and parameter list without names) but place the pointer name preceded by an asterisk (\*) _wrapped in parenthesis_ where the function name would be. Invoke it just like you would any other function.

```c++
int (*func_ptr)(int, int) {}; // unset pointer to a function of structure  int (int, int)

int add(int a, int b) {
    return a + b;
}

int multiply(int a, int b) {
    return a * b;
}

func_ptr = &add;  // point func_ptr to address of add()
func_ptr(1, 2);   // invoke
```

To declare a function pointer to a non-static class method (member function), the class type needs to be included before the asterisk (\*) using the scoped resolution operator (::).

```c++
int (MyClass::*func_ptr)(int, int) {}; // unset pointer to a function of structure  int (int, int)  in or inherited from MyClass

MyClass x {};

func_ptr { &MyClass::multiply }; // point to:  int MyClass::multiply(int, int)
(x.*func_ptr)(2, 3);             // provide x as the MyClass instance when invoking
```

Unlike normal functions, functors cannot be assigned to raw function pointers. A functor's equivalent of a function pointer is a pointer to the function-call operator overload (method).

```c++
int (MyFunctor::*func_ptr)(int, int) {};  // unset pointer to a function of structure  int (int, int)  in or inherited from MyClass

MyFunctor x {};

func_ptr { &MyFunctor::operator() };
(x.*func_ptr)(2, 3);            // provide x as the MyClass instance when invoking
```

Alternatively, to support both functions and functors, the parameter expecting a function pointer should be changed to the `std::function` or the code doing the invocation should be changed to use the `std::invoke` wrapper. These wrappers abstract away the differences between pointers to functions and functors.

## References

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

## Rvalue References

An rvalue reference is similar to a reference except that it tells the compiler that it's working with is an rvalue. Rvalue references are declared by adding two ampersands (&&) after the type rather than just one. It's initialized using the `std::move()` function within the utility header, which casts its input into an rvalue reference.

Rvalue references are typically used for moving objects (not copying, but actually moving the guts of one object into another). This is typically done through something called a move constructor, which will be explained further on.

```c++
MyObject a {};
MyObject &&b { std::move(a) }; // get rvalue reference
MyObject c {b};                // move a into c (gut it into c) via the move constructor
// b is in an invalid state
```

```{note}
Once an object is moved, it's in an invalid state. The only two reliable operations you can perform on it is to either destroy or re-assign it to something else (assignments are discussed elsewhere).
```

```{note}
There's a piece here I don't fully understand about "forwarding references". See [here](https://github.com/AnthonyCalandra/modern-cpp-features#forwarding-references).
```

## Size

`sizeof` is a unary operator that returns the size of its operand in bytes as a `size_t` type. If the operand is a ...

* data type or a variable, it'll return the number of bytes needed to hold that type. For example, ...

  * `sizeof char` is guaranteed to be 1.
  * `sizeof (char &)` is guaranteed to be 1.
  * `sizeof (char *)` is platform dependant, typically either 4 or 8.
  * `char * x { "hi" }; sizeof x` is equivalent to `sizeof (char *)` (see above).

* an expression such as a structure/class literal, array literal, or string literal, it'll return the number of bytes needed to hold it. For example, ...

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

```{note}
Remember that `sizeof` is a unary operator, similar to how the negative sign is a unary operator that negates whatever is to the right of it. People usually structure its usage in code as if it were a function (e.g. `sizeof(x)` vs `sizeof x`). This sometimes causes confusion for people coming from other languages.
```

## Aliasing

The `using` keyword is used to give synonyms to types. Other than having a new name, a type alias is the exact same as the originating type.

```c++
using IntegerButWithNewName = int;
int x {42};
IntegerButWithNewName y {42};    // equivalent to:  int y {42};
IntegerButWithNewName z {x + y}; // equivalent to:  int z {x + y};

int func(float x);
int func(short x);
int func(int x);
int func(IntegerButWithNewName x);  // NOT ALLOWED -- this overload is equivalent to the overload above
```

````{note}
To allow for use-cases such as the function overloading case in the example above, the cleanest solution is to wrap the type in a class

````

The benefit of type aliasing is that it helps shorten type names, which can be especially useful when using a template.

```c++
using BasicGraph = DirectedGraph::Graph<std::string, std::map<std::string, std::string>, std::string, std::map<std::string, std::string>>;

BasicGraph removeLimbs(const BasicGraph &g);
```

## Constant

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
                  
"int const * * const: An unmodifiable pointer to a pointer to an unmodifiable int" 
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

## Volatile

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

## Deduction

The keyword `auto` may be used during a variable declaration to deduce the resulting type of that variable from whatever it's being initialized with.

```c++
auto a { 1 };  // int
auto b { 1L }; // long
auto c { &a }; // int *
auto d { *c }; // int
auto &e { a }; // int &  <-- THIS IS A SPECIAL CASE. YOU ALWAYS NEED TO USE auto& FOR REFERENCES
```

Note that the last variable in the example above explicitly the ampersand (&) to declare e as a reference type. This is required because reference initialization works the same way as normal initialization (`auto` can't disambiguate).

## Implicit Conversion

An implicit type conversion is when an object of a certain type is converted (cast) automatically, without code explicitly changing the object to a different type. For example, `long x {1}` implicitly converts the `int` literal in the initializer to a `long`.

```c++
int x {5};
long y {x};  // int to long
```

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

## Common Attributes

If a variable has been deprecated, adding a `[[deprecated]]` attribute will allow the compiler to generate a warning if it sees it being used.

```c++
[[deprecated("Warning -- this is going away in the next release")]]
int add(int a, int b) {
    return a + b;
}
```

## Explicit Conversion

An explicit type conversion is the opposite of an implicit type conversion. It's when an object of a certain type is explicitly converted (cast) to another type in code.

```c++
long x {5L};
int y {static_cast<int>(x)};   // long to int
```

Explicit type conversions come in two forms:

 * Named conversions are the official way to cast in C++.
 * C-style casts are the legacy way to cast in C++.

Named conversions should be preferred over C-style casts. Any C-style cast can be performed through a named conversion.

#### Named Conversions

Named conversion functions are a set of (seemingly templated) functions to convert an object's types. These functions provides safety mechanisms that aren't available in other older ways of casting.

 * `const_cast` removes the `const` modifier from an object's type.
   
   ```c++
   void func(const MyType &t) {
       T &moddable_t { const_cast<MyType &>(t) };
   }
   ```

   Performing this type of conversion should only be done in extreme situations since it breaks contracts.

 * `static_cast` forces the reverse of an implicit conversion.

   ```c++
   int a[] {1,2,3,4};
   int *b { a };  // ok, implicit conversion (decay to pointer)
   void *c { b }; // ok, implicit conversion
   int *d { c };  // error, can't go in reverse
   int *e { static_cast<int *>(c) }; // ok
   ```

   In the above example, a `uint32_t *` implicitly converts to `void *`, but not the reverse. A `static_cast` makes going in reverse possible. However, that doesn't mean it's always safe to do. For example, `uint32_t` reads may need to be aligned to 4 byte boundaries on certain platforms. If the `void *` was arbitrary data (e.g. coming in over a network), it might cause a crash to just treat it as a `uint32_t *` and start reading.

   ```{note}
   Why does a `uint32_t*` implicitly convert to a `void *`? Recall that `void *` just means "pointer to something unknown", which is something the language is okay automatically / implicitly converting.
   ```

 * `reinterpret_cast` forces a reinterpretation of an object into an entirely different type.

   ```c++
   int a[] {1,2,3,4};
   int *b { a };   // ok, implicit conversion (decay to pointer)
   short *c { b }; // error, you can't convert from an int* to a short* (not even with a static_cast because it's not an implicit conversion)
   short *d { reinterpret_cast<int *>; } // ok
   ```

 * `narrow_cast` is similar to `static_cast` for numerics, except it ensures that no information loss occurred.

   ```c++
   uint32_t a { 70000 };                     // ok
   uint16_t b { static_cast<uint16_t>(a) };  // ok, but since uint16_t has a max of65535, this object is mangled
   uint16_t c { narrow_cast<uint16_t>(a) };  // runtime exception, narrow_cast sees that the object will be mangled
   ```

   ```{note}
   Is this part of the standard? The book seems to give the code for `narrow_cast` and looking online it looks like people have their own implementations?
   ```

#### C-style Casts

C-style casts are similar to casts seen in Java. The type is bracketed before whatever is being evaluated.

```c++
int x { (int) 9999999999L };
```

The problem with C-style casts are that they don't provide the same safety mechanisms as named conversions do (e.g. inadvertently strip the `const`-ness). Named conversions provide these safety mechanisms and as such should be preferred over C-style casts. Any C-style cast can be performed using a named conversion.

## Object Lifecycle

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

### Static Objects

By default, an object declared within a function is said to be an automatic object. Automatic objects have automatic storage durations: start at the beginning of the block and finish at the end of the block. When the keyword `static` (or `extern` in some cases) is added to the declaration, the storage duration of the function changes.

At global scope, if an object is declared as `static` or `extern`, storage duration of the object spans the entire duration of the program. The difference between the two is essentially just visibility:

 * `static` makes it so it's accessible to only the translation unit it's declared in.
 * `extern` makes it so it's accessible to other translation units as well as the translation unit it's declared in.

```c++
static int a { 0 }; // static variable
extern int b { 1 }; // static variable (accessible outside translation unit)
```

At function scope, the storage duration of objects declared as `static` starts at the first invocation of that function and ends when the program exits.

```c++
int f1() {
    static int z {0}; // static variable
    z += 1;
    return z;
}
```

At class level, the storage duration of a member (field or method) declared as `static` is essentially the same as if it were declared at global scope (they aren't bound to an individual instance of the class the same way a normal field or method is). The only differences are that the static member is accessed on the class itself using the scoped resolution operator (::) and that static members that are fields must be initialized at global scope.

```c++
class X {
public:
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
static int a {0};
thread_local static int b {1};
thread_local extern int c {2};
```

### Dynamic Objects

An object can be created in an ad-hoc manner, such that its storage duration is entirely controlled by the user. The operator ...

 * `new` allocates a new object and calling its the constructor.
 * `delete` calls the destructor of some object and deallocates it.

Both keywords work with pointers: `new` returns a pointer while `delete` requires a pointer. To create a new object, use `new` followed by the type.

```c++
int * ptr { new int };
*ptr = 0;
delete ptr;
```

Objects may be initialized directly within the `new` invocation just as if it were an automatic object initialization. The only caveat is that equals initialization and brace-plus-equals initialization won't work because the equal sign is already being used during `new` (speculation -- it doesn't work but I don't know the exact reason). As such, braced initialization is the best way to initialize a dynamic object.

```c++
int * ptr { new int {0} }; // initialize to 0
delete ptr;
```

The same process can be used to create an array of objects. Unlike automatic object arrays, dynamic arrays don't have a constant size array lengths restriction.. However, the return value `new` will decay from an array type to a pointer type.

When deleting a dynamic object array, square brackets need to be appended to `delete` operator: `delete[]`. Doing so ensures that the destructor for each object in the array gets invoked before deallocation.

```c++
int * ptr { new int[len] };  // len is some non-constant positive integer, decayed to pointer type because array length can be non-constant.
delete[] ptr;
```

Braced initialization may be used when declaring dynamic arrays so long as the size of the array is at least the size of the initialization list.

```c++
int * ptr1 { new int[10] {1,2,3} };  // initialize the first 3 elems of a 10 elem array
int * ptr2 { new int[2] {1,2,3} };   // throws exception  (size too small for initializer list)
int * ptr3 { new int[n] {1,2,3} };   // okay -- so long as n >= 3
delete[] ptr1;
delete[] ptr2;
delete[] ptr3;
```

By default, dynamic objects are stored on a block of memory called the heap, also sometimes referred to as the free store.

```{note}
See operator overloading section to see how the `new` and `delete` operators may be overridden to customize where and how a specific type gets stored.

The `new` and `delete` operators may also be overridden globally rather than per-type. See the new header.
```

## User-defined Literals

C++ provides a way for users to define their own literals through the use of operator overloading, called user-defined literals. User-defined literals wrap built-in literals and perform some operation to convert them to either another type or another value. It's identified by a unique suffix that starts with an underscore (e.g. `_km`). 

The operator overload is identified by two quotes followed by the suffix.

```c++
Distance operator"" _km (long double n) {
    return Distance {n * 1000.0};
}

Distance operator"" _mi (long double n) {
    return Distance {n * 1609.34};
}

Distance d { 1.2_km + 4.0_mi };
```

As stated above, user-defined literals must wrap an existing built-in literal type.

| Type                  | Definition                                                   |
|-----------------------|--------------------------------------------------------------|
| integral              | `return_type operator"" identifier (unsigned long long int)` |
| floating point        | `return_type operator"" identifier (long double)`            | 
| character             | `return_type operator"" identifier (char)`                   |
| wide character        | `return_type operator"" identifier (wchar_t)`                | 
| utf-8 character       | `return_type operator"" identifier (char8_t)`                | 
| utf-16 character      | `return_type operator"" identifier (char16_t)`               | 
| utf-32 character      | `return_type operator"" identifier (char32_t)`               | 
| character string      | `return_type operator"" identifier (char *, size_t)`         |
| wide character string | `return_type operator"" identifier (wchar_t *, size_t)`      | 
| utf-8 string          | `return_type operator"" identifier (char8_t *, size_t)`      | 
| utf-16 string         | `return_type operator"" identifier (char16_t *, size_t)`     | 
| utf-32 string         | `return_type operator"" identifier (char32_t *, size_t)`     | 
| raw                   | `return_type operator"" identifier (const char *)`           |

Note that, for ...

 * numerics, the widest possible C++ type is used for both integral (unsigned long long int) and floating point (long double).
 * characters, each character type gets its own definition.
 * strings, each string type gets its own definition.

The last definition in the table above, raw, will get a character string of any numeric literal used.

```c++
const char * operator"" _as_str (const char * n) {
    std::cout << "input str: " << n;
    return n;
}

123.5e+12_as_str;  // outputs "input str: 123.5e+12"
```

The standard C++ library makes use of user-defined literals in various places, but its identifiers don't require an underscore (_) prefix.

 * Date-time API (chrono header): `std:chrono::duration d  { 2h + 15ms }`.
 * Complex numbers API (complex header): `std::complex<double> { (1.0 + 2.0i) * (3.0 + 4.0i) }`.
 * String API (string): `std::string str { "hello"s + "world"s }`.

# Functions

C++ function declarations and definitions have the following form: `prefix-modifiers return-type name(parameters) suffix-modifiers`

 * **return-type** (required) - Type returned by function.

 * **name**: (required) - Name of function.

 * **parameters** (required) - Parameter list of function.

 * **prefix-modifiers** (optional) - Markers controlling the behaviour / properties of a function.

   (e.g. `static`, `virtual`,  `constexpr`, `[[noreturn]]`, `inline`, ...)

 * **suffix-modifiers** (optional) - Markers controlling the behaviour / properties of a function.

   (e.g. `noexcept`, `const`,  `final`, `override`, `volatile`, ...)

```c++
int add(int x, int y) {
    return x + y;
}
```

In C++, functions that are ...

 * methods (assigned to a class) are called member functions.
 * global are called free functions.

This section deals with free functions.

```{note}
Some of the modifiers listed above are for member functions, not free functions.
```

## Overloading

Function overloading is when there are multiple functions with the same name in the same scope. For free functions, each function overload must have the same return type and a unique set of parameters.

```c++
bool test(int a) { return a != 0; }
bool test(double a) { return a != 0.0; }
bool test(int a, int b) { return a != b; }
```

When an overloaded function is called, the compiler will try to match argument types against parameter types to figure out which overloaded function to call. If no exact match can be found, the compiler attempts to obtain a correct set of types through a set of conversions.

```c++
int num { 1 };
test(1);  // calls the first overload in the code above:  bool test(int a);
```

```{note}
See argument matching section.
```

## Argument Matching

When an function is called but the arguments types don't match the parameter list types, the compiler attempts to obtain a correct set of types through a set of conversions on the arguments. For example, if a parameter expects a reference to an constant object but what gets passed into the argument is an object, the argument is automatically converted to a constant object and its reference is used.

```c++
bool test(const int &obj) { ... }

int x {};
test(x); // x is turned into a "const int" and passed in as a reference
```

For floating point and integral types, the compiler will widen or _narrow_ the if the exact type isn't found.

```c++
bool test(int32_t a) {
    std::cout << a;
    return a != 0;
}

float x {1.5};
test(x); // automatic narrowing
```

Similarly, the compiler will convert between signed and unsigned integral types if the exact integral type isn't found.

```c++
bool test(uint32_t a) {
    std::cout << a;
    return a != 0;
}

int64_t x {10};
test(x); // automatic narrowing and change to unsigned
```

When function overloads are involved, the candidate with the arguments matching most closely is the one chosen.

```{note}
The exact rules here seem hard to definitively pin down. If you have two overloads of a function, one accepting int16 and int64, it'll fail when you try to call it with int8 claiming that it's too ambiguous. The best thing to do is to just ask the compiler to either warn on implicit conversion (`-Wconversion`) flag or on narrowing implicit conversion (`-Wnarrowing` / `-Wno-narrowing`). These flags may not be included under `-Wall`.
```

## Type Deduction

Similar to variable declarations, the `auto` keyword is also usable to deduce a function's parameter and return types based on usage.

```c++
auto add(auto x) {
    return x + 5;
}
```

The use of `auto` is essentially short-hand for a function template. In the example above, each unique set of types used when invoking `add()` is a template instantiation.

```c++
test(5);     // uses  int add(int x)
test(6);     // uses  int add(int x)
test(5ULL);  // uses  unsigned long long add(unsigned long long x)
```

When using `auto` for a return type, you can optionally add a `->` immediately after the parameter list followed by a type expression that defines what expression should generate the returning type.

```c++
// return type should be whatever type the result of x + 5LL is, which is long long
auto add(auto x) -> decltype(x+5LL) {
    return x + 5;
}
```

```{note}
Why is the above useful? Using `auto` on functions is discouraged because function definitions act as documentation. The exception is with templates, where the types depend in potentially complex ways on template parameters.

By adding the type expression in, you're re-introducing a form of documentation.
```

```{note}
Try running functions with auto through [here](https://cppinsights.io) to get a feel for how this transforms to function templates.
```

## Main Function

The entry-point to any C++ program is the `main` function, which can take one of three possible forms:

 1. `int main()`

    No arguments.

 1. `int main(int argc, char* argv[])`

    Command-line arguments, where `argv` is an array of size `argc` containing the null-terminated command-line arguments. On most modern platform, the first argument is the path of the executable.

 1. `int main(int argc, char* argv[], EXTRA_PLATFORM_SPECIFIC_PARAMS)`

    Same as the above except extra arguments are supplied that are platform-specific.

All three forms return an integer known as an exit code. On most modern day platforms, an exit code of 0 means success. If the code doesn't return an exit code, 0 is assumed.

```c++
#include <iostream>

int main(int argc, char* argv[]) {
    std::cout << "hello world!" << ' ' << argv[0];
    return 0;
}
```

```{note}
Should `argv` be `const char * const *`? In that you shouldn't be able to change the strings or the string pointer at each array index.
```

## Variadic

A variadic function is one that takes in a variable number of arguments, sometimes called varargs in other languages. A function can be made variadic by placing `...` as the final parameter. The arguments for this final parameter are called the variadic arguments.

The variadic arguments for a function are accessible through functionality provided by the cstdargs header.

```c++
#include <cstdargs>

float avg(size_t n, ...) {
    va_list args;
    va_start(args, n);
    float sum {0};
    while (size_t i {0}; i < n; i++) {
        sum += va_args(args, float);
    }
    va_end(args);
    return sum /= n;
}
```

 * `va_list` - Access point to variadic arguments.
 * `va_start` - Initializes access to variadic arguments (requires the `va_list` variable and the expected count of variadic arguments).
 * `va_args` - Gets the next variadic argument (requires the `va_list` variable and the expected type).
 * `va_end` - Tears down access to the variadic arguments (requires the `va_list` variable).

In addition, the `va_copy()` can be used to copy one `va_list` to another. The source will need to be initialized before the copy (via `va_start`). Once `va_copy` returns, copy will already be initialized (no need for `va_start`) but will need to be torn down before the function exits (via `va_end`).

```c++
#include <cstdargs>

float add_and_mult(size_t n, ...) {
    va_list args;
    va_list args2;
    va_start(args, n);
    va_copy(args2, args);  // 1st param is dst, 2nd param is src
    float res {0};
    while (size_t i {0}; i < n; i++) {
        res += va_args(args, float);
    }
    va_end(args);
    while (size_t i {0}; i < n; i++) {
        res *= va_args(args2, float);
    }
    va_end(args2);
    return res;
}
```

```{note}
The book recommends against using variadic functions due to confusing usage and having to explicitly know the count and types of the variadic arguments before hand (can become security problem is screwed up). Instead it recommends using variadic templates for functions instead.
```

## No Exception

In certain cases, it'll be impossible for a function to throw an exception. Either the function (and the functions it calls into) never throws an exception or the conditions imposed by the function make it impossible for any exception to be thrown. In such cases, a function may be marked with the `noexcept` keyword. This keyword allows the compiler to perform certain optimizations that it otherwise wouldn't have been able to, but it doesn't necessarily mean that the compiler will check to ensure an exception can't be thrown.

```c++
int add(int a, int b) noexcept {
    return a + b;
}
```

```{note}
The book mentions this is documented in "Item 16 of Effective Modern C++ by Scott Meyers". It goes on to say that, unless specified otherwise, the compiler assumes move constructors / move-assignment operators can thrown an exception if they try to allocate memory but the system doesn't have any. This prevents it from making certain optimizations.
```

## Common Attributes

If a function has no possibility of ever gracefully returning to the caller, adding a `[[noreturn]]` attribute will allow the compiler to make certain optimizations and provide / remove relevant warnings around that function.

```c++
[[noreturn]] int add(int a, int b) {
    throw "error";
}
```

If a function returns something and it's of vital importance that the return value should be used by the invoker, adding a `[[nodicard]]` attribute will allow the compiler to generate a warning.

```c++
[[nodiscard]] Result perform(int a) {
    // perform some computation
    if (result < 0) {
        return ERROR_CODE;
    }
    return SUCCESS_CODE;
}
```

If a function's parameter isn't used but it's inclusion in the parameter list is intentional, adding a `[[maybe_used]]` attribute will allow the compiler to remove any warnings that it might otherwise show up about it being unused.

```c++
int add(int a, int b, [[maybe_unused]] int c) {
    return a + b;
}
```

If a function has been deprecated, adding a `[[deprecated]]` attribute will allow the compiler to generate a warning if it it being used.

```c++
[[deprecated("Warning -- this is going away in the next release")]]
int add(int a, int b) {
    return a + b;
}
```

## Coroutines

A coroutine that can suspend its own execution and have it be continued at a later time. Similar to async functions in Javascript, C++ coroutines can work with promise objects (objects that do work asynchronously). A function can be made into a coroutine by using any of the following: 

 * `co_await` - suspend execution waiting for a promise to finish.
 * `co_yield` - suspend execution and optionally return a value. 
 * `co_return` - complete execution and optionally return a value.

The return value of a coroutine is a "promise type", a C++ class that has a specific structure and specific set of functionality that the compiler calls to determine and control the coroutine's state.

```{note}
This is deeply convoluted and requires a lot more digging and documentation, possibly in its own section instead of sub-section under the Function header.
```

```c++
#include <iostream>
#include <cstdlib>
#include <coroutine>

struct Resumable {
    struct promise_type; // forward declaration
    Resumable(std::coroutine_handle<promise_type> coro) : coro(coro) {}
    ~Resumable() {
        coro.destroy();
    }
    void destroy() { coro.destroy(); }
    void resume() { coro.resume(); }
private:
    std::coroutine_handle<promise_type> coro;
};

struct Resumable::promise_type {
    auto get_return_object() { return Resumable(std::coroutine_handle<Resumable::promise_type>::from_promise(*this)); }
    auto initial_suspend() { return std::suspend_never(); }
    auto final_suspend() noexcept { return std::suspend_never(); }
    auto yield_value(int value) {
        current_value = value;
        return std::suspend_always{};
    }
    void return_void() { }
    void unhandled_exception() { }
    int current_value;
};

Resumable range(int start, int end) {
    while (start < end) {
        co_yield start;
        std::cout << start << '\n';
        start++;
    }
    co_return;
}

int main() {
    auto x {range(0, 10)};
    x.resume();  // prints 0
    x.resume();  // prints 1
    x.resume();  // prints 2
}
```

```{note}
It's said that the coroutine state is kept on the stack, resulting in C++ coroutines being a performance hog. Maybe it's possible to use a custom allocator to work around performance problems?
```

# Enumerations

C++ enumerations are declared using `enum class`.

```c++
enum class MyEnum {
   OptionA,
   OptionB,
   OptionC
};

MyEnum x {MyEnum::OptionC};

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

An enumeration may be brought into scope via `using` to removing the need to prefix with the enumeration's name.

```c++
switch (x) {
    using enum MyEnum;
    case OptionA:
        ...
        break;
    case OptionB:
        ...
        break;
    case OptionC:
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

MyEnum x {OptionC}; // this is okay -- don't have to use MyEnum::OptionC
int y {OptionC};    // this is okay -- options are integers
```

You should prefer `enum class`.
````

# Classes

C++ classes are declared using either the `struct` keyword or `class` keyword. When ...

 * `struct` is used, the default visibility of class members is public.
 * `class` is used, the default visibility of class members is private.

Public and private visibility are the same as in most other languages: private members aren't accessible outside the class while public members are. In C++ nomenclature, ...

 * methods are commonly referred to as member functions. 
 * fields are commonly referred to as member variables.

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

## This Pointer

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

## Constant

For fields of a class, a `const` before the type has the same meaning as a `const` type at global scope: It's unmodifiable.

For methods of a class, a `const` after the parameter list indicates that the class's fields won't be modified (read-only). This is a deep check rather than a shallow check, meaning that the entire call graph is considered when checking for modification.

```c++
struct Inner {
    int x {5};
    int y {6};
    void change(int n) {
        x = n;
    }
};

struct X {
    int a {0};
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

## Volatile

For fields of a class, a `volatile` before the type has the same meaning as a `volatile` type at global scope: The compiler won't optimize its access.

For methods of a class, a `volatile` after the parameter list indicates that all fields should be treated as `volatile` (access won't be optimized away or re-ordered). This is a deep check rather than a shallow check, meaning that the entire call graph requires `volatile`.

```{note}
Another way to think of this is that the `volatile` on a method makes it treat the instance of the class as if the variable that was declaring it were `volatile` -- meaning all of its members are treated as `volatile` recursively down the object tree.
```

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

## Common Attributes

If a class has been deprecated, adding a `[[deprecated]]` attribute will allow the compiler to generate a warning if it sees it being used.

```c++
[[deprecated("Warning -- this is going away in the next release")]]
int add(int a, int b) {
    return a + b;
}
```

## Static

For fields of a class, a `static` before the type indicates that the function is independent of any instances of the class type: a static field points the same memory across all instances.

For methods of a class, a `static` before the return type indicates that the function is independent of any instances of the class type, meaning that the only class fields that a `static` method can access are `static` fields.

`static` methods and fields are accessed using the scope resolution (::) operator, where the scope is the class itself.

```c++
struct X {
    static int a {1};
    int b {0};
    static void double_it() {
        a *= 2; 
    }
};

X::double_it();  // call using scoped resolution
```

```{note}
Be careful, `static` has a different meaning for functions than it does for methods.
```

## Construction

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

## Destruction

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

Destructors must never be called directly by the user. Treat any destructor as if it were marked with `noexcept`. That is, an exception should never be thrown in a destructor. When an exception gets thrown, the call stack unwinds. As each function exits, the destructors for automatic variables of that function get invoked. Another exception getting thrown while one is already in flight means two exceptions would be in flight, which isn't supported.

If a destructor isn't declared, an empty one is implicitly generated.

## Copying

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

## Moving

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

## Inheritance

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

To be able to override a method in a child class the same way as its done in other languages (e.g. Java), the base call must have the `virtual` keyword prepended on the method, making it a virtual method. Similarly, any method that overrides a virtual method should have the `override` keyword appended just after the parameter list.

```{note}
`override` isn't strictly required, but it's a hint that the compiler can use to prevent you from making a mistake (e.g. it sees `override` but what's being overridden isn't `virtual`). It's similar to Java's `@Override` annotation.
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

To prevent a method from being overriddable at all, add the `final` keyword just after the parameter list.

```c++
struct MyParent {
    virtual int methodA() final { ... }
};

struct MyChild : MyParent {
    virtual int methodA() { ... }  // ERROR HERE -- not allowed
};
```

Similarly, to prevent the entire class itself from being inheritable, add the `final` keyword just after the name.

```c++
struct MyParent final {
    virtual int methodA() { ... }
};
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


MyParent *c {new MyChild{}};
delete c;  // calls MyParent's destructor instead of MyChild's destructor
```

When inheritance is involved, it's almost always a good idea to enforce a virtual destructor. Since not having a virtual destructor sometimes makes sense (e.g. user determined that it's safe to omit it and as such omitted it to improve performance), the compiler won't produce a warning if it isn't virtual.

```c++
struct MyParent {
    virtual int v1() { ... };
    virtual ~MyParent() { ... };
};
```

## Interfaces

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

## Operator Overloading

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
MyClass operator+(const MyClass &lhs, int rhs) {
    MyClass ret { lhs.value + x };
    return ret;
};

// MyClass + MyClass
MyClass operator+(const MyClass &lhs, const MyClass &rhs) {
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
MyClass operator+(const MyClass &lhs, const MyClass &rhs) {
    MyClass ret { lhs.value + rhs.value };
    return ret;
}
```

Those `const`s ensures that the operands aren't changed in the method. Imagine that you're performing `x = y + z`. It doesn't make sense for `y` or `z` to get modified.

The signature could have just as well been modified to be the types themselves rather than `const` references, in which case both the left-hand side and right-hand side would get copied on invocation of the method (modifications to copies don't matter).

```c++
MyClass operator+(MyClass lhs, MyClass rhs) {
    MyClass ret { lhs.value + rhs.value };
    return ret;
}
```

```{note}
See [here](https://gist.github.com/beached/38a4ae52fcadfab68cb6de05403fa393) for a list of operators and their signatures (still incomplete).

There's also the option to create operators that allow for implicit type casting and explicit type casting. See the type casting section for more information.
```

## Three-way Comparison Overloading

The three-way comparison operator, also called the spaceship operator, is a more terse way of providing comparison operators for a class. Typically, if a class is sortable and comparable, it should provide operator overloads for the typical comparison operators:

 * equality (==)
 * inequality (!=)
 * less-than (<)
 * less-than or equal (<=)
 * greater-than (>)
 * greater-than or equal (>=)

The three-way comparison operator bundles the at least the last four of those (potentially all of them) into a single operator, where the symbol for that operator is an equal-sign sandwiched between angle brackets (\<=\>).

```c++
struct MyClass {
    int hour;
    int minute;
};

std::strong_ordering operator<=>(MyClass& lhs, MyClass& rhs) const {
    if (lhs.hour < rhs.hour) {
        return std::strong_ordering::less;
    } else if (lhs.hour > rhs.hour) {
        return std::strong_ordering::greater;
    } else {
        if (lhs.minute < rhs.minute) {
            return std::strong_ordering::less;
        } else if (lhs.minute > rhs.minute) {
            return std::strong_ordering::greater;
        } else {
            return std::strong_ordering::equal;
        }
    }
}

// Test
MyClass lunch_time {12, 00};
MyClass sleep_time {22, 00};
std::cout << "<= via spaceship operator: " << (lunch_time <= sleep_time) << "\n";
// You can also call the spaceship operator directly:   std::strong_ordering res {lunch_time <=> sleep_time}
```

```{note}
Not sure why but when the above operator overload is a member function (instead of a free function) the compiler starts producing a bunch of warnings.
```

Note that the above is comparing each member variable in the order it's declared. The default operator overload implementation of the spaceship operator will do exactly the same thing. Had the class inherited from some other class, the default implementation would first compare the parent classes (left-right order -- C++ has multiple inheritance) before comparing the member variables in the class itself.

```c++
struct MyClass {
    int hour;
    int minute;
    std::strong_ordering operator<=>(MyClass& rhs) const = default;
};
```

In addition, a default operator overload implementation provides both equality (==) and inequality (!=) support. The operator overload implementation in the first example does not support either -- their operator overloads need to be added manually.

```{note}
See [here](https://stackoverflow.com/a/58780946) for reasoning.
```

There are three types of ordering supported by the spaceship operator:

 * `std::strong_ordering` - equality (==) means that one object may be substituted for the other (they are the same).

   Possible values:

   * `std::strong_ordering::less` for less-than
   * `std::strong_ordering::greater` for greater-than
   * `std::strong_ordering::equal` for equality

   Examples:

   * Comparing circles by their radius. A circle with a radius of 5 is the same as another circle with a radius of 5.

 * `std::weak_ordering` - equality (==) means that one object substitution isn't guaranteed (they may not be the same even though they're equivalent).

   Possible values:

   * `std::weak_ordering::less` for less-than
   * `std::weak_ordering::greater` for greater-than
   * `std::weak_ordering::equivalent` for equivalence (note that this is NOT equality -- it's equivalence)

   Examples:

   * Comparing rectangles by their area: A rectangle that's 1-by-15 has the same area as a rectangle that's 5-by-3, but those rectangles are not the same.
   * Comparing strings while ignoring case: The string `"hello world"` is equivalent to `"HELLO WORLD"`, but the two strings aren't the same.

 * `std::partial_ordering` -- same as `std::weak_ordering`, but with the addition that objects may not being comparable at all.

   Possible values:

   * `std::partial_ordering::less` for less-than
   * `std::partial_ordering::greater` for greater-than
   * `std::partial_ordering::equivalent` for equivalence (Note that this is NOT equality -- it's equivalence)
   * `std::partial_ordering::unordered` the objects weren't comparable

   Examples:
   
   * Comparing floating point numbers: The number `3.5` is not comparable at all to `NaN` (not a number).

The return type defined for the operator overload provides context to the user as to how the objects are comparable.

```{note}
Source of ordering types is [here](https://news.ycombinator.com/item?id=20551212).

[here](https://news.ycombinator.com/item?id=20550165) talks about the importance of choosing the right ordering type.

The rectangle example was lifted from [here](https://blog.tartanllama.xyz/spaceship-operator/).
```


## Conversion Overloading

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
int x {cls}; // triggers operator overload method
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
int x {static_cast<int>(cls)};  // static_cast required to trigger operator overload method
```

```{note}
The book recommends not preferring explicit over implicit because implicit is a source for confusion.

Do these still qualify as operator overloads? Return types should be there.
```

## Const / Volatile Overloading

In addition to following the same function overloading rules as free functions, a member function may be overloaded based on whether the `this` pointer is to a `volatile` and / or `const` object.

```c++
class MyClass {
public:
    int get_data() {
        std::cout << "non-const non-volatile\n";
        counter += 1;
        return counter;
    }
    int get_data() const {
        std::cout << "const non-volatile\n";
        return counter;
    }
    int get_data() volatile {
        std::cout << "non-const volatile\n";
        counter += 1;
        return counter;
    }
    int get_data() volatile const {
        std::cout << "const volatile\n";
        return counter;
    }
private:
    int counter;
};


MyClass c1{};
c1.get_data(); // prints "non-const non-volatile"
const MyClass c2{};
c2.get_data(); // prints "const non-volatile"
volatile MyClass c3{};
c3.get_data(); // prints "non-const volatile"
const volatile MyClass c4{};
c4.get_data(); // prints "const volatile"
```

## Reference Overloading

In addition to following the same function overloading rules as free functions, a member function may be overloaded based on whether the `this` reference is an l-value or r-value. To target ...

 * l-value, add an ampersand (&) after the parameter list
 * r-value, add two ampersands (&&) after the parameter list

The benefit of reference overloading is being able to define a version of the function with efficient move semantics when the object is transient.

```c++
// THIS EXAMPLE WAS LIFTED FROM https://docs.microsoft.com/en-us/cpp/cpp/function-overloading?view=msvc-170#ref-qualifiers
class MyClass {
public:
    MyClass() {/*expensive initialization*/}
    std::vector<int> get_data() & {
        std::cout << "lvalue\n";
        return _data;
    }
    std::vector<int> get_data() && {
        std::cout << "rvalue\n";
        return std::move(_data);
    }
private:
    std::vector<int> _data;
};


MyClass c {};
auto v {c.get_data()}; // get a copy. prints "lvalue".
auto v2 {C().get_data()}; // get the original. prints "rvalue"
```

```{note}
The website said l-value, but does it mean gl-value?
```

## Functors

A functor, also called a function object, is a class that you can invoke as if it were a function because it has an operator overloads for function-call.

```c++
struct MyFunctor {
    int operator()(int y) const { return -y + x; }
private:
    int x {5};
};

MyFunctor inst{};
inst(15);  // computes -15 + 5
```

Functors are useful because they allow for state (via fields) and parameterization (via constructor arguments) but still retain a function-like syntax.

```{note}
Unlike normal functions, functors cannot be assigned to function pointers. See section on function pointers.
```

## Lambdas

Lambdas are unnamed functors (not functions) that are expressed in a succinct form. Lambdas in C++ work similarly to lambdas in other high-level languages. They allow for capturing objects from the outer scope and pulling them into the body, where they can be used for whatever processing the functor's body performs.

```c++
// as a function
struct MyFunctor {
    MyFunctor(int x) {
        this->x = x;
    };
    int operator()(int y) const { return -y + x; }
private:
    int x {5};
};

MyFunction f1{}
f1(42);

// as a lambda
int x {5};
auto f2 = [=] (int y) { return -y + x; };

f2(42);
```

The general syntax of a lambda is as follows: `[captures] (parameters) modifiers -> return-type { body }`.

 * **capture** (required) - Objects to pull in from outer scopes.

   ```c++
   int x {5};
   int y {6};
   auto f1 = [] (int z) -> int { return z / 2; };           // no capture
   auto f2 = [x, y] (int z) -> int { return x + y + z; };   // explicitly copy x and y from outer scope
   auto f3 = [&x, &y] (int z) -> int { return x + y + z; }; // explicitly reference x and y from outer scope
   auto f4 = [=] (int z) -> int { return x + y + z; };      // automatically copy x and y from outer scope
   auto f5 = [&] (int z) -> int { return x + y + z; };      // automatically reference x and y from outer scope
   int t {1};
   auto f6 = [&, y] () -> int { return x + y + t; };        // automatically reference x and t but force y to be a copy
   ```

   Capture lists are essentially the functor's constructor. When the capture was pulled in ...

   * because it was explicitly stated, it's called to as a named capture.
   * automatically, it's called a default capture.

   ```{note}
   The book recommends against default captures.
   ```

   Named captures can also be initializer expressions by adding an equal sign after the name of the capture.

   ```c++
   int x {5};
   int y {6};
   auto f1 = [modified_x=x/2, y] (int z) -> int { return x + y + z; };
   ```

   If used within an enclosing class, the this pointer can be captured.

   ```c++
   auto f1 = [*this] (int z) -> int { return z / 2; };  // capture a COPY OF *this and pass it in as a pointer
   auto f1 = [this] (int z) -> int { return z / 2; };   // capture this as pointer
   ```

   ```{note}
   It's mentioned that prior to C++20, automatic copy capturing (`[=]`) would pull in `this`. That feature has been deprecated.
   ```

 * **parameters** (optional) - Parameter list of functor.

   ```c++
   auto f1 = [] (int x, int y) -> int { return x + y; };
   auto f2 = [] (int x, int y = 99) -> int { return x + y; };  // default args
   auto f3 = [] (auto x, auto y) { return x + y; };            // generic params (compiler deduces types based on usage)
   ```

 * **modifiers** (optional) - Function modifiers.

   ```c++
   auto f1 = [] (int x, int y) constexpr -> int { return x + y; };  // constant expression
   ```
 
 * **return-type** (optional) - Return type.

   ```c++
   auto f1 = [] (int x, int y) { return x + y; };                    // deduced by compiler if not set
   auto f2 = [] (int x, int y) -> int { return x + y; };
   auto f3 = [] (int x, auto y) -> decltype(x+y) { return x + y; };  // generic param + decltype (compiler sets return type to resulting type of x + y)
   ```

 * **body** (required) - Function body.

   ```c++
   auto f1 = [] (int x, int y) { return x + y; };
   ```

If the compiler decides that a lambda can be turned into a constant expression, it will automatically do so. Alternatively, you can force a lambda to be a constant expression by adding `constexpr` as one of the modifiers.

```{note}
In many cases, you need to return a lambda from a function. The easiest way to do this is to set the function's return type to `auto` and return the lambda as if it were any other variable.
```

## Friends

A friend is a function or class that can access the non-public members of some other class that it wasn't declared in.

For friend functions, the class to be accessed needs to declare the function's prototype (function declaration) before implementations of a friend function (function definition) can exist. The prototype is included in the class just like any other member function, but the `friend` prefix modifier is tacked on.

```c++
class MyClass {
public:
    friend int addAndNegate(MyClass& obj, int n);  // prototype
private:
    int x {0};
};

int addAndNegate(MyClass& obj, int n) {  // implementation -- friend of MyClass
    return -(n + obj.x);
}

// test
MyClass obj{};
cout << addAndNegate(obj,5);
```

For friend classes, the class to be accessed needs to specify which outside class is able to access it using `friend class`.

```c++
class MyClass {
public:
    friend class MyFriend;  // state that MyFriend can access MyClass's non-public members
private:
    int x {0};
};

class MyFriend {
public:
    int addAndNegate(MyClass& obj, int n) {  // function in MyFriend accessing non-public members of MyClass
        return -(n + obj.x);
    }
};


// test
MyFriend obj_friend{};
MyClass obj{};
cout << obj_friend.addAndNegate(obj,5);
```

```{note}
The `class` in `friend class` may be omitted if `MyFriend` was already declared before `MyClass`. Adding the word `class` is a forward declaration -- it tells the compiler to just believe that it exists even though it may not have come across it yet.
```

Friend functions and friend classes may also target templated types.

```c++
class MyClass {
public:
    template<typename T> friend int addAndNegate(MyClass& obj, T n);  // every addAndNegate(MyClass&, T) will be a friend
private:
    int x {0};
};
```

````{note}
This is how C++ provides its equivalent of Java's `Object.toString()`. For each class that you want to be able to print as a string, you implement a templated friend function of the left-shift operator overload (<<) that targets the class `ostream`, making it usable in something like `std::cout`.

```c++
ostream& operator<<(ostream &os, const MyClass &obj) {
    os << obj.x << "\n";
    return os;
}
```

It seems like a convoluted way to do it.
````

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
float x {obj.perform(5, 3)};
```

Declaring templated functions is done in the same manner as templated classes, and using templated functions is done similarly to templated classes: Use the function as if it were a normal function but immediately after the function name add in a common separated list of substitutions sandwiched within angle brackets.

```c++
// declare
template <typename X, typename Y, typename Z, int N>
X perform(Y &var1, Z &var2) {
    return (var1 + var2) * N;
}

// use
float x {perform<float, int, int, 2>(5, 3)};
```

When the template parameters are for types only (not values), it's possible to leave out substitutions during usage. The compiler will deduce the types from the argument you pass in and substitute them automatically.

```c++
// declare
template <typename X, typename Y, typename Z>
X perform(Y &var1, Z &var2) {
    return var1 + var2;
}

// use
float x {perform(5, 3)};  // template arguments omitted, deduced by compiler
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

Similarly, it's possible to use templates with type aliasing to create shorthand names where only some of the template parameters need to be set, called partial templates.

```c++
// declare
template <typename Y, typename Z>
using MyClassPartialTemplate = MyClass<float, Y, Z, 42>;

// use
MyClass<float, int, int, 42> x{}; 
MyClassPartialTemplate<int, int> y{};  // same type as previous line
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

Alternatively, rather than using recursion to exhaustively apply a binary operator, a fold expression may be applied to the parameter pack. A fold expression applies a binary operator to the contents of a parameter pack and return the final result.

The syntax for fold expressions is `...` and the parameter pack's name sandwiched in between the operator, all encapsulated within a pair of brackets. Which side of the operator the `...` appears at defines if the fold expression will be left associative or right associative.

```c++
template<typename... R>
T test(R... args) {
    R l_ass_res = (... - args);  // ((((a-b)-c)-d)-...)
    R r_ass_res = (args - ...);  // (...-(w-(x-(y-z))))
    return l_ass_res + r_ass_res;
}
```

```{note}
Just a heads up that, depending on the operator, associativity matters. For example `((5-4)-3)` is not equal to `(5-(4-3))`.
```

To get the size of a parameter pack, add `...` after the `sizeof` operator.

```c++
template <typename X, typename... R>
size_t calculate_size(R... args) {
    return sizeof...(args);
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

# Unions

C++ unions are a set of variables that point to the same underlying memory. Each union takes up only as much memory as its largest member.

```c++
union MyUnion {
   char raw[100];
   short num_int;
   double num_dbl;
}

MyUnion x;
// set all bytes of raw to 0
for (int i {0}; i < sizeof(x.raw); i++) {
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

# Namespaces

Namespaces are C++'s way of organizing code into a logical hierarchy / avoiding naming conflicts, similar to packages in Java or Python. Unlike packages, namespaces don't use the filesystem to define their logical hierarchy. Instead, the hierarchy is specified directly in code using `namespace` blocks.

```c++
namespace FirstLevel {
    namespace MiddleLevel {
        namespace LastLevel {
            struct MyStruct {
                int count;
                bool flag;
            };
        }
    }
}
```

The nesting in the example above is avoidable via the scope operator (::).

```c++
namespace FirstLevel::MiddleLevel::LastLevel {
    struct MyStruct {
        int count;
        bool flag;
    };
}
```

To use the symbols within a namespace, either include the namespace in symbol or bring all symbols within the namespace to the forefront via the `using` keyword (similar to Java's `import` or Python's `from` / `import`).

```c++
// Use namespace directly.
FirstLevel:MiddleLevel::LastLevel::MyStruct x{};

// Bring all symbols within a namespace to the forefront.
using FirstLevel:MiddleLevel::LastLevel;
MyStruct y{};

// Bring a single symbol within a namespace to the forefront.
using FirstLevel:MiddleLevel::LastLevel::MyStruct;
MyStruct z{};
```

# Linker Behaviour

Modifiers on a variable or function declaration are used to control how the linker behaves. Specifically, the modifiers can ask the linker to automatically ...

 * merge the item that has the modifier applied (`inline`)
 * find the item that has the modifier applied (`extern`)
 * keep hidden the item that has the modifier applied (`static`). 

## Static Linkage

A static function or variable is one that's only visible to other code in the same translation unit. The linker will make sure that the function doesn't intermingle with other translation units.

Static functions/variables have the `static` modifier applied.

```c++
static int add(int a, int b) {
    return a + b;
}
```

```{note}
This is only for non-members (not belonging to a class).

The meaning of `static` changes when the function or variables belongs to a class (method). When applied on a member function, it means that it isn't bound to any instance of the class -- it can't access fields belonging to an instance.
```

## Inline Linkage

An inline function or variable is one that may be defined in multiple different translation units. The linker will make sure all translation units use a single instance of that function/variable even though it may have been defined multiple times.

Inline functions/variables have the `inline` modifier applied.

```c++
int add(int a, int b) inline {
    return a + b;
}
```

```{note}
See [this](https://stackoverflow.com/a/1759575). Typically, the compiler applies `inline` automatically based on what it sees, meaning that it isn't something that should be adding in most cases. The only exception to that seems to be templates? See some of the other answers in the linked stack overflow question.
```

```{note}
The original intent of `inline` was to indicate to the compiler that embedding a copy of the function for an invocation was preferred over an function call. The reason being that is certain cases the code would be faster if it were embedded rather than having it branch into a function call.
```

## External Linkage

An external function or variable is a one that's usable within the translation unit but isn't defined. The linker will sort out where the function is when the time comes.

External linkage functions/variables have the `extern` modifier applied.

```c++
extern int add(int a, int b);
```

```{note}
Sounds similar to forward declaration but across different translation units?
```

# Control Flow

C++ flow control structures are similar to those in other high-level languages (e.g. Java), with the exception that ...

 * it's possible to have initializer statements in control structures other than for loops.
 * jumping to arbitrary labels are allowed (goto statements).

```{note}
An important caveat about loops in C++ from [cppreference.com](https://en.cppreference.com/w/cpp/language/while):

> As part of the C++ forward progress guarantee, the behavior is undefined if a loop that has no observable behavior (does not make calls to I/O functions, access volatile objects, or perform atomic or synchronization operations) does not terminate. Compilers are permitted to remove such loops. 
```

## If Statement

If statements follow a similar structure to if statements in Java. The only major difference is that an initializer statement is allowed before the condition in the initial `if`.

```c++
if (int r {rand()}; r % 2 == 0) {
    std::cout << r << " even";
else if (r % 5 == 0) {
    std::cout << r << " div by 5";
} else {
    std::cout << r << " odd";
}
```

In the example above, an initializer statement has been added that sets a variable to a random number. That variable is only accessible inside the different branches of the if statement.

## Switch Statement

Switch statements follow a similar structure to switch statements in Java. The only major difference is that an initializer statement is allowed before the condition.

```c++
switch (int r {rand()}; r % 2) {
    case 0:
    std::cout << r << " even";
    break;
    case 1:
    std::cout << r << " odd";
    break;
    default:
    std::cout << "this should never happen";
    break;
}
```

To indicate to the compiler that a fallthrough case is intended behaviour, use the `[[fallthrough]]` attribute.

```c++
switch (x) {
    case 0: [[fallthrough]]
    std::cout << r << " even";
    case 1:
    std::cout << r << " odd";
    break;
    default:
    std::cout << "this should never happen";
    break;
}
```

## For Loop

For loops follow a similar structure to for loop in Java.

```c++
for (int i {0}; i < 10; i++)  {
    std::cout << i;
}
```

Similarly, an analog to Java's for-each loop exists called range-based for loops. The only major difference is that an initializer statement is allowed before the range declaration.

```c++
for (int r {rand()}; int val : array)  {
    std::cout << (r + val) << ' ';
}
```

## While Loop

While and do-while loops follow a similar structure to their counterparts in Java.

```c++
int r {rand() % 5};
while (r > 0) {
    std::cout << r << " ";
    r--;
}
```

```c++
int r {rand() % 5};
do {
    std::cout << r << " ";
    r--;
} while (r > 0);  // semicolon required at the end
```

```{note}
Unlike other control structures, these loops cannot have initializer statements.
```

## Goto Statement

Unlike most other high-level languages (e.g. Java), C++ allows the use of goto statements. However, note that goto statements are generally considered bad practice and should somehow be refactored to higher-level constructs (e.g. loops, if statements, etc..).

```c++
retry:
int r {rand()};
if (r % 2 == 0) {
    goto retry;
}
std::cout << r << " odd";
```

## Branching Likelihood

Conditional branching operations in flow control statements may have the `[[likely]]` and `[[unlikely]]` attributes applied to hint at the likelihood / unlikelihood that of the path execution will take. This allows for better optimization by the compiler (based on your assumptions).

```c++
switch (exit_code) {
    case 0:
    // happy path
    break;
    case 1:
    // recognized error path
    break;
    [[unlikely]] default:
    // unrecognized error path
    break;
}
```

```c++
if (is_valid(email)) [[likely]] {
    // happy path
} else {
    // error path
}
```

```c++
while (i > 0) [[unlikely]] {
  // do something
}
```

```{note}
I read something online saying you shouldn't use both `[[likely]]` and `[[unlikely]]` on the same switch/if/while/etc...
```

# Attributes

C++ attributes are similar to annotations in Java, providing information to the user / compiler about the code that it's applied to. Unlike Java, C++ compilers are free to pick and choose which attributes they support and how they support them. There is no guarantee what action a compiler will take, if any, when it sees an attribute (e.g. compiler warnings).

An attribute is applied by nesting it in double squared brackets (e.g. `[[noreturn]]`) and placing it as a modifier on the function.

```c++
[[noreturn]] void fail() {
    throw std::runtime_error { "Failed" };
}
```

Common attributes:

| Attribute               | Description                                                                                                                     |
|-------------------------|---------------------------------------------------------------------------------------------------------------------------------|
| `[[deprecated("msg")]]` | Indicates that a function is deprecated. Message is optional.                                                                   |
| `[[noreturn]]`          | Indicates that a function doesn't return.                                                                                       |
| `[[fallthrough]]`       | Indicates that a switch case was explicitly designed to fall through to the next case (no `break` / `return` / etc.. intended). |
| `[[nodiscard]]`         | Indicates that a function's result should be used somehow (produce compiler warning).                                           |
| `[[maybe_unused]]`      | Indicates that a function's result doesn't have to be used (avoid compile warning).                                             |


# Constant Expressions

A constant expression is an expression that gets evaluated at compile-time, such that any invocation of it gets swapped out for the result computed at compile-time. It comes in two forms: variable and function.

A constant expression variable requires using `constexpr` instead of `const`. The difference between a `const` variable and `constexpr` variable is that the former only guarantees the variable is unmodifiable. It doesn't actually guarantee that the expression within is evaluated at compile-time.

```c++
const int x {5 + 5};      // COULD BE evaluated at run-time or compile-time, but guaranteed to be unmodifiable
constexpr int y {5 + 5};  // MUST BE evaluated at compile-time and guaranteed to be unmodifiable
```

Similarly, a constant expression function requires prefixing `constexpr` to a function. The entire compilation can be terminated at any point through the use of `static_assert`.

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

````{note}
An alternate version of constant expression functions, called immediate functions, have the restriction that they must produce a compile-time constants. An immediate function requires a requires prefixing `consteval` to a function instead of `constexpr`.

What's the point on this? According to [here](https://stackoverflow.com/a/53347377)...

> constexpr functions may be evaluated at compile time or run time, and need not produce a constant in all cases.

Here's an example from [here](https://github.com/AnthonyCalandra/modern-cpp-features)...

```c++
consteval int sqr(int n) {
  return n * n;
}

constexpr int r {sqr(100)}; // OK
int x {100};
int r2 {sqr(x)}; // ERROR: the value of 'x' is not usable in a constant expression
                 // OK if `sqr` were a `constexpr` function
```
````

The restrictions on constant expressions are vast. At a high-level, a constant expression is only allowed inputs and outputs that are literal types:

 * **Scalar**: Floating point types, integral types, pointer types, enumeration types, `std::nullptr_t`, etc..
 * **Reference**
 * **Array**: Every element must be a literal.
 * **Class**: Constructor must be a constant expression. Non-static fields initializers using braced initialization, equals initialization, or brace-plus-equals initialization must use constant expressions. The destructor must be a trivial destructor (non-virtual, does nothing, and all base class destructors do nothing).
 * **Union**: Must have at least one non-static member that is a literal type.

```{note}
The rules here are vast and complicated. The above might not be entirely correct, may be missing some conditions, or may not cover certain aspects. In the type_traits header, there's a function called `std::is_literal_type` that can be used to test if a type is a literal type.
```

There are several benefits to constant expressions. First, constant expressions help with reducing the use of hard coded numbers whose origins are obtuse, called magic numbers. A constant expression uses the computation to get to that obtuse magic number rather than the number itself, meaning its easier to understand and requires less effort to tweak (via the parameters of the constant expression).

Second, there exists a special type of compile-time if-else where the chosen path is the only one in which code is generated for. These compile-time if-elses, identified by the `constexpr` keyword immediately after the `if`, use constant expressions in their conditionals when deciding which path to choose. These are use-cases such as ...

 * omitting parts of a program from compilation (e.g. demonstration software).
 * working around compiler-specific / platform-specific inconsistencies (e.g. only include code if `int`'s max value is above some threshold).
 * performing specific actions based on the types chosen for template parameters (e.g. include code path 1 if pointer, otherwise code path 2).

```c++
if constexpr (y == sizeof(int)) {
    // constant expression y is equivalent to the number of bytes for an int, so compile this block
    ...
} else {
    // constant expression y is NOT equivalent to the number of bytes for an int, so compile this block
    ...
}
```

```{note}
Type information is queryable at compile-time through the type_traits. Information about numeric types is queryable at compile-time using numeric_limits, cstdlib, and cfloat headers.

Those are what you would commonly use in `if constexpr` blocks. They help with building portable software.
```

```{note}
All of this seems to replace the need for C preprocessor macros `#define` / `#ifdef` / etc...
```

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

# Structured Binding

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
int a { 0 }; // move -- 0 is being generated and MOVED into a (the expression 0 is a prvalue)
//      ^
//      |
//   rvalue

int b { a }; // copy -- a already exists and its being COPIED into b (the expression a is NOT a prvalue)
```

In essence, the way to think of a prvalue is that its an expression that meets the following 3 conditions ...

1. can't have the address-of operator used on it.

   ```c++
   MyStruct* a {&MyStruct(true)}; // error -- right-hand expression is transient, not a var that you can get the address of   
   int* b {&(5)}                  // error -- right-hand expression is a literal, not a var that you can get the address of
   int* c {&get_int()}            // error -- right-hand expression is the return val of function, not a var that you can get the address of
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
MyObject &&b {std::move(a)};  // get rvalue reference
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

# Iterators

Iterators in C++ are similar to iterators in Java. In Java, objects that...

 * produce an iterator typically implement the `Iterable` interface (e.g. `ArrayList`)
 * are iterators must implement the `Iterator` interface.

In C++, there is no requirement to extend from any base classes or interfaces. Instead, any type can act as an iterator so long as it supports as set of operators:

 * `!=` - test if the position of one iterator doesn't match the position of another iterator (e.g. `my_iterator != end_iterator`).
 * `++` - move to the next item (e.g. `my_iterator++`).
 * `*` (dereference) - access the next item (e.g. `int value {*my_iterator}`).

```{note}
Notice that the operators are more or less array / pointer behaviour. Given something like `int *` pointing to the beginning of an array, ...

 * incrementing it by 1 (`++`) moves it to the next element of the array via pointer arithmetic.
 * dereferencing it (`*`) provides the value at the array element its points to.
 * testing it using inequality (`!=`) is a way to check if it hasn't gone past the last array element.

An iterator is basically a set of operators that walk elements in the same way as you would an array. A class can implement the operator overloads and behave the same way.
```

Similarly, any class can act as an iterable by implementing begin and end methods, commonly referred to as a range:

 * `begin()` - returns an iterator pointing to the first item.
 * `end()` - returns an iterator pointing to _past-the-end_ (just after the last element).

```c++
MyIterator it {collection.begin()};
while (it != collection.end()) {
    MyObject value {*it};
    // do something with value here
    ++iterator;
}
```

C++ iterables and iterators can be used together in range-based for loops.

```c++
for (MyIterator it : collection) {
    MyObject value {*it};
    // do something with value here
}
```

In total, 5 kinds of iterators are supported by C++. The kind of iterator described above is called an input iterator and it typically requires an equality operator overload (`operator ==()`) in addition to inequality. Input iterators are the closest thing to a standard Java `Iterator` -- read-only and forward-only. Other kinds of iterators require different operator overloads.

 * Input iterator, steps forwards one element at a time and reads items of the container.
 * Output iterator, steps forwards one element at a time and writers items of the container.
 * Forward iterator, combination of input iterator and output iterator.
 * Bidirectional iterator, forward iterator with the ability to move back.
 * Random access iterator, bidirectional iterator with the ability to jump to different positions.

|                                                               | Input | Output | Forward | Bidirectional | Random access |
|---------------------------------------------------------------|-------|--------|---------|---------------|---------------|
| `++it` and `it++` (move forward)                              |   ✓   |    ✓   |    ✓    |      ✓        |       ✓       |
| `--it` and `it--` (move backward)                             |       |    ✓   |    ✓    |      ✓        |       ✓       |
| `it1 == it2` and`it1 != it2` (test if at same position)       |   ✓   |    ✓   |    ✓    |      ✓        |       ✓       |
| `it1 < it2` (test if before)                                  |       |        |         |               |       ✓       |
| `it1 <= it2` (test if before or at)                           |       |        |         |               |       ✓       |
| `it1 > it2` (test if after)                                   |       |        |         |               |       ✓       |
| `it1 >= it2` (test if after or at)                            |       |        |         |               |       ✓       |
| `x = *it` (dereference and get)                               |   ✓   |        |    ✓    |      ✓        |       ✓       |
| `*it = x` (dereference and set)                               |       |    ✓   |    ✓    |      ✓        |       ✓       |
| `it1 += n` and `it1 + n` (add integer)                        |       |        |         |               |       ✓       |
| `it1 -= n` and `it1 - n` (subtract integer)                   |       |        |         |               |       ✓       |
| `it2 - it1` (subtract iterators to get positional difference) |       |        |         |               |       ✓       |
| `it1 + it2` (add iterators)                                   |       |        |         |               |               |

```{note}
Note that the adding of iterators is listed above but is not supported by any of the iterator types. It's there to make it explicit that adding together two iterators isn't a thing.
```

```{note}
If you're dealing with the STL, there's also special iterator implementations that allow insertions rather than setting elements. See `insert_iterator`, `back_insert_iterator`, and `front_insert_iterator`.
```

# Modules

```{note}
Source is [this website](https://vector-of-bool.github.io/2019/03/10/modules-1.html).
```

C++ modules change how C++ source code files interface with each other. Normally, a C++ source / header file would use `#include <...>` directives to pull in other source code files that it needs access to. Those outside source code files provided things like preprocessor macros, function declarations, class declarations, global variable constants, forward declarations, templates, etc...

Instead of dealing with source code files directly, C++ modules allow for independently "compiling" source code files and importing them for use into different source code files, similar to how a Java source code file imports compiled Java class files for use. Modules reduce some of the complexities of using header files but certain functionality is also gone. Specifically, before modules go through compilation, preprocessor macros and preprocessor directives aren't included.

To create a module from a single file, add `export module` followed by the name of the module in the beginning of the file. Then, prefix `export` to any function, enumeration, class, etc.. that the module should expose.

```c++
export module my_module;

export int add(int a, int b) {
   return a + b;
}

export int multiply(int a, int b) {
   return a * b;
}
```

To make use of a module in some other source code, use `import` followed by the module's name.

```c++
import my_module;

int main() {
   return add(1, 2);
}
```

Similar to how non-module C++ source code is broken up into a source file containing definitions and its accompanying header file would containing declarations, a module may also be broken up into separate definition and declaration files. The declarations go in a file with `export module` at the top (as shown above) and the definitions go in a file with just `module`. Declaration files aren't allowed to use `export` at all.

```c++
// my_module.cpp
export module my_module;
export int add(int a, int b);
export int multiply(int a, int b);

// my_module_impl.cpp
module my_module;  // no "export" in module declaration, meaning export not allowed anywhere else in this file
int add(int a, int b) {
   return a + b;
}
int multiply(int a, int b) {
   return a * b;
}
```

Modules may be broken up into several pieces using module partitions, with each piece in its own file, using colons (:).

```c++
// my_module_addition.cpp
export my_module:addition;
export int add(int a, int b) {
   return a + b;
}

// my_module_multiplication.cpp
export my_module:multiplication;
export int multiply(int a, int b) {
   return a * b;
}

// my_module.cpp
export module my_module;
export import :addition;        // export everything under my_module:addition partition
export import :multiplication;  // export everything under my_module:multiplication partition
```

Module partitions may be made non-exportable as well, similar to the definition / declaration example earlier. The parent would need to re-define anything it wants to explicitly export.

```c++
// my_module_addition.cpp
export my_module:addition;
int add(int a, int b) {
   return a + b;
}

// my_module_multiplication.cpp
my_module:multiplication;
int multiply(int a, int b) {
   return a * b;
}

// my_module.cpp
export module my_module;
import :addition;
import :multiplication;
export int add(int a, int b);      // explicitly export this function (imported from my_module:addition partition)
export int multiply(int a, int b); // explicitly export this function (imported from my_module:multiplication partition)
```

Note that there can only ever be 1 parent for a partition. All partitions are a part of their parent module, not modules themselves. The parent module must import all of its partitions using either `import` or `export import` as shown in the examples above. No module can directly import a partition that doesn't belong to it.

One way to work around these restrictions is to simply make the partitions their own modules. The most common way to do this is to replace the colons (:) in each partition name with a dot (.), making sure to use the full name in the import lines (because the pieces being imported are no longer partitions of the parent module).

```c++
// my_module_addition.cpp
export my_module.addition;
export int add(int a, int b) {
   return a + b;
}

// my_module_multiplication.cpp
export my_module.multiplication;
export int multiply(int a, int b) {
   return a * b;
}

// my_module.cpp
export module my_module;
export import my_module.addition;        // export everything under my_module.addition (FULL NAME USED)
export import my_module.multiplication;  // export everything under my_module.multiplication (FULL NAME USED)
```

```{note}
Last I recall using this, each compiler required a special flag to turn on modules. Just because you're code uses modules doesn't mean the internal C++ libraries (e.g. standard template library, `cstdint`, etc..) are going to expose things as modules. You still have to include those using the `#include <...>` directives (maybe -- I think I remember there being some roundabout way of getting modules to work).
```

# Preprocessor

The preprocessor is a component of the C++ compiler. Before the programming statements in a source code file are compiled, the processor goes over the file looking for preprocessor directives. Preprocessor directives either...

1. perform some basic text manipulation.
1. signal certain things to the compiler (e.g. use a specific feature, turn off a specific feature, etc..).

The first case (text manipulation) is primarily what the preprocessor is used for. Unlike normal C++ programming statements, preprocessor directives start with the pound sign (#) and shouldn't include a semicolon (;) at the end.

To include one file in another file, use `#include`. Local files should be wrapped in quotes while files coming from libraries should be wrapped in a angled brackets.

```c++
#include <vector>          // library header
#include "OtherClass.hpp"  // local header
```

To replace strings in a file with another string, use `#define`.

```c++
#define INITIAL_VALUE 500
int x {INITIAL_VALUE};
int y {INITIAL_VALUE};
```

To replace strings in a file with a _parameterized replacement_, use `#define` with parenthesis.

```c++
#define ADDED_VALUE(x, y) x + y - 15
int x {ADDED_VALUE(1, 7)};
int y {ADDED_VALUE(5, 3)};
```

To stop replacing a string, use `#undef`.

```c++
#define INITIAL_VALUE 500
int x {INITIAL_VALUE};
#undef INITIAL_VALUE
#define INITIAL_VALUE 8
int y {INITIAL_VALUE};
```

To conditionally include / ignore portions of a file, use an `#ifdef` / `#else` / `#endif` block.

```c++
#ifdef INITIAL_VALUE
int x {INITIAL_VALUE};
#else
int x {ADDED_VALUE(1, 7)};
#endif
```

Similarly, `#ifndef` may be used to conditionally include / ignore portions of a file (`#ifndef` -- note the n, if NOT defined).

```c++
#ifndef INITIAL_VALUE
int x {ADDED_VALUE(1, 7)};
#else
int x {INITIAL_VALUE};
#endif
```

Conditional inclusion preprocessor directives come in an alternate form that allows for more flexible conditions: `#if` / `#elif` /`#else` / `#endif` block.

```c++
#if !defined INITIAL_VALUE
int x {1}
#elif INITIAL_VALUE > 50
int x {INITIAL_VALUE - 50}
#else
int x {INITIAL_VALUE}
#endif
```

```{note}
Compiler / compilation options may be controlled through `#pragma`s. I've left `#pragma`s out of the document because they're specific to the compiler and platform.
```

# Inconsistent Behaviour

High-level languages are typically very consistent. For example, except for a handful of small things, Java's runtime and core libraries are consistent across different platforms (e.g. Windows vs Linux), architectures (e.g. ARM vs x86), and compilers (e.g. OpenJDK vs Eclipse compiler). C++ has much less consistency than those other high-level languages because it has to support more platforms and architectures. In addition, having less consistency sometimes allows for more aggressive optimization during compilation.

Inconsistencies comes in three different types:

* Implementation-defined behaviour: Behaviour varies between implementations, where that behaviour is valid (e.g. no hard crash) and documented.
* Unspecified behaviour: Behaviour varies between implementations, where that behaviour is valid (e.g. no hard crash) but _not_ documented.
* Undefined behaviour: Behaviour is unrestricted (e.g. maybe hard crash, bad computation, or expected computation) and not documented.

|                                  | Valid | Documented |
|----------------------------------|-------|------------|
| Implementation-defined behaviour | YES   | YES        |
| Unspecified behaviour            | YES   | NO         |
| Undefined behaviour              | MAYBE | NO         |

## Implementation-defined Behaviour

Implementation-defined behaviour is behaviour that varies between implementations, where that behaviour is valid (e.g. no hard crash) and documented. The obvious example is with numeric data types: `short`, `int`, `float`, etc.. will each have a different minimum and maximum across different platforms:

 * `short` is from `SHORT_MIN` to `SHORT_MAX`.
 * `int` is from `INT_MIN` to `INT_MAX`.
 * ...

```{note}
Someone posted up [this](http://eel.is/c++draft/impldefindex) as a comprehensive list of implementation-defined behaviour.
```

## Unspecified Behaviour

Unspecified behaviour is behaviour that varies between implementations, where that behaviour is valid (e.g. no hard crash) but _not_ documented. The obvious example is the order in which operands are evaluated in an expression. For example, consider the following statement ...

```c++
int x {bird_func() / cow_func()};
```

The results of `bird_func()` and `cow_func()` may be gotten in any order prior to performing the division. There is no requirement as to which one gets invoked first. The division itself with the correct operands in the correct spots, but which function gets called first is up to the compiler.

```c++
// option1  -- bird_func() evaluated first
int a {bird_func()};
int b {cow_func()};
int x {a / b};

// option2  -- cow_func() evaluated first
int b {cow_func()};
int a {bird_func()};
int x {a / b};
```

Another example is the memory representation of core types (e.g. integral types). The platform's memory layout could be either big-endian, little-endian, or some other uncommon memory layout.

```c++
int x {5};
// big endian:    00 00 00 05  (e.g. ARM)
// little endian: 05 00 00 00  (e.g. x86)
```

The above doesn't matter unless you're trying to read raw contents of core types (e.g. for serializing classes to disk).

```{note}
I wasn't able to find a comprehensive list of what the C++ spec considers as unspecified behaviour.
```

## Undefined Behaviour

```{note}
According to documentation online: "Compilers are not required to diagnose or do anything meaningful when undefined behaviour is present. Correct C++ programs are free of undefined behaviour". Not exactly sure how to fix some scenarios to be "free" of undefined behaviour. Specifically, there are a lot of cases where signed integer overflow (described below) happens, but that's undefined behaviour. I read online that the way to handle these cases is to test at the beginning of the function if overflow is possible and bail out if it is, but there's no built-in C++ mechanism to do that.

The statement and the examples below, were lifted from [here](https://en.cppreference.com/w/cpp/language/ub).
```

Undefined behaviour is behaviour that is unrestricted and not documented. The compiler may do anything for code producing undefined behaviour. For example, code producing undefined behaviour could end up ...

 * causing a hard crash.
 * doing exactly what the the author of the source code originally intended for.
 * doing something different than what the author of the source code originally intended for.
 * causing the program to not immediately crash, but potentially much later.

None of the examples have to be consistent. For example, it could produce a hard crash some of the time and the intended results the rest of the time.

 * Signed integer overflow

   Although signed integers are guaranteed to be two's complement (as of C++20), what happens when a signed integer overflows is still undefined behaviour. In many cases, the compiler will treat signed integer operations as if overflowing isn't possible. For example, consider the following function ...
   
   ```c++
   bool test(int x) {
       return x < x + 1;
   }
   ```

   What may happen: The compilers will optimize away the return expression to always return `true`. Had signed integer overflow NOT been undefined behaviour, the function would return `true` except in the case where `x == INT_MAX`: When `x == INT_MIN`, the expression `x + 1` would rollover to `INT_MIN`, leading `x < x + 1` to evaluate to `false`.

 * Array out of bounds access

   Array out of bounds access typically ends up touching memory past the array's boundaries.
   
   ```c++
   int data[5] {1,2,3,4,5};
   data[65535] {15};
   ```

   What may happen: Out of bounds data access will result in either...

    * the reading/writing of some other object's memory (e.g. corruption of another object, if writing).
    * the reading/writing of memory not assigned to an object.
    * a crash.

 * Uninitialized scalar

   Uninitialized scalars are scalars that are read before being written to.

   ```c++
   int x;
   std:cout << x; // what's in x? 
   ```

   What may happen: Uninitialized scalars contain junk data (e.g. whatever was in the memory before).

   ```{note}
   Scalar typically means arithmetic type or pointer / reference type. See [this](https://stackoverflow.com/a/14822074).
   ```
   
 * Invalid scalar

   When a scalar gets reinterpreted as something else (e.g. a byte array) and its contents are manipulated, reading from that original scalar is undefined behaviour.

   ```c++
   // EXAMPLE FROM https://en.cppreference.com/w/cpp/language/ub
   int f() {
       bool b {true};
       unsigned char* p {reinterpret_cast<unsigned char*>(&b)};
       *p {10};
       // reading from b is now UB
       return b == 0;
   }
   ```

   What may happen: modifications on the reinterpretation are treated as if it never happened.

   ```{note}
   Scalar typically means arithmetic type or pointer / reference type. See [this](https://stackoverflow.com/a/14822074).
   ```

 * Null pointer dereference

   ```c++
   // EXAMPLE FROM https://en.cppreference.com/w/cpp/language/ub
   int foo(int* p) {
       int x {*p};
       if(!p) return x; // Either UB above or this branch is never taken
       else return 0;
   }
   int bar() {
       int* p {nullptr};
       return *p;        // Unconditional UB
   }
   ```

   What may happen: Trying to read or write to a dereferenced `nullptr` will cause a crash.

 * Side-effect free infinite loops

   A side-effect free infinite loop is a loop goes on forever but doesn't change anything outside of its own scope (e.g. no global variable is changed, nothing is printed to standard out, etc..).

   ```c++
   // EXAMPLE FROM https://en.cppreference.com/w/cpp/language/ub
   while (1) {
       if (((a*a*a) == ((b*b*b)+(c*c*c)))) return 1;
       a++;
       if (a>MAX) { a=1; b++; }
       if (b>MAX) { b=1; c++; }
       if (c>MAX) { c=1;}
   }
   ```

   What may happen: Side-effect free infinite loops are removed entirely.


```{note}
I wasn't able to find a comprehensive list of what the C++ spec considers as undefined behaviour. The above examples were taken from [cppreference](https://en.cppreference.com/w/cpp/language/ub).
```

# Terminology

 * `{bm} processor/(preprocessor|translation unit)/i` - A tool that takes in a C++ source file and performs basic manipulation on it to produce what's called a translation unit.

   ```{note}
   See compilation section.
   ```

 * `{bm} compiler/(compiler|object file|object code)/i` - A tool that takes in a translation unit to produce an intermediary format called an object file.

   ```{note}
   See compilation section.
   ```

 * `{bm} linker/(linker|executable)/i` - A tool that takes multiple object files to produce an executable. Linkers are are also responsible for finding libraries used by the program and integrating them into the executable.

   ```{note}
   See compilation section.
   ```

 * `{bm} enumeration/(enumeration|enum)/i` - A user-defined type that can be set to one of a set of possibilities.

   ```c++
   enum class MyEnum {
      OptionA,
      OptionB,
      OptionC
   };
   
   MyEnum x {MyEnum::OptionC};
   ```

 * `{bm} class/(class|\bstruct)/i` - A user-defined type that pairs together data and the functions that operate on that data.

   ```c++
   class MyClass {
   public:
       MyClass(int x, long y) {
           this->x = x;
           this->y = y;
       }

       int add(int z) {
           this->x += z;
           return y + z;
       }
   private:
       int x;
       long y;
   }
   ```

 * `{bm} union` - A user-defined type where all members share the same memory location (different representations of the same data).

   ```c++
   union MyUnion {
       int x;
       long y;
   }
   ```

 * `{bm} plain-old-data class/(plain-old-data class|plain-old data class|plain old data class|plain-old-data structure|plain-old data structure|plain old data structure|plain-old-data struct|plain-old data struct|plain old data struct)/i` `{bm} /(POD)/` - A class that contains only data, not functions.

   ```c++
   struct Podo {
       int x;
       long y;
   }
   ```

 * `{bm} member/\b(member)/i` - Data or function belonging to a class.

 * `{bm} member function/(method|\bmember function)/i` - Function belonging to a class (class member that is a function).

   ```c++
   struct C {
       ...
       int add(int y) { return this->x + y; }
   };
   ```

 * `{bm} free function/(free function|non-member function)/i` - Function not belonging to a class.

   ```c++
   int negate(int x) { return -x; }
   ```

 * `{bm} field/(field|\bmember variable|\bmember field)/i` - Variable belonging to a class (class member that is a variable).

   ```c++
   struct C {
       int x;
   };
   ```

 * `{bm} class invariant` - When using some class, a class invariant is a feature of that class that is always true (never varies). For example, if a class is used to hold on to an IP and port combination, and it ensures that the port can never be 0, that's a class invariant.

 * `{bm} fundamental type/(fundamental type|built-in type)/i` - C++ type that's built into the compiler itself rather than being declared through code. Examples include `void`, `bool`, `int`, `char`, etc..

* `{bm} user-defined type/(user[\s\-]defined type)/i` - A type that's defined by a user, typically derived from existing types. Examples include enumerations, classes, unions, etc..

 * `{bm} object initialization` - The process by which a C++ program initializes an object (e.g. an `int`, array of `int`s, object of a class type, etc..).

 * `{bm} braced initialization/(brace initialization|braced initialization|uniform initialization)/i` - A form of object initialization where braces are used to set values (e.g. `int x {1}`, `MyStruct x{ 1, true }`, etc..). Braced initialization is often the least error-prone form of object initialization, where other forms may introduce ambiguity.

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

 * `{bm} equals initialization/(equals? initialization)/i` - A form of object initialization where the equals sign is used (e.g. `int x = 5`).

 * `{bm} braces-plus-equals initialization/(brace[sd]?[\-\s]plus[\-\s]equals? initialization)/i` - A form of object initialization where both the equals sign and braces are used for initialization (e.g. `MyStruct x = { 1, true }`). This is mostly equivalent to braced initialization.

   ```{note}
   See [here](https://stackoverflow.com/a/20733537). Even though there's an equal sign (=), there is no copy semantics / move semantics.
   ```

 * `{bm} constructor` - A function used for initializing an object.

    ```c++
    struct MyStruct : MyParent {
        ...
        MyStruct() {
            // do some setup here
        }
    };
    ```

 * `{bm} destructor` - A function used for cleanup when an object is destroyed.

    ```c++
    struct MyStruct : MyParent {
        ...
        ~MyStruct() {
            // do some cleanup here
        }
    };
    ```

    See also: virtual destructor.

 * `{bm} pointer` - A data type used to point to a different piece of memory (e.g. `int yPtr { &y }`).

 * `{bm} reference` - A data type used to point to a different piece of memory, but in a more sanitized / less confusing manner (e.g. `int &yRef { y };`).

 * `{bm} sizeof` - A unary operator that returns the size of a type or object (known at compile-time).

   ```c++
   int x {5};
   size_t x_size {sizeof x};
   ```

 * `{bm} address-of (&)/(address[\-\s]of)/i` - A unary operator used to obtain the memory address of an object (pointer) (e.g. `int *ptr {&x}`).

 * `{bm} dereference (*)/(dereference|dereferencing)/i` - A unary operator used to obtain the object at some memory address (e.g. `int x {*ptr}`).

 * `{bm} member-of-pointer (->)/(member[\-\s]of[\-\s]pointer)/i` - An operator that dereferences a pointer and access a member of the object pointed to (e.g. `ptr->x`).

 * `{bm} member-of-object (.)/(member[\-\s]of[\-\s]object)/i` - An operator that accesses a member of an object to (e.g. `obj.x`).

 * `{bm} pointer arithmetic` - Adding or subtracting integer types to a pointer will move that pointer by the number of bytes that makes up its underlying type (e.g. `uint32_t *ptrB = ptrA + 1` will set `ptrB` to 4 bytes ahead of ptrA).

 * `{bm} reseating/(reseat)/i` - The concept_NORM of a variable that points to something updating to point to something else. Pointers can be reseated, but references cannot.

   ```c++
   int x {5};
   int *p {&x};
   int y {7};
   p = &y; // reseat p
   ```

 * `{bm} member initializer list/(member initializer list|member initialization list|member initializer)/i` - A comma separated list of object initializations for the fields of a class appearing just before a constructor's body.

   ```c++
   struct MyStruct {
       int count;
       bool flag;
   
       MyStruct(): count{0}, flag{false} {
       }
   }
   ```

 * `{bm} default member initialization/(default member initializer|default member initialization)/i` - The object initialization of a field directly where that field is declared.

   ```c++
   struct MyClass {
       ...
       int my_var {5};
   };
   ```

 * `{bm} object/(object|instance)/i` - A region of memory that has a type and a value (e.g. class, an integer, a pointer to an integer, etc..).

 * `{bm} allocation/(allocation|allocate)/i` - The act of reserving memory for an object.

 * `{bm} deallocation/(deallocation|deallocate)/i` - The act of releasing the memory used by an object.

 * `{bm} storage duration` - The duration between an object's allocation and deallocation.

 * `{bm} lifetime` - The duration between when an object's constructor _completes_ (meaning the constructor finishes) and when its destructor is _invoked_ (meaning when the destructor starts).

 * `{bm} automatic object/(automatic object|automatic variable|automatic storage duration)/i` - An object that's declared within an enclosing code block. The storage duration of these objects start at the beginning of the block and finish at the end of the block.

   ```c++
   int my_func(int x) {
       int automatic_object {x + 5};
       return automatic_object;
   }
   ```

 * `{bm} static object/(static object|static variable|static storage duration)/i` - An object that's declared using `static` or `extern`. The storage duration of these objects start at the beginning of the program and finish at the end of the program.

 * `{bm} local static object/(local static object|local static variable|local static storage duration)/i` - A static object but declared at function scope. The storage duration of these objects start at the first invocation of the function and finish at the end of the program.

   ```c++
   int my_func() {
       static int local_static_object {0};
       local_static_object++;
       return local_static_object;
   }
   ```

 * `{bm} static member/(static field|static member)/i` - An object that's a member of a class but bound globally rather than on an instance of the class. A static field is essentially a static object that's accessible through the class itself (not an instance of the class). Similarly, a static method is essentially a global function that's accessed through the class (not an instance of the class).

   ```c++
   struct MyClass {
       ...
       static int my_var {5};
   };
   ```

 * `{bm} thread local object/(thread[\-\s]local object|thread[\-\s]local variable|thread[\-\s]local storage duration|thread storage duration)/i` - An object where each thread has access to its own copy. The storage duration of these objects start at the beginning of the thread and finish when the thread ends.

 * `{bm} dynamically allocated object/(dynamic object|dynamic array|dynamically allocated object|dynamically allocated array|dynamic storage duration)/i` - An object that's allocated and deallocated at the user's behest, meaning that it's storage duration is also controlled by the user.

   ```c++
   int * x { new x {5} };
   delete x;
   ```

 * `{bm} internal linkage` - A variable only visible to the translation unit it's in.

 * `{bm} external linkage` - A variable visible to the translation units that it's in as well as other translation units.

 * `{bm} scope resolution (::)/(scope resolution)/i` - A operator that's used to access static members (e.g. `MyStruct::static_func()`).

 * `{bm} extend/(extend|subclass)/i` - Another way of expressing class inheritance (e.g. B extends A is equivalent to saying B is a child of A).

 * `{bm} exception/(exception|try[\-\s]catch)/i` - An exception operation accepts an object and unwinds the call stack until reaching a special region specifically intended to stop the unwinding for objects of that type, called a try-catch block. Exceptions are a way for code to signal that something unexpected / exceptional happened.

 * `{bm} structured binding` - A language feature that allows for unpacking an object's members / array's elements into a set of variables (e.g. `auto [x, y] { two_elem_array }`).

 * `{bm} copy semantics` - The rules used for making copies of objects of some type. A copy, once made, should be equivalent to its source. A modification on the copy shouldn't modify the source as well.

 * `{bm} member-wise copy/(member[\-\s]wise copy)/i` - The default copy semantics for classes. Each individual field is copied.

 * `{bm} copy constructor` - A constructor with a single parameter that takes in a reference to an object of the same type (e.g. `T(const T &) { ... }`). A copy constructor is used to specify the copy semantics for that class.

 * `{bm} copy assignment` - An assignment operator overload that copies one object into another (e.g. `x = y`). Copy assignment requires that resources in the destination object be cleaned up prior to performing the copy.

 * `{bm} RAII/(RAII|CADRe)/` - Short for resource acquisition is initialization, the concept_NORM that the life cycle of some resource (e.g. open file, database object, etc..) is bound to an object's lifetime via it's constructor and destructor.

   Sometimes also referred to constructor acquires destructor releases (CADRe).

 * `{bm} moved-from object/(moved[\-\s]from object|moved[\-\s]from state)/i` - When an object is moved to another object, that object enters a special state where the only possible operation allowed on it is either destruction or re-assignment.

 * `{bm} move constructor` - A constructor with a single parameter that takes in an rvalue reference to an object of the same type (e.g. `T(T &&) { ... }`). A move constructor is used to specify the move semantics for that class.

 * `{bm} move assignment` - An assignment operator overload that moves one object into another (e.g. `x = y`).

 * `{bm} value categories/(value categories|value category|pr[\s\-]?value|l[\s\-]?value|x[\s\-]?value|r[\s\-]?value|gl[\s\-]?value)/i` - A classification hierarchy for C++ expressions. Any C++ expression falls into one of the following categories: lvalue, xvalue, or prvalue.

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

   ```c++
   struct MyParent {
       ...
       virtual int v2() {
           return this->x + this->y;
       }
   };
   ```

 * `{bm} pure virtual method/(pure[\-\s]virtual method|pure[\-\s]virtual function)/i` - A virtual method that requires an implementation (no implementation has been provided by the base class that declares it). For a class to be instantiable, it cannot have any pure virtual methods (similar to an abstract class in Java).

   ```c++
   struct MyParent {
       ...
       virtual int v2() = 0;
       ...
   };
   ```

 * `{bm} pure virtual class/(pure[\-\s]virtual class)/i` - A class that only contains pure virtual methods.

   ```c++
   struct MyParent {
       virtual int v1() = 0;
       virtual int v2() = 0;
       virtual ~MyParent() {};  // also okay to do   "virtual ~MyParent() = default"
   };
   ```

 * `{bm} virtual destructor` - A destructor that's a virtual method.

    ```c++
    struct MyStruct : MyParent {
        ...
        virtual ~MyStruct() {
            // do some cleanup here
        }
    };
    ```

 * `{bm} vtable` - A table of pointers to virtual functions, generated by the compiler. When a virtual function gets invoked (runtime) vtables are used to determining which method implementation to use.

 * `{bm} template` - A class or function where parts of the code are intended for substitution (by other code). At compile-time, a user supplies a set of substitutions for each usage of a template, customizing it for the specific use-case that user is dealing with.

   ```c++
   template <typename X, typename Y, typename Z>
   X add(Y y, Z z) {
       return y + z;
   }
   ```

 * `{bm} template parameter` - An identifier within the template. At compile time, any time a template is used its template parameters are substituted with code that the usage supplies.
 
   A template parameter may be used multiple times throughout the template. At compile-time, each usage is substituted with the same piece of code.

   ```c++
   // X, Y, Z, and N are template parameters
   template <typename X, typename Y, typename Z, int N>
   struct MyClass {
       X perform(Y &var1, Z &var2) {
           return (var1 + var2) * N;
       }
   };
   ```

 * `{bm} template instantiation` - The process of substituting the template parameters in a template with real code.

   ```c++
   MyClass<float, int, int, 2> obj {}; // X = float, Y = int, Z = int, N = 2
   float x { obj.perform(5, 3) };
   ```

 * `{bm} named conversion/(named conversion function|named conversion|const[_\s]cast|static[_\s]cast|reinterpret[_\s]cast|narrow[_\s]cast)/i` - A set of language features / functions used for converting types (casting): `const_cast`, `static_cast`, `reinterpret_cast`, and `narrow_cast`.

 * `{bm} concept/(concept)_TEMPLATE/i` - A compile-time check to ensure that the type substituted for a template parameter matches a set of requirements (e.g. the type support certain operators).

   ```c++
   // concept
   template <typename T1, typename T2, typename TR>
   concept MyConcept = std::is_default_constructible<T1>::value
           && std::is_default_constructible<T2>::value
           && requires(T1 a, T2 b) {
               { a + b } -> std::same_as<TR>;
               { a * b } -> std::same_as<TR>;
           };
   
   // usage of concept
   template <typename T1, typename T2>
       requires MyConcept<T1, T2, T1>
   T1 add_and_multiply(T1 &var1, T2 &var2) {
       return (var1 + var2) * var2;
   }
   ```

 * `{bm} compile-time` - Used in reference to something that happens during the compilation process.

 * `{bm} runtime` - Used in reference to something that happens when the compiled program is running.

 * `{bm} zero-arg/\b(zero-arg|no-arg)\b/i` - Short for zero argument. A function with zero parameters.

 * `{bm} parameter pack` - In the context of templates, a parameter pack is a single template parameter declaration that can take in zero or more substitutions (variadic).

   ```c++
   template <typename X, typename... R>
   X create(R... args) {
       return X {args...};
   }
   ```

 * `{bm} variadic/(variadic|vararg)/i` - A function that takes in a variable number of arguments, sometimes also called varargs.

   ```c++
   float avg(size_t n, ...) {
       va_list args;
       va_start(args, n);
       float sum {0};
       while (size_t i {0}; i < n; i++) {
           sum += va_args(args, float);
       }
       va_end(args);
       return sum /= n;
   }
   ```

 * `{bm} template specialization` - Given a specific substitutions set substitutions for the template parameters of a template, a template specialization is code that overrides the template generated code. Often times template specializations are introduced because they're more memory or computationally efficient than the standard template generated code.

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

 * `{bm} partial template specialization/(partial template specialization | template partial specialization)/i` - A template specialization where not all of the template parameters have been removed.

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

 * `{bm} partial template` - A template with some of its template parameters set (not all).

   ```c++
   // declare
   template <typename Y, typename Z>
   using MyClassPartialTemplate = MyClass<float, Y, Z, 42>;
   
   // use
   MyClass<float, int, int, 42> x{}; 
   MyClassPartialTemplate<int, int> y{};  // same type as previous line
   ```

 * `{bm} default template argument` - The default substitute in use for a template parameter.

   ```c++
   template <typename X, typename Y = long, typename Z = long>
   X perform(Y &var1, Z &var2) {
       return var1 + var2;
   }
   ```

 * `{bm} heap/(heap|free store)/i` - An implementation-specific block of memory used for dynamic objects. Also called the free store.

 * `{bm} implicit type conversion` - When an object of a certain type is converted automatically, without code explicitly changing the object to a different type (e.g. `long x {1}` implicitly converts the `int` literal in the initializer to the `long` type).

 * `{bm} explicit type conversion` - When an object of a certain type is explicitly converted to another type: casting and named conversions.

 * `{bm} promotion rule` - An implicit type conversion that may occur when an operator's operands are of differing integral and floating point types. For example, adding an integral type with a smaller integral type will cause the result to be of the same type as the larger type.

   ```c++
   int x {5};
   long y {5L};
   auto z {x + y};  // z will be long
   ```

 * `{bm} narrowing conversion` - When an object of a certain type is truncated to a lesser type (e.g. `int` to `short`). 

   Narrowing conversions may be implicit during object initialization. To erroneous cases of narrowing, use braced initialization to force the compiler to generate a warning.

 * `{bm} constant expression` - A function that gets evaluated at compile-time, such that at run-time any invocation of it simply returns the result computed at compile-time. Constant expressions are represented as functions prefixed with `constexpr`.

   ```c++
   constexpr int test(int n) {
       return n % 2;
   }
   ```

 * `{bm} immediate function` - A function that gets evaluated at compile-time and must produce a compile-time constant. Immediate functions expressions are represented as functions prefixed with `consteval`.

   ```c++
   consteval int test(const int n) {
       return n % 2;
   }
   ```

 * `{bm} literal type` - A type that's usable in a constant expression (for parameters and return), meaning that objects of this type can have a value that's knowable at compile-time (e.g. `nullptr`).

 * `{bm} volatile` - A volatile variable's usage in code is immune to compiler optimizations such as operation re-ordering and removal. Mutations and accesses, no matter how irrelevant they may seem, are kept in-place and in-order by the compiler.

   ```c++
   volatile int x {5};
   x = 5;
   x = 6;
   x = 7;
   ```

 * `{bm} type alias` - A synonym (different name) for an existing type.

   ```c++
   using BasicGraph = DirectedGraph::Graph<std::string, std::map<std::string, std::string>, std::string, std::map<std::string, std::string>>;
   
   BasicGraph removeLimbs(const BasicGraph &g);
   ```

 * `{bm} attribute` - A tag applied to code that provides information to the user / compiler about whatever it is that it's applied to. Similar to Java annotations.

   ```c++
   if (x == 0) [[likely]] {
       return x + y;
   } else {
       report_error();
   }
   ```

 * `{bm} iterator/(input iterator|output iterator|forward iterator|bi-?directional iterator|random access iterator|iterator)/i` - A type used to access elements within some sequence (e.g. array, class representing a list, class representing an infinite stream of `int`s, etc..). An iterator requires a specific set of operators to be implemented, where those operators function similar to accessing memory using pointer arithmetic / arrays.
 
   ```c++
   MyIterator it {collection.begin()};
   while (it != collection.end()) {
       MyObject value {*it};
       // do something with value here
       ++iterator;
   }
   ```

   Five types of iterators exist:

    * input iterator - An iterator that can only move forward in the sequence one element at a time and can only read elements of the sequence.
    * output iterator - An iterator that can only move forward in the sequence one element at a time and can only write elements of the sequence.
    * forward iterator - An iterator that combines the functionality of both input iterator and output iterator.
    * bidirectional iterator - An iterator that has the same functionality as forward iterator but also allows for moving backward in the sequence one element at a time, meaning it
    can move forward as well as backward.
    * random access iterator - An iterator that has the same functionality as bidirectional iterator but also allows randomly jumping to different elements within the sequence.
   
 * `{bm} modifier/(specifier|modifier)/i` - Optional marker that alters a function. With functions, a modifier may be required to go either before the return type (prefix modifier) or after the parameter list (suffix modifier).
 
    ```c++
    //                  modifier here
    //                    vvvvvvvv
    int add(int x, int y) noexcept {
        return x + y;
    }
    ```

   Modifiers are also sometimes referred to as specifiers.

 * `{bm} fold expression` - Exhaustively applies a binary operator to the contents of a parameter pack and return the final result.

    ```c++
    template<typename... R>
    T test(R... args) {
        R l_ass_res {... - args};  // ((((a-b)-c)-d)-...)
        R r_ass_res {args - ...};  // (...-(w-(x-(y-z))))
        return l_ass_res + r_ass_res;
    }
    ```

 * `{bm} associativity/(associativity|associative)/i` - In the context of binary operators, associativity refers to the order in which an expression with a chain of the same binary operator is evaluated. The term ...

   * left associative means that the chain is evaluated left-to-right (left-most first, right-most last).

     ```c++
     a ? b ? c ? d == (((a ? b) ? c) ? d)
     ```

   * right associative means that the chain is evaluated right-to-left (right-most first, left-most last).

     ```c++
     a ? b ? c ? d == (a ? (b ? (c ? d)))
     ```

 * `{bm} function pointer` - A pointer to a function.

   ```c++
   int add(int a, int b) {
       return a + b;
   }

   int (*p)(int, int) {add};
   p(1, 2);   // invoke
   ```

 * `{bm} functor/(functor|function object)/i` - A class that you can invoke as if it were a function because it has an operator overload for the function-call operator.

   ```c++
   struct MyFunctor {
       int operator()(int y) const { return -y + x; }
   private:
       int x {5};
   };
   ```

 * `{bm} function call operator/(function[\s\-]call operator)/i` - The operator used for making function calls (parenthesis), may be operator overloaded on classes to turn them into functors.

   ```c++
   int operator()(int y) const { return -y + x; }
   ```

 * `{bm} lambda` - Shorthand notation for an unnamed functor.

   ```c++
   auto f = [] (int z) -> int { return -z; };
   ```

 * `{bm} named capture` - Pulling in objects from the outer scope into a lambda by explicitly listing their names in the capture clause, adding `&` before each name if wanting to pull it in by reference rather than by copy.

   ```c++
   auto f = [&x, &y] (int z) -> int { return x + y + z; }; // x and y from outer scope
   ```

 * `{bm} default capture` - Pulling in objects from the outer scope into a lambda automatically (based on their usage) but putting either an `=` (for copying into lambda) or `&` (for referencing into lambda) in the capture clause.

   ```c++
   auto f = [=] (int z) -> int { return x + y + z; };
   ```

 * `{bm} init capture/(init capture|initializer capture)/i` - An initializer expression used as a lambda named capture.

   ```c++
   auto f = [new_x=x/2, &y] (int z) -> int { return new_x + y + z; };
   ```

 * `{bm} callable object` - An object that can be invoked: a function, functor, or lambda.

 * `{bm} function overload/(function overload|overloaded function|overload)/i` - A function that has the same name as another function within the same scope.

   ```c++
   bool test(int a) { return a != 0; }
   bool test(double a) { return a != 0.0; }
   ```

 * `{bm} forward declaration` - To use a function, class, variable, etc.. within some C++ code, only its declaration is needed, not its definition (implementation). The compiler wll ensure that the usage points to the implementation when the time comes.

   The compiler needs this to handle cyclical references. It can also significantly reduce build times.

   ```c++
   class MyClassA; // forward declaration of MyClassA
   class MyClassB; // forward declaration of MyClassB
   int myFunction(MyClassA &objA, MyClassB &objB); // forward declaration of a function


   // implement myFunction, using MyClassA and MyClassB before implementation is defined
   int myFunction(MyClassA &objA, MyClassB &objB) {
       ...
   }
   // implement MyClassA, using MyClassB before implementation is defined
   class MyClassA {
       ...
   private:
       MyClassB objB;
   }
   // implement MyClassB
   class MyClassA {
       ...
   private:
       MyClassA objA;
   }
   ```

 * `{bm} user-defined literal` - A literal suffix defined by a user, where when that suffix is applied to some literal, some computation is performed.

   ```c++
   Distance d {42.0_km};  // the suffix _km converts the literal 42.0 to an instance of the Distance type
   ```

 * `{bm} module unit` - A translation unit that contains a module declaration.

   ```c++
   export module MyModule;  // module declaration

   export int add(int a, int b) {
      return a + b;
   }
   ```

 * `{bm} three-way comparison operator/(three-way comparison operator|3-way comparison operator|spaceship operator)/i` - Given two objects `a` and `b`, the three-way comparison operator determines if `a < b`, `a == b`, or `a > b`.
 
   The symbol for the operator is an equal-sign sandwiched between angle brackets: `a <=> b`. This operator is sometimes called the spaceship operator because it's said that the symbol for the operator looks like a spaceship.

`{bm-ignore} (classification)/i`
`{bm-ignore} (structure)/i`
`{bm-error} Did you mean variadic?/(vardic)/i`
`{bm-error} Did you mean template parameter?/(type parameter)/i`

`{bm-error} Add the suffix _NORM or _TEMPLATE/(concept)/i`
`{bm-ignore} (concept)_NORM/i`