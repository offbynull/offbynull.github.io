<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

The book mentions a couple of niche cases to do with decaying of types.

 1. When `e` is a raw array (e.g. `e=int[13]`) and `p` is a reference type (e.g. `p=T&`, `p=const T&`, `p=T&&`, ...), `p` doesn't decay to a pointer (it doesn't become `p=int* &`). Instead, an actual reference to the array (including its size) gets passed in, meaning that it's possible to get the array's size via `sizeof()`. This isn't possible if it decayed to a pointer.
   
    The book recommends using `std::array` instead of relying on this.

 2. When `e` is a function and `p` is a reference type, `p` doesn't decay to a function pointer. It ends up being a reference to the actual function.

    The book mentions that, in practice, the non-decaying of functions rarely makes a difference to the code.
</div>

