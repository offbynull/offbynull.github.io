<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

Note what this algorithm is doing. The Pevzner book claims that it's very similar to Llyod's algorithm for k-means clustering in that it's starting off at some random point and pushing that point around to maximize some metric (generic name for this is called [Expectation-maximization](https://en.wikipedia.org/wiki/Expectation%E2%80%93maximization_algorithm)).

The book claims that this is soft clustering. But if you only have one observed sequence, aren't you clustering a single data point? Shouldn't you have many observed sequences? Or maybe having many observed sequences is the same thing as having one sequence and concatenating them (need to figure out some special logic for each sequence's first transition from SOURCE)?

Monte Carlo algorithms like this are typically executed many times, where the best performing execution is the one that gets chosen.
</div>

