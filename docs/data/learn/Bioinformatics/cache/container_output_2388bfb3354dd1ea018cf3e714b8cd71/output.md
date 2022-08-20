<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

The first-last property is explained in detail in the subsection that describes the standard algorithm.

BWT matrices have historically been used by data compression algorithms to ...

 * find runs of similar substrings in the sequence (e.g. "ana" appears twice in "banana¶")
 * transform the sequence into a more compressible version of itself (e.g. last colum of BWT matrix above is "annb¶aa", which has more characters repeating one after the other compared to "banana¶", and is convertible back to "banana¶").

How "annb¶aa" is convertible back to "banana¶" is discussed further in the subsection that describes the standard algorithm. Specifically, the section on serialization / deserialization.

More information is also available in the [Wikipedia article](https://en.wikipedia.org/wiki/Burrows%E2%80%93Wheeler_transform).
</div>

