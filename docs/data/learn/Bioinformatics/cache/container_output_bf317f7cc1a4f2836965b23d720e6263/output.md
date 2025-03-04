<div style="border:1px solid black;">

`{bm-disable-all}`

Given the distance matrix ...

<table><thead><tr><th></th><th>v0</th><th>v1</th><th>v2</th><th>v3</th><th>v4</th><th>v5</th></tr></thead><tbody><tr><td>v0</td><td>0.0</td><td>13.0</td><td>21.0</td><td>21.0</td><td>22.0</td><td>22.0</td></tr><tr><td>v1</td><td>13.0</td><td>0.0</td><td>12.0</td><td>12.0</td><td>13.0</td><td>13.0</td></tr><tr><td>v2</td><td>21.0</td><td>12.0</td><td>0.0</td><td>20.0</td><td>21.0</td><td>21.0</td></tr><tr><td>v3</td><td>21.0</td><td>12.0</td><td>20.0</td><td>0.0</td><td>7.0</td><td>13.0</td></tr><tr><td>v4</td><td>22.0</td><td>13.0</td><td>21.0</td><td>7.0</td><td>0.0</td><td>14.0</td></tr><tr><td>v5</td><td>22.0</td><td>13.0</td><td>21.0</td><td>13.0</td><td>14.0</td><td>0.0</td></tr></tbody></table>


Trimmed v0 to produce distance matrix ...

<table><thead><tr><th></th><th>v1</th><th>v2</th><th>v3</th><th>v4</th><th>v5</th></tr></thead><tbody><tr><td>v1</td><td>0.0</td><td>12.0</td><td>12.0</td><td>13.0</td><td>13.0</td></tr><tr><td>v2</td><td>12.0</td><td>0.0</td><td>20.0</td><td>21.0</td><td>21.0</td></tr><tr><td>v3</td><td>12.0</td><td>20.0</td><td>0.0</td><td>7.0</td><td>13.0</td></tr><tr><td>v4</td><td>13.0</td><td>21.0</td><td>7.0</td><td>0.0</td><td>14.0</td></tr><tr><td>v5</td><td>13.0</td><td>21.0</td><td>13.0</td><td>14.0</td><td>0.0</td></tr></tbody></table>


Trimmed v1 to produce distance matrix ...

<table><thead><tr><th></th><th>v2</th><th>v3</th><th>v4</th><th>v5</th></tr></thead><tbody><tr><td>v2</td><td>0.0</td><td>20.0</td><td>21.0</td><td>21.0</td></tr><tr><td>v3</td><td>20.0</td><td>0.0</td><td>7.0</td><td>13.0</td></tr><tr><td>v4</td><td>21.0</td><td>7.0</td><td>0.0</td><td>14.0</td></tr><tr><td>v5</td><td>21.0</td><td>13.0</td><td>14.0</td><td>0.0</td></tr></tbody></table>


Trimmed v3 to produce distance matrix ...

<table><thead><tr><th></th><th>v2</th><th>v4</th><th>v5</th></tr></thead><tbody><tr><td>v2</td><td>0.0</td><td>21.0</td><td>21.0</td></tr><tr><td>v4</td><td>21.0</td><td>0.0</td><td>14.0</td></tr><tr><td>v5</td><td>21.0</td><td>14.0</td><td>0.0</td></tr></tbody></table>


Trimmed v2 to produce distance matrix ...

<table><thead><tr><th></th><th>v4</th><th>v5</th></tr></thead><tbody><tr><td>v4</td><td>0.0</td><td>14.0</td></tr><tr><td>v5</td><td>14.0</td><td>0.0</td></tr></tbody></table>


Obvious simple tree...

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[fontname="Courier-Bold", fontsize=10]
v4
v5
v4 -- v5 [label="14.0"]
}
```


Attached v2 to produce tree...

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[fontname="Courier-Bold", fontsize=10]
N1
v2
v4
v5
v4 -- N1 [label="7.0"]
N1 -- v5 [label="7.0"]
N1 -- v2 [label="14.0"]
}
```


Attached v3 to produce tree...

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[fontname="Courier-Bold", fontsize=10]
N1
N2
v2
v3
v4
v5
N1 -- v5 [label="7.0"]
N1 -- v2 [label="14.0"]
v4 -- N2 [label="4.0"]
N2 -- N1 [label="3.0"]
N2 -- v3 [label="3.0"]
}
```


Attached v1 to produce tree...

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[fontname="Courier-Bold", fontsize=10]
N1
N2
N3
v1
v2
v3
v4
v5
N3 -- v1 [label="2.0"]
N1 -- v5 [label="7.0"]
v4 -- N2 [label="4.0"]
N2 -- N1 [label="3.0"]
N2 -- v3 [label="3.0"]
N1 -- N3 [label="4.0"]
N3 -- v2 [label="10.0"]
}
```


Attached v0 to produce tree...

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[fontname="Courier-Bold", fontsize=10]
N1
N2
N3
v0
v1
v2
v3
v4
v5
N3 -- v1 [label="2.0"]
N3 -- v0 [label="11.0"]
N1 -- v5 [label="7.0"]
v4 -- N2 [label="4.0"]
N2 -- N1 [label="3.0"]
N2 -- v3 [label="3.0"]
N1 -- N3 [label="4.0"]
N3 -- v2 [label="10.0"]
}
```


</div>

`{bm-enable-all}`

