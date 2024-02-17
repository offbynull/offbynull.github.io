<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

When a denominator of a rational function approaches 0, it doesn't automatically mean you get an infinite limit. The learning material says: "When both numerator and denominator approach 0, it may be an infinite limit or some finite value. For example, `{kt} \lim\limits_{x \rarr 1} \frac{x^2-1}{x-1}` is *not* an infinite (if you graph it, it's a straight line where x=1 is undefined) but `{kt} \lim\limits_{x \rarr 0} \frac{sin(x)}{x^3}` is an infinite limit (both the numerator and denominator approach 0).

```{calculus}
Graph
funcs: [(x^2-1)/(x-1), sin(x)/x^3]
x_lim: [-5, 5]
y_lim: [-5, 5]
fig_size: [3, 3]
```

Why isn't `{kt} \lim\limits_{x \rarr 1} \frac{x^2-1}{x-1}` an infinite limit? `{kt} \frac{x^2-1}{x-1}`'s numerator factors to `{kt} \frac{(x-1)(x+1)}{x-1}` (difference of square). From there, you can eliminate the denominator: `{kt} x+1`.
</div>

