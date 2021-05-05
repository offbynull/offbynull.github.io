<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

This was the version of the algorithm used to solve chapter 4's final assignment (sequence a real experimental spectrum for some unknown variant of Tyrocidine). Note how the parameters into sequence_peptide take an initial leaderboard. This initial leaderboard was primed with subpeptide sequences from other Tyrocidine variants discusses in chapter 4. The problem wasn't solvable without these subpeptide sequences. More information on this can be found in the Python file for the final assignment.

Before coming up with the above solution, I came up with another heuristic that I tried: Use basic genetic algorithms / evolutionary algorithms as the heuristic to move forward peptides. This performed even worse than leaderboard: If the mutation rate is too low, the candidates converge to a local optima and can't break out. If the mutation rate is too high, the candidates never converge to a solution. As such, it was removed from the code.
</div>

