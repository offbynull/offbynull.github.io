<div style="border:1px solid black;">

`{bm-disable-all}`

Parser.py produced the following ...

```
Parse (4 * (6 + 1)) / 2 + 3 ...
    +(/(*(4, +(6, 1)), 2), 3)
Parse 5/2 + (-45/10)^-x + -(3 * 8) / -log(2, 32) ...
    +(+(/(5, 2), ^(/(-45, 10), *(-1, x))), /(*(-1, *(3, 8)), *(-1, log(2, 32))))
```

</div>

`{bm-enable-all}`

