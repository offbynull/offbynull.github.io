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
Lion [label="Lion\nseq: ACTGCT"]
i0 [label="i0\n"]
i1 [label="i1\n"]
Cat -- i0 [label=""]
Lion -- i0 [label=""]
i0 -- i1 [label=""]
Bear -- i1 [label=""]
}
```

... with i0 set as its root ...

... and the distances ...

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

... has the following inferred ancestor sequences ...

```{dot}
graph G {
 graph[rankdir=BT]
 node[shape=box, fontname="Courier-Bold", fontsize=10]
 edge[fontname="Courier-Bold", fontsize=10]
 layout=fdp
Bear [label="Bear\nseq: ATTCCC\ndist_set_0: {'A': 0.0, 'C': inf, 'T': inf, 'G': inf}\ndist_set_1: {'A': inf, 'C': inf, 'T': 0.0, 'G': inf}\ndist_set_2: {'A': inf, 'C': inf, 'T': 0.0, 'G': inf}\ndist_set_3: {'A': inf, 'C': 0.0, 'T': inf, 'G': inf}\ndist_set_4: {'A': inf, 'C': 0.0, 'T': inf, 'G': inf}\ndist_set_5: {'A': inf, 'C': 0.0, 'T': inf, 'G': inf}"]
Cat [label="Cat\nseq: ACTGGT\ndist_set_0: {'A': 0.0, 'C': inf, 'T': inf, 'G': inf}\ndist_set_1: {'A': inf, 'C': 0.0, 'T': inf, 'G': inf}\ndist_set_2: {'A': inf, 'C': inf, 'T': 0.0, 'G': inf}\ndist_set_3: {'A': inf, 'C': inf, 'T': inf, 'G': 0.0}\ndist_set_4: {'A': inf, 'C': inf, 'T': inf, 'G': 0.0}\ndist_set_5: {'A': inf, 'C': inf, 'T': 0.0, 'G': inf}"]
Lion [label="Lion\nseq: ACTGCT\ndist_set_0: {'A': 0.0, 'C': inf, 'T': inf, 'G': inf}\ndist_set_1: {'A': inf, 'C': 0.0, 'T': inf, 'G': inf}\ndist_set_2: {'A': inf, 'C': inf, 'T': 0.0, 'G': inf}\ndist_set_3: {'A': inf, 'C': inf, 'T': inf, 'G': 0.0}\ndist_set_4: {'A': inf, 'C': 0.0, 'T': inf, 'G': inf}\ndist_set_5: {'A': inf, 'C': inf, 'T': 0.0, 'G': inf}"]
i0 [label="i0\ndist_set_0: {'A': 0.0, 'C': 3.0, 'T': 3.0, 'G': 3.0}\ndist_set_1: {'A': 3.0, 'C': 1.0, 'T': 2.0, 'G': 3.0}\ndist_set_2: {'A': 3.0, 'C': 3.0, 'T': 0.0, 'G': 3.0}\ndist_set_3: {'A': 3.0, 'C': 2.0, 'T': 3.0, 'G': 1.0}\ndist_set_4: {'A': 3.0, 'C': 1.0, 'T': 3.0, 'G': 2.0}\ndist_set_5: {'A': 3.0, 'C': 2.0, 'T': 1.0, 'G': 3.0}\nseq: ACTGCT"]
i1 [label="i1\ndist_set_0: {'A': 0.0, 'C': 1.0, 'T': 1.0, 'G': 1.0}\ndist_set_1: {'A': 1.0, 'C': 1.0, 'T': 0.0, 'G': 1.0}\ndist_set_2: {'A': 1.0, 'C': 1.0, 'T': 0.0, 'G': 1.0}\ndist_set_3: {'A': 1.0, 'C': 0.0, 'T': 1.0, 'G': 1.0}\ndist_set_4: {'A': 1.0, 'C': 0.0, 'T': 1.0, 'G': 1.0}\ndist_set_5: {'A': 1.0, 'C': 0.0, 'T': 1.0, 'G': 1.0}\nseq: ATTCCC"]
Cat -- i0 [label=""]
Lion -- i0 [label=""]
i0 -- i1 [label=""]
Bear -- i1 [label=""]
}
```

</div>

`{bm-enable-all}`

