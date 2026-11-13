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
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="nan", style="dashed"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="nan", style="dashed"]
"SYMBOL_x" [label="x", style="dashed"]
"STATE_A" -> "SYMBOL_x" [label="nan", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="nan", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="nan", style="dashed"]
"STATE_B" -> "SYMBOL_x" [label="nan", style="dashed"]
"STATE_D" -> "SYMBOL_y" [label="nan", style="dashed"]
"STATE_D" -> "SYMBOL_z" [label="nan", style="dashed"]
"STATE_D" -> "SYMBOL_x" [label="nan", style="dashed"]
"STATE_E" -> "SYMBOL_y" [label="nan", style="dashed"]
"STATE_E" -> "SYMBOL_z" [label="nan", style="dashed"]
"STATE_E" -> "SYMBOL_x" [label="nan", style="dashed"]
"STATE_F" -> "SYMBOL_y" [label="nan", style="dashed"]
"STATE_F" -> "SYMBOL_z" [label="nan", style="dashed"]
"STATE_F" -> "SYMBOL_x" [label="nan", style="dashed"]
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
"STATE_A" -> "STATE_B" [label="0.3863681042872421"]
"STATE_A" -> "STATE_E" [label="0.2535630654278777"]
"STATE_A" -> "STATE_F" [label="0.3600688302848803"]
"STATE_B" -> "STATE_C" [label="0.35934448186125634"]
"STATE_B" -> "STATE_D" [label="0.6406555181387437"]
"STATE_C" -> "STATE_F" [label="1.0"]
"STATE_D" -> "STATE_A" [label="1.0"]
"STATE_E" -> "STATE_A" [label="1.0"]
"STATE_F" -> "STATE_B" [label="0.014454667508826066"]
"STATE_F" -> "STATE_E" [label="0.9855453324911739"]
"STATE_SOURCE" -> "STATE_A" [label="0.602652919459112"]
"STATE_SOURCE" -> "STATE_B" [label="0.3264811804181394"]
"STATE_SOURCE" -> "STATE_D" [label="0.07086590012274863"]
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="0.1688012866443133", style="dashed"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="0.4666797731288763", style="dashed"]
"SYMBOL_x" [label="x", style="dashed"]
"STATE_A" -> "SYMBOL_x" [label="0.3645189402268104", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="0.19220690830050635", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="0.5645564802024741", style="dashed"]
"STATE_B" -> "SYMBOL_x" [label="0.24323661149701953", style="dashed"]
"STATE_D" -> "SYMBOL_y" [label="0.44549481572902805", style="dashed"]
"STATE_D" -> "SYMBOL_z" [label="0.22718435208222068", style="dashed"]
"STATE_D" -> "SYMBOL_x" [label="0.32732083218875124", style="dashed"]
"STATE_E" -> "SYMBOL_y" [label="0.3447213253013478", style="dashed"]
"STATE_E" -> "SYMBOL_z" [label="0.6455747836890986", style="dashed"]
"STATE_E" -> "SYMBOL_x" [label="0.009703891009553524", style="dashed"]
"STATE_F" -> "SYMBOL_y" [label="0.0913836426551549", style="dashed"]
"STATE_F" -> "SYMBOL_z" [label="0.07374311402323235", style="dashed"]
"STATE_F" -> "SYMBOL_x" [label="0.8348732433216127", style="dashed"]
}
```

Applying Viterbi learning for 3 cycles ...

 1. Hidden path for emitted sequence: SOURCE→A, A→B, B→C, C→F, F→E, E→A, A→B, B→D, D→A, A→E, E→A, A→B, B→D, D→A

    New transition probabilities:
    * SOURCE→A = 0.9998000599820054
    * SOURCE→D = 9.997000899730082e-05
    * SOURCE→B = 9.997000899730082e-05
    * A→E = 0.2500249925022493
    * A→F = 9.997000899730082e-05
    * A→B = 0.7498750374887534
    * B→D = 0.6666333399986669
    * B→C = 0.333366660001333
    * C→F = 1.0
    * D→A = 1.0
    * E→A = 1.0
    * F→E = 0.9999000199960009
    * F→B = 9.998000399920017e-05

    New emission probabilities:
    * (A, y) = 9.997000899730082e-05
    * (A, z) = 0.9998000599820054
    * (A, x) = 9.997000899730082e-05
    * (D, y) = 9.997000899730082e-05
    * (D, z) = 0.49995001499550135
    * (D, x) = 0.49995001499550135
    * (B, y) = 0.6665666966576693
    * (B, z) = 0.3333333333333333
    * (B, x) = 9.997000899730082e-05
    * (E, y) = 9.997000899730082e-05
    * (E, z) = 0.9998000599820054
    * (E, x) = 9.997000899730082e-05
    * (F, y) = 9.997000899730082e-05
    * (F, z) = 0.9998000599820054
    * (F, x) = 9.997000899730082e-05

 1. Hidden path for emitted sequence: SOURCE→A, A→B, B→D, D→A, A→E, E→A, A→B, B→D, D→A, A→E, E→A, A→B, B→D

    New transition probabilities:
    * SOURCE→A = 0.9998000599820054
    * SOURCE→D = 9.997000899730082e-05
    * SOURCE→B = 9.997000899730082e-05
    * A→E = 0.39998000599820055
    * A→F = 9.997000899730082e-05
    * A→B = 0.5999200239928022
    * B→D = 0.9999000199960009
    * B→C = 9.998000399920017e-05
    * C→F = 1.0
    * D→A = 1.0
    * E→A = 1.0
    * F→E = 0.5
    * F→B = 0.5

    New emission probabilities:
    * (A, y) = 9.997000899730082e-05
    * (A, z) = 0.9998000599820054
    * (A, x) = 9.997000899730082e-05
    * (D, y) = 9.997000899730082e-05
    * (D, z) = 0.3333333333333333
    * (D, x) = 0.6665666966576693
    * (B, y) = 0.6665666966576693
    * (B, z) = 0.3333333333333333
    * (B, x) = 9.997000899730082e-05
    * (E, y) = 9.997000899730082e-05
    * (E, z) = 0.9998000599820054
    * (E, x) = 9.997000899730082e-05
    * (F, y) = 0.3333333333333333
    * (F, z) = 0.3333333333333333
    * (F, x) = 0.3333333333333333

 1. Hidden path for emitted sequence: SOURCE→A, A→B, B→D, D→A, A→E, E→A, A→B, B→D, D→A, A→E, E→A, A→B, B→D

    New transition probabilities:
    * SOURCE→A = 0.9998000599820054
    * SOURCE→D = 9.997000899730082e-05
    * SOURCE→B = 9.997000899730082e-05
    * A→E = 0.39998000599820055
    * A→F = 9.997000899730082e-05
    * A→B = 0.5999200239928022
    * B→D = 0.9999000199960009
    * B→C = 9.998000399920017e-05
    * C→F = 1.0
    * D→A = 1.0
    * E→A = 1.0
    * F→E = 0.5
    * F→B = 0.5

    New emission probabilities:
    * (A, y) = 9.997000899730082e-05
    * (A, z) = 0.9998000599820054
    * (A, x) = 9.997000899730082e-05
    * (D, y) = 9.997000899730082e-05
    * (D, z) = 0.3333333333333333
    * (D, x) = 0.6665666966576693
    * (B, y) = 0.6665666966576693
    * (B, z) = 0.3333333333333333
    * (B, x) = 9.997000899730082e-05
    * (E, y) = 9.997000899730082e-05
    * (E, z) = 0.9998000599820054
    * (E, x) = 9.997000899730082e-05
    * (F, y) = 0.3333333333333333
    * (F, z) = 0.3333333333333333
    * (F, x) = 0.3333333333333333


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
"STATE_A" -> "STATE_B" [label="0.5999200239928022"]
"STATE_A" -> "STATE_E" [label="0.39998000599820055"]
"STATE_A" -> "STATE_F" [label="9.997000899730082e-05"]
"STATE_B" -> "STATE_C" [label="9.998000399920017e-05"]
"STATE_B" -> "STATE_D" [label="0.9999000199960009"]
"STATE_C" -> "STATE_F" [label="1.0"]
"STATE_D" -> "STATE_A" [label="1.0"]
"STATE_E" -> "STATE_A" [label="1.0"]
"STATE_F" -> "STATE_B" [label="0.5"]
"STATE_F" -> "STATE_E" [label="0.5"]
"STATE_SOURCE" -> "STATE_A" [label="0.9998000599820054"]
"STATE_SOURCE" -> "STATE_B" [label="9.997000899730082e-05"]
"STATE_SOURCE" -> "STATE_D" [label="9.997000899730082e-05"]
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="9.997000899730082e-05", style="dashed"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="0.9998000599820054", style="dashed"]
"SYMBOL_x" [label="x", style="dashed"]
"STATE_A" -> "SYMBOL_x" [label="9.997000899730082e-05", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="0.6665666966576693", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="0.3333333333333333", style="dashed"]
"STATE_B" -> "SYMBOL_x" [label="9.997000899730082e-05", style="dashed"]
"STATE_D" -> "SYMBOL_y" [label="9.997000899730082e-05", style="dashed"]
"STATE_D" -> "SYMBOL_z" [label="0.3333333333333333", style="dashed"]
"STATE_D" -> "SYMBOL_x" [label="0.6665666966576693", style="dashed"]
"STATE_E" -> "SYMBOL_y" [label="9.997000899730082e-05", style="dashed"]
"STATE_E" -> "SYMBOL_z" [label="0.9998000599820054", style="dashed"]
"STATE_E" -> "SYMBOL_x" [label="9.997000899730082e-05", style="dashed"]
"STATE_F" -> "SYMBOL_y" [label="0.3333333333333333", style="dashed"]
"STATE_F" -> "SYMBOL_z" [label="0.3333333333333333", style="dashed"]
"STATE_F" -> "SYMBOL_x" [label="0.3333333333333333", style="dashed"]
}
```

</div>

`{bm-enable-all}`

