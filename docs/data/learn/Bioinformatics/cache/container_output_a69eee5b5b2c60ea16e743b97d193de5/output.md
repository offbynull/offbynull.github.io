<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

The Pevzner book calls this !!Soft Decoding!! and it never covers a good use-case for it. What is the point of this? Imagine I've used the Viterbi algorithm to generate the most probable hidden path. I've determined that one of the transitions in that hidden path leads to a hidden state symbol emission with low certainty. So what do I do at that point? In the hidden path, do I try swapping that transition's destination to another hidden state? Maybe the revised hidden path will be slightly less probable but the certainty calculations will even out more?
</div>

