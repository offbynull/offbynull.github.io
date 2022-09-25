<div style="border:1px solid black;">

`{bm-disable-all}`

Building BWT using the following settings...

```
sequence: abbazabbabbu¶
test: bba
end_marker: ¶

```


The following first and last columns were produced ...

 * First: [('¶', 1), ('a', 1), ('a', 2), ('a', 3), ('a', 4), ('b', 1), ('b', 2), ('b', 3), ('b', 4), ('b', 5), ('b', 6), ('u', 1), ('z', 1)]
 * Last: [('u', 1), ('z', 1), ('¶', 1), ('b', 1), ('b', 2), ('b', 3), ('b', 4), ('a', 1), ('a', 2), ('a', 3), ('b', 5), ('b', 6), ('a', 4)]
 * Last-to-First: [11, 12, 0, 5, 6, 7, 8, 1, 2, 3, 9, 10, 4]


*bba* found in *abbazabbabbu¶* 2 times.
</div>

`{bm-enable-all}`

