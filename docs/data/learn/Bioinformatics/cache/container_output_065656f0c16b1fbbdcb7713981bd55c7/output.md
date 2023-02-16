<div style="border:1px solid black;">

`{bm-disable-all}`

Building exploded graph after applying psuedocounts to HMM, using the following settings...

```
transition_probabilities:
  SOURCE: {A: 0.5, B: 0.5}
  A: {A: 0.377, B: 0.623}
  B: {A: 0.301, C: 0.699}
  C: {B: 1.0}
emission_probabilities:
  SOURCE: {}
  A: {y: 0.596, z: 0.404}
  B: {y: 0.572, z: 0.428}
  C: {}
  # C set to empty dicts to identify as non-emittable hidden state.
source_state: SOURCE
sink_state: SINK  # Must not exist in HMM (used only for exploded graph)
pseudocount: 0.0001
emission_len: 3

```

The following HMM was produced before applying pseudocounts ...

```{dot}
digraph G {
 graph[rankdir=LR]
 node[shape=egg, fontname="Courier-Bold", fontsize=10]
 edge[fontname="Courier-Bold", fontsize=10]
"STATE_A" [label="A"]
"STATE_B" [label="B"]
"STATE_C" [label="C"]
"STATE_SOURCE" [label="SOURCE"]
"STATE_A" -> "STATE_A" [label="0.377"]
"STATE_A" -> "STATE_B" [label="0.623"]
"STATE_B" -> "STATE_A" [label="0.301"]
"STATE_B" -> "STATE_C" [label="0.699"]
"STATE_C" -> "STATE_B" [label="1.0"]
"STATE_SOURCE" -> "STATE_A" [label="0.5"]
"STATE_SOURCE" -> "STATE_B" [label="0.5"]
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="0.596", style="dashed"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="0.404", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="0.572", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="0.428", style="dashed"]
}
```

After pseudocounts are applied, the HMM becomes as follows ...

```{dot}
digraph G {
 graph[rankdir=LR]
 node[shape=egg, fontname="Courier-Bold", fontsize=10]
 edge[fontname="Courier-Bold", fontsize=10]
"STATE_A" [label="A"]
"STATE_B" [label="B"]
"STATE_C" [label="C"]
"STATE_SOURCE" [label="SOURCE"]
"STATE_A" -> "STATE_A" [label="0.3770245950809838"]
"STATE_A" -> "STATE_B" [label="0.6229754049190162"]
"STATE_B" -> "STATE_A" [label="0.30103979204159165"]
"STATE_B" -> "STATE_C" [label="0.6989602079584083"]
"STATE_C" -> "STATE_B" [label="1.0"]
"STATE_SOURCE" -> "STATE_A" [label="0.5"]
"STATE_SOURCE" -> "STATE_B" [label="0.5"]
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="0.5959808038392321", style="dashed"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="0.40401919616076787", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="0.571985602879424", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="0.4280143971205759", style="dashed"]
}
```

The following exploded graph was produced for the HMM and an emission length of 3 ...

```{dot}
digraph G {
 graph[rankdir=LR]
 node[shape=egg, fontname="Courier-Bold", fontsize=10]
 edge[fontname="Courier-Bold", fontsize=10]
"(-1, 'SINK', None)" [label="(-1, 'SINK', None)"]
"(-1, 'SOURCE', None)" [label="(-1, 'SOURCE', None)"]
"(0, 'A', 'y')" [label="(0, 'A', 'y')"]
"(0, 'A', 'z')" [label="(0, 'A', 'z')"]
"(0, 'B', 'y')" [label="(0, 'B', 'y')"]
"(0, 'B', 'z')" [label="(0, 'B', 'z')"]
"(0, 'C', 'y')" [label="(0, 'C', 'y')"]
"(0, 'C', 'z')" [label="(0, 'C', 'z')"]
"(1, 'A', 'y')" [label="(1, 'A', 'y')"]
"(1, 'A', 'z')" [label="(1, 'A', 'z')"]
"(1, 'B', 'y')" [label="(1, 'B', 'y')"]
"(1, 'B', 'z')" [label="(1, 'B', 'z')"]
"(1, 'C', 'y')" [label="(1, 'C', 'y')"]
"(1, 'C', 'z')" [label="(1, 'C', 'z')"]
"(2, 'A', 'y')" [label="(2, 'A', 'y')"]
"(2, 'A', 'z')" [label="(2, 'A', 'z')"]
"(2, 'B', 'y')" [label="(2, 'B', 'y')"]
"(2, 'B', 'z')" [label="(2, 'B', 'z')"]
"(2, 'C', 'y')" [label="(2, 'C', 'y')"]
"(2, 'C', 'z')" [label="(2, 'C', 'z')"]
"(-1, 'SOURCE', None)" -> "(0, 'A', 'y')"
"(-1, 'SOURCE', None)" -> "(0, 'A', 'z')"
"(-1, 'SOURCE', None)" -> "(0, 'B', 'y')"
"(-1, 'SOURCE', None)" -> "(0, 'B', 'z')"
"(0, 'A', 'y')" -> "(1, 'A', 'y')"
"(0, 'A', 'y')" -> "(1, 'A', 'z')"
"(0, 'A', 'y')" -> "(1, 'B', 'y')"
"(0, 'A', 'y')" -> "(1, 'B', 'z')"
"(0, 'A', 'z')" -> "(1, 'A', 'y')"
"(0, 'A', 'z')" -> "(1, 'A', 'z')"
"(0, 'A', 'z')" -> "(1, 'B', 'y')"
"(0, 'A', 'z')" -> "(1, 'B', 'z')"
"(0, 'B', 'y')" -> "(0, 'C', 'y')"
"(0, 'B', 'y')" -> "(0, 'C', 'z')"
"(0, 'B', 'y')" -> "(1, 'A', 'y')"
"(0, 'B', 'y')" -> "(1, 'A', 'z')"
"(0, 'B', 'z')" -> "(0, 'C', 'y')"
"(0, 'B', 'z')" -> "(0, 'C', 'z')"
"(0, 'B', 'z')" -> "(1, 'A', 'y')"
"(0, 'B', 'z')" -> "(1, 'A', 'z')"
"(0, 'C', 'y')" -> "(1, 'B', 'y')"
"(0, 'C', 'y')" -> "(1, 'B', 'z')"
"(0, 'C', 'z')" -> "(1, 'B', 'y')"
"(0, 'C', 'z')" -> "(1, 'B', 'z')"
"(1, 'A', 'y')" -> "(2, 'A', 'y')"
"(1, 'A', 'y')" -> "(2, 'A', 'z')"
"(1, 'A', 'y')" -> "(2, 'B', 'y')"
"(1, 'A', 'y')" -> "(2, 'B', 'z')"
"(1, 'A', 'z')" -> "(2, 'A', 'y')"
"(1, 'A', 'z')" -> "(2, 'A', 'z')"
"(1, 'A', 'z')" -> "(2, 'B', 'y')"
"(1, 'A', 'z')" -> "(2, 'B', 'z')"
"(1, 'B', 'y')" -> "(1, 'C', 'y')"
"(1, 'B', 'y')" -> "(1, 'C', 'z')"
"(1, 'B', 'y')" -> "(2, 'A', 'y')"
"(1, 'B', 'y')" -> "(2, 'A', 'z')"
"(1, 'B', 'z')" -> "(1, 'C', 'y')"
"(1, 'B', 'z')" -> "(1, 'C', 'z')"
"(1, 'B', 'z')" -> "(2, 'A', 'y')"
"(1, 'B', 'z')" -> "(2, 'A', 'z')"
"(1, 'C', 'y')" -> "(2, 'B', 'y')"
"(1, 'C', 'y')" -> "(2, 'B', 'z')"
"(1, 'C', 'z')" -> "(2, 'B', 'y')"
"(1, 'C', 'z')" -> "(2, 'B', 'z')"
"(2, 'A', 'y')" -> "(-1, 'SINK', None)"
"(2, 'A', 'z')" -> "(-1, 'SINK', None)"
"(2, 'B', 'y')" -> "(-1, 'SINK', None)"
"(2, 'B', 'y')" -> "(2, 'C', 'y')"
"(2, 'B', 'y')" -> "(2, 'C', 'z')"
"(2, 'B', 'z')" -> "(-1, 'SINK', None)"
"(2, 'B', 'z')" -> "(2, 'C', 'y')"
"(2, 'B', 'z')" -> "(2, 'C', 'z')"
"(2, 'C', 'y')" -> "(-1, 'SINK', None)"
"(2, 'C', 'z')" -> "(-1, 'SINK', None)"
}
```

</div>

`{bm-enable-all}`

