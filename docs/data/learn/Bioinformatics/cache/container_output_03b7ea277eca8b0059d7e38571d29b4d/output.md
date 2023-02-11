<div style="border:1px solid black;">

`{bm-disable-all}`

Building HMM alignment chain (from w's perspective), using the following settings...

```
v_sequence: hi
w_sequence: qi

```

The following HMM was produced ...

```{dot}
digraph G {
 graph[rankdir=LR]
 node[shape=egg, fontname="Courier-Bold", fontsize=10]
 edge[fontname="Courier-Bold", fontsize=10]
"STATE_D,0,1" [label="D,0,1"]
"STATE_D,0,2" [label="D,0,2"]
"STATE_D,1,1" [label="D,1,1"]
"STATE_D,1,2" [label="D,1,2"]
"STATE_D,2,1" [label="D,2,1"]
"STATE_D,2,2" [label="D,2,2"]
"STATE_E,1,0" [label="E,1,0"]
"STATE_E,1,1" [label="E,1,1"]
"STATE_E,1,2" [label="E,1,2"]
"STATE_E,2,0" [label="E,2,0"]
"STATE_E,2,1" [label="E,2,1"]
"STATE_E,2,2" [label="E,2,2"]
"STATE_S,-1,-1" [label="S,-1,-1"]
"STATE_D,0,1" -> "STATE_D,0,2" [label="nan"]
"STATE_D,0,1" -> "STATE_E,1,1" [label="nan"]
"STATE_D,0,1" -> "STATE_E,1,2" [label="nan"]
"STATE_D,0,2" -> "STATE_E,1,2" [label="nan"]
"STATE_D,1,1" -> "STATE_D,1,2" [label="nan"]
"STATE_D,1,1" -> "STATE_E,2,1" [label="nan"]
"STATE_D,1,1" -> "STATE_E,2,2" [label="nan"]
"STATE_D,1,2" -> "STATE_E,2,2" [label="nan"]
"STATE_D,2,1" -> "STATE_D,2,2" [label="nan"]
"STATE_E,1,0" -> "STATE_D,1,1" [label="nan"]
"STATE_E,1,0" -> "STATE_E,2,0" [label="nan"]
"STATE_E,1,0" -> "STATE_E,2,1" [label="nan"]
"STATE_E,1,1" -> "STATE_D,1,2" [label="nan"]
"STATE_E,1,1" -> "STATE_E,2,1" [label="nan"]
"STATE_E,1,1" -> "STATE_E,2,2" [label="nan"]
"STATE_E,1,2" -> "STATE_E,2,2" [label="nan"]
"STATE_E,2,0" -> "STATE_D,2,1" [label="nan"]
"STATE_E,2,1" -> "STATE_D,2,2" [label="nan"]
"STATE_S,-1,-1" -> "STATE_D,0,1" [label="nan"]
"STATE_S,-1,-1" -> "STATE_E,1,0" [label="nan"]
"STATE_S,-1,-1" -> "STATE_E,1,1" [label="nan"]
"SYMBOL_h" [label="h", style="dashed"]
"STATE_E,1,0" -> "SYMBOL_h" [label="1.0", style="dashed"]
"STATE_E,1,1" -> "SYMBOL_h" [label="1.0", style="dashed"]
"STATE_E,1,2" -> "SYMBOL_h" [label="1.0", style="dashed"]
"SYMBOL_i" [label="i", style="dashed"]
"STATE_E,2,0" -> "SYMBOL_i" [label="1.0", style="dashed"]
"STATE_E,2,1" -> "SYMBOL_i" [label="1.0", style="dashed"]
"STATE_E,2,2" -> "SYMBOL_i" [label="1.0", style="dashed"]
}
```

</div>

`{bm-enable-all}`

