<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

What the above is saying is that, if e ends up being an rvalue reference, it uses the basic rules explained just previous to this universal references explainer. Recall that parameters that are universal references borrow the rvalue reference syntax of double ampersand (&&) -- double ampersands are universal references if the type is used in a parameter and left as-is (no `const`/`volatile`/etc..).

The types for `T` and `p` look invalid in lvalue cases but there's some special logic going on under the hood in terms of "reference collapsing" and doing things internally that would be explicitly illegal to do in code. For example, normally, if `p=int&` then `T=int`. But that isn't the case with universal references: `p=int&` (interpreted) but then `T=int&` as well.
</div>

