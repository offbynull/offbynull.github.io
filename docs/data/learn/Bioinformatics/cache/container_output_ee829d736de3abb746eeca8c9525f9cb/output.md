<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

Still confused?

Given a simple tree, `combine_edge_multiple(A, B)` will make it so that...

 * limb A has a weight multiplicity of `leaf_count`.
 * limb B has a weight multiplicity of `leaf_count`.
 * other limbs each have a weight multiplicity of 2.
 * internal edges each have a weight multiplicity of > 2.
 
For example, the following diagrams visualize edge weight multiplicities produced by `combine_edge_multiple()` for various pairs in a 4 leaf simple tree. Note how the selected pair's limbs have a multiplicity of 4, other limbs have a multiplicity of 2, and internal edges have a multiplicity of 4...

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
 ranksep=0.25
 subgraph cluster_4 {
  label="combine_edge_multiple(v1,v2)"
  fontname="Courier-Bold"
  fontsize=10
  v0_z -- i0_z [label=" ", penwidth=2.5, color="purple:invis:orange"]
  v1_z -- i0_z [label=" ", penwidth=2.5, color="purple:invis:purple:invis:purple:invis:orange"]
  i0_z -- i1_z [label=" ", penwidth=2.5, color="purple:invis:purple:invis:orange:invis:orange"]
  i1_z -- v2_z [label=" ", penwidth=2.5, color="purple:invis:orange"]
  i1_z -- v3_z [label=" ", penwidth=2.5, color="purple:invis:orange:invis:orange:invis:orange"]
  v0_z [label=v0]
  v1_z [label=v1, style=filled, fillcolor=purple]
  v2_z [label=v2]
  v3_z [label=v3, style=filled, fillcolor=orange]
  i0_z [label=i0]
  i1_z [label=i1]
 }
 subgraph cluster_3 {
  label="combine_edge_multiple(v1,v2)"
  fontname="Courier-Bold"
  fontsize=10
  v0_y -- i0_y [label=" ", penwidth=2.5, color="purple:invis:orange"]
  v1_y -- i0_y [label=" ", penwidth=2.5, color="purple:invis:purple:invis:purple:invis:orange"]
  i0_y -- i1_y [label=" ", penwidth=2.5, color="purple:invis:purple:invis:orange:invis:orange"]
  i1_y -- v2_y [label=" ", penwidth=2.5, color="purple:invis:orange:invis:orange:invis:orange"]
  i1_y -- v3_y [label=" ", penwidth=2.5, color="orange:invis:purple"]
  v0_y [label=v0]
  v1_y [label=v1, style=filled, fillcolor=purple]
  v2_y [label=v2, style=filled, fillcolor=orange]
  v3_y [label=v3]
  i0_y [label=i0]
  i1_y [label=i1]
 }
 subgraph cluster_2 {
  label="combine_edge_multiple(v0,v1)"
  fontname="Courier-Bold"
  fontsize=10
  v0_x -- i0_x [label=" ", penwidth=2.5, color="purple:invis:orange:invis:orange:invis:orange"]
  v1_x -- i0_x [label=" ", penwidth=2.5, color="purple:invis:purple:invis:purple:invis:orange"]
  i0_x -- i1_x [label=" ", penwidth=2.5, color="purple:invis:purple:invis:orange:invis:orange"]
  i1_x -- v2_x [label=" ", penwidth=2.5, color="purple:invis:orange"]
  i1_x -- v3_x [label=" ", penwidth=2.5, color="purple:invis:orange"]
  v0_x [label=v0, style=filled, fillcolor=orange]
  v1_x [label=v1, style=filled, fillcolor=purple]
  v2_x [label=v2]
  v3_x [label=v3]
  i0_x [label=i0]
  i1_x [label=i1]
 }
}
```

`combine_edge_multiple_and_normalize(A, B)` normalizes these multiplicities such that ...

 * limb A's weight multiplicity reduces to 2.
 * limb B's weight multiplicity reduces to 2.
 * other limbs keep their weight multiplicities at 2.
 * if the pair are neighbours, each internal edge multiplicity remains at > 2.
 * if the pair aren't neighbours, at least one internal edge multiplicity reduces to 2 while others remain at > 2.

|                        | limb multiplicity | internal edge multiplicity   |
|------------------------|-------------------|------------------------------|
| neighbouring pairs     |      all = 2      |          all >= 2            |
| non-neighbouring pairs |      all = 2      | at least one = 2, others > 2 | 

Since limbs always contribute the same regardless of whether the pair is neighbouring or not (2*weight), they can be ignored. That leaves internal edge contributions as the only thing differentiating between neighbouring and non-neighbouring pairs.

A simple tree with 2 or more leaf nodes is guaranteed to have at least 1 neighbouring pair. The pair producing the largest result is the one with maxed out contributions from its multiplied internal edges weights, meaning that none of those contributions were for internal edges reduced to 2\*weight. Lesser results MAY be lesser because normalization reduced some of their internal edge weights to 2\*weight, but the largest result you know for certain has all of its internal edge weights > 2\*weight.
</div>

