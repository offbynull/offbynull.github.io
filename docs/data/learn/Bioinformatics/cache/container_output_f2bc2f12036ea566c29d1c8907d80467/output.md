<div style="border:1px solid black;">

`{bm-disable-all}`

Deriving HMM probabilities using the following settings...

```
transitions:
  SOURCE: [A, B]
  A: [A, B]
  B: [A, C]
  C: [B]
emissions:
  SOURCE: []
  A: [y, z]
  B: [y, z]
  C: []
observed:
  - [SOURCE, A, z]
  - [A, A, y]
  - [A, B, z]
  - [B, A, z]
  - [A, B, z]
  - [B, C]
  - [C, B, y]
  - [B, A, y]
  - [A, A, y]
  - [A, A, z]
  - [A, A, z]
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
"STATE_SOURCE" [label="SOURCE"]
"STATE_A" -> "STATE_A" [label="nan"]
"STATE_A" -> "STATE_B" [label="nan"]
"STATE_B" -> "STATE_A" [label="nan"]
"STATE_B" -> "STATE_C" [label="nan"]
"STATE_C" -> "STATE_B" [label="nan"]
"STATE_SOURCE" -> "STATE_A" [label="nan"]
"STATE_SOURCE" -> "STATE_B" [label="nan"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="nan", style="dashed"]
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="nan", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="nan", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="nan", style="dashed"]
}
```

The following probabilities were derived from the observed sequence of transitions and emissions ...

 * Transition probabilities:
   * SOURCE→B = 0.0
   * SOURCE→A = 1.0
   * A→B = 0.3333333333333333
   * A→A = 0.6666666666666666
   * B→A = 0.6666666666666666
   * B→C = 0.3333333333333333
   * C→B = 1.0

 * Emission probabilities:
   * (B, z) = 0.6666666666666666
   * (B, y) = 0.3333333333333333
   * (A, z) = 0.5714285714285714
   * (A, y) = 0.42857142857142855

The following HMM was produced after derived probabilities were applied ...

```{dot}
digraph G {
 graph[rankdir=LR]
 node[shape=egg, fontname="Courier-Bold", fontsize=10]
 edge[fontname="Courier-Bold", fontsize=10]
"STATE_A" [label="A"]
"STATE_B" [label="B"]
"STATE_C" [label="C"]
"STATE_SOURCE" [label="SOURCE"]
"STATE_A" -> "STATE_A" [label="0.6666666666666666"]
"STATE_A" -> "STATE_B" [label="0.3333333333333333"]
"STATE_B" -> "STATE_A" [label="0.6666666666666666"]
"STATE_B" -> "STATE_C" [label="0.3333333333333333"]
"STATE_C" -> "STATE_B" [label="1.0"]
"STATE_SOURCE" -> "STATE_A" [label="1.0"]
"STATE_SOURCE" -> "STATE_B" [label="0.0"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="0.5714285714285714", style="dashed"]
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="0.42857142857142855", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="0.6666666666666666", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="0.3333333333333333", style="dashed"]
}
```

After pseudocounts are applied, the HMM becomes as follows ...

```{dot}
digraph G {
 graph[rankdir=LR]
 node[shape=egg, fontname="Courier-Bold", fontsize=10]
 edge[fontname="Courier-Bold", fontsize=10]
"STATE_A" [label="A"]
"STATE_B" [label="B"]
"STATE_C" [label="C"]
"STATE_SOURCE" [label="SOURCE"]
"STATE_A" -> "STATE_A" [label="0.6666333399986669"]
"STATE_A" -> "STATE_B" [label="0.333366660001333"]
"STATE_B" -> "STATE_A" [label="0.6666333399986669"]
"STATE_B" -> "STATE_C" [label="0.333366660001333"]
"STATE_C" -> "STATE_B" [label="1.0"]
"STATE_SOURCE" -> "STATE_A" [label="0.9999000199960009"]
"STATE_SOURCE" -> "STATE_B" [label="9.998000399920017e-05"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="0.5714142885708572", style="dashed"]
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="0.4285857114291427", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="0.6666333399986669", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="0.333366660001333", style="dashed"]
}
```

</div>

`{bm-enable-all}`

