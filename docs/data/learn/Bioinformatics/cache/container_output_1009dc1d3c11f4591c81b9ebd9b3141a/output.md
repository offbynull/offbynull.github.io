<div style="border:1px solid black;">

`{bm-disable-all}`

Building and searching trie using the following settings...

```
{
  trie_sequences: [apple¶, applet¶, appeal¶],
  test_sequence: "How do you feel about apples?",
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
N10 -> N11 [label="¶"]
N5 -> N12 [label="¶"]
N2 -> N3 [label="p"]
N3 -> N4 [label="l"]
N4 -> N5 [label="e"]
N5 -> N6 [label="t"]
N6 -> N7 [label="¶"]
N3 -> N8 [label="e"]
N8 -> N9 [label="a"]
N9 -> N10 [label="l"]
}
```


Searching `How do you feel about apples?` with the trie revealed the following was found: (22, apple)
</div>

`{bm-enable-all}`

