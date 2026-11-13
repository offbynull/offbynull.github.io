<div style="border:1px solid black;">

`{bm-disable-all}`

The tree...

```{dot}
graph G {
 graph[rankdir=BT]
 node[shape=box, fontname="Courier-Bold", fontsize=10]
 edge[fontname="Courier-Bold", fontsize=10]
 layout=fdp
Bear [label="Bear\nseq: ATTCCC"]
Cat [label="Cat\nseq: ACTGGT"]
Elephant [label="Elephant\nseq: TTTCCC"]
Kangaroo [label="Kangaroo\nseq: ATTCCT"]
Lion [label="Lion\nseq: ACTGCT"]
i0 [label="i0\n"]
i1 [label="i1\n"]
i2 [label="i2\n"]
Cat -- i0 [label=""]
Lion -- i0 [label=""]
i0 -- i1 [label=""]
Bear -- i1 [label=""]
Kangaroo -- i2 [label=""]
Elephant -- i2 [label=""]
i0 -- i2 [label=""]
}
```

... with i0 set as its root and the distances ...

<table>
<thead><tr>
<th></th>
<th>A</th>
<th>C</th>
<th>T</th>
<th>G</th>
</tr></thead>
<tbody>
<tr>
<td>A</td>
<td>0.0</td>
<td>1.0</td>
<td>1.0</td>
<td>1.0</td>
</tr>
<tr>
<td>C</td>
<td>1.0</td>
<td>0.0</td>
<td>1.0</td>
<td>1.0</td>
</tr>
<tr>
<td>T</td>
<td>1.0</td>
<td>1.0</td>
<td>0.0</td>
<td>1.0</td>
</tr>
<tr>
<td>G</td>
<td>1.0</td>
<td>1.0</td>
<td>1.0</td>
<td>0.0</td>
</tr>
</tbody>
</table>

... has the following inferred ancestor sequences after using nearest neighbour interchange ...

graph score: 9.0

```{dot}
graph G {
 graph[rankdir=BT]
 node[shape=box, fontname="Courier-Bold", fontsize=10]
 edge[fontname="Courier-Bold", fontsize=10]
 layout=fdp
Bear [label="Bear\nseq: ATTCCC\ndist_set_0: {'A': 0.0, 'C': inf, 'T': inf, 'G': inf}\ndist_set_1: {'A': inf, 'C': inf, 'T': 0.0, 'G': inf}\ndist_set_2: {'A': inf, 'C': inf, 'T': 0.0, 'G': inf}\ndist_set_3: {'A': inf, 'C': 0.0, 'T': inf, 'G': inf}\ndist_set_4: {'A': inf, 'C': 0.0, 'T': inf, 'G': inf}\ndist_set_5: {'A': inf, 'C': 0.0, 'T': inf, 'G': inf}"]
Cat [label="Cat\nseq: ACTGGT\ndist_set_0: {'A': 0.0, 'C': inf, 'T': inf, 'G': inf}\ndist_set_1: {'A': inf, 'C': 0.0, 'T': inf, 'G': inf}\ndist_set_2: {'A': inf, 'C': inf, 'T': 0.0, 'G': inf}\ndist_set_3: {'A': inf, 'C': inf, 'T': inf, 'G': 0.0}\ndist_set_4: {'A': inf, 'C': inf, 'T': inf, 'G': 0.0}\ndist_set_5: {'A': inf, 'C': inf, 'T': 0.0, 'G': inf}"]
Elephant [label="Elephant\nseq: TTTCCC\ndist_set_0: {'A': inf, 'C': inf, 'T': 0.0, 'G': inf}\ndist_set_1: {'A': inf, 'C': inf, 'T': 0.0, 'G': inf}\ndist_set_2: {'A': inf, 'C': inf, 'T': 0.0, 'G': inf}\ndist_set_3: {'A': inf, 'C': 0.0, 'T': inf, 'G': inf}\ndist_set_4: {'A': inf, 'C': 0.0, 'T': inf, 'G': inf}\ndist_set_5: {'A': inf, 'C': 0.0, 'T': inf, 'G': inf}"]
Kangaroo [label="Kangaroo\nseq: ATTCCT\ndist_set_0: {'A': 0.0, 'C': inf, 'T': inf, 'G': inf}\ndist_set_1: {'A': inf, 'C': inf, 'T': 0.0, 'G': inf}\ndist_set_2: {'A': inf, 'C': inf, 'T': 0.0, 'G': inf}\ndist_set_3: {'A': inf, 'C': 0.0, 'T': inf, 'G': inf}\ndist_set_4: {'A': inf, 'C': 0.0, 'T': inf, 'G': inf}\ndist_set_5: {'A': inf, 'C': inf, 'T': 0.0, 'G': inf}"]
Lion [label="Lion\nseq: ACTGCT\ndist_set_0: {'A': 0.0, 'C': inf, 'T': inf, 'G': inf}\ndist_set_1: {'A': inf, 'C': 0.0, 'T': inf, 'G': inf}\ndist_set_2: {'A': inf, 'C': inf, 'T': 0.0, 'G': inf}\ndist_set_3: {'A': inf, 'C': inf, 'T': inf, 'G': 0.0}\ndist_set_4: {'A': inf, 'C': 0.0, 'T': inf, 'G': inf}\ndist_set_5: {'A': inf, 'C': inf, 'T': 0.0, 'G': inf}"]
i0 [label="i0\ndist_set_0: {'A': 1.0, 'C': 5.0, 'T': 4.0, 'G': 5.0}\ndist_set_1: {'A': 4.0, 'C': 2.0, 'T': 2.0, 'G': 4.0}\ndist_set_2: {'A': 4.0, 'C': 4.0, 'T': 0.0, 'G': 4.0}\ndist_set_3: {'A': 4.0, 'C': 2.0, 'T': 4.0, 'G': 2.0}\ndist_set_4: {'A': 4.0, 'C': 1.0, 'T': 4.0, 'G': 3.0}\ndist_set_5: {'A': 5.0, 'C': 3.0, 'T': 2.0, 'G': 5.0}\nseq: ACTCCT"]
i1 [label="i1\ndist_set_0: {'A': 0.0, 'C': 1.0, 'T': 1.0, 'G': 1.0}\ndist_set_1: {'A': 1.0, 'C': 1.0, 'T': 0.0, 'G': 1.0}\ndist_set_2: {'A': 1.0, 'C': 1.0, 'T': 0.0, 'G': 1.0}\ndist_set_3: {'A': 1.0, 'C': 0.0, 'T': 1.0, 'G': 1.0}\ndist_set_4: {'A': 1.0, 'C': 0.0, 'T': 1.0, 'G': 1.0}\ndist_set_5: {'A': 1.0, 'C': 0.0, 'T': 1.0, 'G': 1.0}\nseq: ATTCCC"]
i2 [label="i2\ndist_set_0: {'A': 1.0, 'C': 2.0, 'T': 1.0, 'G': 2.0}\ndist_set_1: {'A': 2.0, 'C': 2.0, 'T': 0.0, 'G': 2.0}\ndist_set_2: {'A': 2.0, 'C': 2.0, 'T': 0.0, 'G': 2.0}\ndist_set_3: {'A': 2.0, 'C': 0.0, 'T': 2.0, 'G': 2.0}\ndist_set_4: {'A': 2.0, 'C': 0.0, 'T': 2.0, 'G': 2.0}\ndist_set_5: {'A': 2.0, 'C': 1.0, 'T': 1.0, 'G': 2.0}\nseq: ATTCCC"]
Cat -- i0 [label="score: 2.0"]
Lion -- i0 [label="score: 1.0"]
i0 -- i1 [label="score: 2.0"]
Bear -- i1 [label="score: 0.0"]
Kangaroo -- i2 [label="score: 1.0"]
Elephant -- i2 [label="score: 1.0"]
i0 -- i2 [label="score: 2.0"]
}
```


graph score: 6.0

```{dot}
graph G {
 graph[rankdir=BT]
 node[shape=box, fontname="Courier-Bold", fontsize=10]
 edge[fontname="Courier-Bold", fontsize=10]
 layout=fdp
Bear [label="Bear\nseq: ATTCCC\ndist_set_0: {'A': 0.0, 'C': inf, 'T': inf, 'G': inf}\ndist_set_1: {'A': inf, 'C': inf, 'T': 0.0, 'G': inf}\ndist_set_2: {'A': inf, 'C': inf, 'T': 0.0, 'G': inf}\ndist_set_3: {'A': inf, 'C': 0.0, 'T': inf, 'G': inf}\ndist_set_4: {'A': inf, 'C': 0.0, 'T': inf, 'G': inf}\ndist_set_5: {'A': inf, 'C': 0.0, 'T': inf, 'G': inf}"]
Cat [label="Cat\nseq: ACTGGT\ndist_set_0: {'A': 0.0, 'C': inf, 'T': inf, 'G': inf}\ndist_set_1: {'A': inf, 'C': 0.0, 'T': inf, 'G': inf}\ndist_set_2: {'A': inf, 'C': inf, 'T': 0.0, 'G': inf}\ndist_set_3: {'A': inf, 'C': inf, 'T': inf, 'G': 0.0}\ndist_set_4: {'A': inf, 'C': inf, 'T': inf, 'G': 0.0}\ndist_set_5: {'A': inf, 'C': inf, 'T': 0.0, 'G': inf}"]
Elephant [label="Elephant\nseq: TTTCCC\ndist_set_0: {'A': inf, 'C': inf, 'T': 0.0, 'G': inf}\ndist_set_1: {'A': inf, 'C': inf, 'T': 0.0, 'G': inf}\ndist_set_2: {'A': inf, 'C': inf, 'T': 0.0, 'G': inf}\ndist_set_3: {'A': inf, 'C': 0.0, 'T': inf, 'G': inf}\ndist_set_4: {'A': inf, 'C': 0.0, 'T': inf, 'G': inf}\ndist_set_5: {'A': inf, 'C': 0.0, 'T': inf, 'G': inf}"]
Kangaroo [label="Kangaroo\nseq: ATTCCT\ndist_set_0: {'A': 0.0, 'C': inf, 'T': inf, 'G': inf}\ndist_set_1: {'A': inf, 'C': inf, 'T': 0.0, 'G': inf}\ndist_set_2: {'A': inf, 'C': inf, 'T': 0.0, 'G': inf}\ndist_set_3: {'A': inf, 'C': 0.0, 'T': inf, 'G': inf}\ndist_set_4: {'A': inf, 'C': 0.0, 'T': inf, 'G': inf}\ndist_set_5: {'A': inf, 'C': inf, 'T': 0.0, 'G': inf}"]
Lion [label="Lion\nseq: ACTGCT\ndist_set_0: {'A': 0.0, 'C': inf, 'T': inf, 'G': inf}\ndist_set_1: {'A': inf, 'C': 0.0, 'T': inf, 'G': inf}\ndist_set_2: {'A': inf, 'C': inf, 'T': 0.0, 'G': inf}\ndist_set_3: {'A': inf, 'C': inf, 'T': inf, 'G': 0.0}\ndist_set_4: {'A': inf, 'C': 0.0, 'T': inf, 'G': inf}\ndist_set_5: {'A': inf, 'C': inf, 'T': 0.0, 'G': inf}"]
i0 [label="i0\ndist_set_0: {'A': 1.0, 'C': 4.0, 'T': 3.0, 'G': 4.0}\ndist_set_1: {'A': 4.0, 'C': 3.0, 'T': 1.0, 'G': 4.0}\ndist_set_2: {'A': 4.0, 'C': 4.0, 'T': 0.0, 'G': 4.0}\ndist_set_3: {'A': 4.0, 'C': 1.0, 'T': 4.0, 'G': 3.0}\ndist_set_4: {'A': 5.0, 'C': 1.0, 'T': 5.0, 'G': 4.0}\ndist_set_5: {'A': 4.0, 'C': 2.0, 'T': 2.0, 'G': 4.0}\nseq: ATTCCC"]
i1 [label="i1\ndist_set_0: {'A': 0.0, 'C': 1.0, 'T': 1.0, 'G': 1.0}\ndist_set_1: {'A': 1.0, 'C': 1.0, 'T': 0.0, 'G': 1.0}\ndist_set_2: {'A': 1.0, 'C': 1.0, 'T': 0.0, 'G': 1.0}\ndist_set_3: {'A': 1.0, 'C': 0.0, 'T': 1.0, 'G': 1.0}\ndist_set_4: {'A': 1.0, 'C': 0.0, 'T': 1.0, 'G': 1.0}\ndist_set_5: {'A': 1.0, 'C': 0.0, 'T': 1.0, 'G': 1.0}\nseq: ATTCCC"]
i2 [label="i2\ndist_set_0: {'A': 0.0, 'C': 2.0, 'T': 2.0, 'G': 2.0}\ndist_set_1: {'A': 2.0, 'C': 0.0, 'T': 2.0, 'G': 2.0}\ndist_set_2: {'A': 2.0, 'C': 2.0, 'T': 0.0, 'G': 2.0}\ndist_set_3: {'A': 2.0, 'C': 2.0, 'T': 2.0, 'G': 0.0}\ndist_set_4: {'A': 2.0, 'C': 1.0, 'T': 2.0, 'G': 1.0}\ndist_set_5: {'A': 2.0, 'C': 2.0, 'T': 0.0, 'G': 2.0}\nseq: ACTGCT"]
i0 -- i2 [label="score: 3.0"]
i1 -- Bear [label="score: 0.0"]
i0 -- i1 [label="score: 0.0"]
i0 -- Elephant [label="score: 1.0"]
i0 -- Kangaroo [label="score: 1.0"]
i2 -- Cat [label="score: 1.0"]
i2 -- Lion [label="score: 0.0"]
}
```

After applying the nearest neighbour interchange heuristic, the tree updated to have a parismony score of 6.0 vs the original score of 9.0

</div>

`{bm-enable-all}`

