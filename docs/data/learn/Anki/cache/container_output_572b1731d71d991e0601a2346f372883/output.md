<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

This topic was only briefly discussed, so I don't know for sure what the properties/requirements are for a similarity metric other than higher = more similar. Contrast this to distance metrics, where it explicitly mentions the requirements that need to be followed (e.g. triangle inequality property). For similarity metrics, it didn't say if there's some upper-bound to similarity or if totally similar entities have to score the same. For example, does `similarity(snake,snake) == similarity(bird,bird)` have to be true or can it be that `similarity(snake,snake) > similarity(bird,bird)`?

I saw on Wikipedia that sequence alignment scoring matrices like PAM and BLOSUM are similarity matrices, so that implies that totally similar entities don't have to be the same score. For example, in BLOSUM62 `similarity(A,A) = 4` but `similarity(R,R) = 5`.

Also, does a similarity metric have to be symmetric? For example, `similarity(snake,bird) == similarity(bird,snake)`. I think it does have to be symmetric.
</div>

