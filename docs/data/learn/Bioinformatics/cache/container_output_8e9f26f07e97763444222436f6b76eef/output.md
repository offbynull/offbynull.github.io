<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

Notice what's happening here. This can be made very memory efficient:

 1. The calculation is being done front-to-back, so once a column of nodes in the Viterbi have been processed, it doesn't need to be kept around anymore.
 2. You technically don't even need to keep a graph structure in memory. You can just keep the emitted symbols sequence and a pre-calculated set of probabilities.
 3. You can apply the divide-and-conquer algorithm as discussed in Algorithms/Sequence Alignment/Global Alignment/Divide-and-Conquer Algorithm_TOPIC - it's the same type of grid-based graph.
</div>

