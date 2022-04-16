<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

The Pevzner uses the formula `{kt} \lfloor \frac{n}{d+1} \rfloor` for determining the number of nucleotides per seed, where n is the sequence length and d is the number of mismatches. It's the same as the code above but it takes the floor rather than the ceiling. For example, ACGTT with 2 mismatches would break down to `{kt} \frac{5}{3}` = 1.667 nucleotides per seed, which rounds down to 1, which ends up being the seeds [A, C, GTT]. That seems like a not optimal breakup -- smaller seeds may end up with more frequent hits during search?

Maybe this has to do with the BLAST discussion that comes immediately after (section 9.14).
</div>

