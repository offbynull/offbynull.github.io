<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

Why is this the case? Remember that the `last` to `first` walk is just walking over the original sequence in reverse order. In the example above, it walks over "ana" in the sequence "banana¶".

```{svgbob}
"sequence:"  b1 a1 n1 a2 n2 a3 ¶1
                      |  |  |
                      a2 n2 a3
                      <-------
                    "walk direction"
```

`first_idx` holds on to every 3rd index of "banana¶", so the walk only needs to hop 2 times before reaching a `first_idx` entry that has a value.

```{svgbob}
"first_idx:" 0        3        6 
"sequence:"  b1 a1 n1 a2 n2 a3 ¶1
                      |  |  |
                      a2 n2 a3
                      <-------
                    "walk direction"
```

Regardless of where in "banana¶" the walk starts from, it will never take more than 2 hops until reaching a `first_idx` entry that has a value.
</div>

