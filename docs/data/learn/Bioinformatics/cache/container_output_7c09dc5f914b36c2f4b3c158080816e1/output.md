<div style="border:1px solid black;">

`{bm-disable-all}`

Building trie using the following settings...

```
{
  trie_sequences: [apple¶, applet¶, appeal¶],
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
N2 [label=""]
N3 [label=""]
N4 [label=""]
N5 [label=""]
N6 [label=""]
N7 [label=""]
N8 [label=""]
N9 [label=""]
N0 -> N1 [label="a"]
N1 -> N2 [label="p"]
N10 -> N11 [label="l"]
N11 -> N12 [label="¶"]
N2 -> N3 [label="p"]
N3 -> N4 [label="l"]
N4 -> N5 [label="e"]
N5 -> N6 [label="¶"]
N5 -> N7 [label="t"]
N7 -> N8 [label="¶"]
N3 -> N9 [label="e"]
N9 -> N10 [label="a"]
}
```

</div>

`{bm-enable-all}`
