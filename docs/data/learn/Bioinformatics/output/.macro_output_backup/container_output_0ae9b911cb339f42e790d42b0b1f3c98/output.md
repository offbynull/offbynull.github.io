<div style="border:1px solid black;">

`{bm-disable-all}`

Given the permutation ['+A', '+B', '+C', '+D']...

 * START
   * CE(C_h, D_t)
   * SE(C_h, C_t)
   * CE(B_h, C_t)
   * SE(B_h, B_t)
   * CE(A_h, B_t)
   * SE(A_h, A_t)
   * CE(A_t, D_h)
   * SE(D_h, D_t)

CE means colored edge / SE means synteny edge.

Recall that the the breakpoint graph is undirected / a permutation may have been walked in either direction (clockwise vs counter-clockwise). If the output looks like it's going backwards, that's just as correct as if it looked like it's going forward.
</div>

`{bm-enable-all}`

