<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

Note what's happening here. The assumption being made that the leaf nodes for the minimum distance matrix value are always neighbours. Not always true, but probably good enough as a starting point. For example, the following distance matrix and tree would identify v0 and v2 as neighbours when in fact they aren't ...

```{svgbob}
 a             b
  \           /
 1 \         / 1
    e ----- f
90 /    1    \ 90
  /           \
 d             c
```

|   | a  |  b  | c  |  d  |
|---|----|-----|----|-----|
| a | 0  | 91  | 3  | 92  |
| b | 91 | 0   | 92 | 181 |
| c | 3  | 92  | 0  | 91  |
| d | 92 | 181 | 91 | 0   |

It may be a good idea to use Algorithms/Distance Phylogeny/Find Neighbours_TOPIC to short circuit this restriction, possibly producing a better heuristic. But, the original algorithm doesn't call for it.
</div>

