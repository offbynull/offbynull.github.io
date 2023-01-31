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
"STATE_A" -> "STATE_B" [label="0.862648203135135"]
"STATE_A" -> "STATE_E" [label="0.06554889701846214"]
"STATE_A" -> "STATE_F" [label="0.07180289984640269"]
"STATE_B" -> "STATE_C" [label="0.32598584847317835"]
"STATE_B" -> "STATE_D" [label="0.6740141515268216"]
"STATE_C" -> "STATE_F" [label="1.0"]
"STATE_D" -> "STATE_A" [label="1.0"]
"STATE_E" -> "STATE_A" [label="1.0"]
"STATE_F" -> "STATE_B" [label="0.48552465960106383"]
"STATE_F" -> "STATE_E" [label="0.5144753403989362"]
"STATE_SOURCE" -> "STATE_A" [label="0.16842971686841296"]
"STATE_SOURCE" -> "STATE_B" [label="0.4229659942463867"]
"STATE_SOURCE" -> "STATE_D" [label="0.4086042888852004"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="0.6993466883807012", style="dashed"]
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="0.17513973137948086", style="dashed"]
"SYMBOL_x" [label="x", style="dashed"]
"STATE_A" -> "SYMBOL_x" [label="0.12551358023981785", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="0.32903691524230705", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="0.5900577212423003", style="dashed"]
"STATE_B" -> "SYMBOL_x" [label="0.08090536351539267", style="dashed"]
"STATE_D" -> "SYMBOL_z" [label="0.27734693628596224", style="dashed"]
"STATE_D" -> "SYMBOL_y" [label="0.6843077388545339", style="dashed"]
"STATE_D" -> "SYMBOL_x" [label="0.038345324859503795", style="dashed"]
"STATE_E" -> "SYMBOL_z" [label="0.5536803075386381", style="dashed"]
"STATE_E" -> "SYMBOL_y" [label="0.3960151143267686", style="dashed"]
"STATE_E" -> "SYMBOL_x" [label="0.05030457813459329", style="dashed"]
"STATE_F" -> "SYMBOL_z" [label="0.14003049296685663", style="dashed"]
"STATE_F" -> "SYMBOL_y" [label="0.34720152869558435", style="dashed"]
"STATE_F" -> "SYMBOL_x" [label="0.512767978337559", style="dashed"]
}
```

Applying Viterbi learning for 3 cycles ...

 1. Hidden path for emitted sequence: SOURCE→A, A→B, B→C, C→F, F→E, E→A, A→B, B→D, D→A, A→B, B→D, D→A, A→B, B→C, C→F

    New transition probabilities:
    * SOURCE→D = 9.997000899730082e-05
    * SOURCE→B = 9.997000899730082e-05
    * SOURCE→A = 0.9998000599820054
    * A→E = 9.997000899730082e-05
    * A→B = 0.9998000599820054
    * A→F = 9.997000899730082e-05
    * B→C = 0.333366660001333
    * B→D = 0.6666333399986669
    * C→F = 1.0
    * D→A = 1.0
    * E→A = 1.0
    * F→E = 0.9999000199960009
    * F→B = 9.998000399920017e-05

    New emission probabilities:
    * (D, z) = 0.9998000599820054
    * (D, y) = 9.997000899730082e-05
    * (D, x) = 9.997000899730082e-05
    * (B, z) = 0.49995001499550135
    * (B, y) = 0.2500249925022493
    * (B, x) = 0.2500249925022493
    * (A, z) = 0.7498750374887534
    * (A, y) = 0.2500249925022493
    * (A, x) = 9.997000899730082e-05
    * (E, z) = 0.9998000599820054
    * (E, y) = 9.997000899730082e-05
    * (E, x) = 9.997000899730082e-05
    * (F, z) = 0.9998000599820054
    * (F, y) = 9.997000899730082e-05
    * (F, x) = 9.997000899730082e-05

 1. Hidden path for emitted sequence: SOURCE→D, D→A, A→B, B→C, C→F, F→E, E→A, A→B, B→D, D→A, A→B, B→D, D→A, A→B

    New transition probabilities:
    * SOURCE→D = 0.9998000599820054
    * SOURCE→B = 9.997000899730082e-05
    * SOURCE→A = 9.997000899730082e-05
    * A→E = 9.997000899730082e-05
    * A→B = 0.9998000599820054
    * A→F = 9.997000899730082e-05
    * B→C = 0.333366660001333
    * B→D = 0.6666333399986669
    * C→F = 1.0
    * D→A = 1.0
    * E→A = 1.0
    * F→E = 0.9999000199960009
    * F→B = 9.998000399920017e-05

    New emission probabilities:
    * (D, z) = 0.6665666966576693
    * (D, y) = 0.3333333333333333
    * (D, x) = 9.997000899730082e-05
    * (B, z) = 0.6665666966576693
    * (B, y) = 9.997000899730082e-05
    * (B, x) = 0.3333333333333333
    * (A, z) = 0.49995001499550135
    * (A, y) = 0.2500249925022493
    * (A, x) = 0.2500249925022493
    * (E, z) = 0.9998000599820054
    * (E, y) = 9.997000899730082e-05
    * (E, x) = 9.997000899730082e-05
    * (F, z) = 0.9998000599820054
    * (F, y) = 9.997000899730082e-05
    * (F, x) = 9.997000899730082e-05

 1. Hidden path for emitted sequence: SOURCE→D, D→A, A→B, B→D, D→A, A→B, B→D, D→A, A→B, B→C, C→F, F→E, E→A, A→B

    New transition probabilities:
    * SOURCE→D = 0.9998000599820054
    * SOURCE→B = 9.997000899730082e-05
    * SOURCE→A = 9.997000899730082e-05
    * A→E = 9.997000899730082e-05
    * A→B = 0.9998000599820054
    * A→F = 9.997000899730082e-05
    * B→C = 0.333366660001333
    * B→D = 0.6666333399986669
    * C→F = 1.0
    * D→A = 1.0
    * E→A = 1.0
    * F→E = 0.9999000199960009
    * F→B = 9.998000399920017e-05

    New emission probabilities:
    * (D, z) = 0.6665666966576693
    * (D, y) = 0.3333333333333333
    * (D, x) = 9.997000899730082e-05
    * (B, z) = 0.6665666966576693
    * (B, y) = 9.997000899730082e-05
    * (B, x) = 0.3333333333333333
    * (A, z) = 0.7498750374887534
    * (A, y) = 9.997000899730082e-05
    * (A, x) = 0.2500249925022493
    * (E, z) = 9.997000899730082e-05
    * (E, y) = 0.9998000599820054
    * (E, x) = 9.997000899730082e-05
    * (F, z) = 0.9998000599820054
    * (F, y) = 9.997000899730082e-05
    * (F, x) = 9.997000899730082e-05


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
"STATE_B" -> "STATE_C" [label="0.333366660001333"]
"STATE_B" -> "STATE_D" [label="0.6666333399986669"]
"STATE_C" -> "STATE_F" [label="1.0"]
"STATE_D" -> "STATE_A" [label="1.0"]
"STATE_E" -> "STATE_A" [label="1.0"]
"STATE_F" -> "STATE_B" [label="9.998000399920017e-05"]
"STATE_F" -> "STATE_E" [label="0.9999000199960009"]
"STATE_SOURCE" -> "STATE_A" [label="9.997000899730082e-05"]
"STATE_SOURCE" -> "STATE_B" [label="9.997000899730082e-05"]
"STATE_SOURCE" -> "STATE_D" [label="0.9998000599820054"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="0.7498750374887534", style="dashed"]
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="9.997000899730082e-05", style="dashed"]
"SYMBOL_x" [label="x", style="dashed"]
"STATE_A" -> "SYMBOL_x" [label="0.2500249925022493", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="0.6665666966576693", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="9.997000899730082e-05", style="dashed"]
"STATE_B" -> "SYMBOL_x" [label="0.3333333333333333", style="dashed"]
"STATE_D" -> "SYMBOL_z" [label="0.6665666966576693", style="dashed"]
"STATE_D" -> "SYMBOL_y" [label="0.3333333333333333", style="dashed"]
"STATE_D" -> "SYMBOL_x" [label="9.997000899730082e-05", style="dashed"]
"STATE_E" -> "SYMBOL_z" [label="9.997000899730082e-05", style="dashed"]
"STATE_E" -> "SYMBOL_y" [label="0.9998000599820054", style="dashed"]
"STATE_E" -> "SYMBOL_x" [label="9.997000899730082e-05", style="dashed"]
"STATE_F" -> "SYMBOL_z" [label="0.9998000599820054", style="dashed"]
"STATE_F" -> "SYMBOL_y" [label="9.997000899730082e-05", style="dashed"]
"STATE_F" -> "SYMBOL_x" [label="9.997000899730082e-05", style="dashed"]
}
```

</div>

`{bm-enable-all}`

