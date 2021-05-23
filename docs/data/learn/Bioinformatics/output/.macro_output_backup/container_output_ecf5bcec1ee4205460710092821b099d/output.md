<div style="border:1px solid black;">

`{bm-disable-all}`

Applying 2-breaks on circular genome until red_p_list=[['+A', '-B', '-C', '+D'], ['+E']] matches blue_p_list=[['+A', '+B', '-D'], ['-C', '-E']]...

 * red_p_list=[['+A', '-B', '-C', '-E', '+D']]
 * red_p_list=[['+A', '-B', '+D'], ['+C', '+E']]
 * red_p_list=[['+A', '-B', '-D'], ['+C', '+E']]
 * red_p_list=[['+A', '+B', '-D'], ['+C', '+E']]


Recall that the the breakpoint graph is undirected / a permutation may have been walked in either direction (clockwise vs counter-clockwise). If the output looks like it's going backwards, that's just as correct as if it looked like it's going forward.
</div>

`{bm-enable-all}`

