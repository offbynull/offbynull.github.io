<div style="border:1px solid black;">

`{bm-disable-all}`

Given the additive distance matrix for simple tree T...

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

... and simple tree trim(T, v5)...

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[fontname="Courier-Bold", fontsize=10]
i0
i2
v0
v1
v2
v3
v4
i0 -- i2 [label="7.0"]
i2 -- v3 [label="3.0"]
i2 -- v4 [label="4.0"]
v0 -- i0 [label="11.0"]
v1 -- i0 [label="2.0"]
v2 -- i0 [label="10.0"]
}
```

... , v5 is injected at the appropriate location to become simple tree T (un-trimmed) ...


```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[fontname="Courier-Bold", fontsize=10]
N1
i0
i2
v0
v1
v2
v3
v4
v5
i0 -- N1 [label="4.0"]
N1 -- i2 [label="3.0"]
N1 -- v5 [label="7.0"]
i2 -- v3 [label="3.0"]
i2 -- v4 [label="4.0"]
v0 -- i0 [label="11.0"]
v1 -- i0 [label="2.0"]
v2 -- i0 [label="10.0"]
}
```

</div>

`{bm-enable-all}`

