<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

Similar to the Viterbi algorithm, the Pevzner book claims this is [expectation-maximization](https://en.wikipedia.org/wiki/Expectation%E2%80%93maximization_algorithm). The book didn't tell you the HMM probabilities to start with. I just assumed that you start off with randomized probabilities (the code challenge in the book gives you starting probabilities, not sure how they're derived).

This algorithm works for a single emitted sequence, but how do you make it work when you have many emitted sequences? Maybe what you need to do is, in each cycle of the algorithm, select one of the emitted sequences at random and use the certainties from that.

Monte Carlo algorithms like this are typically executed many times, where the best performing execution is the one that gets chosen.
</div>

