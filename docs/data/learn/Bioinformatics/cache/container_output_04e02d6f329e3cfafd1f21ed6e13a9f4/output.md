<div style="border:1px solid black;">

`{bm-disable-all}`

Building HMM alignment chain (from w's perspective), using the following settings...

```
v_element: n
w_element: a
# If a probability doesn't have an override listed, it'll be set to 1.0. It doesn't matter if the
# probabilities are normalized (between 0 and 1 + each hidden state'soutgoing transitions summing
# to 1) because the pseudocount addition (below) will normalize them.
transition_probability_overrides:
  S,-1,-1: {'D,0,1': 0.4, 'E,1,0': 0.6, 'E,1,1': 0.0}
  D,0,1:   {'E,1,1': 1.0}
  E,1,0:   {'D,1,1': 1.0}
  E,1,1:   {'T,1,1': 1.0}
  D,1,1:   {'T,1,1': 1.0}
pseudocount: 0.0001

```

The following HMM was produced AFTER applying pseudocounts ...

```{dot}
digraph G {
 graph[rankdir=LR]
 node[shape=egg, fontname="Courier-Bold", fontsize=10]
 edge[fontname="Courier-Bold", fontsize=10]
"STATE_D,0,1" [label="D,0,1"]
"STATE_D,1,1" [label="D,1,1"]
"STATE_E,1,0" [label="E,1,0"]
"STATE_E,1,1" [label="E,1,1"]
"STATE_S,-1,-1" [label="S,-1,-1"]
"STATE_T,1,1" [label="T,1,1"]
"STATE_D,0,1" -> "STATE_E,1,1" [label="1.0"]
"STATE_D,1,1" -> "STATE_T,1,1" [label="1.0"]
"STATE_E,1,0" -> "STATE_D,1,1" [label="1.0"]
"STATE_E,1,1" -> "STATE_T,1,1" [label="1.0"]
"STATE_S,-1,-1" -> "STATE_D,0,1" [label="0.39998000599820055"]
"STATE_S,-1,-1" -> "STATE_E,1,0" [label="0.5999200239928022"]
"STATE_S,-1,-1" -> "STATE_E,1,1" [label="9.997000899730082e-05"]
"SYMBOL_n" [label="n", style="dashed"]
"STATE_E,1,0" -> "SYMBOL_n" [label="1.0", style="dashed"]
"STATE_E,1,1" -> "SYMBOL_n" [label="1.0", style="dashed"]
"SYMBOL_?" [label="?", style="dashed"]
"STATE_T,1,1" -> "SYMBOL_?" [label="1.0", style="dashed"]
}
```

The following Viterbi graph was produced for the HMM and the emitted sequence n ...

```{dot}
digraph G {
 graph[rankdir=LR]
 node[shape=egg, fontname="Courier-Bold", fontsize=10]
 edge[fontname="Courier-Bold", fontsize=10]
"(-1, 'D,0,1')" [label="(-1, 'D,0,1')"]
"(-1, 'S,-1,-1')" [label="(-1, 'S,-1,-1')"]
"(-1, 'VITERBI_SINK')" [label="(-1, 'VITERBI_SINK')"]
"(0, 'D,1,1')" [label="(0, 'D,1,1')"]
"(0, 'E,1,0')" [label="(0, 'E,1,0')"]
"(0, 'E,1,1')" [label="(0, 'E,1,1')"]
"(1, 'T,1,1')" [label="(1, 'T,1,1')"]
"(-1, 'D,0,1')" -> "(0, 'E,1,1')" [label="1.0"]
"(-1, 'S,-1,-1')" -> "(-1, 'D,0,1')" [label="0.39998000599820055"]
"(-1, 'S,-1,-1')" -> "(0, 'E,1,0')" [label="0.5999200239928022"]
"(-1, 'S,-1,-1')" -> "(0, 'E,1,1')" [label="9.997000899730082e-05"]
"(0, 'D,1,1')" -> "(1, 'T,1,1')" [label="1.0"]
"(0, 'E,1,0')" -> "(0, 'D,1,1')" [label="1.0"]
"(0, 'E,1,1')" -> "(1, 'T,1,1')" [label="1.0"]
"(1, 'T,1,1')" -> "(-1, 'VITERBI_SINK')" [label="1.0"]
}
```


The hidden path with the max product weight in this Viterbi graph is ...

```
n-
```

Most probable hidden path: [('S,-1,-1', 'E,1,0'), ('E,1,0', 'D,1,1'), ('D,1,1', 'T,1,1'), ('T,1,1', 'VITERBI_SINK')]

Most probable hidden path probability: 0.5999200239928022
</div>

`{bm-enable-all}`

