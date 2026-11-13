<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

The Pevzner book says that if the sequences for known entities aren't the same length, common practice is to align them (e.g. multiple alignment) and remove any indels before continuing. Once indels are removed, the sequences will all become the same length.

```{svgbob}
"Step 1: Align and remove indels"

A C T T G - G T
A C T T G G C T
A T - T C G C C
✓ ✓ ✗ ✓ ✓ ✗ ✓ ✓
| |   | |   | |
| |   + +   + +
| |  / /   / / 
| | + +   / /
| | | |  / /
| | | | + +
| | | | | | 
A C T G G T 
A C T G C T 
A T T C C C 


"Step 2: Place new sequences into tree"

         .-----------.
         | AncestorA |
         |  ??????   |
         '-----+-----'
              / \
             /   \
            /     \
     .-----+-----. \
     | AncestorB |  \
     |  ??????   |   \
     '-----+-----'    \
          / \          \
         /   \          \
        /     \          \
.------+-. .---+----. .---+----.
|   Cat  | |  Lion  | |  Bear  |
| ACTGGT | | ACTGCT | | ATTCCC |
'--------' '--------' '--------'
```

I'm not sure why indels can't just be included as an option (e.g. A, C, T, G, and -)? There's probably a reason. Maybe because indels that happen in bursts are likely from genome rearrangement mutations instead of point mutations and including them muddies the waters? I don't know.
</div>

