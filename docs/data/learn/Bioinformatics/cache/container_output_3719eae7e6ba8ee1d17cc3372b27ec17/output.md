<div style="border:1px solid black;">

`{bm-disable-all}`

Given the tree...

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[fontname="Courier-Bold", fontsize=10]
i0
i1
i2
v0
v1
v2
v3
v4
v5
v0 -- i0 [label=" "]
v1 -- i0 [label=" "]
v2 -- i0 [label=" "]
i0 -- i1 [label=" "]
i1 -- i2 [label=" "]
i2 -- v3 [label=" "]
i2 -- v4 [label=" "]
i1 -- v5 [label=" "]
}
```

neighbour_detect reported that v3 and v4 have the highest total edge count of 26 and as such are guaranteed to be neighbours.

For each leaf pair in the tree, `combine_count_and_normalize()` totals are ... 

<table>
<thead><tr>
<th></th>
<th>v0</th>
<th>v1</th>
<th>v2</th>
<th>v3</th>
<th>v4</th>
<th>v5</th>
</tr></thead>
<tbody>
<tr>
<td>v0</td>
<td>0</td>
<td>22</td>
<td>22</td>
<td>16</td>
<td>16</td>
<td>18</td>
</tr>
<tr>
<td>v1</td>
<td>22</td>
<td>0</td>
<td>22</td>
<td>16</td>
<td>16</td>
<td>18</td>
</tr>
<tr>
<td>v2</td>
<td>22</td>
<td>22</td>
<td>0</td>
<td>16</td>
<td>16</td>
<td>18</td>
</tr>
<tr>
<td>v3</td>
<td>16</td>
<td>16</td>
<td>16</td>
<td>0</td>
<td>26</td>
<td>20</td>
</tr>
<tr>
<td>v4</td>
<td>16</td>
<td>16</td>
<td>16</td>
<td>26</td>
<td>0</td>
<td>20</td>
</tr>
<tr>
<td>v5</td>
<td>18</td>
<td>18</td>
<td>18</td>
<td>20</td>
<td>20</td>
<td>0</td>
</tr>
</tbody>
</table>

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape = circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[fontname="Courier-Bold", fontsize=10]
 ranksep=0.25
 fontname="Courier-Bold"
 fontsize=10
  subgraph cluster_v0v1 {
  label="combine_count_and_normalize(v0,v1)"
  v0v1_v2 [label="v2"]
  v0v1_v5 [label="v5"]
  v0v1_v0 [label="v0", style=filled, fillcolor=gray]
  v0v1_v3 [label="v3"]
  v0v1_v4 [label="v4"]
  v0v1_v1 [label="v1", style=filled, fillcolor=gray]
  v0v1_i2 [label="i2"]
  v0v1_i1 [label="i1"]
  v0v1_i0 [label="i0"]
 v0v1_v0 -- v0v1_i0 [label=" ", penwidth="2.5", color="black:invis:black"]
 v0v1_v1 -- v0v1_i0 [label=" ", penwidth="2.5", color="black:invis:black"]
 v0v1_v2 -- v0v1_i0 [label=" ", penwidth="2.5", color="black:invis:black"]
 v0v1_i0 -- v0v1_i1 [label=" ", penwidth="2.5", color="black:invis:black:invis:black:invis:black:invis:black:invis:black"]
 v0v1_i1 -- v0v1_i2 [label=" ", penwidth="2.5", color="black:invis:black:invis:black:invis:black"]
 v0v1_i2 -- v0v1_v3 [label=" ", penwidth="2.5", color="black:invis:black"]
 v0v1_i2 -- v0v1_v4 [label=" ", penwidth="2.5", color="black:invis:black"]
 v0v1_i1 -- v0v1_v5 [label=" ", penwidth="2.5", color="black:invis:black"]
}
  subgraph cluster_v0v2 {
  label="combine_count_and_normalize(v0,v2)"
  v0v2_v2 [label="v2", style=filled, fillcolor=gray]
  v0v2_v5 [label="v5"]
  v0v2_v0 [label="v0", style=filled, fillcolor=gray]
  v0v2_v3 [label="v3"]
  v0v2_v4 [label="v4"]
  v0v2_v1 [label="v1"]
  v0v2_i2 [label="i2"]
  v0v2_i1 [label="i1"]
  v0v2_i0 [label="i0"]
 v0v2_v0 -- v0v2_i0 [label=" ", penwidth="2.5", color="black:invis:black"]
 v0v2_v1 -- v0v2_i0 [label=" ", penwidth="2.5", color="black:invis:black"]
 v0v2_v2 -- v0v2_i0 [label=" ", penwidth="2.5", color="black:invis:black"]
 v0v2_i0 -- v0v2_i1 [label=" ", penwidth="2.5", color="black:invis:black:invis:black:invis:black:invis:black:invis:black"]
 v0v2_i1 -- v0v2_i2 [label=" ", penwidth="2.5", color="black:invis:black:invis:black:invis:black"]
 v0v2_i2 -- v0v2_v3 [label=" ", penwidth="2.5", color="black:invis:black"]
 v0v2_i2 -- v0v2_v4 [label=" ", penwidth="2.5", color="black:invis:black"]
 v0v2_i1 -- v0v2_v5 [label=" ", penwidth="2.5", color="black:invis:black"]
}
  subgraph cluster_v0v3 {
  label="combine_count_and_normalize(v0,v3)"
  v0v3_v2 [label="v2"]
  v0v3_v5 [label="v5"]
  v0v3_v0 [label="v0", style=filled, fillcolor=gray]
  v0v3_v3 [label="v3", style=filled, fillcolor=gray]
  v0v3_v4 [label="v4"]
  v0v3_v1 [label="v1"]
  v0v3_i2 [label="i2"]
  v0v3_i1 [label="i1"]
  v0v3_i0 [label="i0"]
 v0v3_v0 -- v0v3_i0 [label=" ", penwidth="2.5", color="black:invis:black"]
 v0v3_v1 -- v0v3_i0 [label=" ", penwidth="2.5", color="black:invis:black"]
 v0v3_v2 -- v0v3_i0 [label=" ", penwidth="2.5", color="black:invis:black"]
 v0v3_i0 -- v0v3_i1 [label=" ", penwidth="2.5", color="black:invis:black"]
 v0v3_i1 -- v0v3_i2 [label=" ", penwidth="2.5", color="black:invis:black"]
 v0v3_i2 -- v0v3_v3 [label=" ", penwidth="2.5", color="black:invis:black"]
 v0v3_i2 -- v0v3_v4 [label=" ", penwidth="2.5", color="black:invis:black"]
 v0v3_i1 -- v0v3_v5 [label=" ", penwidth="2.5", color="black:invis:black"]
}
  subgraph cluster_v0v4 {
  label="combine_count_and_normalize(v0,v4)"
  v0v4_v2 [label="v2"]
  v0v4_v5 [label="v5"]
  v0v4_v0 [label="v0", style=filled, fillcolor=gray]
  v0v4_v3 [label="v3"]
  v0v4_v4 [label="v4", style=filled, fillcolor=gray]
  v0v4_v1 [label="v1"]
  v0v4_i2 [label="i2"]
  v0v4_i1 [label="i1"]
  v0v4_i0 [label="i0"]
 v0v4_v0 -- v0v4_i0 [label=" ", penwidth="2.5", color="black:invis:black"]
 v0v4_v1 -- v0v4_i0 [label=" ", penwidth="2.5", color="black:invis:black"]
 v0v4_v2 -- v0v4_i0 [label=" ", penwidth="2.5", color="black:invis:black"]
 v0v4_i0 -- v0v4_i1 [label=" ", penwidth="2.5", color="black:invis:black"]
 v0v4_i1 -- v0v4_i2 [label=" ", penwidth="2.5", color="black:invis:black"]
 v0v4_i2 -- v0v4_v3 [label=" ", penwidth="2.5", color="black:invis:black"]
 v0v4_i2 -- v0v4_v4 [label=" ", penwidth="2.5", color="black:invis:black"]
 v0v4_i1 -- v0v4_v5 [label=" ", penwidth="2.5", color="black:invis:black"]
}
  subgraph cluster_v0v5 {
  label="combine_count_and_normalize(v0,v5)"
  v0v5_v2 [label="v2"]
  v0v5_v5 [label="v5", style=filled, fillcolor=gray]
  v0v5_v0 [label="v0", style=filled, fillcolor=gray]
  v0v5_v3 [label="v3"]
  v0v5_v4 [label="v4"]
  v0v5_v1 [label="v1"]
  v0v5_i2 [label="i2"]
  v0v5_i1 [label="i1"]
  v0v5_i0 [label="i0"]
 v0v5_v0 -- v0v5_i0 [label=" ", penwidth="2.5", color="black:invis:black"]
 v0v5_v1 -- v0v5_i0 [label=" ", penwidth="2.5", color="black:invis:black"]
 v0v5_v2 -- v0v5_i0 [label=" ", penwidth="2.5", color="black:invis:black"]
 v0v5_i0 -- v0v5_i1 [label=" ", penwidth="2.5", color="black:invis:black"]
 v0v5_i1 -- v0v5_i2 [label=" ", penwidth="2.5", color="black:invis:black:invis:black:invis:black"]
 v0v5_i2 -- v0v5_v3 [label=" ", penwidth="2.5", color="black:invis:black"]
 v0v5_i2 -- v0v5_v4 [label=" ", penwidth="2.5", color="black:invis:black"]
 v0v5_i1 -- v0v5_v5 [label=" ", penwidth="2.5", color="black:invis:black"]
}
  subgraph cluster_v1v2 {
  label="combine_count_and_normalize(v1,v2)"
  v1v2_v2 [label="v2", style=filled, fillcolor=gray]
  v1v2_v5 [label="v5"]
  v1v2_v0 [label="v0"]
  v1v2_v3 [label="v3"]
  v1v2_v4 [label="v4"]
  v1v2_v1 [label="v1", style=filled, fillcolor=gray]
  v1v2_i2 [label="i2"]
  v1v2_i1 [label="i1"]
  v1v2_i0 [label="i0"]
 v1v2_v0 -- v1v2_i0 [label=" ", penwidth="2.5", color="black:invis:black"]
 v1v2_v1 -- v1v2_i0 [label=" ", penwidth="2.5", color="black:invis:black"]
 v1v2_v2 -- v1v2_i0 [label=" ", penwidth="2.5", color="black:invis:black"]
 v1v2_i0 -- v1v2_i1 [label=" ", penwidth="2.5", color="black:invis:black:invis:black:invis:black:invis:black:invis:black"]
 v1v2_i1 -- v1v2_i2 [label=" ", penwidth="2.5", color="black:invis:black:invis:black:invis:black"]
 v1v2_i2 -- v1v2_v3 [label=" ", penwidth="2.5", color="black:invis:black"]
 v1v2_i2 -- v1v2_v4 [label=" ", penwidth="2.5", color="black:invis:black"]
 v1v2_i1 -- v1v2_v5 [label=" ", penwidth="2.5", color="black:invis:black"]
}
  subgraph cluster_v1v3 {
  label="combine_count_and_normalize(v1,v3)"
  v1v3_v2 [label="v2"]
  v1v3_v5 [label="v5"]
  v1v3_v0 [label="v0"]
  v1v3_v3 [label="v3", style=filled, fillcolor=gray]
  v1v3_v4 [label="v4"]
  v1v3_v1 [label="v1", style=filled, fillcolor=gray]
  v1v3_i2 [label="i2"]
  v1v3_i1 [label="i1"]
  v1v3_i0 [label="i0"]
 v1v3_v0 -- v1v3_i0 [label=" ", penwidth="2.5", color="black:invis:black"]
 v1v3_v1 -- v1v3_i0 [label=" ", penwidth="2.5", color="black:invis:black"]
 v1v3_v2 -- v1v3_i0 [label=" ", penwidth="2.5", color="black:invis:black"]
 v1v3_i0 -- v1v3_i1 [label=" ", penwidth="2.5", color="black:invis:black"]
 v1v3_i1 -- v1v3_i2 [label=" ", penwidth="2.5", color="black:invis:black"]
 v1v3_i2 -- v1v3_v3 [label=" ", penwidth="2.5", color="black:invis:black"]
 v1v3_i2 -- v1v3_v4 [label=" ", penwidth="2.5", color="black:invis:black"]
 v1v3_i1 -- v1v3_v5 [label=" ", penwidth="2.5", color="black:invis:black"]
}
  subgraph cluster_v1v4 {
  label="combine_count_and_normalize(v1,v4)"
  v1v4_v2 [label="v2"]
  v1v4_v5 [label="v5"]
  v1v4_v0 [label="v0"]
  v1v4_v3 [label="v3"]
  v1v4_v4 [label="v4", style=filled, fillcolor=gray]
  v1v4_v1 [label="v1", style=filled, fillcolor=gray]
  v1v4_i2 [label="i2"]
  v1v4_i1 [label="i1"]
  v1v4_i0 [label="i0"]
 v1v4_v0 -- v1v4_i0 [label=" ", penwidth="2.5", color="black:invis:black"]
 v1v4_v1 -- v1v4_i0 [label=" ", penwidth="2.5", color="black:invis:black"]
 v1v4_v2 -- v1v4_i0 [label=" ", penwidth="2.5", color="black:invis:black"]
 v1v4_i0 -- v1v4_i1 [label=" ", penwidth="2.5", color="black:invis:black"]
 v1v4_i1 -- v1v4_i2 [label=" ", penwidth="2.5", color="black:invis:black"]
 v1v4_i2 -- v1v4_v3 [label=" ", penwidth="2.5", color="black:invis:black"]
 v1v4_i2 -- v1v4_v4 [label=" ", penwidth="2.5", color="black:invis:black"]
 v1v4_i1 -- v1v4_v5 [label=" ", penwidth="2.5", color="black:invis:black"]
}
  subgraph cluster_v1v5 {
  label="combine_count_and_normalize(v1,v5)"
  v1v5_v2 [label="v2"]
  v1v5_v5 [label="v5", style=filled, fillcolor=gray]
  v1v5_v0 [label="v0"]
  v1v5_v3 [label="v3"]
  v1v5_v4 [label="v4"]
  v1v5_v1 [label="v1", style=filled, fillcolor=gray]
  v1v5_i2 [label="i2"]
  v1v5_i1 [label="i1"]
  v1v5_i0 [label="i0"]
 v1v5_v0 -- v1v5_i0 [label=" ", penwidth="2.5", color="black:invis:black"]
 v1v5_v1 -- v1v5_i0 [label=" ", penwidth="2.5", color="black:invis:black"]
 v1v5_v2 -- v1v5_i0 [label=" ", penwidth="2.5", color="black:invis:black"]
 v1v5_i0 -- v1v5_i1 [label=" ", penwidth="2.5", color="black:invis:black"]
 v1v5_i1 -- v1v5_i2 [label=" ", penwidth="2.5", color="black:invis:black:invis:black:invis:black"]
 v1v5_i2 -- v1v5_v3 [label=" ", penwidth="2.5", color="black:invis:black"]
 v1v5_i2 -- v1v5_v4 [label=" ", penwidth="2.5", color="black:invis:black"]
 v1v5_i1 -- v1v5_v5 [label=" ", penwidth="2.5", color="black:invis:black"]
}
  subgraph cluster_v2v3 {
  label="combine_count_and_normalize(v2,v3)"
  v2v3_v2 [label="v2", style=filled, fillcolor=gray]
  v2v3_v5 [label="v5"]
  v2v3_v0 [label="v0"]
  v2v3_v3 [label="v3", style=filled, fillcolor=gray]
  v2v3_v4 [label="v4"]
  v2v3_v1 [label="v1"]
  v2v3_i2 [label="i2"]
  v2v3_i1 [label="i1"]
  v2v3_i0 [label="i0"]
 v2v3_v0 -- v2v3_i0 [label=" ", penwidth="2.5", color="black:invis:black"]
 v2v3_v1 -- v2v3_i0 [label=" ", penwidth="2.5", color="black:invis:black"]
 v2v3_v2 -- v2v3_i0 [label=" ", penwidth="2.5", color="black:invis:black"]
 v2v3_i0 -- v2v3_i1 [label=" ", penwidth="2.5", color="black:invis:black"]
 v2v3_i1 -- v2v3_i2 [label=" ", penwidth="2.5", color="black:invis:black"]
 v2v3_i2 -- v2v3_v3 [label=" ", penwidth="2.5", color="black:invis:black"]
 v2v3_i2 -- v2v3_v4 [label=" ", penwidth="2.5", color="black:invis:black"]
 v2v3_i1 -- v2v3_v5 [label=" ", penwidth="2.5", color="black:invis:black"]
}
  subgraph cluster_v2v4 {
  label="combine_count_and_normalize(v2,v4)"
  v2v4_v2 [label="v2", style=filled, fillcolor=gray]
  v2v4_v5 [label="v5"]
  v2v4_v0 [label="v0"]
  v2v4_v3 [label="v3"]
  v2v4_v4 [label="v4", style=filled, fillcolor=gray]
  v2v4_v1 [label="v1"]
  v2v4_i2 [label="i2"]
  v2v4_i1 [label="i1"]
  v2v4_i0 [label="i0"]
 v2v4_v0 -- v2v4_i0 [label=" ", penwidth="2.5", color="black:invis:black"]
 v2v4_v1 -- v2v4_i0 [label=" ", penwidth="2.5", color="black:invis:black"]
 v2v4_v2 -- v2v4_i0 [label=" ", penwidth="2.5", color="black:invis:black"]
 v2v4_i0 -- v2v4_i1 [label=" ", penwidth="2.5", color="black:invis:black"]
 v2v4_i1 -- v2v4_i2 [label=" ", penwidth="2.5", color="black:invis:black"]
 v2v4_i2 -- v2v4_v3 [label=" ", penwidth="2.5", color="black:invis:black"]
 v2v4_i2 -- v2v4_v4 [label=" ", penwidth="2.5", color="black:invis:black"]
 v2v4_i1 -- v2v4_v5 [label=" ", penwidth="2.5", color="black:invis:black"]
}
  subgraph cluster_v2v5 {
  label="combine_count_and_normalize(v2,v5)"
  v2v5_v2 [label="v2", style=filled, fillcolor=gray]
  v2v5_v5 [label="v5", style=filled, fillcolor=gray]
  v2v5_v0 [label="v0"]
  v2v5_v3 [label="v3"]
  v2v5_v4 [label="v4"]
  v2v5_v1 [label="v1"]
  v2v5_i2 [label="i2"]
  v2v5_i1 [label="i1"]
  v2v5_i0 [label="i0"]
 v2v5_v0 -- v2v5_i0 [label=" ", penwidth="2.5", color="black:invis:black"]
 v2v5_v1 -- v2v5_i0 [label=" ", penwidth="2.5", color="black:invis:black"]
 v2v5_v2 -- v2v5_i0 [label=" ", penwidth="2.5", color="black:invis:black"]
 v2v5_i0 -- v2v5_i1 [label=" ", penwidth="2.5", color="black:invis:black"]
 v2v5_i1 -- v2v5_i2 [label=" ", penwidth="2.5", color="black:invis:black:invis:black:invis:black"]
 v2v5_i2 -- v2v5_v3 [label=" ", penwidth="2.5", color="black:invis:black"]
 v2v5_i2 -- v2v5_v4 [label=" ", penwidth="2.5", color="black:invis:black"]
 v2v5_i1 -- v2v5_v5 [label=" ", penwidth="2.5", color="black:invis:black"]
}
  subgraph cluster_v3v4 {
  label="combine_count_and_normalize(v3,v4)"
  v3v4_v2 [label="v2"]
  v3v4_v5 [label="v5"]
  v3v4_v0 [label="v0"]
  v3v4_v3 [label="v3", style=filled, fillcolor=gray]
  v3v4_v4 [label="v4", style=filled, fillcolor=gray]
  v3v4_v1 [label="v1"]
  v3v4_i2 [label="i2"]
  v3v4_i1 [label="i1"]
  v3v4_i0 [label="i0"]
 v3v4_v0 -- v3v4_i0 [label=" ", penwidth="2.5", color="black:invis:black"]
 v3v4_v1 -- v3v4_i0 [label=" ", penwidth="2.5", color="black:invis:black"]
 v3v4_v2 -- v3v4_i0 [label=" ", penwidth="2.5", color="black:invis:black"]
 v3v4_i0 -- v3v4_i1 [label=" ", penwidth="2.5", color="black:invis:black:invis:black:invis:black:invis:black:invis:black"]
 v3v4_i1 -- v3v4_i2 [label=" ", penwidth="2.5", color="black:invis:black:invis:black:invis:black:invis:black:invis:black:invis:black:invis:black"]
 v3v4_i2 -- v3v4_v3 [label=" ", penwidth="2.5", color="black:invis:black"]
 v3v4_i2 -- v3v4_v4 [label=" ", penwidth="2.5", color="black:invis:black"]
 v3v4_i1 -- v3v4_v5 [label=" ", penwidth="2.5", color="black:invis:black"]
}
  subgraph cluster_v3v5 {
  label="combine_count_and_normalize(v3,v5)"
  v3v5_v2 [label="v2"]
  v3v5_v5 [label="v5", style=filled, fillcolor=gray]
  v3v5_v0 [label="v0"]
  v3v5_v3 [label="v3", style=filled, fillcolor=gray]
  v3v5_v4 [label="v4"]
  v3v5_v1 [label="v1"]
  v3v5_i2 [label="i2"]
  v3v5_i1 [label="i1"]
  v3v5_i0 [label="i0"]
 v3v5_v0 -- v3v5_i0 [label=" ", penwidth="2.5", color="black:invis:black"]
 v3v5_v1 -- v3v5_i0 [label=" ", penwidth="2.5", color="black:invis:black"]
 v3v5_v2 -- v3v5_i0 [label=" ", penwidth="2.5", color="black:invis:black"]
 v3v5_i0 -- v3v5_i1 [label=" ", penwidth="2.5", color="black:invis:black:invis:black:invis:black:invis:black:invis:black"]
 v3v5_i1 -- v3v5_i2 [label=" ", penwidth="2.5", color="black:invis:black"]
 v3v5_i2 -- v3v5_v3 [label=" ", penwidth="2.5", color="black:invis:black"]
 v3v5_i2 -- v3v5_v4 [label=" ", penwidth="2.5", color="black:invis:black"]
 v3v5_i1 -- v3v5_v5 [label=" ", penwidth="2.5", color="black:invis:black"]
}
  subgraph cluster_v4v5 {
  label="combine_count_and_normalize(v4,v5)"
  v4v5_v2 [label="v2"]
  v4v5_v5 [label="v5", style=filled, fillcolor=gray]
  v4v5_v0 [label="v0"]
  v4v5_v3 [label="v3"]
  v4v5_v4 [label="v4", style=filled, fillcolor=gray]
  v4v5_v1 [label="v1"]
  v4v5_i2 [label="i2"]
  v4v5_i1 [label="i1"]
  v4v5_i0 [label="i0"]
 v4v5_v0 -- v4v5_i0 [label=" ", penwidth="2.5", color="black:invis:black"]
 v4v5_v1 -- v4v5_i0 [label=" ", penwidth="2.5", color="black:invis:black"]
 v4v5_v2 -- v4v5_i0 [label=" ", penwidth="2.5", color="black:invis:black"]
 v4v5_i0 -- v4v5_i1 [label=" ", penwidth="2.5", color="black:invis:black:invis:black:invis:black:invis:black:invis:black"]
 v4v5_i1 -- v4v5_i2 [label=" ", penwidth="2.5", color="black:invis:black"]
 v4v5_i2 -- v4v5_v3 [label=" ", penwidth="2.5", color="black:invis:black"]
 v4v5_i2 -- v4v5_v4 [label=" ", penwidth="2.5", color="black:invis:black"]
 v4v5_i1 -- v4v5_v5 [label=" ", penwidth="2.5", color="black:invis:black"]
}
}
```
</div>

`{bm-enable-all}`

