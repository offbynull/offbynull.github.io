```{title}
Bioinformatics
```

```{toc}
```

# Introduction

Bioinformatics is the science of transforming and processing biological data to gain new insights, particularly omics data: genomics, proteomics, metabolomics, etc.. Bioinformatics is mostly a mix of biology, computer science, and statistics / data science.

# Algorithms

## K-mer

`{bm} /(Algorithms\/K-mer)_TOPIC/`

A k-mer is a subsequence of length k within some larger biological sequence (e.g. DNA or amino acid chain). For example, in the DNA sequence GAAATC, the following k-mer's exist:

| k | k-mers          |
|---|-----------------|
| 1 | G A A A T C     |
| 2 | GA AA AA AT TC  |
| 3 | GAA AAA AAT ATC |
| 4 | GAAA AAAT AATC  |
| 5 | GAAAT AAATC     |
| 6 | GAAATC          |

Common scenarios involving k-mers:

 * Search for an exact k-mer.
 * Search for an approximate k-mer (fuzzy search).
 * Find k-mers of interest in a sequence (e.g. repeating k-mers).

### Reverse Complement

`{bm} /(Algorithms\/K-mer\/Reverse Complement)_TOPIC/`

**WHAT**: Given a DNA k-mer, calculate its reverse complement.

**WHY**: Depending on the type of biological sequence, a k-mer may have one or more alternatives. For DNA sequences specifically, a k-mer of interest may have an alternate form. Since the DNA molecule comes as 2 strands, where ...
 * each strand's direction is opposite of the other,
 * each strand position has a nucleotide that complements the nucleotide at that same position on the other stand:
   * A ⟷ T
   * C ⟷ G

```{svgbob}
------------------------------>
  "A" "C" "T" "T" "C" "G" "C"
  |   |   |   |   |   |   |
  "T" "G" "A" "A" "G" "C" "G"
<------------------------------
```

, ... the reverse complement of that k-mer may be just as valid as the original k-mer. For example, if an enzyme is known to bind to a specific DNA k-mer, it's possible that it might also bind to the reverse complement of that k-mer.

**ALGORITHM**:

```{output}
ch1_code/src/ReverseComplementADnaKmer.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch1}
ReverseComplementADnaKmer
TAATCCG
```

### Hamming Distance

`{bm} /(Algorithms\/K-mer\/Hamming Distance)_TOPIC/`

**WHAT**: Given 2 k-mers, the hamming distance is the number of positional mismatches between them.

**WHY**: Imagine an enzyme that looks for a specific DNA k-mer pattern to bind to. Since DNA is known to mutate, it may be that enzyme can also bind to other k-mer patterns that are slight variations of the original. For example, that enzyme may be able to bind to both AAACTG and AAAGTG.

**ALGORITHM**:

```{output}
ch1_code/src/HammingDistanceBetweenKmers.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch1}
HammingDistanceBetweenKmers
ACTTTGTT
AGTTTCTT
```

### Hamming Distance Neighbourhood

`{bm} /(Algorithms\/K-mer\/Hamming Distance Neighbourhood)_TOPIC/`

```{prereq}
Algorithms/K-mer/Hamming Distance_TOPIC
```

**WHAT**: Given a source k-mer and a minimum hamming distance, find all k-mers such within the hamming distance of the source k-mer. In other words, find all k-mers such that `hamming_distance(source_kmer, kmer) <= min_distance`.

**WHY**: Imagine an enzyme that looks for a specific DNA k-mer pattern to bind to. Since DNA is known to mutate, it may be that enzyme can also bind to other k-mer patterns that are slight variations of the original. This algorithm finds all such variations.

**ALGORITHM**:

```{output}
ch1_code/src/FindAllDnaKmersWithinHammingDistance.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch1}
FindAllDnaKmersWithinHammingDistance
AAAA
1
```

### Find Locations

`{bm} /(Algorithms\/K-mer\/Find Locations)_TOPIC/`

```{prereq}
Algorithms/K-mer/Hamming Distance_TOPIC
Algorithms/K-mer/Reverse Complement_TOPIC
```

**WHAT**: Given a k-mer, find where that k-mer occurs in some larger sequence. The search may potentially include the k-mer's variants (e.g. reverse complement).

**WHY**: Imagine that you know of a specific k-mer pattern that serves some function in an organism. If you see that same k-mer pattern appearing in some other related organism, it could be a sign that k-mer pattern serves a similar function. For example, the same k-mer pattern could be used by 2 related types of bacteria as a DnaA box.

The enzyme that operates on that k-mer may also operate on its reverse complement as well as slight variations on that k-mer. For example, if an enzyme binds to AAAAAAAAA, it may also bind to its...
* reverse complement: TTTTTTTTT
* approximate variants: AAAAAAAAA, AAATAAAAA, AAAAAGAAA, ...
* approximate variants of its reverse complements: TTTTTTTTT, TTTTTTATT, TTCTTTTTT, ...

**ALGORITHM**:

```{output}
ch1_code/src/FindLocations.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch1}
FindLocations
AAAAGAACCTAATCTTAAAGGAGATGATGATTCTAA
AAAA
1
True
```

### Find Clumps

`{bm} /(Algorithms\/K-mer\/Find Clumps)_TOPIC/`

```{prereq}
Algorithms/K-mer/Find Locations_TOPIC
```

**WHAT**: Given a k-mer, find where that k-mer clusters in some larger sequence. The search may potentially include the k-mer's variants (e.g. reverse complement).

**WHY**: An enzyme may need to bind to a specific region of DNA to begin doing its job. That is, it looks for a specific k-mer pattern to bind to, where that k-mer represents the beginning of some larger DNA region that it operates on. Since DNA is known to mutate, often times you'll find multiple copies of the same k-mer pattern clustered together -- if one copy mutated to become unusable, the other copies are still around.

For example, the DnaA box is a special k-mer pattern used by enzymes during DNA replication. Since DNA is known to mutate, the DnaA box can be found repeating multiple times in the region of DNA known as the replication origin. Finding the DnaA box clustered in a small region is a good indicator that you've found the replication origin.

**ALGORITHM**:

```{output}
ch1_code/src/FindClumps.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch1}
FindClumps
GGGACTGAACAAACAAATTTGGGAGGGCACGGGTTAAAGGAGATGATGATTCAAAGGGT
GGG
3
13
1
True
```

### Find Repeating

`{bm} /(Algorithms\/K-mer\/Find Repeating)_TOPIC/`

```{prereq}
Algorithms/K-mer/Reverse Complement_TOPIC
Algorithms/K-mer/Hamming Distance Neighbourhood_TOPIC
```

**WHAT**: Given a sequence, find clusters of unique k-mers within that sequence. In other words, for each unique k-mer that exists in the sequence, see if it clusters in the sequence. The search may potentially include variants of k-mer variants (e.g. reverse complements of the k-mers).

**WHY**: An enzyme may need to bind to a specific region of DNA to begin doing its job. That is, it looks for a specific k-mer pattern to bind to, where that k-mer represents the beginning of some larger DNA region that it operates on. Since DNA is known to mutate, often times you'll find multiple copies of the same k-mer pattern clustered together -- if one copy mutated to become unusable, the other copies are still around.

For example, the DnaA box is a special k-mer pattern used by enzymes during DNA replication. Since DNA is known to mutate, the DnaA box can be found repeating multiple times in the region of DNA known as the replication origin. Given that you don't know the k-mer pattern for the DnaA box but you do know the replication origin, you can scan through the replication origin for repeating k-mer patterns. If a pattern is found to heavily repeat, it's a good candidate that it's the k-mer pattern for the DnaA box.

**ALGORITHM**:

```{output}
ch1_code/src/FindRepeating.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch1}
FindRepeating
GGGACTGAACAAACAAATTTGGGAGGGCACGGGTTAAAGGAGATGATGATTCAAAGGGT
5
1
True
```

### Find Repeating in Window

`{bm} /(Algorithms\/K-mer\/Find Repeating in Window)_TOPIC/`

```{prereq}
Algorithms/K-mer/Find Repeating_TOPIC
```

**WHAT**: Given a sequence, find regions within that sequence that contain clusters of unique k-mers. In other words, ...
 * slide a window over the cluster.
 * for each unique k-mer that exists in the window, see if it clusters in the sequence.
 
 The search may potentially include variants of k-mer variants (e.g. reverse complements of the k-mers).

**WHY**: An enzyme may need to bind to a specific region of DNA to begin doing its job. That is, it looks for a specific k-mer pattern to bind to, where that k-mer represents the beginning of some larger DNA region that it operates on. Since DNA is known to mutate, often times you'll find multiple copies of the same k-mer pattern clustered together -- if one copy mutated to become unusable, the other copies are still around.

For example, the DnaA box is a special k-mer pattern used by enzymes during DNA replication. Since DNA is known to mutate, the DnaA box can be found repeating multiple times in the region of DNA known as the replication origin. Given that you don't know the k-mer pattern for the DnaA box but you do know the replication origin, you can scan through the replication origin for repeating k-mer patterns. If a pattern is found to heavily repeat, it's a good candidate that it's the k-mer pattern for the DnaA box.

**ALGORITHM**:

```{output}
ch1_code/src/FindRepeatingInWindow.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch1}
FindRepeatingInWindow
TTTTTTTTTTTTTCCCTTTTTTTTTCCCTTTTTTTTTTTTT
9
6
20
1
True
```

### Probability of Appearance

`{bm} /(Algorithms\/K-mer\/Probability of Appearance)_TOPIC/`

```{prereq}
Algorithms/K-mer/Find Locations_TOPIC
```

**WHAT**: Given ...

* the length of a sequence (n)
* a k-mer
* a count (c)

... find the probability of that k-mer appearing at least c times within an arbitrary sequence of length n. For example, the probability that the 2-mer AA appears at least 2 times in a sequence of length 4:

* AAAA - yes
* AAAT - yes
* AAAC - yes
* AAAG - yes
* AATA - no
* AATT - no
* AATC - no
* AATG - no
* ...
* TAAA - yes
* ...
* CAAA - yes
* ...
* GAAA - yes
* ...
* GGGA - no
* GGGT - no
* GGGC - no
* GGGG - no

The probability is 7/256.

This isn't trivial to accurately compute because the occurrences of a k-mer within a sequence may overlap. For example, the number of times AA appears in AAAA is 3 while in CAAA it's 2.

**WHY**: When a k-mer is found within a sequence, knowing the probability of that k-mer being found within an arbitrary sequence of the same length hints at the significance of the find. For example, if some 10-mer has a 0.2 chance of appearing in an arbitrary sequence of length 50, that's too high of a chance to consider it a significant find -- 0.2 means 1 in 5 chance that the 10-mer just randomly happens to appear.

#### Bruteforce Algorithm

**ALGORITHM**:

This algorithm tries every possible combination of sequence to find the probability. It falls over once the length of the sequence extends into the double digits. It's intended to help conceptualize what's going on.

```{output}
ch1_code/src/BruteforceProbabilityOfKmerInArbitrarySequence.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch1}
BruteforceProbabilityOfKmerInArbitrarySequence
ACTG
8
```

#### Selection Estimate Algorithm

**ALGORITHM**:

```{note}
The explanation in the comments below are a bastardization of "1.13 Detour: Probabilities of Patterns in a String" in the Pevzner book...
```

This algorithm tries estimating the probability by ignoring the fact that the occurrences of a k-mer in a sequence may overlap. For example, searching for the 2-mer AA in the sequence AAAT yields 2 instances of AA:

 * \[AA\]AT
 * A\[AA\]T

If you go ahead and ignore overlaps, you can think of the k-mers occurring in a string as insertions. For example, imagine a sequence of length 7 and the 2-mer AA. If you were to inject 2 instances of AA into the sequence to get it to reach length 7, how would that look?

2 instances of a 2-mer is 4 characters has a length of 5. To get the sequence to end up with a length of 7 after the insertions, the sequence needs to start with a length of 3:

```
SSS
```

Given that you're changing reality to say that the instances WON'T overlap in the sequence, you can treat each instance of the 2-mer AA as a single entity being inserted. The number of ways that these 2 instances can be inserted into the sequence is 10:

```
I = insertion of AA, S = arbitrary sequence character

IISSS  ISISS  ISSIS  ISSSI
SIISS  SISIS  SISSI
SSIIS  SSISI
SSSII
```

Another way to think of the above insertions is that they aren't insertions. Rather, you have 5 items in total and you're selecting 2 of them. How many ways can you select 2 of those 5 items? 10.

The number of ways to insert can be counted via the "binomial coefficient": `bc(m, k) = m!/(k!(m-k)!)`, where m is the total number of items (5 in the example above) and k is the number of selections (2 in the example above). For the example above:

```
bc(5, 2) = 5!/(2!(5-2)!) = 10
```

Since the SSS can be any arbitrary nucleotide sequence of 3, count the number of different representations that are possible for SSS: `4^3 = 4*4*4 = 64` (4^3, 4 because a nucleotide can be one of ACTG, 3 because the length is 3). In each of these representations, the 2-mer AA can be inserted in 10 different ways:

```
64*10 = 640
```

Since the total length of the sequence is 7, count the number of different representations that are possible:

```
4^7 = 4*4*4*4*4*4*4 = 16384
```

The estimated probability is 640/16384. For...

* non-overlapping k-mers, the estimation will actually be relatively accurate.
* overlapping k-mers, the estimation won't be as accurate.

```{note}
Maybe try training a deep learning model to see if it can provide better estimates?
```

```{output}
ch1_code/src/EstimateProbabilityOfKmerInArbitrarySequence.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch1}
EstimateProbabilityOfKmerInArbitrarySequence
ACTG
8
```

## GC Skew

`{bm} /(Algorithms\/GC Skew)_TOPIC/`

**WHAT**: Given a sequence, create a counter and walk over the sequence. Whenever a ...

* G is encountered, increment the counter.
* C is encountered, decrement the counter.

**WHY**: Given the DNA sequence of an organism, some segments may have lower count of Gs vs Cs.

During replication, some segments of DNA stay single-stranded for a much longer time than other segments. Single-stranded DNA is 100 times more susceptible to mutations than double-stranded DNA. Specifically, in single-stranded DNA, C has a greater tendency to mutate to T. When that single-stranded DNA re-binds to a neighbouring strand, the positions of any nucleotides that mutated from C to T will change on the neighbouring strand from G to A.

```{note}
Recall that the reverse complements of ...
 * C is G
 * A is T

It mutated from C to T. Since its now T, its complement is A.
```

Plotting the skew shows roughly which segments of DNA stayed single-stranded for a longer period of time. That information hints at special / useful locations in the organism's DNA sequence (replication origin / replication terminus).

**ALGORITHM**:

```{output}
ch1_code/src/GCSkew.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch1}
GCSkew
CACGGGTGGTTTTGGGGGCCCCCC
```

## Motif

`{bm} /(Algorithms\/Motif)_TOPIC/`

```{prereq}
Algorithms/K-mer_TOPIC
```

A motif is a pattern that matches many different k-mers, where those matched k-mers have some shared biological significance. The pattern matches a fixed k where each position may have alternate forms. The simplest way to think of a motif is a regex pattern without quantifiers. For example, the regex `[AT]TT[GC]C` may match to ATTGC, ATTCC, TTTGC, and TTTCC.

A common scenario involving motifs is to search through a set of DNA sequences for an unknown motif: Given a set of sequences, it's suspected that each sequence contains a k-mer that matches some motif. But, that motif isn't known beforehand. Both the k-mers and the motif they match need to be found.

For example, each of the following sequences contains a k-mer that matches some motif:

| Sequences                 |
|---------------------------|
| ATTGTTACCATAACCTTATTGCTAG |
| ATTCCTTTAGGACCACCCCAAACCC |
| CCCCAGGAGGGAACCTTTGCACACA |
| TATATATTTCCCACCCCAAGGGGGG |

That motif is the one described above (`[AT]TT[GC]C`):

| Sequences                     |
|-------------------------------|
| ATTGTTACCATAACCTT**ATTGC**TAG |
| **ATTCC**TTTAGGACCACCCCAAACCC |
| CCCCAGGAGGGAACC**TTTGC**ACACA |
| TATATA**TTTCC**CACCCCAAGGGGGG |

A motif matrix is a matrix of k-mers where each k-mer matches a motif. In the example sequences above, the motif matrix would be:

|0|1|2|3|4|
|-|-|-|-|-|
|A|T|T|G|C|
|A|T|T|C|C|
|T|T|T|G|C|
|T|T|T|C|C|

A k-mer that matches a motif may be referred to as a motif member.

### Consensus String

`{bm} /(Algorithms\/Motif\/Consensus String)_TOPIC/`

**WHAT**: Given a motif matrix, generate a k-mer where each position is the nucleotide most abundant at that column of the matrix.

**WHY**: Given a set of k-mers that are suspected to be part of a motif (motif matrix), the k-mer generated by selecting the most abundant column at each index is the "ideal" k-mer for the motif. It's a concise way of describing the motif, especially if the columns in the motif matrix are highly conserved.

**ALGORITHM**:

```{note}
It may be more appropriate to use a hybrid alphabet when representing consensus string because alternate nucleotides could be represented as a single letter. The Pevzner book doesn't mention this specifically but multiple online sources discuss it.
```

```{output}
ch2_code/src/ConsensusString.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch2}
ConsensusString
ATTGC
ATTCC
TTTGC
TTTCC
TTTCA
```

### Motif Matrix Count

`{bm} /(Algorithms\/Motif\/Motif Matrix Count)_TOPIC/`

**WHAT**: Given a motif matrix, count how many of each nucleotide are in each column.

**WHY**: Having a count of the number of nucleotides in each column is a basic statistic that gets used further down the line for tasks such as scoring a motif matrix.

**ALGORITHM**:

```{output}
ch2_code/src/MotifMatrixCount.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch2}
MotifMatrixCount
ATTGC
TTTGC
TTTGG
ATTGC
```

### Motif Matrix Profile

`{bm} /(Algorithms\/Motif\/Motif Matrix Profile)_TOPIC/`

```{prereq}
Algorithms/Motif/Motif Matrix Count_TOPIC
```

**WHAT**: Given a motif matrix, for each column calculate how often A, C, G, and T occur as percentages.

**WHY**: The percentages for each column represent a probability distribution for that column. For example, in column 1 of...

|0|1|2|3|4|
|-|-|-|-|-|
|A|T|T|C|G|
|C|T|T|C|G|
|T|T|T|C|G|
|T|T|T|T|G|

* A appears 25% of the time.
* C appears 25% of the time.
* T appears 50% of the time.
* G appears 0% of the time.

These probability distributions can be used further down the line for tasks such as determining the probability that some arbitrary k-mer conforms to the same motif matrix.

**ALGORITHM**:

```{output}
ch2_code/src/MotifMatrixProfile.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch2}
MotifMatrixProfile
ATTCG
CTTCG
TTTCG
TTTTG
```

### Motif Matrix Score

`{bm} /(Algorithms\/Motif\/Motif Matrix Score)_TOPIC/`

**WHAT**: Given a motif matrix, assign it a score based on how similar the k-mers that make up the matrix are to each other. Specifically, how conserved the nucleotides at each column are.

**WHY**: Given a set of k-mers that are suspected to be part of a motif (motif matrix), the more similar those k-mers are to each other the more likely it is that those k-mers are member_MOTIFs of the same motif. This seems to be the case for many enzymes that bind to DNA based on a motif (e.g. transcription factors).

#### Popularity Algorithm

**ALGORITHM**:

This algorithm scores a motif matrix by summing up the number of unpopular items in a column. For example, imagine a column has 7 Ts, 2 Cs, and 1A. The Ts are the most popular (7 items), meaning that the 3 items (2 Cs and 1 A) are unpopular -- the score for the column is 3.

Sum up each of the column scores to the get the final score for the motif matrix. A lower score is better.

```{output}
ch2_code/src/ScoreMotif.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch2}
ScoreMotif
ATTGC
TTTGC
TTTGG
ATTGC
```

#### Entropy Algorithm

`{bm} /(Algorithms\/Motif\/Motif Matrix Score\/Entropy Algorithm)_TOPIC/`

```{prereq}
Algorithms/Motif/Motif Matrix Profile_TOPIC
```

**ALGORITHM**:

This algorithm scores a motif matrix by calculating the entropy of each column in the motif matrix. Entropy is defined as the level of uncertainty for some variable. The more uncertain the nucleotides are in the column of a motif matrix, the higher (worse) the score. For example, given a motif matrix with 10 rows, a column with ...

 * 10 A nucleotides has low entropy because it's highly conserved,
 * 6 A and 4 T nucleotides has a higher entropy because it's less highly conserved.

Sum the output for each column to get the final score for the motif matrix. A lower score is better.

```{output}
ch2_code/src/ScoreMotifUsingEntropy.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch2}
ScoreMotifUsingEntropy
ATTGC
TTTGC
TTTGG
ATTGC
```

#### Relative Entropy Algorithm

```{prereq}
Algorithms/Motif/Motif Matrix Score/Entropy Algorithm_TOPIC
```

**ALGORITHM**:

This algorithm scores a motif matrix by calculating the entropy of each column relative to the overall nucleotide distribution of the sequences from which each motif member came from. This is important when finding motif members across a set of sequences. For example, the following sequences have a nucleotide distribution highly skewed towards C...

| Sequences                 |
|---------------------------|
| CCCCCCCCCCCCCCCCCATTGCCCC |
| ATTCCCCCCCCCCCCCCCCCCCCCC |
| CCCCCCCCCCCCCCCTTTGCCCCCC |
| CCCCCCTTTCTCCCCCCCCCCCCCC |

Given the sequences in the example above, of all motif matrices possible for k=5, basic entropy scoring will always lead to a matrix filled with Cs:

|0|1|2|3|4|
|-|-|-|-|-|
|C|C|C|C|C|
|C|C|C|C|C|
|C|C|C|C|C|
|C|C|C|C|C|

Even though the above motif matrix scores perfect, it's likely junk. Member_MOTIFs containing all Cs score better because the sequences they come from are biased (saturated with Cs), not because they share some higher biological significance.

To reduce bias, the nucleotide distributions from which the member_MOTIFs came from need to be factored in to the entropy calculation: relative entropy.

```{output}
ch2_code/src/ScoreMotifUsingRelativeEntropy.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{note}
In the outputs below, the score in the second output should be less than (better) the score in the first output.
```

```{ch2}
ScoreMotifUsingRelativeEntropy
CCCCC
CCCCC
CCCCC
CCCCC
CCCCCCCCCCCCCCCCCATTGCCCC
ATTCCCCCCCCCCCCCCCCCCCCCC
CCCCCCCCCCCCCCCTTTGCCCCCC
CCCCCCTTTCTCCCCCCCCCCCCCC
```

```{ch2}
ScoreMotifUsingRelativeEntropy
ATTGC
ATTCC
CTTTG
TTTCT
CCCCCCCCCCCCCCCCCATTGCCCC
ATTCCCCCCCCCCCCCCCCCCCCCC
CCCCCCCCCCCCCCCTTTGCCCCCC
CCCCCCTTTCTCCCCCCCCCCCCCC
```

### Motif Logo

`{bm} /(Algorithms\/Motif\/Motif Logo)_TOPIC/`

```{prereq}
Algorithms/Motif/Motif Matrix Score/Entropy Algorithm_TOPIC
```

**WHAT**: Given a motif matrix, generate a graphical representation showing how conserved the motif is. Each position has its possible nucleotides stacked on top of each other, where the height of each nucleotide is based on how conserved it is. The more conserved a position is, the taller that column will be. This type of graphical representation is called a sequence logo.

**WHY**: A sequence logo helps more quickly convey the characteristics of the motif matrix it's for.

**ALGORITHM**:

For this particular logo implementation, a lower entropy results in a taller overall column.

```{output}
ch2_code/src/MotifLogo.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch2}
MotifLogo
TCGGGGGTTTTT
CCGGTGACTTAC
ACGGGGATTTTC
TTGGGGACTTTT
AAGGGGACTTCC
TTGGGGACTTCC
TCGGGGATTCAT
TCGGGGATTCCT
TAGGGGAACTAC
TCGGGTATAACC
```

### K-mer Match Probability

`{bm} /(Algorithms\/Motif\/K-mer Match Probability)_TOPIC/`

```{prereq}
Algorithms/Motif/Motif Matrix Count_TOPIC
Algorithms/Motif/Motif Matrix Profile_TOPIC
Algorithms/K-mer_TOPIC
```

**WHAT**: Given a motif matrix and a k-mer, calculate the probability of that k-mer being a member_MOTIF of that motif.

**WHY**: Being able to determine if a k-mer is potentially a member_MOTIF of a motif can help speed up experiments. For example, imagine that you suspect 21 different genes of being regulated by the same transcription factor. You isolate the transcription factor binding site for 6 of those genes and use their sequences as the underlying k-mers for a motif matrix. That motif matrix doesn't represent the transcription factor's motif exactly, but it's close enough that you can use it to scan through the k-mers in the remaining 15 genes and calculate the probability of them being member_MOTIFs of the same motif.

If a k-mer exists such that it conforms to the motif matrix with a high probability, it likely is a member_MOTIF of the motif.

**ALGORITHM**:

Imagine the following motif matrix:

| 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| A | T | G | C | A | C |
| A | T | G | C | A | C |
| A | T | C | C | A | C |
| A | T | C | C | A | C |

Calculating the counts for that motif matrix results in:

|   | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| A | 4 | 0 | 0 | 0 | 4 | 0 |
| C | 0 | 0 | 2 | 4 | 0 | 4 |
| T | 0 | 4 | 0 | 0 | 0 | 0 |
| G | 0 | 0 | 2 | 0 | 0 | 0 |

Calculating the profile from those counts results in:

|   | 0 | 1 |  2  | 3 | 4 | 5 |
|---|---|---|-----|---|---|---|
| A | 1 | 0 | 0   | 0 | 1 | 0 |
| C | 0 | 0 | 0.5 | 1 | 0 | 1 |
| T | 0 | 1 | 0   | 0 | 0 | 0 |
| G | 0 | 0 | 0.5 | 0 | 0 | 0 |

Using this profile, the probability that a k-mer conforms to the motif matrix is calculated by mapping the nucleotide at each position of the k-mer to the corresponding nucleotide in the corresponding position of the profile and multiplying them together. For example, the probability that the k-mer...

 * ATGCAC conforms to the example profile above is calculated as 1\*1\*0.5\*1\*1\*1 = 0.5
 * TTGCAC conforms to the example profile above is calculated as 0\*1\*0.5\*1\*1\*1 = 0

Of the these two k-mers, ...

 * all positions in the first (ATGCAC) have been seen before in the motif matrix.
 * all but one position in the second (TTGCAC) have been seen before in the motif matrix (index 0).

Both of these k-mers should have a reasonable probability of being member_MOTIFs of the motif. However, notice how the second k-mer ends up with a 0 probability. The reason has to do with the underlying concept behind motif matrices: the entire point of a motif matrix is to use the known member_MOTIFs of a motif to find other potential member_MOTIFs of that same motif. The second k-mer contains a T at index 0, but none of the known member_MOTIFs of the motif have a T at that index. As such, its probability gets reduced to 0 even though the rest of the k-mer conforms.

Cromwell's rule says that when a probability is based off past events, a hard 0 or 1 values shouldn't be used. As such, a quick workaround to the 0% probability problem described above is to artificially inflate the counts that lead to the profile such that no count is 0 (pseudocounts). For example, for the same motif matrix, incrementing the counts by 1 results in:

|   | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| A | 5 | 1 | 1 | 1 | 5 | 1 |
| C | 1 | 1 | 3 | 5 | 1 | 5 |
| T | 1 | 5 | 1 | 1 | 1 | 1 |
| G | 1 | 1 | 3 | 1 | 1 | 1 |

Calculating the profile from those inflated counts results in:

|   |   0   |   1   |   2   |   3   |   4   |   5   |
|---|-------|-------|-------|-------|-------|-------|
| A | 0.625 | 0.125 | 0.125 | 0.125 | 0.625 | 0.125 |
| C | 0.125 | 0.125 | 0.375 | 0.625 | 0.125 | 0.625 |
| T | 0.125 | 0.625 | 0.125 | 0.125 | 0.125 | 0.125 |
| G | 0.125 | 0.125 | 0.375 | 0.125 | 0.125 | 0.125 |

Using this new profile, the probability that the previous k-mers conform are:

 * ATGCAC is calculated as 0.625\*0.625\*0.325\*0.625\*0.625\*0.625 = 0.031
 * TTGCAC is calculated as 0.125\*0.625\*0.325\*0.625\*0.625\*0.625 = 0.0062

Although the probabilities seem low, it's all relative. The probability calculated for the first k-mer (ATGCAC) is the highest probability possible -- each position in the k-mer maps to the highest probability nucleotide of the corresponding position of the profile.

```{output}
ch2_code/src/FindMostProbableKmerUsingProfileMatrix.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch2}
FindMostProbableKmerUsingProfileMatrix
ATGCAC
ATGCAC
ATCCAC
ATCCAC
TTGCAC
```

### Find Motif Matrix

`{bm} /(Algorithms\/Motif\/Find Motif Matrix)_TOPIC/`

```{prereq}
Algorithms/Motif/K-mer Match Probability_TOPIC
```

**WHAT**: Given a set of sequences, find k-mers in those sequences that may be member_MOTIFs of the same motif.

**WHY**: A transcription factor is an enzyme that either increases or decreases a gene's transcription rate. It does so by binding to a specific part of the gene's upstream region called the transcription factor binding site. That transcription factor binding site consists of a k-mer that matches the motif expected by that transcription factor, called a regulatory motif. 

A single transcription factor may operate on many different genes. Often times a scientist will identify a set of genes that are suspected to be regulated by a single transcription factor, but that scientist won't know ...

* what the regulatory motif is (the pattern expected by the enzyme).
* where the transcription factor binding sites are (which k-mers the enzyme is targeting).
* how long the transcription factor binding sites are (which k the enzyme is targeting).

The regulatory motif expected by a transcription factor typically expects k-mers that have the same length and are similar to each other (short hamming distance). As such, potential motif candidates can be derived by finding k-mers across the set of sequences that are similar to each other.

#### Bruteforce Algorithm

```{prereq}
Algorithms/K-mer/Hamming Distance Neighbourhood_TOPIC
Algorithms/Motif/Motif Matrix Score_TOPIC
```

**ALGORITHM**:

This algorithm scans over all k-mers in a set of DNA sequences, enumerates the hamming distance neighbourhood of each k-mer, and uses the k-mers from the hamming distance neighbourhood to build out possible motif matrices. Of all the motif matrices built, it selects the one with the lowest score.

Neither k nor the mismatches allowed by the motif is known. As such, the algorithm may need to be repeated multiple times with different value combinations.

Even for trivial inputs, this algorithm falls over very quickly. It's intended to help conceptualize the problem of motif finding.

```{output}
ch2_code/src/ExhaustiveMotifMatrixSearch.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch2}
ExhaustiveMotifMatrixSearch
5
1
ataaagggata
acagaaatgat
tgaaataacct
```

#### Median String Algorithm

```{prereq}
Algorithms/Motif/Consensus String_TOPIC
Algorithms/Motif/Motif Matrix Score_TOPIC
Algorithms/K-mer/Hamming Distance_TOPIC
```

**ALGORITHM**:

This algorithm takes advantage of the fact that the same score can be derived by scoring a motif matrix either row-by-row or column-by-column. For example, the score for the following motif matrix is 3...

|       | 0 | 1 |   2   | 3 |   4   | 5 |   |
|-------|---|---|-------|---|-------|---|---|
|       | A | T | **G** | C |   A   | C |   |
|       | A | T | **G** | C |   A   | C |   |
|       | A | T |   C   | C | **T** | C |   |
|       | A | T |   C   | C |   A   | C |   |
| Score | 0 | 0 |   2   | 0 |   1   | 0 | 3 |

For each column, the number of unpopular nucleotides is counted. Then, those counts are summed to get the score: 0 + 0 + 2 + 0 + 1 + 0 = 3. 

That exact same score scan be calculated by working through the motif matrix row-by-row...

| 0 | 1 |   2   | 3 |   4   | 5 | Score |
|---|---|-------|---|-------|---|-------|
| A | T | **G** | C |   A   | C |   1   |
| A | T | **G** | C |   A   | C |   1   |
| A | T |   C   | C | **T** | C |   1   |
| A | T |   C   | C |   A   | C |   0   |
|   |   |       |   |       |   |   3   |

For each row, the number of unpopular nucleotides is counted. Then, those counts are summed to get the score: 1 + 1 + 1 + 0 = 3.

|       | 0 | 1 |   2   | 3 |   4   | 5 | Score |
|-------|---|---|-------|---|-------|---|-------|
|       | A | T | **G** | C |   A   | C |   1   |
|       | A | T | **G** | C |   A   | C |   1   |
|       | A | T |   C   | C | **T** | C |   1   |
|       | A | T |   C   | C |   A   | C |   0   |
| Score | 0 | 0 |   2   | 0 |   1   | 0 |   3   |

Notice how each row's score is equivalent to the hamming distance between the k-mer at that row and the motif matrix's consensus string. Specifically, the consensus string for the motif matrix is ATCCAC. For each row, ...

 * hamming_distance(ATGCAC, ATCCAC) = 1
 * hamming_distance(ATGCAC, ATCCAC) = 1
 * hamming_distance(ATCCTC, ATCCAC) = 1
 * hamming_distance(ATCCAC, ATCCAC) = 0

Given these facts, this algorithm constructs a set of consensus strings by enumerating through all possible k-mers for some k. Then, for each consensus string, it scans over each sequence to find the k-mer that minimizes the hamming distance for that consensus string. These k-mers are used as the member_MOTIFs of a motif matrix.

Of all the motif matrices built, the one with the lowest score is selected.

Since the k for the motif is unknown, this algorithm may need to be repeated multiple times with different k values. This algorithm also doesn't scale very well. For k=10, 1048576 different consensus strings are possible.

```{output}
ch2_code/src/MedianStringSearch.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch2}
MedianStringSearch
3
AAATTGACGCAT
GACGACCACGTT
CGTCAGCGCCTG
GCTGAGCACCGG
AGTTCGGGACAG
```

#### Greedy Algorithm

```{prereq}
Algorithms/Motif/Motif Matrix Score_TOPIC
Algorithms/Motif/K-mer Match Probability_TOPIC
```

**ALGORITHM**:

This algorithm begins by constructing a motif matrix where the only member_MOTIF is a k-mer picked from the first sequence. From there, it goes through the k-mers in the ...

 1. second sequence to find the one that has the highest match probability to the motif matrix and adds it as a member_MOTIF to the motif matrix.
 2. third sequence to find the one that has the highest match probability to the motif matrix and adds it as a member_MOTIF to the motif matrix.
 3. fourth sequence to find the one that has the highest match probability to the motif matrix and adds it as a member_MOTIF to the motif matrix.
 4. ...

This process repeats once for every k-mer in the first sequence. Each repetition produces a motif matrix. Of all the motif matrices built, the one with the lowest score is selected.

This is a greedy algorithm. It builds out potential motif matrices by selecting the locally optimal k-mer from each sequence. While this may not lead to the globally optimal motif matrix, it's fast and has a higher than normal likelihood of picking out the correct motif matrix.

```{output}
ch2_code/src/GreedyMotifMatrixSearchWithPsuedocounts.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch2}
GreedyMotifMatrixSearchWithPsuedocounts
3
AAATTGACGCAT
GACGACCACGTT
CGTCAGCGCCTG
GCTGAGCACCGG
AGTTCGGGACAG
```

#### Randomized Algorithm

`{bm} /(Algorithms\/Motif\/Find Motif Matrix\/Randomized Algorithm)_TOPIC/`

```{prereq}
Algorithms/Motif/Motif Matrix Score_TOPIC
Algorithms/Motif/Motif Matrix Profile_TOPIC
Algorithms/Motif/K-mer Match Probability_TOPIC
```

**ALGORITHM**:

This algorithm selects a random k-mer from each sequence to form an initial motif matrix. Then, for each sequence, it finds the k-mer that has the highest probability of matching that motif matrix. Those k-mers form the member_MOTIFs of a new motif matrix. If the new motif matrix scores better than the existing motif matrix, the existing motif matrix gets replaced with the new motif matrix and the process repeats. Otherwise, the existing motif matrix is selected.

In theory, this algorithm works because all k-mers in a sequence other than the motif member are considered to be random noise. As such, if no motif members were selected when creating the initial motif matrix, the profile of that initial motif matrix would be more or less uniform:

|   |   0  |   1  |   2  |   3  |   4  |   5  |
|---|------|------|------|------|------|------|
| A | 0.25 | 0.25 | 0.25 | 0.25 | 0.25 | 0.25 |
| C | 0.25 | 0.25 | 0.25 | 0.25 | 0.25 | 0.25 |
| T | 0.25 | 0.25 | 0.25 | 0.25 | 0.25 | 0.25 |
| G | 0.25 | 0.25 | 0.25 | 0.25 | 0.25 | 0.25 |

Such a profile wouldn't allow for converging to a vastly better scoring motif matrix.

However, if at least one motif member were selected when creating the initial motif matrix, the profile of that initial motif matrix would skew towards the motif:

|   |     0     |     1     |     2     |     3     |     4     |     5     |
|---|-----------|-----------|-----------|-----------|-----------|-----------|
| A | **0.333** |   0.233   |   0.233   |   0.233   | **0.333** |   0.233   |
| C |   0.233   |   0.233   | **0.333** | **0.333** |   0.233   | **0.333** |
| T |   0.233   | **0.333** |   0.233   |   0.233   |   0.233   |   0.233   |
| G |   0.233   |   0.233   |   0.233   |   0.233   |   0.233   |   0.233   |

Such a profile would lead to a better scoring motif matrix where that better scoring motif matrix contains the other member_MOTIFs of the motif.

In practice, this algorithm may trip up on real-world data. Real-world sequences don't actually contain random noise. The hope is that the only k-mers that are highly similar to each other in the sequences are member_MOTIFs of the motif. It's possible that the sequences contain other sets of k-mers that are similar to each other but vastly different than the motif members. In such cases, even if a motif member were to be selected when creating the initial motif matrix, the algorithm may converge to a motif matrix that isn't for the motif.

This is a monte carlo algorithm. It uses randomness to deliver an approximate solution. While this may not lead to the globally optimal motif matrix, it's fast and as such can be run multiple times. The run with the best motif matrix will likely be a good enough solution (it captures most of the motif members, or parts of the motif members if k was too small, or etc..).

```{output}
ch2_code/src/RandomizedMotifMatrixSearchWithPsuedocounts.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch2}
RandomizedMotifMatrixSearchWithPsuedocounts
1000
3
AAATTGACGCAT
GACGACCACGTT
CGTCAGCGCCTG
GCTGAGCACCGG
AGTTCGGGACAG
```

#### Gibbs Sampling Algorithm

```{prereq}
Algorithms/Motif/Motif Matrix Score_TOPIC
Algorithms/Motif/K-mer Match Probability_TOPIC
Algorithms/Motif/Find Motif Matrix/Randomized Algorithm_TOPIC
```

**ALGORITHM**:

```{note}
The Pevzner book mentions there's more to Gibbs Sampling than what it discussed. I looked up the topic but couldn't make much sense of it.
```

This algorithm selects a random k-mer from each sequence to form an initial motif matrix. Then, one of the k-mers from the motif matrix is randomly chosen and replaced with another k-mer from the same sequence that the removed k-mer came from. The replacement is selected by using a weighted random number algorithm, where how likely a k-mer is to be chosen as a replacement has to do with how probable of a match it is to the motif matrix.

This process of replacement is repeated for some user-defined number of cycles, at which point the algorithm has hopefully homed in on the desired motif matrix.

This is a monte carlo algorithm. It uses randomness to deliver an approximate solution. While this may not lead to the globally optimal motif matrix, it's fast and as such can be run multiple times. The run with the best motif matrix will likely be a good enough solution (it captures most of the motif members, or parts of the motif members if k was too small, or etc..).

The idea behind this algorithm is similar to the idea behind the randomized algorithm for motif matrix finding, except that this algorithm is more conservative in how it converges on a motif matrix and the weighted random selection allows it to potentially break out if stuck in a local optima.

```{output}
ch2_code/src/GibbsSamplerMotifMatrixSearchWithPsuedocounts.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch2}
GibbsSamplerMotifMatrixSearchWithPsuedocounts
1000
3
AAATTGACGCAT
GACGACCACGTT
CGTCAGCGCCTG
GCTGAGCACCGG
AGTTCGGGACAG
```

### Motif Matrix Hybrid Alphabet

`{bm} /(Algorithms\/Motif\/Motif Matrix Hybrid Alphabet)_TOPIC/`

```{prereq}
Algorithms/Motif/Consensus String_TOPIC
Algorithms/Motif/Motif Matrix Score_TOPIC
Algorithms/Motif/Find Motif Matrix_TOPIC
```

**WHAT**: When creating finding a motif, it may be beneficial to use a hybrid alphabet rather than the standard nucleotides (A, C, T, and G). For example, the following hybrid alphabet marks certain combinations of nucleotides as a single letter:

 * A = A
 * C = C
 * T = T
 * G = G
 * W = A or T
 * S = G or C
 * K = G or T
 * Y = C or T

```{note}
The alphabet above was pulled from the Pevzner book section 2.16: Complications in Motif Finding. It's a subset of the IUPAC nucleotide codes alphabet. The author didn't mention if the alphabet was explicitly chosen for regulatory motif finding. If it was, it may have been derived from running probabilities over already discovered regulatory motifs: e.g. for the motifs already discovered, if a position has 2 possible nucleotides then G/C (S), G/T (K), C/T (Y), and A/T (W) are likely but other combinations aren't.
```

**WHY**: Hybrid alphabets may make it easier for motif finding algorithms to converge on a motif. For example, when scoring a motif matrix, treat the position as a single letter if the distinct nucleotides at that position map to one of the combinations in the hybrid alphabet.

Hybrid alphabets may make more sense for representing a consensus string. Rather than picking out the most popular nucleotide, the hybrid alphabet can be used to describe alternating nucleotides at each position.

**ALGORITHM**:

```{output}
ch2_code/src/HybridAlphabetMatrix.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch2}
HybridAlphabetMatrix
CATCCG
CTTCCT
CATCTT
```

## Assembly

`{bm} /(Algorithms\/Assembly)_TOPIC/`

```{prereq}
Algorithms/K-mer_TOPIC
```

DNA sequencers work by taking many copies of an organism's genome, breaking up those copies into fragment_NORMs, then scanning in those fragment_NORMs. Sequencers typically scan fragment_NORMs in 1 of 2 ways:

 * read_SEQs - small DNA fragment_NORMs of equal size (represented as k-mers).

   ```{svgbob}
   A -> A -> A -> C -> C -> G -> A -> A -> A -> C
   ```

 * read-pairs - small DNA fragment_NORMs of equal size where the bases in the middle part of the fragment_NORM aren't known (represented as kd-mers).

   ```{svgbob}
   A -> C -> A -> ? -> ? -> ? -> ? -> ? -> ? -> ? -> ? -> ? -> ? -> ? -> ? -> ? -> ? -> ? -> ? -> T -> G -> C

   "* First and last k=3 bases are known."
   "* Middle d=16 bases aren't known."
   ```

Assembly is the process of reconstructing an organism's genome from the fragment_SEQs returned by a sequencer. Since the sequencer breaks up many copies of the same genome and each fragment_SEQ's start position is random, the original genome can be reconstructed by finding overlaps between fragment_SEQs and stitching them back together.

```{svgbob}
              "DNA reads"                               "Stitched DNA reads"
 
    +-------------+                                  
 A C|T A A G A A C|C T A A T T T A G C  -----+
    +-------------+                          |                                                 
+-------------+                              \                                                 
|A C T A A G A|A C C T A A T T T A G C  ------]-+   A C T A A G A A C C T A A T T T A G C
+-------------+                              /  |   
                        +-------------+      |  +-> A C T A A G A                            
 A C T A A G A A C C T A|A T T T A G C| --+  |        C T A A G A A <----------------------------+
                        +-------------+   |  +--------> T A A G A A C                            |
        +-------------+                   \             +-> A G A A C C T                        |
 A C T A|A G A A C C T|A A T T T A G C  ---]------------+   +-> A A C C T A A                    |
        +-------------+                   /                 |         C T A A T T T <----------+ \
            +-------------+               \                 |             A A T T T A G <-------]-]-+
 A C T A A G|A A C C T A A|T T T A G C  ---]----------------+               A T T T A G C <--+ / /  |
            +-------------+               /                                                  | | |  |
                  +-------------+        +---------------------------------------------------+ | |  |
 A C T A A G A A C|C T A A T T T|A G C  -------------------------------------------------------+ |  |
                  +-------------+                                                                |  |
  +-------------+                                                                                |  |
 A|C T A A G A A|C C T A A T T T A G C  ---------------------------------------------------------+  |
  +-------------+                                                                                   |
                      +-------------+                                                               |
 A C T A A G A A C C T|A A T T T A G|C  ------------------------------------------------------------+
                      +-------------+                                                          
```

A typical problem with sequencing is that the number of errors in a fragment_SEQ increase as the number of scanned bases increases. As such, read-pairs are preferred over read_SEQs: by only scanning in the head and tail of a long fragment_SEQ, the scan won't contain as many errors as a read_SEQ of the same length but will still contain extra information which helps with assembly (length of unknown nucleotides in between the prefix and suffix).

Assembly has many practical complications that prevent full genome reconstruction from fragment_SEQs:

 * Which strand of double stranded DNA that a read_SEQ / read-pair comes from isn't known, which means the overlaps you find may not be accurate.

   ```{svgbob}
          "DNA reads"           "Stitched DNA reads"
       
       +-------+                             
    T T|T A A A| -------+        T A A A T T T
       +-------+        |                    
   +-------+            +------> T A A A      
   |A A A T|T T  ----------------> A A A T    
   +-------+            +------------> A T T T
       +-------+        |      
    A A|A T T T| -------+                     
       +-------+                                
    "* 1st is the reverse complement of the 2nd and 3rd."
   ```

 * The fragment_SEQs may not cover the entire genome, which prevents full reconstruction.

   ```{svgbob}
          "DNA reads"        "Stitched DNA reads"

    +-------+                  A A T T T         
   G|A A T T|T ---------+
    +-------+           +----> A A T T  
      +-------+        +-------> A T T T
   G A|A T T T| -------+                 
      +-------+                            

   "* Starting G wasn't captured."
   ```

 * The fragment_SEQs may have errors (e.g. wrong nucleotides scanned in), which may prevent finding overlaps.

   ```{svgbob}
          "DNA reads"          "Stitched DNA reads"
      
       +-------+                               
    T A|A A A T| ------+        A A A T T T A             
       +-------+       |                                   
   +-------+           +------> A A A T      
   |A T T T|T A  -----------------> A T T T  
   +-------+           +------------> T T T A
       +-------+       |      
    A T|T T T A| ------+                   
       +-------+                               

   "* 1st is the reverse complement of the 2nd and 3rd."
   "* Reconstructed genome has an extra T prepended."
   ```

 * The fragment_SEQs for repetitive parts of the genome (e.g. transposons) likely can't be accurately assembled.

   ```{svgbob}
          "DNA reads"        "Stitched DNA reads"
      
   +-------+                      T A T A
   |T A T A|T A  ---------+ 
   +-------+              +-----> T A T A
       +-------+           +----> T A T A
    T A|T A T A| ----------+
       +-------+

   "* Wrong overlap identified."
   ```

### Stitch Reads

`{bm} /(Algorithms\/Assembly\/Stitch Reads)_TOPIC/`

**WHAT**: Given a list of overlapping read_SEQs where ...

 * all read_SEQs are of the same k,
 * all overlap regions are of the same length,
 * and each read_SEQ in the list overlaps with the next read_SEQ in the list

... , stitch them together. For example, in the read_SEQ list [GAAA, AAAT, AATC] each read_SEQ overlaps the subsequent read_SEQ by an offset of 1: GAAATC.

|          | 0 | 1 | 2 | 3 | 4 | 5 |
|----------|---|---|---|---|---|---|
| R1       | G | A | A | A |   |   |
| R2       |   | A | A | A | T |   |
| R3       |   |   | A | A | T | C |
| Stitched | G | A | A | A | T | C |

**WHY**: Since the sequencer breaks up many copies of the same DNA and each read_SEQ's start position is random, larger parts of the original DNA can be reconstructed by finding overlaps between fragment_SEQs and stitching them back together.

**ALGORITHM**:

```{output}
ch3_code/src/Read.py
python
# MARKDOWN_MERGE_OVERLAPPING\s*\n([\s\S]+)\n\s*# MARKDOWN_MERGE_OVERLAPPING
```

```{ch3}
Read
stitch
GAAA
AAAT
AATC
```

### Stitch Read-Pairs

`{bm} /(Algorithms\/Assembly\/Stitch Read-Pairs)_TOPIC/`

```{prereq}
Algorithms/Assembly/Stitch Reads_TOPIC
```

**WHAT**: Given a list of overlapping read-pairs where ...

 * all read-pairs are of the same k and d,
 * all overlap regions are of the same length,
 * and each read-pair in the list overlaps with the next read-pair in the list

... , stitch them together. For example, in the read-pair list [ATG---CCG, TGT---CGT, GTT---GTT, TTA---TTC] each read-pair overlaps the subsequent read-pair by an offset of 1: ATGTTACCGTTC.

|          | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10| 11|
|----------|---|---|---|---|---|---|---|---|---|---|---|---|
| R1       | A | T | G | - | - | - | C | C | G |   |   |   |
| R2       |   | T | G | T | - | - | - | C | G | T |   |   |
| R3       |   |   | G | T | T | - | - | - | G | T | T |   |
| R4       |   |   |   | T | T | A | - | - | - | T | T | C |
| Stitched | A | T | G | T | T | A | C | C | G | T | T | C |

**WHY**: Since the sequencer breaks up many copies of the same DNA and each read_SEQ's start position is random, larger parts of the original DNA can be reconstructed by finding overlaps between fragment_SEQs and stitching them back together.

**ALGORITHM**:

Overlapping read-pairs are stitched by taking the first read-pair and iterating through the remaining read-pairs where ...

 * the suffix from each remaining read-pair's head k is appended to the first read-pair's head k.
 * the suffix from each remaining read-pair's tail k is appended to the first read-pair's tail k.

For example, to stitch [ATG---CCG, TGT---CGT], ...

 1. stitch the heads as if they were read_SEQs: [ATG, TGT] results in ATGT,
 2. stitch the tails as if they were read_SEQs: [CCG, CGT] results in CCGT.

|          | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|----------|---|---|---|---|---|---|---|---|---|---|
| R1       | A | T | G | - | - | - | C | C | G |   |
| R2       |   | T | G | T | - | - | - | C | G | T |
| Stitched | A | T | G | T | - | - | C | C | G | T |

```{output}
ch3_code/src/ReadPair.py
python
# MARKDOWN_MERGE_OVERLAPPING\s*\n([\s\S]+)\n\s*# MARKDOWN_MERGE_OVERLAPPING
```

```{ch3}
ReadPair
stitch
ATG|3|CCG
TGT|3|CGT
GTT|3|GTT
TTA|3|TTC
```

### Break Reads

`{bm} /(Algorithms\/Assembly\/Break Reads)_TOPIC/`

**WHAT**: Given a set of read_SEQs that arbitrarily overlap, each read_SEQ can be broken into many smaller read_SEQs that overlap better. For example, given 4 10-mers that arbitrarily overlap, you can break them into better overlapping 5-mers...

```{svgbob}
                    "4 original 10-mers (left) broken up to perfectly overlapping 5-mers (right)"

"1:"        A C T A A G A A C C --+--------------------> A C T A A                                   
                                  +-------------------->   C T A A G                                 
                                  +-------------------->     T A A G A                               
                                  +-------------------->       A A G A A                             
                                  +-------------------->         A G A A C                           
                                  +-------------------->           G A A C C                         
"2:"              A A G A A C C T A A --+-------------->       A A G A A                             
                                        +-------------->         A G A A C                           
                                        +-------------->           G A A C C                         
                                        +-------------->             A A C C T                       
                                        +-------------->               A C C T A                     
                                        +-------------->                 C C T A A                   
"3:"                  G A A C C T A A T T --+---------->           G A A C C                         
                                            +---------->             A A C C T                       
                                            +---------->               A C C T A                     
                                            +---------->                 C C T A A                   
                                            +---------->                   C T A A T                 
                                            +---------->                     T A A T T               
"4:"                            T A A T T T A G C T -+->                     T A A T T               
                                                     +->                       A A T T T             
                                                     +->                         A T T T A           
                                                     +->                           T T T A G         
                                                     +->                             T T A G C       
                                                     +->                               T A G C T     
"String:"   A C T A A G A A C C T A A T T T A G C T      A C T A A G A A C C T A A T T T A G C T     
"Coverage:" 1 1 1 2 2 3 3 3 3 3 3 3 3 2 2 1 1 1 1 1      1 2 3 5 7 9 > > > > 9 8 7 6 6 5 4 3 2 1

"* Coverage of > means more than 9."
```

**WHY**: Breaking reads may cause more ambiguity in overlaps. At the same time, read breaking makes it easier to find overlaps by bringing the overlaps closer together and provides (artificially) increased coverage_SEQ.

**ALGORITHM**:

```{output}
ch3_code/src/Read.py
python
# MARKDOWN_BREAK\s*\n([\s\S]+)\n\s*# MARKDOWN_BREAK
```

```{ch3}
Read
shatter
5
ACTAAGAACC
```

### Break Read-Pairs

`{bm} /(Algorithms\/Assembly\/Break Read-Pairs)_TOPIC/`

```{prereq}
Algorithms/Assembly/Break Reads_TOPIC
```

**WHAT**: Given a set of read-pairs that arbitrarily overlap, each read-pair can be broken into many read-pairs with a smaller k that overlap better. For example, given 4 (4,2)-mers that arbitrarily overlap, you can break them into better overlapping (2,4)-mers...

```{svgbob}
                    "4 original (4,2)-mers (left) broken up to perfectly overlapping (2,4)-mers (right)"

"1:"        A C T A ‑ ‑ A A C C --+------------------> A C ‑ ‑ ‑ ‑ A A                             
                                  +------------------>   C T ‑ ‑ ‑ ‑ A C                           
                                  +------------------>     T A ‑ ‑ ‑ ‑ C C                         
"2:"              A A G A ‑ ‑ C T A A --+------------>       A A ‑ ‑ ‑ ‑ C T                       
                                        +------------>         A G ‑ ‑ ‑ ‑ T A                     
                                        +------------>           G A ‑ ‑ ‑ ‑ A A                   
"3:"                  G A A C ‑ ‑ A A T T --+-------->           G A ‑ ‑ ‑ ‑ A A                 
                                            +-------->             A A ‑ ‑ ‑ ‑ A T                  
                                            +-------->               A C ‑ ‑ ‑ ‑ T T               
"4:"                          C T A A ‑ ‑ A G C T -+->                   C T ‑ ‑ ‑ ‑ A G         
                                                   +->                     T A ‑ ‑ ‑ ‑ G C         
                                                   +->                       A A ‑ ‑ ‑ ‑ C T       
"String:"   A C T A A G A A C C T A A T T A G C T      A C T A A G A A C C T A A T T A G C T     
"Coverage:" 1 1 1 2 1 2 3 2 2 2 2 3 3 2 1 1 1 1 1      1 2 2 2 2 3 4 4 3 3 4 5 4 2 1 1 2 2 1
```

**WHY**: Breaking read-pairs may cause more ambiguity in overlaps. At the same time, read-pair breaking makes it easier to find overlaps by bringing the overlaps closer together and provides (artificially) increased coverage_SEQ.

**ALGORITHM**:

```{output}
ch3_code/src/ReadPair.py
python
# MARKDOWN_BREAK\s*\n([\s\S]+)\n\s*# MARKDOWN_BREAK
```

```{ch3}
ReadPair
shatter
2
ACTA|2|AACC
```

### Probability of Fragment Occurrence

`{bm} /(Algorithms\/Assembly\/Probability of Fragment Occurrence)_TOPIC/`

```{prereq}
Algorithms/Assembly/Stitch Reads_TOPIC
Algorithms/Assembly/Stitch Read-Pairs_TOPIC
Algorithms/Assembly/Break Reads_TOPIC
Algorithms/Assembly/Break Read-Pairs_TOPIC
```

**WHAT**: Sequencers work by taking many copies of an organism's genome, randomly breaking up those genomes into smaller pieces, and randomly scanning in those pieces (fragment_SEQs). As such, it isn't immediately obvious how many times each fragment_SEQ actually appears in the genome.

Imagine that you're sequencing an organism's genome. Given that ...

 * there's good coverage_SEQ of the genome (e.g. ~30x as many fragment_SEQs as the length of the genome),
 * the fragment_SEQs scanned in are chosen at random (unbiased),
 * the fragment_SEQs scanned in start at random offsets in the genome (unbiased),
 * and the majority of fragment_SEQs are for non-repeating parts of the genome.
 
... you can use probabilities to hint at how many times a fragment_SEQ appears in the genome.

**WHY**: 

Determining how many times a fragment_SEQ appears in a genome helps with assembly. Specifically, ...

 * fragment_SEQs for repeat regions of the genome can be accounted for during assembly.
 * fragment_SEQs containing sequencing errors may be detectable and filtered out prior to assembly.

**ALGORITHM**:

```{note}
For simplicity's sake, the genome is single-stranded (not double-stranded DNA / no reverse complementing stand).
```

Imagine a genome of ATGGATGC. A sequencer runs over that single strand and generates 3-mer read_SEQs with roughly 30x coverage_SEQ. The resulting fragment_SEQs are ...

| Read_SEQ | # of Copies |
|----------|-------------|
| ATG      | 61          |
| TGG      | 30          |
| GAT      | 31          |
| TGC      | 29          |
| TGT      | 1           |

Since the genome is known to have less than 50% repeats, the dominate number of copies likely maps to 1 instance of that read_SEQ appearing in the genome. Since the dominate number is ~30, divide the number of copies for each read_SEQ by ~30 to find out roughly how many times each read_SEQ appears in the genome ...

| Read_SEQ | # of Copies | # of Appearances in Genome |
|----------|-------------|----------------------------|
| ATG      | 61          | 2                          |
| TGG      | 30          | 1                          |
| GAT      | 31          | 1                          |
| TGC      | 29          | 1                          |
| TGT      | 1           | 0.03                       |

Note the last read_SEQ (TGT) has 0.03 appearances, meaning it's a read_SEQ that it either

 * contains a sequencing error,
 * or it has poor coverage_SEQ (likely because it's at the head / tail of the genome so it got scanned in less than other fragment_SEQs).

In this case, it's an error because it doesn't appear in the original genome: TGT is not in ATGGATGC.

```{output}
ch3_code/src/FragmentOccurrenceProbabilityCalculator.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch3}
FragmentOccurrenceProbabilityCalculator
ATG 61
TGG 30
GAT 31
TGC 29
TGT 1
```

### Overlap Graph

`{bm} /(Algorithms\/Assembly\/Overlap Graph)_TOPIC/`

```{prereq}
Algorithms/Assembly/Stitch Reads_TOPIC
Algorithms/Assembly/Stitch Read-Pairs_TOPIC
Algorithms/Assembly/Break Reads_TOPIC
Algorithms/Assembly/Break Read-Pairs_TOPIC
Algorithms/Assembly/Probability of Fragment Occurrence_TOPIC
```

**WHAT**: Given the fragment_SEQs for a single strand of DNA, create a directed graph where ...

  1. each node is a fragment_SEQ.

     ```{svgbob}
     TTA     TAG     AGT     GTT 
     TAC     TTA     CTT     ACT 
     ```

  2. each edge is between overlapping fragment_SEQs (nodes), where the ...
     * source node has the overlap in its suffix .
     * destination node has the overlap in its prefix.

     ```{svgbob}
     .----------------------------------------------------------------.
     |                                                                |
     |                                                                |
     `-> TTA --> TAG --> AGT --> GTT --> TTA --> TAC --> ACT --> CTT -'
          ^                       |       ^                       |
          |                       |       |                       |
          `-----------------------'       `-----------------------'
     ```

This is called an overlap graph.

**WHY**: An overlap graph shows the different ways that fragment_SEQs can be stitched together. A path in in an overlap graph that touches each node exactly once is one possibility for the original single stranded DNA that the fragment_SEQs came from. For example...

  * \[TTA, TAG, AGT, GTT, TTA, TAC, ACT, CTT\] ⟶ TTAGTTACTT
  * \[TTA, TAC, ACT, CTT, TTA, TAG, AGT, GTT\] ⟶ TTACTTAGTT
  * \[ACT, CTT, TTA, TAG, AGT, GTT, TTA, TAC\] ⟶ ACTTAGTTAC
  * \[CTT, TTA, TAG, AGT, GTT, TTA, TAC, ACT\] ⟶ CTTAGTTACT
  * ...

These paths are referred to as Hamiltonian paths.

```{note}
Notice that the example graph is circular. If the organism genome itself were also circular (e.g. bacterial genome), the genome guesses above are all actually the same because circular genomes don't have a beginning / end.
```

**ALGORITHM**:

Sequencers produce fragment_SEQs, but fragment_SEQs by themselves typically aren't enough for most experiments / algorithms. In theory, stitching overlapping fragment_SEQs for a single-strand of DNA should reveal that single-strand of DNA. In practice, real-world complications make revealing that single-strand of DNA nearly impossible:

 * Fragment_SEQs are for both strands (strand of double-stranded DNA a fragment_SEQ's from isn't known).
 * Fragment_SEQs may be missing (sequencer didn't capture it).
 * Fragment_SEQs may have incorrect occurrence counts (sequencer captured it too many/few times).
 * Fragment_SEQs may have errors (sequencer produced sequencing errors).
 * Fragment_SEQs may be stitch-able in more than one way (multiple guesses).
 * Fragment_SEQs may take a long time to stitch (computationally intensive).

Never the less, in an ideal world where most of these problems don't exist, an overlap graph is a good way to guess the single-strand of DNA that a set of fragment_SEQs came from. An overlap graph assumes that the fragment_SEQs it's operating on ...

 * are from a single-strand of DNA,
 * have correct occurrence counts (no missing or extra),
 * and contain no errors.

```{note}
Although the complications discussed above make it impossible to get the original genome in its entirety, it's still possible to pull out large parts of the original genome. This is discussed in Algorithms/Assembly/Find Contigs_TOPIC.
```

To construct an overlap graph, create an edge between fragment_SEQs that have an overlap.

For each fragment_SEQ, add that fragment_SEQ's ...

 * prefix to a hash table.
 * suffix to a hash table.
 
Then, join the hash tables together to find overlapping fragment_SEQs.


```{output}
ch3_code/src/ToOverlapGraphHash.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch3}
ToOverlapGraphHash
reads
TTA
TTA
TAG
AGT
GTT
TAC
ACT
CTT
```

A path that touches each node of an graph exactly once is a Hamiltonian path. Each  The Hamiltonian path in an overlap graph is a guess as to the original single strand of DNA that the fragment_SEQs for the graph came from.

The code shown below recursively walks all paths. Of all the paths it walks over, the ones that walk every node of the graph exactly once are selected.

This algorithm will likely fall over on non-trivial overlap graphs. Even finding one Hamiltonian path is computationally intensive.

```{output}
ch3_code/src/WalkAllHamiltonianPaths.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch3}
WalkAllHamiltonianPaths
reads
TTA
TTA
TAG
AGT
GTT
TAC
ACT
CTT
```

### De Bruijn Graph

`{bm} /(Algorithms\/Assembly\/De Bruijn Graph)_TOPIC/`

```{prereq}
Algorithms/Assembly/Stitch Reads_TOPIC
Algorithms/Assembly/Stitch Read-Pairs_TOPIC
Algorithms/Assembly/Break Reads_TOPIC
Algorithms/Assembly/Break Read-Pairs_TOPIC
Algorithms/Assembly/Probability of Fragment Occurrence_TOPIC
Algorithms/Assembly/Overlap Graph_TOPIC
```

**WHAT**: Given the fragment_SEQs for a single strand of DNA, create a directed graph where ...

  1. each fragment_SEQ is represented as an edge connecting 2 nodes, where the ...
     * source node is the prefix of the fragment_SEQ.
     * destination node is the suffix of the fragment_SEQ.

     ```{svgbob}
         TTC             TCT             CTT
     TT -----> TC    TC -----> CT    CT -----> TT 

         TTA             TAT             ATT
     TT -----> TA    TA -----> AT    AT -----> TT 
     ```

  2. duplicate nodes are merged into a single node.

     ```{svgbob}
                  CTT
     .--------------------------.
     |                          |
     |     TTC       TCT        |
     |   +-----> TC -----> CT --'
     v  /
     TT 
     ^  \
     |   +-----> TA -----> AT --.
     |     TTA       TAT        |
     |                          |
     `--------------------------'
                  ATT
     ```

This graph is called a de Bruijn graph: a balanced_GRAPH and strongly connected graph where the fragment_SEQs are represented as edges.

```{note}
The example graph above is balanced_GRAPH. But, depending on the fragment_SEQs used, the graph may not be totally balanced_GRAPH. A technique for dealing with this is detailed below. For now, just assume that the graph will be balanced_GRAPH.
```

**WHY**:  Similar to an overlap graph, a de Bruijn graph shows the different ways that fragment_SEQs can be stitched together. However, unlike an overlap graph, the fragment_SEQs are represented as edges rather than nodes. Where in an overlap graph you need to find paths that touch every node exactly once (Hamiltonian path), in a de Bruijn graph you need to find paths that walk over every edge exactly once (Eulerian cycle).

A path in a de Bruijn graph that walks over each edge exactly once is one possibility for the original single stranded DNA that the fragment_SEQs came from: it starts and ends at the same node (a cycle), and walks over every edge in the graph.

In contrast to finding a Hamiltonian path in an overlap graph, it's much faster to find an Eulerian cycle in an de Bruijn graph.

De Bruijn graphs were originally invented to solve the k-universal string problem, which is effectively the same concept as assembly.

**ALGORITHM**:

Sequencers produce fragment_SEQs, but fragment_SEQs by themselves typically aren't enough for most experiments / algorithms. In theory, stitching overlapping fragment_SEQs for a single-strand of DNA should reveal that single-strand of DNA. In practice, real-world complications make revealing that single-strand of DNA nearly impossible:

 * Fragment_SEQs are for both strands (strand of double-stranded DNA a fragment_SEQ's from isn't known).
 * Fragment_SEQs may be missing (sequencer didn't capture it).
 * Fragment_SEQs may have incorrect occurrence counts (sequencer captured it too many/few times).
 * Fragment_SEQs may have errors (sequencer produced sequencing errors).
 * Fragment_SEQs may be stitch-able in more than one way (multiple guesses).
 * Fragment_SEQs may take a long time to stitch (computationally intensive).

Never the less, in an ideal world where most of these problems don't exist, an de Bruijn graph is a good way to guess the single-strand of DNA that a set of fragment_SEQs came from. A de Bruijn graph assumes that the fragment_SEQs it's operating on ...

 * are from a single-strand of DNA,
 * have correct occurrence counts (no missing or extra),
 * and contain no errors.

```{note}
Although the complications discussed above make it impossible to get the original genome in its entirety, it's still possible to pull out large parts of the original genome. This is discussed in Algorithms/Assembly/Find Contigs_TOPIC.
```

To construct a de Bruijn graph, add an edge for each fragment_SEQ, creating missing nodes as required.

```{output}
ch3_code/src/ToDeBruijnGraph.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch3}
ToDeBruijnGraph
reads
TTAG
TAGT
AGTT
GTTA
TTAC
TACT
ACTT
CTTA
```

Note how the graph above is both balanced_GRAPH and strongly connected. In most cases, non-circular genomes won't generate a balanced graph like the one above. Instead, a non-circular genome will very likely generate a graph that's nearly balanced_GRAPH: Nearly balanced graphs are graphs that are would be balanced_GRAPH if not for a few unbalanced nodes (usually root and tail nodes). They can artificially be made to become balanced_GRAPH by finding imbalanced nodes and creating artificial edges between them until they become balanced nodes.

```{note}
Circular genomes are genomes that wrap around (e.g. bacterial genomes). They don't have a beginning / end.
```

```{output}
ch3_code/src/BalanceNearlyBalancedGraph.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch3}
BalanceNearlyBalancedGraph
reads
TTAC
TACC
ACCC
CCCT
```

Given a de Bruijn graph (strongly connected and balanced_GRAPH), you can find a Eulerian cycle by randomly walking unexplored edges in the graph. Pick a starting node and randomly walk edges until you end up back at that same node, ignoring all edges that were previously walked over. Of the nodes that were walked over, pick one that still has unexplored edges and repeat the process: Walk edges from that node until you end up back at that same node, ignoring edges all edges that were previously walked over (including those in the past iteration). Continue this until you run out of unexplored edges.

```{output}
ch3_code/src/WalkRandomEulerianCycle.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch3}
WalkRandomEulerianCycle
reads
TTA
TAT
ATT
TTC
TCT
CTT
```

Note that the graph above is naturally balanced_GRAPH (no artificial edges have been added in to make it balanced_GRAPH). If the graph you're finding a Eulerian cycle on has been artificially balanced_GRAPH, simply start the search for a Eulerian cycle from one of the original head node. The artificial edge will show up at the end of the Eulerian cycle, and as such can be dropped from the path.

```{svgbob}
TTA --> TAC --> ACC --> CCC --> CCT
 ^                               |
 |                               |
 `-------------------------------'
            "artificial edge"


"Path = [TTA, TAC, ACC, CCC, CCT, TTA]"

"* Last path element must be dropped (TTA)"
```

This algorithm picks one Eulerian cycle in a graph. Most graph have multiple Eulerian cycles, likely too many to enumerate all of them.

```{note}
See the section on k-universal strings to see a real-world application of Eulerian graphs. For something like k=20, good luck trying to enumerate all Eulerian cycles.
```

### Find Bubbles

`{bm} /(Algorithms\/Assembly\/Find Bubbles)_TOPIC/`

```{prereq}
Algorithms/Assembly/Overlap Graph_TOPIC
Algorithms/Assembly/De Bruijn Graph_TOPIC
```

**WHAT**: Given a set of a fragment_SEQs that have been broken to k (read breaking / read-pair breaking), any ...

 * forked prefixes,
 * forked suffixes,
 * or bubbles

... of length ...

 * k in the overlap graph,
 * or k-1 in the de Bruijn graph

... may have been from a sequencing error.

```{svgbob}
    "Forked prefix"                   "Forked suffix"                "Bubble"
                                                                             
x --> x --> x --.               .--> x --> x --> x           .--> x --> x --> x --.      
                |               |                            |                    |      
                +--> x      x --+                        x --+                    +--> x
                |               |                            |                    |      
x --> x --> x --'               `--> x --> x --> x           `--> x --> x --> x--'      
```

**WHY**: When fragment_SEQs returned by a sequencer get broken (read breaking / read-pair breaking), any fragment_SEQs containing sequencing errors may show up in the graph as one of 3 structures: forked prefix, forked suffix, or bubble. As such, it may be possible to detect these structures and flatten them (by removing bad branches) to get a cleaner graph.

For example, imagine the read_SEQ ATTGG. Read breaking it into 2-mer read_SEQs results in: \[AT, TT, TG, GG\]. 

```{svgbob}
AT --> TT --> TG --> GG 
```

Now, imagine that the sequencer captures that same part of the genome again, but this time the read_SEQ contains a sequencing error. Depending on where the incorrect nucleotide is, one of the 3 structures will get introduced into the graph:

 * ATTGG vs A**C**TGG (within first 2 elements)

   ```{svgbob}
   "ATTGG = [AT, TT, TG, GG]"
   "ACTGG = [AC, CT, TG, GG]"

   AT --> TT --.
               |
               +--> TG --> GG 
               |
   AC --> CT --'

   "This is a forked prefix"
   ```

 * ATTGG vs ATT**C**G (within last 2 elements)

   ```{svgbob}
   "ATTGG breaks into [AT, TT, TG, GG]"
   "ATTCG breaks into [AT, TT, TC, CG]"

               .--> TG --> GG
               |
   AT --> TT --+
               |
               `--> TC --> CG

   "This is a forked suffix"
   ```

 * ATTGG vs AT**C**GG (sandwiched after first 2 elements and before last 2 elements)

   ```{svgbob}
   "ATTGG = [AT, TT, TG, GG]"
   "ATCGG = [AT, TC, CG, GG]"

        .--> TC --> CG --.
        |                |
   AT --+                +--> GG 
        |                |
        `--> TT --> TG --'
    
   "This is a bubble"
   ```

Note that just because these structures exist doesn't mean that the fragment_SEQs they represent definitively have a sequencing errors. These structures could have been caused by other problems / may not be problems at all:

 * Bubbles may be caused by repetitive regions of DNA.

   Fragment_SEQs from different parts of the genome that are the same except for a few positions will show up as bubbles.

 * Bubbles / forks may be caused when sequencing double-stranded DNA.

   When both strands of DNA get tangled into the same graph, it's possible that fragment_SEQs from different strands may form bubbles or forks.

```{note}
The Pevzner book says that bubble removal is a common feature in modern assemblers. My assumption is that, before pulling out contigs (described later on), basic probabilities are used to try and suss out if a branch in a bubble / prefix fork / suffix fork is bad and remove it if it is. This (hopefully) results in longer contigs.
```

**ALGORITHM**:

```{output}
ch3_code/src/FindGraphAnomalies.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch3}
FindGraphAnomalies
reads
14
ATAGGAC 1
ATTGGAC 55
TTGGACA 30
TGGACAA 30
GGACAAT 30
GACAATC 30
ACAATCT 30
ACAGTCT 1
CAATCTC 30
AATCTCG 30
ATCTCGG 30
TCTCGGG 30
CTCGGGC 55
CTCGTGC 1
4
```

### Find Contigs

`{bm} /(Algorithms\/Assembly\/Find Contigs)_TOPIC/`

```{prereq}
Algorithms/Assembly/Overlap Graph_TOPIC
Algorithms/Assembly/De Bruijn Graph_TOPIC
Algorithms/Assembly/Find Bubbles_TOPIC
```

TODO: CONTINUE HERE

TODO: CONTINUE HERE

TODO: CONTINUE HERE

TODO: CONTINUE HERE

TODO: CONTINUE HERE

TODO: CONTINUE HERE

TODO: CONTINUE HERE

TODO: CONTINUE HERE

TODO: CONTINUE HERE

TODO: CONTINUE HERE

TODO: CONTINUE HERE

TODO: CONTINUE HERE

TODO: CONTINUE HERE

TODO: CONTINUE HERE

TODO: CONTINUE HERE

TODO: CONTINUE HERE

TODO: CONTINUE HERE

TODO: CONTINUE HERE

TODO: CONTINUE HERE

TODO: CONTINUE HERE

TODO: CONTINUE HERE

TODO: CONTINUE HERE


```{output}
ch3_code/src/FindMaximalNonBranchingPaths.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

# Stories

## Bacteria Replication

Bacteria are known to have a single chromosome of circular / looping DNA. On that DNA, the replication origin (ori) is the region in which DNA replication starts, while the replication terminus (ter) is where it ends. The ori and ter and usually placed on opposite ends of each other.

```{svgbob}
        5' ----> 3'
.---------- ori ----------.
|   | | | | | | | | | |   |
| -  ------ ori ------  - |
| - |   3' <---- 5'   | - |
| - |                 | - |
| - |                 | - |
| - |                 | - |
| -  ------ ter ------  - |
|   | | | | | | | | | |   |
`---------- ter ----------`
```

The replication process begins by a replication fork opening at the ori. As replication happens, that fork widens until the point it reaches ter...

```{svgbob}
              ori
               |
               v
     .+----------------+.
-----+                  +------
| | |                    | | | 
-----+                  +------
     `+----------------+`
               ^
               |
              ori
```
   
For each forked single-stranded DNA, DNA polymerases attach on and synthesize a new reverse complement strand so that it turns back into double-stranded DNA....

```{svgbob}
                        G <- C <- T <- T <- T <- T <- G <- . . .
                        |                            
           <-------- .- | ----------.                    
5' . . . A -> A -> A -> C -> C -> G -> A -> A -> A -> C -> . . . 3'
                     `--------------`                    

                 "Forward direction of DNA:"                       5' -----> 3'
                 "DNA polymerases moves in the reverse direction:" 5' <----- 3'
```

The process of synthesizing a reverse complement strand is different based on the section of DNA that DNA polymerase is operating on. For each single-stranded DNA, if the direction of that DNA strand is traveling from ...

 * ori to ter, it's called a forward half-strand.
 * ter to ori, it's called a reverse half-strand.

```{svgbob}
                              5' ----> 3'
                      .---------- ori ----------.
                      |   | | | | | | | | | |   |
                      | -  ------ ori ------  - |
                      | - |   3' <---- 5'   | - |
                      | - |                 | - |
                      | - |                 | - |
                      | - |                 | - |
                      | -  ------ ter ------  - |
                      |   | | | | | | | | | |   |
                      `---------- ter ----------`


      forward half-strands                      reverse half-strands 
                                                                     
            ori ->----->--.                   .-->--->--- ori        
                          |                   |                        
    .---<-  ori           v                   ^           ori ---<--.
    |                     |                   |                     |
    v                     v                   ^                     |
    |                     |                   |                     ^
    |                     v                   ^                     |
    `->---  ter           |                   |           ter --->--`  
                          |                   |                        
            ter ---<---<--`                   `--<---<--- ter        
```

Since DNA polymerase can only walk over DNA in the reverse direction (3' to 5'), the 2 reverse half-strands will quickly get walked over in one shot. A primer gets attached to the ori, then a DNA polymerase attaches to that primer to begin synthesis of a new strand. Synthesis continues until the ter is reached...

```{svgbob}
                                              "DNA polymerase synthesizing the reverse half-strand"

    "A single DNA polymerase walks the reverse half-strand,"
    "from ori to ter, as the replication fork widens."
                                             
                                                                 ori
                                                                  
                                                                  
                                        G <- C <- T <- . . . T <- G
                                        |                                         
                           <------  .-- | ----------.                       
                              A -> C -> C -> G -> A -> . . . A -> C -> T -> . . . -> G -> A -> A -> A -> C                     
                             /      `---------------`                                                     \                    
      5' . . . A -> C -> T -+                                                                              A -> C -> T . . . 3'
ter                                                                                                                               ter
      3' . . . T <- G <- A <+                                                                              T <- G <- A . . . 5'
                             \                                                       .---------------.    /                    
                              T <- G <- G <- C <- T <- . . . T <- G <- A <- . . . <- C <- T <- T <- T <- G                     
                                                                                     `-------- | ----`  ------>
                                                                                               |
                                                                  C -> T -> . . . -> G -> A -> A
                                                                  
                                                                  
                                                                 ori
``` 

For the forward half-strands, the process is much slower. Since DNA polymerase can only walk DNA in the reverse direction, the forward half-strands get replicated in small segments. That is, as the replication fork continues to grow, every ~2000 nucleotides a new primer attaches to the end of the fork on the forward strands. A new DNA polymerase attaches to each primer and walks in the reverse direction (towards the ori) to synthesize a small segment of DNA. That small segment of DNA is called an Okazaki fragment...


```{svgbob}
                                              "DNA polymerase synthesizing the forward half-strand"

    "A DNA polymerase attaches to the tip of the replication fork at"
    "the forward half-strand, roughly every 2000 nucleotide opening,"
    "to produce a small segment of DNA called an Okazaki fragment."

                                                           ori                          
      
      
                                                                       C <- T <- T <- T <- G
                                                                       |                                         
                                                              <---- .- | ----------.                                 
                              A -> C -> C -> G -> A -> . . . . . . -> G -> A -> A -> A -> C                     
                             /                                      `--------------`       \                    
      5' . . . A -> C -> T -+                                                               A -> C -> T . . . 3'
ter                                                                                                               ter
      3' . . . T <- G <- A <+                                                               T <- G <- A . . . 5'
                             \         .-------------.                                     /                    
                              T <- G <- G <- C <- T <- . . . . . . <- C <- T <- T <- T <- G                     
                                       `--------- | -` ---->                                               
                                                  |
                              A -> C -> C -> G -> A


                                                           ori                             
``` 

The replication fork will keep widening until the original 2 strands split off. DNA polymerase will have made sure that for each separated strand, a newly synthesized reverse complement is paired to it. The end result is 2 daughter chromosome where each chromosome has gaps...

```{svgbob}
                        "Two daughter chromosomes"

  "The end result is 2 daughter chromosomes, but the synthesized strand for each"
  "forward strand is chopped up into pieces (Okazaki fragments)."

          5' ----> 3'                            5' ----> 3'        
  .---------- ori ----------.            .---------- ori  - - - - -.
  |   | | | | | | | | | |   |            |   | | | | | | | | | |   :
  | -  ------ ori  - - -  - |            | -  ------ ori ------  - :
  | - |   3' <---- 5'   : - |            | - |   3' <---- 5'   | - :
  | - |                 : - |            | - |                 | - :
  | - |                 : - |            | - |                 | - :
  | - |                 : - |            | - |                 | - :
  | -  ------ ter - - -   - |            | -  ------ ter ------  - :
  |   | | | | | | | | | |   |            |   | | | | | | | | | |   :
  `---------- ter ----------`            `---------- ter  - - - - -`

  "original strand is outside strand"    "original strand is inner strand"
```

The Okazaki fragments synthesized on the forward strands end up getting sewn together by DNA ligase...

```{svgbob}
                        "Two daughter chromosomes"

  "Totally complete once DNA ligase has sewn together the Okazaki fragments."

          5' ----> 3'                            5' ----> 3'        
  .---------- ori ----------.            .---------- ori ----------.
  |   | | | | | | | | | |   |            |   | | | | | | | | | |   |
  | -  ------ ori ------  - |            | -  ------ ori ------  - |
  | - |   3' <---- 5'   | - |            | - |   3' <---- 5'   | - |
  | - |                 | - |            | - |                 | - |
  | - |                 | - |            | - |                 | - |
  | - |                 | - |            | - |                 | - |
  | -  ------ ter ------  - |            | -  ------ ter ------  - |
  |   | | | | | | | | | |   |            |   | | | | | | | | | |   |
  `---------- ter ----------`            `---------- ter ----------`
```

There are now two complete copies of the DNA.

### Find Ori and Ter

`{bm} /(Stories\/Bacteria Replication\/Find Ori and Ter)_TOPIC/`

```{prereq}
Algorithms/GC Skew_TOPIC
```

Since the forward half-strand gets its reverse complement synthesized at a much slower rate than the reverse half-strand, it stays single stranded for a much longer time. Single-stranded DNA is 100 times more susceptible to mutations than double-stranded DNA. Specifically, in single-stranded DNA, C has a greater tendency to mutate to T. This process of mutation is referred to as deanimation.

```{svgbob} 
                             ori -->---->--.
                                           |
                                           v
                                           |
                                           v
                                           |
                                           v
                                           |
                                           |
                             ter --<---<---`

                                   |
                                   | "synthesize reverse complement"
                                   v

                             ori -->---->--.       
                                | | | |    |       
                             ori --<---  - v       
                                       | - |    
"Reverse half-strand (synthesized)"    | - v    "Forward half-strand (original)"
"less Gs / more As"                    ^ - |    "less Cs / more Ts"     
                                       | - v       
                             ter -->---  - |       
                                | | | |    |       
                             ter --<---<---`       

"The forward half-strand ends up with less Cs and more Ts. As such, the"
"reverse complement strand that gets synthesized for it by DNA polymerase"
"will have less Gs and more As."
```

The reverse half-strand spends much less time as a single-stranded DNA. As such, it experiences much less C to T mutations.

```{svgbob} 
                                    .-->--->--- ori
                                    |              
                                    ^           
                                    |              
                                    ^              
                                    |              
                                    ^              
                                    |           
                                    |              
                                    `--<---<--- ter
       
                                          |
                                          | "synthesize reverse complement"
                                          v
       
                                    .-->--->---- ori       
                                    |   | | | | |          
                                    ^ -  --<---- ori       
                                    | - |              
"Reverse half-strand (original)"    ^ - v    "Forward half-strand (synthesized)"
"more normal G / A distribution"    | - |    "more normal C / more T distribution"     
                                    ^ - |                 
                                    | -  -->---- ter       
                                    |   | | | | |             
                                    `--<---<---- ter       

"The reverse half-strands end up with a more normal G and A distribution. As such, the"
"reverse complement strand that gets synthesized for it by DNA polymerase will have a"
"more normal C and T distribution."
```

Ultimately, that means that a single strand will have a different nucleotide distribution between its forward half-strand vs its backward half-strand. If the half-strand being targeted for replication is the ...

 * forward half-strand, some Cs get replaced with Ts. As such, its synthesized reverse half-strand will have less Gs.
 * reverse half-strand, most Cs are kept. As such, its synthesized forward half-strand will keep its Gs.

To simplify, the ...

 * forward half-strand: loses Cs, keeps Gs.
 * reverse half-strand: keeps Cs, loses Gs.

You can use a GC skew diagram to help pinpoint where the ori and ter might be. The plot will typically form a peak where the ter is (more G vs C) and form a valley where the ori is (less G vs C). For example, the GC skew diagram for E. coli bacteria shows a distinct peak and distinct valley.

```{ch1}
GCSkew_File
/input/ch1_code/src/GCA_000008865.2_ASM886v2_genomic.fna.xz
```

```{note}
The material talks about how not all bacteria have a single peak and single valley. Some may have multiple. The reasoning for this still hasn't been discovered. It was speculated at one point that some bacteria may have multiple ori / ter regions.
```

### Find the DnaA Box

```{prereq}
Stories/Bacteria Replication/Find Ori and Ter_TOPIC
Algorithms/K-mer/Find Repeating in Window_TOPIC
Algorithms/GC Skew_TOPIC
```

Within the ori region, there exists several copies of some k-mer pattern. These copies are referred to as DnaA boxes.

```{svgbob}
                     DnaA boxes within the ori

+--------------------------------------------------------------------+
|   :   :             :   :                            :   :         |
+-----+-----------------+--------------------------------+-----------+
      |                 |                                |           
  DnaA box          DnaA box                         DnaA box        
```

The DnaA protein binds to a DnaA box to activate the process of DNA replication. Through experiments, biologists have determined that DnaA boxes are typical 9-mers. The 9-mers may not match exactly -- the DnaA protein may bind to ...

 * the 9-mer itself.
 * slight variations of the 9-mer.
 * the reverse complement of the 9-mer.
 * slight variations of the reverse complement of the 9-mer.

```{note}
The reason why multiple copies of the DnaA box exist probably has to do with DNA mutation. If one of the copies mutates to a point where the DnaA protein no longer binds to it, it can still bind to the other copies.
```

In the example below, the general vicinity of E. coli's ori is found using GC skew, then that general vicinity is searched for repeating 9-mers. These repeating 9-mers are potential DnaA box candidates.

```{ch1}
DnaABoxCandidateFinder
/input/ch1_code/src/GCA_000008865.2_ASM886v2_genomic.fna.xz
```

## Transcription Factors

A transcription factor / regulatory protein is an enzyme that influences the rate of gene expression for some set of genes. As the saturation of a transcription factor changes, so does the rate of gene expression for the set of genes that it influences.

Transcription factors bind to DNA near the genes they influence: a transcription factor binding site is located in a gene's upstream region and the sequence at that location is a fuzzy nucleotide sequence of length 8 to 12 called a regulatory motif. The simplest way to think of a regulatory motif is a regex pattern without quantifiers. For example, the regex `[AT]TT[GC]CCCTA` may match to ATTGCCCTA, ATTCCCCTA, TTTGCCCTA, and TTTCCCCTA. The regex itself is the motif, while the sequences being matched are motif members.

```{svgbob}
  |- - - - - - - - - - - - - - - - gene upstream - - - - - - - - - - - - - - - - - -|- - - - - - - - gene - - - - - -|

                       .------------------------------------------.
                       |          transcription factor            |
5' . . . A -> A -> A -> A -> T -> T -> G -> C -> C -> C -> T -> A -> A -> C -> . . . . . . A -> C -> G -> G -> C . . . 3'
                       `------------------------------------------`

"Transcription factor binding to a transcription factor binding site."
```

The production of transcription factors may be tied to certain internal or external conditions. For example, imagine a flower where the petals...

 * bunch together at night time when sunlight is hidden and temperature is lower.
 * spread out at day time when sunlight is available and temperature is higher.

The external conditions of sunlight and temperature causes the saturation of some transcription factors to change. Those transcription factors influence the rate of gene expression for the genes that control the bunching and spreading of the petals.

```{svgbob}
   "sunlight"    "temperature"
        |            |
        +-----+------+
              |
              v
"change transcription factor saturation"
              |
              v
   "change gene expression rate"
              |
              v
 "change petal bunching/spreading"
```

### Find Regulatory Motif

```{prereq}
Algorithms/Motif/Find Motif Matrix_TOPIC
```

Given a organism, it's suspected that some physical change in that organism is linked to a transcription factor. However, it isn't known ...

 * which transcription factor (if any).
 * what the regulatory motif for that transcription factor is.

A special device is used to take snapshots of the organism's mRNA at different points in time: DNA microarray / RNA sequencer. Specifically, two snapshots are taken:

 1. When the physical change is expressed.
 2. When the physical change isn't expressed.
 
Comparing these snapshots identifies which genes have noticeably differing rates of gene expression. If these genes (or a subset of these genes) were influenced by the same transcription factor, their upstream regions would contain member_MOTIFs of that transcription factor's regulatory motif.

Since neither the transcription factor nor its regulatory motif are known, there is no specific motif to search for in the upstream regions. But, because motif members are typically similar to each other, motif matrix finding algorithms can be used on these upstream regions to find sets of similar k-mers. These similar k-mers may all be member_MOTIFs of the same transcription factor's regulatory motif.

```{svgbob}
         "find genes with differing gene expression levels"
                          |
                          v
"search for similar k-mers in upstream regions (1 per upstream region)"
```

In the example below, a set of genes in baker's yeast (Saccharomyces cerevisiae) are suspected of being influenced by the same transcription factor. These genes are searched for a common motif. Assuming one is found, it could be the motif of the suspected transcription factor.

````{note}
The example below hard codes k to 18, but you typically don't know what k should be set to beforehand. The Pevzner book doesn't discuss how to work around this problem. A strategy for finding k may be to run the motif matrix finding algorithm multiple times, but with a different k each time. For each member_MOTIF, if the k-mers selected across the runs came from the same general vicinity of the gene's upstream region, those k-mers may either be picking ...

 * the actual member_MOTIF.
 * a part of the actual member_MOTIF.
 * a part of the actual member_MOTIF with some junk prepended/appended to it.
````

```{ch2}
PracticalMotifFindingExample
```

# Terminology

 * `{bm} k-mer/(\d+-mer|k-mer|kmer)/i` - A subsequence of length k within some larger biological sequence (e.g. DNA or amino acid chain). For example, in the DNA sequence GAAATC, the following k-mer's exist:

   | k | k-mers          |
   |---|-----------------|
   | 1 | G A A A T C     |
   | 2 | GA AA AA AT TC  |
   | 3 | GAA AAA AAT ATC |
   | 4 | GAAA AAAT AATC  |
   | 5 | GAAAT AAATC     |
   | 6 | GAAATC          |

 * `{bm} kd-mer/(\(\d+,\s*\d+\)-mer|kd-mer|kdmer|\(k,\s*d\)-mer)/i` - A subsequence of length 2k + d within some larger biological sequence (e.g. DNA or amino acid chain) where the first k elements and the last k elements are known but the d elements in between isn't known.
 
   When identifying a kd-mer with a specific k and d, the proper syntax is (k, d)-mer. For example, (1, 2)-mer represents a kd-mer with k=1 and d=2. In the DNA sequence GAAATC, the following (1, 2)-mer's exist: `G--A`, `A--T`, `A--C`.

   See read-pair.

 * `{bm} 5'` (`{bm} 5 prime`) / `{bm} 3'` (`{bm} 3 prime`) - 5' (5 prime) and 3' (3 prime) describe the opposite ends of DNA. The chemical structure at each end is what defines if it's 5' or 3' -- each end is guaranteed to be different from the other. The forward direction on DNA is defined as 5' to 3', while the backwards direction is 3' to 5'.

   Two complementing DNA strands will always be attached in opposite directions.
 
   ```{svgbob}
         forward
        --------->
   5' -+-+-+-+-+-+-+- 3'
       | | | | | | |
   3' -+-+-+-+-+-+-+- 5'
        <---------
         backward
   ```
 
 * `{bm} DNA polymerase` - An enzyme that replicates a strand of DNA. That is, DNA polymerase walks over a single strand of DNA bases (not the strand of base pairs) and  generates a strand of complements. Before DNA polymerase can attach itself and start replicating DNA, it requires a primer.
 
 
   ```{svgbob}
                           G <- C <- T <- T <- T <- T <- G <- . . .
                           |                            
              <-------- .- | ----------.                    
   5' . . . A -> A -> A -> C -> G -> A -> A -> A -> A -> C -> . . . 3'
                        `--------------`                    
   
                    "Forward direction of DNA:"                       5' -----> 3'
                    "DNA polymerases moves in the reverse direction:" 5' <----- 3'
   ```
 
   DNA polymerase is unidirectional, meaning that it can only walk a DNA strand in one direction: reverse (3' to 5') 
 
 * `{bm} primer` - A primer is a short strand of RNA that binds to some larger strand of DNA (single bases, not a strand of base pairs) and allows DNA synthesis to  happen. That is, the primer acts as the entry point for special enzymes DNA polymerases. DNA polymerases bind to the primer to get access to the strand.
 
 * `{bm} replication fork` - The process of DNA replication requires that DNA's 2 complementing strands be unwound and split open. The area where the DNA starts to  split is called the replication fork. In bacteria, the replication fork starts at the replication origin and keeps expanding until it reaches the replication terminus.  Special enzymes called DNA polymerases walk over each unwound strand and create complementing strands.
 
   ```{svgbob}
                 ori
                  |
                  v
        .+----------------+.
   -----+                  +------
   | | |                    | | | 
   -----+                  +------
        `+----------------+`
                  ^
                  |
                 ori
   ```
 
 * `{bm} replication origin` (`{bm} ori/\b(ori)\b/i`) - The point in DNA at which replication starts.
 
 * `{bm} replication terminus` (`{bm} ter/\b(ter)\b/i`) - The point in DNA at which replication ends.

 * `{bm} forward half-strand` / `{bm} reverse half-strand/(reverse half-strand|backward half-strand|backwards half-strand)/i` - Bacteria are known to have a single chromosome of circular / looping DNA. In this DNA, the replication origin (ori) is the region of DNA where replication starts, while the replication terminus (ter) is where replication ends.

   ```{svgbob}
           5' ----> 3`
   .---------- ori ----------.
   |   | | | | | | | | | |   |
   | -  ------ ori ------  - |
   | - |   3' <---- 5`   | - |
   | - |                 | - |
   | - |                 | - |
   | - |                 | - |
   | -  ------ ter ------  - |
   |   | | | | | | | | | |   |
   `---------- ter ----------`
   ```

   If you split up the DNA based on ori and ter being cutting points, you end up with 4 distinct strands. Given that the direction of a strand is 5' to 3', if the direction of the strand starts at...

   * ori and ends at ter, it's called the forward half-strand.

     ```{svgbob}
      forward half-strands  
                            
             ori ->----->--.
                           |
     .---<-  ori           v
     |                     |
     v                     v
     |                     |
     |                     v
     `->---  ter           |
                           |
             ter ---<---<--`
     ```

   * ter and ends at ori, it's called the reverse half-strand.

     ```{svgbob}
       reverse half-strands 
                            
     .-->--->--- ori        
     |                      
     ^           ori ---<--.
     |                     |
     ^                     |
     |                     ^
     ^                     |
     |           ter --->--`
     |                      
     `--<---<--- ter        
     ```

   ```{note}
   * Forward half-strand is the same as lagging half-strand.
   * Reverse half-strand is the same as leading half-strand.
   ```

 * `{bm} leading half-strand` / `{bm} lagging half-strand` - Given the 2 strands tha make up a DNA molecule, the strand that goes in the...

   * reverse direction (3' to 5') is called the leading half-strand.
   * forward direction (5' to 3') is called the lagging half-strand.

   This nomenclature has to do with DNA polymerase. Since DNA polymerase can only walk in the reverse direction (3' to 5'), it synthesizes the leading half-strand in one shot. For the lagging half-strand (5' to 3'), multiple DNA polymerases have to used to synthesize DNA, each binding to the lagging strand and walking backwards a small amount to generate a small fragment_NORM of DNA (Okazaki fragment). the process is much slower for the lagging half-strand, that's why it's called lagging.

   ```{note}
   * Leading half-strand is the same as reverse half-strand.
   * Lagging half-strand is the same as forward half-strand.
   ```

 * `{bm} Okazaki fragment` - A small fragment_NORM of DNA generated by DNA polymerase for forward half-strands. DNA synthesis for the forward half-strands can only happen in small pieces. As the fork open ups every ~2000 nucleotides, DNA polymerase attaches to the end of the fork on the forward half-strand and walks in reverse to generate that small segment (DNA polymerase can only walk in the reverse direction).

 * `{bm} DNA ligase` - An enzyme that sews together short segments of DNA called Okazaki fragments by binding the phosphate group on the end of one strand with the deoxyribose group on the other strand.

 * `{bm} DnaA box` - A sequence in the ori that the DnaA protein (responsible for DNA replication) binds to.

 * `{bm} single stranded DNA/(single stranded DNA|single-stranded DNA)/i` - A single strand of DNA, not bound to a strand of its reverse complements.

   ```{svgbob}
   5' . . . A -> A -> A -> C -> C -> G -> A -> A -> A -> C -> . . . 3'
   ```

 * `{bm} double stranded DNA/(double stranded DNA|double-stranded DNA|reverse complement)/i` - Two strands of DNA bound together, where each strand is the reverse complement of the other.

   ```{svgbob}
   3' . . . T <- T <- T <- G <- C <- T <- T <- T <- T <- G <- . . . 5'
            |    |    |    |    |    |    |    |    |    | 
   5' . . . A -> A -> A -> C -> G -> A -> A -> A -> A -> C -> . . . 3'    
   ```

 * `{bm} gene/(\bgenes\b|\bgene\b)/i` - A segment of DNA that contains the instructions for either a protein or functional RNA.

 * `{bm} gene product` - The final synthesized material resulting from the instructions that make up a gene. That synthesized material either being a protein or functional RNA.

 * `{bm} transcription/(transcription|transcribed|transcribe)/i` - The process of transcribing a gene to RNA. Specifically, the enzyme RNA polymerase copies the segment of DNA that makes up that gene to a strand of RNA.

   ```{svgbob}
        +--> mRNA
   DNA -+
        +--> "functional RNA"
   ```

 * `{bm} translation/(translation|translated|translate)/i` - The process of translating mRNA to protein. Specifically, a ribosome takes in the mRNA generated by transcription and outputs the protein that it codes for.

   ```{svgbob}
        +--> mRNA ---> protein
   DNA -+
   ```

 * `{bm} gene expression` - The process by which a gene is synthesized into a gene product. When the gene product is...

   * a protein, the gene is transcribed to mRNA and translated to a protein.
   * functional RNA, the gene is transcribed to a type of RNA that isn't mRNA (only mRNA is translated to a protein).

   ```{svgbob}
          +--> mRNA ---> "protein"
          |              "(gene product)"
   DNA   -+
   (gene) |
          +--> "functional RNA"
               "(gene product)"
   ```

 * `{bm} regulatory gene` / `{bm} regulatory protein` - The proteins encoded by these genes effect gene expression for certain other genes. That is, a regulatory protein can cause certain other genes to be expressed more (promote gene expression) or less (repress gene expression).

   Regulatory genes are often controlled by external factors (e.g. sunlight, nutrients, temperature, etc..)

 * `{bm} feedback loop` / `{bm} negative feedback loop` / `{bm} positive feedback loop` - A feedback loop is a system where the output (or some part of the output) is fed back into the system to either promote or repress further outputs.

   ```{svgbob}
          +--------+
   IN --->|        |
          | SYSTEM +--+-----> OUT 
      +-->|        |  |
      |   +--------+  v
      |               |
      +--<------<-----+
             OUT
   ```

   A positive feedback loop amplifies the output while a negative feedback loop regulates the output. Negative feedback loops in particular are important in biology because they allow organisms to maintain homeostasis / equilibrium (keep a consistent internal state). For example, the system that regulates core temperatures in a human is a negative feedback loop. If a human's core temperature gets too...
   * low, they shiver to drive the temperature up.
   * high, they sweat to drive the temperature down.

   In the example above, the output is the core temperature. The body monitors its core temperature and employs mechanisms to bring it back to normal if it goes out of range (e.g. sweat, shiver). The outside temperature is influencing the body's core temperature as well as the internal shivering / sweating mechanisms the body employs.

   ```{svgbob}
                      +--------+
   "OUTSIDE HEAT" --->|        |
                      |  BODY  +--+-----> "CORE HEAT"
                  +-->|        |  |
                  |   +--------+  v
                  |               |
                  +--<------<-----+
                     "CORE HEAT"
   ```

 * `{bm} circadian clock` / `{bm} circadian oscillator` - A biological clock that synchronizes roughly around the earth's day-night cycle. This internal clock helps many species regulate their physical and behavioural attributes. For example, hunt during the night vs sleep during the day (e.g. nocturnal owls).

 * `{bm} upstream region` - The area just before some interval of DNA. Since the direction of DNA is 5' to 3', this area is towards the 5' end (upper end).

 * `{bm} downstream region` - The area just after some interval of DNA. Since the direction of DNA is 5' to 3', this area is towards the 3' end (lower end).

 * `{bm} transcription factor` - A regulatory protein that controls the rate of transcription for some gene that it has influence over (the copying of DNA to mRNA). The protein binds to a specific sequence in the gene's upstream region.

 * `{bm} motif` - A pattern that matches against many different k-mers, where those matched k-mers have some shared biological significance. The pattern matches a fixed k where each position may have alternate forms. The simplest way to think of a motif is a regex pattern without quantifiers. For example, the regex `[AT]TT[GC]C` may match to ATTGC, ATTCC, TTTGC, and TTTCC.

 * `{bm} motif member` `{bm} /\b(member)_MOTIF/i` - A specific nucleotide sequence that matches a motif. For example, given a motif represented by the regex `[AT]TT[GC]C`, the sequences ATTGC, ATTCC, TTTGC, and TTTCC would be its member_MOTIFs.

 * `{bm} motif matrix/(motif matrix|motif matrices)/i` - A set of k-mers stacked on top of each other in a matrix, where the k-mers are either...

   * member_MOTIFs of the same motif,
   * or suspected member_MOTIFs of the same motif.
   
   For example, the motif `[AT]TT[GC]C` has the following matrix:

   |0|1|2|3|4|
   |-|-|-|-|-|
   |A|T|T|G|C|
   |A|T|T|C|C|
   |T|T|T|G|C|
   |T|T|T|C|C|

 * `{bm} regulatory motif` - The motif of a transcription factor, typically 8 to 12 nucleotides in length.

 * `{bm} transcription factor binding site` - The physical binding site for a transcription factor. A gene that's regulated by a transcription factor needs a sequence located in its upstream region that the transcription factor can bind to: a motif member of that transcription factor's regulatory motif.

   ```{note}
   A gene's upstream region is the 600 to 1000 nucleotides preceding the start of the gene.
   ```

 * `{bm} cDNA/(cDNA)/` - A single strand of DNA generated from mRNA. The enzyme reverse transcriptase scans over the mRNA and creates the complementing single DNA strand.

   ```{svgbob}
   3' . . . U <- U <- U <- G <- C <- U <- U <- U <- U <- G <- . . . 5'   mRNA  
            |    |    |    |    |    |    |    |    |    | 
   5' . . . A -> A -> A -> C -> G -> G -> A -> A -> A -> C -> . . . 3'   cDNA  
   ```

   The mRNA portion breaks off, leaving the single-stranded DNA.

   ```{svgbob}
   5' . . . A -> A -> A -> C -> G -> G -> A -> A -> A -> C -> . . . 3'   cDNA  
   ```

 * `{bm} DNA microarray` / `{bm} DNA array` - A device used to compare gene expression. This works by measuring 2 mRNA samples against each other: a control sample and an experimental sample. The samples could be from...
 
   * the same organism but at different times.
   * diseased and healthy versions of the same organism.
   * etc..

   Both mRNA samples are converted to cDNA and are given fluorescent dyes. The control sample gets dyed green while the experimental sample gets dyed red.

   ```{svgbob}
   "control mRNA"      -> cDNA -> "cDNA dyed red"
   "experimental mRNA" -> cDNA -> "cDNA dyed green"
   ```
   
   A sheet is broken up into multiple regions, where each region has the cDNA for one specific gene from the control sample printed.

   ```{svgbob}
   +---+---+---+---+---+---+---+
   |c1 |c4 |c7 |c10|c13|c16|c19|
   +---+---+---+---+---+---+---+
   |c2 |c5 |c8 |c11|c14|c17|c20|
   +---+---+---+---+---+---+---+
   |c3 |c6 |c9 |c12|c15|c18|c21|
   +---+---+---+---+---+---+---+
   ```
   
   The idea is that once the experimental cDNA is introduced to that region, it should bind to the control cDNA that's been printed to form double-stranded DNA. The color emitted in a region should correspond to the amount of gene expression for the gene that region represents. For example, if a region on the sheet is fully yellow, it means that the gene expression for that gene is roughly equal (red mixed with green is yellow).

 * `{bm} greedy algorithm` - An algorithm that tries to speed things up by taking the locally optimal choice at each step. That is, the algorithm doesn't look more than 1 step ahead.
 
   For example, imagine a chess playing AI that had a strategy of trying to eliminate the other player's most valuable piece at each turn. It would be considered greedy because it only looks 1 move ahead before taking action. Normal chess AIs / players look many moves ahead before taking action. As such, the greedy AI may be fast but it would very likely lose most matches. 
  
 * `{bm} Cromwell's rule` - When a probability is based off past events, 0.0 and 1.0 shouldn't be used. That is, if you've...
 
   * never seen an even occur in the past, it doesn't mean that there's a 0.0 probability of it occurring next.
   * always seen an event occur in the past, it doesn't mean that there's a 1.0 probability of it occurring next.
 
   Unless you're dealing with hard logical statements where prior occurrences don't come in to play (e.g. 1+1=2), you should include a small chance that some extremely unlikely event may happen. The example tossed around is "the probability that the sun will not rise tomorrow." Prior recorded observations show that that sun has always risen, but that doesn't mean that there's a 1.0 probability of the sun rising tomorrow (e.g. some extremely unlikely cataclysmic event may prevent the sun from rising).

 * `{bm} Laplace's rule of succession/(Laplace's rule of succession|Laplace's rule)/i` - If some independent true/false event occurs n times, and s of those n times were successes, it's natural for people to assume the probability of success is `{kt} \frac{s}{n}`. However, if the number of successes is 0, the probability would be 0.0. Cromwell's rule states that when a probability is based off past events, 0.0 and 1.0 shouldn't be used. As such, a more appropriate / meaningful measure of probability is `{kt} \frac{s+1}{n+2}`.

   For example, imagine you're sitting on a park bench having lunch. Of the 8 birds you've seen since starting your lunch, all have been pigeons. If you were to calculate the probability that the next bird you'll see a crow, `{kt} \frac{0}{8}` would be flawed because it states that there's no chance that the next bird will be a crow (there obviously is a chance, but it may be a small chance). Instead, applying Laplace's rule allows for the small probability that a crow may be seen next: `{kt} \frac{0+1}{8+2}`.

   Laplace's rule of succession is more meaningful when the number of trials (n) is small.

 * `{bm} pseudocount` - When a zero is replaced with a small number to prevent unfair scoring. See Laplace's rule of succession.

 * `{bm} randomized algorithm` - An algorithm that uses a source of randomness as part of its logic. Randomized algorithms come in two forms: Las Vegas algorithms and Monte Carlo algorithms

 * `{bm} Las Vegas algorithm` - A randomized algorithm that delivers a guaranteed exact solution. That is, even though the algorithm makes random decisions it is guaranteed to converge on the exact solution to the problem its trying to solve (not an approximate solution).

   An example of a Las Vegas algorithm is randomized quicksort (randomness is applied when choosing the pivot).

 * `{bm} Monte Carlo algorithm` - A randomized algorithm that delivers an approximate solution. Because these algorithms are quick, they're typically run many times. The approximation considered the best out of all runs is the one that gets chosen as the solution.

   An example of a Monte Carlo algorithm is a genetic algorithm to optimize the weights of a deep neural network. That is, a step of the optimization requires running n different neural networks to see which gives the best result, then replacing those n networks with n copies of the best performing network where each copy has randomly tweaked weights. At some point the algorithm will stop producing incrementally better results.

   Perform the optimization (the entire thing, not just a single step) thousands of times and pick the best network.
  
 * `{bm} consensus string/(consensus string|consensus sequence)/i` - The k-mer generated by selecting the most abundant column at each index of a motif matrix.

   |         |0|1|2|3|4|
   |---------|-|-|-|-|-|
   |k-mer 1  |A|T|T|G|C|
   |k-mer 2  |A|T|T|C|C|
   |k-mer 3  |T|T|T|G|C|
   |k-mer 4  |T|T|T|C|C|
   |k-mer 5  |A|T|T|C|G|
   |consensus|A|T|T|C|C|

   The generate k-mer may also use a hybrid alphabet. The consensus string for the same matrix above using IUPAC nucleotide codes: `WTTSS`.
  
 * `{bm} entropy` - The uncertainty associated with a random variable. Given some set of outcomes for a variable, it's calculated as `{kt} -\sum_{i=1}^{n} P(x_i) log P(x_i)`.

   This definition is for information theory. In other contexts (e.g. physics, economics), this term has a different meaning.

 * `{bm} genome` - All of the DNA for some organism.

 * `{bm} sequence` - The ordered elements that make up some biological entity. For example, a DNA sequence contains the set of nucleotides and their positions for that DNA strand.

 * `{bm} sequencing/(sequencing|sequenced)/i` - The process of determining which nucleotides are assigned to which positions in a strand of DNA or RNA.

   The machinery used for DNA sequencing is called a sequencer. A sequencer takes multiple copies of the same DNA, breaks that DNA up into smaller fragment_NORMs, and scans in those fragment_SEQs. Each fragment_SEQ is typically the same size but has a unique starting offset. Because the starting offsets are all different, the original larger DNA sequence that can be constructed by finding fragment_SEQ with overlapping regions and stitching them together.

   |             |0|1|2|3|4|5|6|7|8|9|
   |-------------|-|-|-|-|-|-|-|-|-|-|
   |read_SEQ 1   | | | | |C|T|T|C|T|T|
   |read_SEQ 2   | | | |G|C|T|T|C|T| |
   |read_SEQ 3   | | |T|G|C|T|T|C| | |
   |read_SEQ 4   | |T|T|G|C|T|T| | | |
   |read_SEQ 5   |A|T|T|G|C|T| | | | |
   |reconstructed|A|T|T|G|C|T|T|C|T|T|

 * `{bm} sequencer` - A machine that performs DNA or RNA sequencing.

 * `{bm} sequencing error` - An error caused by a sequencer returning a fragment_SEQ where a nucleotide was misinterpreted at one or more positions (e.g. offset 3 was actually a C but it got scanned in as a G).

 * `{bm} read/\b(read)_SEQ/i` - A segment of genome scanned in during the process of sequencing.

 * `{bm} read-pair/(read-pair|read pair)/i` - A segment of genome scanning in during the process of sequencing, where the middle of the segment is unknown. That is, the first k elements and the last k elements are known, but the d elements in between aren't known. The total size of the segment is 2k + d.

   Sequencers provide read-pairs as an alternative to longer read_SEQs because the longer a read_SEQ is the more errors it contains.

   See kd-mer.

 * `{bm} fragment/(fragment)_SEQ/i` - A scanned sequence returned by a sequencer. Represented as either a read_SEQ or a read-pair.

 * `{bm} assembly/(assembly|assemble)/i` - The process of stitching together overlapping fragment_SEQs to construct the sequence of the original larger DNA that those fragment_SEQs came from.

 * `{bm} hybrid alphabet/(hybrid alphabet|alternate alphabet|alternative alphabet)/i` - When representing a sequence that isn't fully conserved, it may be more appropriate to use an alphabet where each letter can represent more than 1 nucleotide. For example, the IUPAC nucleotide codes provides the following alphabet:

   * A = A
   * C = C
   * T = T
   * G = G
   * W = A or T
   * S = G or C
   * K = G or T
   * Y = C or T 
   * ...

   If the sequence being represented can be either AAAC or AATT, it may be easier to represent a single string of AAWY.
  
 * `{bm} IUPAC nucleotide code` - A hybrid alphabet with the following mapping:

   | Letter   | Base                |
   |----------|---------------------|
   | A        | Adenine             |
   | C        | Cytosine            |
   | G        | Guanine             |
   | T (or U) | Thymine (or Uracil) |
   | R        | A or G              |
   | Y        | C or T              |
   | S        | G or C              |
   | W        | A or T              |
   | K        | G or T              |
   | M        | A or C              |
   | B        | C or G or T         |
   | D        | A or G or T         |
   | H        | A or C or T         |
   | V        | A or C or G         |
   | N        | any base            |
   | . or -   | gap                 |

   [Source](https://www.bioinformatics.org/sms/iupac.html).

 * `{bm} sequence logo/(\blogo|sequence logo)/i` - A graphical representation of how conserved a sequence's positions are. Each position has its possible nucleotides stacked on top of each other, where the height of each nucleotide is based on how conserved it is. The more conserved a position is, the taller that column will be.
 
   Typically applied to DNA or RNA, and May also be applied to other biological sequence types (e.g. amino acids).

   The following is an example of a logo generated from a motif sequence:

   ```{ch2}
   MotifLogo
   TCGGGGGTTTTT
   CCGGTGACTTAC
   ACGGGGATTTTC
   TTGGGGACTTTT
   AAGGGGACTTCC
   TTGGGGACTTCC
   TCGGGGATTCAT
   TCGGGGATTCCT
   TAGGGGAACTAC
   TCGGGTATAACC
   ```

 * `{bm} transposon/(transposon|transposable element|jumping gene)/i` - A DNA sequence that can change its position within a genome, altering the genome size. They come in two flavours:

   * Class I (retrotransposon) - Behaves similarly to copy-and-paste where the sequence is duplicated. DNA is transcribed to RNA, followed by that RNA being reverse transcribed back to DNA by an enzyme called reverse transcriptase.
   * Class II (DNA transposon) - Behaves similarly to cut-and-paste where the sequence is moved. DNA is physically cut out by an enzyme called transposases and placed back in at some other location.
  
   Often times, transposons cause disease. For example, ...

   * insertion of a transposon into a gene will likely disable that gene.
   * after a transposon leaves a gene, the gap likely won't be repaired correctly.

 * `{bm} adjacency list` - An internal representation of a graph where each node has a list of pointers to other nodes that it can forward to.

   ```{svgbob}
   A ---> B ---> C ---> D ---> F
                 |      ^      ^
                 |      |      |
                 +----> E -----+
   ```

   The graph above represented as an adjacency list would be...

   | From | To  |
   |------|-----|
   | A    | B   |
   | B    | C   |
   | C    | D,E |
   | D    | F   |
   | E    | D,F |
   | F    |     |

 * `{bm} adjacency matrix` - An internal representation of a graph where a matrix defines the number of times that each node forwards to every other node.

   ```{svgbob}
   A ---> B ---> C ---> D ---> F
                 |      ^      ^
                 |      |      |
                 +----> E -----+
   ```

   The graph above represented as an adjacency matrix would be...

   |   | A | B | C | D | E | F |
   |---|---|---|---|---|---|---|
   | A | 0 | 1 | 0 | 0 | 0 | 0 |
   | B | 0 | 0 | 1 | 0 | 0 | 0 |
   | C | 0 | 0 | 0 | 1 | 1 | 0 |
   | D | 0 | 0 | 0 | 0 | 0 | 1 |
   | E | 0 | 0 | 0 | 1 | 0 | 1 |
   | F | 0 | 0 | 0 | 0 | 0 | 0 |

 * `{bm} Hamiltonian path/(Hamiltonian path|Hamilton path)/i` - A path in a graph that visits every node exactly once.
 
   The graph below has the Hamiltonian path ABCEDF.

   ```{svgbob}
   A ---> B ---> C ---> D ---> F
                 |      ^      ^
                 |      |      |
                 +----> E -----+
   ```

 * `{bm} Eulerian path` `{bm} /(Eulerian)_PATH/i` - A path in a graph that visits every edge exactly once.
 
   In the graph below, the Eulerian path is (A,B), (B,C), (C,D), (D,E), (E,C), (C,D), (D,F).

   ```{svgbob}
                 +------+
                 |      |
                 |      v
   A ---> B ---> C ---> D ---> F
                 ^      |
                 |      v
                 +----- E
   ```

 * `{bm} Eulerian cycle` `{bm} /(Eulerian)_CYCLE/i` - An Eulerian path that forms a cycle. That is, a path in a graph that is a cycle and visits every edge exactly once.
 
   The graph below has an Eulerian cycle of (A,B), (B,C) (C,D), (D,F), (F,C), (C,A).

   ```{svgbob}
                 +-------------+
                 |             |
                 v             |
   A ---> B ---> C ---> D ---> F
   ^             |
   |             |
   +-------------+
   ```

   If a graph contains an Eulerian cycle, it's said to be an Eulerian graph.

 * `{bm} Eulerian graph` `{bm} /(Eulerian)_GRAPH/i` - For a graph to be Eulerian_GRAPH, it must have am Eulerian cycle. For a graph to have an Eulerian cycle, it must be both balanced_GRAPH and strongly connected.
 
    ```{svgbob}
                 +-------------+
                 |             |
                 v             |
   A ---> B ---> C ---> D ---> F
   ^             |
   |             |
   +-------------+
   ```

   Note how in the graph above, ...
   
   * every node is reachable from every other node (strongly connected),
   * every node has an outdegree equal to its indegree (balanced_GRAPH).

     | Node | Indegree | Outdegree |
     |------|----------|-----------|
     | A    | 1        | 1         |
     | B    | 1        | 1         |
     | C    | 2        | 2         |
     | D    | 1        | 1         |
     | F    | 1        | 1         |

   In contrast, the following graphs are not Eulerian graphs (no Eulerian cycles exist):
   
   * Strongly connected but not balanced_GRAPH.

     ```{svgbob}
     A ---> B <--- D
     ^      |      ^
     |      v      |
     +----- C -----+

     "* B contains 2 indegree but only 1 outdegree."
     ```

   * Balanced_GRAPH but not strongly connected.

     ```{svgbob}
     A ---> B ---> E ---> F
     ^      |      ^      |
     |      v      |      v
     D <--- C      H <--- G

     "* It isn't possible to reach B from E, F, G, or H"
     ```

   * Balanced_GRAPH but disconnected (not strongly connected).

     ```{svgbob}
     A ---> B      E ---> F
     ^      |      ^      |
     |      v      |      v
     D <--- C      H <--- G

     "* It isn't possible to reach E, F, G, or H from A, B, C, or D (and vice versa)"
     ```

 * `{bm} disconnected` / `{bm} connected` - A graph is disconnected if you can break it out into 2 or more distinct sub-graphs without breaking any paths. In other words, the graph contains at least two nodes which aren't contained in any path.

   The graph below is disconnected because there is no path that contains E, F, G, or H and A, B, C, or D.

    ```{svgbob}
   A ---> B      E ---> F
   ^      |      ^      |
   |      v      |      v
   D <--- C      H <--- G
   ```

   The graph below is connected.

   ```{svgbob}
   A ---> B ---> E ---> F
   ^      |      ^      |
   |      v      |      v
   D <--- C      H <--- G
   ```

 * `{bm} strongly connected` - A graph is strongly connected if every node is reachable from every other node.

   The graph below is **not** strongly connected because neither A nor B is reachable by C, D, E, or F.

   ```{svgbob}
   A ---> B ---> C ---> D ---> F
                 |      ^      ^
                 |      |      |
                 +----> E -----+
   ```

   The graph below is strongly connected because all nodes are reachable from all nodes.

   ```{svgbob}
                 +-------------+
                 |             |
                 v             |
   A ---> B ---> C ---> D ---> F
   ^             |
   |             |
   +-------------+
   ```

 * `{bm} indegree` / `{bm} outdegree` - The number of edges leading into / out of a node of a directed graph.

    The node below has an indegree of 3 and an outdegree of 1.

    ```{svgbob}
    -----+
         |
         v
    ---> N --->
         ^
         |
    -----+
    ```

 * `{bm} balanced node` `{bm} /(balanced)_NODE/i` - A node of a directed graph that has an equal indegree and outdegree. That is, the number of edges coming in is equal to the number of edges going out.

    The node below has an indegree and outdegree of 1. It is balanced_NODE.

    ```{svgbob}
    ---> N --->
    ```

    `{bm-error} Just use the words balanced node/(balanced_NODE node)/i`

 * `{bm} balanced graph` `{bm} /(balanced)_GRAPH/i` - A directed graph where ever node is balanced_NODE.

   The graph below is balanced_GRAPH because all nodes are balanced_NODE.

   ```{svgbob}
                 +-------------+
                 |             |
                 v             |
   A ---> B ---> C ---> D ---> F
   ^             |
   |             |
   +-------------+
   ```

   | Node | Indegree | Outdegree |
   |------|----------|-----------|
   | A    | 1        | 1         |
   | B    | 1        | 1         |
   | C    | 2        | 2         |
   | D    | 1        | 1         |
   | F    | 1        | 1         |

   `{bm-error} Just use the words balanced graph/(balanced_GRAPH graph)/i`

 * `{bm} overlap graph` - A graph representing the k-mers making up a string. Specifically, the graph is built in 2 steps:
 
   1. Each node is a fragment_SEQ.
 
      ```{svgbob}
      TTA     TAG     AGT     GTT 
      TAC     TTA     CTT     ACT 
      ```
 
   2. Each edge is between overlapping fragment_SEQs (nodes), where the ...
      * source node has the overlap in its suffix .
      * destination node has the overlap in its prefix.
 
      ```{svgbob}
      +----------------------------------------------------------------+
      |                                                                |
      |                                                                |
      +-> TTA --> TAG --> AGT --> GTT --> TTA --> TAC --> ACT --> CTT -+
           ^                       |       ^                       |
           |                       |       |                       |
           +-----------------------+       +-----------------------+
      ```

   Overlap graphs used for genome assembly.

 * `{bm} de Bruijn graph` - A special graph representing the k-mers making up a string. Specifically, the graph is built in 2 steps:
 
   1. Each k-mer is represented as an edge connecting 2 nodes. The ...

      * source node represents the first 0 to n-1 elements of the k-mer,
      * destination node represents last 1 to n elements of the k-mer,
      * and edge represents the k-mer.

      For example, ...

      ```{svgbob}
      "* GGTGGT has k-mers GGT GTG TGG GGT"
      
         GGT
      GG ---> GT

         GTG
      GT ---> TG

         TGG
      TG ---> GG

         GGT
      GG ---> GT
      ```

   2. Each node representing the same value is merged together to form the graph.

      For example, ...

      ```{svgbob}
      "* GGTGGT has k-mers GGT GTG TGG GGT"

              GTG       
      +----------------+
      |                |
      |        +------+|
      |        | GGT  ||
      v  TGG   |      v|
      TG ---> GG      GT
               |      ^
               | GGT  |
               +------+
      ```

   De Bruijn graphs are used for genome assembly. It's much faster to assemble a genome from a de Bruijn graph than it is to from an overlap graphs.
   
   De Bruijn graphs were originally invented to solve the k-universal string problem.

 * `{bm} k-universal/(k-universal|\d+-universal)/i` - For some alphabet and k, a string is considered k-universal if it contains every k-mer for that alphabet exactly once. For example, for an alphabet containing only 0 and 1 (binary) and k=3, a 3-universal string would be 0001110100 because it contains every 3-mer exactly once:

   * 000: **000**1110100
   * 001: 0**001**110100
   * 010: 000111**010**0
   * 011: 00**011**10100
   * 100: 0001110**100**
   * 101: 00011**101**00
   * 110: 0001**110**100
   * 111: 000**111**0100

   ```{note}
   This is effectively assembly. There are a set of k-mers and they're being stitched together to form a larger string. The only difference is that the elements aren't nucleotides.
   ```

   De Bruijn graphs were invented in an effort to construct k-universal strings for arbitrary values of k. For example, given the k-mers in the example above (000, 001, ...), a k-universal string can be found by constructing a de Bruijn graph from the k-mers and finding a Eulerian cycle in that graph.

   ```{svgbob}
        001                011
   +-----------> 01 -------------+
   |             ^|              |
   |+----+       |+----+   +----+|
   ||    |  +----+ 010 |   |    ||
   ||    |  |          |   |    ▼▼
   00    |  |          |   |    11
   ^^    |  |          |   |    || 
   ||000 |  | 101 +----+   |111 ||
   |+----+  +----+|        +----+|
   |             |v              |
   +------------ 10 <------------+
       100                110
   
   "* Cycle 1:"            00 -> 00
   "* Cycle 2:"                  00 -> 01 -------------------------> 10 -> 00
   "* Cycle 3:"                        01 -> 11 -> 11 -> 10 -> 01
   "* Merged 1 to 2 to 3:" 00 -> 00 -> 01 -> 11 -> 11 -> 10 -> 01 -> 10 -> 00

   "* k-universal string:" 0001110100
   ```

   There are multiple Eulerian cycles in the graph, meaning that there are multiple 3-universal strings:
  
   * 0001110100
   * 0011101000
   * 1110001011
   * 1100010111
   * ...
   
   For larger values of k (e.g. 20), finding k-universal strings would be too computationally intensive without De Bruijn graphs and Eulerian cycles.

 * `{bm} coverage/(coverage)_SEQ/i` - Given a substring from some larger sequence that was reconstructed from a set of fragment_SEQs, the coverage_SEQ of that substring is the number of read_SEQs used to construct it. The substring length is typically 1: the coverage_SEQ for each position of the sequence.

   ```{svgbob}
              "Read coverage for each 1-mer"
   
   "1:"        A C T A A G A              
   "2:"          C T A A G A A            
   "3:"            T A A G A A C          
   "4:"                A G A A C C T                
   "5:"                    A A C C T A A            
   "6:"                          C T A A T T T      
   "7:"                              A A T T T A G  
   "8:"                                A T T T A G C
   "String:"   A C T A A G A A C C T A A T T T A G C
   
   "Coverage:" 1 2 3 3 4 4 5 4 3 3 3 3 4 3 3 3 2 2 1
   ```

 * `{bm} read breaking/(read breaking|read-breaking|breaking reads)/i` - The concept of taking multiple read_SEQs and breaking them up into smaller read_SEQs.

   ```{svgbob}
                       "4 original 10-mers (left) broken up to perfectly overlapping 5-mers (right)"
   
   "1:"        A C T A A G A A C C --+--------------------> A C T A A                                   
                                     +-------------------->   C T A A G                                 
                                     +-------------------->     T A A G A                               
                                     +-------------------->       A A G A A                             
                                     +-------------------->         A G A A C                           
                                     +-------------------->           G A A C C                         
   "2:"              A A G A A C C T A A --+-------------->       A A G A A                             
                                           +-------------->         A G A A C                           
                                           +-------------->           G A A C C                         
                                           +-------------->             A A C C T                       
                                           +-------------->               A C C T A                     
                                           +-------------->                 C C T A A                   
   "3:"                  G A A C C T A A T T --+---------->           G A A C C                         
                                               +---------->             A A C C T                       
                                               +---------->               A C C T A                     
                                               +---------->                 C C T A A                   
                                               +---------->                   C T A A T                 
                                               +---------->                     T A A T T               
   "4:"                            T A A T T T A G C T -+->                     T A A T T               
                                                        +->                       A A T T T             
                                                        +->                         A T T T A           
                                                        +->                           T T T A G         
                                                        +->                             T T A G C       
                                                        +->                               T A G C T     
   "String:"   A C T A A G A A C C T A A T T T A G C T      A C T A A G A A C C T A A T T T A G C T     
   "Coverage:" 1 1 1 2 2 3 3 3 3 3 3 3 3 2 2 1 1 1 1 1      1 2 3 5 7 9 > > > > 9 8 7 6 6 5 4 3 2 1
   
   "* Coverage of > means more than 9."
   ```

   When read breaking, smaller k-mers result in better coverage_SEQ but also make the de Bruijn graph more tangled. The more tangled the de Bruijn graph is, the harder it is to infer the full sequence.

   In the example above, the average coverage_SEQ...

    * for the left-hand side (original) is 2.1.
    * for the right-hand side (broken) is 4.

   See also: read-pair breaking.

   ```{note}
   What purpose does this actually serve? Mimicking 1 long read_SEQ as n shorter read_SEQs isn't equivalent to actually having sequenced those n shorter read_SEQs. For example, what if the longer read_SEQ being broken up has an error? That error replicates when breaking into n shorter read_SEQs, which gives a false sense of having good coverage_SEQ and makes it seems as if it wasn't an error.
   ```

 * `{bm} read-pair breaking/(read-pair breaking|read pair breaking|breaking read-pairs|breaking read pairs)/i` - The concept of taking multiple read-pairs and breaking them up into read-pairs with a smaller k.

   ```{svgbob}
                       "4 original (4,2)-mers (left) broken up to perfectly overlapping (2,4)-mers (right)"
   
   "1:"        A C T A ‑ ‑ A A C C --+------------------> A C ‑ ‑ ‑ ‑ A A                             
                                     +------------------>   C T ‑ ‑ ‑ ‑ A C                           
                                     +------------------>     T A ‑ ‑ ‑ ‑ C C                         
   "2:"              A A G A ‑ ‑ C T A A --+------------>       A A ‑ ‑ ‑ ‑ C T                       
                                           +------------>         A G ‑ ‑ ‑ ‑ T A                     
                                           +------------>           G A ‑ ‑ ‑ ‑ A A                   
   "3:"                  G A A C ‑ ‑ A A T T --+-------->           G A ‑ ‑ ‑ ‑ A A                 
                                               +-------->             A A ‑ ‑ ‑ ‑ A T                  
                                               +-------->               A C ‑ ‑ ‑ ‑ T T               
   "4:"                          C T A A ‑ ‑ A G C T -+->                   C T ‑ ‑ ‑ ‑ A G         
                                                      +->                     T A ‑ ‑ ‑ ‑ G C         
                                                      +->                       A A ‑ ‑ ‑ ‑ C T       
   "String:"   A C T A A G A A C C T A A T T A G C T      A C T A A G A A C C T A A T T A G C T     
   "Coverage:" 1 1 1 2 1 2 3 2 2 2 2 3 3 2 1 1 1 1 1      1 2 2 2 2 3 4 4 3 3 4 5 4 2 1 1 2 2 1
   ```

   When read-pair breaking, a smaller k results in better coverage_SEQ but also make the de Bruijn graph more tangled. The more tangled the de Bruijn graph is, the harder it is to infer the full sequence.

   In the example above, the average coverage_SEQ...

    * for the left-hand side (original) is 1.6.
    * for the right-hand side (broken) is 2.5.

   See also: read breaking.

   ```{note}
   What purpose does this actually serve? Mimicking 1 long read-pair as n shorter read-pairs isn't equivalent to actually having sequenced those n shorter read-pairs. For example, what if the longer read-pair being broken up has an error? That error replicates when breaking into n shorter read-pairs, which gives a false sense of having good coverage_SEQ and makes it seems as if it wasn't an error.
   ```

 * `{bm} contig/(contig)s?\b/i/true/true` - A long continuous piece of DNA. Derived by searching a directed graph for paths that are the longest possible stretches of nodes with 1 indegree and 1 outdegree. That is, a path must either ...

   * be a cycle where each node has an indegree and outdegree of 1.
   * start and end at a node that doesn't have an indegree and outdegree of 1.

   For example, in the following de Bruijn graph, the contigs are: GTGG, GGT, and GGT:

   ```{svgbob}
       "Original"            "Contig 1: GTGG"      "Contig 2: GGT"     "Contig 3: GGT"    "Contig 4: CACCA"

           GTG                      GTG                                          
   +----------------+       +----------------+                                   
   |                |       |                |                                   
   |        +------+|       |                |        +------+                   
   |        | GGT  ||       |                |        | GGT  |                   
   v  TGG   |      v|       v  TGG           |        |      v                   
   TG ---> GG      GT       TG ---> GG      GT       GG      GT        GG      GT
            |      ^                                                    |      ^  
            | GGT  |                                                    | GGT  |  
            +------+                                                    +------+  

       CAC     ACC                                                                          CAC     ACC    
    CA ---> AC ---> CC                                                                   CA ---> AC ---> CC
    ^                |                                                                   ^                |
    |      CCA       |                                                                   |      CCA       |
    +----------------+                                                                   +----------------+
   ```
 
   Assemblies often have gaps due to...
   
    * repeats in the genome, which make it impossible to fully assemble.
    * poor coverage_SEQ, which may be cost prohibitive to fix (more read_SEQs required).
    
   As such, biologists / bioinformaticians have no choice but to settle on contigs.

 * `{bm} ribonucleotide` - Elements that make up RNA, similar to how nucleotides are the elements that make up DNA.

   * A = Adenine (same as nucleotide)
   * C = Cytosine (same as nucleotide)
   * G = Guanine (same as nucleotide)
   * U = Uracil (replace nucleotide Thymine)
  
 * `{bm} antibiotic` - A substance (typically an enzyme) for killing, preventing, or inhibiting the grow of bacterial infections.

 * `{bm} amino acid` - The building blocks of peptides / proteins, similar to how nucleotides are the building blocks of DNA.

   | 1 Letter Code | 3 Letter Code | Amino Acid                  |
   |---------------|---------------|-----------------------------|
   | A             | Ala           | Alanine                     |
   | C             | Cys           | Cysteine                    |
   | D             | Asp           | Aspartic acid               |
   | E             | Glu           | Glutamic acid               |
   | F             | Phe           | Phenylalanine               |
   | G             | Gly           | Glycine                     |
   | H             | His           | Histidine                   |
   | I             | Ile           | Isoleucine                  |
   | K             | Lys           | Lysine                      |
   | L             | Leu           | Leucine                     |
   | M             | Met           | Methionine                  |
   | N             | Asn           | Asparagine                  |
   | P             | Pro           | Proline                     |
   | Q             | Gln           | Glutamine                   |
   | R             | Arg           | Arginine                    |
   | S             | Ser           | Serine                      |
   | T             | Thr           | Threonine                   |
   | V             | Val           | Valine                      |
   | W             | Trp           | Tryptophan                  |
   | Y             | Tyr           | Tyrosine                    |

 * `{bm} peptide` - A short amino acid chain of at least size two. Peptides are considered miniature proteins, but when something should be called a peptide vs a protein is loosely defined: the cut-off is anywhere between 50 to 100 amino acids.
 
 * `{bm} polypeptide` - A peptide of at least size 10.

 * `{bm} cyclopeptide` - A cyclic peptide.

 * `{bm} central dogma of molecular biology` - The overall concept of transcription and translation: Instructions for making a protein are copied from DNA to RNA, then RNA feeds into the ribosome to make that protein (DNA → RNA → Protein).

   Most, not all, peptides are synthesized as described above. Non-ribosomal peptides are synthesized outside of the transcription and translation.

 * `{bm} non-ribosomal peptide` `{bm} /\b(NRP)\b/i` - A peptide that was synthesized by a protein called NRP synthetase rather than synthesized by a ribosome. NRP synthethase builds peptides one amino acid at a time without relying on transcription or translation.

   Non-ribosomal peptides may be cyclic. Common use-cases for non-ribosomal peptides:

   * antibiotics
   * anti-tumor agents
   * immunosuppressors
   * communication between bacteria (quorum sensing)

 * `{bm} mass spectrometer/(mass spectrometer|mass spectrometry)/i` - A device that shatters molecules into pieces and weighs the resulting pieces (measured in daltons). Mass spectrometry can be used to sequence peptides by inferring the amino acid sequence from the collection of masses.

 * `{bm} experimental spectrum` - Given a shattered molecule, a collection consisting of the each piece's mass as measured by a mass spectrometer. For example, given the peptide ACDEFG, the experimental spectrum may be...

   * mass(A)
   * mass(AC)
   * mass(ACD)
   * mass(ACDE)
   * mass(ACDEF)

   Experimental spectrum are the masses returned from an actual mass spectrometry experiment, while theoretical spectrum are all possible masses for a mass spectrometry experiment.

 * `{bm} theoretical spectrum` - A collection consisting of all possible masses measurable by a mass spectrometer in addition to 0 and the mass of the entire molecule being measured. For example, given the peptide ACDEFG, the theoretical spectrum would be...

   * mass() = 0
   * mass(A)
   * mass(AC)
   * mass(ACD)
   * mass(ACDE)
   * mass(ACDEF)
   * mass(ACDEFG)

   Experimental spectrum are the masses returned from an actual mass spectrometry experiment, while theoretical spectrum are all possible masses for a mass spectrometry experiment.

 * `{bm} ideal spectrum` - When the experimental spectrum matches the theoretical spectrum.

 * `{bm} dalton` `{bm} /\b(Da)\b/i` - A unit of measurement used in physics and chemistry. 1 Dalton is approximately the mass of a single proton / neutron, derived by taking the mass of a carbon-12 atom and dividing it by 12.

 * `{bm} codon/(codon|genetic code)/i` - A sequence of 3 ribonucleotides that maps to an amino acid or a stop marker. During translation, the ribosome translates the RNA to a protein 3 ribonucleotides at a time:

   ```{note}
   The stop marker tells the ribosome to stop translating / the protein is complete.
   ```

   ```{note}
   The codons are listed as ribonucleotides (RNA). For nucleotides (DNA), swap U with T.
   ```

   | 1 Letter Code | 3 Letter Code | Amino Acid                  | Codons                       |
   |---------------|---------------|-----------------------------|------------------------------|
   | A             | Ala           | Alanine                     | GCA, GCC, GCG, GCU           |
   | C             | Cys           | Cysteine                    | UGC, UGU                     |
   | D             | Asp           | Aspartic acid               | GAC, GAU                     |
   | E             | Glu           | Glutamic acid               | GAA, GAG                     |
   | F             | Phe           | Phenylalanine               | UUC, UUU                     |
   | G             | Gly           | Glycine                     | GGA, GGC, GGG, GGU           |
   | H             | His           | Histidine                   | CAC, CAU                     |
   | I             | Ile           | Isoleucine                  | AUA, AUC, AUU                |
   | K             | Lys           | Lysine                      | AAA, AAG                     |
   | L             | Leu           | Leucine                     | CUA, CUC, CUG, CUU, UUA, UUG |
   | M             | Met           | Methionine                  | AUG                          |
   | N             | Asn           | Asparagine                  | AAC, AAU                     |
   | P             | Pro           | Proline                     | CCA, CCC, CCG, CCU           |
   | Q             | Gln           | Glutamine                   | CAA, CAG                     |
   | R             | Arg           | Arginine                    | AGA, AGG, CGA, CGC, CGG, CGU |
   | S             | Ser           | Serine                      | AGC, AGU, UCA, UCC, UCG, UCU |
   | T             | Thr           | Threonine                   | ACA, ACC, ACG, ACU           |
   | V             | Val           | Valine                      | GUA, GUC, GUG, GUU           |
   | W             | Trp           | Tryptophan                  | UGG                          |
   | Y             | Tyr           | Tyrosine                    | UAC, UAU                     |
   | *             | * 	           | **STOP**                    | UAA, UAG, UGA                |

 * `{bm} reading frame` - The different ways of dividing a DNA string into codons. Specifically, there are 6 different ways that a DNA string can be divided into codons:

    * You can start dividing at index 0, 1, or 2.
    * You can divide either the DNA string itself or the reverse complementing DNA string.
 
   For example, given the the string ATGTTCCATTAA, the the following codon division are possible:

    | DNA          | Start Index | Discard Prefix | Codons             | Discard Suffix |
    |--------------|-------------|----------------|--------------------|----------------|
    | ATGTTCCATTAA | 0           |                | ATG, TTC, CAT, TAA |                |
    | ATGTTCCATTAA | 1           | A              | TGT, TCC, ATT      | AA             |
    | ATGTTCCATTAA | 2           | AT             | GTT, CCA, TTA      | A              |
    | TTAATGGAACAT | 0           |                | TTA, ATG, GAA, CAT |                |
    | TTAATGGAACAT | 1           | T              | TAA, TGG, AAC      | AT             |
    | TTAATGGAACAT | 2           | TT             | AAT, GGA, ACA      | T              |
    
   ```{note}
   TTAATGGAACAT is the reverse complement of ATGTTCCATTAA.
   ```

 * `{bm} encode/(encode|encoding|decode|decoding)/i` - When a DNA string or its reverse complement is made up of the codons required for an amino acid sequence. For example, ACAGTA encodes for the amino acid sequence...

    * Threonine-Valine
    * Tyrosine-Cysteine (derived from reverse complement)
    
 * `{bm} branch-and-bound algorithm/(branch-and-bound algorithm|branch and bound algorithm)/i` - A bruteforce algorithm that enumerates candidates to explore at each step but also discards untenable candidates using various checks. The enumeration of candidates is the branching step, while the culling of untenable candidates is the bounding step.

`{bm-ignore} \b(read)_NORM/i`
`{bm-error} Apply suffix _NORM or _SEQ/\b(read)/i`

`{bm-ignore} \b(member)_NORM/i`
`{bm-error} Apply suffix _NORM or _MOTIF/\b(member)/i`

`{bm-ignore} (balanced)_NORM/i`
`{bm-error} Apply suffix _NORM, _GRAPH, or _NODE/(balanced)/i`

`{bm-ignore} (coverage)_NORM/i`
`{bm-error} Apply suffix _NORM, _SEQ/(coverage)/i`

`{bm-ignore} (fragment)_NORM/i`
`{bm-error} Apply suffix _NORM, _SEQ/(fragment)/i`

`{bm-ignore} (Eulerian)_NORM/i`
`{bm-error} Apply suffix _PATH, _CYCLE, _GRAPH, or _NORM/(Eulerian)/i`

`{bm-error} Missing topic reference/(_TOPIC)/i`
`{bm-error} Use you instead of we/\b(we)\b/i`