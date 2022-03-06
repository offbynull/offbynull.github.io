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
  edge_scale: 0.3
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
N1
N2
N3
N4
VEC1
VEC2
VEC3
VEC4
VEC5
VEC6
VEC4 -- N4 [label="0.52", len=0.1558756692]
N4 -- N2 [label="26.63", len=7.9877305285]
N4 -- N3 [label="0.48", len=0.1441243308]
N3 -- VEC5 [label="1.08", len=0.3240158358]
N3 -- VEC3 [label="0.65", len=0.1955994064]
N2 -- VEC6 [label="0.06", len=0.0182361896]
N2 -- N1 [label="14.85", len=4.4544978200]
N1 -- VEC1 [label="0.77", len=0.2305498043]
N1 -- VEC2 [label="0.23", len=0.0694501957]
}
```

The following leaf node membership probabilities were produced (per internal node) ...

 * N4 = VEC1=0.01,VEC2=0.01,VEC3=0.25,VEC4=0.54,VEC5=0.18,VEC6=0.01
 * N2 = VEC1=0.00,VEC2=0.00,VEC3=0.00,VEC4=0.00,VEC5=0.00,VEC6=0.99
 * N3 = VEC1=0.01,VEC2=0.01,VEC3=0.43,VEC4=0.28,VEC5=0.26,VEC6=0.01
 * N1 = VEC1=0.23,VEC2=0.75,VEC3=0.00,VEC4=0.00,VEC5=0.00,VEC6=0.01

</div>

`{bm-enable-all}`

