<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

For sample variance, why use (n-1) instead of n? The sample variance is trying to estimate the population variance, and dividing by (n-1) gives you a number that's closer to the population variance. In the example above, if the sample variance was dividing by n instead of n-1, it would end up being 6.222, which is farther away from the population variance.

As the sample size approaches the population size, the significance of variance dividing by (n-1) vs n becomes less and less.

The official name for this is Bessel's correction.
</div>

