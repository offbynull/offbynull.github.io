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
"STATE_A" -> "STATE_B" [label="0.05343970934524711"]
"STATE_A" -> "STATE_E" [label="0.9328178419744396"]
"STATE_A" -> "STATE_F" [label="0.013742448680313301"]
"STATE_B" -> "STATE_C" [label="0.5718583749182152"]
"STATE_B" -> "STATE_D" [label="0.42814162508178477"]
"STATE_C" -> "STATE_F" [label="1.0"]
"STATE_D" -> "STATE_A" [label="1.0"]
"STATE_E" -> "STATE_A" [label="1.0"]
"STATE_F" -> "STATE_B" [label="0.7001858034669421"]
"STATE_F" -> "STATE_E" [label="0.29981419653305785"]
"STATE_SOURCE" -> "STATE_A" [label="0.11271205133746391"]
"STATE_SOURCE" -> "STATE_B" [label="0.4007165969798245"]
"STATE_SOURCE" -> "STATE_D" [label="0.4865713516827116"]
"SYMBOL_x" [label="x", style="dashed"]
"STATE_A" -> "SYMBOL_x" [label="0.3023481226276986", style="dashed"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="0.38801087829550657", style="dashed"]
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="0.30964099907679477", style="dashed"]
"STATE_B" -> "SYMBOL_x" [label="0.36465012661063506", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="0.12077752974290627", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="0.5145723436464587", style="dashed"]
"STATE_D" -> "SYMBOL_x" [label="0.2370828701550448", style="dashed"]
"STATE_D" -> "SYMBOL_z" [label="0.342117402453705", style="dashed"]
"STATE_D" -> "SYMBOL_y" [label="0.4207997273912502", style="dashed"]
"STATE_E" -> "SYMBOL_x" [label="0.15760907138715222", style="dashed"]
"STATE_E" -> "SYMBOL_z" [label="0.7122473266289889", style="dashed"]
"STATE_E" -> "SYMBOL_y" [label="0.1301436019838589", style="dashed"]
"STATE_F" -> "SYMBOL_x" [label="0.1854344444836496", style="dashed"]
"STATE_F" -> "SYMBOL_z" [label="0.5005105530301552", style="dashed"]
"STATE_F" -> "SYMBOL_y" [label="0.3140550024861953", style="dashed"]
}
```

Applying Viterbi learning for 3 cycles ...

 1. Hidden path for emitted sequence: SOURCE→A, A→E, E→A, A→E, E→A, A→E, E→A, A→E, E→A, A→E, E→A, A→E, E→A

    New transition probabilities:
    * SOURCE→B = 9.997000899730082e-05
    * SOURCE→D = 9.997000899730082e-05
    * SOURCE→A = 0.9998000599820054
    * A→B = 9.997000899730082e-05
    * A→E = 0.9998000599820054
    * A→F = 9.997000899730082e-05
    * B→D = 0.5
    * B→C = 0.5
    * C→F = 1.0
    * D→A = 1.0
    * E→A = 1.0
    * F→B = 0.5
    * F→E = 0.5

    New emission probabilities:
    * (B, x) = 0.3333333333333333
    * (B, z) = 0.3333333333333333
    * (B, y) = 0.3333333333333333
    * (D, x) = 0.3333333333333333
    * (D, z) = 0.3333333333333333
    * (D, y) = 0.3333333333333333
    * (A, x) = 0.28572856714414246
    * (A, z) = 0.5713571642792876
    * (A, y) = 0.14291426857656986
    * (E, x) = 9.997000899730082e-05
    * (E, z) = 0.8331833783198375
    * (E, y) = 0.1667166516711653
    * (F, x) = 0.3333333333333333
    * (F, z) = 0.3333333333333333
    * (F, y) = 0.3333333333333333

 1. Hidden path for emitted sequence: SOURCE→A, A→E, E→A, A→E, E→A, A→E, E→A, A→E, E→A, A→E, E→A, A→E, E→A

    New transition probabilities:
    * SOURCE→B = 9.997000899730082e-05
    * SOURCE→D = 9.997000899730082e-05
    * SOURCE→A = 0.9998000599820054
    * A→B = 9.997000899730082e-05
    * A→E = 0.9998000599820054
    * A→F = 9.997000899730082e-05
    * B→D = 0.5
    * B→C = 0.5
    * C→F = 1.0
    * D→A = 1.0
    * E→A = 1.0
    * F→B = 0.5
    * F→E = 0.5

    New emission probabilities:
    * (B, x) = 0.3333333333333333
    * (B, z) = 0.3333333333333333
    * (B, y) = 0.3333333333333333
    * (D, x) = 0.3333333333333333
    * (D, z) = 0.3333333333333333
    * (D, y) = 0.3333333333333333
    * (A, x) = 0.28572856714414246
    * (A, z) = 0.5713571642792876
    * (A, y) = 0.14291426857656986
    * (E, x) = 9.997000899730082e-05
    * (E, z) = 0.8331833783198375
    * (E, y) = 0.1667166516711653
    * (F, x) = 0.3333333333333333
    * (F, z) = 0.3333333333333333
    * (F, y) = 0.3333333333333333

 1. Hidden path for emitted sequence: SOURCE→A, A→E, E→A, A→E, E→A, A→E, E→A, A→E, E→A, A→E, E→A, A→E, E→A

    New transition probabilities:
    * SOURCE→B = 9.997000899730082e-05
    * SOURCE→D = 9.997000899730082e-05
    * SOURCE→A = 0.9998000599820054
    * A→B = 9.997000899730082e-05
    * A→E = 0.9998000599820054
    * A→F = 9.997000899730082e-05
    * B→D = 0.5
    * B→C = 0.5
    * C→F = 1.0
    * D→A = 1.0
    * E→A = 1.0
    * F→B = 0.5
    * F→E = 0.5

    New emission probabilities:
    * (B, x) = 0.3333333333333333
    * (B, z) = 0.3333333333333333
    * (B, y) = 0.3333333333333333
    * (D, x) = 0.3333333333333333
    * (D, z) = 0.3333333333333333
    * (D, y) = 0.3333333333333333
    * (A, x) = 0.28572856714414246
    * (A, z) = 0.5713571642792876
    * (A, y) = 0.14291426857656986
    * (E, x) = 9.997000899730082e-05
    * (E, z) = 0.8331833783198375
    * (E, y) = 0.1667166516711653
    * (F, x) = 0.3333333333333333
    * (F, z) = 0.3333333333333333
    * (F, y) = 0.3333333333333333


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
"SYMBOL_x" [label="x", style="dashed"]
"STATE_A" -> "SYMBOL_x" [label="0.28572856714414246", style="dashed"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="0.5713571642792876", style="dashed"]
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="0.14291426857656986", style="dashed"]
"STATE_B" -> "SYMBOL_x" [label="0.3333333333333333", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="0.3333333333333333", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="0.3333333333333333", style="dashed"]
"STATE_D" -> "SYMBOL_x" [label="0.3333333333333333", style="dashed"]
"STATE_D" -> "SYMBOL_z" [label="0.3333333333333333", style="dashed"]
"STATE_D" -> "SYMBOL_y" [label="0.3333333333333333", style="dashed"]
"STATE_E" -> "SYMBOL_x" [label="9.997000899730082e-05", style="dashed"]
"STATE_E" -> "SYMBOL_z" [label="0.8331833783198375", style="dashed"]
"STATE_E" -> "SYMBOL_y" [label="0.1667166516711653", style="dashed"]
"STATE_F" -> "SYMBOL_x" [label="0.3333333333333333", style="dashed"]
"STATE_F" -> "SYMBOL_z" [label="0.3333333333333333", style="dashed"]
"STATE_F" -> "SYMBOL_y" [label="0.3333333333333333", style="dashed"]
}
```

</div>

`{bm-enable-all}`

