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
N60 [label=""]
N61 [label=""]
N62 [label=""]
N63 [label=""]
N64 [label=""]
N65 [label=""]
N7 [label=""]
N8 [label=""]
N9 [label=""]
N0 -> N2 [label="_\n[0, 1)\n[1, 2)\n[43, 44)\n[44, 45)"]
N9 -> N6 [label="na ankle baxana orange banxxa vehicle__¶\n[6, 46)"]
N0 -> N11 [label="a\n[3, 4)\n[5, 6)\n[7, 8)\n[9, 10)\n[16, 17)\n[18, 19)\n[20, 21)\n[24, 25)\n[30, 31)\n[34, 35)"]
N11 -> N14 [label="n\n[4, 5)\n[6, 7)\n[10, 11)\n[19, 20)\n[25, 26)\n[31, 32)"]
N14 -> N7 [label="a\n[5, 6)\n[7, 8)\n[20, 21)"]
N14 -> N15 [label="kle baxana orange banxxa vehicle__¶\n[11, 46)"]
N0 -> N16 [label="n\n[4, 5)\n[6, 7)\n[10, 11)\n[19, 20)\n[25, 26)\n[31, 32)"]
N16 -> N9 [label="a\n[5, 6)\n[7, 8)\n[20, 21)"]
N16 -> N17 [label="kle baxana orange banxxa vehicle__¶\n[11, 46)"]
N0 -> N18 [label="kle baxana orange banxxa vehicle__¶\n[11, 46)"]
N0 -> N21 [label=" \n[8, 9)\n[14, 15)\n[21, 22)\n[28, 29)\n[35, 36)"]
N21 -> N13 [label="ankle baxana orange banxxa vehicle__¶\n[9, 46)"]
N0 -> N23 [label="ba\n[2, 4)\n[15, 17)\n[29, 31)"]
N2 -> N3 [label="banana ankle baxana orange banxxa vehicle__¶\n[2, 46)"]
N23 -> N24 [label="xana orange banxxa vehicle__¶\n[17, 46)"]
N11 -> N25 [label="xana orange banxxa vehicle__¶\n[17, 46)"]
N7 -> N27 [label=" \n[8, 9)\n[21, 22)"]
N27 -> N8 [label="ankle baxana orange banxxa vehicle__¶\n[9, 46)"]
N27 -> N28 [label="orange banxxa vehicle__¶\n[22, 46)"]
N9 -> N29 [label=" \n[8, 9)\n[21, 22)"]
N29 -> N10 [label="ankle baxana orange banxxa vehicle__¶\n[9, 46)"]
N29 -> N30 [label="orange banxxa vehicle__¶\n[22, 46)"]
N11 -> N31 [label=" \n[8, 9)\n[21, 22)\n[35, 36)"]
N31 -> N12 [label="ankle baxana orange banxxa vehicle__¶\n[9, 46)"]
N31 -> N32 [label="orange banxxa vehicle__¶\n[22, 46)"]
N21 -> N33 [label="orange banxxa vehicle__¶\n[22, 46)"]
N0 -> N34 [label="orange banxxa vehicle__¶\n[22, 46)"]
N0 -> N35 [label="range banxxa vehicle__¶\n[23, 46)"]
N14 -> N36 [label="ge banxxa vehicle__¶\n[26, 46)"]
N16 -> N37 [label="ge banxxa vehicle__¶\n[26, 46)"]
N0 -> N38 [label="ge banxxa vehicle__¶\n[26, 46)"]
N39 -> N20 [label="xana orange banxxa vehicle__¶\n[17, 46)"]
N39 -> N40 [label="nxxa vehicle__¶\n[31, 46)"]
N21 -> N41 [label="ba\n[15, 17)\n[29, 31)"]
N41 -> N22 [label="xana orange banxxa vehicle__¶\n[17, 46)"]
N41 -> N42 [label="nxxa vehicle__¶\n[31, 46)"]
N23 -> N43 [label="n\n[4, 5)\n[31, 32)"]
N43 -> N4 [label="ana ankle baxana orange banxxa vehicle__¶\n[5, 46)"]
N43 -> N44 [label="xxa vehicle__¶\n[32, 46)"]
N14 -> N45 [label="xxa vehicle__¶\n[32, 46)"]
N16 -> N46 [label="xxa vehicle__¶\n[32, 46)"]
N0 -> N47 [label="x\n[17, 18)\n[32, 33)\n[33, 34)"]
N47 -> N48 [label="xa vehicle__¶\n[33, 46)"]
N47 -> N49 [label="a\n[18, 19)\n[34, 35)"]
N49 -> N26 [label="na orange banxxa vehicle__¶\n[19, 46)"]
N49 -> N50 [label=" vehicle__¶\n[35, 46)"]
N31 -> N51 [label="vehicle__¶\n[36, 46)"]
N21 -> N52 [label="vehicle__¶\n[36, 46)"]
N0 -> N53 [label="vehicle__¶\n[36, 46)"]
N0 -> N54 [label="e\n[13, 14)\n[27, 28)\n[37, 38)\n[42, 43)"]
N54 -> N39 [label=" ba\n[14, 17)\n[28, 31)"]
N54 -> N55 [label="hicle__¶\n[38, 46)"]
N0 -> N56 [label="hicle__¶\n[38, 46)"]
N0 -> N57 [label="icle__¶\n[39, 46)"]
N0 -> N58 [label="cle__¶\n[40, 46)"]
N0 -> N59 [label="le\n[12, 14)\n[41, 43)"]
N59 -> N19 [label=" baxana orange banxxa vehicle__¶\n[14, 46)"]
N59 -> N60 [label="__¶\n[43, 46)"]
N54 -> N61 [label="__¶\n[43, 46)"]
N2 -> N62 [label="_\n[1, 2)\n[44, 45)"]
N7 -> N5 [label="na ankle baxana orange banxxa vehicle__¶\n[6, 46)"]
N62 -> N1 [label="banana ankle baxana orange banxxa vehicle__¶\n[2, 46)"]
N62 -> N63 [label="¶\n[45, 46)"]
N2 -> N64 [label="¶\n[45, 46)"]
N0 -> N65 [label="¶\n[45, 46)"]
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

