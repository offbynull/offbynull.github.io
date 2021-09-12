<div style="border:1px solid black;">

`{bm-disable-all}`

The tree...

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
v0 -- i0 [label="11.0"]
v1 -- i0 [label="2.0"]
v2 -- i0 [label="10.0"]
i0 -- i1 [label="4.0"]
i1 -- i2 [label="3.0"]
i2 -- v3 [label="3.0"]
i2 -- v4 [label="4.0"]
i1 -- v5 [label="7.0"]
}
```

... produces the additive distance matrix ...

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

</div>

`{bm-enable-all}`

