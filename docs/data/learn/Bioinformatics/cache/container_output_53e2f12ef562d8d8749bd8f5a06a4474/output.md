<div style="border:1px solid black;">

`{bm-disable-all}`

Building HMM alignment chain (from w's perspective), using the following settings...

```
v_sequence: [h, i]
w_sequence: [q, i]
# If a probability doesn't have an override listed, it'll be set to 1.0. It doesn't matter if the
# probabilities are normalized (between 0 and 1 + each hidden state'soutgoing transitions summing
# to 1) because the pseudocount addition (below) will normalize them.
transition_probability_overrides:
  S,-1,-1: {'D,0,1': 0.4, 'I,1,0': 0.6, 'M,1,1': 0.0}
  I,1,0:   {'I,2,0': 0.4, 'D,1,1': 0.6, 'M,2,1': 0.0}
  D,0,1:   {'D,0,2': 0.5, 'I,1,1': 0.5, 'M,1,2': 0.0}
  D,1,2:   {'I,2,2': 1.0}
  M,1,1:   {'D,1,2': 0.0, 'I,2,1': 0.0, 'M,2,2': 1.0}
  I,1,1:   {'D,1,2': 0.0, 'I,2,1': 0.0, 'M,2,2': 1.0}
  D,1,1:   {'D,1,2': 0.0, 'I,2,1': 0.0, 'M,2,2': 1.0}
  D,0,2:   {'I,1,2': 1.0}
  I,1,2:   {'I,2,2': 1.0}
  M,1,2:   {'I,2,2': 1.0}
  I,2,0:   {'D,2,1': 1.0}
  D,2,1:   {'D,2,2': 1.0}
  I,2,1:   {'D,2,2': 1.0}
  M,2,1:   {'D,2,2': 1.0}
  D,2,2:   {'T,2,2': 1.0}
  M,2,2:   {'T,2,2': 1.0}
  I,2,2:   {'T,2,2': 1.0}
pseudocount: 0.0001

```

The following HMM was produced AFTER applying pseudocounts ...

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
"STATE_I,1,0" [label="I,1,0"]
"STATE_I,1,1" [label="I,1,1"]
"STATE_I,1,2" [label="I,1,2"]
"STATE_I,2,0" [label="I,2,0"]
"STATE_I,2,1" [label="I,2,1"]
"STATE_I,2,2" [label="I,2,2"]
"STATE_M,1,1" [label="M,1,1"]
"STATE_M,1,2" [label="M,1,2"]
"STATE_M,2,1" [label="M,2,1"]
"STATE_M,2,2" [label="M,2,2"]
"STATE_S,0,0" [label="S,0,0"]
"STATE_T,2,2" [label="T,2,2"]
"STATE_D,0,1" -> "STATE_D,0,2" [label="0.49995001499550135"]
"STATE_D,0,1" -> "STATE_I,1,1" [label="0.49995001499550135"]
"STATE_D,0,1" -> "STATE_M,1,2" [label="9.997000899730082e-05"]
"STATE_D,0,2" -> "STATE_I,1,2" [label="1.0"]
"STATE_D,1,1" -> "STATE_D,1,2" [label="9.997000899730082e-05"]
"STATE_D,1,1" -> "STATE_I,2,1" [label="9.997000899730082e-05"]
"STATE_D,1,1" -> "STATE_M,2,2" [label="0.9998000599820054"]
"STATE_D,1,2" -> "STATE_I,2,2" [label="1.0"]
"STATE_D,2,1" -> "STATE_D,2,2" [label="1.0"]
"STATE_D,2,2" -> "STATE_T,2,2" [label="1.0"]
"STATE_I,1,0" -> "STATE_D,1,1" [label="0.5999200239928022"]
"STATE_I,1,0" -> "STATE_I,2,0" [label="0.39998000599820055"]
"STATE_I,1,0" -> "STATE_M,2,1" [label="9.997000899730082e-05"]
"STATE_I,1,1" -> "STATE_D,1,2" [label="9.997000899730082e-05"]
"STATE_I,1,1" -> "STATE_I,2,1" [label="9.997000899730082e-05"]
"STATE_I,1,1" -> "STATE_M,2,2" [label="0.9998000599820054"]
"STATE_I,1,2" -> "STATE_I,2,2" [label="1.0"]
"STATE_I,2,0" -> "STATE_D,2,1" [label="1.0"]
"STATE_I,2,1" -> "STATE_D,2,2" [label="1.0"]
"STATE_I,2,2" -> "STATE_T,2,2" [label="1.0"]
"STATE_M,1,1" -> "STATE_D,1,2" [label="9.997000899730082e-05"]
"STATE_M,1,1" -> "STATE_I,2,1" [label="9.997000899730082e-05"]
"STATE_M,1,1" -> "STATE_M,2,2" [label="0.9998000599820054"]
"STATE_M,1,2" -> "STATE_I,2,2" [label="1.0"]
"STATE_M,2,1" -> "STATE_D,2,2" [label="1.0"]
"STATE_M,2,2" -> "STATE_T,2,2" [label="1.0"]
"STATE_S,0,0" -> "STATE_D,0,1" [label="0.3333333333333333"]
"STATE_S,0,0" -> "STATE_I,1,0" [label="0.3333333333333333"]
"STATE_S,0,0" -> "STATE_M,1,1" [label="0.3333333333333333"]
"SYMBOL_h" [label="h", style="dashed"]
"STATE_I,1,0" -> "SYMBOL_h" [label="1.0", style="dashed"]
"STATE_I,1,1" -> "SYMBOL_h" [label="1.0", style="dashed"]
"STATE_I,1,2" -> "SYMBOL_h" [label="1.0", style="dashed"]
"SYMBOL_i" [label="i", style="dashed"]
"STATE_I,2,0" -> "SYMBOL_i" [label="1.0", style="dashed"]
"STATE_I,2,1" -> "SYMBOL_i" [label="1.0", style="dashed"]
"STATE_I,2,2" -> "SYMBOL_i" [label="1.0", style="dashed"]
"STATE_M,1,1" -> "SYMBOL_h" [label="1.0", style="dashed"]
"STATE_M,1,2" -> "SYMBOL_h" [label="1.0", style="dashed"]
"STATE_M,2,1" -> "SYMBOL_i" [label="1.0", style="dashed"]
"STATE_M,2,2" -> "SYMBOL_i" [label="1.0", style="dashed"]
"SYMBOL_?" [label="?", style="dashed"]
"STATE_T,2,2" -> "SYMBOL_?" [label="1.0", style="dashed"]
}
```

The following Viterbi graph was produced for the HMM and the emitted sequence ['h', 'i'] ...

```{dot}
digraph G {
 graph[rankdir=LR]
 node[shape=egg, fontname="Courier-Bold", fontsize=10]
 edge[fontname="Courier-Bold", fontsize=10]
"(-1, 'D,0,1')" [label="(-1, 'D,0,1')"]
"(-1, 'D,0,2')" [label="(-1, 'D,0,2')"]
"(-1, 'S,0,0')" [label="(-1, 'S,0,0')"]
"(-1, 'VITERBI_SINK')" [label="(-1, 'VITERBI_SINK')"]
"(0, 'D,1,1')" [label="(0, 'D,1,1')"]
"(0, 'D,1,2')" [label="(0, 'D,1,2')"]
"(0, 'I,1,0')" [label="(0, 'I,1,0')"]
"(0, 'I,1,1')" [label="(0, 'I,1,1')"]
"(0, 'I,1,2')" [label="(0, 'I,1,2')"]
"(0, 'M,1,1')" [label="(0, 'M,1,1')"]
"(0, 'M,1,2')" [label="(0, 'M,1,2')"]
"(1, 'D,2,1')" [label="(1, 'D,2,1')"]
"(1, 'D,2,2')" [label="(1, 'D,2,2')"]
"(1, 'I,2,0')" [label="(1, 'I,2,0')"]
"(1, 'I,2,1')" [label="(1, 'I,2,1')"]
"(1, 'I,2,2')" [label="(1, 'I,2,2')"]
"(1, 'M,2,1')" [label="(1, 'M,2,1')"]
"(1, 'M,2,2')" [label="(1, 'M,2,2')"]
"(2, 'T,2,2')" [label="(2, 'T,2,2')"]
"(-1, 'D,0,1')" -> "(-1, 'D,0,2')" [label="0.49995001499550135"]
"(-1, 'D,0,1')" -> "(0, 'I,1,1')" [label="0.49995001499550135"]
"(-1, 'D,0,1')" -> "(0, 'M,1,2')" [label="9.997000899730082e-05"]
"(-1, 'D,0,2')" -> "(0, 'I,1,2')" [label="1.0"]
"(-1, 'S,0,0')" -> "(-1, 'D,0,1')" [label="0.3333333333333333"]
"(-1, 'S,0,0')" -> "(0, 'I,1,0')" [label="0.3333333333333333"]
"(-1, 'S,0,0')" -> "(0, 'M,1,1')" [label="0.3333333333333333"]
"(0, 'D,1,1')" -> "(0, 'D,1,2')" [label="9.997000899730082e-05"]
"(0, 'D,1,1')" -> "(1, 'I,2,1')" [label="9.997000899730082e-05"]
"(0, 'D,1,1')" -> "(1, 'M,2,2')" [label="0.9998000599820054"]
"(0, 'D,1,2')" -> "(1, 'I,2,2')" [label="1.0"]
"(0, 'I,1,0')" -> "(0, 'D,1,1')" [label="0.5999200239928022"]
"(0, 'I,1,0')" -> "(1, 'I,2,0')" [label="0.39998000599820055"]
"(0, 'I,1,0')" -> "(1, 'M,2,1')" [label="9.997000899730082e-05"]
"(0, 'I,1,1')" -> "(0, 'D,1,2')" [label="9.997000899730082e-05"]
"(0, 'I,1,1')" -> "(1, 'I,2,1')" [label="9.997000899730082e-05"]
"(0, 'I,1,1')" -> "(1, 'M,2,2')" [label="0.9998000599820054"]
"(0, 'I,1,2')" -> "(1, 'I,2,2')" [label="1.0"]
"(0, 'M,1,1')" -> "(0, 'D,1,2')" [label="9.997000899730082e-05"]
"(0, 'M,1,1')" -> "(1, 'I,2,1')" [label="9.997000899730082e-05"]
"(0, 'M,1,1')" -> "(1, 'M,2,2')" [label="0.9998000599820054"]
"(0, 'M,1,2')" -> "(1, 'I,2,2')" [label="1.0"]
"(1, 'D,2,1')" -> "(1, 'D,2,2')" [label="1.0"]
"(1, 'D,2,2')" -> "(2, 'T,2,2')" [label="1.0"]
"(1, 'I,2,0')" -> "(1, 'D,2,1')" [label="1.0"]
"(1, 'I,2,1')" -> "(1, 'D,2,2')" [label="1.0"]
"(1, 'I,2,2')" -> "(2, 'T,2,2')" [label="1.0"]
"(1, 'M,2,1')" -> "(1, 'D,2,2')" [label="1.0"]
"(1, 'M,2,2')" -> "(2, 'T,2,2')" [label="1.0"]
"(2, 'T,2,2')" -> "(-1, 'VITERBI_SINK')" [label="1.0"]
}
```


The hidden path with the max product weight in this Viterbi graph is ...

```
hi
```

Most probable hidden path: [('S,0,0', 'M,1,1'), ('M,1,1', 'M,2,2'), ('M,2,2', 'T,2,2'), ('T,2,2', 'VITERBI_SINK')]

Most probable hidden path probability: 0.33326668666066844
</div>

`{bm-enable-all}`

