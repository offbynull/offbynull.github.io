`{title} C++`

```{toc}
```

# How to Read

This document is broken down into sections and sub-sections. To understand a specific section, you need to understand all of its parent sections as well as any prerequisites that it lists. For example, if section `Fruits/Apples/Granny Smith` has prerequisites `Vegetables/Peas` and `Fish` listed, you'll need to have read ...

* `Fruits` (just that section, not its sub-sections)
* `Fruits/Apples` (just that section, not its sub-sections)
* `Vegetables/Peas` (that section and including ALL of its sub-sections)
* `Fish` (that section including ALL of its sub-sections)

This is essentially a tree where each section is a node. To understand a node, you need to understand ...

1. its ancestor nodes __not including__ the children of those ancestors (these are the parent sections).
1. any nodes it links to __as well as__ their descendants (these are the sections listed as prerequisites).

# Essentials

`{bm} /(Essentials)_TOPIC/`

The following document is my attempt at charting out the various pieces of the modern C++ landscape, focusing on the 80% of features that get used most of the time rather than the 20% of highly esoteric / confusing features. It isn't comprehensive and some of the information may not be entirely correct / may be missing large portions.

The key points of similarity to remember:

1. Scope in C++ is similar to Java/C# (e.g. function scope, class scope, etc...). Variables, classes, etc.. come into and leave out of scopes in similar ways.
1. Compound statements in C++ are similar Java/C#. They create a scope, and things declared in that scope are gone once the scope is exited.
1. Control flow statements in C++ are similar to Java/C#. All the basics are there: for loops, for-each loops, while loops, if-else, switch, etc...
1. Data can exist on the heap or stack similar to Java/C#.

The key point of dissimilarity to remember:

1. **C++ does not come with a garbage collector**. You are responsible for releasing memory, although the C++ standard library has a lot of pieces to help with this.
1. C++ has a lot of legacy baggage and many edge cases. Compared to Java/C#, the language is powerful but also deeply convoluted with many foot-guns and esoteric syntax / semantics.
1. C++ has a lot of ambiguous behaviour. Compared to Java/C#, the language specifically carves out pieces of the spec and leaves it as platform-specific behaviour, undefined behaviour, etc.. so that compilers have more room to optimize code. 

```{seealso}
Core Language/Inconsistent Behaviour_TOPIC
```

## Language Basics

`{bm} /(Essentials\/Language Basics)_TOPIC/`

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

## Compilation Basics

`{bm} /(Essentials\/Compilation Basics)_TOPIC/`

```{prereq}
Essentials/Language Basics_TOPIC
```

Several C++ compilers exist, the most popular of which are the GNU C++ compiler and LLVM clang. C++ compilers generally follow the same set of steps to go from C++ code to an executable.

1. C++ source files get fed into a preprocessor to generate translation units. A translation unit is the C++ source file after going through modifications based on compiler specifics, platform specifics, libraries used, compile options / library options, etc..
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

`{bm} /(Essentials\/Header Files)_TOPIC/`

```{prereq}
Essentials/Language Basics_TOPIC
Essentials/Compilation Basics_TOPIC
```

For each source code file that gets compiled, the compiler needs to know that the entities (variables, functions, classes, etc..) accessed within that file actually exist. The scope at which the compiler keeps track of these entities is per source code file. For example, imagine a source code file that defines a function named `myFunction` (definition). There are 5 other source code files that call `myFunction` at some point. Each of those 5 other files is required to tell the compiler what `myFunction` is (declaration) before it can invoke it.

One way to handle this scenario is to put `myFunction`'s declaration in each source code file that calls it.

```c++
OtherClass myFunction(int a);
```

The problem with doing this is that ...

1. you're duplicating something 5 times, meaning you need to update 5 different places should anything change with the class.
2. you need a declaration for more than just `myFunction` (e.g. `myFunction` requires `OtherClass`, which may require even more entities). 
3. as a result of 1 and 2, source code file sizes explode and quickly become unmanageable.

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

## Development Environment

`{bm} /(Essentials\/Development Environment)_TOPIC/`

```{prereq}
Essentials/Compilation Basics_TOPIC
```

There are many different compilers, IDEs, build systems, and dependency managers for C++.

Common compilers:

 * GNU C++ compiler
 * LLVM Clang
 * Microsoft Visual C++ compiler

Common IDEs:

 * Visual Studio Code (open-source, multi-platform), commonly referred to as vscode
 * Visual Studio C++ (proprietary, Windows only)
 * CLion (proprietary, multi-platform)
 * KDevelop  (open-source, multi-platform)

Common build systems:

 * Make
 * Automake / Autoconf / Autotools
 * CMake

```{note}
CMake isn't a build system itself, but a tool that generates the configuration needed for build systems. The idea is that, since C++ code can be compiled on many different platforms and build systems, this high-level tool can be used to generate the configuration for those build systems. For example, building on Linux is commonly done using Make while on Windows it's commonly done through Microsoft Visual Studio IDE project files. CMake can configure both using the same CMake script.
```

Common dependency managers:

 * Conan
 * Vcpkg
 * Spack

Of the tools above, the best mixture I've found so far is to use ...

 1. LLVM Clang as the compiler (installable via apt -- `apt install clang-12`)
 2. Visual Studio Code as the editor (installable via snap -- `snap install --classic code`)
 3. CMake as the build system  (installable via apt -- `apt install cmake`)
 4. Conan as the dependency manager (install deb file from website)
 5. C++ extension pack for vscode (install via extension section of vscode)
 6. LLVM clangd extension for vscode (install via extension section of vscode)
 7. C-Mantic extension for vscode (install via extension section of vscode)

There are basic guides / tutorials for each of these tools available online. With the C++ extensions (5, 6, and 7), vscode (3) works similar to a professional IDE. It will parse a CMake configuration (3) to figure out how the code should be built as well as to provide C++ intellisense / auto-complete / formatting / debugging / etc.. support. Conan (4) integrates with CMake, so intellisense and builds through vscode automatically include the libraries.

````{note}
Make sure to turn off the C++ extension's intellisense support or else it'll interfere with clangd's superior intellisense support. You can do this by adding the following to your `.vscode/settings.json file`...

```json
{
    "C_Cpp.intelliSenseEngine": "Disabled",
    "C_Cpp.autocomplete": "Disabled",  // So you don't get autocomplete from both extensions.
    "C_Cpp.errorSquiggles": "Disabled", // So you don't get error squiggles from both extensions (clangd's seem to be more reliable anyway).
}
```
````

```{note}
Make sure that you don't have other C++ extensions installed. I'd initially installed a Makefile plugin into vscode that was tripping up the CMake plugin and breaking my intellisense.
```

Assuming you have all the software above installed, [`{bm-skip} this cookie cutter template`](my_cpp_template.tar.xz) can be used to set up a simple project structure that you can open directly in vscode. The template primes the project by ...

 1. creating a main source folder (`src/main`).
 1. creating a test source folder (`src/test`).
 1. setting Conan to download POCO C++ Libraries and Google Test.
 1. setting CMake and Conan to use LLVM Clang 12.
 1. setting CMake to build using C++20.
 1. setting CMake to integrate with Conan.
 1. setting CMake to recursive glob compile.

```{note}
I keep reading that globs aren't recommended in CMake. If you don't use globs, you'll have to go in and manually add in each source file into the CMake configuration.
```

```{note}
Recall that ...

* vscode will automatically reconfigure CMake on any change to the configuration file.
* vscode will build your code when you hit F7.

Conan changes ARE NOT automatically picked up. You need to re-run conan (from `./build` -- see the cookie cutter template post hook) to pick up any library changes.
```

# Core Language

`{bm} /(Core Language)_TOPIC/`

```{prereq}
Essentials_TOPIC
```

The following subsection loosely details core C++ language features. It isn't comprehensive and some of the information may not be entirely correct / may be missing large portions.

## Operators

`{bm} /(Core Language\/Operators)_TOPIC/`

The following is a list of operators available in C++. Some operators are obvious, while others are explained in other sections.

__Bitwise Logical Operators__

| name                       | example            | note                                              |
|----------------------------|--------------------|---------------------------------------------------|
| Bitwise AND         (`&`)  | `0b1011 & 0b0110`  |                                                   |
| Bitwise OR          (`\|`) | `0b1011 \| 0b0110` |                                                   |
| Bitwise XOR         (`^`)  | `0b1011 ^ 0b0110`  |                                                   |
| Bitwise NOT         (`~`)  | `~0b1011`          |                                                   |
| Bitwise left-shift  (`<<`) | `0b1011 << 2`      |                                                   |
| Bitwise right-shift (`>>`) | `0b1011 >> 2`      | Results on signed may be different than unsigned. |

__Boolean Logical Operators__

| name                 | example           | note |
|----------------------|-------------------|------|
| Logical AND (`&&`)   | `true && true`    |      |
| Logical OR  (`\|\|`) | `true \|\| false` |      |
| Logical NOT (`!`)    | `!true`           |      |

__Arithmetic Operators__

| name                   | example | note |
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

__Assignment Operators__

| name                                   | example        | note                                                                                                                             |
|----------------------------------------|----------------|----------------------------------------------------------------------------------------------------------------------------------|
| Assignment                     (`=`)   | `x = 5`        |                                                                                                                                  |
| Assignment Bitwise AND         (`&=`)  | `x &= 0b0110`  |                                                                                                                                  |
| Assignment Bitwise OR          (`\|=`) | `x \|= 0b0110` |                                                                                                                                  |
| Assignment Bitwise XOR         (`^=`)  | `x ^= 0b0110`  |                                                                                                                                  |
| Assignment Bitwise left-shift  (`<<=`) | `x <<= 2`      |                                                                                                                                  |
| Assignment Bitwise right-shift (`>>=`) | `x >>= 2`      | Result  on signed may be different than unsigned.                                                                                |
| Assignment Addition            (`+=`)  | `x += 2`       |                                                                                                                                  |
| Assignment Subtraction         (`-=`)  | `x -= 1`       |                                                                                                                                  |
| Assignment Multiplication      (`*=`)  | `x *= 3`       |                                                                                                                                  |
| Assignment Division            (`/=`)  | `x /= 2`       |                                                                                                                                  |
| Assignment Modulo              (`%=`)  | `x %= 4`       |                                                                                                                                  |
| Increment                      (`++`)  | `x++`          | Applicable BEFORE or AFTER the operand: `++x` returns the value AFTER modification, `x++` returns the value BEFORE modification. |
| Decrement                      (`--`)  | `x--`          | Applicable BEFORE or AFTER the operand: `--x` returns the value AFTER modification, `x--` returns the value BEFORE modification. |

All assignment operators work similar to those in Java except for the increment and decrement operators. Due to the confusion it causes, Java disallows the increment / decrement from returning a value, meaning that it can't be used in an expression. Not so in C++. In addition to modifying the variable passed as the operand, in C++ these operators also return a result, meaning that it's okay to increment / decrement operator within some larger expression. 

```c++
int x {3};
int y {(x++) + 2};
// at this point, x is 4, y is 5
int a {3};
int b {(++a) + 2};
// at this point, a is 4, b is 6
```

```{note}
You probably shouldn't do this because it gets confusing. Also, incrementing/decrementing the same variable more than once in the same expression isn't defined behaviour: The order of  incrementing/decrementing can change based on whatever the compiler thinks is best, meaning that the results won't be consistent across different platforms / compilers / compiler options / etc...
```

__Comparison Operator__

| name                             | example   | note                                                                                    |
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

__Member Access Operators__

| name                     | example     | note                                                                                       |
|--------------------------|-------------|--------------------------------------------------------------------------------------------|
| Subscript         (`[]`) | `x[0]`      |                                                                                            |
| Indirection       (`*`)  | `*x`        | Doesn't conflict with arithmetic multiplication operator because this is a unary operator. |
| Address Of        (`&`)  | `&x`        |                                                                                            |
| Member Of Object  (`.`)  | `x.member`  |                                                                                            |
| Member Of Pointer (`->`) | `x->member` |                                                                                            |

These operators are used in scenarios that deal with accessing the members of an object (e.g. element in an array, field of a class) or dealing with memory addresses / pointers. The subscript and and member of object operators are similar to their counterparts in other high-level languages (e.g. Java, Python, C#, etc..). The others are unique to languages with support for lower-level programming like C++. Their usage is detailed in other sections.

__Dynamic Object Operators__

| name                                | example       | note |
|-------------------------------------|---------------|------|
| Create Dynamic Object       (`new`) | `new int`     |      |
| Create Dynamic Array      (`new[]`) | `new int[50]` |      |
| Destroy Dynamic Object   (`delete`) | `delete x`    |      |
| Destroy Dynamic Array  (`delete[]`) | `delete[] x`  |      |

```{note}
If you already know about dynamic objects and arrays and constructors/destructors, make sure you delete an array using `delete[]`. It makes sure to call the destructor for each element of the array.
```

__Size Operator__

| name            | example     | note |
|-----------------|-------------|------|
| Size (`sizeof`) | `sizeof x]` |      |

This operator gets the size of an object in bytes. Note that an object's byte size may not be indicative of the da may include padding required by the platform (e.g. an object requiring 5 bytes may get expanded to 8 bytes because the platform requires 8 byte boundary alignments).

__Other Operators__

C++ provides a set of other operators such as the ...

 * comma operator (`,`).
 * function call operator (`()`).
 * conversion operator (e.g. casting).
 * user-defined literal operator (e.g. `_`)

While it isn't worth going into them in detail here, the reason the language explicitly lists them as operators is because they're overload-able (e.g. operator overloading). Overloading these operators is heavily discouraged since doing so causes confusion.

````{note}
The book mentions the comma operator specifically. It doesn't look like this is used for much and the book recommends against using it for anything (e.g. operator overloading) due to the confusion it causes. This gives off similar vibes to Python's tuple syntax, where you can pass an unenclosed tuple as a subscript to something. When I was learning Python, that also came off as very confusing.

```python
x = obj['column name', 100]
```
````

## Variables

`{bm} /(Core Language\/Variables)_TOPIC/`

```{prereq}
Core Language/Operators_TOPIC: Just basic ones like comparison and arithmetic.
```

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
   
   It seems like the safest bet is to always use brace initialization where possible. Just use the braces as if they were parentheses or braces in Java (specific to the context). The others have surprising behaviour (e.g. they won't warn about narrowing conversions).
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

### Core Types

`{bm} /(Core Language\/Variables\/Core Types)_TOPIC/`

```{prereq}
Core Language/Operators_TOPIC (just the basics like comparison and arithmetic)
```

The following sections list out core C++ types and their analogs. These include numeric types, character types, and string types.

#### Integral

`{bm} /(Core Language\/Variables\/Core Types\/Integral)_TOPIC/`

C++'s core integer types are as follows...

1. `short int`
1. `int`
1. `long int`
1. `long long int`

The above integer types come in two forms: signed and unsigned. The range of ...

* unsigned integers start at 0 and end at a positive integer.
* signed integers start at a negative integer and positive integer.

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
Not all types guaranteed to be present (e.g. 64-bit types may be missing if the platform can't support it). Unsigned types don't have a minimum extent defined because a minimum of any unsigned integer type is always 0 (e.g. uint64_t can't go any lower than 0).
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

#### Floating Point

`{bm} /(Core Language\/Variables\/Core Types\/Floating Point)_TOPIC/`

C++'s core floating point types are as follows...

| type          | description        | literal suffix | example  |
|---------------|--------------------|----------------|----------|
| `float`       | single precision   | `f`            | `123.0f` |
| `double`      | double precision   |                | `123.0`  |
| `long double` | extended precision | `L`            | `123.0L` |

The specifics of each type are platform-dependent. The only guarantee is that each type has to hold at least the same range as the type before it (e.g. `double`'s range should cover `float`'s range). Other than that, ...

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
 * 1 means toward whichever is nearest.
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

#### Character String

`{bm} /(Core Language\/Variables\/Core Types\/Character String)_TOPIC/`

```{prereq}
Core Language/Variables/Core Types/Integral_TOPIC
```

Core C++ strings are represented as an array of characters, where that array ends with a null character to signify its end. This is in contrast to other major platforms that typically structure strings a size integer along with the array (no null terminator).

Individual characters all map to integer types, where literals are defined by wrapping the character in single quotes. Even though they're integers, the signed-ness of each of the types below isn't guaranteed.

| type       | bits | literal prefix | example | description                                                 |
|------------|------|----------------|---------|-------------------------------------------------------------|
| `char`     | >= 8 |                | `'T'`   | >= 8-bit wide character (smallest unit of memory -- 1 byte) |
| `char8_t`  | 8    | `u8`           | `u8'T'` | 16-bit wide character (e.g. UTF-8)                          |
| `char16_t` | 16   | `u`            | `u'T'`  | 16-bit wide character (e.g. UTF-16)                         |
| `char32_t` | 32   | `U`            | `U'T'`  | 32-bit wide character (e.g. UTF-32)                         |
| `wchar_t`  |      | `L`            | `L'T'`  | at least as wide as `char`                                  |

Note that `char` and `wchar_t` don't have predefined bit lengths. They are platform-dependent. The bit length for...

* `char` is defined in `CHAR_BIT` of climits and must be at least 8 bits.
* `wchar_t` must be equal to or greater than that of `char`.

```{note}
`char` literals can also be integers, but the signed-ness of the `char` type isn't defined by default (speculation). It can specifically be made to be signed / unsigned by prefixing it as such: `signed char` / `unsigned char`.
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

#### Void

`{bm} /(Core Language\/Variables\/Core Types\/Void)_TOPIC/`

`void` is a type that represents an empty set of values. Since it can't hold a value, C++ won't allow you to declare an object of type void. However, you can use it to declare that a function ...

* returns no value (`void` return).
* accepts no arguments (`void` parameter list).

### Arrays

`{bm} /(Core Language\/Variables\/Arrays)_TOPIC/`

```{prereq}
Core Language/Variables/Core Types_TOPIC
Core Language/Variables/Pointers_TOPIC: Just the main section, not any of the subsections.
```

C++ allows for the creation of arrays of constant length (size of the array must be known at compile-time). Elements of an array are guaranteed to be contiguous in memory (speculation).

* `int x[100]` - Creates an array of 100 ints where those 100 ints are junk values (data previously at that memory location is not zeroed out).
* `int x[] { 5, 5, 5 }` - Creates an array of 3 ints where each of those ints have been initialized to 5 (braced initialization).
* `int x[] = { 5, 5, 5 }` - Equivalent to above (assignment does not do any extra work).
* `int x[3] {}` - Creates an array of 3 ints where each of those ints are 0 (memory zeroed out -- braced initialization).
* `int x[3] = {}` - Equivalent to above (assignment does not do any extra work).
* `int x[n]` - Disallowed by C++ if n isn't a constant. These types of arrays are allowed in C (called variable length arrays / VLA), but not in C++ because C++ has collection classes that allow for sizes not known at compile-time.

Accessing arrays is done similarly to how it is in most other languages, by subscripting (e.g. `x[0] = 5`). The only difference is that array access isn't bounds-checked and array length information isn't automatically maintained at run-time. For example, if an array has 100 elements, C++ won't stop you from trying to access element 250 -- out-of-bounds array access is undefined behaviour.

One way to think of an array is as a pointer to a contiguous block of elements of the array type. In fact, if an array type gets used where it isn't expected, that array type automatically decays to a pointer type.

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
My understanding is that arrays are typically passed to functions as pointers + array length. This is because the array length information is only available at compile-time, meaning that if you have a function that takes in an array, how would it know the size of the array it's working with when it runs (it isn't the one who declared it). It looks like a function parameter can be an array type of fixed size, but apparently that doesn't mean anything? The compiler doesn't enforce that a caller use an array of that fixed size, and using sizeof on the array will produce a warning saying that it's decaying into a pointer.

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
std::cout << sizeof x;  // should be the size of 3 ints
std::cout << sizeof y;  // should be the size of a pointer
```

Similarly, range-based for loops won't work if the type has decayed to a pointer type because the array size of that pointer isn't known at compile-time.

```c++
int x[3] = {1,2,3};
int *y {x};
for (int i {0}; i < 3; i++) { // OK
   std::cout << y[i] << std::endl;
}
for (int v : x) { // OK
   std::cout << v << std::endl;
}
for (int v : y) { // ERROR
   std::cout << v << std::endl;
}
```

You may be tempted to use `sizeof(array) / sizeof(type)` to determine the number of elements within an array. It's a better idea to use `std::size(array)` instead (found in the iterator header) because it should have logic to workaround and platform-specific behaviours that might cause inconsistent results / unexpected behaviour (speculation).

### Pointers

`{bm} /(Core Language\/Variables\/Pointers)_TOPIC/`

```{prereq}
Core Language/Variables/Core Types_TOPIC
```

C++ provides types that reference a memory address, called pointers. Variables of these types can point to different memory addresses / objects.

Adding an asterisk (\*) to the end of any type makes it a pointer type (e.g. `int *` is a type that can contain a pointer to an `int`). A pointer to any object can be retrieved using the address-of unary operator (&). Similarly, the value in any pointer can be retrieved using the dereference unary operator (\*).

```c++
int w {5};
int *x { &w }; // x points to w
int *y { &w }; // y points to w
int z { *x };   // z is a copy of whatever x points to, which is w, which means it gets set to 5
*x = 7;        // w is set to 5 through x

int **a { &x }; // a points to x, which points to w (a pointer to a pointer to an int)
```

As shown in the example above, it's perfectly valid to use the dereference operator on the left-side of the equals. It defines where the result of the right side should go.

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
It seems like there's some implicit conversions to boolean that are possible with pointers. If whatever the pointer is going to expect a boolean, it's implicitly converted to `ptr != nullptr`? So in if / while/ for conditions, you can just use the pointer as is without explicitly writing out a condition?
```

```{note}
How is this different than the NULL macro? I guess because it's a distance type, you can have a function overload that takes in param of type `std::nullptr_t`? But why would you ever want to do that?
```

#### Pointer Arithmetic

`{bm} /(Core Language\/Variables\/Pointers\/Pointer Arithmetic)_TOPIC/`

```{prereq}
Core Language/Variables/Arrays_TOPIC
```

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
An array guarantees that its elements appear contiguously and in order within memory (I think?), so if the pointer is from a decayed array, using pointer arithmetic to access its elements is perfectly fine.
```

#### Void Pointer

`{bm} /(Core Language\/Variables\/Pointers\/Void Pointer)_TOPIC/`

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

#### Function Pointer

`{bm} /(Core Language\/Variables\/Pointers\/Function Pointer)_TOPIC/`

```{prereq}
Core Language/Functions_TOPIC: Just enough to know what a function is / how to define one.
```

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

### References

`{bm} /(Core Language\/Variables\/References)_TOPIC/`

```{prereq}
Core Language/Variables/Core Types_TOPIC
Core Language/Variables/Pointers_TOPIC
```

C++ provides a more sanitized version of pointers called references. A reference type is declared by adding an ampersand (&) after the type rather than an asterisk (*), and it implicitly takes the address of whatever is passed into it when it's created.

```c++
int w {5};

int *x { &w }; // x points to w
int &y { w };  // y references to w (note address-of operator not used here)
```

The main difference between pointer types and reference types is that a reference type doesn't need to explicitly dereference to access the object pointed to. The object pointed to by the reference type is accessed as if it were the object itself.

```c++
*x = 10;       // x explicitly dereferenced to w and set to 10
y = 15;        // y implicitly dereferenced to w and set to 15
```

As shown in the example above, assignment to a reference type is assignment on the underlying object being referenced. As such, having the reference type point to a different object isn't possible (referred to as reseating).

Similarly, it's not possible to have a reference to a reference.

```c++
int &&z { y }; // this isn't a thing -- fail
```

```{note}
The way to think of references is documented [here](https://stackoverflow.com/a/1164267). Don't consider a reference as an object the same way a pointer is an object. In the compiler's eyes, a reference doesn't store anything like a pointer does (stores a memory address). It's just a "reference" to an object -- the object itself has storage, but the reference to that object doesn't.

In that sense, it's impossible to have ...

* a `const` reference like you have a `const` pointer or an array of references.
* an array of references
* etc...

... the same way that you can have with a pointer.
```

### Rvalue References

`{bm} /(Core Language\/Variables\/Rvalue References)_TOPIC/`

```{prereq}
Core Language/Variables/References_TOPIC
Core Language/Expression Categories_TOPIC
Core Language/Templates_TOPIC
```

An rvalue reference is similar to a reference except that it tells the compiler that it's working with an rvalue. Rvalue references are declared by adding two ampersands (&&) after the type rather than just one.

```c++
// Function return type is an rvalue reference
MyObject && gimmie_an_rvalueref(int x) {
    ...
}
```

A variable of type rvalue reference is actually an lvalue to an rvalue reference. As such, passing a variable of type revalue reference as a function argument will treat it as if it were an lvalue.

```{note}
Confused? Recall from the expression categories section that, if it has a name (named variable or function), it's probably an lvalue.
```

```c++
void my_func(MyObject & x) {
    std::cout << "NO RREF";
}
void my_func(MyObject && xRref) {
    std::cout << "YES RREF";
}
MyObject &&a { gimmie_an_rvalueref(42) }; // a has a name, meaning its an lvalue to an rvalue reference
my_func(a);  // calls "NO RREF" version
```

If you need to pass a variable of type rvalue reference as a function argument, the typical approach is to either never store it as a variable or to use `std::forward` to ensure the object remains an rvalue reference.

```c++
my_func(gimmie_an_rvalueref(42));      // calls "YES RREF" version
my_func(std::forward<MyObject &&>(b)); // calls "YES RREF" version
// NOTE: you MUST specify the full type in std::forward's template parameter -- automatic type inference not supported
```

```{note}
See [here](https://github.com/AnthonyCalandra/modern-cpp-features#forwarding-references).
```

Rvalue references are typically used for moving objects (not copying, but actually moving the guts of one object into another). This is done through something called a move constructor, which is explained in another section.

```{seealso}
Core Language/Classes/Moving_TOPIC
```

### Size

`{bm} /(Core Language\/Variables\/Size)_TOPIC/`

```{prereq}
Core Language/Variables/Core Types_TOPIC
Core Language/Variables/Arrays_TOPIC
Core Language/Variables/Pointers_TOPIC
```

`sizeof` is a unary operator that returns the size of its operand in bytes as a `size_t` type. If the operand is a ...

* data type or a variable, it'll return the number of bytes needed to hold that type. For example, ...

  * `sizeof char` is guaranteed to be 1.
  * `sizeof (char &)` is guaranteed to be 1.
  * `sizeof (char *)` is platform dependent, typically either 4 or 8.
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

### Aliasing

`{bm} /(Core Language\/Variables\/Aliasing)_TOPIC/`

```{prereq}
Core Language/Variables/Core Types_TOPIC
Core Language/Variables/Arrays_TOPIC
Core Language/Variables/Pointers_TOPIC
```

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

```{seealso}
Core Language/Templates/Type Aliasing_TOPIC
```

### Constant

`{bm} /(Core Language\/Variables\/Constant)_TOPIC/`

```{prereq}
Core Language/Variables/Core Types_TOPIC
Core Language/Variables/Arrays_TOPIC
Core Language/Variables/Pointers_TOPIC
```

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

### Volatile

`{bm} /(Core Language\/Variables\/Volatile)_TOPIC/`

```{prereq}
Core Language/Variables/Core Types_TOPIC
Core Language/Variables/Arrays_TOPIC
Core Language/Variables/Pointers_TOPIC
```

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

### Common Attributes

`{bm} /(Core Language\/Variables\/Common Attributes)_TOPIC/`

If a variable has been deprecated, adding a `[[deprecated]]` attribute will allow the compiler to generate a warning if it sees it being used.

```c++
[[deprecated("Warning -- this is going away in the next release")]]
int my_variable;
```

### Implicit Conversion

`{bm} /(Core Language\/Variables\/Implicit Conversion)_TOPIC/`

```{prereq}
Core Language/Variables/Core Types_TOPIC
Core Language/Variables/Arrays_TOPIC
Core Language/Variables/Pointers_TOPIC
Core Language/Variables/References_TOPIC
```

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

| source type    | destination type | behaviour                                                                                                                                         |
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

### Explicit Conversion

`{bm} /(Core Language\/Variables\/Explicit Conversion)_TOPIC/`

```{prereq}
Core Language/Variables/Core Types_TOPIC
Core Language/Variables/Arrays_TOPIC
Core Language/Variables/Pointers_TOPIC
Core Language/Variables/References_TOPIC
```

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

`{bm} /(Core Language\/Variables\/Explicit Conversion\/Named Conversions)_TOPIC/`

Named conversion functions are a set of (seemingly templated) functions to convert an object's types. These functions provide safety mechanisms that aren't available in other older ways of casting.

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

```{seealso}
Library Functions/Utility Wrappers/Any_TOPIC (`any_cast` for an "any" container)
Library Functions/Time/Timestamps/Clocks_TOPIC (`clock_cast` for converting times between different types of clocks)
Library Functions/Time/Durations_TOPIC (`duration_cast` for converting between different types of durations)
```

#### C-style Casts

`{bm} /(Core Language\/Variables\/Explicit Conversion\/C-style Casts)_TOPIC/`

C-style casts are similar to casts seen in Java. The type is bracketed before whatever is being evaluated.

```c++
int x { (int) 9999999999L };
```

The problem with C-style casting is that it doesn't provide the same safety mechanisms as named conversions do (e.g. inadvertently strip the `const`-ness). Named conversions provide these safety mechanisms and as such should be preferred over C-style casts. Any C-style cast can be performed using a named conversion.

## Object Lifecycle

`{bm} /(Core Language\/Object Lifecycle)_TOPIC/`

```{prereq}
Core Language/Variables_TOPIC: Just enough to know how to define and use one.
Core Language/Functions_TOPIC: Just enough to know how to define and use one.
Core Language/Classes_TOPIC: Just enough to know how to define and use one.
```

In C++, an object is a region of memory that has a type and a value (e.g. a class instance, an integer, a pointer to an integer, etc..). Contrary to other more high-level languages (e.g. Java), C++ objects aren't exclusive to classes (e.g. a boolean is an object).

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

Since C++ doesn't have a garbage collector performing cleanup like other high-level languages, it's the user's responsibility to ensure object lifetimes. The user is responsible for knowing when objects should be destroyed and ensuring that objects are only accessed within their lifetime.

The typical storage durations supported by C++ are...

 * automatic storage duration - scoped to duration of some function within the program.
 * static storage duration - scoped to the entire duration of the program.
 * thread storage duration - scoped to the entire duration of a thread in the program.
 * dynamic storage duration - allocated and deallocated on request of the user.

### Static Objects

`{bm} /(Core Language\/Object Lifecycle\/Static Objects)_TOPIC/`

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

`{bm} /(Core Language\/Object Lifecycle\/Dynamic Objects)_TOPIC/`

An object can be created in an ad-hoc manner, such that its storage duration is entirely controlled by the user. The operator ...

 * `new` allocates a new object and calls its constructor.
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

The same process can be used to create an array of objects. Unlike automatic object arrays, dynamic arrays don't have a constant size array length restriction. However, the return value of `new` will decay from an array type to a pointer type.

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

## Functions

`{bm} /(Core Language\/Functions)_TOPIC/`

```{prereq}
Core Language/Variables_TOPIC: Just enough to know how to define and use one.
```

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

### Overloading

`{bm} /(Core Language\/Functions\/Overloading)_TOPIC/`

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

### Argument Matching

`{bm} /(Core Language\/Functions\/Argument Matching)_TOPIC/`

When a function is called but the arguments types don't match the parameter list types, the compiler attempts to obtain a correct set of types through a set of conversions on the arguments. For example, if a parameter expects a reference to a constant object but what gets passed into the argument is an object, the argument is automatically converted to a constant object and its reference is used.

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

### Main Function

`{bm} /(Core Language\/Functions\/Main Function)_TOPIC/`

```{prereq}
Core Language/Variables/Core Types_TOPIC
Core Language/Variables/Pointers_TOPIC
Core Language/Variables/Arrays_TOPIC
```

The entry-point to any C++ program is the `main` function, which can take one of three possible forms:

 1. `int main()`

    No arguments.

 1. `int main(int argc, char* argv[])`

    Command-line arguments, where `argv` is an array of size `argc` containing the null-terminated command-line arguments. On most modern platforms, the first argument is the path of the executable.

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

### Variadic

`{bm} /(Core Language\/Functions\/Variadic)_TOPIC/`

```{prereq}
Core Language/Variables/Core Types_TOPIC
Core Language/Variables/Pointers_TOPIC
Core Language/Variables/Arrays_TOPIC
```

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
The book recommends against using variadic functions due to confusing usage and having to explicitly know the count and types of the variadic arguments before hand (can become security problem if screwed up). Instead it recommends using variadic templates for functions instead.
```

### No Exception

`{bm} /(Core Language\/Functions\/No Exception)_TOPIC/`

In certain cases, it'll be impossible for a function to throw an exception. Either the function (and the functions it calls into) never throws an exception or the conditions imposed by the function make it impossible for any exception to be thrown. In such cases, a function may be marked with the `noexcept` keyword. This keyword allows the compiler to perform certain optimizations that it otherwise wouldn't have been able to, but it doesn't necessarily mean that the compiler will check to ensure an exception can't be thrown.

```c++
int add(int a, int b) noexcept {
    return a + b;
}
```

```{note}
The book mentions this is documented in "Item 16 of Effective Modern C++ by Scott Meyers". It goes on to say that, unless specified otherwise, the compiler assumes move constructors / move-assignment operators can throw an exception if they try to allocate memory but the system doesn't have any. This prevents it from making certain optimizations.
```

### Common Attributes

`{bm} /(Core Language\/Functions\/Common Attributes)_TOPIC/`

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

If a function has been deprecated, adding a `[[deprecated]]` attribute will allow the compiler to generate a warning if it's being used.

```c++
[[deprecated("Warning -- this is going away in the next release")]]
int add(int a, int b) {
    return a + b;
}
```

## Enumerations

`{bm} /(Core Language\/Enumerations)_TOPIC/`

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

An enumeration may be brought into scope via `using` to remove the need to prefix with the enumeration's name.

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
enum MyEnum { // no class keyword
   OptionA,
   OptionB,
   OptionC
};

MyEnum x {OptionC}; // this is okay -- don't have to use MyEnum::OptionC
int y {OptionC};    // this is okay -- options are integers
```

You should prefer `enum class`.
````

## Classes

`{bm} /(Core Language\/Classes)_TOPIC/`

```{prereq}
Core Language/Variables_TOPIC: Just enough to know how to define and use one.
Core Language/Functions_TOPIC: Just enough to know how to define and use one.
```

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

### This Pointer

`{bm} /(Core Language\/Classes\/This Pointer)_TOPIC/`

```{prereq}
Core Language/Variables/Pointers_TOPIC
```

Non-static methods of a class have access to an implicit pointer called `this`, which allows for accessing that instance's members. As long as the class member doesn't conflict with any parameter name of the method invoked, the usage of that name will implicitly reference the `this` pointer.

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

### Constant

`{bm} /(Core Language\/Classes\/Constant)_TOPIC/`

```{prereq}
Core Language/Classes/This Pointer_TOPIC
Core Language/Variables/Constant_TOPIC
```

For fields of a class, a `const` before the type has the same meaning as a `const` variable at global scope: It's unmodifiable.

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

### Volatile

`{bm} /(Core Language\/Classes\/Volatile)_TOPIC/`

```{prereq}
Core Language/Classes/This Pointer_TOPIC
Core Language/Variables/Volatile_TOPIC
```

For fields of a class, a `volatile` before the type has the same meaning as a `volatile` variable at global scope: The compiler won't optimize its access.

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

### Common Attributes

`{bm} /(Core Language\/Classes\/Common Attributes)_TOPIC/`

If a class has been deprecated, adding a `[[deprecated]]` attribute will allow the compiler to generate a warning if it sees it being used.

```c++
[[deprecated("Warning -- this is going away in the next release")]]
int add(int a, int b) {
    return a + b;
}
```

### Static

`{bm} /(Core Language\/Classes\/Static)_TOPIC/`

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

```{seealso}
Core Language/Object Lifecycle/Static Objects_TOPIC
Core Language/Linker Behaviour/Static Linkage_TOPIC
```

### Construction

`{bm} /(Core Language\/Classes\/Construction)_TOPIC/`

```{prereq}
Core Language/Classes/This Pointer_TOPIC
```

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

MyStruct a;                    // initialized to zeroed out memory (via implicit constructor)
MyStruct b {};                 // initialized to zeroed out memory (via implicit constructor)
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

A field may be initialized to a value either through default member initialization or the member initializer list. For default member initializations, the initialization is done directly in the field's declaration.

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

```{seealso}
Core Language/Classes/Deleted Implementations_TOPIC
```

### Destruction

`{bm} /(Core Language\/Classes\/Destruction)_TOPIC/`

```{prereq}
Core Language/Classes/This Pointer_TOPIC
Core Language/Classes/Construction_TOPIC
```

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

```{note}
When inheritance is involved, it's almost always to make the destructor a virtual function.
```

```{seealso}
Core Language/Classes/Inheritance_TOPIC
```

### Copying

`{bm} /(Core Language\/Classes\/Copying)_TOPIC/`

```{prereq}
Core Language/Classes/This Pointer_TOPIC
Core Language/Classes/Construction_TOPIC
Core Language/Classes/Operator Overloading_TOPIC
Core Language/Classes/Deleted Implementations_TOPIC
```

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

To suppress the compiler from allowing copying or assignment of an object, add ` = delete` after both signatures instead of specifying a body. This is important if the object holds on to an uncopyable resource such as a lock.

```c++
class MyStruct {
    ...

    MyStruct(const MyStruct &orig) = delete;
    MyStruct& operator=(const MyStruct &orig) = delete;
}
```

````{note}
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
````

### Moving

`{bm} /(Core Language\/Classes\/Moving)_TOPIC/`

```{prereq}
Core Language/Classes/This Pointer_TOPIC
Core Language/Classes/Construction_TOPIC
Core Language/Classes/Operator Overloading_TOPIC
Core Language/Classes/Copying_TOPIC
Core Language/Classes/Deleted Implementations_TOPIC
Core Language/Variables/Rvalue References_TOPIC
```

There are two built-in mechanisms for moving in C++: the move constructor and move assignment. Moving is different from copying in that moving actually guts the insides (data) of one object and transfers it into another, leaving that object in an invalid state. If the scenario allows for it, moving is oftentimes more efficient than copying.

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
MyStruct c { std::move(a) };  // std::move returns MyObject && type, which calls MyObject's move constructor
// a is in an invalid state
```

```{note}
Don't `std::move` into a variable and pass that variable to the constructor. The reason is that the variable will be treated as an lvalue (an lvalue to an rvalue reference), meaning that the copy constructor will get invoked instead of the move constructor.
```

In the example above, the move constructor has `noexcept` set to indicate that it will never throw an exception. Move constructors that can throw exceptions are problematic for the compiler to use. If a move constructor throws an exception, the source object will likely enter into an inconsistent state, meaning the program will likely be in an inconsistent state. As such, if the compiler sees that the move constructor can throw an exception, it'll prefer to copy it instead.

Similarly to the move constructor, move assignment is a method invoked when the assignment operator is used, called an operator overload. It has the same parameter list and it shouldn't throw exceptions either (`noexcept`), the only difference is that it returns a reference to itself at the end.

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

```
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

### Default Implementations

`{bm} /(Core Language\/Classes\/Default Implementations)_TOPIC/`

```{prereq}
Core Language/Classes/Construction_TOPIC
```

The compiler may automatically generate default implementations for some member functions (e.g. default constructor), called special member functions. However, under certain conditions, it may choose to omit generating them. If the compiler chooses to not generate a default implementation where one was expected, it's possible to force the compiler to generate that function by explicitly declaring it but replacing the function body `= default`.

```c++
struct MyClass {
    MyStruct() = default;        // forcefully generate default constructor
}
```

```{note}
Reasons why a compiler may decide to skip generating a function: it doesn't think it's needed, it doesn't think the behavior will be correct, ...?
```

### Deleted Implementations

`{bm} /(Core Language\/Classes\/Deleted Implementations)_TOPIC/`

```{prereq}
Core Language/Classes/Construction_TOPIC
```

The compiler may automatically generate default implementations for some member functions (e.g. default constructor), called special member functions. There are two ways to turn off these automatically generated member functions. The first way is to declare the function but make it privately scoped so that nothing outside can access it.

```c++
struct MyClass {
    ...
private:
    MyStruct() { };             // default constructor is private
}
```

The second way is to explicitly declare the function but mark it as deleted by appending `= delete` in place of the function body.

```c++
struct MyClass {
    MyStruct() = delete;        // default constructor is forcefully deleted
}
```

```{note}
The 2nd way is the more "modern" way to do it.
```

### Inheritance

`{bm} /(Core Language\/Classes\/Inheritance)_TOPIC/`

```{prereq}
Core Language/Classes/Construction_TOPIC
Core Language/Classes/Destruction_TOPIC
```

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

To be able to override a method in a child class the same way as it's done in other languages (e.g. Java), the base call must have the `virtual` keyword prepended on the method, making it a virtual method. Similarly, any method that overrides a virtual method should have the `override` keyword appended just after the parameter list.

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

If the base class and child class have the exact same non-virtual method, which method gets called depends on the type of the variable.

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

To prevent a method from being overridable at all, add the `final` keyword just after the parameter list.

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

### Interfaces

`{bm} /(Core Language\/Classes\/Interfaces)_TOPIC/`

```{prereq}
Core Language/Classes/Inheritance_TOPIC
```

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

`{bm} /(Core Language\/Classes\/Operator Overloading)_TOPIC/`

```{prereq}
Core Language/Classes/This Pointer_TOPIC
Core Language/Operators_TOPIC
```

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

Those `const`s ensure that the operands aren't changed in the method. Imagine that you're performing `x = y + z`. It doesn't make sense for `y` or `z` to get modified.

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

### Three-way Comparison Overloading

`{bm} /(Core Language\/Classes\/Three-way Comparison Overloading)_TOPIC/`

```{prereq}
Core Language/Classes/Operator Overloading_TOPIC
```

The three-way comparison operator, also called the spaceship operator, is a more terse way of providing comparison operators for a class. Typically, if a class is sortable and comparable, it should provide operator overloads for the typical comparison operators:

 * equality (==)
 * inequality (!=)
 * less-than (<)
 * less-than or equal (<=)
 * greater-than (>)
 * greater-than or equal (>=)

The three-way comparison operator bundles _at least_ the last four of those (potentially all of them) into a single operator, where the symbol for that operator is an equal-sign sandwiched between angle brackets (\<=\>).

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

 * `std::partial_ordering` -- same as `std::weak_ordering`, but with the addition that objects may not be comparable at all.

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

[Here](https://news.ycombinator.com/item?id=20550165) talks about the importance of choosing the right ordering type.

The rectangle example was lifted from [here](https://blog.tartanllama.xyz/spaceship-operator/).
```


### Conversion Overloading

`{bm} /(Core Language\/Classes\/Conversion Overloading)_TOPIC/`

```{prereq}
Core Language/Classes/Operator Overloading_TOPIC
Core Language/Variables/Implicit Conversion_TOPIC
Core Language/Variables/Explicit Conversion_TOPIC
```

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

### Const / Volatile Overloading

`{bm} /(Core Language\/Classes\/Const \/ Volatile Overloading)_TOPIC/`

```{prereq}
Core Language/Classes/Operator Overloading_TOPIC
Core Language/Classes/Constant_TOPIC
Core Language/Classes/Volatile_TOPIC
```

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

### Reference Overloading

`{bm} /(Core Language\/Classes\/Reference Overloading)_TOPIC/`

```{prereq}
Core Language/Classes/Operator Overloading_TOPIC
Core Language/Variables/References_TOPIC
Core Language/Variables/Rvalue References_TOPIC
Core Language/Classes/Moving_TOPIC
```

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

### Functors

`{bm} /(Core Language\/Classes\/Functors)_TOPIC/`

```{prereq}
Core Language/Classes/Operator Overloading_TOPIC
Core Language/Functions_TOPIC
```

A functor, also called a function object, is a class that you can invoke as if it were a function because it has an operator overload for function-call.

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

### Friends

`{bm} /(Core Language\/Classes\/Friends)_TOPIC/`

```{prereq}
Core Language/Classes/This Pointer_TOPIC
```

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
int t = addAndNegate(obj,5);
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
int t = obj_friend.addAndNegate(obj,5);
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

### User-defined Literals

`{bm} /(Core Language\/Classes\/User-defined Literals)_TOPIC/`

```{prereq}
Core Language/Classes/Operator Overloading_TOPIC
```

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

| type                  | definition                                                   |
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

```{seealso}
Library Functions/Time/Durations_TOPIC
```

## Lambdas

`{bm} /(Core Language\/Lambdas)_TOPIC/`

```{prereq}
Core Language/Classes/Functors_TOPIC
Core Language/Classes/Constant_TOPIC
Core Language/Constant Expressions_TOPIC
Core Language/Templates/Auto Syntax_TOPIC
```

Lambdas are unnamed functors (not functions) that are expressed in a succinct form. Lambdas in C++ work similarly to lambdas in other high-level languages. They capture copies of / references to objects from the outer scope such that they can be used for whatever processing the functor performs.

For example, consider the following functor.

```c++
// define
constexpr struct MyFunctor {
    MyFunctor(int x) {
        this->x = x;
    };

    constexpr int operator()(int a) const {
        return a + x;
    }
private:
    int x;
};

// instantiate
MyFunction f1{ 5 };

// invoke
f1(42);
```

The functor above can be written much more succinctly as a lambda.

```c++
// define and instantiate
auto f2 { [x=5] (int a) -> int { return a + x; } };

// invoke
f2(42);
```

The general syntax of a lambda is as follows: `[capture-list] (parameter-list) modifiers -> return-type { body }`. The subsections below detail this general syntax.

```{note}
Be aware that, by default, the function-call operator in the lambda version is `const` and will automatically be made into a `constexpr` if it satisfies all the requirements of `constexpr`. This is discussed more in the modifiers subsections.
```

### Capture List

`{bm} /(Core Language\/Lambdas\/Capture List)_TOPIC/`

```{prereq}
Core Language/Classes/Moving_TOPIC
```

`[capture-list]` is a _required_ part of `[capture-list] (parameter-list) modifiers -> return-type { body }` that defines and sets member variables inside the functor. It's a comma separated list where each element is a list is a variable to capture as a member variable. 

There are 3 different ways to capture member variables.

 * **Copy** a variable from the outer scope.
    
   To create a copy of an individual variable into the functor, put the variable's name in the capture list.

   ```c++
   int x {5};
   int y {6};
   // explicitly copy x and y from outer scope
   auto f { [x, y] (int z) -> int { return x + y + z; } };
   ```

   One way to avoid listing out individual variable names is to put `=` as the first element of the capture list. When `=` is present, missing member variables will automatically get copied as member variables.

   ```c++
   int x {5};
   int y {6};
   // explicitly copy x and implicitly copy y from outer scope
   auto f { [=, x] (int z) -> int { return x + y + z; } };
   ```

   If used within an enclosing class, the `this` pointer can be captured.

   ```c++
   auto f { [this] (int z) -> int { return z + this->x; } };   // capture this as a pointer
   auto f { [*this] (int z) -> int { return z + this->x; } };  // capture a COPY OF *this and pass it in as a pointer
   ```

   ```{note}
   It's mentioned that prior to C++20, automatic copy capturing (`[=]`) would pull in `this`. That feature has been deprecated.
   ```

 * **Reference** a variable from the outer scope.

   To create reference to an individual variable into the functor, put the variable's name in the capture list preceded by an ampersand (&).

   ```c++
   int x {5};
   int y {6};
   // explicitly reference x and y from outer scope
   auto f { [&x, &y] (int z) -> int { return x + y + z; } };
   ```

   One way to avoid listing out individual variable names is to put `&` as the first element of the capture list. When `&` is present, missing member variables will automatically get referenced as member variables.

   ```c++
   int x {5};
   int y {6};
   // explicitly reference x and implicitly reference y from outer scope
   auto f { [&, &x] (int z) -> int { return x + y + z; } };
   ```

 * **Initialize** a variable using an expression.

   When a variable name is followed by `=` and an expression, the expression is evaluated and captured.

   ```c++
   int x {5};
   int y {6};
   auto f { [mod_x=x/2, mod_y=y/2] (int z) -> int { return mod_x + mod_y + z; } };
   ```

   This is especially useful for capturing an object by moving it (as opposed to copying it or referencing it).

   ```c++
   auto f { [o=std::move(my_obj)] (int z) -> int { return o.do_something(z); } };
   ```

### Parameter List

`{bm} /(Core Language\/Lambdas\/Parameter List)_TOPIC/`

`(parameter-list)` is a _required_ part of `[capture-list] (parameter-list) modifiers -> return-type { body }` that defines the parameter list of the functor's function-call operator.

```c++
auto f1 { [] (int x, int y) -> int { return x + y; } };
auto f2 { [] (int x, int y = 99) -> int { return x + y; } };  // default args
auto f3 { [] (auto x, auto y) -> int { return static_cast<int>(x + y); } };  // templated params (compiler deduces types based on usage)
```

Lambda parameter lists are defined similarly to standard function parameter lists. It's common for a lambda's parameter list to use template parameters via `auto` as is done in `f3` of the example above. The reason for using `auto` is that the lambda can still work even if you don't know / can't predict the exact types of the arguments passed in (e.g. you know the arguments will be integral types, but you don't know exactly which exact integral types).

```{note}
`auto` is a placeholder for a template parameter, and as such type deduction rules come into play. If you aren't careful, you'll end up with strange or incorrect behaviour. For example, in certain cases the compiler may decide to create a local copy for an argument that gets passed in where you may be expecting a reference.
```

```{seealso}
Core Language/Templates/Type Deduction_TOPIC
```

### Return Type

`{bm} /(Core Language\/Return Type)_TOPIC/`

```{prereq}
Core Language/Variables/Arrays_TOPIC
Core Language/Variables/Pointers_TOPIC
Core Language/Templates/Type Deduction_TOPIC
```

`return-type` is an _optional_ part of `[capture-list] (parameter-list) modifiers -> return-type { body }` that defines the return type of the functor's function-call operator. The syntax of using an arrow and defining the type after the parameter list is called the trailing return syntax.

```c++
auto f1 { [] (int a, int b) -> int { return a+b; } };
auto f2 { [] (MyObject* v) -> const MyObject& { return v[5]; } };
```

```{seealso}
Core Language/Templates/Type Deduction/Type Cloning Deduction_TOPIC (different use-case for trailing return type syntax)
```

When a lambda doesn't provide a return type, the return type is implicitly `auto`. The compiler uses standard template parameter type deduction rules to determine what the return type should be.

```c++
auto f3 { [] (int a, int b) { return a+b; } };  // return deduced to int
auto f4 { [] (MyObject* v) { return v[5]; } };  // return deduced to MyObject
```

In `f4`, even though `v[5]` returns a `const MyObject &`, type deduction rules evaluate it to `const MyObject` (not a reference). That means `f4` returns a copy of the object at `v[5]` rather than a reference to the real thing. Type deduction rules such as the one here may end up causing subtle bugs if you aren't careful.

Another option is to explicitly return `decltype(auto)`, which copies the exact type being returned.

```c++
auto f5 { [] (MyObject* v) -> decltype(auto) { return v[5]; } };  // return deduced to const MyObject&
```

```{note}
When unsure, it's best to explicitly declare the return type or use `decltype(auto)`. 
```

### Modifiers

`{bm} /(Core Language\/Classes\/Lambdas\/Modifiers)_TOPIC/`

```{prereq}
Core Language/Variables/Arrays_TOPIC
Core Language/Variables/Pointers_TOPIC
Core Language/Templates/Type Deduction_TOPIC
```

`modifiers` is an _optional_ part of `[capture-list] (parameter-list) modifiers -> return-type { body }` that lists the modifiers of the functor's function-call operator. Except for the following special cases, modifiers work the same way that they do for normal functions.

 * The function-call operator is set to be a `constexpr` function if it meets the requirements of being a constant expression. You can force it to be a constant expression by adding `constexpr` as one of the modifiers.

   ```c++
   auto f1 { [] (int x, int y) constexpr -> int { return x + y; } };  // force as constant expression
   ```
 
 * The function-call operator is set to be a `const` function. You can force this off by adding `mutable` as one of the modifiers.

   ```c++
   auto f2 { [] (int x, int y) mutable -> int { return x + y; } };    // make non-const
   ```

### Template Parameters

`{bm} /(Core Language\/Classes\/Template Parameters)_TOPIC/`

```{prereq}
Core Language/Templates_TOPIC
```

A lambda may have template parameters added by injecting template parameters in angle brackets between `[capture-list]` and `(parameter-list)` of the lambda declaration `[capture-list] (parameter-list) modifiers -> return-type { body }`.

```c++
auto f1 { [] <typename T>(T x, T y) -> T { return x + y; } };
```

This is useful in cases where you need to be more explicit with the types of parameters / return types (`auto` is too loose). The most obvious case is with containers, where you likely want the underlying container type listed.

```c++
// f2 and f3 will do the same thing when passed a std::vector, but f3 is much more explicit.
auto f2 { [] (auto& v) -> const auto& { return v[7]; } };
auto f3 { [] <typename T>(std::vector<T>& v) -> const T& { return v[7]; } };
```

```{note}
Concept_TEMPLATEs may be used both with `auto` and with explicit template parameters (e.g. `T`). See the section on concept_TEMPLATEs to see how to they're applied in both cases.
```

```{seealso}
Core Language/Templates/Concepts_TOPIC
Library Functions/Containers_TOPIC
```

## Templates

`{bm} /(Core Language\/Templates)_TOPIC/`

```{prereq}
Core Language/Functions_TOPIC: Just enough to know how to define and use one.
Core Language/Classes_TOPIC: Just enough to know how to define and use one.
```

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

Declaring templated functions is done in the same manner as templated classes, and using templated functions is done similarly to templated classes: Use the function as if it were a normal function but immediately after the function name add in a comma separated list of substitutions sandwiched within angle brackets.

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

### Universal References

`{bm} /(Core Language\/Templates\/Universal References)_TOPIC/`

```{prereq}
Core Language/Templates/Concepts_TOPIC
Core Language/Variables/References_TOPIC
Core Language/Variables/Rvalue References_TOPIC
Core Language/Classes/Moving_TOPIC
```

Universal references allow for collapsing together multiple function overloads where the only differences between overloads are the same parameters being overloaded as both lvalue references and rvalue references. In the following non-templated code, the only difference between the overloads is that one takes a lvalue reference and the other takes a rvalue reference (and moves it).

```c++
void test(int & x) {
    if (x % 2 == 0) {
        vector.push_back(x);            // calls push_back(int &x)
    }
}

void test(int && x) {
    if (x % 2 == 0) {
        vector.push_back(std::move(x)); // calls push_back(int &&x)
    }
}

int main() {
    int val {5};
    test(5);    // calls test(int && x)
    test(val);  // calls test(int & x)
    return 0;
}
```

By templating the code above and forcing the compiler to deduce the parameter type through usage, the compiler can expand out the function overloads on its own.

```c++
template<typename T>
void test(T && x) {
    if (x % 2 == 0) {
        vector.push_back(std::forward<T>(x)); // forward to push_back(int &x) OR push_back(int &&x) based on the reference type
    }
}

int main() {
    int val {5};
    test(5);    // calls test(int && x)
    test(val);  // calls test(int & x)
    return 0;
}
```

In the example above, the parameter `x` is a universal reference. A universal reference has two ampersands (&&) as if it were a rvalue reference, but since the top-level type is a template parameter (`T` in this case) it's considered a universal reference. `std::forward<T>()` is used to maintain the rvalue-ness / lvalue-ness of the argument as it's passed forward into other functions.

```{note}
Not using `std::forward<T>()` will force the argument to get moved forward as a lvalue reference. You must use `std::forward<T>()` to maintain the type of reference.
```

For a parameter to be a universal reference, it must follow the pattern `NAME &&` where `NAME` is the template parameter.

 * Adding a `const`, `volatile`, or modifying it in any other way will make it go back to becoming a rvalue reference rather a universal reference.
 * Nesting `NAME` as an argument of another type will make it get interpreted as a rvalue reference rather than a universal reference.

```c++
template<typename T>
void test(const T&& param) { ... }      // BAD: && means rvalue reference (because of const)

template<typename T>
void test(MyClass<T> && param) { ... }  // BAD: && means rvalue reference (because it's wrapped in a concrete type)

template<typename T>
void test(T&& param) { ... }            // OK: “&&” means universal reference
```

More examples of universal references in different contexts:

```c++
// CONTEXT: Multiple universal references of different types.
template<typename T, typename U>
void test(T && x, U && y) {
    if (x % 2 == 0) {
        vector.push_back(std::forward<U>(y));
    }
}

// CONTEXT: Universal reference of a member function where the class itself is templated.
template<typename UNRELATED_PARAM>
struct MyClass {
    ...
    template<typename T, typename U>
    void test(T && x, U && y) {
        if (x % 2 == 0) {
            vector.push_back(std::forward<U>(y));
        }
    }
    ...
}
```

```{note}
The reason why universal references work is that the compiler is deducing the correct type for the template parameter based on how its used. If it gets passed a lvalue reference, it'll invoke the lvalue version. If it gets passed a rvalue reference, it'll invoke the rvalue version.

Internally, the compiler uses a technique called "reference collapsing" to get this to work, which temporarily / internally allows certain unallowable C++ constructs (references to references are disallowed). See [here](https://isocpp.org/blog/2012/11/universal-references-in-c11-scott-meyers) for more information.
```

````{note}
Concept_TEMPLATEs can be used to ensure that the underlying type of a universal reference is correct. In the example above, it's expected that the underlying type is `int`.

```c++
// VERSION 1: Accept only int, int &, or int &&
template<typename T>
  requires std::same_as<T, int> || std::same_as<T, int &> || std::same_as<T, int &&>
void test(T && x) {
    ...
}

// VERSION 2: Must be the same as int once you strip the reference and const/volatile off
template<typename T>
  requires std::is_same_v<std::remove_cv_t<std::remove_reference_t<T>>, int>
void test(T && x) {
    ...
}
```
````

### Auto Syntax

`{bm} /(Core Language\/Templates\/Auto Syntax)_TOPIC/`

```{prereq}
Core Language/Templates/Universal References_TOPIC
```

`auto` may be used as shorthand for template parameters. If a parameter has a type of `auto`, that `auto` assumes the place of a unique template parameter (e.g. `T`).

```c++
void func(auto p);          // template<T> void func(T p);
void func(auto & p);        // template<T> void func(T & p);
void func(auto * p);        // template<T> void func(T * p);
void func(const auto & p);  // template<T> void func(const T & p);
void func(const auto * p);  // template<T> void func(const T * p);
void func(auto && p);       // template<T> void func(T && p);
```

Likewise, if a return type has a type of `auto` it assumes the place of a unique template parameter.

```c++
auto func(int p);          // template<T> T func(int p);
```

`auto` is typically also used for variable declarations. One important aspect of `auto` for variable declarations to be aware of: Braced initialization / braced-plus-equals initialization produces an `std::initializer_list<T>` rather than just `T`.

```c++
int x = 5;     // x is int of 5
int x (5);     // x is int of 5
int x {5};     // x is int of 5
int x = {5};   // x is int of 5

// ... vs ...

auto x = 5;    // x is int of 5
auto x (5);    // x is int of 5
auto x {5};    // x is std::initializer_list<int>
auto x = {5};  // x is std::initializer_list<int>
```

````{note}
This seems to mesh with how certain classes work. For example, to create a `std::vector<int>`, you can pass in an `std::initializer_list<int>` via its constructor to prime it with a set of values. That `std::initializer_list<int>` is typically created using the curly brace syntax.

```c++
std::vector<int> v ( {1, 2, 3, 4, 5} );
```

**However**, when you use `auto` as the return type of a function OR `auto` for parameters in a lambda, the curly-brace to `std::initializer<T>` conversion discussed below doesn't happen. The compiler will fail to deduce the type if you use supply a list in curly braces.
````

```{note}
Later sections discuss template deduction and `decltype(auto)`, both of which are important to know about when using template parameters. `decltype(auto)` can be used for variable declarations as well.
```

```{seealso}
Core Language/Templates/Type Cloning_TOPIC (`decltype(...)` usage)
Core Language/Templates/Type Deduction_TOPIC
Core Language/Templates/Type Deduction/Type Cloning Deduction_TOPIC (`decltype(auto)` usage)
```

### Type Cloning

`{bm} /(Core Language\/Templates\/Type Cloning)_TOPIC/`

```{prereq}
Core Language/Classes/Functors_TOPIC
Core Language/Lambdas_TOPIC
```

To automatically derive the type of a variable something to be passed in as a template parameter, use `decltype()`. This is useful in scenarios where it's difficult or impossible to determine the exact type for a template parameter (e.g. functions, functors, template parameters).

```c++
// declare
template <typename FUNC_TYPE>
void perform(FUNC_TYPE * func) {
    func(55);
}

// use
auto my_lambda = [](int x) { std::cout << x; };
perform<decltype(my_lambda)>(my_lambda};
```

`decltype()` can take in either an entity (as shown above) or an expression.

```c++
// declare
template <typename N>
void perform(N n) {
    std::cout << n;
}

// use
MyClass myClass{}
perform<decltype(myClass.numVar + 1L)>(my_lambda}; // N set to whatever type "myClass.numVar + 1L" evaluates to
```


````{note}
The book mentions that, if you're going to use `decltype()`, don't wrap the expression in brackets. The reason is that `decltype()`, for whatever reason, will end up interpreting it different than what it is.

```c++
int x { 5 };

decltype(x)    // will be an int
decltype((x))  // will be an int &
```
````

### Type Deduction

`{bm} /(Core Language\/Templates\/Type Deduction)_TOPIC/`

```{prereq}
Core Language/Templates/Universal References_TOPIC
Core Language/Templates/Auto Syntax_TOPIC
```

C++ templates allow for template parameters to be deduced based on usage.

```c++
template<typename T>
bool test(T x) {
    return x % 2 == 0;
}

test(5);     // equivalent to test<int>(5)
test(5ULL);  // equivalent to test<unsigned long long>(5ULL)
```

The following subsections detail type deduction rules for templates as well as edge cases and workarounds.

#### Deduction Rules

`{bm} /(Core Language\/Templates\/Type Deduction\/Deduction Rules)_TOPIC/`

```c++
template<typename T>
bool test(T p) {
    return p % 2 == 0;
}
```

What the type `T` gets deduced to depends on what `p` is specified as and what type gets passed into `p` as an argument. 

```c++
int a { 5 };
const int * aPtr { &a };


// Scenario #1: p is just "T" by itself
template<typename T>
bool test1(T p) {
    return *p % 2 == 0;
}
test1(aPtr);

// Scenario #2: p is "T *"
template<typename T>
bool test2(T * p) {
    return *p % 2 == 0;
}
test2(aPtr);

// Scenario #2: p is "const T *"
template<typename T>
bool test3(const T * p) {
    return *p % 2 == 0;
}
test3(aPtr);
```

The idea with C++'s type deduction is that it tries to do the right thing through pattern matching. In the example above, `T` was deduced to be the correct type in each of the scenarios.

 * In scenario 1, `T=const int *`.
 * In scenario 2, `T=const int`.
 * In scenario 3, `T=int`.

Pattern matching attempts to deduce template parameter `T` based on...

 * how `T` is used for function parameter `p`,
 * what expression `e` is passed as the argument to `p`.

```c++
template<T>
void func(??? p) { // ??? can be T, T&, const T, const T&, ...
    ...
}

func(e); // Given the expression e, func()'s parameter p, what will T be?
```

For value types, pointer types, lvalue reference types, and rvalue reference types, the rules are as follows:

 * When `e` and `p` are both values, `const` / `volatile` will never transfer over to `T` because a copy of `e` is being passed in.
 * When `e` and `p` are both pointers, `const` / `volatile` will transfer over to `T` if not already set on `p`.
 * When `e` and `p` are both references, `const` / `volatile` will transfer over to `T` if not already set on `p`.
 * When `e` is a value but `p` is a reference, `e` gets passed into the function as a reference (`const` / `volatile` are maintained on `e`'s reference, see rule where both `e` and `p` are references).
 * When `e` is a reference but `p` is a value, `e` gets passed into the function as a copy of the value it references (`const` / `volatile` are removed from `e`'s copy, see rule where both `e` and `p` are values).

|              | p=T         | p=const T | p=T&        | p=const T& | p=T*        | p=const T* |
|--------------|-------------|-----------|-------------|------------|-------------|------------|
| e=int        | T=int       | T=int     | T=int       | T=int      |             |            |
| e=const int  | T=int       | T=int     | T=const int | T=int      |             |            |
| e=int&       | T=int       | T=int     | T=int       | T=int      |             |            |
| e=const int& | T=int       | T=int     | T=const int | T=int      |             |            |
| e=int*       |             |           |             |            | T=int       | T=int      |
| e=const int* |             |           |             |            | T=const int | T=int      |

```{note}
* `volatile` not included in above matrix to keep things simple. It behaves just like `const`.
* rvalue references not included in the matrix to keep things simple. It behaves just like lvalue references.
```

```{note}
The rules above work for return types exactly the same way that they do for parameter types: `e` ends up being the expression being returned by the function and `p` is the function's return type.
```

For universal references, the rules are more complicated. `p` gets reinterpreted based on whether `e` is a lvalue reference or rvalue reference:

 * When `e` is a lvalue reference, both `p` and `T` will be interpreted as lvalue reference to the core type.
 * When `e` is a rvalue reference, `p` is interpreted as an rvalue reference and `T` is the reference-less version of `p`.

|                | p=T&&                                      |
|----------------|--------------------------------------------|
| e=int&         | T=int& (p interpreted as int&)             |
| e=const int&   | T=const int& (p interpreted as const int&) |
| e=int&&        | T=int (p interpreted as int&&)             |
| e=const int&&  | T=const i (p interpreted as const int&&)   |

```{note}
What the above is saying is that, if e ends up being an rvalue reference, it uses the basic rules explained just previous to this universal references explainer. Recall that parameters that are universal references borrow the rvalue reference syntax of double ampersand (&&) -- double ampersands are universal references if the type is used in a parameter and left as-is (no `const`/`volatile`/etc..).

The types for `T` and `p` look invalid in lvalue cases but there's some special logic going on under the hood in terms of "reference collapsing" and doing things internally that would be explicitly illegal to do in code. For example, normally, if `p=int&` then `T=int`. But that isn't the case with universal references: `p=int&` (interpreted) but then `T=int&` as well.
```

````{note}
A quick-and-dirty way to determine what a type is deduced is to use `typeid()` in combination with querying type traits.

```c++
template<typename T>
void test(T p) {  // T or T& or const T or const T& or ...
    using P = decltype(p);
    using T_ref_removed = std::remove_reference<T>::type;
    using P_ref_removed = std::remove_reference<P>::type;
    using T_ref_and_cv_removed = std::remove_cv<T_ref_removed>::type;
    using P_ref_and_cv_removed = std::remove_cv<P_ref_removed>::type;
    // is_const/is_volatile must have ref removed for test to work: https://en.cppreference.com/w/cpp/types/is_const
    std::cout
        << "p: "
        << (std::is_const<P_ref_removed>::value ? "[const]" : "")
        << (std::is_volatile<P_ref_removed>::value ? "[volatile]" : "")
        << (std::is_lvalue_reference<P>::value ? "[&]" : "")
        << (std::is_rvalue_reference<P>::value ? "[&&]" : "")
        << typeid(P_ref_and_cv_removed).name()
        << "  /  "
        << "T:"
        << (std::is_const<T_ref_removed>::value ? "[const]" : "")
        << (std::is_volatile<T_ref_removed>::value ? "[volatile]" : "")
        << (std::is_lvalue_reference<T>::value ? "[&]" : "")
        << (std::is_rvalue_reference<T>::value ? "[&&]" : "")
        << typeid(T_ref_and_cv_removed).name()
        << std::endl;
}
```

`typeid()` by itself has a couple of issue:

 1. In certain cases, it won't output specifics of the type (see https://stackoverflow.com/q/37412265). I've tried to work around this by using type traits in the code above.
 
 2. The mains are mangled in G++ and clang (MSVC produces full type names). To de-mangle, you can use a command-line tool (that comes with most Linux g++/clang setups) called "c++-filt". For example, if `typeid().name()` outputs "PKi", ...

    ```
    user@localhost$ c++filt -t Pki
    int const*
    ```
````

```{note}
The book mentions a couple of niche cases to do with decaying of types.

 1. When `e` is a raw array (e.g. `e=int[13]`) and `p` is a reference type (e.g. `p=T&`, `p=const T&`, `p=T&&`, ...), `p` doesn't decay to a pointer (it doesn't become `p=int* &`). Instead, an actual reference to the array (including its size) gets passed in, meaning that it's possible to get the array's size via `sizeof()`. This isn't possible if it decayed to a pointer.
   
    The book recommends using `std::array` instead of relying on this.

 2. When `e` is a function and `p` is a reference type, `p` doesn't decay to a function pointer. It ends up being a reference to the actual function.

    The book mentions that, in practice, the non-decaying of functions rarely makes a difference to the code.
```

Type deduction for `auto` works almost exactly the same as template parameter type deduction. If a parameter type has `auto`, that `auto` assumes the place of a unique template parameter (e.g. `T`). What `auto` gets deduced to follows the same rules -- it takes into account the expression passed in as the argument for the parameter and how the parameter is specified (e.g. if it's `const`, a reference, a pointer, etc..).

```c++
void func(auto p);          // template<T> void func(T p);
void func(auto & p);        // template<T> void func(T & p);
void func(auto * p);        // template<T> void func(T * p);
void func(const auto & p);  // template<T> void func(const T & p);
void func(const auto * p);  // template<T> void func(const T * p);
void func(auto && p);       // template<T> void func(T && p);
auto func(int p);           // template<T> T func(int p);
```

This extends to variable declarations that use `auto`. The rules are essentially the same:

 * `auto` assumes the role of the template parameter
 * The full type assumes the role of the parameter (e.g. if it's `const`, a reference, a pointer, etc..).
 * The initializing expression assumes the role of the argument being passed into the parameter.

```c++
const auto p = 5;
// Imagine p is a parameter in a function and 5 is the argument being passed into it:
//
// template<T>
// void func(const T p) {
//     ...
// }
// func(5);
```

The rules are the same even for variables typed as `auto &&`. When a variable type is `auto &&`, it's _interpreted as a universal reference rather than a rvalue reference_. It only becomes a rvalue reference if it's set to a rvalue reference. Otherwise, it's a lvalue reference.

```c++
int x { 22 };

auto && p1 = 52;  // p1 is rvalue reference
auto && p2 = x;   // p2 is lvalue reference
```

#### Type Cloning Deduction

`{bm} /(Core Language\/Templates\/Type Deduction\/Type Cloning Deduction)_TOPIC/`

```{prereq}
Core Language/Templates/Type Deduction/Deduction Rules_TOPIC
Core Language/Templates/Type Cloning_TOPIC
```

In certain cases, a variable declaration / return statement needs to replicate the exact type of whatever expression is being assigned to it. This is possible with `decltype(auto)`.

```c++
// funcA()'s return type is the exact same as f_ptr()'s return type.
template<typename F>
decltype(auto) funcA(F * f_ptr, int index) {
    return f_ptr(index);
}

// x's type is the exact same as f()'s return type.
decltype(auto) x = f(a1, a2, a3, a4);
```

This is needed because, with normal type deduction rules, the deduction of `T` changes based on how the overall type is specified (e.g. (e.g. `T`, `const T`, `T&`, `T*`, etc..) and the type of the expression that gets assigned to it.

```{note}
See previous section for a refresher on type deduction rules.
```

```c++
template<typename F, typename T>
T funcA(F * f_ptr, int index) {
    return f_ptr(index);
}

// What does T get deduced as here? Impossible to know because the signature of "f_ptr()" isn't known beforehand. But,
// if "f_ptr(index)" returns a reference, type deduction rules say that T will end up stripping off the reference. So,
// for example, if "f_ptr(index)" returns "MyObject &", this function will end up returning a COPY of that object
// rather than the reference itself.
```

* If `f_ptr()` returns a copy and your return type is `T`, everything is okay.

  ```c++
  template<typename T, typename F>
  T test(F * f_ptr, int index) {
      return f_ptr(index); // f_ptr() returns a COPY and you return a COPY
  }
  ```

* If `f_ptr()` returns a reference and your return type is `T&`, everything is okay.

  ```c++
  template<typename T, typename F>
  T& test(F * f_ptr, int index) {
      return f_ptr(index); // f_ptr() returns a REFERENCE and you return a REFERENCE
  }
  ```

* If `f_ptr()` returns a reference but your return type is `T`, it's **inefficient code**. 

  ```c++
  template<typename T, typename F>
  T& test(F * f_ptr, int index) {
      return f_ptr(index); // f_ptr() returns a REFERENCE and you return a COPY of that reference -- it would have been fine
                           // to return just the reference itself
  }
  ```

* If `f_ptr()` returns a copy but your return type is `T&`, it's **faulty code**. 

  ```c++
  template<typename T, typename F>
  T& test(F * f_ptr, int index) {
      return f_ptr(index); // f_ptr() returns a COPY and you return a REFERENCE to that local copy -- copy is destroyed once
                           // this function exits meaning that the reference will be pointing to junk.
  }
  ```

If you don't know whether `f_ptr()` will return a reference or a copy (you just want to mirror back whatever its return type is), use `decltype(auto)`.

```c++
template<typename T, typename F>
decltype(auto) test(F * f_ptr, int index) {
    return f_ptr(index); // returns the exact type of f_ptr()
}
```

````{note}
The book mentions that, if you're going to use `decltype(auto)`, don't wrap the expression in brackets. The reason is that `decltype()`, for whatever reason, will end up interpreting it different than what it is.

```c++ 
// Example from the book
decltype(auto) f1() {
  int x = 0;
  return x;        // decltype(x) is int, so f1 returns int
}

decltype(auto) f2() {
  int x = 0;
  return (x);      // decltype((x)) is int&, so f2 returns int&
}
```
````

````{note}
The book mentions that, before `decltype(auto)`, you needed to use the trailing return type syntax to get similar behaviour when the return type depended on the parameter types.

```c++
template<typename T>
auto f1(T x) -> decltype(x + 5) {
    return x + 5;
}
```

You can't do something similar with the original return type syntax because the compiler doesn't know what's in the parameter list -- it hasn't parsed that part yet.

```c++
template<typename T>
decltype(x + 5) f1(T x) { // THIS WON'T WORK: x used in decltype() before it's encountered in parameter list
    return x + 5;
}
```
````

### Type Traits

`{bm} /(Core Language\/Templates\/Type Traits)_TOPIC/`

The C++ standard library includes a set of templated classes that detects the traits of a type at compile-time. This is useful in cases where template parameters need to be restricted.

```c++
template<typename T>
T test(T t) {
    static_assert(std::is_integral<T>::value, "Must be integral");
    return t + 1;
}

test(4);     // OK
test(4ULL);  // OK
test(4.09);  // FAIL -- 4.09 is a floating point number, not an integral number
```

The `value` field is `true` / `false` depending on if the type passes the check. A shortcut in later versions of C++ is to append `_v` to the name of the class performing the check rather than explicitly querying the `value` field (e.g. `std::is_integral<T>::value` vs `std::is_integral_v<T>`).

List of useful checks:

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

```{seealso}
Core Language/Variables/Aliasing_TOPIC (refresher)
```

Type traits may also be manipulated at compile-time via a set of templated classes.

```c++
template<typename T>
auto test(T t) {
    using R = std::make_unsigned<T>::type;  // R is same type as T but unsigned (if it already isn't)
    R x { t + 1 };
    return x;
}
```

The `type` field contains the name type. A shortcut in later versions of C++ is to append `_t` to the name of the class doing the manipulation rather than explicitly querying the `type` field (e.g. `std::make_unsigned<T>::type` vs `std::make_unsigned_t<T>`).

List of useful conversions:

 * `std::remove_cv` - remove `const` and / or `volatile`.
 * `std::remove_const` - remove `const`.
 * `std::remove_volatile` - remove `volatile`.
 * `std::remove_pointer` - make into non-pointer type (removes a `*` from the type).
 * `std::remove_reference` - make into non-reference type.
 * `std::add_cv` - add `const` and / or `volatile`.
 * `std::add_const` - add `const`.
 * `std::add_volatile` - add `volatile`.
 * `std::add_pointer` - make into pointer type (adds a `*` to the type).
 * `std::add_lvalue_reference` - make into a lvalue reference type.
 * `std::add_rvalue_reference` - make into a rvalue reference type.
 * `std::make_signed` - make into an equivalent version of the same type that's signed.
 * `std::make_unsigned` - make into an equivalent version of the same type that's unsigned.

```{note}
Are constant expressions used to write these checks and transformations? Maybe.
```

```{seealso}
Core Language/Constant Expressions_TOPIC
```

### Concepts

`{bm} /(Core Language\/Templates\/Concepts)_TOPIC/`

```{prereq}
Core Language/Templates/Type Traits_TOPIC
Core Language/Templates/Auto Syntax_TOPIC
```

In certain cases, a set of types substituted in for a template parameters won't produce working code.

```c++
// declare
template <typename X, typename Y, typename Z>
X perform(Y& var1, Z& var2) {
    return var1 + var2;
}
```

In the example above, `Y` and `Z` need to be types that support the plus operator (+) on each other (e.g. `int` and `short`) and the result must be of type `X` (or convertible to `X`). If types substituted for `X`, `Y`, and `Z` don't satisfy those conditions, the compiler gives back cryptic compilation errors.

Concept_TEMPLATEs may be used within a template to produce more straightforward compilation errors for bad type substitutions: A concept_TEMPLATE is a predicate, evaluated at compile-time (not runtime), that ensures a set of substituted types support specific type traits (e.g. supports plus operator, has a specific member function, has a copy constructor, etc..). The compiler gives back easier to understand compilation errors when the predicate fails.

Concept_TEMPLATEs themselves are templates where the `concept` keyword is used followed by its name and a compile-time evaluated expression that returns a `bool`. For example, the concept_TEMPLATE below uses the type traits library to ensure that `T` is both has a default constructor and a copy constructor.

```c++
template <typename T>
concept DefaultAndCopy = std::is_default_constructible<T>::value && std::is_copy_constructible<T>::value;
```

A concept_TEMPLATE's expression can invoke other concept_TEMPLATEs. For example, the concept_TEMPLATE below makes use of the example concept_TEMPLATE above and includes an additional type traits check to ensure that `T` also has a move constructor.

```c++
template <typename T>
concept DefaultAndCopyAndMove = DefaultAndCopy<T> && std::is_move_constructible<T>::value;
```

The C++ standard library includes a set of commonly used concept_TEMPLATEs. These concept_TEMPLATEs perform checks similar to the checks provided by the type traits library.

```c++
// equiv to DefaultAndCopyAndMove but written using the concepts library.
template <typename T>
concept DefaultAndCopyAndMove = std::default_initializable<T> && std::copy_constructible<T> && std::move_constructible<T>;
```

In cases where neither the type traits library nor the concept_TEMPLATEs library has the check you need, a special `requires` clause can be used to directly specify exactly what a type needs to support. This `requires` clause has a parameter list (exactly as if it were a function), and within its body is a list of expressions that _must_ be supported by the types.

```c++
template <typename T1, typename T2, typename TR>
concept MyConcept =
        requires(const T1* t1, const T2& t2) { // param list may also contain non-template types like int, float, ...
            { (*t1) + t2 } -> std::same_as<TR>;
            { (*t1) * t2 } -> std::same_as<TR>;
            { std::hash<T1>{}(*t1) } -> std::convertible_to<std::size_t>;
            { std::hash<T2>{}(t2)  } -> std::convertible_to<std::size_t>;
        }
        && std::is_default_constructible<T1>::value
        && std::is_default_constructible<T2>::value;
```

The `requires` clause in the example above pretends as if it's a function taking a pointer to a `const` (`T1`) and a lvalue reference to a `const` (`T2`).

 * When `T1` is dereferenced and either added / multiplied to `T2`, it must produce a type of `TR`.
 * When `T1` is dereferenced and passed to `std::hash`, it must produce a type that's convertible to `size_t`.
 * When `T2` is passed to `std::hash`, it must produce a type that's convertible to `size_t`.

```{note}
Note the syntax. Each statement in the body of `requires` is an expression that must result in a type that passes its concept_TEMPLATE check.
```

To apply a concept_TEMPLATE to a template, add a `requires` just before the body of the template with a concept_TEMPLATE expression. The concept_TEMPLATE expression is the exact same as the expressions used to define concept_TEMPLATEs: It's evaluated at compile-time, can reference type traits, can reference other concept_TEMPLATEs, can have a special parameter list `requires` clause, and must return a `bool`.

```c++
// templated function perform() using the concept "MyConcept" declared above.
template <typename T1, typename T2, typename TR>
    requires MyConcept<T1, T2, TR>
TR perform(T1 t1, T2 t2) { /* ... implementation ... */ }


// templated function perform() embedding the rules for that same concept.
template <typename T1, typename T2, typename TR>
    requires requires(const T1* t1, const T2& t2) {
        { (*t1) + t2 } -> std::same_as<TR>;
        { (*t1) * t2 } -> std::same_as<TR>;
        { std::hash<T1>{}(*t1) } -> std::convertible_to<std::size_t>;
        { std::hash<T2>{}(t2)  } -> std::convertible_to<std::size_t>;
    }
    && std::is_default_constructible<T1>::value
    && std::is_default_constructible<T2>::value;
TR perform(T1 t1, T2 t2) {
    /* ... implementation ... */
}
```

```{note}
The `requires requires` above is valid. The first `requires` is saying that this template is performing checks, and the second `requires` is the special parameter list `requires` clause that lists out what operations `T1`, `T2`, and `TR` must support.
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
    X x { var1 + var 2};
    return x * var2;
}
```

For function templates specifically, rather than parameterizing using `template`, a common shorthand is to use `auto` for the return type / parameter types being templated. The compiler automatically infers the correct types based on usage. Each `auto` parameter / return type can have a concept_TEMPLATE applied to it by placing that concept_TEMPLATE's name just before `auto`. For example, the usage of `SingleTypeConcept` in the example above can be rewritten as follows.

```c++
// usage of concept
SingleTypeConcept auto add_and_multiply(
    SingleTypeConcept auto &var1,
    SingleTypeConcept auto &var2
) {
    auto x { var1 + var 2};
    return x * var2;
}
```

````{note}
Be careful when making use of concept_TEMPLATEs like this. When `const auto` is involved, it'll break compilation. 

```c++
std::integral const auto f() {
    return 0;
}
```

The above function won't compile because there's something before the `const`. When a `const` is the left-most thing, it can't have anything further left of it. You need to move the `const` after `auto` (`const auto` is the exact same as `auto const`, having `const` as left-most thing is just a syntactical convenience thing).

```c++
std::integral auto const f() {
    return 0;
}
```
````

```{note}
Does this work with `decltype(auto)` as well?
```

```{seealso}
Core Language/Templates/Type Deduction/Type Cloning Deduction_TOPIC (`decltype(auto)` description)
```

#### Known Types

`{bm} /(Core Language\/Templates\/Concepts\/Known Types)_TOPIC/`

One of the most basic use-cases for concept_TEMPLATEs is to require that a type be one of a set of known types (e.g. require that the type be either `short`, `int`, or `long`). In the example below, a clever use of templates is used to test if the two types are equal, then a concept_TEMPLATE makes use of those templates to see if a type is contained in some larger set.

```c++
// templates
template<typename T, typename U>
struct is_same {
    static constexpr bool value = false; 
};

template<typename T>
struct is_same<T, T> { 
   static constexpr bool value = true; 
};


// concept for a function whose first parameter's type is an integral type
template<typename T>
concept integral_check = is_same<T, short>::value || is_same<T, int>::value || is_same<T, long>::value;


// usage
template<integral_check T>
long square(T num) {
    return num * num;
}

int main() {
    std::cout << square(2) << std::endl;
    std::cout << square(2L) << std::endl;
    return 0;
}
```

```{note}
In most cases, you shouldn't have to write out templates like `is_same<>` yourself. The C++ standard library provides the `type_traits` header library which contains `std::is_same<>` and several other type checks. The C++ standard library also provides a set of pre-built concept_TEMPLATEs that make use of check that a type has specific type traits. For example, `std::is_same<>` is exposed as the concept_TEMPLATE `std::same_as<>`.

Likewise, the C++ standard library provides a more elaborate version of `integral_check<>` as `std::integral<>`.
```

#### Callable Types

`{bm} /(Core Language\/Templates\/Concepts\/Callable Types)_TOPIC/`

```{prereq}
Core Language/Templates/Variadic_TOPIC
Core Language/Templates/Concepts/Known Types_TOPIC
```

Concept_TEMPLATEs can be used to specify the requirements for a callable object:

* How many parameters it takes in.
* The types allowed for each parameter / the type traits required by each parameter type.
* The types allowed for return / traits required by the return type.

Up to C++20, the C++ standard library doesn't provide much functionality for verifying the requirements above. The subsections below make clever use of templates to design checks for these requirements from scratch.

```{note}
These sub-sections come from my question on [stackoverflow](https://stackoverflow.com/q/73198589/1196226). Everything was tested on g++12.1 using C++20 standard. Newer versions of C++ or the g++ compiler might have better stuff to handle these types of requirements.
```

##### Parameter Counts

`{bm} /(Core Language\/Templates\/Concepts\/Callable Types\/Parameter Counts)_TOPIC/`

```{prereq}
Core Language/Templates/Variadic_TOPIC
Core Language/Constant Expressions_TOPIC
```

To test a callable object's parameter count within a concept_TEMPLATE, templates can be used to extract the parameter count. In the example below, the concept_TEMPLATE checks that a callable object has exactly 1 parameter.

```c++
// template(s) to extract parameter count
template <typename F>
struct argCnt;

template <typename R, typename ... As>
struct argCnt<R(*)(As...)> { static constexpr size_t cnt = sizeof...(As); };  // needed for std::integral<>

template <typename R, typename ... As>
struct argCnt<R(As...)> { static constexpr size_t cnt = sizeof...(As); };  // needed for std::integral<>


// concept for a callable object that has exactly 1 parameter
template<typename Fn>
concept MySpecialFunction = argCnt<Fn>::cnt == 1;


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

```{note}
Instead of using the templates show above, one other solution is to use [Boost's type traits library](https://www.boost.org/doc/libs/1_79_0/libs/type_traits/doc/html/boost_typetraits/reference/function_traits.html): `function_traits<my_func>::arity`.
```

##### Parameter Types

`{bm} /(Core Language\/Templates\/Concepts\/Callable Types\/Parameter Types)_TOPIC/`

```{prereq}
Core Language/Templates/Variadic_TOPIC
```

To test a callable object's parameter type within a concept_TEMPLATE, templates can be used to extract the parameter type. In the example below, the concept_TEMPLATE checks that a callable object's first parameter has a type conforming to the concept_TEMPLATE `std::integral`.

```c++
// template(s) to extract parameter types
template <std::size_t N, typename T0, typename ... Ts>
struct typeN { using type = typename typeN<N-1U, Ts...>::type; };

template <typename T0, typename ... Ts>
struct typeN<0U, T0, Ts...> { using type = T0; };

template <std::size_t, typename F>
struct argN;

template <std::size_t N, typename R, typename ... As>
struct argN<N, R(*)(As...)> { using type = typename typeN<N, As...>::type; };  // needed for std::integral<>

template <std::size_t N, typename R, typename ... As>
struct argN<N, R(As...)>  { using type = typename typeN<N, As...>::type; };  // needed for std::is_integeral_v<>


// concept for a function whose first parameter's type is an integral type
template<typename Fn>
concept MySpecialFunction = std::integral<typename argN<0U, Fn>::type>;


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


// type trait checks using static_assert() -- not necessary
static_assert( std::is_integral_v<typename argN<0U, decltype(square_int)>::type> );
static_assert( std::is_integral_v<typename argN<0U, decltype(square_long)>::type> );
```

```{note}
Instead of using the templates show above, one other solution is to use [Boost's type traits library](https://www.boost.org/doc/libs/1_79_0/libs/type_traits/doc/html/boost_typetraits/reference/function_traits.html): `function_traits<my_func>::argN_type`
```

````{note}
Cleverly using templates as shown above is the most robust way to check a parameter's type. But, if your requirements aren't overly complex, there may be simpler ways.

**SCENARIO 1: Testing for a known concrete types**

In this scenario, the requirement is that a callable object's parameter type be a concrete type that's known beforehand (e.g. `int`). The concept_TEMPLATE for the callable object itself can simply use a parameter list `requires` clause.

```c++
// concept for a function that takes in a single argument of type int
template <typename Fn>
concept MySpecialFunction = requires(Fn f, int t) {
            { f(t) } -> std::same_as<int>;
        };
```

**SCENARIO 2: Testing for a set of known concrete types**

In this scenario, the requirement is that a callable object's parameter be one of a set of concrete types that's known beforehand (e.g. `int` or `long`). The concept_TEMPLATE for the callable object can be exploded out into several sub-concept_TEMPLATEs: Each sub-concept_TEMPLATE checks that the callable object's parameter type match a specific concrete type, then those sub-concept_TEMPLATEs combine to form the full concept_TEMPLATE.

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

The problem with exploding out to sub-concept_TEMPLATEs is that the number of sub-concept_TEMPLATEs can get very large. For example, if the callable object should have 4 parameters and each of those parameters should be of type `int`, `long`, `short`, or `void*`, that's 256 different sub-concept_TEMPLATEs to list out.

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

Doing this removes the sub-concept_TEMPLATE explosion problem, but it introduces a new problem of the compiler losing the ability to infer template parameters from usage. In the example below, the concept_TEMPLATE for the callable object is concise, but usages of `call()` now need to explicitly specify what each template argument is because the C++ compiler is no longer able to infer them on its own.

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
````

##### Return Types

`{bm} /(Core Language\/Templates\/Concepts\/Callable Types\/Return Types)_TOPIC/`

```{prereq}
Core Language/Templates/Variadic_TOPIC
Core Language/Templates/Concepts/Callable Types/Parameter Types_TOPIC
```

To test a callable object's return type within a concept_TEMPLATE, templates can be used to extract the type. In the example below, the concept_TEMPLATE checks that a callable object has a return type of integral.

```c++
// template(s) to extract return types
template <typename F>
struct returnType;

template <typename R, typename ... As>
struct returnType<R(*)(As...)> { using type = R; };

template <typename R, typename ... As>
struct returnType<R(As...)> { using type = R; };


// concept for a function whose return type is an integral type
template<typename Fn>
concept MySpecialFunction =
    std::integral<typename returnType<Fn>::type>;


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

```{note}
Instead of using the templates show above, one other solution is to use [Boost's type traits library](https://www.boost.org/doc/libs/1_79_0/libs/type_traits/doc/html/boost_typetraits/reference/function_traits.html): `function_traits<my_func>::result_type`

Somewhat related as well from the C++ standard library: `std::result_of` / `std::invoke_result`.
```

````{note}
Cleverly using templates as shown above is the most robust way to check a callable object's return type. But, if your requirements aren't overly complex, it may be feasible to use simpler checks such as those discussed in the parameter types section before this section. For example, if the scenario allows for it, a concept_TEMPLATE check can be reduced to just a set of parameter list `requires` clauses being logically or'd together.

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
````

### Variadic

`{bm} /(Core Language\/Templates\/Variadic)_TOPIC/`

A variadic function is one that takes in a variable number of arguments, sometimes called varargs in other languages. A template can be made variadic by placing a final template parameter with `...` preceding the name, where this template parameter is referred to as parameter pack.

One common use-case for parameter packs is invoking functions where the parameter list isn't known before hand.

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

Another less common use-case is to repeatedly apply some operator or function.

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

Alternatively, rather than using recursion to exhaustively apply a binary operator, a fold expression may be applied to the parameter pack. A fold expression applies a binary operator to the contents of a parameter pack and returns the final result.

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

### Specialization

`{bm} /(Core Language\/Templates\/Specialization)_TOPIC/`

Given a specific set of substitutions for the template parameters of a template, a template specialization is code that overrides the template generated code. Oftentimes template specializations are introduced because they're more memory or computationally efficient than the standard template generated code. The classic example is a template that holds on to an array. Most C++ implementations represent a `bool` as a single byte, however it's more compact to store an array of `bool`s as a set of bits.

Declare a template specialization with the `template` keyword but without any template parameters (empty angle brackets). The class or function that follows should list out substitutions after its name and the code within it should be real (non-templated).

```c++
// template
template<typename T>
T sum(T a, T b) {
    return a + b;
}

// template specialization for bool: bitwise or
template<>
bool sum<bool>(bool a, bool b) {
    return a | b;
}
```

Template specialization doesn't have to substitute all template parameters. When a template specialization only provides substitutes for some of its template parameters, leaving other template parameters as-is or partially refined, it's called a partial template specialization.

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
Partial template specializations for functions aren't supported (yet?). See [here](https://stackoverflow.com/a/8061522).
```

In certain cases, the compiler is able to deduce the types for a specialization from its usage, meaning explicitly listing substitutions after the name may not be required.

```c++
// first example without explicitly listing out substitutions
template<>
bool sum(bool a, bool b) {  // type removed after name: "sum<bool>" to just "sum"
    return a | b;
}
```

### Type Aliasing

`{bm} /(Core Language\/Templates\/Type Aliasing)_TOPIC/`

```{prereq}
Core Language/Variables/Aliasing_TOPIC
```

Similar to classes and functions, type aliasing can be templated. A `template` declaration is needed before the the type alias itself.

```c++
template<typename T>
using V = std::vector<T>;

// usage
V<int> my_vec { 1, 2, 3 };
```

In certain cases, when using a templated type within a templated type alias, the keywords `typename` and `template` may be required within the type alias declaration itself.

```c++
struct Option {
    template<typename T>
    using Vector = std::vector<T>;
};

template<typename O, typename T>
using Vector = typename O::template Vector<T>;

// usage
Vector<Option, int> v { 1, 2, 3 };
```

The rules for this are complex, but essentially in certain cases the compiler can't decide how to parse a templated type alias and the keywords `typename` and `template` act as disambiguation. The compiler will usually generate an error telling you that `typename` is needed, but may not warn for `template` and essentially interpret it as something other than what the programmer intended.

```{note}
For a full breakdown, see [here](https://stackoverflow.com/a/613132).
```

## Coroutines

`{bm} /(Core Language\/Coroutines)_TOPIC/`

```{prereq}
Core Language/Functions_TOPIC
Core Language/Classes_TOPIC
```

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
It's said that the coroutine state is kept on the heap, resulting in C++ coroutines being a performance hog. Maybe it's possible to use a custom allocator to work around performance problems?
```

## Unions

`{bm} /(Core Language\/Unions)_TOPIC/`

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
int x = x.num_in;
int y = x.num_dbl;
```

```{seealso}
Library Functions/Utility Wrappers/Variant_TOPIC (consider using this instead of unions)
```

## Namespaces

`{bm} /(Core Language\/Namespaces)_TOPIC/`

```{prereq}
Core Language/Classes_TOPIC: Just enough to know how to define and use one.
```

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

To use the symbols within a namespace, either include them directly or bring all symbols within the namespace to the forefront via the `using` keyword (similar to Java's `import` or Python's `from` / `import`).

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

A special type of namespace, called an unnamed namespace, limits the visibility of the code to the containing translation unit. That means you can't reference an unnamed namespace in some other translation unit: It behaves as if you gave the namespace a unique name and never referenced that namespace outside of the translation unit.

```c++
// A.h
namespace {
    void help() {
        // ... code removed ...
    }
}

// B.h
#include "A.h"  // help() in A.h won't conflict with the help() here
void help() {
    // ... code removed ...
}
```

## Linker Behaviour

`{bm} /(Core Language\/Linker Behaviour)_TOPIC/`

```{prereq}
Core Language/Object Lifecycle_TOPIC
```

Modifiers on a variable or function declaration are used to control how the linker behaves. Specifically, the modifiers can ask the linker to automatically ...

 * merge the item that has the modifier applied (`inline`)
 * find the item that has the modifier applied (`extern`)
 * keep hidden the item that has the modifier applied (`static`). 

### Static Linkage

`{bm} /(Core Language\/Linker Behaviour\/Static Linkage)_TOPIC/`

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

### Inline Linkage

`{bm} /(Core Language\/Linker Behaviour\/Inline Linkage)_TOPIC/`

An inline function or variable is one that may be defined in multiple different translation units. The linker will make sure all translation units use a single instance of that function/variable even though it may have been defined multiple times.

Inline functions/variables have the `inline` modifier applied.

```c++
int add(int a, int b) inline {
    return a + b;
}
```

```{note}
See [this](https://stackoverflow.com/a/1759575). Typically, the compiler applies `inline` automatically based on what it sees, meaning that it isn't something that should be added by the programmer in most cases. The only exception to that seems to be templates? See some of the other answers in the linked stack overflow question.
```

```{note}
The original intent of `inline` was to indicate to the compiler that embedding a copy of the function for an invocation was preferred over an function call. The reason being that in certain cases the code would be faster if it were embedded rather than having it branch into a function call.
```

### External Linkage

`{bm} /(Core Language\/Linker Behaviour\/External Linkage)_TOPIC/`

An external function or variable is a one that's usable within the translation unit but isn't defined. The linker will sort out where the function is when the time comes.

External linkage functions/variables have the `extern` modifier applied.

```c++
extern int add(int a, int b);
```

```{note}
Sounds similar to forward declaration but across different translation units?
```

## Control Flow

`{bm} /(Core Language\/Control Flow)_TOPIC/`

C++ flow control structures are similar to those in other high-level languages (e.g. Java), with the exception that ...

 * it's possible to have initializer statements in control structures other than for loops.
 * jumping to arbitrary labels are allowed (goto statements).

```{note}
An important caveat about loops in C++ from [cppreference.com](https://en.cppreference.com/w/cpp/language/while):

> As part of the C++ forward progress guarantee, the behavior is undefined if a loop that has no observable behavior (does not make calls to I/O functions, access volatile objects, or perform atomic or synchronization operations) does not terminate. Compilers are permitted to remove such loops. 
```

### If Statement

`{bm} /(Core Language\/Control Flow\/If Statement)_TOPIC/`

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

### Switch Statement

`{bm} /(Core Language\/Control Flow\/Switch Statement)_TOPIC/`

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

### For Loop

`{bm} /(Core Language\/Control Flow\/For Loop)_TOPIC/`

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

### While Loop

`{bm} /(Core Language\/Control Flow\/While Loop)_TOPIC/`

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

### Goto Statement

`{bm} /(Core Language\/Control Flow\/Goto Statement)_TOPIC/`

Unlike most other high-level languages (e.g. Java), C++ allows the use of goto statements. However, note that goto statements are generally considered bad practice and should somehow be refactored to higher-level constructs (e.g. loops, if statements, etc..).

```c++
retry:
int r {rand()};
if (r % 2 == 0) {
    goto retry;
}
std::cout << r << " odd";
```

### Branching Likelihood

`{bm} /(Core Language\/Control Flow\/Branching Likelihood)_TOPIC/`

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

## Attributes

`{bm} /(Core Language\/Attributes)_TOPIC/`

```{prereq}
Core Language/Variables_TOPIC: Just enough to know how to define and use one.
Core Language/Functions_TOPIC: Just enough to know how to define and use one.
Core Language/Classes_TOPIC: Just enough to know how to define and use one.
```

C++ attributes are similar to annotations in Java, providing information to the user / compiler about the code that it's applied to. Unlike Java, C++ compilers are free to pick and choose which attributes they support and how they support them. There is no guarantee what action a compiler will take, if any, when it sees an attribute (e.g. compiler warnings).

An attribute is applied by nesting it in double square brackets (e.g. `[[noreturn]]`) and placing it as a modifier on the function.

```c++
[[noreturn]] void fail() {
    throw std::runtime_error { "Failed" };
}
```

Common attributes:

| attribute               | description                                                                                                                     |
|-------------------------|---------------------------------------------------------------------------------------------------------------------------------|
| `[[deprecated("msg")]]` | Indicates that a function is deprecated. Message is optional.                                                                   |
| `[[noreturn]]`          | Indicates that a function doesn't return.                                                                                       |
| `[[fallthrough]]`       | Indicates that a switch case was explicitly designed to fall through to the next case (no `break` / `return` / etc.. intended). |
| `[[nodiscard]]`         | Indicates that a function's result should be used somehow (produce compiler warning).                                           |
| `[[maybe_unused]]`      | Indicates that a function's result doesn't have to be used (avoid compile warning).                                             |

```{seealso}
Core Language/Variables/Common Attributes_TOPIC
Core Language/Functions/Common Attributes_TOPIC
Core Language/Classes/Common Attributes_TOPIC
```

## Constant Expressions

`{bm} /(Core Language\/Constant Expressions)_TOPIC/`

```{prereq}
Core Language/Variables_TOPIC: Just enough to know how to define and use one.
Core Language/Functions_TOPIC: Just enough to know how to define and use one.
Core Language/Classes_TOPIC: Just enough to know how to define and use one.
```

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

Constant expression functions can be used as normal functions as long as the arguments being passed into them aren't known at compile-time. If the arguments are known at compile-time, the function gets invoked during compilation.

````{note}
An alternate version of constant expression functions, called immediate functions, have the restriction that they must produce a compile-time constant. An immediate function requires prefixing `consteval` to a function instead of `constexpr`.

What's the point of this? According to [here](https://stackoverflow.com/a/53347377)...

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
 * **Class**: Constructor must be a constant expression. Non-static field initializers using braced initialization, equals initialization, or brace-plus-equals initialization must use constant expressions. The destructor must be a trivial destructor (non-virtual, does nothing, and all base class destructors do nothing).
 * **Union**: Must have at least one non-static member that is a literal type.

```{note}
The rules here are vast and complicated. The above might not be entirely correct, may be missing some conditions, or may not cover certain aspects. In the type_traits header, there's a function called `std::is_literal_type` that can be used to test if a type is a literal type.
```

There are several benefits to constant expressions. First, constant expressions help with reducing the use of hard coded numbers whose origins are obtuse, called magic numbers. A constant expression uses the computation to get to that obtuse magic number rather than the number itself, meaning it's easier to understand and requires less effort to tweak (via the parameters of the constant expression).

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

## Exceptions

`{bm} /(Core Language\/Exceptions)_TOPIC/`

```{prereq}
Core Language/Functions_TOPIC: Just enough to know how to define and use one.
```

C++ exceptions work similarly to exceptions in other languages, except that there is no `finally` block. The idea behind this is that resources should be bound to an object's lifetime (destructor). As the call stack unwinds and the automatic objects that each function owns are destroyed, the destructors of those objects should be cleaning up any resources that would have been cleaned up by the `finally` block. This concept_NORM is referred to as resource acquisition is initialization (RAII).

```{note}
What does accordingly mean? For example, wrap the dynamically allocated object in a class where allocation happens in the constructor / deallocation happens in the destructor. An automatic object of that class type will clean up properly when the function exits.
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

To catch an exception potentially being thrown, wrap code in a try-catch block. Typical inheritance rules apply when catching an exception. For example, catching a `std:runtime_error` type will also catch anything that extends from it as well (e.g. `std:overflow_error`).

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

## Structured Binding

`{bm} /(Core Language\/Structured Binding)_TOPIC/`

```{prereq}
Core Language/Variables_TOPIC: Just enough to know how to define and use one.
Core Language/Variables/References_TOPIC
Core Language/Functions_TOPIC: Just enough to know how to define and use one.
Core Language/Classes_TOPIC: Just enough to know how to define and use one.
```

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

## Expression Categories

`{bm} /(Core Language\/Expression Categories)_TOPIC/`

Value categories are a classification of expressions in C++. At their core, these categories are used for determining when objects get _moved_ vs copied, where a move means that the guts of the object are scooped out and transferred to another object.

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

In essence, the way to think of a prvalue is that it's an expression that meets the following 3 conditions ...

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

An lvalue is an expression that is the opposite of a prvalue. An lvalue expression CAN use the address-of operator (opposite of point 1 above), it CANNOT have guts scooped out and moved into something else (opposite of point 2 above), and it DOES persist (opposite of point 3 above). The typical example of an lvalue is an expression that's solely a variable name or function name.

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
MyObject c { std::move(a) };  // std::move returns MyObject && type, which calls MyObject's move constructor
// a is in an invalid state
```

```{note}
The example above is using features that haven't been introduced yet (`std::move`, rvalue references, move constructor). Just ignore it if you don't know those pieces yet. They're explained in other sections.
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

Similarly, if it's an expression that can be _moved_ (gutted), it's called an rvalue regardless of if the address-of operator can be used on it or not.

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

```{seealso}
Core Language/Variables/Rvalue References_TOPIC
Core Language/Classes/Moving_TOPIC
```

## Iterators

`{bm} /(Core Language\/Iterators)_TOPIC/`

```{prereq}
Core Language/Classes/Operator Overloading_TOPIC
```

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
 * dereferencing it (`*`) provides the value at the array element it points to.
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

 * Input iterator, steps forward one element at a time and reads items of the container.
 * Output iterator, steps forward one element at a time and writes items of the container.
 * Forward iterator, combination of input iterator and output iterator.
 * Bidirectional iterator, forward iterator with the ability to move back.
 * Random access iterator, bidirectional iterator with the ability to jump to different positions.

|                                                               | input | output | forward | bidirectional | random access |
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

## Modules

`{bm} /(Core Language\/Modules)_TOPIC/`

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

Similar to how non-module C++ source code is broken up into a source file containing definitions and accompanying header file containing declarations, a module may also be broken up into separate definition and declaration files. The declarations go in a file with `export module` at the top (as shown above) and the definitions go in a file with just `module`. Declaration files aren't allowed to use `export` at all.

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
Last I recall using this, each compiler required a special flag to turn on modules. Just because your code uses modules doesn't mean the internal C++ libraries (e.g. standard template library, `cstdint`, etc..) are going to expose things as modules. You still have to include those using the `#include <...>` directives (maybe -- I think I remember there being some roundabout way of getting modules to work).
```

## Preprocessor

`{bm} /(Core Language\/Preprocessor)_TOPIC/`

The preprocessor is a component of the C++ compiler. Before the programming statements in a source code file are compiled, the processor goes over the file looking for preprocessor directives. Preprocessor directives either...

1. perform some basic text manipulation.
1. signal certain things to the compiler (e.g. use a specific feature, turn off a specific feature, etc..).

The first case (text manipulation) is primarily what the preprocessor is used for. Unlike normal C++ programming statements, preprocessor directives start with the pound sign (#) and shouldn't include a semicolon (;) at the end.

To include one file in another file, use `#include`. Local files should be wrapped in quotes while files coming from libraries should be wrapped in angled brackets.

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

## Inconsistent Behaviour

`{bm} /(Core Language\/Inconsistent Behaviour)_TOPIC/`

High-level languages are typically very consistent. For example, except for a handful of small things, Java's runtime and core libraries are consistent across different platforms (e.g. Windows vs Linux), architectures (e.g. ARM vs x86), and compilers (e.g. OpenJDK vs Eclipse compiler). C++ has much less consistency than those other high-level languages because it has to support more platforms and architectures. In addition, having less consistency sometimes allows for more aggressive optimization during compilation.

Inconsistencies comes in three different types:

* Implementation-defined behaviour: Behaviour varies between implementations, where that behaviour is valid (e.g. no hard crash) and documented.
* Unspecified behaviour: Behaviour varies between implementations, where that behaviour is valid (e.g. no hard crash) but _not_ documented.
* Undefined behaviour: Behaviour is unrestricted (e.g. maybe hard crash, bad computation, or expected computation) and not documented.

|                                  | valid | documented |
|----------------------------------|-------|------------|
| Implementation-defined behaviour | YES   | YES        |
| Unspecified behaviour            | YES   | NO         |
| Undefined behaviour              | MAYBE | NO         |

### Implementation-defined Behaviour

`{bm} /(Core Language\/Inconsistent Behaviour\/Implementation-defined Behaviour)_TOPIC/`

Implementation-defined behaviour is behaviour that varies between implementations, where that behaviour is valid (e.g. no hard crash) and documented. The obvious example is with numeric data types: `short`, `int`, `float`, etc.. will each have a different minimum and maximum across different platforms:

 * `short` is from `SHORT_MIN` to `SHORT_MAX`.
 * `int` is from `INT_MIN` to `INT_MAX`.
 * ...

```{note}
Someone posted [this](http://eel.is/c++draft/impldefindex) as a comprehensive list of implementation-defined behaviour.
```

### Unspecified Behaviour

`{bm} /(Core Language\/Inconsistent Behaviour\/Unspecified Behaviour)_TOPIC/`

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

### Undefined Behaviour

`{bm} /(Core Language\/Inconsistent Behaviour\/Undefined Behaviour)_TOPIC/`

```{prereq}
Core Language/Variables/Pointers_TOPIC
Core Language/Variables/Arrays_TOPIC
```

```{note}
According to documentation online: "Compilers are not required to diagnose or do anything meaningful when undefined behaviour is present. Correct C++ programs are free of undefined behaviour". Not exactly sure how to fix some scenarios to be "free" of undefined behaviour. Specifically, there are a lot of cases where signed integer overflow (described below) happens, but that's undefined behaviour. I read online that the way to handle these cases is to test at the beginning of the function if overflow is possible and bail out if it is, but there's no built-in C++ mechanism to do that.

The statement and the examples below, were lifted from [here](https://en.cppreference.com/w/cpp/language/ub).
```

Undefined behaviour is behaviour that is unrestricted and not documented. The compiler may do anything for code producing undefined behaviour. For example, code producing undefined behaviour could end up ...

 * causing a hard crash.
 * doing exactly what the author of the source code originally intended for.
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

   A side-effect free infinite loop is a loop that goes on forever but doesn't change anything outside of its own scope (e.g. no global variable is changed, nothing is printed to standard out, etc..).

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

# Library Functions

`{bm} /(Library Functions)_TOPIC/`

```{prereq}
Core Language_TOPIC
```

By default, C++ comes packages with the C++ standard library. You can think of this as C++'s equivalent of core Java packages: collection classes in `java.util`, thread classes in `java.util.concurrent`, IO classes in `java.io`, etc... In addition, several third-party C++ libraries exist that provide commonly needed functionality. You can think of these are as C++'s equivalent to common Java libraries: Guava, Apache Commons, etc...

Common third-party C++ libraries:

* [Boost](https://www.boost.org/)
* [Absiel](https://abseil.io/) (Google)
* [Folly](https://github.com/facebook/folly) (Facebook)

The subsections below detail important functionality across the many C++ libraries in existence. If the functionality being documented is for a third party library, it'll be signalled in some way (e.g. namespace / header files / comments used in sample code will make it apparent).

## Allocators

`{bm} /(Library Functions\/Allocators)_TOPIC/`

Allocators allow for customizing how objects are allocated and deallocated. Some library APIs allow you to provide a custom allocator rather than using the typical `new`/`new[]` and `delete`/`delete[]` operators. In certain scenarios where performance is important (e.g. gaming, simulations, high-frequency trading, etc..), custom allocators are often used. A custom allocator could increase performance by ...

* using alternate data structures (e.g. finding free memory to assign to a new object is faster).
* using an object pool (e.g. an object put back into the pool and taken out again may not need to be fully re-initialized).
* attempting to allocate related objects closer together in memory (e.g. less cache misses).

By default, libraries that support custom allocators will default to `std::allocator`, which just wraps the `new`/`new[]` and `delete`/`delete[]` operators.

To implement a custom allocator, you need to create a templated class with a single template parameter representing the type being allocated / deallocated. The class must have the following traits...

1. a default constructor.
2. a constructor to "rebind" another allocator (copy).
3. a nested type alias `value_type` corresponding to the template parameter.
4. an allocate method.
5. a deallocate method.
6. operator overloads for equality inequality.

```c++
template <typename T>
struct MyAllocator {
    using value_type = T;  // 3

    MyAllocator() noexcept{ }  // 1
    
    template <typename U>
    MyAllocator(const MyAllocator<U>&) noexcept { }  // 2 (why is this here? https://docs.microsoft.com/en-us/cpp/standard-library/allocator-class?view=msvc-170#allocator)
    
    T* allocate(size_t n) { // 4
        auto ret = operator new(sizeof(T) * n);
        std::cout << "allocated!" << ret << "\n";
        return static_cast<T*>(ret);
    }
    
    void deallocate(T* p, size_t n) { //5
        std::cout << "deallocated!" << ret << "\n";
        operator delete(p);
    }
};

template <typename T1, typename T2>
bool operator==(const MyAllocator<T1>&, const MyAllocator<T2>&) { // 6 (why is this here? https://stackoverflow.com/a/30654267)
    return true; // always because this class retains no state
}

template <typename T1, typename T2>
bool operator!=(const MyAllocator<T1>&, const MyAllocator<T2>&) { // 6 (why is this here? https://stackoverflow.com/a/30654267)
    return false; // always because this class retains no state
}
```

```{note}
I don't fully understand what the copy constructor and the operator overloads are for. The copy constructor seems to be for cases where you pass in an allocator to some container class (e.g. `vector`) but that container class needs to allocate more than just the type you're interested in. For example, the allocator may be for creating `int`s (e.g. template parameter `T` = `int`) but the container class you're storing those `int`s may have bookkeeping structures that it wraps each `int` in (e.g. each `int` is wrapped as a `Node` object which also contains some extra pointers). This copy constructor "repurposes" the allocator, allowing you to to pass in `MyAllocator<int>` but have it repurposed to `MyAllocator<SomeOtherTypeHere>`.

But if you're copying the guts of one allocator into another but both keep on allocating and deallocating, won't they trip up over each other?

I haven't been able to find answers online as to what's going on here. The book just seems to hand wave it away.
```

```{note}
Why not just do operator overloading for the new operator? The answer seems to be that allocators are simpler to deal with and handle wider scenarios (such as the concatenating example in the note above).
```

## Smart Pointers

`{bm} /(Library Functions\/Smart Pointers)_TOPIC/`

```{prereq}
Library Functions/Allocators_TOPIC
```

```{seealso}
Core Language/Classes/Moving_TOPIC (refresher)
Core Language/Classes/Copying_TOPIC (refresher)
```

Smart pointers are classes that wrap pointers to dynamically objects. These wrappers provide some level of automated pointer management / memory management through the use of move semantics, copy semantics, and RAII. 

The subsections below document some common smart pointers and their usages.

### Scoped Pointer

`{bm} /(Library Functions\/Smart Pointers\/Scoped Pointer)_TOPIC/`

(non-moveable, non-copyable)

A scoped pointer wraps a pointer to an existing dynamic object / dynamic array and invokes `delete` / `delete[]` on it once it exits the current scope. It explicitly turns off class copy semantics and move semantics, meaning that copying a scoped pointer or moving it isn't allowed.

```c++
if (x == 123L) {
    boost::scoped_ptr<int> ptr { new int {5} };
    x += *ptr; // like a real pointer, use indirection operator / member of pointer operator 
} // ptr destroyed via delete operator at the end of if block (RAII)
```

Scoped pointers come in two flavours: 
   
 * `scoped_ptr`: pointer to a dynamic object.
 * `scoped_array`: pointer to a dynamic array.

```c++
boost::scoped_ptr<int> ptr { new int {5} };
boost::scoped_array<int> ptr { new int[4] {1, 1, 1, 1} }};
```

Although the official move semantics of a scoped pointer are to deny moves, it does provide a ...
   
 * `swap()` function that lets you swap the dynamic objects between two scoped pointers.
 * `destroy()` function that destroys the current dynamic object and sets it to the argument passed in, if any.

In addition, it's possible to have an unset scoped pointer (`nullptr`). An unset scoped pointer won't attempt to destroy an object when it goes out of scope.

### Unique Pointer

`{bm} /(Library Functions\/Smart Pointers\/Unique Pointer)_TOPIC/`

```{prereq}
Library Functions/Smart Pointers/Scoped Pointer_TOPIC
```

(moveable, non-copyable)

A unique pointer supports all the same features as a scoped pointer, except that it also supports moving: The ownership of the pointer that unique pointer has is transferable to another unique pointer via move semantics (e.g. assignment operator move constructor). Like scoped pointer, a unique pointer doesn't support copying.

```c++
if (x == 123L) {
    std::unique_ptr<int> ptr { new int {5} };
    x += *ptr;
    std::unique_ptr<int> ptr2 { std::move(ptr) };  // ALLOWED: move ptr into ptr2 -- ptr is invalid after this point
    x -= *ptr2;
}
```

Unlike scoped pointers, a unique pointer uses the same class for both dynamic objects and dynamic arrays.

```c++
std::unique_ptr<int> ptr { new int {5} };
std::unique_ptr<int[]> ptr { new int[4] {1, 1, 1, 1} }};
```

```{note}
Look at the template parameters in the example above. It's important that you add `[]` into the template parameter when you're dealing with arrays so the destroy dynamic array operator (`delete[]`) gets used. If the destroy dynamic object operator (`delete`) is used for an array, it's undefined behaviour. Likewise, don't add `[]` into the template parameter if you aren't dealing with arrays.
```

In older versions of C++, the templated function `std::make_unique()` was provided to create unique pointers because the normal way (shown in the example above) has subtle edge cases that could result in memory leaks. Newer versions of C++ fixed the memory leak problem, so using `std::make_unique()` isn't necessary but it's still available for backwards compatibility.

```c++
// following two are equivalent
std::unique_ptr<int> ptr { new int {5} };
std::unique_ptr<int> ptr = std::make_unique<int>(5);  // make_unique automatically calls new
```

Unique pointers don't support custom allocators: You pass the pointer you want to track directly into the constructor or create it via `std::make_unique()`. But, unique pointers do support taking in a function-like object (e.g. function, functor, lambda) to invoke instead of using `delete` / `delete[]` on the tracked pointer. This is useful in cases where the pointer is being tracked ...
   
 * wasn't created using `new` / `new[]` (e.g. `FILE *` created using `fopen()`).
 * needs to have deletion logged (e.g. print out whenever the object is deleted).
 * is associated with extra resources that need to be handled in some way on release.
    
For example, a unique pointer that points to a memory mapped file region shouldn't call `delete[]` when it goes out of scope because it isn't actually pointing to a dynamic array. Instead, it should invoke the relevant function(s) that release a memory mapped file region.

```c++
auto custom_deleter = [](int* x) {
    std::cout << "Deleting an int at " << x;
    delete x;
};
std::unique_ptr<int, decltype(custom_deleter)> ptr{ new int {5}, custom_deleter };
// NOTE: Types have to match -- if the unique pointer is for an "int", the custom deleter should take in an "int *"
```

### Shared Pointer

`{bm} /(Library Functions\/Smart Pointers\/Shared Pointer)_TOPIC/`

```{prereq}
Library Functions/Smart Pointers/Unique Pointer_TOPIC
```

(moveable, copyable)

A shared pointer tracks the number of copies it has in existence and only destroys the dynamic object it points to once the number of copies reaches 0 (reference counting). The reference count increments when a new copy is made (e.g. copy constructor) and decrements when a copy is destroyed (e.g. goes out of scope). Moves don't modify the reference count.

```c++
std::shared_ptr<int> ptr { new int {5} }; // ref count 1
if (x == 123L) {
    std::shared_ptr<int> ptrCopy { ptr }; // ref count 2
    x += *ptrCopy;
} // ref count back to 1 because ptrCopy destroyed here
x -= *ptr2;
```

```{note}
There's a version of shared pointer in Boost and one in the C++ standard library. The Boost version is legacy.
```

The construction of shared pointers is similar to the construction of unique pointers. You can either call the constructor directly or you can use the templated function `std::make_shared()`. Where as `std::make_unique()` was a legacy creation mechanism for unique pointers, `std::make_shared()` is the preferred creation mechanism for shared pointers. That's because shared pointers require a "control block" that holds onto tracking information (e.g. reference counts), and using `std:make_shared()` allocates that control block along with the dynamic object in one single allocation (better performance: one allocation vs two allocations).
   
```c++
std::shared_ptr<int> ptr { std::make_shared<int>(5) };  // allocates the control block and object together
std::shared_ptr<int> ptr { new int {5} };
std::shared_ptr<int[]> ptr { new int[4] {1, 1, 1, 1} }};
```

```{note}
The book says that sometimes you want to avoid `std::make_shared` because you might need the control block even if the dynamic object goes away (mentions weak pointers). This isn't possible if the control block and the dynamic object are allocated as one, because if they're allocated as one then you can't individually delete them (you can only delete both things at once).
```

Like unique pointer, shared pointer's constructor may take in a custom deleter. In addition, it may also take in a custom allocator. The custom allocator has nothing to do with the underlying pointer -- it gets used for allocating and deallocating the control block.

```c++
auto object_deleter = [](int* x) {
    std::cout << "Deleting an int at " << x;
    delete x;
};
auto control_block_allocator { std::allocator<void>{}} ;
std::shared_ptr<int> ptr{ new int {5}, object_deleter, control_block_allocator };
```

```{note}
There are no template parameters for the deleter or allocator. You just pass them in as the last two constructor arguments and it should just work. The book is saying that they were left out for "complicated reason".
```

It isn't possible to use a custom allocator with `std::make_shared()`. It forces the use of `new` / `new[]` and `delete` / `delete[]` for single combined allocation of the control block and the dynamic object. To perform a single combined allocation and use a custom allocator for that allocation, you need to use `std::allocate_shared()` instead.

```c++
auto my_allocator { std::allocator<void>{}} ;
std::shared_ptr<int> ptr{ std::allocate_shared<int>(my_allocator, 5) };
```

```{note}
There is no template parameter for the allocator. You just pass it in as the first constructor argument and it should just work.

There is no custom deleter with `std::allocate_shared` because the deletion happens via the allocator. Both the control block and the dynamic object are being allocated and deallocated together.
```

In certain cases, a class may want to return shared pointers to itself (a shared pointer to its `this` pointer). A class can't ...

 * maintain a member variable that's a shared pointer to itself: That shared pointer's reference count would never reach 0 because the object itself will always be holding onto a copy of that shared pointer.
 * provide a function to generate shared pointers to itself: There will be multiple shared pointers leading to the same object, meaning that if one of those shared pointers were to reach a reference count of 0 it would delete the object while the other shared pointers would still think the object still exists (dangling pointer).

To work around these problems, C++ provides the `std::enable_shared_from_this` base class that you can inherit from.

```c++
struct MyClass : public std::enable_shared_from_this<MyClass> {
    shared_ptr<MyClass> getSharedPointer() {
        return shared_from_this(); // special function provided by the base class
    }
}
```

```{note}
See [here](https://stackoverflow.com/a/712307) for more information.
```

### Weak Pointer

`{bm} /(Library Functions\/Smart Pointers\/Weak Pointer)_TOPIC/`

```{prereq}
Library Functions/Smart Pointers/Shared Pointer_TOPIC
```

A weak pointer is essentially a shared pointer that doesn't increment or decrement the reference count. At any moment, it can generate an actual shared pointer via its `lock()` method, thereby increasing the reference count.

```c++
std::shared_ptr<int> sp1 { new int {5} }; // ref count = 1
std::weak_ptr<int> wp{ sp };              // ref count = 1
std::shared_ptr<int> sp2 { wp.lock() };   // ref count = 2
std::shared_ptr<int> sp3 { wp.lock() };   // ref count = 3
```

If the shared pointer reference count has already reached 0 when `lock()` is invoked, the returned shared pointer will be empty.

```c++
std::weak_ptr<int> wp {};  // unset weak pointer
{
    std::shared_ptr<int> sp { new int {5} };  // create a new shared pointer
    wp = sp;                                  // assign the shared pointer to the weak pointer
} // scope ends, shared pointer destroyed (reference count drops from 1 to 0, meaning object is deleted)
std::shared_ptr<int> sp { wp.lock() };
bool isEmpty = (sp == std::nullptr); // isEmpty will be true
```

```{note}
There's a version of weak pointer in Boost and one in the C++ standard library. The Boost version is legacy. Each weak pointer version is tied to the shared pointer from its library. For example, if you're using the weak pointer in Boost, you need to use it with the shared pointer from Boost.
```

The typical use-cases for weak pointers are ...

 * caching (e.g. only calculate data if weak pointer is unset).
 * cyclical references (e.g. data structures such as cyclical graphs).

For cyclical references point above, what it means is that shared pointers forming a cycle will never reach a reference count of 0.

```{svgbob}
C <------- B 
|          ^
|          |
'---> A ---'
```

In the example above...

 * A has a shared pointer to C (reference count = 1)
 * C has a shared pointer to B (reference count = 1)
 * B has a shared pointer to A (reference count = 1)

Nothing else holds these shared pointers. They all reference each other, meaning that none of the shared pointer reference counts will never reach 0 (memory leak).

### Intrusive Pointer

`{bm} /(Library Functions\/Smart Pointers\/Intrusive Pointer)_TOPIC/`

```{prereq}
Library Functions/Smart Pointers/Shared Pointer_TOPIC
```

An intrusive pointer invokes the free function `intrusive_ptr_add_ref()` on any allocation and `intrusive_ptr_release()` on any deallocation. Both functions take in a single argument: a pointer of the type being allocated / deallocated.

```c++
size_t cnt {};

void intrusive_ptr_add_ref(int* ptr) {
    cnt++;
}

void intrusive_ptr_release(int* ptr) {
    cnt--;
}

boost::intrusive_ptr<int> a { new int{5} };     // after this, cnt will be 1
{
    boost::intrusive_ptr<int> b { new int{6} }; // after this, cnt will be 2
    boost::intrusive_ptr<int> c { a };          // after this, cnt will be 3
} // at the end of this scope, cnt will be 1 again
```

Where as a shared pointer keeps a count of how many copies of itself are live (reference count), an intrusive pointer is typically used for keeping count of how many of some specific _pointer type_ are live. In the example above it's tracking `int`, but you can track more types by simply overloading `intrusive_ptr_add_ref()` and `intrusive_ptr_release()`.

```{note}
The book mentions that this is useful in cases where the OS or framework requires some cleanup operation once the last instance of some type goes away (e.g. the old school Windows component object model).
```

## Utility Wrappers

`{bm} /(Library Functions\/Utility Wrappers)_TOPIC/`

There are utility classes that wrap one or more other objects, such as optionals or tuples. They either provide some type of extra functionality or provide abstractions that make code easier to handle and reason about.

The subsections below document some common wrappers classes and their usages.

### Optional

`{bm} /(Library Functions\/Utility Wrappers\/Optional)_TOPIC/`

An optional class is a wrapper that either holds on to an object or is empty (similar to Java or Python's optional class).

```c++
std::optional<int> take(int x) {
    if (x < 0) {
        return std::nullopt;  // nullopt = empty optional
    }
    return std::optional<int> { x * x };
}
```

As shown in the example above, the typical usecase for optional is to have a function return an empty optional on failure.

```{note}
Other strategies for reporting failure are throwing an error and returning an error code along with the object.
```

In addition to the optional provided by the C++ standard library, Boost provides its own version of optional `boost::optional` as well as provides an optional-like boolean type called tribool: `boost::logic::tribool`. A tribool has a third state in addition to true and false, called indeterminate. Boolean operations where one of the operands is a boolean value and the other is indeterminate will always result in false (tribools convert to booleans via implicit conversion).

```{seealso}
Core Language/Classes/Conversion Overloading_TOPIC (refresher -- tribool class implements implicit conversion semantics)
```

```c++
boost::logic::tribool tb { boost::logic::indeterminate };
bool x {tb == true};  // false
bool y {tb == false}; // false
bool z {!tb};         // false
```

The typical usecase for tribool is for operations that take a long time to complete. A tribool may be set as indeterminate while the operation is running, then be set to true (success) or false (failure) once the operation completes.

### Tuple

`{bm} /(Library Functions\/Utility Wrappers\/Tuple)_TOPIC/`

A tuple class is a templated class that holds on to an arbitrary number of elements of arbitrary types. The number of elements and types of elements must be known at compile-time, and any code accessing those elements must know which element it's accessing at compile-time.

```c++
std::tuple<int, long, MyClass> my_tuple{ 1, 500L, MyClass{} };
auto& x { std::get<0>(my_tuple) };
auto& y { std::get<1>(my_tuple) };
auto& z { std::get<2>(my_tuple) };
// OR you can use structured binding
auto& [x, y, z] = my_tuple;
```

Note how the elements are being accessed using `std::get()`, which requires the index being accessed passed in as a template parameter. Elements your code accesses _must be known at compile-time_, meaning you can't evaluate some expression at run-time to determine which index to access like you can with tuples in other high-level languages (e.g. Python).

If all the types in for a tuple are different, the type itself can be passed into `std::get()`.

```c++
std::tuple<int, long, MyClass> my_tuple{ 1, 500L, MyClass{} };
auto& x { std::get<int>(my_tuple) };
auto& y { std::get<long>(my_tuple) };
auto& z { std::get<MyClass>(my_tuple) };
```

```{note}
I guess the way to think about tuples is that they're short-hand for PODs. Declaring a tuple is like creating a custom POD where each element of the tuple is a member variable of the POD.
```

Pairs are special cases of tuples where they're restricted to exactly two elements. Accessing the elements in a pair is done through the `first` and `second` member variables.

```c++
std::pair<int, long> my_pair{ 1, 500L };
auto& x {my_pair->first};
auto& y {my_pair->second};
// OR you can use structured binding
auto& [x, y] = inimitable_duo;
```

Boost also provides a version of pair, `boost::compressed_pair`, except that it's slightly more efficient when either of the template parameters points to an empty class.

```c++
struct EmptyClass {};

std::pair<int, EmptyClass> p {5, EmptyClass{} };
boost::compressed_pair<int, EmptyClass> cp {5, EmptyClass{} };  // this one consumes less memory
```

```{note}
There's a helper function called `std::make_tuple()` / `std::make_pair()` which makes tuples / pairs but has problems when the type is a reference. Be aware of that if you decide to use it. See [here](https://stackoverflow.com/a/7867662).
```

### Any

`{bm} /(Library Functions\/Utility Wrappers\/Any)_TOPIC/`

An any class is a wrapper that can hold on to an object of unknown type (a type that isn't known at compile-time).

```c++
std::any wrapper {};
wrapper.emplace<MyClass> { arg1, arg2 };
auto v1 = std::any_cast<MyClass>(wrapper); // ok
auto v2 = std::any_cast<BadType>(wrapper); // should throws std::bad_any_cast
```

To place an object into the wrapper, use `emplace()`. This _creates_ a new object and places it into the wrapper, destroying the object previously held. The type of the object is passed in as a template parameter argument while the function arguments are used to initialize that object (e.g. passed directly to constructor). 

Accessing the object within the wrapper is done via `std::any_cast()`. The function argument is the wrapper itself and the template parameter argument is the type of  object _you think_ is being held. If the object is of a different type, the function throws `std::bad_any_cast` instead of returning the object.

```{note}
The closest Java analog I could think of is the base class hierarchy where all Java objects have to derive from `java.lang.Object`. You can accept a type of `Java.lang.Object` and cast it at runtime to the correct type (or one of its ancestors). The C++ any class provides similar functionality to that.
```

Boost also provides a version of this wrapper, `boost::any`.

### Variant

`{bm} /(Library Functions\/Utility Wrappers\/Variant)_TOPIC/`

```{prereq}
Library Functions/Utility Wrappers/Any
Library Functions/Utility Wrappers/Tuple
```

A variant class is a type-restricted form of the `std::any`. Where as with the `std::any` you can hold on to an object of any type, with `std::variant` you can hold on to an object of one of several predefined types.

```c++
std::variant<int, float, MyClass> wrapper {};  // may hold on to either int, float, or MyClass
wrapper.emplace<MyClass> { arg1, arg2 };
auto v1 = std::get<MyClass>(wrapper);     // ok
auto v2 = std::get_if<MyClass>(wrapper);  // ok
auto v3 = std::get_if<int>(wrapper);      // returns nullptr
auto v4 = std::get<int>(wrapper);         // throws std::bad_variant_exception
auto which_type = wrapper.index();    // returns 2
```

To determine which of the allowed types is currently held, use `index()`.

To access data, use `std::get()` where the template parameter argument is the type you're interested in (similar to how data access is done in `std::tuple`). If the variant isn't holding an object of the type trying to be extracted, `std::get()` will throw `std::bad_variant_exception`. To avoid an exception, use `std::get_if()` -- it will return `nullptr` rather than throw an exception.

Unlike `std::any`, `std::variant` cannot be left unset (it must hold on to an object). Initially, it creates and holds on to an object of the first type in its allowed types list. That means the first type in its allowed types list must be constructible with empty initializer arguments (e.g. default constructor). In the example above, the first allowed type is `int`, meaning that the variant starts off by holding on to an `int` created using an empty initializer (will have value of 0).

The easiest way to work around this problem is to set the first type to `std::monostate`. This allows your variant to be unset. Trying to call `std::get()` on an unset variant throws `std::bad_variant_access`.

```c++
std::variant<std::monostate, int, float, MyClass> wrapper {};  // may hold on to nothing, int, float, or MyClass
auto which_type = wrapper.index();     // returns 0
auto v1 = std::get<MyClass>(wrapper);  // throws std::bad_variant_access
```

If you have a set of single parameter functions with the same name (function overload), where those parameters contains all the types in a variant's allowed types list, you can use `std::visit()` to automatically pull out the object contained in the variant and call the appropriate function overload with that object as the argument.

```c++
std::variant<int, float> wrapper {};  // may hold on to either int, float
// call into a generic lambda / functor
auto res1 = std::visit([](auto& x) { return 5 * x; }, wrapper);
// call into an overloaded free function (via a generic lambda / functor)
auto res2 = std::visit([](auto &x) { return my_function(x); }, wrapper);
// call into a specific lambda / functor based on type currently being held
std::visit(
    overloaded {
        [](int& x) { std::cout << "int" << x; },
        [](float& x) { std::cout << "float" << x; },
        [](auto &) { std::cout << "OTHER"; }
    },
    wrapper
);
```

Boost also provides a version of this wrapper, `boost::variant`.

```{seealso}
Core Language/Unions_TOPIC (variants are similar to unions but type-safe)
```

### Function

A function class is a standardized wrapper for function-like objects.

```c++
void print_num(int i)
{
    std::cout << i << '\n';
}
 
struct PrintNum {
    void operator()(int i) const
    {
        std::cout << i << '\n';
    }
};


std::function<void(int)> f1 { print_num };
std::function<void(int)> f2 { PrintNum };
```

```{seealso}
Core Language/Variables/Pointers/Function Pointer_TOPIC (refresher)
Core Language/Classes/Functors_TOPIC (refresher)
Core Language/Lambdas_TOPIC (refresher)
```

The typical use-case for `std::function` is to provide a function with a unified way to accept all function-like objects (e.g. functors and function pointers) as a parameter. The alternative would be to explicitly provide an overload for each function-like object type.

```c++
void call_func_with_42(std::function<void(int)> func) {
    func(42);
}
```

### Reference Wrapper

`{bm} /(Library Functions\/Utility Wrappers\/Reference Wrapper)_TOPIC/`

```{prereq}
Library Functions/Containers
```

```{seealso}
Core Language/Variables/Rvalue References_TOPIC (refresher)
```

A reference wrapper is a wrapper that holds a reference to an object. This is important because, in C++, you can't have a reference to a reference like you can have a pointer to a pointer. References, from a usage perspective, are treated as if they're the direct object themselves.

```c++
int ** x { ... };                                             // OK:  x is a pointer to a pointer to a n integer
int && y { ... };                                             // BAD: y is an rvalue reference, NOT a reference to a reference
std::reference_wrapper<std::reference_wrapper<int>> z{ ... }; // OK:  z is a reference wrapper to a reference wrapper
```

To create a `std::reference_wrapper`, use `std::ref()`. To access the value referenced to by a reference wrapper, use `get()`.

```c++
const int a { 5 };
const std::reference_wrapper<const int> aWrapped{ std::ref(a) };
const int b { aWrapped.get() };
const int c { aWrapped }; // This can also work because std::reference_wrapper provides implicit conversion
```

`std::reference_wrapper`s are especially useful for containers. Normally, containers won't allow you to store references. The only options are to store either full objects or pointers to objects.

```c++
std::vector<int> vec2 {};   // OK: stores ints
std::vector<int *> vec2 {}; // OK: stores int pointers
std::vector<int &> vec3 {}; // BAD: not allowed
```

While storing pointers seems like a good alternative to storing references, certain container types may not work as expected with pointers. For example, unordered associative containers like `std::unordered_set` will use the default pointer template specializations for `std::hash` and `std::equal_to`, meaning that the container determines equality by inspecting the pointer rather than the object it points to.

```c++
int a {0}; int b {1}; int c {1}; int d {1}; int e {1};

// The following outputs 1 0
std::unordered_set<int> vec2 { a, b, c, d, e };
for (auto e : vec2) {
    std::cout << e << ' ';
}
std::cout << std::endl;

// The following outputs 1 1 1 1 0
std::unordered_set<int *> vec1 { &a, &b, &c, &d, &e };
for (auto e : vec1) {
    std::cout << *e << ' ';
}
std::cout << std::endl;
```

Using `std::reference_wrapper` allows for the template specializations of the object itself to be used. The only caveat is that the template specializations need to be declared directly in the container type.

```c++
// The following outputs 1 0
std::unordered_set<
    std::reference_wrapper<int>, // type to store
    std::hash<int>,              // std::hash specialization to use
    std::equal_to<int>           // std::equal_to specialization to use
> vec3 { a, b, c };
for (auto e : vec3) {
    std::cout << e.get() << ' ';
}
std::cout << std::endl;

// HOW CAN THE ABOVE WORK if the stored type is std::reference_wrapper<int> but hash/equal_to accept only int? Recall that
// std::reference_wrapper<int> can implicitly convert to its underlying type. For example, the following is equivalent ...

int & x { (*vec3.begin()).get() };
int & y {  *vec3.begin() };  // references same object as X

// As such, when std::hash<int> / std::equal_to<int> to get invoked, they get passed in a std::reference_wrapper<int> which
// implicitly converts to int.
```

Common pattern for different container types:

 * `std::vector<std::reference_type<T>>`
 * `std::unordered_set<std::reference_type<K>, std::hash<K>, std::equal_to<K>>`
 * `std::unordered_map<std::reference_type<K>, V, std::hash<K>, std::equal_to<K>>`
 * `std::ordered_set<std::reference_type<K>, std::less_than<K>>`
 * `std::ordered_map<std::reference_type<K>, V, std::less_than<K>>`

````{note}
Another option is to go ahead and use pointers, but rather than specifying `std::hash<K>` / `std::equal_to<K>` / `std::less_than<K>` in the template parameters, create custom functor that access data on the object being pointed to.

```c++
struct custom_less_functo {
    constexpr bool operator()(const MyObject* & lhs, const MyObject* & rhs) const {
        return lhs->val1 < rhs->val1 || lhs->val2 < rhs->val2;
    }
}
std::ordered_set<MyObject*, custom_less_functor_for> s { ... }
```
````

## Containers

`{bm} /(Library Functions\/Containers)_TOPIC/`

```{prereq}
Library Functions/Allocators_TOPIC
```

C++'s equivalent of Java collections are commonly referred to as containers. C++ containers come in 3 major types:

 * Sequence containers - Objects organized in a sequence, where they're (at least) accessible from one end to the other.
   
   | C++ container       | nearest Java equivalent                                      |
   |---------------------|--------------------------------------------------------------|
   | `std::array`        | standard Java array                                          |
   | `std::vector`       | `ArrayList`                                                  |
   | `std::deque`        | `Deque` (an interface -- the C++ class is an implementation) |
   | `std::list`         | `LinkedList` (doubly-linked list)                            |
   | `std::forward_list` | `LinkedList` (singly-linked list)                            |
 
 * Associative containers - Objects organized by key and potentially a value (keys sorted, requiring a comparison function).
 
   | C++ container   | nearest Java equivalent                |
   |-----------------|----------------------------------------|
   | `std::set`      | `TreeSet`                              |
   | `std::map`      | `TreeMap`                              |
   | `std::multiset` | `TreeBag` (Apache Commons Collections) |
   | `std::multimap` | `TreeMultimap` (Guava)                 |

 * Unordered associative containers - Objects organized by key and potentially a value (keys unsorted).

   | C++ container             | nearest Java equivalent                               |
   |---------------------------|-------------------------------------------------------|
   | `std::unordered_set`      | `HashSet`                                             |
   | `std::unordered_map`      | `HashMap`                                             |
   | `std::unordered_multiset` | `HashBag` (Apache Commons Collections)                |
   | `std::unordered_multimap` | `ArrayListValuedHashMap` (Apache Commons Collections) |

```{seealso}
Core Language/Control Flow/For Loop_TOPIC (for-each loop refresher)
Core Language/Iterators_TOPIC (refresher)
```

Containers support iterators via their `begin()` and `end()` functions. Looping over a container using a for-each loop calls those functions, but the order in which containers are iterated over depends on the container. For example ...

 * `std::vector` maintains insertion order.
 * `std::map` iterates in sort order.
 * `std::unordered_map` iterators in some unknown order (unordered).

```c++
std::vector<MyObject> container { /* items here */ };
for (MyObject &obj : container) {
    // do something with value here
}
```

Most (not all) containers allow using user-supplied allocators via template parameter argument.

```c++
std::vector<MyObject, CustomAllocator> container { };
```

The subsections below detail some of the containers mentioned above. Other major libraries provide more specialized containers (boost, abseil, etc..), but those containers aren't detailed here.

### Sequential

`{bm} /(Library Functions\/Containers\/Sequential)_TOPIC/`

Sequential containers organize objects as a sequence, where they're (at least) accessible from one end to the other. The container may or may not be dynamically sized (grow vs shrink) and underlying data structures used by sequential containers aren't the same.

The subsections below detail the various sequential containers that are provided by the C++ standard library.

#### Array

`{bm} /(Library Functions\/Containers\/Sequential\/Array)_TOPIC/`

`std::array` is a container that's more-or-less a wrapper around a normal C++ array. Like normal C++ arrays, it ...

 * is fixed-size, meaning it can't automatically grow or shrink,
 * allows reads and writes to random positions using its subscript operator.

One caveat to this container is that it _does not_ allocate a dynamic object array. That means, just like normal C++ arrays created on the stack, the number of elements must be known at compile-time.

```c++
int my_arr1[55] {};              // int array of size 55
std::array<int, 55> my_arr2 {};  // std::array of ints, with size 55

for (auto &obj : my_arr2) {
    // do something with value here
}
```

`std::array` provides copy semantics and move semantics. However, because the underlying array is a local object, both moving and copying end up recreating that underlying array. This means that copying and moving may potentially be expensive.

```c++
std::array<int, 55> my_arr3 { std::move(my_arr2) };   // move my_arr2 into my_arr3
```

To read elements, use the subscript operator ([]) or `at()`. The main difference between the two is that the latter has bounds checking. Alternatively, ...

 * `front()` may be used as shorthand to get the first element.
 * `back()` may be used as shorthand to get the last element.
 * `std::get()` may be used to read a random element so long as the index being read is known at compile-time (does bounds checking at compile-time).

```c++
int w { my_arr2[20] };
int x { my_arr2.at(20) };
int y { my_arr2.at(1000) };  // throws std::out_of_range
int z { std::get<20>(my_arr2) };
int a { my_arr2.front() };  // WARNING: undefined behaviour of len is 0
int b { my_arr2.back() };  // WARNING: undefined behaviour of len is 0
```

```{seealso}
Library Functions/Utility Wrappers/Tuple_TOPIC (refresher on `std::get()`)
```

To replace elements, use any of the same functions used for reading elements except `std::get()`. They return a reference, which means assigning something to them will assign into the container.

```c++
my_arr2[20] = 123;
my_arr2.at(20) = 123;
my_arr2.front() = 123;
my_arr2.back() = 123;

auto & ref = my_arr(20);
ref = 123;
```

To get the size, use `size()`.

```c++
int len { my_arr2.size() };
```

```{note}
`size()` and `max_size()` are equivalent for `std::array`, but not for other containers that can grow / shrink.
```

To gain access to the underlying array being wrapped, use `data()`.

```c++
int * backing_arr = my_arr2.data();
// NOTE: each below are equivalent to the above, but the one above should be preferred
//       because the ones below will have undefined behaviour if array length is 0.
int * backing_arr = &my_arr2[0];
int * backing_arr = &my_arr2.at(0);
int * backing_arr = &my_arr2.front();
```

To iterate over the elements, use `being()` and `end()`.

```c++
// RECALL: for-each loop will implicitly call begin() and end()
for (auto &obj : my_arr2) {
    // do something with value here
}
```

```{note}
There's also ..

 * `cbegin()` / `cend()` which returns a constant iterator (can't change values?).
 * `rbegin()` / `rend()` which returns an iterator that goes in reverse order.
 * `crbegin()` / `crend()` which is a mixture of the above two.
```

#### Vector

`{bm} /(Library Functions\/Containers\/Sequential\/Vector)_TOPIC/`

```{prereq}
Library Functions/Containers/Sequential/Array_TOPIC
Library Functions/Allocators_TOPIC
```

```{note}
WARNING: The book is saying that there is no hard requirement for a container to return copies vs references. Most of the time a container returns references, but in special cases it may return a copy of some object. For example, `vector<bool>` has a template specialization that returns a proxy object rather than a direct reference (`std::vector<bool>::reference`).
```

`std::vector` is a container that holds on to its elements sequentially and contiguously in memory (array), but it can dynamically size itself (e.g. expand the internal array if not enough room is available to add a new element). It has most of the same functions as `std::array`, in addition to some others.

To create an `std::vector` primed with a sequence of values known as compile-time, use typical braced initialization.

```c++
std::vector<int> my_vec1 { 5, 5, 5, 5, 5, 5, 5, 5 };
```

To create an `std::vector` without priming it directly to a sequence of values, you can't use braced initialization or brace-plus-equals initialization. You must use parenthesis.

```c++
std::vector<int> my_vec2 (8, 5); // equivalent to initializing to above (8 copies of 5)
std::vector<int> my_vec3 (c)  // copy another container
std::vector<int> my_vec4 (c.begin(), c.begin() + 10)  // copy first 10 elems from another container
```

```{note}
The rules for initialization are complex. In this case, there's a constructor that takes in an `std::initializer_list`. That means braced initialization / brace-plus-equals initialization will in most cases call that constructor, where that initializer list gets populated with whatever is in the braces. To avoid that, the easiest thing you can do is fall back to using the legacy way of calling constructors (parenthesis).
```

`std::vector` provides copy semantics and move semantics. Because elements are dynamic objects, moving one `std::vector` into another is fast because it's simply passing off a pointer / reference. Copying can potentially be expensive.

```c++
std::vector<int> my_vec5 { std::move(my_vec1) };   // move my_vec1 into my_vec5
```

Similarly, because `std::vector`'s elements are created as dynamic objects, you have the option of supplying a custom allocator.

```c++
CustomAllocator allocator {};
std::vector<int, CustomAllocator> my_vec6 (allocator);
```

To read elements, the same read functions for `std::array` are available here.

```c++
int w { my_vec1[5] };
int x { my_vec1.at(5) };
int y { my_vec1.at(1000) };  // throws std::out_of_range
int a { my_vec1.front() };  // WARNING: undefined behaviour of len is 0
int b { my_vec1.back() };  // WARNING: undefined behaviour of len is 0
```

```{note}
Does `std::get()` work here as well? I don't think so because this is a dynamic array.
```

To replace elements, the same write functions for `std::array` are available here. Those functions are the same functions used for reading elements. They return a reference, which means assigning something to them will assign into the container.

```c++
my_vec1[20] = 123;
my_vec1.at(20) = 123;
my_vec1.front() = 123;
my_vec1.back() = 123;
```

To add elements, the following functions are available:

 * `insert()` will insert an element just behind some iterator position (object copied / moved).
 * `emplace()` will insert an element just behind some iterator _by creating it directly_ (no copying / moving).
 * `push_back()` will append an element (copy semantics)
 * `emplace_back()` will append an element _by creating it directly_ (no copying / moving).

```c++
auto it1 = my_vec1.begin() + 3;
my_vec1.insert(it1, 77); // WARNING: it1 invalid after this call
auto it2 = my_vec1.begin() + 3;
my_vec1.emplace(it2, 77); // WARNING: it2 invalid after this call
my_vec1.push_back(123);
my_vec1.emplace_back(123);
```

```{note}
`emplace()` / `emplace_back()` don't copy or move because you pass in initialization arguments directly into the functions. Internally, they use template parameter packs to forward arguments for object creation (e.g. constructor arguments, initializer list, etc..).
```

```{seealso}
Library Functions/Utility Wrappers/Any_TOPIC (also has an `emplace()` function)
Library Functions/Utility Wrappers/Variant_TOPIC (also has an `emplace()` function)
```

To delete either a single element or a range of elements, use `erase()` and pass into it either an iterator at some position or an iterator range.

```c++
auto it1 {my_vec1.begin() + 3};
my_vec1.erase(it1); // WARNING: it1 invalid after this call

auto it2 {my_vec1.begin()};
auto it3 {my_vec1.begin() + 10};
my_vec1.erase(it2, it3); // WARNING: it2/it3 invalid after this call
```

To delete the last element, use `pop_back()`. It's similar to `back()` (returns element) but it removes the element as well.

```c++
int c { my_vec1.pop_back() }; // REMOVES the last 
```

To delete all elements, use `clear()`.

```c++
my_vec1.clear();
```

To delete all elements and re-assign to a list of new elements, use `assign()`.

```c++
my_vec1.assign(5, 10); // 5 copies of 10
my_vec1.assign({5,5,5,5,5}); // 5 copies of 10
my_vec1.assign(c.begin(), c.begin() + 5); // starting 5 elements of another container
```

To get the number of elements, the same functions for `std::array` are available here.

```c++
auto is_empty1 { my_vec1.size() == 0 };
auto is_empty2 { my_vec1.empty() };
```

Internally, `std::vector` grows in chunks. For example, if the underlying array has a size of 5 and all of those 5 elements are occupied, when you add in a 6th element the underlying array resizes to have a capacity larger than 6 (e.g. 10). This way, you can continue adding in a few more elements without another resize happening right away (more efficient).

To get the current capacity, use `capacity()`.

```c++
float usage { my_vec1.size() / my_vec2.capacity() };
```

If you ...

 * know the capacity you want ahead of time, use `reserve()`.
 * want to shrink the capacity to match the number of elements stored, use `shrink_to_fit()`.

```c++
my_vec1.reserve(1000);
my_vec1.shrink_to_fit();
```

Similar to `std::array`, you can access the underlying array for an `std::vector`. However, the returned array may become invalid as soon as you start performing operations on the owning `std::vector` (e.g. it may get recreated due to shrinkage/growth).

To gain access to the underlying array being wrapped, use `data()`.

```c++
int * backing_arr = my_vec1.data();
// NOTE: each below are equivalent to the above, but the one above should be preferred
//       because the ones below will have undefined behaviour if array length is 0.
int * backing_arr = &my_vec1[0];
int * backing_arr = &my_vec1.at(0);
int * backing_arr = &my_vec1.front();
```

To iterate over the elements, use `being()` and `end()`.

```c++
// RECALL: for-each loop will implicitly call begin() and end()
for (auto &obj : my_vec1) {
    // do something with value here
}
```

```{note}
There's also ..

 * `cbegin()` / `cend()` which returns a constant iterator (can't change values?).
 * `rbegin()` / `rend()` which returns an iterator that goes in reverse order.
 * `crbegin()` / `crend()` which is a mixture of the above two.
```

#### Deque

`{bm} /(Library Functions\/Containers\/Sequential\/Deque)_TOPIC/`

```{prereq}
Library Functions/Containers/Sequential/Vector_TOPIC
```

`std::deque` is a container that holds on to its elements sequentially but not contiguously in memory (not an array). It can dynamically size itself (e.g. expand the internal array if not enough room is available to add a new element) just like `std::vector` and it supports most of the same function as `std::vector`. The most prominent functions it _doesn't_ support:

 * `data()` because there is no underlying array with this container.
 * `capacity()`.
 * `reserve()`.

Because of the internal data structure used by this container, the added functions above are efficient.

To create an `std::deque` primed with a sequence of values known as compile-time, use typical braced initialization.

```c++
std::deque<int> d1 { 5, 5, 5, 5, 5, 5, 5, 5 };
```

To create an `std::deque` without priming it directly to a sequence of values, you can't use braced initialization or brace-plus-equals initialization. You must use parenthesis.

```c++
std::deque<int> d2 (8, 5); // equivalent to initializing to above (8 copies of 5)
std::deque<int> d3 (c)  // copy another container
std::deque<int> d4 (c.begin(), c.begin() + 10)  // copy first 10 elems from another container
```

`std::deque` provides copy semantics and move semantics. Because elements are dynamic objects, moving one `std::deque` into another is fast because it's simply passing off a pointer / reference. Copying can potentially be expensive.

```c++
std::deque<int> d5 { std::move(d1) }; // move d1 into d5
```

Similarly, because `std::deque`'s elements are created as dynamic objects, you have the option of supplying a custom allocator.

```c++
CustomAllocator allocator {};
std::deque<int, CustomAllocator> d6 (allocator);
```

To read elements, the same read functions for `std::vector` are available here.

```c++
int w { d1[5] };
int x { d1.at(5) };
int y { d1.at(1000) };  // throws std::out_of_range
int a { d1.front() };  // WARNING: undefined behaviour of len is 0
int b { d1.back() };  // WARNING: undefined behaviour of len is 0
```

To replace elements, the same write functions for `std::vector` are available here. Those functions are the same functions used for reading elements. They return a reference, which means assigning something to them will assign into the container.

```c++
d1[20] = 123;
d1.at(20) = 123;
d1.front() = 123;
d1.back() = 123;
```

To add elements, the same add functions for `std::vector` are available here in addition to...

 * `emplace_front()` - similar to `emplace_back()` but adds to the front.
 * `push_front()` - similar to `push_back()` but adds to the front.

```c++
auto it1 = d1.begin() + 3;
d1.insert(it1, 77); // WARNING: it1 invalid after this call
auto it2 = d1.begin() + 3;
d1.emplace(it2, 77); // WARNING: it2 invalid after this call
d1.push_back(123);
d1.push_front(123); // similar to push_back, but adds to front
d1.emplace_back(123);
d1.emplace_front(123); // similar to emplace_back, but adds to front
```

```{note}
Recall that "emplace" functions don't copy or move. They're templated functions. You pass in object initialization arguments directly into the functions and it uses a template parameter pack to forward those arguments for object creation directly within the function (e.g. constructor arguments, initializer list, etc..).
```

To delete elements, the same delete functions for `std::vector` are available here in addition to ...

 * `pop_front()` - similar to  `pop_back()` but removes from the front.

```c++
// DELETE at ifx
auto it1 {d1.begin() + 3};
d1.erase(it1); // WARNING: it1 invalid after this call
// DELETE between idx range
auto it2 {d1.begin()};
auto it3 {d1.begin() + 10};
d1.erase(it2, it3); // WARNING: it2/it3 invalid after this call
// DELETE front or back
int c { d1.pop_back() };
int d { d1.pop_front() }; // similar to pop_back, but removed from the FRONT
// DELETE all
d1.clear();
// DELETE all and RE-ASSIGN
d1.assign(5, 10); // 5 copies of 10
d1.assign({5,5,5,5,5}); // 5 copies of 10
d1.assign(c.begin(), c.begin() + 5); // starting 5 elements of another container
```

To get the number of elements, the same functions for `std::vector` are available here.

```c++
auto is_empty1 { d1.size() == 0 };
auto is_empty2 { d1.empty() };
```

To release unused memory that's been reserved by the container, use `shrink_to_fit()`. The `capacity()` and `reserve()` functions found in `std::vector` are not present in this container.


To iterate over the elements, use `being()` and `end()`.

```c++
// RECALL: for-each loop will implicitly call begin() and end()
for (auto &obj : d1) {
    // do something with value here
}
```

```{note}
There's also ..

 * `cbegin()` / `cend()` which returns a constant iterator (can't change values?).
 * `rbegin()` / `rend()` which returns an iterator that goes in reverse order.
 * `crbegin()` / `crend()` which is a mixture of the above two.
```

#### List

`{bm} /(Library Functions\/Containers\/Sequential\/List)_TOPIC/`

```{prereq}
Library Functions/Containers/Sequential/Deque_TOPIC
```

`std::list` is a container that holds on to its elements sequentially. It's implemented as a doubly-linked list, meaning its size is dynamic but it isn't stored contiguously in memory (not an array).

`std::list` supports a similar set of functions as `std::deque` except for the fact that random element access isn't allowed (the functions for it don't exist -- random access is inefficient with linked lists). You can only access elements by walking either forward or backward. In addition, it provides several built-in helper functions such as sorting and de-duplication.

```{note}
List of helper functions is documented near the end.
```

```{note}
There's also `std::forward_list` which is a singly-linked list. It's functionality is very similar to this class, but since it only supports walking forward, some of the functions listed here are missing.
```

To create a `std::list` primed with a sequence of values known as compile-time, use typical braced initialization.

```c++
std::list<int> l1 { 5, 5, 5, 5, 5, 5, 5, 5 };
```

To create a `std::list` without priming it directly to a sequence of values, you can't use braced initialization or brace-plus-equals initialization. You must use parenthesis.

```c++
std::list<int> l2 (8, 5); // equivalent to initializing to above (8 copies of 5)
std::list<int> l3 (c)  // copy another container
std::list<int> l4 (c.begin(), c.begin() + 10)  // copy first 10 elems from another container
```

`std::list` provides copy semantics and move semantics. Because elements are dynamic objects, moving one `std::list` into another is fast because it's simply passing off a pointer / reference. Copying can potentially be expensive.

```c++
std::list<int> l5 { std::move(l1) }; // move l1 into l5
```

Similarly, because `std::list`'s elements are created as dynamic objects, you have the option of supplying a custom allocator.

```c++
CustomAllocator allocator {};
std::list<int, CustomAllocator> l6 (allocator);
```

To read elements, use the iterator functions `begin()` and / or `end()` to walk the sequence. Alternatively, the `front()` and `back()` functions give direct access to the first and last elements respectively.

```c++
// WARNING: undefined behaviour of len is < 3
auto it = l1.begin();
int a { *it };
it++;
int b { *it };
it++;
int c { *it };

int d { l1.front() }; // WARNING: undefined behaviour of len is 0
int e { l1.back() };  // WARNING: undefined behaviour of len is 0
```

To replace elements, the same iterator functions `begin()` and / or `end()` need to be used to walk the sequence to the point of replacement.

```c++
// WARNING: undefined behaviour of len is < 3
auto it = l1.begin() + 2;
*it = 55;
```

To add elements, the same add functions for `std::deque` are available here.

```c++
auto it1 = l1.begin() + 3;
l1.insert(it1, 77);
auto it2 = l1.begin() + 3;
l1.emplace(it2, 77);
l1.push_back(123);
l1.push_front(123);
l1.emplace_back(123);
l1.emplace_front(123);
```

```{note}
I'm getting conflicting information about if an iterator is invalid after a write. Right now I'm leaning towards NOT invalid.
```

```{note}
Recall that "emplace" functions don't copy or move. They're templated functions. You pass in object initialization arguments directly into the functions and it uses a template parameter pack to forward those arguments for object creation directly within the function (e.g. constructor arguments, initializer list, etc..).
```

To delete elements, the same delete functions for `std::deque` are available here.

```c++
// DELETE at idx
auto it1 {l1.begin() + 3};
d1.erase(it1); // WARNING: it1 invalid after this call
// DELETE between idx range
auto it2 {l1.begin()};
auto it3 {l1.begin() + 10};
l1.erase(it2, it3); // WARNING: it2/it3 invalid after this call
// DELETE front or back
int c { l1.pop_back() };
int d { l1.pop_front() }; // similar to pop_back, but removed from the FRONT
// DELETE all
l1.clear();
// DELETE all and RE-ASSIGN
l1.assign(5, 10); // 5 copies of 10
l1.assign({5,5,5,5,5}); // 5 copies of 10
l1.assign(c.begin(), c.begin() + 5); // starting 5 elements of another container
```

To get the number of elements, the same functions for `std::deque` are available here.

```c++
auto is_empty1 { l1.size() == 0 };
auto is_empty2 { l1.empty() };
```

To iterate over the elements, use `being()` and `end()`.

```c++
// RECALL: for-each loop will implicitly call begin() and end()
for (auto &obj : l1) {
    // do something with value here
}
```

```{note}
There's also ..

 * `cbegin()` / `cend()` which returns a constant iterator (can't change values?).
 * `rbegin()` / `rend()` which returns an iterator that goes in reverse order.
 * `crbegin()` / `crend()` which is a mixture of the above two.
```

`std::list` has several helper functions built-in.

 * `merge()` combines two sorted `std::list`s into a single sorted `std::list` and empty them.
 * `splice()` transfers a range of elements from one `std::list` to another.
 * `remove()` searches for and removes all matching elements in a `std::list`.
 * `remove_if()` removes all elements in a `std::list` that matches some predicate.
 * `reverse()` reverses an `std::list` (in-place reversal).
 * `sort()` sorts an `std::list` based on a comparator (in-place sort).
 * `unique()` removes consecutive duplicate elements.

### Ordered Associative

`{bm} /(Library Functions\/Containers\/Ordered Associative)_TOPIC/`

Ordered associative containers organize objects by key and potentially a value. Keys are sorted into a specific order, meaning that a comparison function is required. The underlying data structure used by ordered associative containers is a red-black tree.

```{note}
Unsure if the spec defines if they should be implemented as red-black trees, but from what I've read that's how they're implemented.
```

The subsections below detail the various ordered associative containers that are provided by the C++ standard library.

#### Set

`{bm} /(Library Functions\/Containers\/Ordered Associative\/Set)_TOPIC/`

```{prereq}
Library Functions/Allocators_TOPIC
```

`std::set` is a container that holds on to _unique_ elements in sorted order, where that order is defined by a comparator.

To create a `std::set` primed with a sequence of values known as compile-time, use typical braced initialization. Since only unique values are allowed, duplicates will be ignored. By default, the comparator `std::less` is used which uses the less than operator (<) to compare two objects for priority.

```c++
std::set<int> s1 { 1, 1, 2, 3, 4, 5 };
```

To create a `std::set` without priming it directly to a sequence of values, you can't use braced initialization or brace-plus-equals initialization. You must use parenthesis.

```c++
std::set<int> s2 (c.begin(), c.begin() + 10)  // copy first 10 elems from another container

// CUSTOM COMPARATOR
auto comparator = [] (const int & lhs, const int & rhs) -> bool { return lhs < rhs; };
std::set<int, decltype(comparator)> s3 ({ 1, 1, 2, 3, 4, 5 }, comparator);
std::set<int, decltype(std::greater)> s4 ({ 1, 1, 2, 3, 4, 5 }, std::greater);
```

`std::set` provides copy semantics and move semantics. Because elements are dynamic objects, moving one `std::set` into another is fast because it's simply passing off a pointer / reference. Copying can potentially be expensive.

```c++
std::set<int> s5 { std::move(s1) }; // move s1 into s5
```

Similarly, because `std::set`'s elements are created as dynamic objects, you have the option of supplying a custom allocator.

```c++
CustomAllocator allocator {};
std::set<int, decltype(std::less), CustomAllocator> s6 (std::less, allocator);
```

To check an element exists, the following functions are available:

 * `find()` return an iterator primed at the position of the found element (returns `end()` iterator position if not found).
 * `contains()` returns bool (true if it exists, false otherwise).
 * `count()` returns integer (1 if it exists, 0 otherwise).

```c++
bool found { s1.find(3) != s1.end() };
bool found { s1.contains(3) };
bool found { s1.count(3) == 1 };
```

To find the first element that is greater than or equal (>=) to some value, use `lower_bound()`. Similarly, to find the first element that's greater than (>) some value, use `upper_bound()`.

```c++
auto it1 { s1.lower_bound(4) }; // get iterator to elem 4 if 4 exists, otherwise get iterator to the elem just after 4 (could be s1.end() if no such elem)
auto it2 { s1.upper_bound(4) }; // get iterator to elem just after 4 (could be s1.end() if no such elem)
```

To add an element, the following functions are available:

 * `insert()` either copies or moves into the container (depending on if the reference passed in is an rvalue reference).
 * `emplace()` adds an element _by creating it directly_ (no copying / moving).
 * `emplace_hint()` like the above but also takes in an iterator primed to some position as a hint.

```c++
s1.insert(6);
s1.emplace(6);
s1.emplace_hint(s1.begin(), 6);  // iterator should be near to where the value is
```

```{note}
`emplace()` / `emplace_hint()` don't copy or move because you pass in initialization arguments directly into the functions. Internally, they use template parameter packs to forward arguments for object creation (e.g. constructor arguments, initializer list, etc..).
```

```{seealso}
Library Functions/Utility Wrappers/Any_TOPIC (also has an `emplace()` function)
Library Functions/Utility Wrappers/Variant_TOPIC (also has an `emplace()` function)
```

To delete an element at some specific iterator position, use either `extract()` or `erase()`. The difference is that `extract()` will return the element while `erase()` won't.

```c++
auto it1 { s1.begin() };
int res { s1.extract(it1) };  // WARNING: it1 invalid after this point
auto it2 { s1.begin() };
s1.erase(it2);  // WARNING: it2 invalid after this point

// DELETE between idx range
auto it3 {s1.begin()};
auto it4 {s1.begin() + 10};
l1.erase(it3, it4); // WARNING: it3/it4 invalid after this call
```

To delete all elements, use `clear()`.

```c++
s1.clear();
```

To get the number of elements, use `size()`. Similarly, use `empty()` to check if empty.

```c++
auto is_empty1 { s1.size() == 0 };
auto is_empty2 { s1.empty() };
```

To iterate over the elements, use `being()` and `end()`.

```c++
// RECALL: for-each loop will implicitly call begin() and end()
for (auto &obj : s1) {
    // do something with value here
}
```

```{note}
There's also ..

 * `cbegin()` / `cend()` which returns a constant iterator (can't change values?).
 * `rbegin()` / `rend()` which returns an iterator that goes in reverse order.
 * `crbegin()` / `crend()` which is a mixture of the above two.
```

#### Multiset

`{bm} /(Library Functions\/Containers\/Ordered Associative\/Multiset)_TOPIC/`

```{prereq}
Library Functions/Containers/Ordered Associative/Set_TOPIC
```

`std::multiset` is a container that, like a `std::set`, holds on to elements in sorted order where that order is defined by a comparator. Unlike `std::set`, it can hold on to multiple instances of the same element (elements aren't unique). Rather than using the equality operator (==) to find duplicates, `std::multiset` uses the sorting comparator: two objects a and b are considered equivalent if neither compares less than the other: `!comp(a, b) && !comp(b, a)`.

```{note}
Definition is from cppreference.
```

To create a `std::multiset`, the same `std::set` constructors apply. The only major difference is that, if you're initializing the values, any duplicate values are kept.

```c++
// prime
std::multiset<int> s1 { 1, 1, 2, 3, 4, 5 };  // DUPLICATES RETAINED
// copy range
std::multiset<int> s2 (c.begin(), c.begin() + 10)  // copy first 10 elems from another container
// custom comparator
auto comparator = [] (const int & lhs, const int & rhs) -> bool { return lhs < rhs; };
std::multiset<int, decltype(comparator)> s3 ({ 1, 1, 2, 3, 4, 5 }, comparator);
std::multiset<int, decltype(std::greater)> s4 ({ 1, 1, 2, 3, 4, 5 }, std::greater);
// copy/move
std::multiset<int> s5 { std::move(s1) };  // move s1 into s5
// custom allocator
CustomAllocator allocator {};
std::multiset<int, decltype(std::less), CustomAllocator> s6 (std::less, allocator);
```

Functions are more or less the same as those in `std::set`. The only major difference is that `count()` returns the number of instances for an element.

```c++
// find
bool found { s1.find(1) != s1.end() };
bool found { s1.contains(1) };
// get number of instances
bool is_two_instances { s1.count(1) == 2 };
// get lower/upper bound
auto it1 { s1.lower_bound(4) }; // get iterator to elem 4 if 4 exists, otherwise get iterator to the elem just after 4 (could be s1.end() if no such elem)
auto it2 { s1.upper_bound(4) }; // get iterator to elem just after 4 (could be s1.end() if no such elem)
// add
s1.insert(6);
s1.emplace(6);
s1.emplace_hint(s1.begin(), 6);  // iterator should be near to where the value is
// remove
auto it1 { s1.begin() };
int res { s1.extract(it1) };  // WARNING: it1 invalid after this point
auto it2 { s1.begin() };
s1.erase(it2);  // WARNING: it2 invalid after this point
// remove range
auto it3 {s1.begin()};
auto it4 {s1.begin() + 10};
l1.erase(it3, it4); // WARNING: it3/it4 invalid after this call
// remove all
s1.clear();
// get size
auto is_empty1 { s1.size() == 0 };
auto is_empty2 { s1.empty() };
// iterate
for (auto &obj : s1) {  // RECALL: for-each loop will implicitly call begin() and end()
    // do something with value here
}
```

```{note}
There's also ..

 * `cbegin()` / `cend()` which returns a constant iterator (can't change values?).
 * `rbegin()` / `rend()` which returns an iterator that goes in reverse order.
 * `crbegin()` / `crend()` which is a mixture of the above two.
```

#### Map

`{bm} /(Library Functions\/Containers\/Ordered Associative\/Map)_TOPIC/`

```{prereq}
Library Functions/Containers/Ordered Associative/Set_TOPIC
```

`std::map` is a container similar to `std::set`, with the major difference being that each element in a `std::map` has a secondary value associated with it: key to value. Only the key is used for ordering, uniqueness, and lookup. The value just tags along.

To create a `std::map`, the same `std::set` constructors apply. The only major differences are that ...

 1. the type of the value needs to be specified as the second template parameter.
 2. if initializing to a list of key-value pairs, each element of the initializer list must be `std::pair<K,V>` (`K` is key type, `V` is value type).

```c++
// prime
std::map<int. float> s0 {
    std::pair<int, float> { 1, 99.0f },
    std::pair<int, float> { 1, -99.0f },  // WARNING: this is the 2nd instance of the key 1, which value is inserted for the key is undefined
    std::pair<int, float> { 2, -100.0f },
    std::pair<int, float> { 4, 123.0f },
    std::pair<int, float> { 5, 4.0f }
};
std::map<int. float> s1 {
    { 1, 99.0f },
    { 1, -99.0f },  // WARNING: this is the 2nd instance of the key 1, which value is inserted for the key is undefined
    { 2, -100.0f },
    { 4, 123.0f },
    { 5, 4.0f }
};
// copy range
std::map<int> s2 (c.begin(), c.begin() + 10)  // copy first 10 key-value pairs from another container
// custom comparator
auto comparator = [] (const int & lhs, const int & rhs) -> bool { return lhs < rhs; };
std::map<int, float, decltype(comparator)> s3 ({ { 1, 99.0f }, { 2, 3.0f }, ... }, comparator);
std::map<int, float, decltype(std::greater)> s4 ({ { 1, 99.0f }, { 2, 3.0f }, ... }, std::greater);
// copy/move
std::map<int, float> s5 { std::move(s1) }; // move s1 into s5
// custom allocator
CustomAllocator allocator {};
std::map<int, float, decltype(std::less), CustomAllocator> s6 (std::less, allocator);
```


To check an element exists, the following functions are available:

 * `find()` return an iterator primed at the position of the found element (returns `end()` iterator position if not found).
 * `contains()` returns bool (true if it exists, false otherwise).
 * `count()` returns integer (0 is false, 1 is true).

```c++
bool found { s1.find(3) != s1.end() };
bool found { s1.contains(3) };
bool found { s1.count(3) == 1 };
```

Dereferencing an iterator will give back both the key and value as a `std::pair<K,V>`.

```c++
auto it { s1.find(3) };
std::pair<int, float> found_pair { *it };
```

To find the first key-value pair where the key is greater than or equal (>=) to some other key, use `lower_bound()`. Similarly, to find the first key-value pair where the key is greater than (>) some other key, use `upper_bound()`.

```c++
auto it1 { s1.lower_bound(4) }; // get iterator to elem 4 if 4 exists, otherwise get iterator to the elem just after 4 (could be s1.end() if no such elem)
auto it2 { s1.upper_bound(4) }; // get iterator to elem just after 4 (could be s1.end() if no such elem)
```

To add a key-value pair (not _replace_ an existing value), the following functions are available:

 * `insert()` either copies or moves into the container (depending on if the reference passed in is an rvalue reference).
 * `emplace()` adds an element _by creating it directly_ (no copying / moving).
 * `try_emplace()` like `emplace()` but has special move semantics (does not move template parameter pack rvalue arguments if insertion doesn't happen -- see docs for more info).
 * `emplace_hint()` like `emplace()` but also takes in an iterator primed to some position as a hint.

```c++
// NOTE: Each func returns a bool (true for insertion, false for already exists) + an iterator to the key-value pair (existing one if not added)
s1.insert(6, 122.0f);
s1.insert(std::pair<int, float> {6, 122.0f});
s1.emplace(6, 122.0f);
s1.emplace(std::pair<int, float> {6, 122.0f});
s1.try_emplace(6, 122.0f);
s1.try_emplace(std::pair<int, float> {6, 122.0f});
s1.emplace_hint(s1.begin(), 6, 122.0f);  // iterator should be near to where the value is
s1.emplace_hint(s1.begin(), std::pair<int, float> {6, 122.0f});
```

To replace a value for an already existing key, `insert_or_assign()` either copies or moves into the container (depending on if the reference passed in is an rvalue reference), replacing it if it already exists.

```c++
// NOTE: returns a bool (true for insertion, false for assignment) + an iterator to the key-value pair (existing one if not added)
s1.insert_or_assign(6, 122.0f);
s1.insert_or_assign(std::pair<int, float> {6, 122.0f});
```

To delete an element at some specific iterator position, use either `extract()` or `erase()`. The difference is that `extract()` will return the key-value while `erase()` won't.

```c++
auto it1 { s1.begin() };
int res { s1.extract(it1) };  // WARNING: it1 invalid after this point
auto it2 { s1.begin() };
s1.erase(it2);  // WARNING: it2 invalid after this point

// DELETE between idx range
auto it3 {s1.begin()};
auto it4 {s1.begin() + 10};
l1.erase(it3, it4); // WARNING: it3/it4 invalid after this call
```

To delete all elements, use `clear()`.

```c++
s1.clear();
```

To get the number of elements, use `size()`. Similarly, use `empty()` to check if empty.

```c++
auto is_empty1 { s1.size() == 0 };
auto is_empty2 { s1.empty() };
```

To iterate over the elements, use `being()` and `end()`.

```c++
// RECALL: for-each loop will implicitly call begin() and end()
for (auto &obj : s1) {
    // do something with value here
}
```

```{note}
There's also ..

 * `cbegin()` / `cend()` which returns a constant iterator (can't change values?).
 * `rbegin()` / `rend()` which returns an iterator that goes in reverse order.
 * `crbegin()` / `crend()` which is a mixture of the above two.
```

#### Multimap

`{bm} /(Library Functions\/Containers\/Ordered Associative\/Multimap)_TOPIC/`

```{prereq}
Library Functions/Containers/Ordered Associative/Multiset_TOPIC
Library Functions/Containers/Ordered Associative/Map_TOPIC
```

`std::multimap` is a container that's a combination of `std::multiset` and `std::map`. That is, it's a `std::map` but it allows for many key-value pairs with the same key (keys aren't unique). Similar to `std::multiset`, `std::multimap` uses the sorting comparator to find duplicates: two objects a and b are considered equivalent if neither compares less than the other: `!comp(a, b) && !comp(b, a)`.

```{note}
Definition is from cppreference.
```

To create a `std::multimap`, the same `std::map` constructors apply. The only major difference is that, if you're initializing the values, any duplicate values are kept.

```c++
// prime
std::unordered_multimap<int. float> s0 {
    std::pair<int, float> { 1, 99.0f },
    std::pair<int, float> { 1, -99.0f },  // NOTE: this is the 2nd instance of the key 1, both key-value pairs are kept
    std::pair<int, float> { 2, -100.0f },
    std::pair<int, float> { 4, 123.0f },
    std::pair<int, float> { 5, 4.0f }
};
std::unordered_multimap<int. float> s1 {
    { 1, 99.0f },
    { 1, -99.0f },  // NOTE: this is the 2nd instance of the key 1, both key-value pairs are kept
    { 2, -100.0f },
    { 4, 123.0f },
    { 5, 4.0f }
};
// copy range
std::unordered_multimap<int> s2 (c.begin(), c.begin() + 10)  // copy first 10 key-value pairs from another container
// custom comparator
auto comparator = [] (const int & lhs, const int & rhs) -> bool { return lhs < rhs; };
std::unordered_multimap<int, float, decltype(comparator)> s3 ({ { 1, 99.0f }, { 2, 3.0f }, ... }, comparator);
std::unordered_multimap<int, float, decltype(std::greater)> s4 ({ { 1, 99.0f }, { 2, 3.0f }, ... }, std::greater);
// copy/move
std::unordered_multimap<int, float> s5 { std::move(s1) }; // move s1 into s5
// custom allocator
CustomAllocator allocator {};
std::unordered_multimap<int, float, decltype(std::less), CustomAllocator> s6 (std::less, allocator);
```

Functions are more or less the same as their `std::map` counterparts. The only major difference are that...

 1. `count()` returns the number of instances for an element.are available
 2. `insert_or_assign()` is removed because it doesn't make sense to have it (you can have duplicate keys).
 3. `try_emplace()` is removed because it doesn't make sense to have it (you can have duplicate keys).

```c++
// find
bool found { s1.find(3) != s1.end() };
bool found { s1.contains(3) };
// get
auto it { s1.find(3) };  // WARNING: if there's multiple instances of key, any of them could be returned here
std::pair<int, float> found_pair { *it };
// get number of instances
bool is_two_instances { s1.count(1) == 2 };
// get lower/upper bound
auto it1 { s1.lower_bound(4) }; // get iterator to elem 4 if 4 exists, otherwise get iterator to the elem just after 4 (could be s1.end() if no such elem)
auto it2 { s1.upper_bound(4) }; // get iterator to elem just after 4 (could be s1.end() if no such elem)
// add
s1.insert(6, 122.0f);
s1.insert(std::pair<int, float> {6, 122.0f});
s1.emplace(6, 122.0f);
s1.emplace(std::pair<int, float> {6, 122.0f});
s1.emplace_hint(s1.begin(), 6, 122.0f);  // iterator should be near to where the value is
s1.emplace_hint(s1.begin(), std::pair<int, float> {6, 122.0f});  // iterator should be near to where the value is
// remove
auto it1 { s1.begin() };
int res { s1.extract(it1) };  // WARNING: it1 invalid after this point
auto it2 { s1.begin() };
s1.erase(it2);  // WARNING: it2 invalid after this point
// remove range
auto it3 {s1.begin()};
auto it4 {s1.begin() + 10};
l1.erase(it3, it4); // WARNING: it3/it4 invalid after this call
// remove all
s1.clear();
// get size
auto is_empty1 { s1.size() == 0 };
auto is_empty2 { s1.empty() };
// iterate
for (auto &obj : s1) {
    // do something with value here
}
```

```{note}
There's also ..

 * `cbegin()` / `cend()` which returns a constant iterator (can't change values?).
 * `rbegin()` / `rend()` which returns an iterator that goes in reverse order.
 * `crbegin()` / `crend()` which is a mixture of the above two.
```

### Unordered Associative

`{bm} /(Library Functions\/Containers\/Unordered Associative)_TOPIC/`

Unordered associative containers organize objects by key and potentially a value. Keys are stored in an unordered fashion. The underlying data structure used by unordered associative containers is a hash table.

By default, unordered associative containers attempt to hash keys by calling template specializations of `std::hash<T>`. Several pre-existing template specializations are provided by the C++ standard library (e.g. `int` ,`long`, `std::string`, etc..), but custom types need their own specialization to be written by the user.

`std::hash<T>` implementations must be exposed as a functor that takes in the type in question and returns a `std::size_t`.

```c++
template<>
struct std::hash<MyType> {
    std::size_t operator()(S const& s) const noexcept {
        std::size_t h1 { std::hash<std::string>{} (s.student_name) };
        std::size_t h2 { std::hash<int>{} (s.student_age) };
        return h1 ^ h2; // see boost::hash_combine
    }
};
```

A common point of confusion is what you have to do to use `std::hash` with a reference type. Note that the function call operator in the example above is taking a reference, meaning you always use the non-reference type as the type argument when invoking.

```c++
int x { 55 };
int & xRef { x };
std::size_t hash1 { std::hash<int>{} (x) };
std::size_t hash2 { std::hash<int>{} (xRef) };
```

The subsections below detail the various unordered associative containers that are provided by the C++ standard library.

#### Set

`{bm} /(Library Functions\/Containers\/Unordered Associative\/Set)_TOPIC/`

```{prereq}
Library Functions/Containers/Ordered Associative/Set_TOPIC
Library Functions/Allocators_TOPIC
```

`std::unordered_set` is a container that's similar to `std::set`. It holds on to unique elements but does so _unordered_ (whereas `std::set` has some sort order). It's implemented as a hash table, so rather than having to specify a comparator, you're required to specify a hash function.

Several pre-existing hash functions are provided by the C++ standard library via `std::hash<T>` (`T` being the type in question). If the user doesn't supply a hash function directly, the default is to use `std::hash<T>` with the element type substituted in (compilation will fail if no `std::hash<T>` implementation for that element type exists). For example, `std::hash<int>` exists for integers and gets automatically plugged in when the element type of the container is `int`.

````{note}
Details on providing a custom `std::hash<T>` implementation are in the parent section.
````

In addition to a hash function, a `std::unordered_set` may have a custom equivalence function. By default, `std::equal_to<T>` is used if none is supplied by the user, which uses the equality operator (==).

To create a `std::unordered_set` primed with a sequence of values known as compile-time, use typical braced initialization. Since only unique values are allowed, duplicates will be ignored. 

```c++
std::unordered_set<int> s1 { 1, 1, 2, 3, 4, 5 };
```

To create a `std::unordered_set` without priming it directly to a sequence of values, you can't use braced initialization or brace-plus-equals initialization. You must use parenthesis.

```c++
std::unordered_set<int> s2 (c.begin(), c.begin() + 10)  // copy first 10 elems from another container
```

To create a `std::unordered_set` with a custom hash function, that custom hash function can be implemented in one of two ways: 

 * a function-like object that takes a single parameter of element type and returns the hash code as a `size_t`.
 * a template specialization `std::hash<T>` for the element type (assuming one wasn't already supplied by the C++ standard library).

```c++
// function-like object
auto hasher = [] (const int & val) -> size_t { return static_cast<size_t>(val); };
std::unordered_set<int, decltype(hasher)> s3 ({ 1, 1, 2, 3, 4, 5 }, hasher);
```

```{note}
I think (not sure) if you create a `std::hash<T>` implementation for the element type, the `std::unordered_set` should automatically pick it without having to specify the template parameter + directly passing it in as an argument (as done above). It should work so long as the implementation is visible (e.g. whatever file its in has been `#include`-ed) when the container is created.
```

`std::unordered_set` provides copy semantics and move semantics. Because elements are dynamic objects, moving one `std::unordered_set` into another is fast because it's simply passing off a pointer / reference. Copying can potentially be expensive.

```c++
std::unordered_set<int> s4 { std::move(s1) }; // move s1 into s4
```

Similarly, because `std::unordered_set`'s elements are created as dynamic objects, you have the option of supplying a custom allocator.

```c++
CustomAllocator allocator {};
std::unordered_set<int, decltype(std::hash<int>), decltype(std::equal_to<int>), CustomAllocator> s5 (allocator);
```

```{note}
Similar to a Java `HashMap`, a `std::unordered_set` has concept_NORMs such as bucket count and load factor. It'll automatically add more buckets and rehash once the load factor reaches some point, all of which is tunable if you deem the performance of the defaults as not good. Alternatively, you can always trigger a rehash manually.

Those features aren't discussed here.
```

`std::unordered_set` supports most of the same functions as `std::set` except for those that have to do with sorted ordering. For example, `lower_bound()` and `upper_bound()` are missing here because the elements here aren't ordered.

To check if a set contains an element, the following functions are available:

 * `find()` return an iterator primed at the position of the found element (returns `end()` iterator position if not found).
 * `contains()` returns bool (true if it exists, false otherwise).
 * `count()` returns integer (1 if it exists, 0 otherwise).

```c++
bool found { s1.find(3) != s1.end() };
bool found { s1.contains(3) };
bool found { s1.count(3) == 1 };
```

To add an element, the following functions are available:

 * `insert()` either copies or moves a value into the container (depending on if the reference passed in is an rvalue reference).
 * `emplace()` adds an element _by creating it directly_ (no copying / moving).
 * `emplace_hint()` like the above but also takes in an iterator primed to some position as a hint.

```c++
s1.insert(6);
s1.emplace(6);
s1.emplace_hint(6, s1.begin());
```

```{note}
`emplace()` / `emplace_hint()` don't copy or move because you pass in initialization arguments directly into the functions. Internally, they use template parameter packs to forward arguments for object creation (e.g. constructor arguments, initializer list, etc..).
```

```{seealso}
Library Functions/Utility Wrappers/Any_TOPIC (also has an `emplace()` function)
Library Functions/Utility Wrappers/Variant_TOPIC (also has an `emplace()` function)
```

To delete an element at some specific iterator position, use either `extract()` or `erase()`. The difference is that `extract()` will return the element while `erase()` won't.

```c++
auto it1 { s1.begin() };
int res { s1.extract(it1) };  // WARNING: it1 invalid after this point
auto it2 { s1.begin() };
s1.erase(it2);  // WARNING: it2 invalid after this point

// DELETE between idx range
auto it3 {s1.begin()};
auto it4 {s1.begin() + 10};
l1.erase(it3, it4); // WARNING: it3/it4 invalid after this call
```

To delete all elements, use `clear()`.

```c++
s1.clear();
```

To get the number of elements, use `size()`. Similarly, use `empty()` to check if empty.

```c++
auto is_empty1 { s1.size() == 0 };
auto is_empty2 { s1.empty() };
```

To iterate over the elements, use `being()` and `end()`.

```c++
// RECALL: for-each loop will implicitly call begin() and end()
for (auto &obj : s1) {
    // do something with value here
}
```

```{note}
There's also ..

 * `cbegin()` / `cend()` which returns a constant iterator (can't change values?).
 * `rbegin()` / `rend()` which returns an iterator that goes in reverse order.
 * `crbegin()` / `crend()` which is a mixture of the above two.
```

#### Multiset

`{bm} /(Library Functions\/Containers\/Unordered Associative\/Multiset)_TOPIC/`

```{prereq}
Library Functions/Containers/Unordered Associative/Set_TOPIC
```

`std::unordered_multiset` is a container that, like a `std::unordered_set`, holds on to unordered elements. Like `std::unordered_set`, it requires a hashing function and an equivalence function (same defaults are used if not supplied). Unlike `std::unordered_set`, it can hold on to multiple instances of the same element (elements aren't unique). 

````{note}
Details on providing a custom `std::hash<T>` implementation are in the parent section.

Details on providing a custom hasher implementation specifically for the container are in the unordered set section.
````

To create a `std::unordered_multiset`, the same `std::unordered_set` constructors apply. The only major difference is that, if you're initializing the values, any duplicate values are kept.

```c++
// prime
std::unordered_multiset<int> s1 { 1, 1, 2, 3, 4, 5 };  // DUPLICATED RETAINED
// copy range
std::unordered_multiset<int> s2 (c.begin(), c.begin() + 10)  // copy first 10 elems from another container
// custom hash function
auto hasher = [] (const int & val) -> size_t { return static_cast<size_t>(val); };
std::unordered_multiset<int, decltype(hasher)> s3 ({ 1, 1, 2, 3, 4, 5 }, hasher);
// copy/move
std::unordered_multiset<int> s4 { std::move(s1) };  // move s1 into s4
CustomAllocator allocator {};
std::unordered_multiset<int, decltype(std::hash<int>), decltype(std::equal_to<int>), CustomAllocator> s5 (allocator);
```

Functions are more or less the same as those in `std::unordered_set`. The only major difference is that `count()` returns the number of instances for an element.

```c++
// find
bool found { s1.find(1) != s1.end() };
bool found { s1.contains(1) };
// get number of instances
bool is_two_instances { s1.count(1) == 2 };
// add
s1.insert(6);
s1.emplace(6);
s1.emplace_hint(s1.begin(), 6);  // iterator should be near to where the value is
// remove
auto it1 { s1.begin() };
int res { s1.extract(it1) };  // WARNING: it1 invalid after this point
auto it2 { s1.begin() };
s1.erase(it2);  // WARNING: it2 invalid after this point
// remove range
auto it3 {s1.begin()};
auto it4 {s1.begin() + 10};
l1.erase(it3, it4); // WARNING: it3/it4 invalid after this call
// remove all
s1.clear();
// get size
auto is_empty1 { s1.size() == 0 };
auto is_empty2 { s1.empty() };
// iterate
for (auto &obj : s1) {  // RECALL: for-each loop will implicitly call begin() and end()
    // do something with value here
}
```

```{note}
There's also ..

 * `cbegin()` / `cend()` which returns a constant iterator (can't change values?).
 * `rbegin()` / `rend()` which returns an iterator that goes in reverse order.
 * `crbegin()` / `crend()` which is a mixture of the above two.
```

#### Map

`{bm} /(Library Functions\/Containers\/Unordered Associative\/Map)_TOPIC/`

```{prereq}
Library Functions/Containers/Unordered Associative/Set_TOPIC
```

`std::unordered_map` is a container similar to `std::unordered_set`, with the major difference being that each element in a `std::unordered_map` has a secondary value associated with it: key to value. Only the key is used for uniqueness and lookup. The value just tags along.

````{note}
Details on providing a custom `std::hash<T>` implementation are in the parent section.

Details on providing a custom hasher implementation specifically for the container are in the unordered set section.
````

To create a `std::unordered_map`, the same `std::unordered_set` constructors apply. The only major differences are that ...

 1. the type of the value needs to be specified as the second template parameter.
 2. if initializing to a list of key-value pairs, each element of the initializer list must be `std::pair<K,V>` (`K` is key type, `V` is value type).

```c++
// prime
std::unordered_map<int. float> s0 {
    std::pair<int, float> { 1, 99.0f },
    std::pair<int, float> { 1, -99.0f },  // WARNING: this is the 2nd instance of the key 1, which value is inserted for the key is undefined
    std::pair<int, float> { 2, -100.0f },
    std::pair<int, float> { 4, 123.0f },
    std::pair<int, float> { 5, 4.0f }
};
std::unordered_map<int. float> s1 {
    { 1, 99.0f },
    { 1, -99.0f },  // WARNING: this is the 2nd instance of the key 1, which value is inserted for the key is undefined
    { 2, -100.0f },
    { 4, 123.0f },
    { 5, 4.0f }
};
// copy range
std::unordered_map<int> s2 (c.begin(), c.begin() + 10)  // copy first 10 key-value pairs from another container
// custom hash function
auto hasher = [] (const int & val) -> size_t { return static_cast<size_t>(val); };
std::unordered_map<int, float, decltype(hasher)> s3 ({ { 1, 99.0f }, { 2, 3.0f }, ... }, hasher);
// copy/move
std::unordered_map<int, float> s5 { std::move(s1) };  // move s1 into s5
// custom allocator
CustomAllocator allocator {};
std::unordered_map<int, float, decltype(std::less), CustomAllocator> s6 (std::less, allocator);
```

To check an element exists, the following functions are available:

 * `find()` return an iterator primed at the position of the found element (returns `end()` iterator position if not found).
 * `contains()` returns bool (true if it exists, false otherwise).
 * `count()` returns integer (0 is false, 1 is true).

```c++
bool found { s1.find(3) != s1.end() };
bool found { s1.contains(3) };
bool found { s1.count(3) == 1 };
```

Dereferencing an iterator will give back both the key and value as a `std::pair<K,V>`.

```c++
auto it { s1.find(3) };
std::pair<int, float> found_pair { *it };
```

To add a key-value pair (not _replace_ an existing value), the following functions are available:

 * `insert()` either copies or moves into the container (depending on if the reference passed in is an rvalue reference).
 * `emplace()` adds an element _by creating it directly_ (no copying / moving).
 * `try_emplace()` like `emplace()` but has special move semantics (does not move template parameter pack rvalue arguments if insertion doesn't happen -- see docs for more info).
 * `emplace_hint()` like `emplace()` but also takes in an iterator primed to some position as a hint.

```c++
// NOTE: Each func returns a bool (true for insertion, false for already exists) + an iterator to the key-value pair (existing one if not added)
s1.insert(6, 122.0f);
s1.insert(std::pair<int, float> {6, 122.0f});
s1.emplace(6, 122.0f);
s1.emplace(std::pair<int, float> {6, 122.0f});
s1.try_emplace(6, 122.0f);
s1.try_emplace(std::pair<int, float> {6, 122.0f});
s1.emplace_hint(s1.begin(), 6, 122.0f);  // iterator should be near to where the value is
s1.emplace_hint(s1.begin(), std::pair<int, float> {6, 122.0f});
```

To replace a value for an already existing key, `insert_or_assign()` either copies or moves into the container (depending on if the reference passed in is an rvalue reference), replacing it if it already exists.

```c++
// NOTE: returns a bool (true for insertion, false for assignment) + an iterator to the key-value pair (existing one if not added)
s1.insert_or_assign(6, 122.0f);
s1.insert_or_assign(std::pair<int, float> {6, 122.0f});
```

To delete an element at some specific iterator position, use either `extract()` or `erase()`. The difference is that `extract()` will return the key-value while `erase()` won't.

```c++
auto it1 { s1.begin() };
int res { s1.extract(it1) };  // WARNING: it1 invalid after this point
auto it2 { s1.begin() };
s1.erase(it2);  // WARNING: it2 invalid after this point

// DELETE between idx range
auto it3 {s1.begin()};
auto it4 {s1.begin() + 10};
l1.erase(it3, it4); // WARNING: it3/it4 invalid after this call
```

To delete all elements, use `clear()`.

```c++
s1.clear();
```

To get the number of elements, use `size()`. Similarly, use `empty()` to check if empty.

```c++
auto is_empty1 { s1.size() == 0 };
auto is_empty2 { s1.empty() };
```

To iterate over the elements, use `being()` and `end()`.

```c++
// RECALL: for-each loop will implicitly call begin() and end()
for (auto &obj : s1) {
    // do something with value here
}
```

```{note}
There's also ..

 * `cbegin()` / `cend()` which returns a constant iterator (can't change values?).
 * `rbegin()` / `rend()` which returns an iterator that goes in reverse order.
 * `crbegin()` / `crend()` which is a mixture of the above two.
```

#### Multimap

`{bm} /(Library Functions\/Containers\/Unordered Associative\/Multimap)_TOPIC/`

```{prereq}
Library Functions/Containers/Unordered Associative/Multiset_TOPIC
Library Functions/Containers/Unordered Associative/Map_TOPIC
```

`std::unordered_multimap` is a container that's a combination of `std::unordered_multiset` and `std::unordered_map`. That is, it's a `std::unordered_map` but it allows for many key-value pairs with the same key (keys aren't unique). Similar to `std::unordered_multiset`, `std::unordered_multimap` requires a hashing function and an equivalence function (same defaults are used if not supplied).

````{note}
Details on providing a custom `std::hash<T>` implementation are in the parent section.

Details on providing a custom hasher implementation specifically for the container are in the unordered set section.
````

To create a `std::multimap`, the same `std::map` constructors apply. The only major difference is that, if you're initializing the values, any duplicate values are kept.

```c++
// prime
std::unordered_multimap<int. float> s0 {
    std::pair<int, float> { 1, 99.0f },
    std::pair<int, float> { 1, -99.0f },  // NOTE: this is the 2nd instance of the key 1, both key-value pairs are kept
    std::pair<int, float> { 2, -100.0f },
    std::pair<int, float> { 4, 123.0f },
    std::pair<int, float> { 5, 4.0f }
};
std::unordered_multimap<int. float> s1 {
    { 1, 99.0f },
    { 1, -99.0f },  // NOTE: this is the 2nd instance of the key 1, both key-value pairs are kept
    { 2, -100.0f },
    { 4, 123.0f },
    { 5, 4.0f }
};
// copy range
std::unordered_multimap<int> s2 (c.begin(), c.begin() + 10)  // copy first 10 key-value pairs from another container
// custom comparator
auto hasher = [] (const int & val) -> size_t { return static_cast<size_t>(val); };
std::unordered_multimap<int, float, decltype(hasher)> s3 ({ { 1, 99.0f }, { 2, 3.0f }, ... }, hasher);
// copy/move
std::unordered_multimap<int, float> s5 { std::move(s1) }; // move s1 into s5
// custom allocator
CustomAllocator allocator {};
std::unordered_multimap<int, float, decltype(std::less), CustomAllocator> s6 (std::less, allocator);
```

Functions are more or less the same as their `std::unordered_map` counterparts. The only major difference are that...

 1. `count()` returns the number of instances for an element.are available
 2. `insert_or_assign()` is removed because it doesn't make sense to have it (you can have duplicate keys).
 3. `try_emplace()` is removed because it doesn't make sense to have it (you can have duplicate keys).

```c++
// find
bool found { s1.find(3) != s1.end() };
bool found { s1.contains(3) };
// get
auto it { s1.find(3) };  // WARNING: if there's multiple instances of key, any of them could be returned here
std::pair<int, float> found_pair { *it };
// get number of instances
bool is_two_instances { s1.count(1) == 2 };
// add
s1.insert(6, 122.0f);
s1.insert(std::pair<int, float> {6, 122.0f});
s1.emplace(6, 122.0f);
s1.emplace(std::pair<int, float> {6, 122.0f});
s1.emplace_hint(s1.begin(), 6, 122.0f);  // iterator should be near to where the value is
s1.emplace_hint(s1.begin(), std::pair<int, float> {6, 122.0f});  // iterator should be near to where the value is
// remove
auto it1 { s1.begin() };
int res { s1.extract(it1) };  // WARNING: it1 invalid after this point
auto it2 { s1.begin() };
s1.erase(it2);  // WARNING: it2 invalid after this point
// remove range
auto it3 {s1.begin()};
auto it4 {s1.begin() + 10};
l1.erase(it3, it4); // WARNING: it3/it4 invalid after this call
// remove all
s1.clear();
// get size
auto is_empty1 { s1.size() == 0 };
auto is_empty2 { s1.empty() };
// iterate
for (auto &obj : s1) {
    // do something with value here
}
```

```{note}
There's also ..

 * `cbegin()` / `cend()` which returns a constant iterator (can't change values?).
 * `rbegin()` / `rend()` which returns an iterator that goes in reverse order.
 * `crbegin()` / `crend()` which is a mixture of the above two.
```

## Container Adapters

`{bm} /(Library Functions\/Container Adapters)_TOPIC/`

```{prereq}
Library Functions/Containers_TOPIC
```

Container adapters are light-weight wrappers around sequential containers that expose them in a simplified way that matches a common data structure. For example, an `std::vector` can be wrapped such that it's exposed as a queue. The caller of the queue doesn't have to know what type of sequential container is backing that queue.

The type of sequential container usable by a container adaptor depends on the functions it has. For example, some container adaptors require both `front()` and `back()` functions to be supported by the sequential container type.

### Stack

`{bm} /(Library Functions\/Container Adapters\/Stack)_TOPIC/`

`std::stack` wraps a sequential container as if it were a stack abstract data type: 

 * The only way to write is to append.
 * The only element that can be read / removed is the last one.

To create a `std::stack`, pass in a reference to the sequential container to wrap: `std::vector`, `std::deque`, or `std::list`. The container will either be copied or moved depending on whether the container reference is an normal reference or an rvalue reference. Alternatively, if you pass in no reference at all, an empty container of the type specified will get used.

```{note}
The sequential container can technically be any class, so long as it supports the expected type traits (e.g. it's expected to have a function called `push_back()` that has a single parameter of type ...).
```

```c++
// create by copying
std::vector<int> c1 { 5, 5, 5, 5, 5, 5, 5, 5 };
std::stack<int, decltype(c1)> s1 { c1 };
// create by moving
std::deque<int> c2 { 5, 5, 5, 5, 5, 5, 5, 5 };
std::stack<int, decltype(c2)> s2 { std::move(c2) };
// create into brand new
std::stack<int, std::list<int>> s3 {};
std::queue<int> q4 {};  // equivalent to using std::deque<int> as the backing type
```

```{seealso}
Core Language/Variables/Rvalue References_TOPIC (refresher on rvalue references)
Core Language/Templates/Type Cloning_TOPIC (refresher on decltype)
```

To add an item, use `push()`. Internally, this invokes the wrapped container's `push_back()` function.

```c++
s3.push(1);
s3.push(2);
s3.push(3);
```

To read the most recently added item, use `top()`. Internally, this invokes the wrapped container's `back()` function.

```c++
int a { s3.top() };
```

To remove the most recently added item, use `pop()`. Internally, this invokes the wrapped container's `pop_back()` function.

```c++
// NOTE: also returns the element removed
s3.pop();
s3.pop();
s3.pop();
```

To get the size, use `size()`. Internally, this invokes the wrapped container function with the same name.

```c++
auto is_empty { s3.size() == 0 };
```

### Queue

`{bm} /(Library Functions\/Container Adapters\/Queue)_TOPIC/`

`std::queue` wraps a sequential container as if it were a queue abstract data type: 

 * The only way to write is to append.
 * The only element that can be read / removed is the head.

To create a `std::queue`, pass in a reference to the sequential container to wrap: `std::deque` or `std::list`. The container will either be copied or moved depending on whether the container reference is an normal reference or an rvalue reference. Alternatively, if you pass in no reference at all, an empty container of the type specified will get used.

```{note}
The sequential container can technically be any class, so long as it supports the expected type traits (e.g. it's expected to have a function called `push_back()` that has a single parameter of type ...).
```

```c++
// create by copying
std::deque<int> c1 { 5, 5, 5, 5, 5, 5, 5, 5 };
std::queue<int, decltype(c1)> q1 { c1 };
// create by moving
std::deque<int> c2 { 5, 5, 5, 5, 5, 5, 5, 5 };
std::queue<int, decltype(c2)> q2 { std::move(c2) };
// create into brand new
std::queue<int, std::list<int>> q3 {};
std::queue<int> q4 {};  // equivalent to using std::deque<int> as the backing type
```

```{seealso}
Core Language/Variables/Rvalue References_TOPIC (refresher on rvalue references)
Core Language/Templates/Type Cloning_TOPIC (refresher on decltype)
```

To add an item, use `push()`. Internally, this invokes the wrapped container's `push_back()` function.

```c++
q3.push(1);
q3.push(2);
q3.push(3);
```

To read the most recently added item, use either `front()` or `back()`. Internally, these invoke the wrapped container functions with the same name.

```c++
int a { q3.front() };
int b { q3.back() };
```

To remove the most recently added item, use `pop()`. Internally, this invokes the wrapped container's `pop_front()` function.

```c++
// NOTE: also returns the element removed
q3.pop();
q3.pop();
q3.pop();
```

To get the size, use `size()`. Internally, this invokes the wrapped container function with the same name.

```c++
auto is_empty { q3.size() == 0 };
```

### Priority Queue

`{bm} /(Library Functions\/Container Adapters\/Priority Queue)_TOPIC/`

`std::priority_queue` wraps a sequential container as if it were a priority queue abstract data type: Regardless of what order elements are added in, the only element that can be read / removed is the element with the highest priority (priority is defined by a comparator).

```{note}
The sequential container can technically be any class, so long as it supports the expected type traits (e.g. it's expected to have a function called `push_back()` that has a single parameter of type ...).
```

To create a `std::priority_queue`, pass in a reference to the sequential container to wrap: `std::vector`, `std::deque`, or `std::list`. The container will either be copied or moved depending on whether the container reference is an normal reference or an rvalue reference. Alternatively, if you pass in no reference at all, an empty container of the type specified will get used.

```c++
// create by copying
std::vector<int> c1 { 5, 5, 5, 5, 5, 5, 5, 5 };
std::priority_queue<int, decltype(c1)> q1 { c1 };
// create by moving
std::deque<int> c2 { 5, 5, 5, 5, 5, 5, 5, 5 };
std::priority_queue<int, decltype(c2)> q2 { std::move(c2) };
// create into brand new
std::priority_queue<int, std::list<int>> q3 {};
std::priority_queue<int> q4 {};  // equivalent to using std::vector<int> as the backing type
```

```{seealso}
Core Language/Variables/Rvalue References_TOPIC (refresher on rvalue references)
Core Language/Templates/Type Cloning_TOPIC (refresher on decltype)
```

In the above examples the default comparator of `std::less` is used, which uses the less than operator (<) to compare two objects for priority. To define a custom comparator, pass in that comparator's type as the 3rd template parameter argument and pass it into the constructor.

```c++
auto comparator = [] (const int & lhs, const int & rhs) -> bool { return lhs < rhs; };
std::priority_queue<int, std::deque<int>, decltype(comparator)> q5 { comparator };
std::priority_queue<int, std::deque<int>, decltype(std::greater<int>)> q6 { std::greater<int> };
```

```{seealso}
Core Language/Lambdas_TOPIC (lambda refresher)
```

To add an item, use `push()`.

```c++
q1.push(10);
q1.push(100);
q1.push(-5);
```

To read the most high priority element, use `top()`.

```c++
int a { q1.top() };
```

To remove the most high priority element, use `pop()`.

```c++
// NOTE: also returns the element removed
q1.pop();
q1.pop();
q1.pop();
```

To get the size, use `size()`.

```c++
auto is_empty { s3.size() == 0 };
```

## Iterator Helpers

`{bm} /(Library Functions\/Iterator Helpers)_TOPIC/`

```{seealso}
Core Language/Iterators_TOPIC (refresher)
```

When writing _generic_ code that makes use of iterators, directly using the iterator may lead to poor performance. For example, if you want an iterator to move up 100 spaces, you can't do `it += 100` because `it` may not be a random access iterator. The safest thing to do for generic code would be to perform `it++` 100 times, but that means you miss out any performance gains of doing `it += 100` if `it` were a random access iterator.

Several helper functions exist to help with examples like the one above. These helper functions choose the most performant way of doing something based on the type traits of the iterator (e.g. if it's a bidirectional iterator vs a random access iterator).

 * `std::advance()` - move forward / backward an iterator by some amount.

   ```c++
   std::advance(it, 100); // move forward 100 spaces
   std::advance(it, -100); // move backward 100 spaces
   ```

 * `std::next()` - move forward by some amount.

   ```c++
   std::next(it); // move forward 1 space
   std::next(it, 100); // move forward 100 spaces
   ```

 * `std::prev()` - move backward by some amount.

   ```c++
   std::prev(it); // move backward 1 space
   std::prev(it, 100); // move backward 100 spaces
   ```

 * `std::distance()` - get distance between two iterators.

   ```c++
   auto d { std::distance(it1, it2) }; // it2 should be > than it1
   ```

 * `std::iter_swap()` - given two iterators, swap the elements at their current position.

    ```c++
    std::iter_swap(it1, it2);
    // NOTE: it1 and it2 don't have to point to the same underlying container or
    // underlying type -- as long as the types are assignable to each other, it'll work.
    ```

## Iterator Adapters

`{bm} /(Library Functions\/Iterator Adapters)_TOPIC/`

```{seealso}
Core Language/Iterators_TOPIC (refresher)
```

Iterator adapters are light-weight wrappers that either simplify operations or provide some functionality under the type traits of an iterator. For example, an iterator exists that can wrap a container as an iterator, where writes to that iterator will translate to inserts into the container.

### Insert

`{bm} /(Library Functions\/Iterator Adapters\/Insert)_TOPIC/`

```{prereq}
Library Functions/Containers_TOPIC
```

An iterator adaptor that wraps a container and exposes it as an output iterator, where writes are translated to inserts on the container. The  It comes in 3 flavours:

 * `std::back_insert_iterator` - invokes the container's `push_back()` function.

   ```c++
   std::vector<int> container {};
   std::back_insert_iterator it { container };
   *it = 1;
   it++;
   *it = 2;
   it++;
   *it = 3;
   ```

 * `std::front_insert_iterator` - invokes the container's `push_front()` function.

   ```c++
   std::deque<int> container {};
   std::front_insert_iterator it { container };
   *it = 3;
   it++;
   *it = 2;
   it++;
   *it = 1;
   ```

 * `std::insert_iterator`- invokes the container's `insert()` function.

   ```c++
   std::deque<int> container { 1, 2, 3, 4, 5, 6, 7};
   std::insert_iterator it { container, container.begin() + 2 }; // start inserting at 2 elements down
   *it = 100;
   it++;
   *it = 101;
   it++;
   *it = 102;
   ```

```{note}
According to the book, these adapters ignore the increment operator because it isn't required for what's being done (insertion function calls to the wrapped container). Ignored parts are there because type traits for output iterator require them to be there.
```

```{note}
There are helper functions available for creating these. The function names are similar to the iterator adapter names: replace the `insert_iterator` part with `inserter` (e.g. `std::back_inserter()`).
```

### Move

`{bm} /(Library Functions\/Iterator Adapters\/Move)_TOPIC/`

```{seealso}
Core Language/Classes/Copying_TOPIC (refresher)
Core Language/Classes/Moving_TOPIC (refresher)
```

An iterator adaptor that wraps another iterator but modifies the dereferencing operator such that it returns an rvalue -- it forcefully moves the element. The typical use case for this is moving items from one container to another (as opposed to copying).

```c++
std::vector<MyMovableObject> container1 {};
container1.emplace_back(1, "morning");
container1.emplace_back(2, "midday");
container1.emplace_back(3, "evening");
// MOVE each item in container1 to container 2 (move semantics / move constructor)
std::vector<MyMovableObject> container2(
    std::move_iterator{ container1.begin() },
    std::move_iterator{ container1.end() }
);
```

```{note}
There is a helper function for creating this: `std::make_move_iterator()`.
```

### Reverse

`{bm} /(Library Functions\/Iterator Adapters\/Reverse)_TOPIC/`

An iterator adaptor that wraps another iterator but exposes it in reverse order -- last element to first element.

```c++
std::vector<int> container1 { 1, 2, 3, 4, 5, 6, 7, 8, 9 };
std::vector<MyMovableObject> container2(
    std::reverse_iterator{ container1.end() },
    std::reverse_iterator{ container1.begin() }
);
```

One important thing to note is that the first iterator being wrapped _must not be_ before the 2nd iterator being wrapped. If it were, it'd be undefined behaviour. 

```c++
if (it2 > it1)
std::vector<MyMovableObject> container2(  // THIS IS UNDEFINED BEHAVIOUR
    std::reverse_iterator{ container1.begin() },
    std::reverse_iterator{ container1.begin() + 2 }
);
```

```{note}
There is a helper function for creating this: `std::make_reverse_iterator()`.
```

```{note}
Most collections expose `rbegin()` / `rend()` functions that automatically give back a reverse iterator.
```

## Time

`{bm} /(Library Functions\/Time)_TOPIC/`

Similar to Java's `java.time` package, the C++ standard library offers several classes that represent various time-based constructs. This includes timestamps, durations, calendar representations, timezones, and various helper functions.

The subsections below document some common time-related classes and their usages.

### Timestamps

`{bm} /(Library Functions\/Time\/Timestamps)_TOPIC/`

Time points are classes that represent some point in type. They're typically created by clocks, which are classes that measure time. Each clock has a set of specifics:

| property     | description                                                                             |
|--------------|-----------------------------------------------------------------------------------------|
| Epoch        | When does it start from? (e.g. since boot, app launch, Jan 1, 1970 00:00:00 UTC, etc..) |
| Tick Period  | How often does it update? (e.g. once per millisecond)                                   |
| Monotonicity | Could it go back in time? (e.g. time returned is before a previous time returned)       |
| Leap Seconds | Does it include leap seconds?                                                           |

```{note}
Monotonicity is important. In certain cases the clock could go back in time (e.g. inaccurate clocks are a thing, leap seconds, updates from NTP server, etc..).
```

#### Clocks

`{bm} /(Library Functions\/Time\/Timestamps\/Clocks)_TOPIC/`

There are multiple types of clock. Each type of clock has the following set of important type traits that you can use to obtain key details about it:

 * `T::period` - Reports tick period of the clock in seconds (`std::ratio`)
 * `T::is_steady` - Reports monotonicity of the clock (`bool`).
 * `T::now()` - Get the current time (`std::chrono::time_point`).

```c++
std::cout << "Ticks per Second: " << std::chrono::system_clock::period::den << std::endl;
std::cout << "Monotonic:        " << std::chrono::system_clock::is_steady << std::endl;
std::chrono::time_point<std::chrono::system_clock> time { std::chrono::system_clock::now() };
```

Note how the `std::chrono::time_point` type returned by the clock above is templated to the clock's type. The return type of a clock's `now()` typically won't be able to intermingle with one returned by another type of clock. To do that, you need to use `std::chrono::clock_cast<SRC, DST>()` first to convert it.

```c++
auto sys_pt { std::chrono::system_clock::now() };
auto utc_pt { clock_cast<std::chrono::system_clock, std::chrono::utc_clock>(sys_pt) };
```

Common types of clock are listed below.

 * `std::chrono::system_clock`
 
   This clock is the system clock (e.g. wrist watch -- it tells you what time it is). Its epoch is whatever the epoch of the system's clock is (e.g. Jan 1, 1970 at midnight on most systems). Leap second inclusions are unspecified. 

   ```c++
   auto now { std::chrono::system_clock::now() };
   ```

 * `std::chrono::steady_clock`
 
   This clock is used to measure time intervals (e.g. stopwatch -- measure how long something takes). It's guaranteed to be monotonic, meaning each time you query it for the time it'll be greater than or equal to the result of your last query (e.g. `next_time >= prev_time`). Epoch is unspecified and leap second inclusions are unspecified.

   ```c++
   auto now { std::chrono::steady_clock::now() };
   ```

   ```{note}
   Would it make sense to include leap seconds here if this is a "stopwatch"? I don't think so, but nothing is mentioned about leap seconds when I look up the docs online.
   ```

 * `std::chrono::high_resolution_clock`
 
   This clock is guaranteed to have the shortest possible tick period available (e.g. gaming, real-time systems, etc..). Its epoch and leap second inclusions are unspecified.

   ```c++
   auto now { std::chrono::high_resolution_clock::now() };
   ```

   ```{note}
   Would it make sense to include leap seconds here if this is supposed to be used for high-precision timing? I don't think so, but nothing is mentioned about leap seconds when I look up the docs online.
   ```

 * `std::chrono::utc_clock` (Coordinated Universal Time)

   This clock is guaranteed to have an epoch of Jan 1, 1970 at midnight UTC and includes leap seconds.

   ```c++
   auto now { std::chrono::utc_clock::now() };
   auto ls_info { get_leap_second_info(now) };
   std::cout << ls_info.elapsed;       // leap seconds elapsed since epoch until time_point
   std::cout << ls_info.is_leap_second // did time_point fall on a leap second?
   ```

 * `std::chrono::tai_clock` (International Atomic Time)

   This clock is guaranteed to have an epoch of Dec 31, 1957 at 23:59:50 UTC and _does not_ include leap seconds.

   ```c++
   auto now { std::chrono::tai_clock::now() };
   ```

   ```{note}
   I'm not sure what the point of this clock is? Is it slowing down time / speeding up time based on the rate of "real" time vs atomic time?
   ```

 * `std::chrono::gps_clock` (Global Positioning System)

   This clock is guaranteed to have an epoch of Jan 6, 1980 at midnight UTC and _does not_ include leap seconds.

   ```c++
   auto now { std::chrono::gps_clock::now() };
   ```

   ```{note}
   I'm not sure what the point of this clock is? Is it slowing down time / speeding up time based on the rate of "real" time vs gps time? (e.g. GPS time is roughly ~38 microseconds faster per day)
   ```

 * `std::chrono::file_clock`

   This clock is used for file times (alias for `std::filesystem::file_time_type::clock`).  Its epoch and leap second inclusions are unspecified.

   ```c++
   auto now { std::chrono::gps_clock::now() };
   ```

Boost has a similar set of clocks: `boost::chrono::system_clock`, `boost::chrono::steady_clock`, `boost::chrono::high_resolution_clock`, `boost::chrono::process_cpu_clock`, etc... But, Boost clocks can't intermingle with clocks from the C++ standard library (e.g. `clock_cast()` won't work).

#### Conversions

`{bm} /(Library Functions\/Time\/Timestamps\/Conversions)_TOPIC/`

```{prereq}
Library Functions/Time/Timestamps/Clocks_TOPIC
Library Functions/Time/Date and Time_TOPIC
```

```{note}
Timezone functionality doesn't seem to be implemented as of clang or GCC as of yet, meaning the code below that uses timezones fails to compile.
```

To convert a time point from the system clock to a date and time representation, use `std::chrono::floor()` to cut out the relevant durations before using them to create the date and time objects...

```c++
// SOURCE: https://stackoverflow.com/a/15958113
using namespace std::chrono;

auto tp = system_clock::now();
auto tp_rounded = floor<days>(tp);
year_month_day ymd { tp_rounded };
hh_mm_ss time { floor<milliseconds>(tp - tp_rounded) };
```

The process is similar for converting a _zoned_ time point (time point associated with a timezone) ..

```c++
// SOURCE: https://stackoverflow.com/a/15958113
using namespace std::chrono;

auto tp = zoned_time{current_zone(), system_clock::now()}.get_local_time();
auto tp_rounded = floor<days>(tp_rounded);
year_month_day ymd {tp - tp_rounded};
hh_mm_ss time {floor<milliseconds>(tp-dp)};
```

To go the other way around (date and time objects to time point), use the `std::chrono::local_days` / `std::chrono::sys_days` aliases (they alias `std::chrono::time_point`).

```c++
using namespace std::literals::chrono_literals;

std::chrono::year_month_day date { January / 27d / 2022y };
std::chrono::hh_mm_ss time { 8h + 30m + 45s };

auto tp = std::chrono::local_days { date } + time;  // or use sys_days for system time
```

### Durations

`{bm} /(Library Functions\/Time\/Durations)_TOPIC/`

```{prereq}
Library Functions/Time/Timestamps/Clocks_TOPIC
```

```{seealso}
Core Language/Classes/User-defined Literals_TOPIC (variants are similar to unions but type-safe)
```

A duration is a class that represents some amount of time.

```c++
// use helper functions
auto hour { std::chrono::hours(1) };
auto hour { std::chrono::minutes(60) };
auto hour { std::chrono::seconds(3600) };
auto hour { std::chrono::milliseconds(3600000) };
auto hour { std::chrono::microseconds(3600000000) };
auto hour { std::chrono::nanoseconds(3600000000000) };

// use user-defined literals
using namespace std::literals::chrono_literals; // import the literals
auto hour { 1h };
auto hour { 60m };
auto hour { 3600s };
auto hour { 3600000ms };
auto hour { 3600000000us };
auto hour { 3600000000000ns };
```

Subtracting two time points produces the duration in between them.

```c++
auto before_tp { std::chrono::steady_clock::now() };
auto after_tp { std::chrono::steady_clock::now() };
std::chrono::duration d { after_tp - before_tp };
```

Similarly, adding a duration to a time point moves it accordingly.

```c++
auto before_tp { std::chrono::steady_clock::now() };
auto hour { std::chrono::hours(1) };
auto after_tp { before_tp + hour };  // move up by 1 hr
```

A duration object has a tick period. For example, `std::chrono::hours(1)` and `std::chrono::minutes(60)` both represent exactly 1 hour (equality operator (==) returns true), but the former has a tick period of 1 hour and the latter has a tick period if 1 minute. To get the number of ticks in a duration, use `count()`.

```c++
// NOTE if you're calling a method of a user-defined literal, you need a space before the dot
auto x {3600s .count()}; // x will be 3600
auto y {1h .count()};    // y will be 1
auto z {3600s == 1h};    // z will be true
```

```{note}
I've read online that you shouldn't use `count()` unless absolutely necessary because it breaks a lot of the abstraction / encapsulation that the library does.
```

`std::chrono::duration_cast<DST>` may be used to convert one type of duration to another.

```c++
auto x { std::chrono::duration_cast<std::chrono::seconds>(1h) };
auto y { std::chrono::duration_cast<std::chrono::hours>(3600s) };
auto xTicks { x.count() }; // xTicks will be 3600
auto yTicks { y.count() }; // xTicks will be 1
auto z { std::chrono::duration_cast<std::chrono::hours>(3599s) };
auto zTicks { z.count() }; // zTicks will be 0 (ROUNDS DOWN TO 0 -- not enough seconds for 1 hour)
```

### Date and Time

`{bm} /(Library Functions\/Time\/Date and Time)_TOPIC/`

```{prereq}
Library Functions/Time/Timestamps/Clocks_TOPIC
Library Functions/Time/Durations_TOPIC
```

Date and time functionality build on durations and time points by providing things like calendar representations, time of day representations (e.g. 12-hour vs 24-hour), timezone conversions, etc..

Calendar classes represent some exact region (e.g. 5th, 1st, last, etc..) of a specific calendar granularity (day, month, year, weekday).

|                                        | day | day of week | month | year | example                       |
|----------------------------------------|-----|-------------|-------|------|-------------------------------|
| `std::chrono::day`                     |  X  |             |       |      | 31                            |
| `std::chrono::weekday`                 |     |     X       |       |      | Tuesday                       |
| `std::chrono::weekday_indexed`         |     |     X       |       |      | 3rd Tuesday of unknown month  |
| `std::chrono::weekday_last`            |     |     X       |       |      | last weekday of unknown month |
| `std::chrono::month`                   |     |             |   X   |      | January                       |
| `std::chrono::month_day`               |  X  |             |   X   |      | December 25                   |
| `std::chrono::month_day_last`          |  X  |             |   X   |      | last day of January           |
| `std::chrono::month_weekday`           |     |     X       |   X   |      | 3rd Tuesday of January        |
| `std::chrono::month_weekday_last`      |     |     X       |   X   |      | last weekday of January       |
| `std::chrono::year`                    |     |             |       |  X   | 2022                          |
| `std::chrono::year_month`              |     |             |   X   |  X   | January 2022                  |
| `std::chrono::year_month_day`          |  X  |             |   X   |  X   | January 26, 2022              |
| `std::chrono::year_month_day_last`     |  X  |             |   X   |  X   | last day of January 2022      |
| `std::chrono::year_month_weekday`      |     |     X       |   X   |  X   | 3rd Tuesday of January        |
| `std::chrono::year_month_weekday_last` |     |     X       |   X   |  X   | last weekday of January 2022  |

```c++
// create jan 27 2022 as year_month_day
std::chrono::year y { 2022 };
std::chrono::month m { 1 };
std::chrono::day d { 27 };
std::chrono::year_month_day today { y, m, d };
```

Adding or subtracting a duration to a calendar object adjusts it accordingly.

```c++
std::chrono::year_month_day today { y, m, d };

using namespace std::literals::chrono_literals;
today += 5d;  // add 5 days to today
```

If the calendar class captures a full date (e.g. `year_month_day`, `year_month_weekday`, etc..), it's convertible to a time point via `std::chrono::local_days` / `std::chrono::sys_days`.

```c++
std::chrono::year y { 2022 };
std::chrono::month m { 1 };
std::chrono::day d { 27 };
std::chrono::year_month_day today { y, m, d };

std::chrono::local_days today_tp { today };
```

```{note}
Which should you use? I'm not sure of the difference. `std::chrono::sys_days` is shorthand for `std::chrono::time_point<std::chrono::system_clock, std::chrono::days>`, which is the time point type for the system clock. `std::chrono::local_days` expands to the same thing but for the local clock. I'm not sure what local clock actually is. It wasn't listed as one of the clocks.
```

Similarly, a time point is convertible to a full date calendar class.

```c++
auto sys_tp { std::chrono::system_clock::now() };
auto sys_tp_rounded { std::chrono::floor<std::chrono::days>(sys_tp) };  // round tp down to days
std::chrono::year_month_day ymd{ sys_tp_rounded };
```

```{note}
What type is `sys_tp_rounded`? It's `std::chrono::sys_days`, which is shorthand for `std::chrono::time_point<std::chrono::system_clock, std::chrono::days>`. The `std::chrono::year_month_day` constructor also accepts `std::chrono::local_days` -- I'm unsure which clock generates that (maybe utc clock?).
```

If two calendar objects both capture a full date but are of different types, you can still compare them by first converting them to time points.

```c++
// as year_month_day
std::chrono::year y { 2022 };
std::chrono::month m { 1 };
std::chrono::day d { 27 };
std::chrono::year_month_day today1 { y, m, d };
// as year_month_weekday
std::chrono::weekday thurs { 4 };
std::chrono::weekday_indexed _4th_thurs { thurs, 4 };
std::chrono::year_month_weekday today2 { y, m, _4th_thurs };
// convert both to time point
std::chrono::local_days today1_tp {today1};
std::chrono::local_days today2_tp {today2};
// compare -- they both represent the same date so they should be equal
auto sameDay { today1_tp == today2_tp }; // returns true
```

Calendar objects can be created more intuitively via a set of operator overloads, constants, and user-defined literals.

```c++
using namespace std::literals::chrono_literals;
using namespace std::chrono;

year_month_day today1 { January / 27d / 2022y };
year_month_weekday today2 { 2022y / January / Thursday[4] };
year_month_weekday_last today3 { 2022y / January / Thursday[last] };
// all 3 of the above represent the same date
```

The `std::chrono::hh_mm_ss` class is a container for the time that's elapsed since midnight (also known as time of day).

```c++
auto tp { std::chrono::system_clock::now() };
auto tp_rounded { std::chrono::floor<days>(tp) };
std::chrono::year_month_day ymd{ tp_rounded };

auto time_duration ( std::chrono::floor<milliseconds>(tp - tp_rounded) );
std::chrono::hh_mm_ss time{ time_duration };
// the variables below are of duration type
auto h { time.hours() };
auto m { time.minutes() };
auto s { time.seconds() };
auto ms { time.subseconds() };
```

Several time-related helper functions are provided to deal with 12-hour vs 24-hour time.

```c++
auto hour_of_day { time.hours() }; // using object from example above

auto am { std::chrono::is_am(hour_of_day) };
auto pm { std::chrono::is_pm(hour_of_day) };

auto hour_of_day_12 { std::chrono::make_12(hour_of_day) };        // as 12-hour format
auto hour_of_day_24 { std::chrono::make_12(hour_of_day_12, pm) }; // back to 24-hour format
```

```{note}
Timezone functionality doesn't seem to be implemented as of clang or GCC as of yet, meaning the code below fails to compile. It does seem to be implemented in MSVC though.
```

Timezones are accessible through a timezone database.

```c++
const auto my_tzdb = std::chrono::get_tzdb(); // also get_tzdb_list()

const std::chrono::time_zone* la_tz { my_tzdb.locate_zone("America/Los_Angeles") };
const std::chrono::time_zone* local_tz { my_tzdb.current_zone() };
```

You can apply a timezone to a time point, then convert it to the appropriate date and time objects.

```c++
// From https://stackoverflow.com/a/15958113
auto tp { std::chrono::system_clock::now() };
auto ztp { std::chrono::zoned_time {local_tz, tp}.get_local_time() };
auto ztp_rounded { std::chrono::floor<days>(ztp) };
std::chrono::year_month_day ymd { tp_rounded };
std::chrono::hh_mm_ss time { std::chrono::floor<milliseconds>(ztp - ztp_rounded) };
```

Similarly, you can construct a zoned time point from date and time details.

```c++
using namespace std::literals::chrono_literals;

std::chrono::year_month_day date { January / 27d / 2022y };
std::chrono::hh_mm_ss time { 8h + 30m + 45s };

auto tp { std::chrono::local_days { date } + time };  // or use sys_days for system time
```

## Numbers

`{bm} /(Library FunctionsTime\/Numbers)_TOPIC/`

Both the C++ standard library and third-party libraries (e.g. Boost) provide several pieces of functionality that make working with numbers easier: Math constants and functions, random number generation, bounds-checked numeric type casting, etc..

The subsections below document some common number-related classes and their usages.

### Random Numbers

`{bm} /(Library FunctionsTime\/Numbers\/Random Numbers)_TOPIC/`

There are several options for random number generation. For ...

 * non-cryptographic scenarios, use `std::mt19937_64`, an implementation of Mersenne Twister.
 * cryptographic scenarios, use `std::random_device`, which tries to use an unpredictable hardware source (but may not).

The classes are functors, where each invocation generates a random integral.

```c++
std::mt19937_64 mt_rand{ 12345 };  // seed value of 12345
std::cout << mt_rand() << std::endl;

std::random_device secure_rand {}; // doesn't take a seed
std::cout << secure_rand() << std::endl;
```

To have a random number generator return a distribution other than a normal distribution, you can use one of the distribution wrappers.

```c++
std::mt19937_64 rng{ 12345 };
std::uniform_int_distribution<int> uniform_dist{ 0, 10 };
auto value { uniform_dist(rng) };
```

 * `std::uniform_int_distribution`
 * `std::uniform_real_distribution` (like the above but for floating point types)
 * `std::normal_distribution` (a tweaked normal distribution)
 * etc..

Boost provides a set of distributions as well.

```{note}
Are there friendly wrappers here? What if I want the random number generator to give me a float, bool, or an alphanumeric string instead of an int?
```

### Numeric Type Information

`{bm} /(Library FunctionsTime\/Numbers\/Numeric Type Information)_TOPIC/`

Recall that C++'s numeric types are wishy-washy (e.g. there is no guarantee as to how large an `int` is, just that it must be greater than or equal to `short`). The `std::numeric_limits` class allows you to get compile-time information about a numeric type, such as signed-ness, min, max, etc..

```c++
auto a { std::numeric_limits<float>::is_integer };      // false
auto b { std::numeric_limits<uint16_t>::is_integer };   // true
auto c { std::numeric_limits<uint16_t>::has_infinity }; // false
```

 * `std::numeric_limits<T>::is_signed` - if the type is signed
 * `std::numeric_limits<T>::is_integer` - if the type is an integral
 * `std::numeric_limits<T>::has_infinity` - if the type supports infinity (e.g. floats do)
 * `std::numeric_limits<T>::has_quiet_NaN` - if the type can be set to not-a-number (e.g. IEEE floats can be set to not a number)
 * `std::numeric_limits<T>::round_style` - rounding mode for a type
 * `std::numeric_limits<T>::is_iec559` - if the type is an IEEE float.
 * `std::numeric_limits<T>::lowest()` - maximum negative value.
 * `std::numeric_limits<T>::max()` - maximum value.
 * `std::numeric_limits<T>::min()` - smallest representable value (different from `::lowest()`).
 * `std::numeric_limits<T>::quiet_NaN()` - get a not-a-number value.
 * etc..

Boost's Integer library also provides additional functionality for determining information about numerics (e.g. which one is the fastest for the platform you're on).

### Numeric Type Casting

`{bm} /(Library FunctionsTime\/Numbers\/Numeric Type Casting)_TOPIC/`

```{seealso}
(Core Language/Variables/Explicit Conversion/Named Conversions_TOPIC (refresher)
```

Typically, the named conversion function `static_cast` is used for converting from one numeric type to another (e.g. `double` to `int`). In most cases, `static_cast` is fine to use, however  certain scenarios require a more customizable form of conversion (e.g. don't allow overflow). More customizable forms of numeric conversions are possible via the class `boost::numeric::converter`.

To use `boost::numeric::converter`, two template parameters are required:

 1. `T` - (REQUIRED) output numeric type for the conversion.
 1. `S` - (REQUIRED) input numeric type for the conversion.

Either use its `convert()` function or invoke the class directly (it's a functor) to perform a conversion.

```c++
int x { boost::numeric::converter<int, double>::convert(1.234) };
int y { boost::numeric::converter<int, double>(1.234) };  // same thing as above
```

Several other optional template parameters control how the numeric conversion happens. For example, what to do on overflow (e.g. throw exception), how to round a float (e.g. round down), etc.. The most important thing to remember is that the default overflow configuration is to throw an exception -- either `boost::numeric::positive_overflow` or `boost::numeric::negative_overflow`.

```{note}
See [here](https://www.boost.org/doc/libs/1_33_1/libs/numeric/conversion/doc/converter.html) for all template parameters.
```

If the default conversion options are desirable, then an analog to `static_cast` called `boost::numeric_cast` may be used instead of `boost::numeric::converter`.

```c++
int z { boost::numeric_cast<int>(1.234) };  // same thing as the examples above
```

### Numeric String Conversion

`{bm} /(Library FunctionsTime\/Numbers\/Numeric String Conversion)_TOPIC/`

```{prereq}
Library Functions/Strings/String_TOPIC
Library Functions/Strings/Formatter_TOPIC
```

The appropriate way to convert to string is `std::formatter`. For quick-and-dirty conversions of numeric built-in types to `std::string` / `std::wstring`, use `std::to_string()` / `std::to_wstring()`. Other string types such as `std::u8string` aren't supported.

```c++
auto s { std::to_string(10) }; // int
auto s { std::to_string(10U) }; // unsigned int 
auto s { std::to_string(10L) }; // long
auto s { std::to_string(10UL) }; // unsigned long
auto s { std::to_string(10LL) }; // long long
auto s { std::to_string(10ULL) }; // unsigned long long
auto s { std::to_string(1.0f) }; // float
auto s { std::to_string(1.0) }; // double
auto s { std::to_string(1.0L) }; // long double
```

For quick-and-dirty conversions of `std::string` / `std::wstring` to built-in numeric types, use any of the `std::sto*()` functions. For integer types, it also takes in a base (defaults to base 10).

```c++
auto num { std::stoi(my_string) }; // int
// THERE IS NO sto*() FOR unsigned int -- use stoul() and cast to an unsigned int
auto num { std::stol(my_string) }; // long
auto num { std::stoul(my_string) }; // unsigned long
auto num { std::stoll(my_string) }; // long long
auto num { std::stoull(my_string) }; // unsigned long long
auto num { std::stof(my_string) }; // float
auto num { std::stod(my_string) }; // double
auto num { std::stold(my_string) }; // long double
```

```{note}
There is no equivalent or overloads for string specializations like `std::u8string`? How is someone supposed to convert those? The answer seems to be to use a third-party library (ICU might provide some functionality for this). It seems as if the C++20 standard still doesn't have full support for text encoding. Third-party libraries are required.
```

```{note}
`sto*()` functions also take in a pointer as a parameter, when finished, will be set to the pointer of the input string's `c_str()` just after the number. By default this parameter is set to `std::nullptr`, which means don't set it.
```

### Math

`{bm} /(Library FunctionsTime\/Numbers\/Math)_TOPIC/`

Several common math functions are provided directly within the C++ standard library.

| function(s)                                          | description                                                                                                         |
|------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|
| `abs(x)`                                             | absolute value                                                                                                      |
| `max(x) min(x)`                                      | minimum/maximum of two values                                                                                       |
| `isfinite(x) isinf(x)`                               | check if finite / infinite (e.g. floating point infinite)                                                           |
| `pow(x,y)`                                           | power of (x to the power of y)                                                                                      |
| `sqrt(x)`                                            | square root                                                                                                         |
| `cbrt(x)`                                            | cube root                                                                                                           |
| `sin(x) cos(x) tan(x) asin(x) acos(x) atan(x)`       | trigonometry functions                                                                                              |
| `sinh(x) cosh(x) tanh(x) asinh(x) acosh(x) atanh(x)` | hyperbolic functions                                                                                                |
| `ceil(x) floor(x) round(x)`                          | rounding function                                                                                                   |
| `div(x, y)`                                          | divides and gives both the quotient AND remainder                                                                   |
| `fmod(x, y)`                                         | modulo for floating point                                                                                           |
| `remainder(x, y)`                                    | signed remainder of x div y ([different from modulo for non-positive values](https://stackoverflow.com/a/13683709)) |
| `log(x) log10(x) log2(x)`                            | logarithm functions                                                                                                 |

Boost provides several math constants through `boost::math::double_constants`.

| constant | description                  |
|----------|------------------------------|
| `pi`     | archimedes's constant        |
| `e`      | euler's constant             |
| `degree` | number of radians per degree |
| `radian` | number of degrees per radian |

```{note}
The functions / constants listed above the useful ones. There are more.
```

In addition, there's support for complex numbers via `std::complex`, which implements various common complex number operations via operator overloading and free functions.

```c++
std::complex<double> a{1.0, 33.71};
auto aReal { std::real(a) };      // get real part
auto aImaginary { std::imag(a)} ; // get imaginary part
```

```{note}
This seems like such a niche thing that I don't think it's worth fleshing it out.
```

### Bitset

```{prereq}
Library Functions/Containers/Sequential/Array_TOPIC
```

`{bm} /(Library Functions\/Numbers\/Bitset)_TOPIC/`

`std::bitset` is a pseudo-container that wraps a fixed-size sequence of bits. It's similar to an `std::array<bool, N>` or `bool [N]`, but optimized for space and provides functions more appropriate for working with bits.

To create a `std::bitset` from an integral type, set the number of bits to capture as the template parameter. The constructor can optionally take in the integral value to initialize to (if not present, all sets initialized to 0).

```c++
std::bitset<4> b1 {};  // 4 bits, 0000
std::bitset<4> b2 {0b1011}; // 4 bits, 1011
```

```{seealso}
Core Language/Variables/Core Types/Integral_TOPIC (refresher on 0b prefix for integral literals specified as binary)
```

To create a `std::bitset` that's potentially larger than the largest available integral type, pass in an `std::string` of ones and zeros. Alternatively, you can use a custom character for the both ones and zeros by passing those characters into the constructor.

```c++
std::string str3 { "1011" };
std::bitset<4> b3 { str3 };
std::string str4 { "TFTT" };
std::bitset<4> b4 { str4, 0, str4.size(), 'T', 'F' };
```

```{note}
When working with `std::bitset`'s functions, bits are represented as a bool type. The value false is for 0 / true is for 1.
```

Operator overloads are available for all bitwise operators and their assignment operator equivalents.

```c++
auto b5 { b1 & b2 };  //AND
auto b6 { b1 | b2 };  // OR
auto b7 { b1 ^ b2 };  // XOR
auto b8 { ~b1 }; // NOT
auto b9 { b1 << 2 };  // shift-left
auto b10 { b1 >> 2 };  // shift-right
b1 &= b2;
b1 |= b2;
b1 ^= b2;
b1 <<= 2;
b1 >>= 2;
```

```{note}
I'm assuming if you're going to be using bitwise operators, the `set::bitset`s must be of the same size.
```

To read an individual bit as a bool, use either the subscript operator ([]) or `test()`. The difference is that `test()` provides bounds checking.

```c++
bool a = b1[1];
bool b = b1.test(1);
bool c = b1.test(999);  // throws std::out_of_range
```

To replace an individual bit as a bool, use either the subscript operator ([]) or `set()`. The difference is that `set()` provides bounds checking.

```c++
b1[1] = true;
b1.set(1, true)
b1.set(999, true)  // throws std::out_of_range
```

To set a single bit to 0, use `reset()`.

```c++
b1.reset(1);
```

To set all bits to 1, use `set()` without any arguments. Similarly, to set all bits to 0, use `reset()` without any arguments.

```c++
b1.set();  // sets all bits to true
b1.reset();  // sets all bits to false
```

To flip a single bit, use `flip()`. Don't specify an argument to flip all bits.

```c++
b1.flip(1);
b1.flip(); // flips all bits
```

To get the number of times 1 occurs in the sequence, use `count()`.

```c++
int d { b1.count() };
```

To test the sequence if ...

 * all bits are set to 1, use `all()`.
 * all bits are set to 0, use `none()`.
 * at least a single bit is set to 1, use `any()`.

```c++
bool e { b1.all() };
bool f { b1.none() };
bool g { b1.any() };
```

To get the size, use `size()`.

```c++
int len { b1.size() };
```

## Strings

`{bm} /(Library Functions\/Strings)_TOPIC/`

In addition to null-terminated character strings (e.g. `const char * = "hello world"`), the C++ standard library provides a higher-level character string abstractions. These higher-level abstractions provide more type safety, protect against common problems like buffer overflows, and generally make working with strings easier.

The subsections below document some common number-related classes and their usages.

```{note}
As of C++20, there is very little support for things like locale and character encodings. If you need need that type of functionality, check out the ICU library.
```

### String

`{bm} /(Library Functions\/Strings\/String)_TOPIC/`

```{prereq}
Library Functions/Allocators_TOPIC
Library Functions/Containers/Sequential/Vector_TOPIC
```

```{seealso}
Core Language/Variables/Core Types/Character String_TOPIC (refresher on C-style character strings)
```

`std::basic_string` is used as a wrapper for representing character strings. It's different from null-terminated character strings in that strings are resizable and manipulatable similarly to how they are in other high-level languages (e.g. Java or Python). Unlike other high-level languages, a C++ string _is not immutable_ (it's characters can change).

A `std::basic_string` supports all of the same functionality as a `std::vector` in addition to more. It takes 3 template parameters:

 1. `CharT` - type of character.
 2. `Traits` - type supporting a specific set of fields and methods for working with `CharT` (defaults to `std::char_traits<CharT>`).
 3. `Allocator` - type of custom allocator (defaults to `std::allocator<CharT>`).

Several template specializations are provided out-of-the-box for `std::basic_string`, one for each character type. In almost all cases, you'll want to use these template specializations rather than than using `std::basic_string`. The most common case for using `std::basic_string` directly is the need for a custom allocator, which isn't possible with template specializations.

| class            | character type |
|------------------|----------------|
| `std::string`    | `char`         |
| `std::wstring`   | `wchar_t`      |
| `std::u8string`  | `char8_t`      |
| `std::u16string` | `char16_t`     |
| `std::u32string` | `char32_t`     |

```{note}
The text and examples below use `std::string`, but they should work for the other template specializations as well. Make sure to use the correct literal for raw character string types (e.g. `u8"example"` for `char_8t`).
```

To create a `std::string` primed with a sequence of characters known as compile-time, use typical braced initialization. 

```c++
std::string s1 { 'h', 'e', 'l', 'l', 'o' };
```

To create a `std::string` without priming it directly to a sequence of characters, you can't use braced initialization or brace-plus-equals initialization. You must use parenthesis.

```c++
std::string s2("hello"); // create from null-terminated string
std::string s3("hello", 2); // create from first 2 chars of null-terminated string
std::string s4(10, 'a'); // create by repeating a 10 times
std::string s5(s1);  // create by copying s1
std::string s6(s1, 3);  // create by copying substring of s1 from index 3 until end
std::string s7(s1, 3, 2);  // create by copying 2 char long substring of s1 starting at index 3
std::string s8(s1.begin() + 3, s1.begin() + 5);  // create by copying substring of s1 from index 3 to 5
std::string s9(std::move(s1)); // create by moving s1 into s5
```

To append to a string, use either the addition operator (+) the assignment addition operator (+=), `push_back()`, or `append()`.

```c++
std::string s10 { s1 + s2 };
std::string s11 { s1 + "boop" };
std::string s12 { s1 };
s12 += s2;
s12.push_back('x');  // single character only
s12.append({ 'x', 'y', 'z' }); // append compile-time list
s12.append("xyz"); // append null-terminated string
s12.append(s1); // append s1
s12.append(s1, 3, 2); // append 2 char substring of s1 starting at index 3
s12.append(s1.begin() + 3, s1.begin() + 5);  // append substring of s1 from index 3 to 5
s12.append(10, 'a'); // append a 10 times
```

To insert at a specific position of a string, use `insert()`.

```c++
s1.insert(3, 5, 'X'); // insert X 5 times at index 3
s1.insert(3, "xyz"); // insert "xyz" at index 3
s1.insert(3, s2); // insert s2 at index 3
s1.insert(s1.begin() + 3, 5, 'X'); // insert X 5 times at iterator position
s1.insert(s1.begin() + 3, "xyz"); // insert "xyz" at iterator position
s1.insert(s1.begin() + 3, s2); // insert s2 at iterator position
```

To see if a string has a specific prefix or suffix with a string, use `starts_with()` and `ends_with()`.

```c++
s1.starts_with('h');
s1.starts_with("he");
s1.ends_with(s2);
```

To see if a string contains a specific substring, use `contains()`.

```c++
auto found { s1.contains("ell") };
auto found { s1.contains(s2) };
```

To find the position of a substring within a string, use `find()` or `rfind()`. The latter finds in reverse (from end to beginning). If the substring wasn't found, `std::string::npos` is returned.

```c++
// find
auto pos1 { s1.find("llo") };  // find index within s1 going FORWARD from index 0, or npos if not found
auto pos2 { s1.find("llo", 2) };  // find index within s1 going FORWARD from index 2, or npos if not found
auto pos3 { s1.find('l', 2) };  // find index within s1 going FORWARD from index 2, or npos if not found
// rfind
auto pos4 { s1.rfind("llo") };  // find index within s1 going BACKWARD from last index, or npos if not found
auto pos5 { s1.rfind("llo", 5) };  // find index within s1 going BACKWARD from index 5, or npos if not found
auto pos6 { s1.rfind('l', 5) };  // find index within s1 going BACKWARD from index 5, or npos if not found
```

To get a substring of a string, use `substr()`.

```c++
std::string s13 { s1.substr(3, 2) }; // create by copying 2 char long substring of s1 starting at index 3
std::string s14(s1, 3, 2);  // equivalent to the substr() above
```

To delete a specific position or range of a string, use either `pop_back()`, `clear()`, or `erase()`.

```c++
s1.pop_back(); // remove element from end
s1.clear(); // reset to empty string
s1.erase(1, 3); // remove 3 characters starting from index 1
s1.erase(s1.begin() + 1, s1.begin() + 5); // remove characters at index 1 to 5
s1.erase(s1.begin() + 1); // remove character at index 1
```

To replace a part of the string, use `replace()`, which takes in some position / range and another string to replace it with.

```c++
s1.replace(3, 2, "hello"); // replace 2 char substring of s1 starting at index 3 with hello
s1.replace(3, 2, "hello", 3, 2); // replace 2 char substring of s1 starting at index 3 with 2 char substring at index 3 of "hello"
s1.replace(3, 2, 10, 'a'); // replace 2 char substring of s1 starting at index 3 with a 10 times
s1.replace(s1.begin() + 1, s1.begin() + 5, "hello"); // replace characters at index 1 to 5 with hello
s1.replace(s1.begin() + 1, s1.begin() + 5, {'h', 'e', 'l', 'l', 'o'}); // replace characters at index 1 to 5 with hello
s1.replace(s1.begin() + 1, s1.begin() + 5, 10, 'a'); // replace characters at index 1 to 5 with a 10 times
```

```{note}
Need more elaborate string algorithms? Check out Boost's string functions.
```

To get the number of characters in a `std::string`, use either `size()`, `length()`, or `empty()`.

```c++
bool empty { s1.empty() }; // check if empty
auto len { s1.size() };
auto len { s1.length() }; // equivalent to size()
```

To test if two strings have the exact same sequence of characters, use the equality operator (==) and inequality operator (!=).

```c++
bool equal { s1 == s2 };
bool not_equal { s1 != s2 };
```

To test if a string is lexicographically less than the other, use the greater than operator (>) or less than operators (<).

```c++
bool less_than { s1 < s2 };
bool greater_than { s1 > s2 };
```

```{note}
Don't depend on this to sort alphabetically because it isn't portable. Lexicographically doesn't mean alphabetical, it just means that it compares by the symbol (character in this case). The comparisons depend on the encoding of the string. According to the book, for US-ASCII (most common), it means `A < Z < a < z`.
```

To access individual characters within a `std::string`, use either the subscript operator ([]), `at()`, `front()`, and `back()`. The behaviour of these functions is similar to their `std::vector` equivalents.

```c++
// WARNING: first() and last() have undefined behaviour if size is 0.
char first_char { s1.first(); }
char last_char { s1.last(); }

// WARNING: at() does bounds checking while the subscript operator does not.
char x { s1.at(2) };
char w { s1[2] };
char y { s1.at(1000) }; // throws std::out_of_range
char z { s1[1000] };    // out of bounds -- undefined behaviour
```

To access individual characters within `std::string` via a random access iterator, use the typical `begin()` and `end()` functions (and their variants).

 * `begin()` / `end()`
 * `cbegin()` / `cend()` - returns characters as `const`
 * `rbegin()` / `rend()` - returns characters in reverse
 * `crbegin()` / `crend()` - returns characters in reverse and as `const`

To access the underlying character data of a `std::string`, use either `data()` or `c_str()`. Both return a null-terminated string, but the latter is `const`.

```c++
char * data1 { s1.data() };
const char * data2 { s1.c_str() };
```

### String View

`{bm} /(Library Functions\/Strings\/String View)_TOPIC/`

```{prereq}
Library Functions/Strings/String_TOPIC
```

`std::basic_string_view` is a wrapper around a `std::basic_string` that represents some range of characters within the string. Similar to `std::basic_string`, `std::basic_string_view` has several out-of-the-box template specializations for each character type.

| class                 | character type |
|-----------------------|----------------|
| `std::string_view`    | `char`         |
| `std::wstring_view`   | `wchar_t`      |
| `std::u8string_view`  | `char8_t`      |
| `std::u16string_view` | `char16_t`     |
| `std::u32string_view` | `char32_t`     |

`std::basic_string_view` works by holding on to the underlying string as a pointer, meaning that it's efficient but unsafe. Specifically, it has the _potential for a memory leak_: If the underlying string gets destroyed, the view pointing to it will be pointing at bad data.

`std::basic_string_view` (and its specializations) support most of the same functions as `std::basic_string` (and its specializations).

```{note}
The text and examples below use `std::string_view`, but they should work for the other template specializations as well.
```

```c++
std::string_view sv1 { s1, 4 };  // view of first 4 characters of s1
std::string_view sv2 { s1 };  // view of s1
std::string_view sv3 {};  // view of an empty string
std::string_view sv4 { "hello" };  // view of the constant C-string hello
```

### Formatter

`{bm} /(Library Functions\/Strings\/Formatter)_TOPIC/`

```{prereq}
Library Functions/Strings/String_TOPIC
Library Functions/Strings/String View_TOPIC
Library Functions/Time_TOPIC (briefly mentioned below)
```

```{note}
This is from a C++ library called fmt which formats strings (similar to Python format strings). It's been included into the C++ standard library as of C++20, which is the version this section references.
```

`std::format` is a string formatting class that provides functionality very similar to Python's string formatting. Unlike older formatting systems like `sprintf()`, it's ...

* type-safe in that doesn't require you to know the type of varargs beforehand.
* safe in that it avoids buffer overflows by using C++ strings (`std::string`) rather than null-terminated character strings (`char *`).
* extendable in that it's easy to support custom types for the formatter.

```{note}
Much of this functionality is also available in C++ IO streams, but this is vastly simpler to use.
```

```c++
std::format("Hello {}, it's {} degrees outside.", "steven", 42);  // Hello steven, it's 42 degrees outside
std::format("Here's a number: {0}. Here's that same number again: {0}.", 42); // Here's a number: 42. Here's that same number again: 42.
std::format("{0:x>10} {0:x<10}", 42);  // xxxxxxxx42 42xxxxxxxx
```

The formatting of a parameter is controlled by what's inside of the curly brackets for that parameter. At a minimum, it's is empty (e.g. 1st example above). If it should target a specific argument, it needs to take in the index of that parameter (e.g. 2nd example above). Then, any output options for a specific parameter are specified by inserting a colon followed by those options (e.g. 3rd example above).

Examples of the most common formatting options are provided below.

* Padding and alignment

  ```c++
  std::format("{:10}", 42);   // "        42"
  std::format("{:<10}", 42);  // "42        "
  std::format("{:>10}", 42);  // "        42"
  std::format("{:^10}", 42);  // "    42    "
  std::format("{:x^10}", 42); // "xxxx42xxxx"
  ```

* Number signs (e.g. should plus sign be put on a positive integer)

  ```c++
  std::format("{0:},{0:+},{0:-},{0: }", 1);   // "1,+1,1, 1"
  std::format("{0:},{0:+},{0:-},{0: }", -1);  // "-1,-1,-1,-1"
  ```

* Number precision (e.g. where to truncate floating point)

  ```c++
  std::format("{:.5f}", 3.14);      // "3.14000"
  std::format("{:0>10.5f}", 3.14);  // "0003.14000"
  ```

* Numeric encoding (e.g. decimal, hex, octal)

  ```c++
  std::format("{:d}", 10);     // "10"
  std::format("{:x}", 10);     // "a"
  std::format("{:#x}", 10);    // "0xa"
  std::format("{:#X}", 10);    // "0xA"
  std::format("{:#04X}", 10);  // "0x0A"
  std::format("{:o}", 10);     // "12"
  std::format("{:#o}", 10);    // "012"
  std::format("{:b}", 10);     // "1010"
  std::format("{:#b}", 10);    // "0b1010"
  ```

`std::format` provides support for many common parameter types: numbers (e.g. integral and floating point), pointers, single characters, character strings (e.g. null-terminated strings, C++ strings, and C++ string views), dates, times, durations, timezones, etc.. To add support for a new type, that type needs a `std:formatter` template specialization (note the "er" at the end -- formatter, not format).

The simplest approach to implement a template specialization for a custom type is to inherit from an existing template specialization. Formatting options are typically ignored in this case.

```c++
template <>
struct std::formatter<Person> : std::formatter<std::string> {
    auto format(Person s, format_context& ctx) {
        return format_to(ctx.out(), "{} {}", s.firstName, s.lastName);
    }
};

Person p { "steve", "smith" };
std::format("Hello {}, the temperature today is {}!", p, 42);
```

To support formatting options, an extra function needs to be implemented (`parse()`) which sets member variables based on the options it sees.

```c++
// For a better example, see https://www.modernescpp.com/index.php/extend-std-format-in-c-20-for-user-defined-types
template <>
struct std::formatter<Person> {
    int space_count;

    auto parse(format_parse_context& ctx) {
        std::string val {};
        for (auto it { begin(ctx) }; it != end(ctx); ++it) {
            char c { *it };
            if (c == '}') {
                space_count = std::stoi(val);
                return it;
            } else {
                val += c;
            }
        }
        return end(ctx);
    }

    auto format(Person s, format_context& ctx) {
        std::string spacer(space_count, ' ');
        return format_to(ctx.out(), "{}{}{}", s.firstName, spacer, s.lastName);
    }
};

Person p { "steve", "smith" };
std::format("Hello {:1}, the temperature today is {}!", p, 42);
```

### Regular Expressions

`{bm} /(Library Functions\/Strings\/Regular Expressions)_TOPIC/`

```{prereq}
Library Functions/Strings/String_TOPIC
```

`std::basic_regex` is a templated class for regular expression functionality. Similar to `std::basic_string`, `std::basic_regex` has several out-of-the-box template specializations for specific character types (not all character types).

| class           | character type |
|-----------------|----------------|
| `std::regex`    | `char`         |
| `std::wregex`   | `wchar_t`      |

```{note}
What about other character types (e.g. `char8_t`)? Not supported because encoding support in C++ is not really there as of C++20. So what encoding is used here? Platform-specific maybe? or ASCII? It's probably stated somewhere but I have yet to find out what it is. On most major platforms, it's probably safe to assume that basic printable ASCII characters are there encoded as they would be in ASCII.
```

```{note}
The text and examples below use `std::regex`, but they should work for the other template specializations as well.
```

```{seealso}
Core Language/Variables/Core Types/Character String_TOPIC (refresher on raw string literals)
```

To create a `std::regex`, prime it with a specific regex pattern and optionally regex flags. Unless the pattern string is presented as an initializer list argument, you can't use braced initialization or brace-plus-equals initialization. You must use parenthesis.

```c++
std::regex pattern1 { '\\', 'd', '+' };  // initializer list of pattern.
std::regex pattern2(R"|\d+|");
std::regex pattern3(R"|\d+|", std::regex_constants::ECMAScript);  // equivalent to above
std::regex pattern4(R"|\d+|", std::regex_constants::ECMAScript | std::regex_constants::icase);
```

To get the regex flags, use `flags()`. To get the number of groups (sub-expressions), use `mark_count()`.

```c++
auto flags { pattern1.flags() };
auto group_count { pattern1.mark_count() };
```

To search a string for a pattern, use either `std::regex_match()` or `std::regex_search()`. Both have the same set of parameters, but the former requires the entire string to match the pattern while the latter searches the string for a substring that matches the pattern. Parameter number ...

 1. (required) is the string being searched.
    * can be `std::string`.
    * can be `const char *`.
    * can be range between iterator positions.
 2. (optional) is a reference to `std::match_results` where match results go (templated class).
    * if parameter 1 is of type `std::string`, use template specialization `std::smatch`.
    * if parameter 1 is of type `std::wstring`, use template specialization `std::wmatch`.
    * if parameter 1 is of type `const char *`, use template specialization `std::cmatch`.
    * if parameter 1 is of type `const wchar_t *`, use template specialization `std::wcmatch`.
 3. (required) is the pattern to search for.
 4. (optional) is the match flags (optional -- this specifies matching behaviour such as how you should treat EOL)

```{note}
There are lots more specializations for parameter 2. See [here](https://en.cppreference.com/w/cpp/regex/match_results) for more information.
```

```c++
std::string("hello steven");
std::regex pattern5(R"|hello (.*+)|");
std::smatch result;
bool matched { std::regex_match(s1, result, pattern5, std::regex_constants::match_default) };
// matched contains true if the pattern matched the string
// result contains information about the match (e.g. what parts of the string matched which sub-expressions) -- see cppreference for more info
```

```{note}}
If using `std::regex_search()`, you can continue searching the string by extracting the end position of the search from the match result and running the search again from that position.
```

To search a string for a pattern and replace it, use `std::replace()`. Similar to `std::regex_match()` and `std::regex_search()`, this also has a flag argument (same type and default) that defines how replacement happens (e.g. `$1` to replace with capture group 1).

```c++
std::regex pattern6(R"|hello (.*+)|");
std::string res = std::regex_replace("hello steven", pattern6, "goodbye $1");
// res should be "goodbye steven"
```

## Streams

`{bm} /(Library Functions\/Streams)_TOPIC/`

```{prereq}
Library Functions/Containers/Sequential/Array_TOPIC
```

Similar to Java's `InputStream` and `OutputStream` interfaces (and surrounding utilities and packages), the C++ standard library offers several stream classes and interfaces. Similar to `std::basic_string`, a set of templated classes are provided for streams.

 * `std::basic_ostream` is the equivalent of Java's `OutputStream`.
 * `std::basic_istream` is the equivalent of Java's `InputStream`.
 * `std::basic_iostream` is a combination of the above two.

Each of the classes above requires two template parameters: element type of the stream (e.g. is it streaming `char`s, `int`s, a custom type, etc..) and a class that describes the element type's traits (e.g. similar to the `std::basic_string`'s character traits type). Template specializations are provided for some commonly used element types (e.g. `char` and `wchar_t`).

| base stream type      | element type | specialized stream type |
|-----------------------|--------------|-------------------------|
| `std::basic_ostream`  | `char`       | `std::istream`          |
| `std::basic_istream`  | `char`       | `std::ostream`          |
| `std::basic_iostream` | `char`       | `std::iostream`         |
| `std::basic_ostream`  | `wchar_t`    | `std::wistream`         |
| `std::basic_istream`  | `wchar_t`    | `std::wostream`         |
| `std::basic_iostream` | `wchar_t`    | `std::wiostream`        |

You typically won't need to implement your own stream types. The C++ standard library provides stream implementations for common use-cases such as reading/writing to the console and files. The subsections below document these implementations, while the remainder of this section discusses the stream API.

```{note}
The rest of this section talks about the general functionality of streams using `std::cout` for an output stream / `std::cin` for an input stream. These are for writing to / reading from the console, which is documented further in one of the subsections. For now just assume they exist.
```

```{seealso}
Core Language/Classes/Operator Overloading_TOPIC (refresher)
```

To read and write text, operator overloads are provided called formatted operations: The left-shift operator (<<) is for writing while the right-shift operator (>>) is for reading. Each operator overload takes in the type to write/read and returns a reference back to the stream itself, allowing for chaining.

```c++
std::cout << 5 << ' ' << "hello world";
int x {};
int y {};
std::cin >> x >> y;
```

By default, the C++ standard library provides operator overloads for most built-in types (e.g. `int`, `long`, etc.. ) as well as some higher-level types within the C++ standard library strings (e.g. `std::string`, `std::complex`, etc..). To provide support for custom types, simply overload the operators for that type.

```c++
struct MyType {
    int intValue;
    long longValue;
}
std::ostream& operator<<(std::ostream& s, const MyType& val) {
    return s << val.intValue << val.longValue;
}
std::istream& operator>>(std::istream& s, MyType& val) {
    s >> val.intValue;
    s >> val.longValue;
    return s;
}
```

Special objects called manipulators may be used to to modify how a stream interprets formatted operations.

 * `std::ws` skips over all whitespace in the input.
 * `std::flush` flushes any buffered output.
 * `std::ends` writes a null byte (e.g. 0).
 * `std::endl` writes a newline character and flushes.
 * `std::boolalpha` tells the stream to write/read booleans as text rather than 0/1.
 * `std::noboolalpha` tells the stream to write/read booleans as 0/1 rather than text.
 * `std::oct` tells the stream to write/read integrals as octal.
 * `std::dec` tells the stream to write/read integrals as decimal.
 * `std::hex` tells the stream to write/read integrals as hexidecimal.
 * `std::setprecision(p)` tells the stream to write/read floating point at a specific precision.
 * `std::fixed` tells the stream to write/read floating point in fixed notation.
 * `std::scientific` tells the stream to write/read floating point in scientific notation.

```c++
std::cin >> std::ws >> x;  // skip over whitespace and read into variable

std::cout << "hello" << std::flush; // writes string and forces buffer to flush
std::cout << "hello" << std::ends;  // writes string followed by null character
std::cout << "hello" << std::endl;  // writes string followed by new-line character AND forces buffer to flush

std::cout << std::boolalpha << true;   // writes true
std::cout << std::noboolalpha << true; // writes 1
std::cin >> std::boolalpha >> b_var;   // reads true/false into boolean variable
std::cin >> std::noboolalpha >> b_var; // writes 0/1 into boolean variable

std::cout << std::oct << 10 << st::dec << 10 << std::hex << 10;            // writes 10 as octal, decimal, and hex
std::cin >> std::oct >> i_var1 >> st::dec >> i_var2 >> std::hex >> i_var3; // reads integral as octal, decimal, and hex

std::cout << std::setprecision(2) << 3.14159; // writes 3.14
std::cout << std::fixed << 0.1;               // writes 0.100000
std::cout << std::scientific << 0.1;          // writes 1.000000e-01
```

```{seealso}
Core Language/Variables/Implicit Conversion_TOPIC (refresher)
```

At any point, a stream may end or enter into a bad state. A set of member functions can be used to query the state.

 * `good()` returns true if the stream is in a good state.
 * `eof()` returns true if the stream has ended.
 * `fail()` returns true if the last operation failed (but the stream may still be usable).
 * `bad()` returns true if the stream is in an unrecoverable state.

```{note}
At any point, you can call `clear()` to reset the state to good. Why would you ever want to do this?
```

In addition, `exceptions()` can be used to make the stream throw an exception if it enters into one (or more) of the states listed above. 

```c++
std::cin.exceptions(std::istream::badbit | std::istream::failbit); // exception if bad/fail, but not good/eof
```

Streams provide an implicit type conversion for `bool` that gives back the result of `good()`, allowing for shorthand testing of the stream state.

```c++
// keep reading characters until the stream breaks or eof
while (std::cin) {
    char ch {};
    std::cin >> ch;
    process(ch);
}
```

To read non-text data, a set of member functions referred to as unformatted operations are available.

To read non-text data, use `get()`, `peek()`, `getline()`, `read()`, `readsome()`, and `ignore()`. `gcount()` may be used to determine exactly how many characters were read in one of these functions (e.g. may have terminated early because it hit end-of-file or a new-line character).

```c++
char ch {};
std:array<char, 100> arr {};

ch = std::cin.peek(); // read single character WITHOUT moving forward in  the stream
ch = std::cin.get();  // read single character
std::cin.get(ch);     // read single character
std::cin.get(arr, 100);           // read 100 characters OR until \n (\n included in arr)
std::cin.get(arr, 100, ';');      // read 100 characters OR until ;  (; included in arr)
std::cin.getline(arr, 100);       // read 100 characters OR until \n (\n DISCARDED)
std::cin.getline(arr, 100, ';');  // read 100 characters OR until ;  (; DISCARDED)
std::cin.read(arr, 100);          // read 100 characters
std::cin.readsome(arr, 100);      // read 100 characters or however many are "immediately available"
std::cin.ignore();        // skip single char
std::cin.ignore(5);       // skip 5 chars
std::cin.ignore(5, '\n'); // skip up to 5 chars, stopping if \n is encountered (stops AFTER skipping \n)

auto count { std::cin.gcount() };
```

```{note}
`readsome()` is a little more dicey in that how it works is implementation specific.
```

To write non-text data, use `put()` and `write()`. For buffered streams, the buffer may be explicitly flushed by `flush()`.

```c++
std::cout.put('x');         // write single character
std::cout.put("hello", 5);  // write 5 characters
std::cout.flush();
```

To get and move the position of the underlying stream, use `tell*()` and `seek*()` respectively. The suffix depends on the type of stream:

 * input streams use `tellg()` / `seekg()`
 * output streams use `tellp()` / `seekp()`
 * input output streams use `tell()` / `seek()`

```c++
// NOTE: not supported on all stream types
auto pos { std::cin.tellg() };
```

### String

`{bm} /(Library Functions\/Streams\/String)_TOPIC/`

```{prereq}
Library Functions/Strings/String_TOPIC
Library Functions/Strings/String View_TOPIC
```

String streams are equivalent to Java's `ByteArrayInputStream` / `StringReader` and `ByteArrayOutputStream` / `StringWriter`. The underlying types for string streams are ...

* `std::basic_istringstream` for input string stream.
* `std::basic_ostringstream` for output string stream.
* `std::basic_stringstream` for both input and output string stream.

The above types are templated classes, where the template parameters specify element type, element traits, and a custom allocator. The following template specializations are provided out-of the box...

| type                  | element type |
|-----------------------|--------------|
| `std::ostringstream`  | `char`       |
| `std::wostringstream` | `wchar_t`    |
| `std::istringstream`  | `char`       |
| `std::wistringstream` | `wchar_t`    |
| `std::stringstream`   | `char`       |
| `std::wstringstream`  | `wchar_t`    |

```{note}
The text and examples below use `std::ostringstream` / `std::istringstream`, but they should work for the other template specializations as well. Make sure to use the correct literal for raw character string types (e.g. `u8"example"` for `char_8t`).
```

For output string streams, in addition to all of the normal output stream functionality, ...

 * `str()` returns a copy of the internal buffer as a `std::string`.
 * `view()` returns a view to the internal buffer as a `std::string_view`.

```c++
std::ostringstream out {};
out << 3 << "hello!" << std::endl;
std::string output { out.str() };
std::string_view view { out.view() };
```

Input string streams have the same two methods, but they're hardly used because the main point of input string streams is to parse data out of the stream.

```c++
std::istringstream in { "1 9.555555" };
int x;
double y;
in >> x >> y;
```

### File

`{bm} /(Library Functions\/Streams\/File)_TOPIC/`

File streams are equivalent to Java's `FileInputStream` and `FileOutputStream`. The underlying types for string stream are ...

* `std::basic_ifstream` for input string streams.
* `std::basic_ofstream` for output string streams.
* `std::basic_fstream` for both input and output string stream.

The above types are templated classes, where the template parameters specify element type, element traits, and a custom allocator. The following template specializations are provided out-of the box...

| type             | element type |
|------------------|--------------|
| `std::ofstream`  | `char`       |
| `std::wofstream` | `wchar_t`    |
| `std::ifstream`  | `char`       |
| `std::wifstream` | `wchar_t`    |
| `std::fstream`   | `char`       |

```{note}
The text and examples below use `std::ofstream` / `std::ifstream`, but they should work for the other template specializations as well. Make sure to use the correct literal for raw character string types (e.g. `u8"example"` for `char_8t`).
```

To access a file, either pass that file's path to the constructor or to `open()` along with the set of file access flags. Those flags are ...

 * `std::ios::in` - file must exist.
 * `std::ios::out` - file created if it doesn't exist.
 * `std::ios::app` - file created if it doesn't exist AND writes go to the end of the file.
 * `std::ios::trunc` - file contents discarded.
 * `std::ios::binary` - if set, no implicit text manipulations are performed on the file (e.g. replacing `\n` with `\r\n` or vice-versa).

```c++
std::fstream f1 { "/path/to/file.txt", std::ios::in | std::ios::trunc }; // file must exist AND truncate it
std::fstream f2 {};
f2.open("/path/to/file.txt", std::ios::in | std::ios::trunc); // same open operation as f1
```

To close a file, use `close()` or call the stream object's destructor by destroying it.

```c++
f1.close();
```


To check if the stream has a file open, use `is_open()`.

```c++
bool open { f1.is_open() };
```

To read and write, the standard stream mechanisms are available: formatted operations and unformatted operations.

```c++
// write
f1 << 3 << "hello!" << std::endl; // write
// read
int x;
double y;
f1 >> x >> y;
```

To get and set the position, the standard stream mechanisms are available: `seek*()` and `tell*()`

```c++
f1.seek(500);
auto pos { f1.tell() };
```

To handle IO errors, the standard stream mechanisms are available: `exceptions()` to throw exceptions or explicitly check flags (e.g. invoke `good()`).

```c++
f1.exceptions(std::istream::badbit | std::istream::failbit); // exception if bad/fail, but not good/eof
```

### Global

`{bm} /(Library Functions\/Streams\/Global)_TOPIC/`

For console access, global streams provides access to standard input, standard output, and standard error. Global streams are presented to the user as global variables.

| channel        | element type | global variable |
|----------------|--------------|-----------------|
| standard in    | `char`       | `std::cin`      |
| standard out   | `char`       | `std::cout`     |
| standard error | `char`       | `std::cerr`     |
| standard in    | `wchar_t`    | `std::wcin`     |
| standard out   | `wchar_t`    | `std::wcout`    |
| standard error | `wchar_t`    | `std::wcerr`    |

```{note}
The text and examples below use `std::cout` / `std::cin` / `std::cerr`, but they should work for the other template specializations as well. Make sure to use the correct literal for raw character string types (e.g. `u8"example"` for `char_8t`).
```

To read and write, the standard stream mechanisms are available: formatted operations and unformatted operations.

```c++
// write
std::cout << 3 << "hello!" << std::endl; // write
// read
int x;
double y;
std::cin >> x >> y;
```

To handle IO errors, the standard stream mechanisms are available: `exceptions()` to throw exceptions or explicitly check flags (e.g. invoke `good()`).

```c++
std::cin.exceptions(std::istream::badbit | std::istream::failbit); // exception if bad/fail, but not good/eof
```

## Ranges

`{bm} /(Library Functions\/Ranges)_TOPIC/`

```{prereq}
Library Functions/Containers_TOPIC
Library Functions/Utility Wrappers/Tuple_TOPIC
```

The C++ standard library provides an functionality similar to Java streams, called ranges. Like Java streams, ranges enable functional programming in that a range can be fed into a chain of higher-level operations that manipulate the stream of elements within, lazily if possible.

```c++
// The code below prints the numbers 2 and 4. The Java streams equivalent is provided on the right-hand side.
//
//           C++                                           vs                 JAVA
std::vector<int> v{ 0, 1, 2 };                                  // var v = ArrayList<Integer>();
                                                                // v.add(0);
                                                                // v.add(1);
                                                                // v.add(2);
                                                                //
auto range {                                                    // var range =
    v                                                           //          v.stream()
    | std::views::transform([](int x) { return x * 2; })        //         .map(e -> e * 2)
    | std::views::filter([](int x) { return x != 0; })          //         .filter(e -> e != 0);
};                                                              //
for (int e : range) {                                           // range.forEach(e -> { System.out.println(e); } );
    std::cout << e << std::endl;                                //
}                                                               //
```

As shown in the example above, ranges work similarly to Java streams. Operations are chained together using the pipe operator (|), where those operations are applied from left-to-right. 

```{note}
**WARNING**: Once `v` above gets destroyed (e.g. goes out of scope), `range` becomes invalid. `v` is _referenced_ by `range`, it isn't _copied_ / _moved_ into `range`. See the subsection on owning views to workaround this problem.
```

```{note}
Unlike Java streams, the current implementation of ranges (C++20) are missing some major functionality:

* type-erasures (e.g. `std::vector<int> {0, 1, 2} | std::views::transform([](int x) { return x * 2; })` and `std::vector<int> {0, 1, 2} | std::views::filter([](int x) { return x != 0; })` don't have the same type)
* parallel algorithms (e.g. transform using multiple cores)
* actions (e.g. missing things like `forEach()` in Java streams)
```

Any object that has a particular set of type traits is a range. Those type traits map closely to iterator type traits: A range must have implementation for `std::begin(R)` and `std::end(R)` functions, and usage patterns similar to that of the type of iterator it maps to:

 * input range has usage patterns similar to input iterator.
 * output range has usage patterns similar to output iterator.
 * forward range has usage patterns similar to forward iterator.
 * bidirectional range has usage patterns similar to bidirectional iterator.
 * random access range has usage patterns similar to random access iterator.
 * contiguous range has usage patterns similar to contiguous iterator.

One major difference between iterators and ranges is that a range's `end()` function doesn't necessarily have to return the same type as its `begin()` function. It can instead return a sentinel type that marks the end of the range. If a range does return the same type for both `begin()` and `end()`, it's referred to as a common range. Containers in the C++ standard library are all of common ranges. However, once a container gets piped into an operation, it may end up not being a common range.

```{note}
See `std::views::common()` below. It wraps a view and makes it so that `begin()` and `end()` have a common return type.
```

| container                 | range type          |
|---------------------------|---------------------|
| `std::unordered_set`      | input range         |
| `std::unordered_map`      | input range         |
| `std::unordered_multiset` | input range         |
| `std::unordered_multimap` | input range         |
| `std::forward_list`       | input range         |
| `std::set`                | output range        |
| `std::map`                | output range        |
| `std::multiset`           | output range        |
| `std::multimap`           | output range        |
| `std::list`               | output range        |
| `std::deque`              | bidirectional range |
| `std::array`              | contiguous range    |
| `std::vector`             | contiguous range    |

```{note}
`std::string` and other types of string variants, while not containers, are contiguous ranges.
```

When an operation such as transformation or filtering is applied on a range, it's applied through a view. A view is a special type of range that typically doesn't own any data and typically isn't mutable / is state-less. As such, a view typically has constant-time copy, move, and assignment.

| view                     | example                                                    | description                                                                 |
|--------------------------|------------------------------------------------------------|-----------------------------------------------------------------------------|
| `std::views::filter`     | `v \| std::views::filter([](int x) { return x != 0; }`     | keep elements that pass predicate                                           |
| `std::views::transform`  | `v \| std::views::transform([](int x) { return x * 2; }`   | modify elements                                                             |
| `std::views::take`       | `v \| std::views::take(5)`                                 | keep first n elements                                                       |
| `std::views::take_while` | `v \| std::views::take_while([](int x) { return x != 0; }` | keep elements until predicate fails                                         |
| `std::views::drop`       | `v \| std::views::drop(5)`                                 | skip first n elements                                                       |
| `std::views::drop_while` | `v \| std::views::drop_while([](int x) { return x == 0; }` | skip elements until predicate fails                                         |
| `std::views::join`       | `v \| std::views::join`                                    | flatten a range of ranges (2D) into a range (1D)                            |
| `std::views::join_with`  | `v \| std::views::join_with(-1)`                           | flatten a range of ranges (2D) into a range (1D) with delimiters in between |
| `std::views::split`      | `v \| std::views::split(-1)`                               | split a range into a range of ranges using a delimiter                      |
| `std::views::lazy_split` | `v \| std::views::lazy_split(-1)`                          | split a range into a range of ranges using a delimiter (lazily)             |
| `std::views::counted`    | `std::views::counted(v.begin(), 5)`                        | keep a sub-range of a range                                                 |
| `std::views::common`     | `std::views::common(v)`                                    | convert to a common view (`being()` and `end()` have same type)             |
| `std::views::reverse`    | `v \| std::views::reverse`                                 | reverse a view                                                              |
| `std::views::elements`   | `v \| std::views::elements<1>`                             | transform tuples to their nth item                                          |
| `std::views::keys`       | `v \| std::views::keys`                                    | transform pairs to their 1st item                                           |
| `std::views::values`     | `v \| std::views::values`                                  | transform pairs to their 2nd item                                           |
| `std::views::zip`        | `std::views::zip(v1, v2, v3)`                              | zip multiple ranges together (similar to Python's `zip()`)                  |

In addition to performing operations on another range's elements, a view may originate elements itself.

| view                  | example                              | description                            |
|-----------------------|--------------------------------------|----------------------------------------|
| `std::views::empty`   | `std::views::empty<int>`             | empty range of some type               |
| `std::views::single`  | `std::views::single<int> { 5 }`      | range of a single element              |
| `std::views::iota`    | `std::views::iota(1, 5)`             | range of incrementing values (bounded) |

```{note}
The tables above aren't exhaustive.
```

### Concepts

`{bm} /(Library Functions\/Ranges\/Concepts)_TOPIC/`

At it's core, a range must satisfy the concept_TEMPLATE `std::ranges::range`, which only asks that the type have an implementation for the functions `std::ranges::begin(R)` and `std::ranges::end(R)`. There are two concept_TEMPLATE specializations:

 * `std::ranges::sized_range`: A range type that has an implementation for `std::ranges::size(R)`, which returns the number of elements within the range. 
 * `std::ranges::borrowed_range`: A range type that provides a template specialization for `std::ranges::enable_borrowed_range<R>`, which signals that the range type guarantees that the iterators it returns aren't bound to the lifetime of the range. Borrowed ranges are commonly generate elements on-the-fly.
 * `std::ranges::view`: A range type with constant-time copy/move/assignment operations and provides a template specialization for `std::enable_view<R>`, which signals that the range type is a view. Views are commonly used to transform elements from another range or generate elements on the fly.

The following templates provide access to the types used by a range.

 * `std::ranges::iterator_t<R>` - iterator type of range `R`
 * `std::ranges::sentinel_t<R>` - sentinel type of range `R` (type returned by `std::ranges::end(R)`, which may be different from the type returned by `std::ranges::begin(R)`)
 * `std::ranges::size_t<R>` - type of range `R`'s size type (type returned by `std::ranges::size(R)`, if implemented)
 * `std::ranges::difference_t<R>` - type returned by differencing two iterator types of range `R` (resolves to `std::iter_difference_t<std::ranges::iterator)t<R>>`)
 * `std::ranges::range_reference_t<R>` - type returned by _dereferencing an iterator_ of range `R` (type returned by `*(std::ranges::begin(R)`)
 * `std::ranges::range_rvalue_reference_t<R>` - type returned by _dereferencing an iterator_ of range `R` but as an r-value reference (type returned by `std::move(*(std::ranges::begin(R))`)
 * `std::ranges::range_value_t<R>` - type returned by _dereferencing an iterator_ of range `R` but with the reference, `const`, and `volatile` (e.g. if `std::ranges::range_reference_t<R>` is `const int&`, `std::ranges::range_value_t<R>` is `int`)

```c++
void print_range(std::ranges::range auto &&range) {
    using ELEM_REF = std::ranges::range_reference_t<decltype(range)>;
    for (ELEM_REF v : range) {
        std::cout << v << std::endl;
    }
}
```

The following concept_TEMPLATE detail the features supported by a range's iterator type. These concept_TEMPLATE loosely map to the concept_TEMPLATE for iterators.

 * `std::ranges::input_range` maps to `std::input_iterator`
 * `std::ranges::output_range` maps to `std::output_iterator`
 * `std::ranges::forward_range` maps to `std::forward_iterator` 
 * `std::ranges::bidirectional_range` maps to `std::bidirectional_iterator`
 * `std::ranges::random_access_range` maps to `std::random_access_iterator`
 * `std::ranges::contiguous_range` maps to `std::contiguous_iterator`

```c++
void print_range(std::ranges::random_access_range auto &&range) {
    auto it { std::ranges::begin(range) };
    std::cout << it[3] << std::endl;
    std::cout << it[1] << std::endl;
    std::cout << it[2] << std::endl;
}
```

### Owning Views

`{bm} /(Library Functions\/Ranges\/Owning Views)_TOPIC/`

An owning view moves the range it's operating on into itself rather than reference that range. Doing this avoids the problem of a view referencing a destroyed range, which usually happens when a function returns a view but the range that view is referencing goes out of scope.

```c++
// This function is faulty because the returned view REFERENCES vec but
// vec gets destroyed when the function exits. The view references a
// destroyed object.
auto faulty_code() {
    std::vector<int> vec{ 1, 2, 3 };
    return vec
        | std::views::transform([](int i) { return i * 2; })
        | std::views::filter([](int i) { return i != 0; });
}
```

To create an owning view, use `std::move()` on the original range.

```c++
// By using std::move() on the range, the view becomes an owning view.
auto good_code() {
    std::vector<int> vec{ 1, 2, 3 };
    return std::move(vec)
        | std::views::transform([](int i) { return i * 2; })
        | std::views::filter([](int i) { return i != 0; });
}
```

```{note}
This started to be supported in version 12 of g++.
```

### Type-erasure

`{bm} /(Library Functions\/Ranges\/Type-erasure)_TOPIC/`

A range's type depends on the type of the underlying container or generator (e.g. `std::ordered_set`), element type of the range (e.g. `int`), and the list of view manipulations applied to that range. Each change ends up changing the underlying type of the range.

```c++
std::vector<int> vec{ 1, 2, 3 };

// THE CODE BELOW PRINTS "same!"
// ----------------------------
// decltype(v1) == decltype(v2) because both use the same underlying container type, element type,
// and have the exact same list of views applied WITH the exact same functor object.
auto functor { [](int i) { return i * 2; } };
auto v1 { vec | std::views::transform(functor) };
auto v2 { vec | std::views::transform(functor) };
if constexpr (std::is_same_v<decltype(v1), decltype(v2)>) {
    std::cout << "same!";
} else {
    std::cout << "NOT same!";
}

// THE CODE BELOW PRINTS "NOT same!"
// ---------------------------------
// decltype(v1) != decltype(v2) because although the two types use the same underlying container
// type, element type, and have the exact same list of views applied, those views are DIFFERENT the
// functor classes each are unique -- they're technically two different classes, each with its own
//  unique type. Those unique types are included in the types of v3 and v4 somewhere in a depth of
//  template parameter chains.
auto v3 { vec | std::views::transform([](int i) { return i * 2; }) };
auto v4 { vec | std::views::transform([](int i) { return i * 2; }) };
if constexpr (std::is_same_v<decltype(v3), decltype(v4)>) {
    std::cout << "same!";
} else {
    std::cout << "NOT same!";
}
```

The lack of type erasures sometimes causes problems when doing certain types of view manipulations. For example, combining together two ranges with the same element type (flattening) via `std::views::join` isn't possible unless the types of those ranges are exactly the same.

```c++
std::ranges::empty_view<int> y{};
std::ranges::single_view<int> x{5};
std::vector combined{ x , y };  // x and y of different types, vector's type parameter can't be deduced
auto joined { std::ranges::join_view(combined) };
for (auto x : joined) {
    std::cout << x << std::endl;
}
```

To mitigate this, a third-party library called ranges-v3 provides `ranges::any_view<T>`. `ranges::any_view<T>` essentially "erases" the type of a range by wrapping it and unifying it to a specific type. The downside of this wrapping is that it has a performance impact as abstracting away the type information involves extra runtime code.

```c++
std::ranges::empty_view<int> y{};
std::ranges::single_view<int> x{5};
std::vector<ranges::any_view<int>> combined{
    ranges::any_view<int> { x },
    ranges::any_view<int> { y }
};
auto joined { std::ranges::join_view(combined) };
for (auto x : joined) {
    std::cout << x << std::endl;
}
```

One important thing about `ranges::any_view<T>` is that it takes an optional second template parameter which defines the capabilities of the range its wrapping. By default, it's set to `category::input` which supports capabilities of an input range, but it also supports ...

* `category::input` - satisfies `std::ranges::input_range` concept_TEMPLATE
* `category::forward` - satisfies `std::ranges::forward_range` concept_TEMPLATE
* `category::bidirectional` - satisfies `std::ranges::bidirectional_range` concept_TEMPLATE
* `category::random_access` - satisfies `std::ranges::random_access_range` concept_TEMPLATE
* `category::sized` - satisfies `std::ranges::sized_ranges` concept_TEMPLATE

```{note}
There's also `category::none` and `category::mask`, not exactly sure what these are for.
```

```c++
std::ranges::empty_view<int> y{};
std::ranges::single_view<int> x{5};
std::vector<ranges::any_view<int, ranges::category::input>> combined{
    ranges::any_view<int, ranges::category::input> { x },
    ranges::any_view<int, ranges::category::input> { y }
};
auto joined { std::ranges::join_view(combined) };
for (auto x : joined) {
    std::cout << x << std::endl;
}
```

Alternatively, in certain cases `std::span<T>` also abstracts away type information.

```c++
std::ranges::empty_view<int> y{};
std::ranges::single_view<int> x{5};
std::vector<std::span<int>> combined{
    std::span<int> { x },
    std::span<int> { y }
};
auto joined { std::ranges::join_view(combined) };
for (auto x : joined) {
    std::cout << x << std::endl;
}
```

```{note}
C++20 / C++23 has nothing in the standard library for this except for `std::span<T>`, and AFAIK type erasure isn't what it was intended for. You should use ranges-v3. Future versions of C++ might provide something.
```

### Custom Views

`{bm} /(Library Functions\/Ranges\/Custom Views)_TOPIC/`

To write a custom view, create a class that inherits from `std::ranges::view_interface` with a `begin()` function, and an `end()` function, and either a default constructor (if generating values) and / or a constructor that takes in a range (if manipulating values).

```c++
struct FakeGeneratingView : public std::ranges::view_interface<FakeGeneratingView> {
    auto begin() const { return &(values[0]); }
    auto end() const { return &(values[3]); }
private:
    int[3] values = { 0, 1, 2 };
};


// USE THE VIEW
for (auto x : FakeGeneratingView{}) {
    std::cout << x << std::endl;
}
```

```{note}
The above example class is feeding itself as a template parameter to `std::ranges::view_interface`. This is a common C++ idiom referred to as the curiously recurring template pattern (CRTP) which allows for feeding the derived class back into a templated base class. Something to do with compile-time polymorphism.
```

The following example is another custom view but this time it takes in an another range and manipulates its values and it supports the pipe operator.

```c++
template<std::ranges::input_range R> 
    requires std::ranges::view<R>
struct AddFiveView : public std::ranges::view_interface<AddFiveView<R>> {
    AddFiveView() = delete;
    constexpr AddFiveView(R&& r):
        i(std::forward<R>(r)),
        _begin(std::begin(i.range)),
        _end(std::end(i.range)) {}
    constexpr auto begin() const { return _begin; }
    constexpr auto end() const { return _end; }
private:
    struct F : decltype([](auto x) { return x + 5; }) {};
    using R_RES = std::ranges::transform_view<R, F>;
    struct Internal {
        Internal(R&& r) : range(std::forward<R>(r) | std::views::transform(F())) {}
        R_RES range;
    };
    Internal i;  // what do I put as the template arg???
    std::ranges::iterator_t<R_RES> _begin;
    std::ranges::iterator_t<R_RES> _end; 
};


struct AddFiveViewAdaptorClosure {
    constexpr AddFiveViewAdaptorClosure() {}

    template <std::ranges::viewable_range R>
    constexpr auto operator()(R&& r) const {
        return AddFiveView<R>(std::forward<R>(r));
    }
} ;

struct AddFiveViewAdaptor {
    template<std::ranges::viewable_range R>
    constexpr auto operator () (R && r) {
        return AddFiveView(std::forward<R>(r)) ;
    }

    constexpr auto operator () () {
        return AddFiveViewAdaptorClosure();
    }   
};

template <std::ranges::viewable_range R>
constexpr auto operator | (R&& r, AddFiveViewAdaptorClosure const & a) {
    return a(std::forward<R>(r)) ;
}

namespace CustomViews {
    AddFiveViewAdaptorClosure AddFiveView;
}



// USE THE VIEW VIA THE PIPE OPERATOR
//   Note the use of std::views::all -- this is required for some reason (maybe it normalizes some missing pieces)
std::vector<int> v{0,1,3};
for (auto x : v | std::views::all | CustomViews::AddFiveView) {
    std::cout << x << std::endl;
}
```


# Terminology

 * `{bm} preprocessor/(preprocessor|translation unit)/i` - A tool that takes in a C++ source file and performs basic manipulation on it to produce what's called a translation unit.

 * `{bm} compiler/(compiler|object file|object code)/i` - A tool that takes in a translation unit to produce an intermediary format called an object file.

 * `{bm} linker/(linker|executable)/i` - A tool that takes multiple object files to produce an executable. Linkers are also responsible for finding libraries used by the program and integrating them into the executable.

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

 * `{bm} member-of-pointer (->)/(member[\-\s]of[\-\s]pointer)/i` - An operator that dereferences a pointer and accesses a member of the object pointed to (e.g. `ptr->x`).

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

 * `{bm} scope resolution (::)/(scope resolution)/i` - An operator that's used to access static members (e.g. `MyStruct::static_func()`).

 * `{bm} extend/(extends?|subclass)/i` - Another way of expressing class inheritance (e.g. B extends A is equivalent to saying B is a child of A).

 * `{bm} exception/(exception|try[\-\s]catch)/i` - An exception operation accepts an object and unwinds the call stack until reaching a special region specifically intended to stop the unwinding for objects of that type, called a try-catch block. Exceptions are a way for code to signal that something unexpected / exceptional happened.

 * `{bm} structured binding` - A language feature that allows for unpacking an object's members / array's elements into a set of variables (e.g. `auto [x, y] { two_elem_array }`).

 * `{bm} copy semantics` - The rules used for making copies of objects of some type. A copy, once made, should be equivalent to its source. A modification on the copy shouldn't modify the source as well.

 * `{bm} member-wise copy/(member[\-\s]wise copy)/i` - The default copy semantics for classes. Each individual field is copied.

 * `{bm} copy constructor` - A constructor with a single parameter that takes in a reference to an object of the same type (e.g. `T(const T &) { ... }`). A copy constructor is used to specify the copy semantics for that class.

 * `{bm} copy assignment` - An assignment operator overload that copies one object into another (e.g. `x = y`). Copy assignment requires that resources in the destination object be cleaned up prior to performing the copy.

 * `{bm} RAII/(RAII|CADRe)/` - Short for resource acquisition is initialization, the concept_NORM that the life cycle of some resource (e.g. open file, database object, etc..) is bound to an object's lifetime via it's constructor and destructor.

   Sometimes also referred to as constructor acquires destructor releases (CADRe).

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

 * `{bm} rvalue reference` - A data type that's more-or-less the same as a reference but conveys to the compiler that the data it's pointing to is an rvalue (e.g. `MyType &&rref { y }`).

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

 * `{bm} vtable` - A table of pointers to virtual functions, generated by the compiler. When a virtual function gets invoked (runtime) vtables are used to determine which method implementation to use.

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

 * `{bm} concept/(concept)_TEMPLATE/i` - A compile-time check to ensure that the type substituted for a template parameter matches a set of requirements (e.g. the type supports certain operators).

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

 * `{bm} template specialization` - Given a specific substitutions set substitutions for the template parameters of a template, a template specialization is code that overrides the template generated code. Oftentimes template specializations are introduced because they're more memory or computationally efficient than the standard template generated code.

   ```c++
   // template
   template<typename T>
   T sum(T a, T b) {
       return a + b;
   }
   
   // template specialization for bool: bitwise or
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

 * `{bm} fold expression` - Exhaustively applies a binary operator to the contents of a parameter pack and returns the final result.

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

 * `{bm} lambda` - Shorthand expression for an unnamed functor.

   ```c++
   auto f = [] (int z) -> int { return -z; };
   ```

 * `{bm} closure` - An object / instance of a lambda.

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

 * `{bm} operator overload/(operator overload|overloaded operator)/i` - A function that gets invoked when a certain operator is used with some specific class. The function can be either a free function or a member function of the class the operator is intended for.

   ```c++
   struct MyClass {
      int operator()(int y) const { return -y + x; } // function call operator
      ...
   };
   ```

 * `{bm} forward declaration` - To use a function, class, variable, etc.. within some C++ code, only its declaration is needed, not its definition (implementation). The compiler will ensure that the usage points to the implementation when the time comes.

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

 * `{bm} smart pointer` - A class that wraps a pointer to a dynamically object. The class provides some level of automated pointer management / memory management through the use of move semantics, copy semantics, and RAII. 

 * `{bm} namespace` - C++'s mechanism of organizing code into a logical hierarchy / avoiding naming conflicts, similar to packages in Java or Python.

 * `{bm} unnamed namespace` - A special namespace that limits the visibility of the code to the containing translation unit, meaning that code can't be referenced at all outside of the translation unit.

 * `{bm} universal reference` - A function template that automatically creates overloads based on whether the argument passed in for a parameter is a lvalue reference or a rvalue reference.

   ```c++
   // TEMPLATE where the parameter x is a universal reference
   template<typename T>
   void test(T && x) {
       if (x % 2 == 0) {
           vector.push_back(std::forward<T>(x));  // forward based on the reference type
       }
   }

   
   // When the type is an it, the above template expands to the following two overloads ...
   void test(int & x) {
       if (x % 2 == 0) {
           vector.push_back(x);            // calls push_back(int &x) / push_back(int x)
       }
   }  
   void test(int && x) {
       if (x % 2 == 0) {
           vector.push_back(std::move(x)); // calls push_back(int &&x)
       }
   }
   ```

* `{bm} special member function` - A member function which, if invoked but not explicitly implemented, the compiler will automatically generate a default implementation for. Each of the following is considered a special member function: default constructor, copy constructor, move constructor, copy assignment operator, move assignment operator, and destructor.

`{bm-ignore} (classification)/i`
`{bm-ignore} (structure)/i`
`{bm-error} Did you mean variadic?/(vardic)/i`
`{bm-error} Did you mean template parameter?/(type parameter)/i`

`{bm-error} Add the suffix _NORM or _TEMPLATE/(concept)/i`
`{bm-ignore} (concept)_NORM/i`

`{bm-error} Topic not found?/(_TOPIC)/`