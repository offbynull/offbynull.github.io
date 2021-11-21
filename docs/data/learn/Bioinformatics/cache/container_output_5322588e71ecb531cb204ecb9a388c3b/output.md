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


... has a parsimony score of 4.0...

```{dot}
graph G {
 graph[rankdir=BT]
 node[shape=box, fontname="Courier-Bold", fontsize=10]
 edge[fontname="Courier-Bold", fontsize=10]
 layout=fdp
Bear [label="Bear\nseq: ATTCCC"]
Cat [label="Cat\nseq: ACTGGT"]
Lion [label="Lion\nseq: ACTGCT"]
i0 [label="i0\nseq: ACTGCT"]
i1 [label="i1\nseq: ATTCCC"]
Cat -- i0 [label="score: 1.0"]
Lion -- i0 [label="score: 0.0"]
i0 -- i1 [label="score: 3.0"]
Bear -- i1 [label="score: 0.0"]
}
```

</div>

`{bm-enable-all}`

