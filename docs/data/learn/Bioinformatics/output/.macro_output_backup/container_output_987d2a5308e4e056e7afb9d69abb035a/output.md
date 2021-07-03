<div style="border:1px solid black;">

`{bm-disable-all}`

Given the fragments ['TTAC', 'TACC', 'ACCC', 'CCCT'], the artificially balanced de Bruijn graph is...

```{dot}
digraph {
graph[rankdir=LR, center=true, margin=0.2, nodesep=0.15, ranksep=0.1]
node[shape=rectangle, fontname="Courier-Bold", fontsize=10, fixedsize=true]
edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, fixedsize=true, arrowhead=vee]
"TTA [0]" -> "TAC [0]" [label="TTAC"];
"TAC [0]" -> "ACC [0]" [label="TACC"];
"ACC [0]" -> "CCC [0]" [label="ACCC"];
"CCC [0]" -> "CCT [0]" [label="CCCT"];
"CCT [0]" -> "TTA [0]" [label="C?TA"];
}

```


... with original head nodes at {TTA} and tail nodes at {CCT}.
</div>

`{bm-enable-all}`

