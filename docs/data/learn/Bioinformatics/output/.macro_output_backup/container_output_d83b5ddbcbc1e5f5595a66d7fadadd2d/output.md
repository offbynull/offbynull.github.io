<div style="border:1px solid black;">

`{bm-disable-all}`

The graph...

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[fontname="Courier-Bold", fontsize=10]
i0
i1
i2
v0
v1
v2
v3
v4
v5
v0 -- i0 [label="11"]
v1 -- i0 [label="2"]
v2 -- i0 [label="10"]
i0 -- i1 [label="4"]
i1 -- i2 [label="3"]
i2 -- v3 [label="3"]
i2 -- v4 [label="4"]
i1 -- v5 [label="7"]
}
```

... is a simple tree.

</div>

`{bm-enable-all}`

