<div style="border:1px solid black;">

`{bm-disable-all}`

Building BWT using the following settings...

```
sequence: banana¶
end_marker: ¶
last_tallies_checkpoint_n: 3
first_indexes_checkpoint_n: 3
test: ana

```


The following last column and squashed first mapping were produced ...

 * First (squashed): {'¶': 0, 'a': 1, 'b': 4, 'n': 5}
 * First Index Checkpoints: {0: 6, 2: 3, 4: 0}
 * Last: ['a', 'n', 'n', 'b', '¶', 'a', 'a']
 * Last tallies checkpoints: {0: {a=1}, 3: {a=1,n=2,b=1}, 6: {a=3,n=2,b=1,¶=1}}


*ana* found in *banana¶* at indices [3, 1].
</div>

`{bm-enable-all}`
