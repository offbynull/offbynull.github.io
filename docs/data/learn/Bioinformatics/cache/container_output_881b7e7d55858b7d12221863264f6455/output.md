<div style="border:1px solid black;">

`{bm-disable-all}`

Executing UPGMA clustering using the following settings...

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
  }
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

The following UPGMA tree was produced ...

```{dot}
graph G {
 graph[rankdir=BT]
 node[shape=egg, fontname="Courier-Bold", fontsize=10]
 edge[fontname="Courier-Bold", fontsize=10]
C0 [label="C0\n0.50"]
C1 [label="C1\n0.87"]
C2 [label="C2\n0.93"]
C3 [label="C3\n7.70"]
C4 [label="C4\n18.97"]
VEC1 [label="VEC1\n0.00"]
VEC2 [label="VEC2\n0.00"]
VEC3 [label="VEC3\n0.00"]
VEC4 [label="VEC4\n0.00"]
VEC5 [label="VEC5\n0.00"]
VEC6 [label="VEC6\n0.00"]
VEC2 -- C0 [label="0.50"]
VEC1 -- C0 [label="0.50"]
VEC3 -- C1 [label="0.87"]
VEC5 -- C1 [label="0.87"]
VEC4 -- C2 [label="0.93"]
C1 -- C2 [label="0.07"]
VEC6 -- C3 [label="7.70"]
C0 -- C3 [label="7.20"]
C3 -- C4 [label="11.27"]
C2 -- C4 [label="18.04"]
}
```

</div>

`{bm-enable-all}`

