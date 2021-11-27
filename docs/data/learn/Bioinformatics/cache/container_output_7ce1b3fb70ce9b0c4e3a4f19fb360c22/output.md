<div style="border:1px solid black;">

`{bm-disable-all}`

Given NON- additive distance matrix...

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
<td>14.0</td>
<td>22.0</td>
<td>20.0</td>
<td>23.0</td>
<td>22.0</td>
</tr>
<tr>
<td>v1</td>
<td>14.0</td>
<td>0.0</td>
<td>12.0</td>
<td>10.0</td>
<td>12.0</td>
<td>14.0</td>
</tr>
<tr>
<td>v2</td>
<td>22.0</td>
<td>12.0</td>
<td>0.0</td>
<td>20.0</td>
<td>22.0</td>
<td>20.0</td>
</tr>
<tr>
<td>v3</td>
<td>20.0</td>
<td>10.0</td>
<td>20.0</td>
<td>0.0</td>
<td>8.0</td>
<td>12.0</td>
</tr>
<tr>
<td>v4</td>
<td>23.0</td>
<td>12.0</td>
<td>22.0</td>
<td>8.0</td>
<td>0.0</td>
<td>15.0</td>
</tr>
<tr>
<td>v5</td>
<td>22.0</td>
<td>14.0</td>
<td>20.0</td>
<td>12.0</td>
<td>15.0</td>
<td>0.0</td>
</tr>
</tbody>
</table>


Replaced neighbours ('v3', 'v4') with their parent N1 to produce distance matrix ...

<table><thead><tr><th></th><th>N1</th><th>v0</th><th>v1</th><th>v2</th><th>v5</th></tr></thead><tbody><tr><td>N1</td><td>0.0</td><td>17.5</td><td>7.0</td><td>17.0</td><td>9.5</td></tr><tr><td>v0</td><td>17.5</td><td>0.0</td><td>14.0</td><td>22.0</td><td>22.0</td></tr><tr><td>v1</td><td>7.0</td><td>14.0</td><td>0.0</td><td>12.0</td><td>14.0</td></tr><tr><td>v2</td><td>17.0</td><td>22.0</td><td>12.0</td><td>0.0</td><td>20.0</td></tr><tr><td>v5</td><td>9.5</td><td>22.0</td><td>14.0</td><td>20.0</td><td>0.0</td></tr></tbody></table>


Replaced neighbours ('N1', 'v5') with their parent N2 to produce distance matrix ...

<table><thead><tr><th></th><th>N2</th><th>v0</th><th>v1</th><th>v2</th></tr></thead><tbody><tr><td>N2</td><td>0.0</td><td>15.0</td><td>5.75</td><td>13.75</td></tr><tr><td>v0</td><td>15.0</td><td>0.0</td><td>14.0</td><td>22.0</td></tr><tr><td>v1</td><td>5.75</td><td>14.0</td><td>0.0</td><td>12.0</td></tr><tr><td>v2</td><td>13.75</td><td>22.0</td><td>12.0</td><td>0.0</td></tr></tbody></table>


Replaced neighbours ('v0', 'N2') with their parent N3 to produce distance matrix ...

<table><thead><tr><th></th><th>N3</th><th>v1</th><th>v2</th></tr></thead><tbody><tr><td>N3</td><td>0.0</td><td>2.375</td><td>10.375</td></tr><tr><td>v1</td><td>2.375</td><td>0.0</td><td>12.0</td></tr><tr><td>v2</td><td>10.375</td><td>12.0</td><td>0.0</td></tr></tbody></table>


Replaced neighbours ('v1', 'N3') with their parent N4 to produce distance matrix ...

<table><thead><tr><th></th><th>N4</th><th>v2</th></tr></thead><tbody><tr><td>N4</td><td>0.0</td><td>10.0</td></tr><tr><td>v2</td><td>10.0</td><td>0.0</td></tr></tbody></table>


Obvious simple tree...

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[fontname="Courier-Bold", fontsize=10]
N4
v2
N4 -- v2 [label="10.0"]
}
```


Attached ('v1', 'N3') to N4 to produce tree...

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[fontname="Courier-Bold", fontsize=10]
N3
N4
v1
v2
N4 -- v2 [label="10.0"]
N4 -- v1 [label="2.0"]
N4 -- N3 [label="0.375"]
}
```


Attached ('v0', 'N2') to N3 to produce tree...

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[fontname="Courier-Bold", fontsize=10]
N2
N3
N4
v0
v1
v2
N4 -- v2 [label="10.0"]
N4 -- v1 [label="2.0"]
N4 -- N3 [label="0.375"]
N3 -- v0 [label="11.625"]
N3 -- N2 [label="3.375"]
}
```


Attached ('N1', 'v5') to N2 to produce tree...

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[fontname="Courier-Bold", fontsize=10]
N1
N2
N3
N4
v0
v1
v2
v5
N4 -- v2 [label="10.0"]
N4 -- v1 [label="2.0"]
N4 -- N3 [label="0.375"]
N3 -- v0 [label="11.625"]
N3 -- N2 [label="3.375"]
N2 -- N1 [label="2.3333333333333335"]
N2 -- v5 [label="7.166666666666666"]
}
```


Attached ('v3', 'v4') to N1 to produce tree...

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[fontname="Courier-Bold", fontsize=10]
N1
N2
N3
N4
v0
v1
v2
v3
v4
v5
N4 -- v2 [label="10.0"]
N4 -- v1 [label="2.0"]
N4 -- N3 [label="0.375"]
N3 -- v0 [label="11.625"]
N3 -- N2 [label="3.375"]
N2 -- N1 [label="2.3333333333333335"]
N2 -- v5 [label="7.166666666666666"]
N1 -- v3 [label="2.75"]
N1 -- v4 [label="5.25"]
}
```


</div>

`{bm-enable-all}`

