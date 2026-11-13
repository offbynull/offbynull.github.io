<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

When you re-formulate an alignment graph as an HMM, the computation changes to one of most likely vs highest scoring. As such, it doesn't make sense to use the same edge weights in an HMM as you do in an alignment graph. Even if you normalize those weights (based on the "sum to 1" criteria discussed above), the optimal alignment path will likely be different than the the optimal hidden path.

The question remains, if you were to actually do this (re-formulate an alignment graph as an HMM), how would you go about choosing the hidden state transition probabilities? That remains unclear to me. The probabilities in the example below were handpicked to force a specific optimal hidden path.

This section isn't meant to be a solution to some practical problem. It's just a building block for another concept discussed further on. As long as you understand that what's being shown here is a thing that can happen, you're good to move forward.
</div>

