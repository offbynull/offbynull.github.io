<div style="border:1px solid black;">

`{bm-disable-all}`

Building HMM alignment square (from w's perspective), using the following settings...

```
v_element: n
w_element: a

```

The following HMM was produced ...

```{dot}
digraph G {
 graph[rankdir=LR]
 node[shape=egg, fontname="Courier-Bold", fontsize=10]
 edge[fontname="Courier-Bold", fontsize=10]
"STATE_D,1,0" [label="D,1,0"]
"STATE_D,1,1" [label="D,1,1"]
"STATE_E,0,1" [label="E,0,1"]
"STATE_E,1,1" [label="E,1,1"]
"STATE_S,-1,-1" [label="S,-1,-1"]
"STATE_D,1,0" -> "STATE_E,1,1" [label="nan"]
"STATE_E,0,1" -> "STATE_D,1,1" [label="nan"]
"STATE_S,-1,-1" -> "STATE_D,1,0" [label="nan"]
"STATE_S,-1,-1" -> "STATE_E,0,1" [label="nan"]
"STATE_S,-1,-1" -> "STATE_E,1,1" [label="nan"]
"SYMBOL_a" [label="a", style="dashed"]
"STATE_E,0,1" -> "SYMBOL_a" [label="1.0", style="dashed"]
"STATE_E,1,1" -> "SYMBOL_a" [label="1.0", style="dashed"]
}
```

</div>

`{bm-enable-all}`

