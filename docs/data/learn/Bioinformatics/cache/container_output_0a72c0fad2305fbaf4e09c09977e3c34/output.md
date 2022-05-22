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


The following suffix array was produced ...

```
¶
 ankle baxana orange banxxa vehicle¶
 banxxa vehicle¶
 baxana orange banxxa vehicle¶
 orange banxxa vehicle¶
 vehicle¶
a ankle baxana orange banxxa vehicle¶
a orange banxxa vehicle¶
a vehicle¶
ana ankle baxana orange banxxa vehicle¶
ana orange banxxa vehicle¶
anana ankle baxana orange banxxa vehicle¶
ange banxxa vehicle¶
ankle baxana orange banxxa vehicle¶
anxxa vehicle¶
axana orange banxxa vehicle¶
banana ankle baxana orange banxxa vehicle¶
banxxa vehicle¶
baxana orange banxxa vehicle¶
cle¶
e¶
e banxxa vehicle¶
e baxana orange banxxa vehicle¶
ehicle¶
ge banxxa vehicle¶
hicle¶
icle¶
kle baxana orange banxxa vehicle¶
le¶
le baxana orange banxxa vehicle¶
na ankle baxana orange banxxa vehicle¶
na orange banxxa vehicle¶
nana ankle baxana orange banxxa vehicle¶
nge banxxa vehicle¶
nkle baxana orange banxxa vehicle¶
nxxa vehicle¶
orange banxxa vehicle¶
range banxxa vehicle¶
vehicle¶
xa vehicle¶
xana orange banxxa vehicle¶
xxa vehicle¶
```

Searching `banana ankle baxana orange banxxa vehicle¶` with the trie revealed the following was found:

 * Matched `banana` against `banana` with distance of 0 at index 0
 * Matched `anana` against `anana` with distance of 0 at index 1
 * Matched `nana a` against `banana` with distance of 2 at index 2
 * Matched `ana a` against `anana` with distance of 1 at index 3
 * Matched `ankle` against `ankle` with distance of 0 at index 7
 * Matched `baxana` against `banana` with distance of 1 at index 13
 * Matched `axana` against `anana` with distance of 1 at index 14
 * Matched `ana o` against `anana` with distance of 2 at index 16
 * Matched `banxxa` against `banana` with distance of 2 at index 27
 * Matched `anxxa` against `anana` with distance of 2 at index 28
</div>

`{bm-enable-all}`

