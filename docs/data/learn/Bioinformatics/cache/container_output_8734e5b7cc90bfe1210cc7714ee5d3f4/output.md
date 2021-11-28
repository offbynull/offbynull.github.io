<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

BLOSUM80 was chosen because SARS-CoV-2 is a relatively new virus (~2 years). I don't know if it was a good choice because I've been told viruses mutate more rapidly, so maybe BLOSUM62 would have been a better choice.

The original NCBI dataset has 30k to 40k unique spike sequences. I couldn't justify sticking all of that into the git repo (too large) so I whittled it down to a random sample of 1000.

From that 1000, only a sample of 15 are selected to run the code. The problem is that sequence alignments are computationally expensive and Python is slow. Doing a sequence alignment between two spike protein sequences on my VM takes a long time (~4 seconds per alignment), so for the full 1000 sequences the total running time would end up being ~4 years (if I calculated it correctly - single core).
</div>

