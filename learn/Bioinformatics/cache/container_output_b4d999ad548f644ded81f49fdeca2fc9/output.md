<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

The k, score threshold, and scoring matrix (e.g. BLOSUM, PAM, Levenshtein distance, etc..) to be used depends on context / empirical analysis. Different sources say different things about good values. It sounds like, for ...

* proteins, k=5, scoring matrix is BLOSUM62, and scoring threshold is ???
* DNA, k=11, scoring matrix is +5 for match / -4 for mismatch or +2 for match / -3 for mismatch, and scoring threshold is ???

You need to play around with the numbers and find a set that does adequate filtering but still finds related sequences.
</div>

