<div style="border:1px solid black;">

`{bm-disable-all}`

Given the fragments ['TTA', 'TAT', 'ATT', 'TTC', 'TCT', 'CTT'], the de Bruijn graph is...

```{dot}
digraph {
graph[rankdir=LR, center=true, margin=0.2, nodesep=0.15, ranksep=0.1]
node[shape=rectangle, fontname="Courier-Bold", fontsize=10, fixedsize=true]
edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, fixedsize=true, arrowhead=vee]
"TT [0]" -> "TA [0]" [label="TTA"];
"TT [0]" -> "TC [0]" [label="TTC"];
"TA [0]" -> "AT [0]" [label="TAT"];
"AT [0]" -> "TT [0]" [label="ATT"];
"TC [0]" -> "CT [0]" [label="TCT"];
"CT [0]" -> "TT [0]" [label="CTT"];
}

```


... and a Eulerian cycle is ...

TT -> TC -> CT -> TT -> TA -> AT -> TT
</div>

`{bm-enable-all}`

