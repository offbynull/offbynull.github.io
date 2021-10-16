<div style="border:1px solid black;">

`{bm-disable-all}`

Given the distance matrix ...

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
<td>0.0</td>
<td>13.0</td>
<td>21.0</td>
<td>21.0</td>
<td>22.0</td>
<td>22.0</td>
</tr>
<tr>
<td>v1</td>
<td>13.0</td>
<td>0.0</td>
<td>12.0</td>
<td>12.0</td>
<td>13.0</td>
<td>13.0</td>
</tr>
<tr>
<td>v2</td>
<td>21.0</td>
<td>12.0</td>
<td>0.0</td>
<td>20.0</td>
<td>21.0</td>
<td>21.0</td>
</tr>
<tr>
<td>v3</td>
<td>21.0</td>
<td>12.0</td>
<td>20.0</td>
<td>0.0</td>
<td>7.0</td>
<td>13.0</td>
</tr>
<tr>
<td>v4</td>
<td>22.0</td>
<td>13.0</td>
<td>21.0</td>
<td>7.0</td>
<td>0.0</td>
<td>14.0</td>
</tr>
<tr>
<td>v5</td>
<td>22.0</td>
<td>13.0</td>
<td>21.0</td>
<td>13.0</td>
<td>14.0</td>
<td>0.0</td>
</tr>
</tbody>
</table>

... the UPGMA generated tree is ...


```{dot}
graph G {
 graph[rankdir=BT]
 node[shape=egg, fontname="Courier-Bold", fontsize=10]
 edge[fontname="Courier-Bold", fontsize=10]
C0 [label="C0\n3.5"]
C1 [label="C1\n6.0"]
C2 [label="C2\n6.75"]
C3 [label="C3\n8.333333333333334"]
C4 [label="C4\n9.9"]
v0 [label="v0\n0"]
v1 [label="v1\n0"]
v2 [label="v2\n0"]
v3 [label="v3\n0"]
v4 [label="v4\n0"]
v5 [label="v5\n0"]
v4 -- C0 [label="3.5"]
v3 -- C0 [label="3.5"]
v1 -- C1 [label="6.0"]
v2 -- C1 [label="6.0"]
v5 -- C2 [label="6.75"]
C0 -- C2 [label="3.25"]
C1 -- C3 [label="2.333333333333334"]
C2 -- C3 [label="1.583333333333334"]
C3 -- C4 [label="1.5666666666666664"]
v0 -- C4 [label="9.9"]
}
```

</div>

`{bm-enable-all}`

