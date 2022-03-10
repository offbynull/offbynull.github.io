<div style="border:1px solid black;">

`{bm-disable-all}`

Executing neighbour joining phylogeny **soft** clustering using the following settings...

```
{
  metric: euclidean,  # OPTIONS: euclidean, manhattan, cosine, pearson
  vectors: {
    VEC1: [5,6,5],
    VEC2: [5,7,5],
    VEC3: [30,31,30],
    VEC4: [29,30,31],
    VEC5: [31,30,31],
    VEC6: [15,14,14]
  },
  dist_capture: 5.0,
  edge_scale: 0.2
}

```

The following distance matrix was produced ...

<table>
<thead><tr>
<th></th>
<th>VEC1</th>
<th>VEC2</th>
<th>VEC3</th>
<th>VEC4</th>
<th>VEC5</th>
<th>VEC6</th>
</tr></thead>
<tbody>
<tr>
<td>VEC1</td>
<td>0.00</td>
<td>1.00</td>
<td>43.30</td>
<td>42.76</td>
<td>43.91</td>
<td>15.65</td>
</tr>
<tr>
<td>VEC2</td>
<td>1.00</td>
<td>0.00</td>
<td>42.73</td>
<td>42.20</td>
<td>43.37</td>
<td>15.17</td>
</tr>
<tr>
<td>VEC3</td>
<td>43.30</td>
<td>42.73</td>
<td>0.00</td>
<td>1.73</td>
<td>1.73</td>
<td>27.75</td>
</tr>
<tr>
<td>VEC4</td>
<td>42.76</td>
<td>42.20</td>
<td>1.73</td>
<td>0.00</td>
<td>2.00</td>
<td>27.22</td>
</tr>
<tr>
<td>VEC5</td>
<td>43.91</td>
<td>43.37</td>
<td>1.73</td>
<td>2.00</td>
<td>0.00</td>
<td>28.30</td>
</tr>
<tr>
<td>VEC6</td>
<td>15.65</td>
<td>15.17</td>
<td>27.75</td>
<td>27.22</td>
<td>28.30</td>
<td>0.00</td>
</tr>
</tbody>
</table>

The following neighbour joining phylogeny tree was produced ...

```{dot}
graph G {
 layout=neato
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[fontname="Courier-Bold", fontsize=10]
N1 [style=filled, fillcolor="#1ef6f6"]
N2
N3 [style=filled, fillcolor="#fc2d2d"]
N4 [style=filled, fillcolor="#fc2d2d"]
VEC1 [style=filled, fillcolor="#1ef6f6"]
VEC2 [style=filled, fillcolor="#1ef6f6"]
VEC3 [style=filled, fillcolor="#fc2d2d"]
VEC4 [style=filled, fillcolor="#fc2d2d"]
VEC5 [style=filled, fillcolor="#fc2d2d"]
VEC6
N4 -- VEC4 [label="0.52", len=0.1039171128]
N4 -- N2 [label="26.63", len=5.3251536857]
N4 -- N3 [label="0.48", len=0.0960828872]
N3 -- VEC3 [label="0.65", len=0.1303996043]
N3 -- VEC5 [label="1.08", len=0.2160105572]
N2 -- N1 [label="14.85", len=2.9696652133]
N2 -- VEC6 [label="0.06", len=0.0121574597]
N1 -- VEC2 [label="0.23", len=0.0463001305]
N1 -- VEC1 [label="0.77", len=0.1536998695]
}
```

The following clusters were estimated ...

 * VEC4, VEC3, N4, VEC5, N3
 * VEC2, VEC1, N1

</div>

`{bm-enable-all}`

