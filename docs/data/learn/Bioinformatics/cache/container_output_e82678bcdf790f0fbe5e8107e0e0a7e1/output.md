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
N2 [label=""]
N3 [label=""]
N4 [label=""]
N5 [label=""]
N2 -> N1 [label="¶"]
N2 -> N3 [label="t¶"]
N0 -> N4 [label="app"]
N4 -> N2 [label="le"]
N4 -> N5 [label="eal¶"]
}
```

</div>

`{bm-enable-all}`

