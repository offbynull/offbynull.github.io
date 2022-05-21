<div style="border:1px solid black;">

`{bm-disable-all}`

Building and searching suffix tree using the following settings...

```
{
  prefix: an,
  sequence: banana¶,
  end_marker: ¶
}

```


The following suffix tree was produced ...

```{dot}
digraph G {
 rankdir=LR
 node[fontname="Courier-Bold", fontsize=10, shape=point]
 edge[fontname="Courier-Bold", fontsize=10]
N0 [label=""]
N1 [label=""]
N10 [label=""]
N2 [label=""]
N3 [label=""]
N4 [label=""]
N5 [label=""]
N6 [label=""]
N7 [label=""]
N8 [label=""]
N9 [label=""]
N0 -> N1 [label="banana¶\n[0, 7)"]
N8 -> N4 [label="na\n[2, 4)\n[4, 6)"]
N8 -> N9 [label="¶\n[6, 7)"]
N0 -> N10 [label="¶\n[6, 7)"]
N4 -> N2 [label="na¶\n[4, 7)"]
N4 -> N5 [label="¶\n[6, 7)"]
N0 -> N6 [label="na\n[2, 4)\n[4, 6)"]
N6 -> N3 [label="na¶\n[4, 7)"]
N6 -> N7 [label="¶\n[6, 7)"]
N0 -> N8 [label="a\n[1, 2)\n[3, 4)\n[5, 6)"]
}
```


Was *an* found in *banana¶*: True
</div>

`{bm-enable-all}`

