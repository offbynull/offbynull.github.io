<div style="border:1px solid black;">

`{bm-disable-all}`

Deriving HMM probabilities using the following settings...

```
transitions:
  SOURCE: [A, B, D]
  A: [B, E ,F]
  B: [C, D]
  C: [F]
  D: [A]
  E: [A]
  F: [E, B]
emissions:
  SOURCE: []
  A: [x, y, z]
  B: [x, y, z]
  C: []  # C is non-emitting
  D: [x, y, z]
  E: [x, y, z]
  F: [x, y, z]
source_state: SOURCE
sink_state: SINK  # Must not exist in HMM (used only for Viterbi graph)
emission_seq: [z, z, x, z, z, z, y, z, z, z, z, y, x]
cycles: 3
pseudocount: 0.0001

```

The following HMM was produced (no probabilities) ...

```{dot}
digraph G {
 graph[rankdir=LR]
 node[shape=egg, fontname="Courier-Bold", fontsize=10]
 edge[fontname="Courier-Bold", fontsize=10]
"STATE_A" [label="A"]
"STATE_B" [label="B"]
"STATE_C" [label="C"]
"STATE_D" [label="D"]
"STATE_E" [label="E"]
"STATE_F" [label="F"]
"STATE_SOURCE" [label="SOURCE"]
"STATE_A" -> "STATE_B" [label="nan"]
"STATE_A" -> "STATE_E" [label="nan"]
"STATE_A" -> "STATE_F" [label="nan"]
"STATE_B" -> "STATE_C" [label="nan"]
"STATE_B" -> "STATE_D" [label="nan"]
"STATE_C" -> "STATE_F" [label="nan"]
"STATE_D" -> "STATE_A" [label="nan"]
"STATE_E" -> "STATE_A" [label="nan"]
"STATE_F" -> "STATE_B" [label="nan"]
"STATE_F" -> "STATE_E" [label="nan"]
"STATE_SOURCE" -> "STATE_A" [label="nan"]
"STATE_SOURCE" -> "STATE_B" [label="nan"]
"STATE_SOURCE" -> "STATE_D" [label="nan"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="nan", style="dashed"]
"SYMBOL_x" [label="x", style="dashed"]
"STATE_A" -> "SYMBOL_x" [label="nan", style="dashed"]
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="nan", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="nan", style="dashed"]
"STATE_B" -> "SYMBOL_x" [label="nan", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="nan", style="dashed"]
"STATE_D" -> "SYMBOL_z" [label="nan", style="dashed"]
"STATE_D" -> "SYMBOL_x" [label="nan", style="dashed"]
"STATE_D" -> "SYMBOL_y" [label="nan", style="dashed"]
"STATE_E" -> "SYMBOL_z" [label="nan", style="dashed"]
"STATE_E" -> "SYMBOL_x" [label="nan", style="dashed"]
"STATE_E" -> "SYMBOL_y" [label="nan", style="dashed"]
"STATE_F" -> "SYMBOL_z" [label="nan", style="dashed"]
"STATE_F" -> "SYMBOL_x" [label="nan", style="dashed"]
"STATE_F" -> "SYMBOL_y" [label="nan", style="dashed"]
}
```

The following HMM was produced after applying randomized probabilities ...

```{dot}
digraph G {
 graph[rankdir=LR]
 node[shape=egg, fontname="Courier-Bold", fontsize=10]
 edge[fontname="Courier-Bold", fontsize=10]
"STATE_A" [label="A"]
"STATE_B" [label="B"]
"STATE_C" [label="C"]
"STATE_D" [label="D"]
"STATE_E" [label="E"]
"STATE_F" [label="F"]
"STATE_SOURCE" [label="SOURCE"]
"STATE_A" -> "STATE_B" [label="0.05365055020471289"]
"STATE_A" -> "STATE_E" [label="0.7695165892904383"]
"STATE_A" -> "STATE_F" [label="0.17683286050484884"]
"STATE_B" -> "STATE_C" [label="0.9456169158388782"]
"STATE_B" -> "STATE_D" [label="0.054383084161121836"]
"STATE_C" -> "STATE_F" [label="1.0"]
"STATE_D" -> "STATE_A" [label="1.0"]
"STATE_E" -> "STATE_A" [label="1.0"]
"STATE_F" -> "STATE_B" [label="0.7328093454120442"]
"STATE_F" -> "STATE_E" [label="0.26719065458795577"]
"STATE_SOURCE" -> "STATE_A" [label="0.5957683897192098"]
"STATE_SOURCE" -> "STATE_B" [label="0.03741560643170287"]
"STATE_SOURCE" -> "STATE_D" [label="0.36681600384908736"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="0.4342478206422663", style="dashed"]
"SYMBOL_x" [label="x", style="dashed"]
"STATE_A" -> "SYMBOL_x" [label="0.24502206919849306", style="dashed"]
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="0.32073011015924074", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="0.20569858193968676", style="dashed"]
"STATE_B" -> "SYMBOL_x" [label="0.3281663327264545", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="0.4661350853338587", style="dashed"]
"STATE_D" -> "SYMBOL_z" [label="0.49463092301137135", style="dashed"]
"STATE_D" -> "SYMBOL_x" [label="0.11094338502781709", style="dashed"]
"STATE_D" -> "SYMBOL_y" [label="0.3944256919608116", style="dashed"]
"STATE_E" -> "SYMBOL_z" [label="0.5674405458092364", style="dashed"]
"STATE_E" -> "SYMBOL_x" [label="0.3484198772501551", style="dashed"]
"STATE_E" -> "SYMBOL_y" [label="0.08413957694060858", style="dashed"]
"STATE_F" -> "SYMBOL_z" [label="0.4552355441676333", style="dashed"]
"STATE_F" -> "SYMBOL_x" [label="0.4656462506256307", style="dashed"]
"STATE_F" -> "SYMBOL_y" [label="0.07911820520673607", style="dashed"]
}
```

Applying Viterbi learning for 3 cycles ...

 1. Hidden path for emitted sequence: SOURCE→A, A→E, E→A, A→E, E→A, A→E, E→A, A→E, E→A, A→E, E→A, A→E, E→A

    New transition probabilities:
    * SOURCE→A = 0.9998000599820054
    * SOURCE→D = 9.997000899730082e-05
    * SOURCE→B = 9.997000899730082e-05
    * A→F = 9.997000899730082e-05
    * A→B = 9.997000899730082e-05
    * A→E = 0.9998000599820054
    * B→C = 0.5
    * B→D = 0.5
    * C→F = 1.0
    * D→A = 1.0
    * E→A = 1.0
    * F→B = 0.5
    * F→E = 0.5

    New emission probabilities:
    * (A, z) = 0.5713571642792876
    * (A, x) = 0.28572856714414246
    * (A, y) = 0.14291426857656986
    * (D, z) = 0.3333333333333333
    * (D, x) = 0.3333333333333333
    * (D, y) = 0.3333333333333333
    * (B, z) = 0.3333333333333333
    * (B, x) = 0.3333333333333333
    * (B, y) = 0.3333333333333333
    * (F, z) = 0.3333333333333333
    * (F, x) = 0.3333333333333333
    * (F, y) = 0.3333333333333333
    * (E, z) = 0.8331833783198375
    * (E, x) = 9.997000899730082e-05
    * (E, y) = 0.1667166516711653

 1. Hidden path for emitted sequence: SOURCE→A, A→E, E→A, A→E, E→A, A→E, E→A, A→E, E→A, A→E, E→A, A→E, E→A

    New transition probabilities:
    * SOURCE→A = 0.9998000599820054
    * SOURCE→D = 9.997000899730082e-05
    * SOURCE→B = 9.997000899730082e-05
    * A→F = 9.997000899730082e-05
    * A→B = 9.997000899730082e-05
    * A→E = 0.9998000599820054
    * B→C = 0.5
    * B→D = 0.5
    * C→F = 1.0
    * D→A = 1.0
    * E→A = 1.0
    * F→B = 0.5
    * F→E = 0.5

    New emission probabilities:
    * (A, z) = 0.5713571642792876
    * (A, x) = 0.28572856714414246
    * (A, y) = 0.14291426857656986
    * (D, z) = 0.3333333333333333
    * (D, x) = 0.3333333333333333
    * (D, y) = 0.3333333333333333
    * (B, z) = 0.3333333333333333
    * (B, x) = 0.3333333333333333
    * (B, y) = 0.3333333333333333
    * (F, z) = 0.3333333333333333
    * (F, x) = 0.3333333333333333
    * (F, y) = 0.3333333333333333
    * (E, z) = 0.8331833783198375
    * (E, x) = 9.997000899730082e-05
    * (E, y) = 0.1667166516711653

 1. Hidden path for emitted sequence: SOURCE→A, A→E, E→A, A→E, E→A, A→E, E→A, A→E, E→A, A→E, E→A, A→E, E→A

    New transition probabilities:
    * SOURCE→A = 0.9998000599820054
    * SOURCE→D = 9.997000899730082e-05
    * SOURCE→B = 9.997000899730082e-05
    * A→F = 9.997000899730082e-05
    * A→B = 9.997000899730082e-05
    * A→E = 0.9998000599820054
    * B→C = 0.5
    * B→D = 0.5
    * C→F = 1.0
    * D→A = 1.0
    * E→A = 1.0
    * F→B = 0.5
    * F→E = 0.5

    New emission probabilities:
    * (A, z) = 0.5713571642792876
    * (A, x) = 0.28572856714414246
    * (A, y) = 0.14291426857656986
    * (D, z) = 0.3333333333333333
    * (D, x) = 0.3333333333333333
    * (D, y) = 0.3333333333333333
    * (B, z) = 0.3333333333333333
    * (B, x) = 0.3333333333333333
    * (B, y) = 0.3333333333333333
    * (F, z) = 0.3333333333333333
    * (F, x) = 0.3333333333333333
    * (F, y) = 0.3333333333333333
    * (E, z) = 0.8331833783198375
    * (E, x) = 9.997000899730082e-05
    * (E, y) = 0.1667166516711653


The following HMM was produced after Viterbi learning was applied for 3 cycles ...

```{dot}
digraph G {
 graph[rankdir=LR]
 node[shape=egg, fontname="Courier-Bold", fontsize=10]
 edge[fontname="Courier-Bold", fontsize=10]
"STATE_A" [label="A"]
"STATE_B" [label="B"]
"STATE_C" [label="C"]
"STATE_D" [label="D"]
"STATE_E" [label="E"]
"STATE_F" [label="F"]
"STATE_SOURCE" [label="SOURCE"]
"STATE_A" -> "STATE_B" [label="9.997000899730082e-05"]
"STATE_A" -> "STATE_E" [label="0.9998000599820054"]
"STATE_A" -> "STATE_F" [label="9.997000899730082e-05"]
"STATE_B" -> "STATE_C" [label="0.5"]
"STATE_B" -> "STATE_D" [label="0.5"]
"STATE_C" -> "STATE_F" [label="1.0"]
"STATE_D" -> "STATE_A" [label="1.0"]
"STATE_E" -> "STATE_A" [label="1.0"]
"STATE_F" -> "STATE_B" [label="0.5"]
"STATE_F" -> "STATE_E" [label="0.5"]
"STATE_SOURCE" -> "STATE_A" [label="0.9998000599820054"]
"STATE_SOURCE" -> "STATE_B" [label="9.997000899730082e-05"]
"STATE_SOURCE" -> "STATE_D" [label="9.997000899730082e-05"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="0.5713571642792876", style="dashed"]
"SYMBOL_x" [label="x", style="dashed"]
"STATE_A" -> "SYMBOL_x" [label="0.28572856714414246", style="dashed"]
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="0.14291426857656986", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="0.3333333333333333", style="dashed"]
"STATE_B" -> "SYMBOL_x" [label="0.3333333333333333", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="0.3333333333333333", style="dashed"]
"STATE_D" -> "SYMBOL_z" [label="0.3333333333333333", style="dashed"]
"STATE_D" -> "SYMBOL_x" [label="0.3333333333333333", style="dashed"]
"STATE_D" -> "SYMBOL_y" [label="0.3333333333333333", style="dashed"]
"STATE_E" -> "SYMBOL_z" [label="0.8331833783198375", style="dashed"]
"STATE_E" -> "SYMBOL_x" [label="9.997000899730082e-05", style="dashed"]
"STATE_E" -> "SYMBOL_y" [label="0.1667166516711653", style="dashed"]
"STATE_F" -> "SYMBOL_z" [label="0.3333333333333333", style="dashed"]
"STATE_F" -> "SYMBOL_x" [label="0.3333333333333333", style="dashed"]
"STATE_F" -> "SYMBOL_y" [label="0.3333333333333333", style="dashed"]
}
```

</div>

`{bm-enable-all}`

