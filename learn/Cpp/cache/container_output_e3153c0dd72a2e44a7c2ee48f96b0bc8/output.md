<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

The above is an over-simplification. The ways to initialize are vast and complex. See [here](https://en.cppreference.com/w/cpp/language/initialization) for a full accounting and [here](https://youtu.be/7DTlWPgX6zs) for an hour long talk about the edge cases.

It seems like the safest bet is to always use brace initialization where possible. Just use the braces as if they were parentheses or braces in Java (specific to the context). The others have surprising behaviour (e.g. they won't warn about narrowing conversions).
</div>

