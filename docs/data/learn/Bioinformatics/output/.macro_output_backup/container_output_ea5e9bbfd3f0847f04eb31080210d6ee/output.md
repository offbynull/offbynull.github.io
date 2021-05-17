<div style="border:1px solid black;">

`{bm-disable-all}`

Given the permutation ['+A', '+B', '+C', '+D']...

 * START
   * CE(A_t, D_h)
   * SE(A_t, A_h)
   * CE(A_h, B_t)
   * SE(B_t, B_h)
   * CE(B_h, C_t)
   * SE(C_t, C_h)
   * CE(C_h, D_t)
   * SE(D_t, D_h)

CE means colored edge / SE means synteny edge.

Recall that the the breakpoint graph is undirected / a permutation may have been walked in either direction(clockwise vs counter-clockwise). If the output looks like it's going backwards, that's just as correct as if it looked like it's going forward.
</div>

`{bm-enable-all}`

