<div style="border:1px solid black;">

`{bm-disable-all}`

The tree...

```{dot}
graph G {
 graph[rankdir=BT]
 node[shape=egg, fontname="Courier-Bold", fontsize=10]
 edge[fontname="Courier-Bold", fontsize=10]
Bear [label="Bear\nATTCCC"]
Cat [label="Cat\nACTGGT"]
Lion [label="Lion\nACTGCT"]
i0 [label="i0\nACTGCT"]
i1 [label="i1\nATTGCC"]
Cat -- i0 [label="None"]
Lion -- i0 [label="None"]
i0 -- i1 [label="None"]
Bear -- i1 [label="None"]
}
```

... has a parsimony score of ...

4.0

```{dot}
graph G {
 graph[rankdir=BT]
 node[shape=egg, fontname="Courier-Bold", fontsize=10]
 edge[fontname="Courier-Bold", fontsize=10]
Bear [label="Bear\nATTCCC"]
Cat [label="Cat\nACTGGT"]
Lion [label="Lion\nACTGCT"]
i0 [label="i0\nACTGCT"]
i1 [label="i1\nATTGCC"]
Cat -- i0 [label="1"]
Lion -- i0 [label="0"]
i0 -- i1 [label="2"]
Bear -- i1 [label="1"]
}
```

</div>

`{bm-enable-all}`

