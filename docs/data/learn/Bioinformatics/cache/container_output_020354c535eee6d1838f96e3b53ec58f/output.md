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
"STATE_A" -> "STATE_B" [label="0.2503595418585913"]
"STATE_A" -> "STATE_E" [label="0.4197950266675402"]
"STATE_A" -> "STATE_F" [label="0.3298454314738686"]
"STATE_B" -> "STATE_C" [label="0.1492293607659141"]
"STATE_B" -> "STATE_D" [label="0.8507706392340859"]
"STATE_C" -> "STATE_F" [label="1.0"]
"STATE_D" -> "STATE_A" [label="1.0"]
"STATE_E" -> "STATE_A" [label="1.0"]
"STATE_F" -> "STATE_B" [label="0.8263590738663849"]
"STATE_F" -> "STATE_E" [label="0.17364092613361515"]
"STATE_SOURCE" -> "STATE_A" [label="0.48352454001374795"]
"STATE_SOURCE" -> "STATE_B" [label="0.10198505897095514"]
"STATE_SOURCE" -> "STATE_D" [label="0.4144904010152968"]
"SYMBOL_x" [label="x", style="dashed"]
"STATE_A" -> "SYMBOL_x" [label="0.17218217761728194", style="dashed"]
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="0.3823421040841842", style="dashed"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="0.445475718298534", style="dashed"]
"STATE_B" -> "SYMBOL_x" [label="0.2344416601626744", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="0.5326211384602371", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="0.2329372013770885", style="dashed"]
"STATE_D" -> "SYMBOL_x" [label="0.041071523142712944", style="dashed"]
"STATE_D" -> "SYMBOL_y" [label="0.3849281771957611", style="dashed"]
"STATE_D" -> "SYMBOL_z" [label="0.5740002996615259", style="dashed"]
"STATE_E" -> "SYMBOL_x" [label="0.2616988019473071", style="dashed"]
"STATE_E" -> "SYMBOL_y" [label="0.26036540887451937", style="dashed"]
"STATE_E" -> "SYMBOL_z" [label="0.4779357891781734", style="dashed"]
"STATE_F" -> "SYMBOL_x" [label="0.3976531499737627", style="dashed"]
"STATE_F" -> "SYMBOL_y" [label="0.27166718851347976", style="dashed"]
"STATE_F" -> "SYMBOL_z" [label="0.3306796615127576", style="dashed"]
}
```

Applying Viterbi learning for 3 cycles ...

 1. Hidden path for emitted sequence: SOURCE→D, D→A, A→F, F→B, B→D, D→A, A→B, B→D, D→A, A→E, E→A, A→E, E→A

    New transition probabilities:
    * SOURCE→D = 0.9998000599820054
    * SOURCE→B = 9.997000899730082e-05
    * SOURCE→A = 9.997000899730082e-05
    * A→E = 0.49995001499550135
    * A→B = 0.2500249925022493
    * A→F = 0.2500249925022493
    * B→D = 0.9999000199960009
    * B→C = 9.998000399920017e-05
    * C→F = 1.0
    * D→A = 1.0
    * E→A = 1.0
    * F→E = 9.998000399920017e-05
    * F→B = 0.9999000199960009

    New emission probabilities:
    * (D, z) = 0.9998000599820054
    * (D, y) = 9.997000899730082e-05
    * (D, x) = 9.997000899730082e-05
    * (B, z) = 0.49995001499550135
    * (B, y) = 0.49995001499550135
    * (B, x) = 9.997000899730082e-05
    * (A, z) = 0.7998600419874038
    * (A, y) = 9.997000899730082e-05
    * (A, x) = 0.20003998800359893
    * (E, z) = 0.49995001499550135
    * (E, y) = 0.49995001499550135
    * (E, x) = 9.997000899730082e-05
    * (F, z) = 9.997000899730082e-05
    * (F, y) = 9.997000899730082e-05
    * (F, x) = 0.9998000599820054

 1. Hidden path for emitted sequence: SOURCE→D, D→A, A→F, F→B, B→D, D→A, A→E, E→A, A→B, B→D, D→A, A→E, E→A

    New transition probabilities:
    * SOURCE→D = 0.9998000599820054
    * SOURCE→B = 9.997000899730082e-05
    * SOURCE→A = 9.997000899730082e-05
    * A→E = 0.49995001499550135
    * A→B = 0.2500249925022493
    * A→F = 0.2500249925022493
    * B→D = 0.9999000199960009
    * B→C = 9.998000399920017e-05
    * C→F = 1.0
    * D→A = 1.0
    * E→A = 1.0
    * F→E = 9.998000399920017e-05
    * F→B = 0.9999000199960009

    New emission probabilities:
    * (D, z) = 0.9998000599820054
    * (D, y) = 9.997000899730082e-05
    * (D, x) = 9.997000899730082e-05
    * (B, z) = 0.9998000599820054
    * (B, y) = 9.997000899730082e-05
    * (B, x) = 9.997000899730082e-05
    * (A, z) = 0.7998600419874038
    * (A, y) = 9.997000899730082e-05
    * (A, x) = 0.20003998800359893
    * (E, z) = 9.997000899730082e-05
    * (E, y) = 0.9998000599820054
    * (E, x) = 9.997000899730082e-05
    * (F, z) = 9.997000899730082e-05
    * (F, y) = 9.997000899730082e-05
    * (F, x) = 0.9998000599820054

 1. Hidden path for emitted sequence: SOURCE→D, D→A, A→F, F→B, B→D, D→A, A→E, E→A, A→B, B→D, D→A, A→E, E→A

    New transition probabilities:
    * SOURCE→D = 0.9998000599820054
    * SOURCE→B = 9.997000899730082e-05
    * SOURCE→A = 9.997000899730082e-05
    * A→E = 0.49995001499550135
    * A→B = 0.2500249925022493
    * A→F = 0.2500249925022493
    * B→D = 0.9999000199960009
    * B→C = 9.998000399920017e-05
    * C→F = 1.0
    * D→A = 1.0
    * E→A = 1.0
    * F→E = 9.998000399920017e-05
    * F→B = 0.9999000199960009

    New emission probabilities:
    * (D, z) = 0.9998000599820054
    * (D, y) = 9.997000899730082e-05
    * (D, x) = 9.997000899730082e-05
    * (B, z) = 0.9998000599820054
    * (B, y) = 9.997000899730082e-05
    * (B, x) = 9.997000899730082e-05
    * (A, z) = 0.7998600419874038
    * (A, y) = 9.997000899730082e-05
    * (A, x) = 0.20003998800359893
    * (E, z) = 9.997000899730082e-05
    * (E, y) = 0.9998000599820054
    * (E, x) = 9.997000899730082e-05
    * (F, z) = 9.997000899730082e-05
    * (F, y) = 9.997000899730082e-05
    * (F, x) = 0.9998000599820054


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
"STATE_A" -> "STATE_B" [label="0.2500249925022493"]
"STATE_A" -> "STATE_E" [label="0.49995001499550135"]
"STATE_A" -> "STATE_F" [label="0.2500249925022493"]
"STATE_B" -> "STATE_C" [label="9.998000399920017e-05"]
"STATE_B" -> "STATE_D" [label="0.9999000199960009"]
"STATE_C" -> "STATE_F" [label="1.0"]
"STATE_D" -> "STATE_A" [label="1.0"]
"STATE_E" -> "STATE_A" [label="1.0"]
"STATE_F" -> "STATE_B" [label="0.9999000199960009"]
"STATE_F" -> "STATE_E" [label="9.998000399920017e-05"]
"STATE_SOURCE" -> "STATE_A" [label="9.997000899730082e-05"]
"STATE_SOURCE" -> "STATE_B" [label="9.997000899730082e-05"]
"STATE_SOURCE" -> "STATE_D" [label="0.9998000599820054"]
"SYMBOL_x" [label="x", style="dashed"]
"STATE_A" -> "SYMBOL_x" [label="0.20003998800359893", style="dashed"]
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="9.997000899730082e-05", style="dashed"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="0.7998600419874038", style="dashed"]
"STATE_B" -> "SYMBOL_x" [label="9.997000899730082e-05", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="9.997000899730082e-05", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="0.9998000599820054", style="dashed"]
"STATE_D" -> "SYMBOL_x" [label="9.997000899730082e-05", style="dashed"]
"STATE_D" -> "SYMBOL_y" [label="9.997000899730082e-05", style="dashed"]
"STATE_D" -> "SYMBOL_z" [label="0.9998000599820054", style="dashed"]
"STATE_E" -> "SYMBOL_x" [label="9.997000899730082e-05", style="dashed"]
"STATE_E" -> "SYMBOL_y" [label="0.9998000599820054", style="dashed"]
"STATE_E" -> "SYMBOL_z" [label="9.997000899730082e-05", style="dashed"]
"STATE_F" -> "SYMBOL_x" [label="0.9998000599820054", style="dashed"]
"STATE_F" -> "SYMBOL_y" [label="9.997000899730082e-05", style="dashed"]
"STATE_F" -> "SYMBOL_z" [label="9.997000899730082e-05", style="dashed"]
}
```

</div>

`{bm-enable-all}`

