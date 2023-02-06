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
"STATE_A" -> "STATE_B" [label="0.29592204239442627"]
"STATE_A" -> "STATE_E" [label="0.2658942758661529"]
"STATE_A" -> "STATE_F" [label="0.4381836817394208"]
"STATE_B" -> "STATE_C" [label="0.03770977350957017"]
"STATE_B" -> "STATE_D" [label="0.9622902264904298"]
"STATE_C" -> "STATE_F" [label="1.0"]
"STATE_D" -> "STATE_A" [label="1.0"]
"STATE_E" -> "STATE_A" [label="1.0"]
"STATE_F" -> "STATE_B" [label="0.6055669639865234"]
"STATE_F" -> "STATE_E" [label="0.39443303601347657"]
"STATE_SOURCE" -> "STATE_A" [label="0.0723149618670648"]
"STATE_SOURCE" -> "STATE_B" [label="0.4300100480544382"]
"STATE_SOURCE" -> "STATE_D" [label="0.49767499007849697"]
"SYMBOL_x" [label="x", style="dashed"]
"STATE_A" -> "SYMBOL_x" [label="0.6557502338790505", style="dashed"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="0.19539360662600835", style="dashed"]
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="0.1488561594949412", style="dashed"]
"STATE_B" -> "SYMBOL_x" [label="0.5876802740293005", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="0.20212206622887186", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="0.21019765974182772", style="dashed"]
"STATE_D" -> "SYMBOL_x" [label="0.07141147997934821", style="dashed"]
"STATE_D" -> "SYMBOL_z" [label="0.4631434883956674", style="dashed"]
"STATE_D" -> "SYMBOL_y" [label="0.46544503162498446", style="dashed"]
"STATE_E" -> "SYMBOL_x" [label="0.2556158583475854", style="dashed"]
"STATE_E" -> "SYMBOL_z" [label="0.6913378514017167", style="dashed"]
"STATE_E" -> "SYMBOL_y" [label="0.05304629025069793", style="dashed"]
"STATE_F" -> "SYMBOL_x" [label="0.42413063574350074", style="dashed"]
"STATE_F" -> "SYMBOL_z" [label="0.33067475348016606", style="dashed"]
"STATE_F" -> "SYMBOL_y" [label="0.2451946107763332", style="dashed"]
}
```

Applying Viterbi learning for 3 cycles ...

 1. Hidden path for emitted sequence: SOURCE→B, B→D, D→A, A→E, E→A, A→F, F→B, B→D, D→A, A→F, F→B, B→D, D→A

    New transition probabilities:
    * SOURCE→A = 9.997000899730082e-05
    * SOURCE→D = 9.997000899730082e-05
    * SOURCE→B = 0.9998000599820054
    * A→F = 0.6665666966576693
    * A→E = 0.3333333333333333
    * A→B = 9.997000899730082e-05
    * B→D = 0.9999000199960009
    * B→C = 9.998000399920017e-05
    * C→F = 1.0
    * D→A = 1.0
    * E→A = 1.0
    * F→E = 9.998000399920017e-05
    * F→B = 0.9999000199960009

    New emission probabilities:
    * (A, x) = 0.49995001499550135
    * (A, z) = 0.49995001499550135
    * (A, y) = 9.997000899730082e-05
    * (D, x) = 9.997000899730082e-05
    * (D, z) = 0.6665666966576693
    * (D, y) = 0.3333333333333333
    * (B, x) = 9.997000899730082e-05
    * (B, z) = 0.6665666966576693
    * (B, y) = 0.3333333333333333
    * (F, x) = 9.997000899730082e-05
    * (F, z) = 0.9998000599820054
    * (F, y) = 9.997000899730082e-05
    * (E, x) = 9.997000899730082e-05
    * (E, z) = 0.9998000599820054
    * (E, y) = 9.997000899730082e-05

 1. Hidden path for emitted sequence: SOURCE→B, B→D, D→A, A→E, E→A, A→F, F→B, B→D, D→A, A→F, F→B, B→D, D→A

    New transition probabilities:
    * SOURCE→A = 9.997000899730082e-05
    * SOURCE→D = 9.997000899730082e-05
    * SOURCE→B = 0.9998000599820054
    * A→F = 0.6665666966576693
    * A→E = 0.3333333333333333
    * A→B = 9.997000899730082e-05
    * B→D = 0.9999000199960009
    * B→C = 9.998000399920017e-05
    * C→F = 1.0
    * D→A = 1.0
    * E→A = 1.0
    * F→E = 9.998000399920017e-05
    * F→B = 0.9999000199960009

    New emission probabilities:
    * (A, x) = 0.49995001499550135
    * (A, z) = 0.49995001499550135
    * (A, y) = 9.997000899730082e-05
    * (D, x) = 9.997000899730082e-05
    * (D, z) = 0.6665666966576693
    * (D, y) = 0.3333333333333333
    * (B, x) = 9.997000899730082e-05
    * (B, z) = 0.6665666966576693
    * (B, y) = 0.3333333333333333
    * (F, x) = 9.997000899730082e-05
    * (F, z) = 0.9998000599820054
    * (F, y) = 9.997000899730082e-05
    * (E, x) = 9.997000899730082e-05
    * (E, z) = 0.9998000599820054
    * (E, y) = 9.997000899730082e-05

 1. Hidden path for emitted sequence: SOURCE→B, B→D, D→A, A→E, E→A, A→F, F→B, B→D, D→A, A→F, F→B, B→D, D→A

    New transition probabilities:
    * SOURCE→A = 9.997000899730082e-05
    * SOURCE→D = 9.997000899730082e-05
    * SOURCE→B = 0.9998000599820054
    * A→F = 0.6665666966576693
    * A→E = 0.3333333333333333
    * A→B = 9.997000899730082e-05
    * B→D = 0.9999000199960009
    * B→C = 9.998000399920017e-05
    * C→F = 1.0
    * D→A = 1.0
    * E→A = 1.0
    * F→E = 9.998000399920017e-05
    * F→B = 0.9999000199960009

    New emission probabilities:
    * (A, x) = 0.49995001499550135
    * (A, z) = 0.49995001499550135
    * (A, y) = 9.997000899730082e-05
    * (D, x) = 9.997000899730082e-05
    * (D, z) = 0.6665666966576693
    * (D, y) = 0.3333333333333333
    * (B, x) = 9.997000899730082e-05
    * (B, z) = 0.6665666966576693
    * (B, y) = 0.3333333333333333
    * (F, x) = 9.997000899730082e-05
    * (F, z) = 0.9998000599820054
    * (F, y) = 9.997000899730082e-05
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
"STATE_A" -> "STATE_B" [label="9.997000899730082e-05"]
"STATE_A" -> "STATE_E" [label="0.3333333333333333"]
"STATE_A" -> "STATE_F" [label="0.6665666966576693"]
"STATE_B" -> "STATE_C" [label="9.998000399920017e-05"]
"STATE_B" -> "STATE_D" [label="0.9999000199960009"]
"STATE_C" -> "STATE_F" [label="1.0"]
"STATE_D" -> "STATE_A" [label="1.0"]
"STATE_E" -> "STATE_A" [label="1.0"]
"STATE_F" -> "STATE_B" [label="0.9999000199960009"]
"STATE_F" -> "STATE_E" [label="9.998000399920017e-05"]
"STATE_SOURCE" -> "STATE_A" [label="9.997000899730082e-05"]
"STATE_SOURCE" -> "STATE_B" [label="0.9998000599820054"]
"STATE_SOURCE" -> "STATE_D" [label="9.997000899730082e-05"]
"SYMBOL_x" [label="x", style="dashed"]
"STATE_A" -> "SYMBOL_x" [label="0.49995001499550135", style="dashed"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="0.49995001499550135", style="dashed"]
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="9.997000899730082e-05", style="dashed"]
"STATE_B" -> "SYMBOL_x" [label="9.997000899730082e-05", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="0.6665666966576693", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="0.3333333333333333", style="dashed"]
"STATE_D" -> "SYMBOL_x" [label="9.997000899730082e-05", style="dashed"]
"STATE_D" -> "SYMBOL_z" [label="0.6665666966576693", style="dashed"]
"STATE_D" -> "SYMBOL_y" [label="0.3333333333333333", style="dashed"]
"STATE_E" -> "SYMBOL_x" [label="9.997000899730082e-05", style="dashed"]
"STATE_E" -> "SYMBOL_z" [label="0.9998000599820054", style="dashed"]
"STATE_E" -> "SYMBOL_y" [label="9.997000899730082e-05", style="dashed"]
"STATE_F" -> "SYMBOL_x" [label="9.997000899730082e-05", style="dashed"]
"STATE_F" -> "SYMBOL_z" [label="0.9998000599820054", style="dashed"]
"STATE_F" -> "SYMBOL_y" [label="9.997000899730082e-05", style="dashed"]
}
```

</div>

`{bm-enable-all}`

