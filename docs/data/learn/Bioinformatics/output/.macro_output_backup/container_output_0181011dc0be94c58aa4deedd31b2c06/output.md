<div style="border:1px solid black;">

`{bm-disable-all}`

The tree...

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
v0 -- i0 [label="11.0"]
v1 -- i0 [label="2.0"]
v2 -- i0 [label="10.0"]
i0 -- i1 [label="4.0"]
i1 -- i2 [label="3.0"]
i2 -- v3 [label="3.0"]
i1 -- v4 [label="7.0"]
}
```

... simplifies to ...

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[fontname="Courier-Bold", fontsize=10]
i0
i1
v0
v1
v2
v3
v4
v0 -- i0 [label="11.0"]
v1 -- i0 [label="2.0"]
v2 -- i0 [label="10.0"]
i0 -- i1 [label="4.0"]
i1 -- v4 [label="7.0"]
v3 -- i1 [label="6.0"]
}
```

</div>

`{bm-enable-all}`
