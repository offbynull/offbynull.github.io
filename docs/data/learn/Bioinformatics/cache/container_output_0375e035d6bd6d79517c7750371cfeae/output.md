<div style="border:1px solid black;">

`{bm-disable-all}`

Given k=3 and vectors=[(2, 2), (2, 4), (2.5, 6), (3.5, 2), (4, 3), (4, 5), (4.5, 4), (7, 2), (7.5, 3), (8, 1), (9, 2), (8, 7), (8.5, 8), (9, 6), (10, 7)]...

The farthest first travel heuristic produced the clusters at each iteration ...

 * Iteration 0

    * cluster center (9, 6)=[(2, 2), (2, 4), (2.5, 6), (3.5, 2), (4, 3), (4, 5), (4.5, 4), (7, 2), (7.5, 3), (8, 1), (9, 2), (8, 7), (8.5, 8), (9, 6), (10, 7)]

   ![k-centers 2D plot](ch8_0375e035d6bd6d79517c7750371cfeae_plot0.svg)

 * Iteration 1

    * cluster center (9, 6)=[(7, 2), (7.5, 3), (8, 1), (9, 2), (8, 7), (8.5, 8), (9, 6), (10, 7)]
    * cluster center (2, 2)=[(2, 2), (2, 4), (2.5, 6), (3.5, 2), (4, 3), (4, 5), (4.5, 4)]

   ![k-centers 2D plot](ch8_0375e035d6bd6d79517c7750371cfeae_plot1.svg)

 * Iteration 2

    * cluster center (9, 6)=[(8, 7), (8.5, 8), (9, 6), (10, 7)]
    * cluster center (2, 2)=[(2, 2), (2, 4), (2.5, 6), (3.5, 2), (4, 3), (4, 5), (4.5, 4)]
    * cluster center (8, 1)=[(7, 2), (7.5, 3), (8, 1), (9, 2)]

   ![k-centers 2D plot](ch8_0375e035d6bd6d79517c7750371cfeae_plot2.svg)

</div>

`{bm-enable-all}`
