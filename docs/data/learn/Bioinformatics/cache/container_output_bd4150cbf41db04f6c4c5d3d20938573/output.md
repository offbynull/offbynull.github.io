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
"STATE_A" -> "STATE_B" [label="0.3318115610747224"]
"STATE_A" -> "STATE_E" [label="0.09703590330999205"]
"STATE_A" -> "STATE_F" [label="0.5711525356152856"]
"STATE_B" -> "STATE_C" [label="0.205038912797454"]
"STATE_B" -> "STATE_D" [label="0.794961087202546"]
"STATE_C" -> "STATE_F" [label="1.0"]
"STATE_D" -> "STATE_A" [label="1.0"]
"STATE_E" -> "STATE_A" [label="1.0"]
"STATE_F" -> "STATE_B" [label="0.3021878939266843"]
"STATE_F" -> "STATE_E" [label="0.6978121060733157"]
"STATE_SOURCE" -> "STATE_A" [label="0.2924225200487298"]
"STATE_SOURCE" -> "STATE_B" [label="0.2566756848733294"]
"STATE_SOURCE" -> "STATE_D" [label="0.45090179507794087"]
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="0.40643196357567785", style="dashed"]
"SYMBOL_x" [label="x", style="dashed"]
"STATE_A" -> "SYMBOL_x" [label="0.2979142374343824", style="dashed"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="0.2956537989899398", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="0.20782300695332215", style="dashed"]
"STATE_B" -> "SYMBOL_x" [label="0.35555567865230603", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="0.4366213143943719", style="dashed"]
"STATE_D" -> "SYMBOL_y" [label="0.22274312963608095", style="dashed"]
"STATE_D" -> "SYMBOL_x" [label="0.3881792851903411", style="dashed"]
"STATE_D" -> "SYMBOL_z" [label="0.38907758517357793", style="dashed"]
"STATE_E" -> "SYMBOL_y" [label="0.5494536205933639", style="dashed"]
"STATE_E" -> "SYMBOL_x" [label="0.18378284928547364", style="dashed"]
"STATE_E" -> "SYMBOL_z" [label="0.2667635301211625", style="dashed"]
"STATE_F" -> "SYMBOL_y" [label="0.41932916214983046", style="dashed"]
"STATE_F" -> "SYMBOL_x" [label="0.23339697037023058", style="dashed"]
"STATE_F" -> "SYMBOL_z" [label="0.34727386747993905", style="dashed"]
}
```

Applying Viterbi learning for 3 cycles ...

 1. Hidden path for emitted sequence: SOURCE→B, B→D, D→A, A→F, F→B, B→D, D→A, A→B, B→D, D→A, A→F, F→E, E→A

    New transition probabilities:
    * SOURCE→A = 9.997000899730082e-05
    * SOURCE→B = 0.9998000599820054
    * SOURCE→D = 9.997000899730082e-05
    * A→B = 0.3333333333333333
    * A→E = 9.997000899730082e-05
    * A→F = 0.6665666966576693
    * B→C = 9.998000399920017e-05
    * B→D = 0.9999000199960009
    * C→F = 1.0
    * D→A = 1.0
    * E→A = 1.0
    * F→B = 0.5
    * F→E = 0.5

    New emission probabilities:
    * (A, y) = 0.2500249925022493
    * (A, x) = 0.49995001499550135
    * (A, z) = 0.2500249925022493
    * (B, y) = 9.997000899730082e-05
    * (B, x) = 9.997000899730082e-05
    * (B, z) = 0.9998000599820054
    * (D, y) = 9.997000899730082e-05
    * (D, x) = 9.997000899730082e-05
    * (D, z) = 0.9998000599820054
    * (E, y) = 0.9998000599820054
    * (E, x) = 9.997000899730082e-05
    * (E, z) = 9.997000899730082e-05
    * (F, y) = 9.997000899730082e-05
    * (F, x) = 9.997000899730082e-05
    * (F, z) = 0.9998000599820054

 1. Hidden path for emitted sequence: SOURCE→B, B→D, D→A, A→F, F→B, B→D, D→A, A→B, B→D, D→A, A→F, F→E, E→A

    New transition probabilities:
    * SOURCE→A = 9.997000899730082e-05
    * SOURCE→B = 0.9998000599820054
    * SOURCE→D = 9.997000899730082e-05
    * A→B = 0.3333333333333333
    * A→E = 9.997000899730082e-05
    * A→F = 0.6665666966576693
    * B→C = 9.998000399920017e-05
    * B→D = 0.9999000199960009
    * C→F = 1.0
    * D→A = 1.0
    * E→A = 1.0
    * F→B = 0.5
    * F→E = 0.5

    New emission probabilities:
    * (A, y) = 0.2500249925022493
    * (A, x) = 0.49995001499550135
    * (A, z) = 0.2500249925022493
    * (B, y) = 9.997000899730082e-05
    * (B, x) = 9.997000899730082e-05
    * (B, z) = 0.9998000599820054
    * (D, y) = 9.997000899730082e-05
    * (D, x) = 9.997000899730082e-05
    * (D, z) = 0.9998000599820054
    * (E, y) = 0.9998000599820054
    * (E, x) = 9.997000899730082e-05
    * (E, z) = 9.997000899730082e-05
    * (F, y) = 9.997000899730082e-05
    * (F, x) = 9.997000899730082e-05
    * (F, z) = 0.9998000599820054

 1. Hidden path for emitted sequence: SOURCE→B, B→D, D→A, A→F, F→B, B→D, D→A, A→B, B→D, D→A, A→F, F→E, E→A

    New transition probabilities:
    * SOURCE→A = 9.997000899730082e-05
    * SOURCE→B = 0.9998000599820054
    * SOURCE→D = 9.997000899730082e-05
    * A→B = 0.3333333333333333
    * A→E = 9.997000899730082e-05
    * A→F = 0.6665666966576693
    * B→C = 9.998000399920017e-05
    * B→D = 0.9999000199960009
    * C→F = 1.0
    * D→A = 1.0
    * E→A = 1.0
    * F→B = 0.5
    * F→E = 0.5

    New emission probabilities:
    * (A, y) = 0.2500249925022493
    * (A, x) = 0.49995001499550135
    * (A, z) = 0.2500249925022493
    * (B, y) = 9.997000899730082e-05
    * (B, x) = 9.997000899730082e-05
    * (B, z) = 0.9998000599820054
    * (D, y) = 9.997000899730082e-05
    * (D, x) = 9.997000899730082e-05
    * (D, z) = 0.9998000599820054
    * (E, y) = 0.9998000599820054
    * (E, x) = 9.997000899730082e-05
    * (E, z) = 9.997000899730082e-05
    * (F, y) = 9.997000899730082e-05
    * (F, x) = 9.997000899730082e-05
    * (F, z) = 0.9998000599820054


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
"STATE_A" -> "STATE_B" [label="0.3333333333333333"]
"STATE_A" -> "STATE_E" [label="9.997000899730082e-05"]
"STATE_A" -> "STATE_F" [label="0.6665666966576693"]
"STATE_B" -> "STATE_C" [label="9.998000399920017e-05"]
"STATE_B" -> "STATE_D" [label="0.9999000199960009"]
"STATE_C" -> "STATE_F" [label="1.0"]
"STATE_D" -> "STATE_A" [label="1.0"]
"STATE_E" -> "STATE_A" [label="1.0"]
"STATE_F" -> "STATE_B" [label="0.5"]
"STATE_F" -> "STATE_E" [label="0.5"]
"STATE_SOURCE" -> "STATE_A" [label="9.997000899730082e-05"]
"STATE_SOURCE" -> "STATE_B" [label="0.9998000599820054"]
"STATE_SOURCE" -> "STATE_D" [label="9.997000899730082e-05"]
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="0.2500249925022493", style="dashed"]
"SYMBOL_x" [label="x", style="dashed"]
"STATE_A" -> "SYMBOL_x" [label="0.49995001499550135", style="dashed"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="0.2500249925022493", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="9.997000899730082e-05", style="dashed"]
"STATE_B" -> "SYMBOL_x" [label="9.997000899730082e-05", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="0.9998000599820054", style="dashed"]
"STATE_D" -> "SYMBOL_y" [label="9.997000899730082e-05", style="dashed"]
"STATE_D" -> "SYMBOL_x" [label="9.997000899730082e-05", style="dashed"]
"STATE_D" -> "SYMBOL_z" [label="0.9998000599820054", style="dashed"]
"STATE_E" -> "SYMBOL_y" [label="0.9998000599820054", style="dashed"]
"STATE_E" -> "SYMBOL_x" [label="9.997000899730082e-05", style="dashed"]
"STATE_E" -> "SYMBOL_z" [label="9.997000899730082e-05", style="dashed"]
"STATE_F" -> "SYMBOL_y" [label="9.997000899730082e-05", style="dashed"]
"STATE_F" -> "SYMBOL_x" [label="9.997000899730082e-05", style="dashed"]
"STATE_F" -> "SYMBOL_z" [label="0.9998000599820054", style="dashed"]
}
```

</div>

`{bm-enable-all}`

