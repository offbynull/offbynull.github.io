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
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="nan", style="dashed"]
"SYMBOL_x" [label="x", style="dashed"]
"STATE_A" -> "SYMBOL_x" [label="nan", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="nan", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="nan", style="dashed"]
"STATE_B" -> "SYMBOL_x" [label="nan", style="dashed"]
"STATE_D" -> "SYMBOL_z" [label="nan", style="dashed"]
"STATE_D" -> "SYMBOL_y" [label="nan", style="dashed"]
"STATE_D" -> "SYMBOL_x" [label="nan", style="dashed"]
"STATE_E" -> "SYMBOL_z" [label="nan", style="dashed"]
"STATE_E" -> "SYMBOL_y" [label="nan", style="dashed"]
"STATE_E" -> "SYMBOL_x" [label="nan", style="dashed"]
"STATE_F" -> "SYMBOL_z" [label="nan", style="dashed"]
"STATE_F" -> "SYMBOL_y" [label="nan", style="dashed"]
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
"STATE_A" -> "STATE_B" [label="0.47102403612874233"]
"STATE_A" -> "STATE_E" [label="0.20246005676152373"]
"STATE_A" -> "STATE_F" [label="0.32651590710973394"]
"STATE_B" -> "STATE_C" [label="0.47997989260216756"]
"STATE_B" -> "STATE_D" [label="0.5200201073978323"]
"STATE_C" -> "STATE_F" [label="1.0"]
"STATE_D" -> "STATE_A" [label="1.0"]
"STATE_E" -> "STATE_A" [label="1.0"]
"STATE_F" -> "STATE_B" [label="0.5561589916856062"]
"STATE_F" -> "STATE_E" [label="0.4438410083143938"]
"STATE_SOURCE" -> "STATE_A" [label="0.06917571395571083"]
"STATE_SOURCE" -> "STATE_B" [label="0.3136770049854148"]
"STATE_SOURCE" -> "STATE_D" [label="0.6171472810588743"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="0.36100468860575474", style="dashed"]
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="0.23741529968573585", style="dashed"]
"SYMBOL_x" [label="x", style="dashed"]
"STATE_A" -> "SYMBOL_x" [label="0.4015800117085096", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="0.32077644089994617", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="0.3141527992847499", style="dashed"]
"STATE_B" -> "SYMBOL_x" [label="0.36507075981530407", style="dashed"]
"STATE_D" -> "SYMBOL_z" [label="0.3385767633159314", style="dashed"]
"STATE_D" -> "SYMBOL_y" [label="0.12595185483657076", style="dashed"]
"STATE_D" -> "SYMBOL_x" [label="0.5354713818474979", style="dashed"]
"STATE_E" -> "SYMBOL_z" [label="0.4736918743712097", style="dashed"]
"STATE_E" -> "SYMBOL_y" [label="0.2645074366378951", style="dashed"]
"STATE_E" -> "SYMBOL_x" [label="0.2618006889908952", style="dashed"]
"STATE_F" -> "SYMBOL_z" [label="0.4487547875411792", style="dashed"]
"STATE_F" -> "SYMBOL_y" [label="0.4669920697237672", style="dashed"]
"STATE_F" -> "SYMBOL_x" [label="0.08425314273505348", style="dashed"]
}
```

Applying Viterbi learning for 3 cycles ...

 1. Hidden path for emitted sequence: SOURCE→D, D→A, A→B, B→C, C→F, F→E, E→A, A→F, F→B, B→C, C→F, F→E, E→A, A→B, B→D

    New transition probabilities:
    * SOURCE→B = 9.997000899730082e-05
    * SOURCE→D = 0.9998000599820054
    * SOURCE→A = 9.997000899730082e-05
    * A→B = 0.49995001499550135
    * A→F = 0.49995001499550135
    * A→E = 9.997000899730082e-05
    * B→C = 0.9999000199960009
    * B→D = 9.998000399920017e-05
    * C→F = 1.0
    * D→A = 1.0
    * E→A = 1.0
    * F→B = 0.333366660001333
    * F→E = 0.6666333399986669

    New emission probabilities:
    * (B, y) = 9.997000899730082e-05
    * (B, z) = 0.49995001499550135
    * (B, x) = 0.49995001499550135
    * (D, y) = 9.997000899730082e-05
    * (D, z) = 0.9998000599820054
    * (D, x) = 9.997000899730082e-05
    * (A, y) = 0.3333333333333333
    * (A, z) = 0.3333333333333333
    * (A, x) = 0.3333333333333333
    * (F, y) = 9.997000899730082e-05
    * (F, z) = 0.9998000599820054
    * (F, x) = 9.997000899730082e-05
    * (E, y) = 0.49995001499550135
    * (E, z) = 0.49995001499550135
    * (E, x) = 9.997000899730082e-05

 1. Hidden path for emitted sequence: SOURCE→D, D→A, A→B, B→C, C→F, F→B, B→C, C→F, F→E, E→A, A→F, F→B, B→C, C→F, F→E, E→A

    New transition probabilities:
    * SOURCE→B = 9.997000899730082e-05
    * SOURCE→D = 0.9998000599820054
    * SOURCE→A = 9.997000899730082e-05
    * A→B = 0.49995001499550135
    * A→F = 0.49995001499550135
    * A→E = 9.997000899730082e-05
    * B→C = 0.9999000199960009
    * B→D = 9.998000399920017e-05
    * C→F = 1.0
    * D→A = 1.0
    * E→A = 1.0
    * F→B = 0.6666333399986669
    * F→E = 0.333366660001333

    New emission probabilities:
    * (B, y) = 0.3333333333333333
    * (B, z) = 0.3333333333333333
    * (B, x) = 0.3333333333333333
    * (D, y) = 9.997000899730082e-05
    * (D, z) = 0.9998000599820054
    * (D, x) = 9.997000899730082e-05
    * (A, y) = 9.997000899730082e-05
    * (A, z) = 0.9998000599820054
    * (A, x) = 9.997000899730082e-05
    * (F, y) = 9.997000899730082e-05
    * (F, z) = 0.9998000599820054
    * (F, x) = 9.997000899730082e-05
    * (E, y) = 9.997000899730082e-05
    * (E, z) = 0.9998000599820054
    * (E, x) = 9.997000899730082e-05

 1. Hidden path for emitted sequence: SOURCE→D, D→A, A→B, B→C, C→F, F→E, E→A, A→B, B→C, C→F, F→E, E→A, A→F, F→B, B→C, C→F

    New transition probabilities:
    * SOURCE→B = 9.997000899730082e-05
    * SOURCE→D = 0.9998000599820054
    * SOURCE→A = 9.997000899730082e-05
    * A→B = 0.6665666966576693
    * A→F = 0.3333333333333333
    * A→E = 9.997000899730082e-05
    * B→C = 0.9999000199960009
    * B→D = 9.998000399920017e-05
    * C→F = 1.0
    * D→A = 1.0
    * E→A = 1.0
    * F→B = 9.998000399920017e-05
    * F→E = 0.9999000199960009

    New emission probabilities:
    * (B, y) = 9.997000899730082e-05
    * (B, z) = 0.49995001499550135
    * (B, x) = 0.49995001499550135
    * (D, y) = 9.997000899730082e-05
    * (D, z) = 0.9998000599820054
    * (D, x) = 9.997000899730082e-05
    * (A, y) = 0.6665666966576693
    * (A, z) = 0.3333333333333333
    * (A, x) = 9.997000899730082e-05
    * (F, y) = 9.997000899730082e-05
    * (F, z) = 0.6665666966576693
    * (F, x) = 0.3333333333333333
    * (E, y) = 9.997000899730082e-05
    * (E, z) = 0.9998000599820054
    * (E, x) = 9.997000899730082e-05


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
"STATE_A" -> "STATE_B" [label="0.6665666966576693"]
"STATE_A" -> "STATE_E" [label="9.997000899730082e-05"]
"STATE_A" -> "STATE_F" [label="0.3333333333333333"]
"STATE_B" -> "STATE_C" [label="0.9999000199960009"]
"STATE_B" -> "STATE_D" [label="9.998000399920017e-05"]
"STATE_C" -> "STATE_F" [label="1.0"]
"STATE_D" -> "STATE_A" [label="1.0"]
"STATE_E" -> "STATE_A" [label="1.0"]
"STATE_F" -> "STATE_B" [label="9.998000399920017e-05"]
"STATE_F" -> "STATE_E" [label="0.9999000199960009"]
"STATE_SOURCE" -> "STATE_A" [label="9.997000899730082e-05"]
"STATE_SOURCE" -> "STATE_B" [label="9.997000899730082e-05"]
"STATE_SOURCE" -> "STATE_D" [label="0.9998000599820054"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="0.3333333333333333", style="dashed"]
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="0.6665666966576693", style="dashed"]
"SYMBOL_x" [label="x", style="dashed"]
"STATE_A" -> "SYMBOL_x" [label="9.997000899730082e-05", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="0.49995001499550135", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="9.997000899730082e-05", style="dashed"]
"STATE_B" -> "SYMBOL_x" [label="0.49995001499550135", style="dashed"]
"STATE_D" -> "SYMBOL_z" [label="0.9998000599820054", style="dashed"]
"STATE_D" -> "SYMBOL_y" [label="9.997000899730082e-05", style="dashed"]
"STATE_D" -> "SYMBOL_x" [label="9.997000899730082e-05", style="dashed"]
"STATE_E" -> "SYMBOL_z" [label="0.9998000599820054", style="dashed"]
"STATE_E" -> "SYMBOL_y" [label="9.997000899730082e-05", style="dashed"]
"STATE_E" -> "SYMBOL_x" [label="9.997000899730082e-05", style="dashed"]
"STATE_F" -> "SYMBOL_z" [label="0.6665666966576693", style="dashed"]
"STATE_F" -> "SYMBOL_y" [label="9.997000899730082e-05", style="dashed"]
"STATE_F" -> "SYMBOL_x" [label="0.3333333333333333", style="dashed"]
}
```

</div>

`{bm-enable-all}`

