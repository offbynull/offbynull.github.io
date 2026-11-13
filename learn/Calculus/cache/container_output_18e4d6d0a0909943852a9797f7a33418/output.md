<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

There's a more interesting example in the learning material when it comes to the quotient law: `{kt} \lim\limits_{x \rarr 0} \frac{\sqrt{x^2+9}-3}{x^2}`. The quotient law can't be directly applied because the denominator's limit would approach 0, which is not allowed.

* `{kt} \lim\limits_{x \rarr 0} \frac{\sqrt{x^2+9}-3}{x^2}`
* `{kt} \frac{\lim\limits_{x \rarr 0} \sqrt{x^2+9}-3}{\lim\limits_{x \rarr 0} x^2}` - Invalid application of quotient law (limit in the denominator is approaching 0, which is not allowed)

To get past this, the book reworks the equation by rationalizing the numerator:

* `{kt} \frac{\sqrt{x^2+9}-3}{x^2} \cdot \frac{\sqrt{x^2+9}+3}{\sqrt{x^2+9}+3}`
* `{kt} \frac{x^2+9+3\sqrt{x^2+9}-3\sqrt{x^2+9}-9}{x^2(\sqrt{x^2+9}+3)}`
* `{kt} \frac{x^2+9-9}{x^2(\sqrt{x^2+9}+3)}`
* `{kt} \frac{x^2}{x^2(\sqrt{x^2+9}+3)}`
* `{kt} \frac{1}{\sqrt{x^2+9}+3}`

In this updated form, the quotient law doesn't have the same problem. As x approaches 0, the denominator approaches 3. The limit laws can now be applied.

This isn't something that I would have considered doing had I seen this problem?
</div>

