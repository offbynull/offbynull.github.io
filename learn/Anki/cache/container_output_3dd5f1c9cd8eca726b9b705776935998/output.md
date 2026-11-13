<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

This topic was only briefly discussed, so I have no idea what properties are required other than: 0 = completely dissimilar / orthogonal and anything higher than that is more similar. It didn't say if there's some upper-bound to similarity or if totally similar entities have to score the same. For example, does `similarity(snake,snake) == similarity(bird,bird)` have to be true or can it be that `similarity(snake,snake) > similarity(bird,bird)`? I saw on Wikipedia that sequence alignment scoring matrices like PAM and BLOSUM are similarity matrices, so that implies that totally similar entities don't have to be the same score. For example, in BLOSUM62 `similarity(A,A) = 4` but `similarity(R,R) =5`.

There may be other properties involved, such as how the triangle inequality property is a thing for distance matrices / distance metrics.
</div>

