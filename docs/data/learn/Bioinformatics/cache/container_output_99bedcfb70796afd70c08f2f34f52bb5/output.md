<div style="border:1px solid black;">

`{bm-disable-all}`

Building BWT using the following settings...

```
sequence: banana¶
end_marker: ¶
last_tallies_checkpoint_n: 3
test: ana

```


The following first and last columns were produced ...

 * First (squashed): {'¶': 0, 'a': 1, 'b': 4, 'n': 5}
 * Last: ['a', 'n', 'n', 'b', '¶', 'a', 'a']
 * Last tallies checkpoints: {0: {a=1}, 3: {a=1,n=2,b=1}, 6: {a=3,n=2,b=1,¶=1}}


*ana* found in *banana¶* 2 times.
</div>

`{bm-enable-all}`
