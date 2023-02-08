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
"SYMBOL_x" [label="x", style="dashed"]
"STATE_A" -> "SYMBOL_x" [label="nan", style="dashed"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="nan", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="nan", style="dashed"]
"STATE_B" -> "SYMBOL_x" [label="nan", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="nan", style="dashed"]
"STATE_D" -> "SYMBOL_y" [label="nan", style="dashed"]
"STATE_D" -> "SYMBOL_x" [label="nan", style="dashed"]
"STATE_D" -> "SYMBOL_z" [label="nan", style="dashed"]
"STATE_E" -> "SYMBOL_y" [label="nan", style="dashed"]
"STATE_E" -> "SYMBOL_x" [label="nan", style="dashed"]
"STATE_E" -> "SYMBOL_z" [label="nan", style="dashed"]
"STATE_F" -> "SYMBOL_y" [label="nan", style="dashed"]
"STATE_F" -> "SYMBOL_x" [label="nan", style="dashed"]
"STATE_F" -> "SYMBOL_z" [label="nan", style="dashed"]
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
"STATE_A" -> "STATE_B" [label="0.029957482743064638"]
"STATE_A" -> "STATE_E" [label="0.6780829643386523"]
"STATE_A" -> "STATE_F" [label="0.29195955291828296"]
"STATE_B" -> "STATE_C" [label="0.8507525515777299"]
"STATE_B" -> "STATE_D" [label="0.14924744842227008"]
"STATE_C" -> "STATE_F" [label="1.0"]
"STATE_D" -> "STATE_A" [label="1.0"]
"STATE_E" -> "STATE_A" [label="1.0"]
"STATE_F" -> "STATE_B" [label="0.6179165288623389"]
"STATE_F" -> "STATE_E" [label="0.38208347113766106"]
"STATE_SOURCE" -> "STATE_A" [label="0.06738256918470584"]
"STATE_SOURCE" -> "STATE_B" [label="0.5502130434170364"]
"STATE_SOURCE" -> "STATE_D" [label="0.3824043873982578"]
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="0.24373049287089207", style="dashed"]
"SYMBOL_x" [label="x", style="dashed"]
"STATE_A" -> "SYMBOL_x" [label="0.14705209302710465", style="dashed"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="0.6092174141020033", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="0.4611545104933137", style="dashed"]
"STATE_B" -> "SYMBOL_x" [label="0.4749036232280048", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="0.06394186627868155", style="dashed"]
"STATE_D" -> "SYMBOL_y" [label="0.32102591900688376", style="dashed"]
"STATE_D" -> "SYMBOL_x" [label="0.24211286486001343", style="dashed"]
"STATE_D" -> "SYMBOL_z" [label="0.4368612161331028", style="dashed"]
"STATE_E" -> "SYMBOL_y" [label="0.020384614493676553", style="dashed"]
"STATE_E" -> "SYMBOL_x" [label="0.4926431681169396", style="dashed"]
"STATE_E" -> "SYMBOL_z" [label="0.48697221738938384", style="dashed"]
"STATE_F" -> "SYMBOL_y" [label="0.314833044159627", style="dashed"]
"STATE_F" -> "SYMBOL_x" [label="0.3441045501310279", style="dashed"]
"STATE_F" -> "SYMBOL_z" [label="0.3410624057093451", style="dashed"]
}
```

Applying Viterbi learning for 3 cycles ...

 1. Hidden path for emitted sequence: SOURCE→D, D→A, A→E, E→A, A→E, E→A, A→F, F→E, E→A, A→E, E→A, A→F, F→B

    New transition probabilities:
    * SOURCE→A = 9.997000899730082e-05
    * SOURCE→B = 9.997000899730082e-05
    * SOURCE→D = 0.9998000599820054
    * A→E = 0.5999200239928022
    * A→B = 9.997000899730082e-05
    * A→F = 0.39998000599820055
    * B→D = 0.5
    * B→C = 0.5
    * C→F = 1.0
    * D→A = 1.0
    * E→A = 1.0
    * F→E = 0.5
    * F→B = 0.5

    New emission probabilities:
    * (A, y) = 9.997000899730082e-05
    * (A, x) = 9.997000899730082e-05
    * (A, z) = 0.9998000599820054
    * (B, y) = 9.997000899730082e-05
    * (B, x) = 0.9998000599820054
    * (B, z) = 9.997000899730082e-05
    * (D, y) = 9.997000899730082e-05
    * (D, x) = 9.997000899730082e-05
    * (D, z) = 0.9998000599820054
    * (E, y) = 9.997000899730082e-05
    * (E, x) = 0.2500249925022493
    * (E, z) = 0.7498750374887534
    * (F, y) = 0.9998000599820054
    * (F, x) = 9.997000899730082e-05
    * (F, z) = 9.997000899730082e-05

 1. Hidden path for emitted sequence: SOURCE→D, D→A, A→E, E→A, A→E, E→A, A→F, F→E, E→A, A→E, E→A, A→F, F→B

    New transition probabilities:
    * SOURCE→A = 9.997000899730082e-05
    * SOURCE→B = 9.997000899730082e-05
    * SOURCE→D = 0.9998000599820054
    * A→E = 0.5999200239928022
    * A→B = 9.997000899730082e-05
    * A→F = 0.39998000599820055
    * B→D = 0.5
    * B→C = 0.5
    * C→F = 1.0
    * D→A = 1.0
    * E→A = 1.0
    * F→E = 0.5
    * F→B = 0.5

    New emission probabilities:
    * (A, y) = 9.997000899730082e-05
    * (A, x) = 9.997000899730082e-05
    * (A, z) = 0.9998000599820054
    * (B, y) = 9.997000899730082e-05
    * (B, x) = 0.9998000599820054
    * (B, z) = 9.997000899730082e-05
    * (D, y) = 9.997000899730082e-05
    * (D, x) = 9.997000899730082e-05
    * (D, z) = 0.9998000599820054
    * (E, y) = 9.997000899730082e-05
    * (E, x) = 0.2500249925022493
    * (E, z) = 0.7498750374887534
    * (F, y) = 0.9998000599820054
    * (F, x) = 9.997000899730082e-05
    * (F, z) = 9.997000899730082e-05

 1. Hidden path for emitted sequence: SOURCE→D, D→A, A→E, E→A, A→E, E→A, A→F, F→E, E→A, A→E, E→A, A→F, F→B

    New transition probabilities:
    * SOURCE→A = 9.997000899730082e-05
    * SOURCE→B = 9.997000899730082e-05
    * SOURCE→D = 0.9998000599820054
    * A→E = 0.5999200239928022
    * A→B = 9.997000899730082e-05
    * A→F = 0.39998000599820055
    * B→D = 0.5
    * B→C = 0.5
    * C→F = 1.0
    * D→A = 1.0
    * E→A = 1.0
    * F→E = 0.5
    * F→B = 0.5

    New emission probabilities:
    * (A, y) = 9.997000899730082e-05
    * (A, x) = 9.997000899730082e-05
    * (A, z) = 0.9998000599820054
    * (B, y) = 9.997000899730082e-05
    * (B, x) = 0.9998000599820054
    * (B, z) = 9.997000899730082e-05
    * (D, y) = 9.997000899730082e-05
    * (D, x) = 9.997000899730082e-05
    * (D, z) = 0.9998000599820054
    * (E, y) = 9.997000899730082e-05
    * (E, x) = 0.2500249925022493
    * (E, z) = 0.7498750374887534
    * (F, y) = 0.9998000599820054
    * (F, x) = 9.997000899730082e-05
    * (F, z) = 9.997000899730082e-05


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
"STATE_A" -> "STATE_E" [label="0.5999200239928022"]
"STATE_A" -> "STATE_F" [label="0.39998000599820055"]
"STATE_B" -> "STATE_C" [label="0.5"]
"STATE_B" -> "STATE_D" [label="0.5"]
"STATE_C" -> "STATE_F" [label="1.0"]
"STATE_D" -> "STATE_A" [label="1.0"]
"STATE_E" -> "STATE_A" [label="1.0"]
"STATE_F" -> "STATE_B" [label="0.5"]
"STATE_F" -> "STATE_E" [label="0.5"]
"STATE_SOURCE" -> "STATE_A" [label="9.997000899730082e-05"]
"STATE_SOURCE" -> "STATE_B" [label="9.997000899730082e-05"]
"STATE_SOURCE" -> "STATE_D" [label="0.9998000599820054"]
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="9.997000899730082e-05", style="dashed"]
"SYMBOL_x" [label="x", style="dashed"]
"STATE_A" -> "SYMBOL_x" [label="9.997000899730082e-05", style="dashed"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="0.9998000599820054", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="9.997000899730082e-05", style="dashed"]
"STATE_B" -> "SYMBOL_x" [label="0.9998000599820054", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="9.997000899730082e-05", style="dashed"]
"STATE_D" -> "SYMBOL_y" [label="9.997000899730082e-05", style="dashed"]
"STATE_D" -> "SYMBOL_x" [label="9.997000899730082e-05", style="dashed"]
"STATE_D" -> "SYMBOL_z" [label="0.9998000599820054", style="dashed"]
"STATE_E" -> "SYMBOL_y" [label="9.997000899730082e-05", style="dashed"]
"STATE_E" -> "SYMBOL_x" [label="0.2500249925022493", style="dashed"]
"STATE_E" -> "SYMBOL_z" [label="0.7498750374887534", style="dashed"]
"STATE_F" -> "SYMBOL_y" [label="0.9998000599820054", style="dashed"]
"STATE_F" -> "SYMBOL_x" [label="9.997000899730082e-05", style="dashed"]
"STATE_F" -> "SYMBOL_z" [label="9.997000899730082e-05", style="dashed"]
}
```

</div>

`{bm-enable-all}`

