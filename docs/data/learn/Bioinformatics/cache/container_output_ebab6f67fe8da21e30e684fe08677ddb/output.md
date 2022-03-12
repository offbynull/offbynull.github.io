<div style="border:1px solid black;">

`{bm-disable-all}`

Building similarity graph and executing cluster affinity search technique (CAST) using the following settings...

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
  threshold: -15.2
}

```

The following similarity matrix was produced ...

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
<td>-0.00</td>
<td>-1.00</td>
<td>-43.30</td>
<td>-42.76</td>
<td>-43.91</td>
<td>-15.65</td>
</tr>
<tr>
<td>VEC2</td>
<td>-1.00</td>
<td>-0.00</td>
<td>-42.73</td>
<td>-42.20</td>
<td>-43.37</td>
<td>-15.17</td>
</tr>
<tr>
<td>VEC3</td>
<td>-43.30</td>
<td>-42.73</td>
<td>-0.00</td>
<td>-1.73</td>
<td>-1.73</td>
<td>-27.75</td>
</tr>
<tr>
<td>VEC4</td>
<td>-42.76</td>
<td>-42.20</td>
<td>-1.73</td>
<td>-0.00</td>
<td>-2.00</td>
<td>-27.22</td>
</tr>
<tr>
<td>VEC5</td>
<td>-43.91</td>
<td>-43.37</td>
<td>-1.73</td>
<td>-2.00</td>
<td>-0.00</td>
<td>-28.30</td>
</tr>
<tr>
<td>VEC6</td>
<td>-15.65</td>
<td>-15.17</td>
<td>-27.75</td>
<td>-27.22</td>
<td>-28.30</td>
<td>-0.00</td>
</tr>
</tbody>
</table>

The following _original_ similarity graph was produced ...

```{dot}
graph G {
 layout=circo
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[fontname="Courier-Bold", fontsize=10]
VEC1
VEC2
VEC3
VEC4
VEC5
VEC6
VEC1 -- VEC2
VEC6 -- VEC2
VEC4 -- VEC3
VEC3 -- VEC5
VEC4 -- VEC5
}
```

The following _corrected_ similarity graph was produced ...

```{dot}
graph G {
 layout=circo
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[fontname="Courier-Bold", fontsize=10]
VEC1
VEC2
VEC3
VEC4
VEC5
VEC6
VEC2 -- VEC1
VEC4 -- VEC3
VEC5 -- VEC3
VEC5 -- VEC4
}
```

</div>

`{bm-enable-all}`

