<div style="border:1px solid black;">

`{bm-disable-all}`

Building Viterbi graph (with non-emitting hidden states) and finding the max product weight, after applying psuedocounts to HMM, using the following settings...

```
transition_probabilities:
  SOURCE: {A: 0.5, B: 0.5}
  A: {A: 0.377, B: 0.623}
  B: {A: 0.301, C: 0.699}
  C: {B: 0.9,   D: 0.1}
  D: {B: 1.0}
emission_probabilities:
  SOURCE: {}
  A: {x: 0.176, y: 0.596, z: 0.228}
  B: {x: 0.225, y: 0.572, z: 0.203}
  C: {}
  D: {}
  # C and D set to empty dicts to identify them as non-emittable hidden states.
source_state: SOURCE
sink_state: SINK  # Must not exist in HMM (used only for Viterbi graph)
emissions: [z,z,x,x,y]
pseudocount: 0.0001

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
"STATE_D" [label="D"]
"STATE_SOURCE" [label="SOURCE"]
"STATE_A" -> "STATE_A" [label="0.377"]
"STATE_A" -> "STATE_B" [label="0.623"]
"STATE_B" -> "STATE_A" [label="0.301"]
"STATE_B" -> "STATE_C" [label="0.699"]
"STATE_C" -> "STATE_B" [label="0.9"]
"STATE_C" -> "STATE_D" [label="0.1"]
"STATE_D" -> "STATE_B" [label="1.0"]
"STATE_SOURCE" -> "STATE_A" [label="0.5"]
"STATE_SOURCE" -> "STATE_B" [label="0.5"]
"SYMBOL_x" [label="x", style="dashed"]
"STATE_A" -> "SYMBOL_x" [label="0.176", style="dashed"]
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="0.596", style="dashed"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="0.228", style="dashed"]
"STATE_B" -> "SYMBOL_x" [label="0.225", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="0.572", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="0.203", style="dashed"]
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
"STATE_D" [label="D"]
"STATE_SOURCE" [label="SOURCE"]
"STATE_A" -> "STATE_A" [label="0.3770245950809838"]
"STATE_A" -> "STATE_B" [label="0.6229754049190162"]
"STATE_B" -> "STATE_A" [label="0.30103979204159165"]
"STATE_B" -> "STATE_C" [label="0.6989602079584083"]
"STATE_C" -> "STATE_B" [label="0.8999200159968007"]
"STATE_C" -> "STATE_D" [label="0.10007998400319937"]
"STATE_D" -> "STATE_B" [label="1.0"]
"STATE_SOURCE" -> "STATE_A" [label="0.5"]
"STATE_SOURCE" -> "STATE_B" [label="0.5"]
"SYMBOL_x" [label="x", style="dashed"]
"STATE_A" -> "SYMBOL_x" [label="0.17604718584424672", style="dashed"]
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="0.5959212236329101", style="dashed"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="0.22803159052284316", style="dashed"]
"STATE_B" -> "SYMBOL_x" [label="0.22503249025292413", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="0.5719284214735579", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="0.20303908827351796", style="dashed"]
}
```

The following Viterbi graph was produced for the HMM and the emitted sequence ['z', 'z', 'x', 'x', 'y'] ...

```{dot}
digraph G {
 graph[rankdir=LR]
 node[shape=egg, fontname="Courier-Bold", fontsize=10]
 edge[fontname="Courier-Bold", fontsize=10]
"(-1, 'SINK')" [label="(-1, 'SINK')"]
"(-1, 'SOURCE')" [label="(-1, 'SOURCE')"]
"(0, 'A')" [label="(0, 'A')"]
"(0, 'B')" [label="(0, 'B')"]
"(0, 'C')" [label="(0, 'C')"]
"(0, 'D')" [label="(0, 'D')"]
"(1, 'A')" [label="(1, 'A')"]
"(1, 'B')" [label="(1, 'B')"]
"(1, 'C')" [label="(1, 'C')"]
"(1, 'D')" [label="(1, 'D')"]
"(2, 'A')" [label="(2, 'A')"]
"(2, 'B')" [label="(2, 'B')"]
"(2, 'C')" [label="(2, 'C')"]
"(2, 'D')" [label="(2, 'D')"]
"(3, 'A')" [label="(3, 'A')"]
"(3, 'B')" [label="(3, 'B')"]
"(3, 'C')" [label="(3, 'C')"]
"(3, 'D')" [label="(3, 'D')"]
"(4, 'A')" [label="(4, 'A')"]
"(4, 'B')" [label="(4, 'B')"]
"(4, 'C')" [label="(4, 'C')"]
"(4, 'D')" [label="(4, 'D')"]
"(-1, 'SOURCE')" -> "(0, 'A')" [label="0.11401579526142158"]
"(-1, 'SOURCE')" -> "(0, 'B')" [label="0.10151954413675898"]
"(0, 'A')" -> "(1, 'A')" [label="0.08597351808254765"]
"(0, 'A')" -> "(1, 'B')" [label="0.12648835823158272"]
"(0, 'B')" -> "(0, 'C')" [label="0.6989602079584083"]
"(0, 'B')" -> "(1, 'A')" [label="0.06864658258991009"]
"(0, 'C')" -> "(0, 'D')" [label="0.10007998400319937"]
"(0, 'C')" -> "(1, 'B')" [label="0.18271893956708013"]
"(0, 'D')" -> "(1, 'B')" [label="0.20303908827351796"]
"(1, 'A')" -> "(2, 'A')" [label="0.06637411895807382"]
"(1, 'A')" -> "(2, 'B')" [label="0.14018970673524997"]
"(1, 'B')" -> "(1, 'C')" [label="0.6989602079584083"]
"(1, 'B')" -> "(2, 'A')" [label="0.05299720821605947"]
"(1, 'C')" -> "(1, 'D')" [label="0.10007998400319937"]
"(1, 'C')" -> "(2, 'B')" [label="0.20251124222821137"]
"(1, 'D')" -> "(2, 'B')" [label="0.22503249025292413"]
"(2, 'A')" -> "(3, 'A')" [label="0.06637411895807382"]
"(2, 'A')" -> "(3, 'B')" [label="0.14018970673524997"]
"(2, 'B')" -> "(2, 'C')" [label="0.6989602079584083"]
"(2, 'B')" -> "(3, 'A')" [label="0.05299720821605947"]
"(2, 'C')" -> "(2, 'D')" [label="0.10007998400319937"]
"(2, 'C')" -> "(3, 'B')" [label="0.20251124222821137"]
"(2, 'D')" -> "(3, 'B')" [label="0.22503249025292413"]
"(3, 'A')" -> "(4, 'A')" [label="0.22467695804036233"]
"(3, 'A')" -> "(4, 'B')" [label="0.3562973399521835"]
"(3, 'B')" -> "(3, 'C')" [label="0.6989602079584083"]
"(3, 'B')" -> "(4, 'A')" [label="0.17939600123562208"]
"(3, 'C')" -> "(3, 'D')" [label="0.10007998400319937"]
"(3, 'C')" -> "(4, 'B')" [label="0.5146898342015093"]
"(3, 'D')" -> "(4, 'B')" [label="0.5719284214735579"]
"(4, 'A')" -> "(-1, 'SINK')" [label="1.0"]
"(4, 'B')" -> "(-1, 'SINK')" [label="1.0"]
"(4, 'B')" -> "(4, 'C')" [label="0.6989602079584083"]
"(4, 'C')" -> "(-1, 'SINK')" [label="1.0"]
"(4, 'C')" -> "(4, 'D')" [label="0.10007998400319937"]
"(4, 'D')" -> "(-1, 'SINK')" [label="1.0"]
}
```

The hidden path with the max product weight in this Viterbi graph is [('SOURCE', 'A'), ('A', 'B'), ('B', 'C'), ('C', 'B'), ('B', 'C'), ('C', 'B'), ('B', 'C'), ('C', 'B'), ('B', 'SINK')] (max product weight = 0.00010394815803486232).

</div>

`{bm-enable-all}`

