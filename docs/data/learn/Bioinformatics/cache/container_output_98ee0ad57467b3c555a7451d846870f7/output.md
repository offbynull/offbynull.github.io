<div style="border:1px solid black;">

`{bm-disable-all}`

Building BWT using the following settings...

```
{
  sequence: banana¶,
  end_marker: ¶,
  last_tallies_checkpoint_n: 3,
  index: 5
}

```


The following last column and squashed first mapping were produced ...

 * First (squashed): {'¶': 0, 'a': 1, 'b': 4, 'n': 5}
 * Last: ['a', 'n', 'n', 'b', '¶', 'a', 'a']
 * Last tallies checkpoints: {0: {a=1}, 3: {a=1,n=2,b=1}, 6: {a=3,n=2,b=1,¶=1}}

The tally at index 5 is calculated as {a=2,¶=1,n=2,b=1}
</div>

`{bm-enable-all}`
