<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

When searching with mismatches, the string being searched may have to be padded. For example, searching GCCGTTT for GGCC with a mismatch tolerance of 1 should match the beginning.

```
-GCCGTTT-
GGCC
```

Pad each end by the mismatch tolerance count with some character you don't expect to encounter (dashes used in the example above).
</div>

