<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

The entire point of the suffix array is that it's just an array of pointers to the suffix in the source sequence. Since the pointers are sorted (sorted by the suffixes they point to), you can quickly find if a substring exists just by doing a binary search on the suffix array (if a substring exists, it must be a prefix of one of the suffixes).
</div>

