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
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="nan", style="dashed"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="nan", style="dashed"]
"STATE_B" -> "SYMBOL_x" [label="nan", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="nan", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="nan", style="dashed"]
"STATE_D" -> "SYMBOL_x" [label="nan", style="dashed"]
"STATE_D" -> "SYMBOL_y" [label="nan", style="dashed"]
"STATE_D" -> "SYMBOL_z" [label="nan", style="dashed"]
"STATE_E" -> "SYMBOL_x" [label="nan", style="dashed"]
"STATE_E" -> "SYMBOL_y" [label="nan", style="dashed"]
"STATE_E" -> "SYMBOL_z" [label="nan", style="dashed"]
"STATE_F" -> "SYMBOL_x" [label="nan", style="dashed"]
"STATE_F" -> "SYMBOL_y" [label="nan", style="dashed"]
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
"STATE_A" -> "STATE_B" [label="0.5559885902380229"]
"STATE_A" -> "STATE_E" [label="0.1363407019468231"]
"STATE_A" -> "STATE_F" [label="0.30767070781515393"]
"STATE_B" -> "STATE_C" [label="0.627783545469645"]
"STATE_B" -> "STATE_D" [label="0.372216454530355"]
"STATE_C" -> "STATE_F" [label="1.0"]
"STATE_D" -> "STATE_A" [label="1.0"]
"STATE_E" -> "STATE_A" [label="1.0"]
"STATE_F" -> "STATE_B" [label="0.5576076914098105"]
"STATE_F" -> "STATE_E" [label="0.4423923085901896"]
"STATE_SOURCE" -> "STATE_A" [label="0.39818324349807754"]
"STATE_SOURCE" -> "STATE_B" [label="0.33370264446175946"]
"STATE_SOURCE" -> "STATE_D" [label="0.26811411204016294"]
"SYMBOL_x" [label="x", style="dashed"]
"STATE_A" -> "SYMBOL_x" [label="0.45957318563227717", style="dashed"]
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="0.08251984554282275", style="dashed"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="0.4579069688249", style="dashed"]
"STATE_B" -> "SYMBOL_x" [label="0.190510553731653", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="0.3097014582835506", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="0.4997879879847964", style="dashed"]
"STATE_D" -> "SYMBOL_x" [label="0.16032473821929258", style="dashed"]
"STATE_D" -> "SYMBOL_y" [label="0.47541325285248515", style="dashed"]
"STATE_D" -> "SYMBOL_z" [label="0.36426200892822236", style="dashed"]
"STATE_E" -> "SYMBOL_x" [label="0.1367136229554001", style="dashed"]
"STATE_E" -> "SYMBOL_y" [label="0.3663757833926074", style="dashed"]
"STATE_E" -> "SYMBOL_z" [label="0.49691059365199247", style="dashed"]
"STATE_F" -> "SYMBOL_x" [label="0.37708910556448216", style="dashed"]
"STATE_F" -> "SYMBOL_y" [label="0.16002458485827312", style="dashed"]
"STATE_F" -> "SYMBOL_z" [label="0.46288630957724475", style="dashed"]
}
```

Applying Viterbi learning for 3 cycles ...

 1. Hidden path for emitted sequence: SOURCE→A, A→B, B→C, C→F, F→E, E→A, A→B, B→D, D→A, A→B, B→C, C→F, F→B, B→D, D→A

    New transition probabilities:
    * SOURCE→D = 9.997000899730082e-05
    * SOURCE→A = 0.9998000599820054
    * SOURCE→B = 9.997000899730082e-05
    * A→E = 9.997000899730082e-05
    * A→F = 9.997000899730082e-05
    * A→B = 0.9998000599820054
    * B→D = 0.333366660001333
    * B→C = 0.6666333399986669
    * C→F = 1.0
    * D→A = 1.0
    * E→A = 1.0
    * F→E = 0.5
    * F→B = 0.5

    New emission probabilities:
    * (D, x) = 9.997000899730082e-05
    * (D, z) = 0.9998000599820054
    * (D, y) = 9.997000899730082e-05
    * (A, x) = 9.997000899730082e-05
    * (A, z) = 0.9998000599820054
    * (A, y) = 9.997000899730082e-05
    * (B, x) = 0.2500249925022493
    * (B, z) = 0.49995001499550135
    * (B, y) = 0.2500249925022493
    * (E, x) = 9.997000899730082e-05
    * (E, z) = 0.9998000599820054
    * (E, y) = 9.997000899730082e-05
    * (F, x) = 9.997000899730082e-05
    * (F, z) = 0.49995001499550135
    * (F, y) = 0.49995001499550135

 1. Hidden path for emitted sequence: SOURCE→A, A→B, B→C, C→F, F→E, E→A, A→B, B→C, C→F, F→B, B→D, D→A, A→B, B→C, C→F, F→B

    New transition probabilities:
    * SOURCE→D = 9.997000899730082e-05
    * SOURCE→A = 0.9998000599820054
    * SOURCE→B = 9.997000899730082e-05
    * A→E = 9.997000899730082e-05
    * A→F = 9.997000899730082e-05
    * A→B = 0.9998000599820054
    * B→D = 0.333366660001333
    * B→C = 0.6666333399986669
    * C→F = 1.0
    * D→A = 1.0
    * E→A = 1.0
    * F→E = 0.5
    * F→B = 0.5

    New emission probabilities:
    * (D, x) = 9.997000899730082e-05
    * (D, z) = 0.9998000599820054
    * (D, y) = 9.997000899730082e-05
    * (A, x) = 9.997000899730082e-05
    * (A, z) = 0.6665666966576693
    * (A, y) = 0.3333333333333333
    * (B, x) = 0.2500249925022493
    * (B, z) = 0.49995001499550135
    * (B, y) = 0.2500249925022493
    * (E, x) = 9.997000899730082e-05
    * (E, z) = 0.9998000599820054
    * (E, y) = 9.997000899730082e-05
    * (F, x) = 9.997000899730082e-05
    * (F, z) = 0.9998000599820054
    * (F, y) = 9.997000899730082e-05

 1. Hidden path for emitted sequence: SOURCE→D, D→A, A→B, B→C, C→F, F→E, E→A, A→B, B→C, C→F, F→B, B→C, C→F, F→E, E→A, A→B

    New transition probabilities:
    * SOURCE→D = 0.9998000599820054
    * SOURCE→A = 9.997000899730082e-05
    * SOURCE→B = 9.997000899730082e-05
    * A→E = 9.997000899730082e-05
    * A→F = 9.997000899730082e-05
    * A→B = 0.9998000599820054
    * B→D = 9.998000399920017e-05
    * B→C = 0.9999000199960009
    * C→F = 1.0
    * D→A = 1.0
    * E→A = 1.0
    * F→E = 0.5
    * F→B = 0.5

    New emission probabilities:
    * (D, x) = 9.997000899730082e-05
    * (D, z) = 0.9998000599820054
    * (D, y) = 9.997000899730082e-05
    * (A, x) = 9.997000899730082e-05
    * (A, z) = 0.49995001499550135
    * (A, y) = 0.49995001499550135
    * (B, x) = 0.3333333333333333
    * (B, z) = 0.6665666966576693
    * (B, y) = 9.997000899730082e-05
    * (E, x) = 9.997000899730082e-05
    * (E, z) = 0.9998000599820054
    * (E, y) = 9.997000899730082e-05
    * (F, x) = 0.3333333333333333
    * (F, z) = 0.6665666966576693
    * (F, y) = 9.997000899730082e-05


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
"STATE_A" -> "STATE_B" [label="0.9998000599820054"]
"STATE_A" -> "STATE_E" [label="9.997000899730082e-05"]
"STATE_A" -> "STATE_F" [label="9.997000899730082e-05"]
"STATE_B" -> "STATE_C" [label="0.9999000199960009"]
"STATE_B" -> "STATE_D" [label="9.998000399920017e-05"]
"STATE_C" -> "STATE_F" [label="1.0"]
"STATE_D" -> "STATE_A" [label="1.0"]
"STATE_E" -> "STATE_A" [label="1.0"]
"STATE_F" -> "STATE_B" [label="0.5"]
"STATE_F" -> "STATE_E" [label="0.5"]
"STATE_SOURCE" -> "STATE_A" [label="9.997000899730082e-05"]
"STATE_SOURCE" -> "STATE_B" [label="9.997000899730082e-05"]
"STATE_SOURCE" -> "STATE_D" [label="0.9998000599820054"]
"SYMBOL_x" [label="x", style="dashed"]
"STATE_A" -> "SYMBOL_x" [label="9.997000899730082e-05", style="dashed"]
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="0.49995001499550135", style="dashed"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="0.49995001499550135", style="dashed"]
"STATE_B" -> "SYMBOL_x" [label="0.3333333333333333", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="9.997000899730082e-05", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="0.6665666966576693", style="dashed"]
"STATE_D" -> "SYMBOL_x" [label="9.997000899730082e-05", style="dashed"]
"STATE_D" -> "SYMBOL_y" [label="9.997000899730082e-05", style="dashed"]
"STATE_D" -> "SYMBOL_z" [label="0.9998000599820054", style="dashed"]
"STATE_E" -> "SYMBOL_x" [label="9.997000899730082e-05", style="dashed"]
"STATE_E" -> "SYMBOL_y" [label="9.997000899730082e-05", style="dashed"]
"STATE_E" -> "SYMBOL_z" [label="0.9998000599820054", style="dashed"]
"STATE_F" -> "SYMBOL_x" [label="0.3333333333333333", style="dashed"]
"STATE_F" -> "SYMBOL_y" [label="9.997000899730082e-05", style="dashed"]
"STATE_F" -> "SYMBOL_z" [label="0.6665666966576693", style="dashed"]
}
```

</div>

`{bm-enable-all}`
