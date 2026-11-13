<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

The Pevzner book has the 2nd formula above as >= instead of >.

I'm assuming they did this because they're letting edge weights be >= 0 instead of > 0, which doesn't make sense because an edge with a weight of 0 means the same entity exists on both ends of the edge. If an edge weight is 0, it'll contribute nothing to the distance, meaning that more edges being highlighted doesn't necessarily mean a larger distance.
</div>

