<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

The way to think of references is documented [here](https://stackoverflow.com/a/1164267). Don't consider a reference as an object the same way a pointer is an object. In the compiler's eyes, a reference doesn't store anything like a pointer does (stores a memory address). It's just a "reference" to an object -- the object itself has storage, but the reference to that object doesn't.

In that sense, it's impossible to have ...

* a `const` reference like you have a `const` pointer or an array of references.
* an array of references
* etc...

... the same way that you can have with a pointer.
</div>

