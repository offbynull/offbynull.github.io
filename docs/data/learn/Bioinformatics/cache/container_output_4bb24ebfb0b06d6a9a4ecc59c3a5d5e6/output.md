<div style="border:1px solid black;">

`{bm-disable-all}`

Building profile using the following settings...

```
sequence: [A, B, C]
alignment:
  - [G, -, T, -, C]
  - [-, C, T, A, -]
  - [-, T, T, A, -]
  - [-, -, T, -, C]
  - [G, -, -, -, -]
column_removal_threshold: 0.59

```

The following HMM was produced (structure only, no probabilities)...

```{dot}
digraph G {
 graph[rankdir=LR]
 node[shape=egg, fontname="Courier-Bold", fontsize=10]
 edge[fontname="Courier-Bold", fontsize=10]
"STATE_D,0,1" [label="D,0,1"]
"STATE_D,1,1" [label="D,1,1"]
"STATE_D,2,1" [label="D,2,1"]
"STATE_D,3,1" [label="D,3,1"]
"STATE_I,1,0" [label="I,1,0"]
"STATE_I,1,1" [label="I,1,1"]
"STATE_I,2,0" [label="I,2,0"]
"STATE_I,2,1" [label="I,2,1"]
"STATE_I,3,0" [label="I,3,0"]
"STATE_I,3,1" [label="I,3,1"]
"STATE_M,1,1" [label="M,1,1"]
"STATE_M,2,1" [label="M,2,1"]
"STATE_M,3,1" [label="M,3,1"]
"STATE_S,0,0" [label="S,0,0"]
"STATE_T,3,1" [label="T,3,1"]
"STATE_D,0,1" -> "STATE_I,1,1" [label="nan"]
"STATE_D,1,1" -> "STATE_I,2,1" [label="nan"]
"STATE_D,2,1" -> "STATE_I,3,1" [label="nan"]
"STATE_D,3,1" -> "STATE_T,3,1" [label="nan"]
"STATE_I,1,0" -> "STATE_D,1,1" [label="nan"]
"STATE_I,1,0" -> "STATE_I,2,0" [label="nan"]
"STATE_I,1,0" -> "STATE_M,2,1" [label="nan"]
"STATE_I,1,1" -> "STATE_I,2,1" [label="nan"]
"STATE_I,2,0" -> "STATE_D,2,1" [label="nan"]
"STATE_I,2,0" -> "STATE_I,3,0" [label="nan"]
"STATE_I,2,0" -> "STATE_M,3,1" [label="nan"]
"STATE_I,2,1" -> "STATE_I,3,1" [label="nan"]
"STATE_I,3,0" -> "STATE_D,3,1" [label="nan"]
"STATE_I,3,1" -> "STATE_T,3,1" [label="nan"]
"STATE_M,1,1" -> "STATE_I,2,1" [label="nan"]
"STATE_M,2,1" -> "STATE_I,3,1" [label="nan"]
"STATE_M,3,1" -> "STATE_T,3,1" [label="nan"]
"STATE_S,0,0" -> "STATE_D,0,1" [label="nan"]
"STATE_S,0,0" -> "STATE_I,1,0" [label="nan"]
"STATE_S,0,0" -> "STATE_M,1,1" [label="nan"]
"SYMBOL_A" [label="A", style="dashed"]
"STATE_I,1,0" -> "SYMBOL_A" [label="1.0", style="dashed"]
"STATE_I,1,1" -> "SYMBOL_A" [label="1.0", style="dashed"]
"SYMBOL_B" [label="B", style="dashed"]
"STATE_I,2,0" -> "SYMBOL_B" [label="1.0", style="dashed"]
"STATE_I,2,1" -> "SYMBOL_B" [label="1.0", style="dashed"]
"SYMBOL_C" [label="C", style="dashed"]
"STATE_I,3,0" -> "SYMBOL_C" [label="1.0", style="dashed"]
"STATE_I,3,1" -> "SYMBOL_C" [label="1.0", style="dashed"]
"STATE_M,1,1" -> "SYMBOL_A" [label="1.0", style="dashed"]
"STATE_M,2,1" -> "SYMBOL_B" [label="1.0", style="dashed"]
"STATE_M,3,1" -> "SYMBOL_C" [label="1.0", style="dashed"]
"SYMBOL_?" [label="?", style="dashed"]
"STATE_T,3,1" -> "SYMBOL_?" [label="1.0", style="dashed"]
}
```

</div>

`{bm-enable-all}`

