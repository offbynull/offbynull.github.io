<div style="border:1px solid black;">

`{bm-disable-all}`

Building and searching trie using the following settings...

```
{
  trie_sequences: ['anana', 'banana', 'ankle'],
  test_sequence: 'banana ankle baxana orange banxxa vehicle¶',
  end_marker: ¶,
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
N16 [label=""]
N17 [label=""]
N18 [label=""]
N19 [label=""]
N2 [label=""]
N20 [label=""]
N21 [label=""]
N22 [label=""]
N23 [label=""]
N24 [label=""]
N25 [label=""]
N26 [label=""]
N27 [label=""]
N28 [label=""]
N29 [label=""]
N3 [label=""]
N30 [label=""]
N31 [label=""]
N32 [label=""]
N33 [label=""]
N34 [label=""]
N35 [label=""]
N36 [label=""]
N37 [label=""]
N38 [label=""]
N39 [label=""]
N4 [label=""]
N40 [label=""]
N41 [label=""]
N42 [label=""]
N43 [label=""]
N44 [label=""]
N45 [label=""]
N46 [label=""]
N47 [label=""]
N48 [label=""]
N49 [label=""]
N5 [label=""]
N50 [label=""]
N51 [label=""]
N52 [label=""]
N53 [label=""]
N54 [label=""]
N55 [label=""]
N56 [label=""]
N57 [label=""]
N58 [label=""]
N59 [label=""]
N6 [label=""]
N7 [label=""]
N8 [label=""]
N9 [label=""]
N8 -> N11 [label="n\n[2, 3)\n[4, 5)\n[8, 9)\n[17, 18)\n[23, 24)\n[29, 30)"]
N11 -> N4 [label="a\n[3, 4)\n[5, 6)\n[18, 19)"]
N11 -> N12 [label="kle baxana orange banxxa vehicle¶\n[9, 42)"]
N0 -> N13 [label="n\n[2, 3)\n[4, 5)\n[8, 9)\n[17, 18)\n[23, 24)\n[29, 30)"]
N13 -> N6 [label="a\n[3, 4)\n[5, 6)\n[18, 19)"]
N13 -> N14 [label="kle baxana orange banxxa vehicle¶\n[9, 42)"]
N0 -> N15 [label="kle baxana orange banxxa vehicle¶\n[9, 42)"]
N0 -> N18 [label=" \n[6, 7)\n[12, 13)\n[19, 20)\n[26, 27)\n[33, 34)"]
N18 -> N10 [label="ankle baxana orange banxxa vehicle¶\n[7, 42)"]
N0 -> N20 [label="ba\n[0, 2)\n[13, 15)\n[27, 29)"]
N20 -> N21 [label="xana orange banxxa vehicle¶\n[15, 42)"]
N8 -> N22 [label="xana orange banxxa vehicle¶\n[15, 42)"]
N4 -> N24 [label=" \n[6, 7)\n[19, 20)"]
N24 -> N5 [label="ankle baxana orange banxxa vehicle¶\n[7, 42)"]
N24 -> N25 [label="orange banxxa vehicle¶\n[20, 42)"]
N6 -> N26 [label=" \n[6, 7)\n[19, 20)"]
N26 -> N7 [label="ankle baxana orange banxxa vehicle¶\n[7, 42)"]
N26 -> N27 [label="orange banxxa vehicle¶\n[20, 42)"]
N8 -> N28 [label=" \n[6, 7)\n[19, 20)\n[33, 34)"]
N28 -> N9 [label="ankle baxana orange banxxa vehicle¶\n[7, 42)"]
N28 -> N29 [label="orange banxxa vehicle¶\n[20, 42)"]
N18 -> N30 [label="orange banxxa vehicle¶\n[20, 42)"]
N4 -> N2 [label="na ankle baxana orange banxxa vehicle¶\n[4, 42)"]
N0 -> N31 [label="orange banxxa vehicle¶\n[20, 42)"]
N0 -> N32 [label="range banxxa vehicle¶\n[21, 42)"]
N11 -> N33 [label="ge banxxa vehicle¶\n[24, 42)"]
N13 -> N34 [label="ge banxxa vehicle¶\n[24, 42)"]
N0 -> N35 [label="ge banxxa vehicle¶\n[24, 42)"]
N36 -> N17 [label="xana orange banxxa vehicle¶\n[15, 42)"]
N36 -> N37 [label="nxxa vehicle¶\n[29, 42)"]
N18 -> N38 [label="ba\n[13, 15)\n[27, 29)"]
N38 -> N19 [label="xana orange banxxa vehicle¶\n[15, 42)"]
N38 -> N39 [label="nxxa vehicle¶\n[29, 42)"]
N20 -> N40 [label="n\n[2, 3)\n[29, 30)"]
N40 -> N1 [label="ana ankle baxana orange banxxa vehicle¶\n[3, 42)"]
N40 -> N41 [label="xxa vehicle¶\n[30, 42)"]
N11 -> N42 [label="xxa vehicle¶\n[30, 42)"]
N13 -> N43 [label="xxa vehicle¶\n[30, 42)"]
N0 -> N44 [label="x\n[15, 16)\n[30, 31)\n[31, 32)"]
N44 -> N45 [label="xa vehicle¶\n[31, 42)"]
N44 -> N46 [label="a\n[16, 17)\n[32, 33)"]
N46 -> N23 [label="na orange banxxa vehicle¶\n[17, 42)"]
N46 -> N47 [label=" vehicle¶\n[33, 42)"]
N28 -> N48 [label="vehicle¶\n[34, 42)"]
N18 -> N49 [label="vehicle¶\n[34, 42)"]
N0 -> N50 [label="vehicle¶\n[34, 42)"]
N0 -> N51 [label="e\n[11, 12)\n[25, 26)\n[35, 36)\n[40, 41)"]
N51 -> N36 [label=" ba\n[12, 15)\n[26, 29)"]
N51 -> N52 [label="hicle¶\n[36, 42)"]
N0 -> N53 [label="hicle¶\n[36, 42)"]
N0 -> N54 [label="icle¶\n[37, 42)"]
N6 -> N3 [label="na ankle baxana orange banxxa vehicle¶\n[4, 42)"]
N0 -> N55 [label="cle¶\n[38, 42)"]
N0 -> N56 [label="le\n[10, 12)\n[39, 41)"]
N56 -> N16 [label=" baxana orange banxxa vehicle¶\n[12, 42)"]
N56 -> N57 [label="¶\n[41, 42)"]
N51 -> N58 [label="¶\n[41, 42)"]
N0 -> N59 [label="¶\n[41, 42)"]
N0 -> N8 [label="a\n[1, 2)\n[3, 4)\n[5, 6)\n[7, 8)\n[14, 15)\n[16, 17)\n[18, 19)\n[22, 23)\n[28, 29)\n[32, 33)"]
}
```

Searching `banana ankle baxana orange banxxa vehicle¶` with the trie revealed the following was found:

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

