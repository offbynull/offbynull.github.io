<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

`emplace()` / `emplace_back()` don't copy or move because you pass in initialization arguments directly into the functions. Internally, they use template parameter packs to forward arguments for object creation (e.g. constructor arguments, initializer list, etc..).
</div>

