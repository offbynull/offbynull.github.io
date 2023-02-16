<div style="border:1px solid black;">

`{bm-disable-all}`

Building profile HMM and testing against sequence using the following settings...

```
sequence: [G, A]
alignment:
  - [G, -, T, -, C]
  - [-, C, T, A, -]
  - [-, T, T, A, -]
  - [-, -, T, -, C]
  - [G, -, -, -, -]
column_removal_threshold: 0.59
pseudocount: 0.0001
symbols: [A, C, T, G]

```

The following HMM was produced AFTER applying pseudocounts ...

```{dot}
digraph G {
 graph[rankdir=LR]
 node[shape=egg, fontname="Courier-Bold", fontsize=10]
 edge[fontname="Courier-Bold", fontsize=10]
"STATE_D,0,1" [label="D,0,1"]
"STATE_D,1,1" [label="D,1,1"]
"STATE_D,2,1" [label="D,2,1"]
"STATE_I,1,0" [label="I,1,0"]
"STATE_I,1,1" [label="I,1,1"]
"STATE_I,2,0" [label="I,2,0"]
"STATE_I,2,1" [label="I,2,1"]
"STATE_M,1,1" [label="M,1,1"]
"STATE_M,2,1" [label="M,2,1"]
"STATE_S,0,0" [label="S,0,0"]
"STATE_T,2,1" [label="T,2,1"]
"STATE_D,0,1" -> "STATE_I,1,1" [label="1.0"]
"STATE_D,1,1" -> "STATE_I,2,1" [label="1.0"]
"STATE_D,2,1" -> "STATE_T,2,1" [label="1.0"]
"STATE_I,1,0" -> "STATE_D,1,1" [label="0.11117775778377598"]
"STATE_I,1,0" -> "STATE_I,2,0" [label="0.444411121108112"]
"STATE_I,1,0" -> "STATE_M,2,1" [label="0.444411121108112"]
"STATE_I,1,1" -> "STATE_I,2,1" [label="1.0"]
"STATE_I,2,0" -> "STATE_D,2,1" [label="1.0"]
"STATE_I,2,1" -> "STATE_T,2,1" [label="1.0"]
"STATE_M,1,1" -> "STATE_I,2,1" [label="1.0"]
"STATE_M,2,1" -> "STATE_T,2,1" [label="1.0"]
"STATE_S,0,0" -> "STATE_D,0,1" [label="0.11117775778377598"]
"STATE_S,0,0" -> "STATE_I,1,0" [label="0.444411121108112"]
"STATE_S,0,0" -> "STATE_M,1,1" [label="0.444411121108112"]
"SYMBOL_C" [label="C", style="dashed"]
"STATE_I,1,0" -> "SYMBOL_C" [label="0.24997501249375312", style="dashed"]
"SYMBOL_G" [label="G", style="dashed"]
"STATE_I,1,0" -> "SYMBOL_G" [label="0.49985007496251876", style="dashed"]
"SYMBOL_?" [label="?", style="dashed"]
"STATE_I,1,0" -> "SYMBOL_?" [label="9.995002498750626e-05", style="dashed"]
"SYMBOL_A" [label="A", style="dashed"]
"STATE_I,1,0" -> "SYMBOL_A" [label="9.995002498750626e-05", style="dashed"]
"SYMBOL_T" [label="T", style="dashed"]
"STATE_I,1,0" -> "SYMBOL_T" [label="0.24997501249375312", style="dashed"]
"STATE_I,1,1" -> "SYMBOL_C" [label="0.49985007496251876", style="dashed"]
"STATE_I,1,1" -> "SYMBOL_G" [label="9.995002498750626e-05", style="dashed"]
"STATE_I,1,1" -> "SYMBOL_?" [label="9.995002498750626e-05", style="dashed"]
"STATE_I,1,1" -> "SYMBOL_A" [label="0.49985007496251876", style="dashed"]
"STATE_I,1,1" -> "SYMBOL_T" [label="9.995002498750626e-05", style="dashed"]
"STATE_I,2,0" -> "SYMBOL_C" [label="0.24997501249375312", style="dashed"]
"STATE_I,2,0" -> "SYMBOL_G" [label="0.49985007496251876", style="dashed"]
"STATE_I,2,0" -> "SYMBOL_?" [label="9.995002498750626e-05", style="dashed"]
"STATE_I,2,0" -> "SYMBOL_A" [label="9.995002498750626e-05", style="dashed"]
"STATE_I,2,0" -> "SYMBOL_T" [label="0.24997501249375312", style="dashed"]
"STATE_I,2,1" -> "SYMBOL_C" [label="0.49985007496251876", style="dashed"]
"STATE_I,2,1" -> "SYMBOL_G" [label="9.995002498750626e-05", style="dashed"]
"STATE_I,2,1" -> "SYMBOL_?" [label="9.995002498750626e-05", style="dashed"]
"STATE_I,2,1" -> "SYMBOL_A" [label="0.49985007496251876", style="dashed"]
"STATE_I,2,1" -> "SYMBOL_T" [label="9.995002498750626e-05", style="dashed"]
"STATE_M,1,1" -> "SYMBOL_C" [label="9.995002498750626e-05", style="dashed"]
"STATE_M,1,1" -> "SYMBOL_G" [label="9.995002498750626e-05", style="dashed"]
"STATE_M,1,1" -> "SYMBOL_?" [label="9.995002498750626e-05", style="dashed"]
"STATE_M,1,1" -> "SYMBOL_A" [label="9.995002498750626e-05", style="dashed"]
"STATE_M,1,1" -> "SYMBOL_T" [label="0.99960019990005", style="dashed"]
"STATE_M,2,1" -> "SYMBOL_C" [label="9.995002498750626e-05", style="dashed"]
"STATE_M,2,1" -> "SYMBOL_G" [label="9.995002498750626e-05", style="dashed"]
"STATE_M,2,1" -> "SYMBOL_?" [label="9.995002498750626e-05", style="dashed"]
"STATE_M,2,1" -> "SYMBOL_A" [label="9.995002498750626e-05", style="dashed"]
"STATE_M,2,1" -> "SYMBOL_T" [label="0.99960019990005", style="dashed"]
"STATE_T,2,1" -> "SYMBOL_?" [label="1.0", style="dashed"]
}
```

The following Viterbi graph was produced for the HMM and the emitted sequence ['G', 'A'] ...

```{dot}
digraph G {
 graph[rankdir=LR]
 node[shape=egg, fontname="Courier-Bold", fontsize=10]
 edge[fontname="Courier-Bold", fontsize=10]
"(-1, 'D,0,1')" [label="(-1, 'D,0,1')"]
"(-1, 'S,0,0')" [label="(-1, 'S,0,0')"]
"(-1, 'VITERBI_SINK')" [label="(-1, 'VITERBI_SINK')"]
"(0, 'D,1,1')" [label="(0, 'D,1,1')"]
"(0, 'I,1,0')" [label="(0, 'I,1,0')"]
"(0, 'I,1,1')" [label="(0, 'I,1,1')"]
"(0, 'M,1,1')" [label="(0, 'M,1,1')"]
"(1, 'D,2,1')" [label="(1, 'D,2,1')"]
"(1, 'I,2,0')" [label="(1, 'I,2,0')"]
"(1, 'I,2,1')" [label="(1, 'I,2,1')"]
"(1, 'M,2,1')" [label="(1, 'M,2,1')"]
"(2, 'T,2,1')" [label="(2, 'T,2,1')"]
"(-1, 'D,0,1')" -> "(0, 'I,1,1')" [label="9.995002498750626e-05"]
"(-1, 'S,0,0')" -> "(-1, 'D,0,1')" [label="0.11117775778377598"]
"(-1, 'S,0,0')" -> "(0, 'I,1,0')" [label="0.22213893220006678"]
"(-1, 'S,0,0')" -> "(0, 'M,1,1')" [label="4.441890265948146e-05"]
"(0, 'D,1,1')" -> "(1, 'I,2,1')" [label="0.49985007496251876"]
"(0, 'I,1,0')" -> "(0, 'D,1,1')" [label="0.11117775778377598"]
"(0, 'I,1,0')" -> "(1, 'I,2,0')" [label="4.441890265948146e-05"]
"(0, 'I,1,0')" -> "(1, 'M,2,1')" [label="4.441890265948146e-05"]
"(0, 'I,1,1')" -> "(1, 'I,2,1')" [label="0.49985007496251876"]
"(0, 'M,1,1')" -> "(1, 'I,2,1')" [label="0.49985007496251876"]
"(1, 'D,2,1')" -> "(2, 'T,2,1')" [label="1.0"]
"(1, 'I,2,0')" -> "(1, 'D,2,1')" [label="1.0"]
"(1, 'I,2,1')" -> "(2, 'T,2,1')" [label="1.0"]
"(1, 'M,2,1')" -> "(2, 'T,2,1')" [label="1.0"]
"(2, 'T,2,1')" -> "(-1, 'VITERBI_SINK')" [label="1.0"]
}
```


The hidden path with the max product weight in this Viterbi graph is ...

```
G-A
```

Most probable hidden path: [('S,0,0', 'I,1,0'), ('I,1,0', 'D,1,1'), ('D,1,1', 'I,2,1'), ('I,2,1', 'T,2,1'), ('T,2,1', 'VITERBI_SINK')]

Most probable hidden path probability: 0.012344751514325515
</div>

`{bm-enable-all}`

