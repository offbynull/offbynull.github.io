<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

The reason why universal references work is that the compiler is deducing the correct type for the template parameter based on how its used. If it gets passed a lvalue reference, it'll invoke the lvalue version. If it gets passed a rvalue reference, it'll invoke the rvalue version.

Internally, the compiler uses a technique called "reference collapsing" to get this to work, which temporarily / internally allows certain unallowable C++ constructs (references to references are disallowed). See [here](https://isocpp.org/blog/2012/11/universal-references-in-c11-scott-meyers) for more information.
</div>

