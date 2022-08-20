<div style="border:1px solid black;">

`{bm-disable-all}`

Building and searching trie using the following settings...

```
{
  trie_sequences: ['anana', 'banana', 'ankle'],
  test_sequence: 'banana ankle baxana orange banxxa vehicle',
  end_marker: ¶,
  pad_marker: _,
  max_mismatch: 2
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
N2 [label=""]
N3 [label=""]
N4 [label=""]
N5 [label=""]
N6 [label=""]
N7 [label=""]
N8 [label=""]
N9 [label=""]
N0 -> N1 [label="n"]
N1 -> N2 [label="a"]
N0 -> N11 [label="e"]
N11 -> N12 [label="¶"]
N0 -> N13 [label="b"]
N13 -> N14 [label="a"]
N14 -> N15 [label="¶"]
N2 -> N3 [label="¶"]
N0 -> N4 [label="a"]
N4 -> N5 [label="¶"]
N0 -> N6 [label="k"]
N6 -> N7 [label="l"]
N7 -> N8 [label="¶"]
N4 -> N9 [label="n"]
N9 -> N10 [label="¶"]
N2 -> N4 [color=red, style=dashed]
N9 -> N1 [color=red, style=dashed]
N14 -> N4 [color=red, style=dashed]
}
```

Searching `banana ankle baxana orange banxxa vehicle` with the trie revealed the following was found:

 * Matched `_bana` against `anana` with distance of 2 at index -1
 * Matched `banana` against `banana` with distance of 0 at index 0
 * Matched `anana` against `anana` with distance of 0 at index 1
 * Matched `nana a` against `banana` with distance of 2 at index 2
 * Matched `ana a` against `anana` with distance of 1 at index 3
 * Matched `a ank` against `anana` with distance of 2 at index 5
 * Matched `ankle` against `ankle` with distance of 0 at index 7
 * Matched `baxana` against `banana` with distance of 1 at index 13
 * Matched `axana` against `anana` with distance of 1 at index 14
 * Matched `ana o` against `anana` with distance of 2 at index 16
 * Matched `banxxa` against `banana` with distance of 2 at index 27
 * Matched `anxxa` against `anana` with distance of 2 at index 28
</div>

`{bm-enable-all}`

