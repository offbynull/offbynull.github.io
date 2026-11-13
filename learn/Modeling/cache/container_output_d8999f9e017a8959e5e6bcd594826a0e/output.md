<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

I don't know why this algorithm exists. It's shifting the first bucket of the histogram back by some arbitrary nonsensical amount. Other sources online seem to be referencing the same algorithm.

I think what this section of the book was trying to convey is that, for histograms, sometimes you may want to have your first bucket start off at a lower point than the lowest value in your data. For example, if you're bucketing in intervals of 10, and the lowest value is 6, it may make sense to have your intervals be 1-10, 11-20, 21-30, etc.. as opposed to 6-15, 16-25, 26-35, etc..
</div>

