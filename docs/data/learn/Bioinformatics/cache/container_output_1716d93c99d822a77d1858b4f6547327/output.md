<div style="border:1px solid black;">

`{bm-disable-all}`

Deriving HMM probabilities into assumed HMM structure using the following settings...

```
observed:
  - [SOURCE, A, z]
  - [A, A, y]
  - [A, B, z]
  - [B, A, z]
  - [A, B, z]
  - [B, A, y]
  - [A, A, y]
  - [A, A, z]
  - [A, A, z]
  - [A, B, z]
  - [B, B, z]
  - [B, B, z]
cycles: 8
pseudocount: 0.0001

```

The following HMM hidden state transitions and symbol emissions were assumed...

 * transitions={'SOURCE': {'A', 'B'}, 'A': {'A', 'B'}, 'B': {'A', 'B'}}
 * emissions={'SOURCE': {}, 'A': {'y', 'z'}, 'B': {'y', 'z'}}

The following HMM was produced (no probabilities) ...

```{dot}
digraph G {
 graph[rankdir=LR]
 node[shape=egg, fontname="Courier-Bold", fontsize=10]
 edge[fontname="Courier-Bold", fontsize=10]
"STATE_A" [label="A"]
"STATE_B" [label="B"]
"STATE_SOURCE" [label="SOURCE"]
"STATE_A" -> "STATE_A" [label="nan"]
"STATE_A" -> "STATE_B" [label="nan"]
"STATE_B" -> "STATE_A" [label="nan"]
"STATE_B" -> "STATE_B" [label="nan"]
"STATE_SOURCE" -> "STATE_A" [label="nan"]
"STATE_SOURCE" -> "STATE_B" [label="nan"]
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="nan", style="dashed"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="nan", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="nan", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="nan", style="dashed"]
}
```

The following probabilities were derived from the observed sequence of transitions and emissions ...

 * transition_probs={('SOURCE', 'A'): 1.0, ('SOURCE', 'B'): 0.0, ('A', 'A'): 0.5714285714285714, ('A', 'B'): 0.42857142857142855, ('B', 'A'): 0.5, ('B', 'B'): 0.5}
 * emission_probs={('A', 'y'): 0.42857142857142855, ('A', 'z'): 0.5714285714285714, ('B', 'y'): 0.0, ('B', 'z'): 1.0}

The following HMM was produced after derived probabilities were applied ...

```{dot}
digraph G {
 graph[rankdir=LR]
 node[shape=egg, fontname="Courier-Bold", fontsize=10]
 edge[fontname="Courier-Bold", fontsize=10]
"STATE_A" [label="A"]
"STATE_B" [label="B"]
"STATE_SOURCE" [label="SOURCE"]
"STATE_A" -> "STATE_A" [label="0.5714285714285714"]
"STATE_A" -> "STATE_B" [label="0.42857142857142855"]
"STATE_B" -> "STATE_A" [label="0.5"]
"STATE_B" -> "STATE_B" [label="0.5"]
"STATE_SOURCE" -> "STATE_A" [label="1.0"]
"STATE_SOURCE" -> "STATE_B" [label="0.0"]
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="0.42857142857142855", style="dashed"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="0.5714285714285714", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="0.0", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="1.0", style="dashed"]
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
"STATE_SOURCE" [label="SOURCE"]
"STATE_A" -> "STATE_A" [label="0.5714142885708572"]
"STATE_A" -> "STATE_B" [label="0.4285857114291427"]
"STATE_B" -> "STATE_A" [label="0.5"]
"STATE_B" -> "STATE_B" [label="0.5"]
"STATE_SOURCE" -> "STATE_A" [label="0.9999000199960009"]
"STATE_SOURCE" -> "STATE_B" [label="9.998000399920017e-05"]
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="0.4285857114291427", style="dashed"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="0.5714142885708572", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="9.998000399920017e-05", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="0.9999000199960009", style="dashed"]
}
```

</div>

`{bm-enable-all}`

