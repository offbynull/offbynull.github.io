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

... can have any of the following nearest neighbour swaps on edge i0-i1...


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
i0 -- i1 [label=""]
i0 -- Cat [label=""]
i0 -- Bear [label=""]
i1 -- Lion [label=""]
}
```


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
i0 -- i1 [label=""]
i0 -- Lion [label=""]
i0 -- Bear [label=""]
i1 -- Cat [label=""]
}
```

</div>

`{bm-enable-all}`

