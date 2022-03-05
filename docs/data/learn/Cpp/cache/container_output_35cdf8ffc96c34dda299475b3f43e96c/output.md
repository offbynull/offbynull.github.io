<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

The rules for initialization are complex. In this case, there's a constructor that takes in an `std::initializer_list`. That means braced initialization / brace-plus-equals initialization will in most cases call that constructor, where that initializer list get populated with whatever is in the braces. To avoid that, the easiest thing you can do is fall back to using the legacy way of calling constructors (parenthesis).
</div>

