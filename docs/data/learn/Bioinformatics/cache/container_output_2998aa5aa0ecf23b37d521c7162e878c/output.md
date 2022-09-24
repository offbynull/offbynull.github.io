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


The following suffix array was produced ...

```
¶
 ankle baxana orange banxxa vehicle__¶
 banxxa vehicle__¶
 baxana orange banxxa vehicle__¶
 orange banxxa vehicle__¶
 vehicle__¶
_¶
__¶
__banana ankle baxana orange banxxa vehicle__¶
_banana ankle baxana orange banxxa vehicle__¶
a ankle baxana orange banxxa vehicle__¶
a orange banxxa vehicle__¶
a vehicle__¶
ana ankle baxana orange banxxa vehicle__¶
ana orange banxxa vehicle__¶
anana ankle baxana orange banxxa vehicle__¶
ange banxxa vehicle__¶
ankle baxana orange banxxa vehicle__¶
anxxa vehicle__¶
axana orange banxxa vehicle__¶
banana ankle baxana orange banxxa vehicle__¶
banxxa vehicle__¶
baxana orange banxxa vehicle__¶
cle__¶
e banxxa vehicle__¶
e baxana orange banxxa vehicle__¶
e__¶
ehicle__¶
ge banxxa vehicle__¶
hicle__¶
icle__¶
kle baxana orange banxxa vehicle__¶
le baxana orange banxxa vehicle__¶
le__¶
na ankle baxana orange banxxa vehicle__¶
na orange banxxa vehicle__¶
nana ankle baxana orange banxxa vehicle__¶
nge banxxa vehicle__¶
nkle baxana orange banxxa vehicle__¶
nxxa vehicle__¶
orange banxxa vehicle__¶
range banxxa vehicle__¶
vehicle__¶
xa vehicle__¶
xana orange banxxa vehicle__¶
xxa vehicle__¶
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

