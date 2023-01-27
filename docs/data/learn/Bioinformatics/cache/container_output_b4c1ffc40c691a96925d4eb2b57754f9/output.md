<div style="border:1px solid black;">

`{bm-disable-all}`

Finding the probability of an HMM emitting a sequence, using the following settings...

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
sink_state: SINK  # Must not exist in HMM (used only for Viterbi graph)
pseudocount: 0.0001
emission_len: 3

```

The following HMM was produced AFTER applying pseudocounts ...

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

The following exploded graph forward and layer backtracking pointers were produced for the exploded graph...

```{dot}
digraph G {
 graph[rankdir=LR]
 node[shape=egg, fontname="Courier-Bold", fontsize=10]
 edge[fontname="Courier-Bold", fontsize=10]
"(-1, 'SINK', None)" [label="(-1, 'SINK', None)\n('y', 0.287526321185488)"]
"(-1, 'SOURCE', None)" [label="(-1, 'SOURCE', None)\n(None, 1.0)"]
"(0, 'A', 'y')" [label="(0, 'A', 'y')\n(None, 0.29799040191961607)"]
"(0, 'A', 'z')" [label="(0, 'A', 'z')\n(None, 0.20200959808038393)"]
"(0, 'B', 'y')" [label="(0, 'B', 'y')\n(None, 0.285992801439712)"]
"(0, 'B', 'z')" [label="(0, 'B', 'z')\n(None, 0.21400719856028794)"]
"(0, 'C', 'y')" [label="(0, 'C', 'y')\n('y', 0.19989758796890889)"]
"(0, 'C', 'z')" [label="(0, 'C', 'z')\n('y', 0.19989758796890889)"]
"(1, 'A', 'y')" [label="(1, 'A', 'y')\n('y', 0.11826936537850288)"]
"(1, 'A', 'z')" [label="(1, 'A', 'z')\n('y', 0.0801755587140631)"]
"(1, 'B', 'y')" [label="(1, 'B', 'y')\n('y', 0.22052234509949464)"]
"(1, 'B', 'z')" [label="(1, 'B', 'z')\n('y', 0.1650159341672674)"]
"(1, 'C', 'y')" [label="(1, 'C', 'y')\n('y', 0.15413634419021865)"]
"(1, 'C', 'z')" [label="(1, 'C', 'z')\n('y', 0.15413634419021865)"]
"(2, 'A', 'y')" [label="(2, 'A', 'y')\n('y', 0.06613984013697097)"]
"(2, 'A', 'z')" [label="(2, 'A', 'z')\n('y', 0.04483662036461998)"]
"(2, 'B', 'y')" [label="(2, 'B', 'y')\n('y', 0.1303070431028816)"]
"(2, 'B', 'z')" [label="(2, 'B', 'z')\n('y', 0.09750820687352495)"]
"(2, 'C', 'y')" [label="(2, 'C', 'y')\n('y', 0.0910794379456354)"]
"(2, 'C', 'z')" [label="(2, 'C', 'z')\n('y', 0.0910794379456354)"]
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

Between all emissions of length 3, the emitted sequence with the max probability is 0.287526321185488 ...

</div>

`{bm-enable-all}`

