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
  - [B, C]
  - [C, B, y]
  - [B, A, y]
  - [A, A, y]
  - [A, A, z]
  - [A, A, z]
pseudocount: 0.0001

```

The following HMM hidden state transitions and symbol emissions were assumed...

 * transitions={'SOURCE': {'A', 'C', 'B', 'SOURCE'}, 'A': {'A', 'C', 'B', 'SOURCE'}, 'C': {'A', 'C', 'B', 'SOURCE'}, 'B': {'A', 'C', 'B', 'SOURCE'}}
 * emissions={'A': {'z', 'y'}, 'B': {'z', 'y'}, 'C': {}, 'SOURCE': {}}

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
"STATE_A" -> "STATE_C" [label="nan"]
"STATE_A" -> "STATE_SOURCE" [label="nan"]
"STATE_B" -> "STATE_A" [label="nan"]
"STATE_B" -> "STATE_B" [label="nan"]
"STATE_B" -> "STATE_C" [label="nan"]
"STATE_B" -> "STATE_SOURCE" [label="nan"]
"STATE_C" -> "STATE_A" [label="nan"]
"STATE_C" -> "STATE_B" [label="nan"]
"STATE_C" -> "STATE_C" [label="nan"]
"STATE_C" -> "STATE_SOURCE" [label="nan"]
"STATE_SOURCE" -> "STATE_A" [label="nan"]
"STATE_SOURCE" -> "STATE_B" [label="nan"]
"STATE_SOURCE" -> "STATE_C" [label="nan"]
"STATE_SOURCE" -> "STATE_SOURCE" [label="nan"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="nan", style="dashed"]
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="nan", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="nan", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="nan", style="dashed"]
}
```

The following probabilities were derived from the observed sequence of transitions and emissions ...

 * transition_probs={('SOURCE', 'A'): 1.0, ('SOURCE', 'C'): 0.0, ('SOURCE', 'B'): 0.0, ('SOURCE', 'SOURCE'): 0.0, ('A', 'A'): 0.6666666666666666, ('A', 'C'): 0.0, ('A', 'B'): 0.3333333333333333, ('A', 'SOURCE'): 0.0, ('C', 'A'): 0.0, ('C', 'C'): 0.0, ('C', 'B'): 1.0, ('C', 'SOURCE'): 0.0, ('B', 'A'): 0.6666666666666666, ('B', 'C'): 0.3333333333333333, ('B', 'B'): 0.0, ('B', 'SOURCE'): 0.0}
 * emission_probs={('A', 'z'): 0.5714285714285714, ('A', 'y'): 0.42857142857142855, ('B', 'z'): 0.6666666666666666, ('B', 'y'): 0.3333333333333333}

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
"STATE_A" -> "STATE_C" [label="0.0"]
"STATE_A" -> "STATE_SOURCE" [label="0.0"]
"STATE_B" -> "STATE_A" [label="0.6666666666666666"]
"STATE_B" -> "STATE_B" [label="0.0"]
"STATE_B" -> "STATE_C" [label="0.3333333333333333"]
"STATE_B" -> "STATE_SOURCE" [label="0.0"]
"STATE_C" -> "STATE_A" [label="0.0"]
"STATE_C" -> "STATE_B" [label="1.0"]
"STATE_C" -> "STATE_C" [label="0.0"]
"STATE_C" -> "STATE_SOURCE" [label="0.0"]
"STATE_SOURCE" -> "STATE_A" [label="1.0"]
"STATE_SOURCE" -> "STATE_B" [label="0.0"]
"STATE_SOURCE" -> "STATE_C" [label="0.0"]
"STATE_SOURCE" -> "STATE_SOURCE" [label="0.0"]
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
"STATE_A" -> "STATE_A" [label="0.6665000666400106"]
"STATE_A" -> "STATE_B" [label="0.33330001332800213"]
"STATE_A" -> "STATE_C" [label="9.996001599360257e-05"]
"STATE_A" -> "STATE_SOURCE" [label="9.996001599360257e-05"]
"STATE_B" -> "STATE_A" [label="0.6665000666400106"]
"STATE_B" -> "STATE_B" [label="9.996001599360257e-05"]
"STATE_B" -> "STATE_C" [label="0.33330001332800213"]
"STATE_B" -> "STATE_SOURCE" [label="9.996001599360257e-05"]
"STATE_C" -> "STATE_A" [label="9.996001599360257e-05"]
"STATE_C" -> "STATE_B" [label="0.9997001199520192"]
"STATE_C" -> "STATE_C" [label="9.996001599360257e-05"]
"STATE_C" -> "STATE_SOURCE" [label="9.996001599360257e-05"]
"STATE_SOURCE" -> "STATE_A" [label="0.9997001199520192"]
"STATE_SOURCE" -> "STATE_B" [label="9.996001599360257e-05"]
"STATE_SOURCE" -> "STATE_C" [label="9.996001599360257e-05"]
"STATE_SOURCE" -> "STATE_SOURCE" [label="9.996001599360257e-05"]
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

