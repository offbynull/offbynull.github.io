<div style="border:1px solid black;">

`{bm-disable-all}`

Given the fragments ['TGG', 'GGT', 'GGT', 'GTG', 'CAC', 'ACC', 'CCA'], the de Bruijn graph is...

```{dot}
digraph {
graph[rankdir=LR, center=true, margin=0.2, nodesep=0.15, ranksep=0.1]
node[shape=rectangle, fontname="Courier-Bold", fontsize=10, fixedsize=true]
edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, fixedsize=true, arrowhead=vee]
"TG [0]" -> "GG [0]" [label="TGG"];
"GG [0]" -> "GT [0]" [label="GGT"];
"GG [0]" -> "GT [0]" [label="GGT"];
"GT [0]" -> "TG [0]" [label="GTG"];
"CA [0]" -> "AC [0]" [label="CAC"];
"AC [0]" -> "CC [0]" [label="ACC"];
"CC [0]" -> "CA [0]" [label="CCA"];
}

```


The following contigs were found...

GG->GT

GG->GT

GT->TG->GG

CA->AC->CC->CA

</div>

`{bm-enable-all}`

