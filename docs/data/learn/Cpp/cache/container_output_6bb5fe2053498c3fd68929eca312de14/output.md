<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

Recall that "emplace" functions don't copy or move. They're templated functions. You pass in object initialization arguments directly into the functions and it uses a template parameter pack to forward those arguments for object creation directly within the function (e.g. constructor arguments, initializer list, etc..).
</div>

