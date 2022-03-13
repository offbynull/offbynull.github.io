<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

I said "ties are broken arbitrarily" (step 1) because that's what the Pevzner book says. This isn't entirely true? I think it's possible to get into a situation where a tied point ping-pongs back and forth between clusters. So, maybe what actually needs to happen is you need to break ties consistently -- it doesn't matter how, just that it's consistent (e.g. the center closest to origin + smallest angle from origin always wins the tied member_CLUSTER).

Also, if the centers haven't converged, the dragged center is guaranteed to decrease the squared error distortion when compared to the previous center. But, does that mean that a set of converged centers are optimal in terms of squared error distortion? I don't think so. Even if a cluster converged to all the correct member_CLUSTERs, could it be that the center can be slightly tweaked to get the squared error distortion down even more? Probably.
</div>

