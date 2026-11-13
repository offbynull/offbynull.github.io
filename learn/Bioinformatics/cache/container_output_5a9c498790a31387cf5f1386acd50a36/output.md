<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

The standard Levenshtein distance algorithm using a 2D array you remember from over a decade ago is this algorithm: Matrix-based global alignment where matches score 0 but mismatches and indels score -1. The final weight of the alignment is the minimum number of operations required to convert one sequence to another (e.g. swap, insert, delete) -- it'll be negative, ignore the sign.
</div>

