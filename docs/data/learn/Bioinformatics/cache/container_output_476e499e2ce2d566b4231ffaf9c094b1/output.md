<div style="border:1px solid black;">

`{bm-disable-all}`

Building BWT using the following settings...

```
{
  sequence: banana¶,
  end_marker: ¶,
  first_indexes_checkpoint_n: 3,
  from_index: 5
}

```


The following first and last columns were produced ...

 * First: ['¶1', 'a3', 'a2', 'a1', 'b1', 'n2', 'n1']
 * First Index Checkpoints: {0: 6, 2: 3, 4: 0}
 * Last: ['a3', 'n2', 'n1', 'b1', '¶1', 'a2', 'a1']

Walking back to a first index checkpoint resulted in a first index of 4 ...

</div>

`{bm-enable-all}`

