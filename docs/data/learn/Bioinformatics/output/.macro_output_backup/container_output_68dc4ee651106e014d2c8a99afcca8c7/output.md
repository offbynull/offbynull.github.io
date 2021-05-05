<div style="border:1px solid black;">

`{bm-disable-all}`

Given the fragments ['TTAG', 'TAGT', 'AGTT', 'GTTA', 'TTAC', 'TACT', 'ACTT', 'CTTA'], the de Bruijn graph is...

```{dot}
digraph {
graph[rankdir=LR, center=true, margin=0.2, nodesep=0.15, ranksep=0.1]
node[shape=rectangle, fontname="Courier-Bold", fontsize=10, fixedsize=true]
edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, fixedsize=true, arrowhead=vee]
"TTA [0]" -> "TAG [0]" [label="TTAG"];
"TTA [0]" -> "TAC [0]" [label="TTAC"];
"TAG [0]" -> "AGT [0]" [label="TAGT"];
"AGT [0]" -> "GTT [0]" [label="AGTT"];
"GTT [0]" -> "TTA [0]" [label="GTTA"];
"TAC [0]" -> "ACT [0]" [label="TACT"];
"ACT [0]" -> "CTT [0]" [label="ACTT"];
"CTT [0]" -> "TTA [0]" [label="CTTA"];
}

```


</div>

`{bm-enable-all}`

