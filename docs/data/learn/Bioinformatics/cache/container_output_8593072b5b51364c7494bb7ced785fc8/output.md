<div style="border:1px solid black;">

`{bm-disable-all}`

Building and searching trie using the following settings...

```
{
  trie_sequences: [aratrium¶, aratron¶, ration¶],
  test_sequence: There were multiple narrations in the play,
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
N0 -> N1 [label="r"]
N1 -> N2 [label="a"]
N10 -> N11 [label="t"]
N11 -> N12 [label="r"]
N12 -> N13 [label="o"]
N13 -> N14 [label="n"]
N14 -> N15 [label="¶"]
N12 -> N16 [label="i"]
N16 -> N17 [label="u"]
N17 -> N18 [label="m"]
N18 -> N19 [label="¶"]
N2 -> N3 [label="t"]
N3 -> N4 [label="i"]
N4 -> N5 [label="o"]
N5 -> N6 [label="n"]
N6 -> N7 [label="¶"]
N0 -> N8 [label="a"]
N8 -> N9 [label="r"]
N9 -> N10 [label="a"]
N11 -> N3 [color=red, style=dashed]
N2 -> N8 [color=red, style=dashed]
}
```


Searching *There were multiple narrations in the play* with the trie revealed the following was found: {(23, ration)}
</div>

`{bm-enable-all}`

