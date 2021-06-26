<div style="border:1px solid black;">

`{bm-disable-all}`

Given the fragments ['TTA', 'TTA', 'TAG', 'AGT', 'GTT', 'TAC', 'ACT', 'CTT'], the overlap graph is...

```{dot}
digraph {
graph[rankdir=LR, center=true, margin=0.2, nodesep=0.15, ranksep=0.1]
node[shape=rectangle, fontname="Courier-Bold", fontsize=10, fixedsize=true]
edge[arrowsize=0.6, arrowhead=vee]
"TTA [0]" -> "TAG [0]" [shape=plain];
"TTA [0]" -> "TAC [0]" [shape=plain];
"TAG [0]" -> "AGT [0]" [shape=plain];
"TAC [0]" -> "ACT [0]" [shape=plain];
"TTA [1]" -> "TAG [0]" [shape=plain];
"TTA [1]" -> "TAC [0]" [shape=plain];
"AGT [0]" -> "GTT [0]" [shape=plain];
"GTT [0]" -> "TTA [0]" [shape=plain];
"GTT [0]" -> "TTA [1]" [shape=plain];
"CTT [0]" -> "TTA [0]" [shape=plain];
"CTT [0]" -> "TTA [1]" [shape=plain];
"ACT [0]" -> "CTT [0]" [shape=plain];
}

```

... and the Hamiltonian paths are ...

 * TAC -> ACT -> CTT -> TTA -> TAG -> AGT -> GTT -> TTA
 * GTT -> TTA -> TAC -> ACT -> CTT -> TTA -> TAG -> AGT
 * TTA -> TAG -> AGT -> GTT -> TTA -> TAC -> ACT -> CTT
 * TTA -> TAC -> ACT -> CTT -> TTA -> TAG -> AGT -> GTT
 * GTT -> TTA -> TAC -> ACT -> CTT -> TTA -> TAG -> AGT
 * CTT -> TTA -> TAG -> AGT -> GTT -> TTA -> TAC -> ACT
 * TTA -> TAC -> ACT -> CTT -> TTA -> TAG -> AGT -> GTT
 * TTA -> TAG -> AGT -> GTT -> TTA -> TAC -> ACT -> CTT
 * CTT -> TTA -> TAG -> AGT -> GTT -> TTA -> TAC -> ACT
 * AGT -> GTT -> TTA -> TAC -> ACT -> CTT -> TTA -> TAG
 * AGT -> GTT -> TTA -> TAC -> ACT -> CTT -> TTA -> TAG
 * TAC -> ACT -> CTT -> TTA -> TAG -> AGT -> GTT -> TTA
 * TAG -> AGT -> GTT -> TTA -> TAC -> ACT -> CTT -> TTA
 * ACT -> CTT -> TTA -> TAG -> AGT -> GTT -> TTA -> TAC
 * ACT -> CTT -> TTA -> TAG -> AGT -> GTT -> TTA -> TAC
 * TAG -> AGT -> GTT -> TTA -> TAC -> ACT -> CTT -> TTA
</div>

`{bm-enable-all}`

