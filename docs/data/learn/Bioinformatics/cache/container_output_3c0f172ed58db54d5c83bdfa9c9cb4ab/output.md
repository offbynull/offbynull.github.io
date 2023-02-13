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
"SYMBOL_x" [label="x", style="dashed"]
"STATE_A" -> "SYMBOL_x" [label="nan", style="dashed"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="nan", style="dashed"]
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="nan", style="dashed"]
"STATE_B" -> "SYMBOL_x" [label="nan", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="nan", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="nan", style="dashed"]
"STATE_D" -> "SYMBOL_x" [label="nan", style="dashed"]
"STATE_D" -> "SYMBOL_z" [label="nan", style="dashed"]
"STATE_D" -> "SYMBOL_y" [label="nan", style="dashed"]
"STATE_E" -> "SYMBOL_x" [label="nan", style="dashed"]
"STATE_E" -> "SYMBOL_z" [label="nan", style="dashed"]
"STATE_E" -> "SYMBOL_y" [label="nan", style="dashed"]
"STATE_F" -> "SYMBOL_x" [label="nan", style="dashed"]
"STATE_F" -> "SYMBOL_z" [label="nan", style="dashed"]
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
"STATE_A" -> "STATE_B" [label="0.2377744624150729"]
"STATE_A" -> "STATE_E" [label="0.3631885876642511"]
"STATE_A" -> "STATE_F" [label="0.39903694992067607"]
"STATE_B" -> "STATE_C" [label="0.10230470877055443"]
"STATE_B" -> "STATE_D" [label="0.8976952912294456"]
"STATE_C" -> "STATE_F" [label="1.0"]
"STATE_D" -> "STATE_A" [label="1.0"]
"STATE_E" -> "STATE_A" [label="1.0"]
"STATE_F" -> "STATE_B" [label="0.4812058244723345"]
"STATE_F" -> "STATE_E" [label="0.5187941755276655"]
"STATE_SOURCE" -> "STATE_A" [label="0.38101818420528394"]
"STATE_SOURCE" -> "STATE_B" [label="0.15343296462879435"]
"STATE_SOURCE" -> "STATE_D" [label="0.4655488511659217"]
"SYMBOL_x" [label="x", style="dashed"]
"STATE_A" -> "SYMBOL_x" [label="0.31476649122275685", style="dashed"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="0.39300595372807495", style="dashed"]
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="0.29222755504916825", style="dashed"]
"STATE_B" -> "SYMBOL_x" [label="0.5060875535752375", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="0.15523671118842658", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="0.3386757352363359", style="dashed"]
"STATE_D" -> "SYMBOL_x" [label="0.4340877934597644", style="dashed"]
"STATE_D" -> "SYMBOL_z" [label="0.026791232362406832", style="dashed"]
"STATE_D" -> "SYMBOL_y" [label="0.5391209741778288", style="dashed"]
"STATE_E" -> "SYMBOL_x" [label="0.19900529757613783", style="dashed"]
"STATE_E" -> "SYMBOL_z" [label="0.6228284341131863", style="dashed"]
"STATE_E" -> "SYMBOL_y" [label="0.17816626831067595", style="dashed"]
"STATE_F" -> "SYMBOL_x" [label="0.3902263473403556", style="dashed"]
"STATE_F" -> "SYMBOL_z" [label="0.389623854579958", style="dashed"]
"STATE_F" -> "SYMBOL_y" [label="0.22014979807968627", style="dashed"]
}
```

Applying Viterbi learning for 3 cycles ...

 1. Hidden path for emitted sequence: SOURCE→A, A→E, E→A, A→E, E→A, A→E, E→A, A→E, E→A, A→E, E→A, A→B, B→D

    New transition probabilities:
    * SOURCE→B = 9.997000899730082e-05
    * SOURCE→D = 9.997000899730082e-05
    * SOURCE→A = 0.9998000599820054
    * A→B = 0.1667166516711653
    * A→F = 9.997000899730082e-05
    * A→E = 0.8331833783198375
    * B→D = 0.9999000199960009
    * B→C = 9.998000399920017e-05
    * C→F = 1.0
    * D→A = 1.0
    * E→A = 1.0
    * F→B = 0.5
    * F→E = 0.5

    New emission probabilities:
    * (B, x) = 9.997000899730082e-05
    * (B, z) = 9.997000899730082e-05
    * (B, y) = 0.9998000599820054
    * (D, x) = 0.9998000599820054
    * (D, z) = 9.997000899730082e-05
    * (D, y) = 9.997000899730082e-05
    * (A, x) = 0.1667166516711653
    * (A, z) = 0.6665666966576693
    * (A, y) = 0.1667166516711653
    * (F, x) = 0.3333333333333333
    * (F, z) = 0.3333333333333333
    * (F, y) = 0.3333333333333333
    * (E, x) = 9.997000899730082e-05
    * (E, z) = 0.9998000599820054
    * (E, y) = 9.997000899730082e-05

 1. Hidden path for emitted sequence: SOURCE→A, A→E, E→A, A→E, E→A, A→E, E→A, A→E, E→A, A→E, E→A, A→B, B→D

    New transition probabilities:
    * SOURCE→B = 9.997000899730082e-05
    * SOURCE→D = 9.997000899730082e-05
    * SOURCE→A = 0.9998000599820054
    * A→B = 0.1667166516711653
    * A→F = 9.997000899730082e-05
    * A→E = 0.8331833783198375
    * B→D = 0.9999000199960009
    * B→C = 9.998000399920017e-05
    * C→F = 1.0
    * D→A = 1.0
    * E→A = 1.0
    * F→B = 0.5
    * F→E = 0.5

    New emission probabilities:
    * (B, x) = 9.997000899730082e-05
    * (B, z) = 9.997000899730082e-05
    * (B, y) = 0.9998000599820054
    * (D, x) = 0.9998000599820054
    * (D, z) = 9.997000899730082e-05
    * (D, y) = 9.997000899730082e-05
    * (A, x) = 0.1667166516711653
    * (A, z) = 0.6665666966576693
    * (A, y) = 0.1667166516711653
    * (F, x) = 0.3333333333333333
    * (F, z) = 0.3333333333333333
    * (F, y) = 0.3333333333333333
    * (E, x) = 9.997000899730082e-05
    * (E, z) = 0.9998000599820054
    * (E, y) = 9.997000899730082e-05

 1. Hidden path for emitted sequence: SOURCE→A, A→E, E→A, A→E, E→A, A→E, E→A, A→E, E→A, A→E, E→A, A→B, B→D

    New transition probabilities:
    * SOURCE→B = 9.997000899730082e-05
    * SOURCE→D = 9.997000899730082e-05
    * SOURCE→A = 0.9998000599820054
    * A→B = 0.1667166516711653
    * A→F = 9.997000899730082e-05
    * A→E = 0.8331833783198375
    * B→D = 0.9999000199960009
    * B→C = 9.998000399920017e-05
    * C→F = 1.0
    * D→A = 1.0
    * E→A = 1.0
    * F→B = 0.5
    * F→E = 0.5

    New emission probabilities:
    * (B, x) = 9.997000899730082e-05
    * (B, z) = 9.997000899730082e-05
    * (B, y) = 0.9998000599820054
    * (D, x) = 0.9998000599820054
    * (D, z) = 9.997000899730082e-05
    * (D, y) = 9.997000899730082e-05
    * (A, x) = 0.1667166516711653
    * (A, z) = 0.6665666966576693
    * (A, y) = 0.1667166516711653
    * (F, x) = 0.3333333333333333
    * (F, z) = 0.3333333333333333
    * (F, y) = 0.3333333333333333
    * (E, x) = 9.997000899730082e-05
    * (E, z) = 0.9998000599820054
    * (E, y) = 9.997000899730082e-05


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
"STATE_A" -> "STATE_B" [label="0.1667166516711653"]
"STATE_A" -> "STATE_E" [label="0.8331833783198375"]
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
"SYMBOL_x" [label="x", style="dashed"]
"STATE_A" -> "SYMBOL_x" [label="0.1667166516711653", style="dashed"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="0.6665666966576693", style="dashed"]
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="0.1667166516711653", style="dashed"]
"STATE_B" -> "SYMBOL_x" [label="9.997000899730082e-05", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="9.997000899730082e-05", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="0.9998000599820054", style="dashed"]
"STATE_D" -> "SYMBOL_x" [label="0.9998000599820054", style="dashed"]
"STATE_D" -> "SYMBOL_z" [label="9.997000899730082e-05", style="dashed"]
"STATE_D" -> "SYMBOL_y" [label="9.997000899730082e-05", style="dashed"]
"STATE_E" -> "SYMBOL_x" [label="9.997000899730082e-05", style="dashed"]
"STATE_E" -> "SYMBOL_z" [label="0.9998000599820054", style="dashed"]
"STATE_E" -> "SYMBOL_y" [label="9.997000899730082e-05", style="dashed"]
"STATE_F" -> "SYMBOL_x" [label="0.3333333333333333", style="dashed"]
"STATE_F" -> "SYMBOL_z" [label="0.3333333333333333", style="dashed"]
"STATE_F" -> "SYMBOL_y" [label="0.3333333333333333", style="dashed"]
}
```

</div>

`{bm-enable-all}`

