<div style="border:1px solid black;">

`{bm-disable-all}`

Building trie using the following settings...

```
{
  trie_sequences: [aratrium¶, aratron¶, ration¶],
  end_marker: ¶
}

```


The following trie was produced ...

```{dot}
digraph G {
 rankdir=LR
 node[fontname="Courier-Bold", fontsize=10, shape=point]
 edge[fontname="Courier-Bold", fontsize=10]
N0 [label=""]
N1 [label=""]
N10 [label=""]
N11 [label=""]
N12 [label=""]
N13 [label=""]
N14 [label=""]
N15 [label=""]
N16 [label=""]
N17 [label=""]
N18 [label=""]
N19 [label=""]
N2 [label=""]
N3 [label=""]
N4 [label=""]
N5 [label=""]
N6 [label=""]
N7 [label=""]
N8 [label=""]
N9 [label=""]
N0 -> N1 [label="a"]
N1 -> N2 [label="r"]
N10 -> N11 [label="m"]
N11 -> N12 [label="¶"]
N0 -> N13 [label="r"]
N13 -> N14 [label="a"]
N14 -> N15 [label="t"]
N15 -> N16 [label="i"]
N16 -> N17 [label="o"]
N17 -> N18 [label="n"]
N18 -> N19 [label="¶"]
N2 -> N3 [label="a"]
N3 -> N4 [label="t"]
N4 -> N5 [label="r"]
N5 -> N6 [label="o"]
N6 -> N7 [label="n"]
N7 -> N8 [label="¶"]
N5 -> N9 [label="i"]
N9 -> N10 [label="u"]
N4 -> N15 [color=red, style=dashed]
N14 -> N1 [color=red, style=dashed]
}
```

</div>

`{bm-enable-all}`

