<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

If you understand algebra, the reasoning for why the above algorithm works is available at https://math.stackexchange.com/a/71173...

Write `{kt} \frac{a}{b} \div \frac{c}{d}` as `{kt} \frac{\frac{a}{b}}{\frac{c}{d}}`.

Suppose you wanted to clear the denominator of this compound fraction. You could try multiplication by `{kt} \frac{d}{c}`, but you'll have to multiply the top and the bottom of the fraction to avoid changing it. So, you end up with

`{kt} \frac{\frac{a}{b}}{\frac{c}{d}} = \frac{\frac{a}{b}}{\frac{c}{d}} \cdot \frac{\frac{d}{c}}{\frac{d}{c}} = \frac{\frac{a}{b} \cdot \frac{d}{c}}{\frac{c}{d} \cdot \frac{d}{c}} = \frac{\frac{ad}{bc}}{1} = \frac{ad}{bc}.`
</div>

