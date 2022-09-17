<div style="border:1px solid black;">

`{bm-disable-all}`

Building BWT using the following settings...

```
{
  sequence: abbazabbabbu¶,
  end_marker: ¶,
  index: 5,
  symbol: b
}

```


The following first and last columns were produced ...

 * First (squashed): {'¶': 0, 'a': 1, 'b': 5, 'u': 11, 'z': 12}
 * Last: u{u=1}, z{u=1,z=1}, ¶{u=1,z=1,¶=1}, b{u=1,z=1,¶=1,b=1}, b{u=1,z=1,¶=1,b=2}, b{u=1,z=1,¶=1,b=3}, b{u=1,z=1,¶=1,b=4}, a{u=1,z=1,¶=1,b=4,a=1}, a{u=1,z=1,¶=1,b=4,a=2}, a{u=1,z=1,¶=1,b=4,a=3}, b{u=1,z=1,¶=1,b=5,a=3}, b{u=1,z=1,¶=1,b=6,a=3}, a{u=1,z=1,¶=1,b=6,a=4}


There where 2 instances of *b* just before reaching index *5* in last.

There where 3 instances of *b* at index *5* in last.
</div>

`{bm-enable-all}`

