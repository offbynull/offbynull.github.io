```{title}
Bioinformatics Algorithms
```

```{toc}
```

# Introduction

Bioinformatics is the science of transforming and processing biological data to gain new insights, particularly omics data: genomics, proteomics, metabolomics, etc.. Bioinformatics is mostly a mix of biology, computer science, and statistics / data science.

# Algorithms

## K-mer

`{bm} /(Algorithms\/K-mer)_TOPIC/`

A k-mer is a substring of length k within some larger biological sequence (e.g. DNA or amino acid chain). For example, in the DNA sequence GAAATC, the following k-mer's exist:

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

**WHY**: An enzyme may need to bind to a specific region of DNA to begin doing its job. That is, it looks for a specific k-mer pattern to bind to, where that k-mer represents the beginning of some larger DNA region that it operates on. Since DNA is known to mutate, oftentimes you'll find multiple copies of the same k-mer pattern clustered together -- if one copy mutated to become unusable, the other copies are still around.

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

**WHY**: An enzyme may need to bind to a specific region of DNA to begin doing its job. That is, it looks for a specific k-mer pattern to bind to, where that k-mer represents the beginning of some larger DNA region that it operates on. Since DNA is known to mutate, oftentimes you'll find multiple copies of the same k-mer pattern clustered together -- if one copy mutated to become unusable, the other copies are still around.

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

**WHY**: An enzyme may need to bind to a specific region of DNA to begin doing its job. That is, it looks for a specific k-mer pattern to bind to, where that k-mer represents the beginning of some larger DNA region that it operates on. Since DNA is known to mutate, oftentimes you'll find multiple copies of the same k-mer pattern clustered together -- if one copy mutated to become unusable, the other copies are still around.

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

Of these two k-mers, ...

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

A single transcription factor may operate on many different genes. Oftentimes a scientist will identify a set of genes that are suspected to be regulated by a single transcription factor, but that scientist won't know ...

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

In practice, this algorithm may trip up on real-world data. Real-world sequences don't actually contain random noise. The hope is that the only k-mers that are highly similar to each other in the sequences are member_MOTIFs of the motif. It's possible that the sequences contain other sets of k-mers that are similar to each other but vastly different from the motif members. In such cases, even if a motif member were to be selected when creating the initial motif matrix, the algorithm may converge to a motif matrix that isn't for the motif.

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

## DNA Assembly

`{bm} /(Algorithms\/DNA Assembly)_TOPIC/`

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
                                                          
   +-------+                   A T T T T            
   |A T T T|T A ------+
   +-------+          +------> A T T T  
     +-------+       +---------> T T T T       
    A|T T T T|A -----+                   
     +-------+                               

    A T T C T A ------>?

   "* Reconstructed genome is missing the final A."
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

`{bm} /(Algorithms\/DNA Assembly\/Stitch Reads)_TOPIC/`

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

```{note}
See also: Algorithms/Sequence Alignment/Overlap Alignment_TOPIC
```

### Stitch Read-Pairs

`{bm} /(Algorithms\/DNA Assembly\/Stitch Read-Pairs)_TOPIC/`

```{prereq}
Algorithms/DNA Assembly/Stitch Reads_TOPIC
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

```{note}
See also: Algorithms/Sequence Alignment/Overlap Alignment_TOPIC
```

### Break Reads

`{bm} /(Algorithms\/DNA Assembly\/Break Reads)_TOPIC/`

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

`{bm} /(Algorithms\/DNA Assembly\/Break Read-Pairs)_TOPIC/`

```{prereq}
Algorithms/DNA Assembly/Break Reads_TOPIC
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

`{bm} /(Algorithms\/DNA Assembly\/Probability of Fragment Occurrence)_TOPIC/`

```{prereq}
Algorithms/DNA Assembly/Stitch Reads_TOPIC
Algorithms/DNA Assembly/Stitch Read-Pairs_TOPIC
Algorithms/DNA Assembly/Break Reads_TOPIC
Algorithms/DNA Assembly/Break Read-Pairs_TOPIC
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

`{bm} /(Algorithms\/DNA Assembly\/Overlap Graph)_TOPIC/`

```{prereq}
Algorithms/DNA Assembly/Stitch Reads_TOPIC
Algorithms/DNA Assembly/Stitch Read-Pairs_TOPIC
Algorithms/DNA Assembly/Break Reads_TOPIC
Algorithms/DNA Assembly/Break Read-Pairs_TOPIC
Algorithms/DNA Assembly/Probability of Fragment Occurrence_TOPIC
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

**WHY**: An overlap graph shows the different ways that fragment_SEQs can be stitched together. A path in an overlap graph that touches each node exactly once is one possibility for the original single stranded DNA that the fragment_SEQs came from. For example...

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
 * Fragment_SEQs may have inconsistent coverage_SEQ (sequencer captured it too many/few times).
 * Fragment_SEQs may be repeated (regions of the genome may repeat).
 * Fragment_SEQs may have errors (sequencer produced sequencing errors).
 * Fragment_SEQs may be stitch-able in more than one way (multiple genome reconstruction guesses).
 * Fragment_SEQs may take a long time to stitch (computationally intensive).

Nevertheless, in an ideal world where most of these problems don't exist, an overlap graph is a good way to guess the single-strand of DNA that a set of fragment_SEQs came from. An overlap graph assumes that the fragment_SEQs it's operating on ...

 * are from a single-strand of DNA,
 * have correct occurrence counts (no missing or extra),
 * and contain no errors.

```{note}
Although the complications discussed above make it impossible to get the original genome in its entirety, it's still possible to pull out large parts of the original genome. This is discussed in Algorithms/DNA Assembly/Find Contigs_TOPIC.
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

`{bm} /(Algorithms\/DNA Assembly\/De Bruijn Graph)_TOPIC/`

```{prereq}
Algorithms/DNA Assembly/Stitch Reads_TOPIC
Algorithms/DNA Assembly/Stitch Read-Pairs_TOPIC
Algorithms/DNA Assembly/Break Reads_TOPIC
Algorithms/DNA Assembly/Break Read-Pairs_TOPIC
Algorithms/DNA Assembly/Probability of Fragment Occurrence_TOPIC
Algorithms/DNA Assembly/Overlap Graph_TOPIC
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

In contrast to finding a Hamiltonian path in an overlap graph, it's much faster to find an Eulerian cycle in a de Bruijn graph.

De Bruijn graphs were originally invented to solve the k-universal string problem, which is effectively the same concept as assembly.

**ALGORITHM**:

Sequencers produce fragment_SEQs, but fragment_SEQs by themselves typically aren't enough for most experiments / algorithms. In theory, stitching overlapping fragment_SEQs for a single-strand of DNA should reveal that single-strand of DNA. In practice, real-world complications make revealing that single-strand of DNA nearly impossible:

 * Fragment_SEQs are for both strands (strand of double-stranded DNA a fragment_SEQ's from isn't known).
 * Fragment_SEQs may be missing (sequencer didn't capture it).
 * Fragment_SEQs may have inconsistent coverage_SEQ (sequencer captured it too many/few times).
 * Fragment_SEQs may be repeated (regions of the genome may repeat).
 * Fragment_SEQs may have errors (sequencer produced sequencing errors).
 * Fragment_SEQs may be stitch-able in more than one way (multiple genome reconstruction guesses).
 * Fragment_SEQs may take a long time to stitch (computationally intensive).

Nevertheless, in an ideal world where most of these problems don't exist, a de Bruijn graph is a good way to guess the single-strand of DNA that a set of fragment_SEQs came from. A de Bruijn graph assumes that the fragment_SEQs it's operating on ...

 * are from a single-strand of DNA,
 * have correct occurrence counts (no missing or extra),
 * and contain no errors.

```{note}
Although the complications discussed above make it impossible to get the original genome in its entirety, it's still possible to pull out large parts of the original genome. This is discussed in Algorithms/DNA Assembly/Find Contigs_TOPIC.
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

Note how the graph above is both balanced_GRAPH and strongly connected. In most cases, non-circular genomes won't generate a balanced graph like the one above. Instead, a non-circular genome will very likely generate a graph that's nearly balanced_GRAPH: Nearly balanced graphs are graphs that would be balanced_GRAPH if not for a few unbalanced nodes (usually root and tail nodes). They can artificially be made to become balanced_GRAPH by finding imbalanced nodes and creating artificial edges between them until they become balanced nodes.

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

`{bm} /(Algorithms\/DNA Assembly\/Find Bubbles)_TOPIC/`

```{prereq}
Algorithms/DNA Assembly/Overlap Graph_TOPIC
Algorithms/DNA Assembly/De Bruijn Graph_TOPIC
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

Note that just because these structures exist doesn't mean that the fragment_SEQs they represent definitively have sequencing errors. These structures could have been caused by other problems / may not be problems at all:

 * Bubbles may be caused by repetitive regions of DNA: Fragment_SEQs from different parts of the genome that are the same except for a few positions will show up as bubbles.
 * Bubbles / forks may be caused when sequencing double-stranded DNA: When both strands of DNA get tangled into the same graph, it's possible that fragment_SEQs from different strands form bubbles or forks.

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

`{bm} /(Algorithms\/DNA Assembly\/Find Contigs)_TOPIC/`

```{prereq}
Algorithms/DNA Assembly/Overlap Graph_TOPIC
Algorithms/DNA Assembly/De Bruijn Graph_TOPIC
Algorithms/DNA Assembly/Find Bubbles_TOPIC
```

**WHAT**: Given an overlap graph or de Bruijn graph, find the longest possible stretches of non-branching nodes. Each stretch will be a path that's either  ...

 * a line: each node has an indegree and outdegree of 1.

   ```{svgbob}
   GT --> TG --> GG
   ```

 * a cycle: each node has an indegree and outdegree of 1 and it loops.

   ```{svgbob}
   CA ---> AC ---> CC 
   ^                |
   |                |
   `----------------'
   ```

 * a line sandwiched between branching nodes: nodes in between have an indegree and outdegree of 1 but either...
   * starts at a node where indegree != 1 but outdegree == 1 (incoming branch),
   * or ends at a node where indegree == 1 but outdegree != 1 (outgoing branch),
   * or both.

   ```{svgbob}
   -.                 
    |              .->
    v              |
    GT --> TG --> GG
    ^              |
    |              `->
   -'
   ```

Each found path is called a contig: a contiguous piece of the graph. For example, ...

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

**WHY**: An overlap graph / de Bruijn graph represents all the possible ways a set of fragment_SEQs may be stitched together to infer the full genome. However, real-world complications make it impractical to guess the full genome:

 * Fragment_SEQs are for both strands (strand of double-stranded DNA a fragment_SEQ's from isn't known).
 * Fragment_SEQs may be missing (sequencer didn't capture it).
 * Fragment_SEQs may have inconsistent coverage_SEQ (sequencer captured it too many/few times).
 * Fragment_SEQs may be repeated (regions of the genome may repeat).
 * Fragment_SEQs may have errors (sequencer produced sequencing errors).
 * Fragment_SEQs may be stitch-able in more than one way (multiple genome reconstruction guesses).
 * Fragment_SEQs may take a long time to stitch (computationally intensive).

These complications result in graphs that are too tangled, disconnected, etc... As such, the best someone can do is to pull out the contigs in the graph: unambiguous stretches of DNA.

**ALGORITHM**:

```{output}
ch3_code/src/FindContigs.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch3}
FindContigs
reads
TGG
GGT
GGT
GTG
CAC
ACC
CCA
```

## Peptide Sequence

`{bm} /(Algorithms\/Peptide Sequence)_TOPIC/`

```{prereq}
Algorithms/K-mer_TOPIC
```

A peptide is a miniature protein consisting of a chain of amino acids anywhere between 2 to 100 amino acids in length. Peptides are created through two mechanisms:

 1. ribosomal peptides: DNA gets transcribed to mRNA (transcription), which in turn gets translated by the ribosome into a peptide (translation).

    ```{svgbob}
      DNA
       |
       | transcribed
       |
       v
     mRNA
       |
       | translated
       |
       v
    peptide
    ```

 2. non-ribosomal peptides: proteins called NRP synthetase construct peptides one amino acid at a time.

    ```{svgbob}
    .------------.   .------------.   .------------.   .------------.   .------------.
    |   NRP      |   |   NRP      |   |   NRP      |   |   NRP      |   |   NRP      |
    | synthetase |   | synthetase |   | synthetase |   | synthetase |   | synthetase |
    `----. .-----'   `----. .-----'   `----. .-----'   `----. .-----'   `----. .-----'
          N                K                S                N                G       
                           |                |                |                |
                           N                K                S                N
                                            |                |                |
                                            N                K                S
                                                             |                |
                                                             N                K
                                                                              |
                                                                              N
    ```

For ribosomal peptides, each amino acid is encoded as a DNA sequence of length 3. This 3 length DNA sequence is referred to as a codon. By knowing which codons map to which amino acids, the ...

 * peptide sequence can be determined by mapping from DNA to codons (you know the peptide just by looking at the DNA).
 * peptide sequence can be searched for in DNA by finding codons (you can see if the peptide is encoded in a genome).

For non-ribosomal peptides, a sample of the peptide needs to be isolated and passed through a mass spectrometer. A mass spectrometer is a device that shatters and bins molecules by their mass-to-charge ratio: Given a sample of molecules, the device randomly shatters each molecule in the sample (forming ions), then bins each ion by its mass-to-charge ratio (`{kt} \frac{m}{z}`).

The output of a mass spectrometer is a plot called a spectrum_MS. The plot's ...

 * x-axis is the mass-to-charge ratio.
 * y-axis is the intensity of that mass-to-charge ratio (how much more / less did that mass-to-charge appear compared to the others).

```{svgbob}
    y
    ^
    |
    |        |
    |        |
"%" |        |
    |        | |           |
    |        | |           |
    | |      | | |         |        |
    | | | |  | | |     |   |    | | |
    +-+-+-+--+-+-+-----+---+----+-+-+--> x
                     "m/z"
```

For example, given a sample containing multiple instances of the linear peptide NQY, the mass spectrometer will take each instance of NQY and randomly break the bonds between its amino acids:

```{svgbob}
N ---- Q ---- Y   "(NQY not broken)"

N -//- Q ---- Y   "(NQY broken to N and QY)"

N ---- Q -//- Y   "(NQY broken to NQ and Y)"

N -//- Q -//- Y   "(NQY broken to N, Q, and Y)"
```

```{note}
How does it know to break the bonds holding amino acids together and not bonds within the amino acids themselves? My guess is that the bonds coupling one amino acid to another are much weaker than the bonds holding an individual amino acid together -- it's more likely that the weaker bonds will be broken.
```

Each subpeptide then will have its mass-to-charge ratio measured, which in turn gets converted to a set of potential masses by performing basic math. With these potential masses, it's possible to infer the sequence of the peptide.

Special consideration needs to be given to the real-world practical problems with mass spectrometry. Specifically, the spectrum_MS given back by a mass spectrometer will very likely ...

 * miss mass-to-charge ratios for some fragment_NORMs of the intended molecule (missing entries).
 * include mass-to-charge ratios for fragment_NORMs of unintended molecules (faulty entries).
 * have noisy mass-to-charge ratios.

The following table contains a list of proteinogenic amino acids with their masses and codon mappings:

| 1 Letter Code | 3 Letter Code | Amino Acid                  | Codons                       | Monoisotopic Mass (daltons) |
|---------------|---------------|-----------------------------|------------------------------|-----------------------------|
| A             | Ala           | Alanine                     | GCA, GCC, GCG, GCU           | 71.04                       |
| C             | Cys           | Cysteine                    | UGC, UGU                     | 103.01                      |
| D             | Asp           | Aspartic acid               | GAC, GAU                     | 115.03                      |
| E             | Glu           | Glutamic acid               | GAA, GAG                     | 129.04                      |
| F             | Phe           | Phenylalanine               | UUC, UUU                     | 147.07                      |
| G             | Gly           | Glycine                     | GGA, GGC, GGG, GGU           | 57.02                       |
| H             | His           | Histidine                   | CAC, CAU                     | 137.06                      |
| I             | Ile           | Isoleucine                  | AUA, AUC, AUU                | 113.08                      |
| K             | Lys           | Lysine                      | AAA, AAG                     | 128.09                      |
| L             | Leu           | Leucine                     | CUA, CUC, CUG, CUU, UUA, UUG | 113.08                      |
| M             | Met           | Methionine                  | AUG                          | 131.04                      |
| N             | Asn           | Asparagine                  | AAC, AAU                     | 114.04                      |
| P             | Pro           | Proline                     | CCA, CCC, CCG, CCU           | 97.05                       |
| Q             | Gln           | Glutamine                   | CAA, CAG                     | 128.06                      |
| R             | Arg           | Arginine                    | AGA, AGG, CGA, CGC, CGG, CGU | 156.1                       |
| S             | Ser           | Serine                      | AGC, AGU, UCA, UCC, UCG, UCU | 87.03                       |
| T             | Thr           | Threonine                   | ACA, ACC, ACG, ACU           | 101.05                      |
| V             | Val           | Valine                      | GUA, GUC, GUG, GUU           | 99.07                       |
| W             | Trp           | Tryptophan                  | UGG                          | 186.08                      |
| Y             | Tyr           | Tyrosine                    | UAC, UAU                     | 163.06                      |
| *             | * 	          | **STOP**                    | UAA, UAG, UGA                |                             |

```{note}
The stop marker tells the ribosome to stop translating / the protein is complete. The codons are listed as ribonucleotides (RNA). For nucleotides (DNA), swap U with T.
```

### Codon Encode

**WHAT**: Given a DNA sequence, map each codon to the amino acid it represents. In total, there are 6 different ways that a DNA sequence could be translated:

 1. Since the length of a codon is 3, the encoding of the peptide could start from offset 0, 1, or 2 (referred to as reading frames).
 2. Since DNA is double stranded, either the DNA sequence or its reverse complement could represent the peptide.

**WHY**: The composition of a peptide can be determined from the DNA sequence that encodes it.

**ALGORITHM**:

```{output}
ch4_code/src/helpers/AminoAcidUtils.py
python
# MARKDOWN_CODON\s*\n([\s\S]+)\n\s*# MARKDOWN_CODON
```

```{output}
ch4_code/src/EncodePeptide.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch4}
EncodePeptide
AAAAGAACCTAATCTTAAAGGAGATGATGATTCTAA
```

### Codon Decode

**WHAT**: Given a peptide, map each amino acid to the DNA sequences it represents. Since each amino acid can map to multiple codons, there may be multiple DNA sequences for a single peptide.

**WHY**: The DNA sequences that encode a peptide can be determined from the peptide itself.

**ALGORITHM**:

```{output}
ch4_code/src/helpers/AminoAcidUtils.py
python
# MARKDOWN_CODON\s*\n([\s\S]+)\n\s*# MARKDOWN_CODON
```

```{output}
ch4_code/src/DecodePeptide.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch4}
DecodePeptide
NQY
```

### Experimental Spectrum

`{bm} /(Algorithms\/Peptide Sequence\/Experimental Spectrum)_TOPIC/`

**WHAT**: Given a spectrum_MS for a peptide, derive a set of potential masses from the mass-to-charge ratios. These potential masses are referred to as an experimental spectrum.

**WHY**: A peptide's sequence can be inferred from a list of its potential subpeptide masses.

**ALGORITHM**:

Prior to deriving masses from a spectrum_MS, filter out low intensity mass-to-charge ratios. The remaining mass-to-charge ratios are converted to potential masses using `{kt} \frac{m}{z} \cdot z = m`.

For example, consider a mass spectrometer that has a tendency to produce +1 and +2 ions. This mass spectrometer produces the following mass-to-charge ratios: \[100, 150, 250\]. Each mass-to-charge ratio from this mass spectrometer will be converted to two possible masses:

 * 100 ⟶ \[100Da, 200Da\]
 * 150 ⟶ \[150Da, 300Da\]
 * 250 ⟶ \[250Da, 500Da\]

It's impossible to know which mass is correct, so all masses are included in the experimental spectrum:

\[100Da, 150Da, 200Da, 250Da, 300Da, 500Da\].

```{output}
ch4_code/src/ExperimentalSpectrum.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch4}
ExperimentalSpectrum
100 150 250
+1 +2
```

```{note}
The following section isn't from the Pevzner book or any online resources. I came up with it in an effort to solve the final assignment for Chapter 4 (the chapter on non-ribosomal peptide sequencing). As such, it might not be entirely correct / there may be better ways to do this.
```

Just as a spectrum_MS is noisy, the experimental spectrum derived from a spectrum_MS is also noisy. For example, consider a mass spectrometer that produces up to ±0.5 noise per mass-to-charge ratio and has a tendency to produce +1 and +2 charges. A real mass of 100Da measured by this mass spectrometer will end up in the spectrum_MS as a mass-to-charge ratio of either...

 * for +1 charge, anywhere between 99.5 to 100.5 (calculated as `{kt} \frac{100}{1} - 0.5` to `{kt} \frac{100}{1} + 0.5`).
 * for +2 charge, anywhere between 49.5 to 50.5 (calculated as `{kt} \frac{100}{2} - 0.5` to `{kt} \frac{100}{2} + 0.5`).

Converting these mass-to-charge ratio ranges to mass ranges...

 * for +1 charge, anywhere between 99.5Da to 100.5Da (calculated as `{kt} 99.5 \cdot 1` to `{kt} 100.5 \cdot 1`).
 * for +2 charge, anywhere between 99Da to 101Da (calculated as `{kt} 49.5 \cdot 2` to `{kt} 50.5 \cdot 2`).

Note how the +2 charge conversion produces the widest range: 100Da ± 1Da. Any real mass measured by this mass spectrometer will end up in the experimental spectrum with up to ±1Da noise. For example, a real mass of ...

 * 99Da will show up in the experimental spectrum anywhere between 98Da and 100Da.
 * 100Da will show up in the experimental spectrum anywhere between 99Da to 101Da.
 * 101Da will show up in the experimental spectrum anywhere between 100Da to 102Da.

```{svgbob}
r     |
e 101 |                 *-------------*
a     |
l     |
  100 |          *-------------*
m     |
a     |
s 99  |   *-------------*
s     |
      +---+------+------+------+------+
         98     99     100    101    102
                    "exp mass"
```

Similarly, any mass in the experimental spectrum could have come from a real mass within ±1Da of it. For example, an experimental spectrum mass of 100Da could have come from a real mass of anywhere between 99Da to 101Da: At a real mass of ...

 * 99Da, the corresponding experimental spectrum mass range's maximum is 100Da (98Da to 100Da).
 * 100Da, the corresponding experimental spectrum mass range's middle is 100Da (99Da to 101Da).
 * 101Da, the corresponding experimental spectrum mass range's minimum is 100Da: (100Da to 102Da).

```{svgbob}                
r     |                  
e 101 |                 *-------------*
a     |                 :
l     |                 :
  100 |          *------+------*
m     |                 :
a     |                 :
s 99  |   *-------------*
s     |                  
      +---+------+------+------+------+
         98     99     100    101    102
                    "exp mass"
```

As such, the maximum amount of noise for a real mass that made its way into the experimental spectrum is the same as the tolerance required for mapping an experimental spectrum mass back to the real mass it came from. This tolerance can also be considered noise: the experimental spectrum mass is offset from the real mass that it came from.

```{output}
ch4_code/src/ExperimentalSpectrumNoise.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch4}
ExperimentalSpectrumNoise
0.5
+1 +2
```

### Theoretical Spectrum

`{bm} /(Algorithms\/Peptide Sequence\/Theoretical Spectrum)_TOPIC/`

```{prereq}
Algorithms/Peptide Sequence/Experimental Spectrum_TOPIC
```

**WHAT**: A theoretical spectrum is an algorithmically generated list of all subpeptide masses for a known peptide sequence (including 0 and the full peptide's mass).

For example, linear peptide NQY has the theoretical spectrum...

```python
theo_spec = [
  0,    # <empty>
  114,  # N
  128,  # Q
  163,  # Y
  242,  # NQ
  291,  # QY
  405   # NQY
]
```

... while experimental spectrum produced by feeding NQY to a mass spectrometer may look something like...

```python
exp_spec = [
  0.0,    # <empty> (implied)
  113.9,  # N
  115.1,  # N
          # Q missing
  136.2,  # faulty
  162.9,  # Y
  242.0,  # NQ
          # QY missing
  311.1,  # faulty
  346.0,  # faulty
  405.2   # NQY
]
```

The theoretical spectrum is what the experimental spectrum would be in a perfect world...

 * only a single possible mass for each mass-to-charge ratio.
 * no missing masses.
 * no faulty masses.
 * no noise.

**WHY**: The closer a theoretical spectrum is to an experimental spectrum, the more likely it is that the peptide sequence used to generate that theoretical spectrum is related to the peptide sequence that produced that experimental spectrum. This is the basis for how non-ribosomal peptides are sequenced: an experimental spectrum is produced by a mass spectrometer, then that experimental spectrum is compared against a set of theoretical spectrums.

#### Bruteforce Algorithm

`{bm} /(Algorithms\/Peptide Sequence\/Theoretical Spectrum\/Bruteforce Algorithm)_TOPIC/`

**ALGORITHM**:

The following algorithm generates a theoretical spectrum in the most obvious way: iterate over each subpeptide and calculate its mass.

```{output}
ch4_code/src/TheoreticalSpectrum_Bruteforce.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch4}
TheoreticalSpectrum_Bruteforce
NQY
linear
G: 57, A: 71, S: 87, P: 97, V: 99, T: 101, C: 103, I: 113, L: 113, N: 114, D: 115, K: 128, Q: 128, E: 129, M: 131, H: 137, F: 147, R: 156, Y: 163, W: 186
```

#### Prefix Sum Algorithm

`{bm} /(Algorithms\/Peptide Sequence\/Theoretical Spectrum\/Prefix Sum Algorithm)_TOPIC/`

```{prereq}
Algorithms/Peptide Sequence/Theoretical Spectrum/Bruteforce Algorithm_TOPIC
```

**ALGORITHM**:

The algorithm starts by calculating the prefix sum of the mass at each position of the peptide. The prefix sum is calculated by summing all amino acid masses up until that position. For example, the peptide GASP has the following masses at the following positions...

| G  | A  | S  | P  |
|----|----|----|----|
| 57 | 71 | 87 | 97 |

As such, the prefix sum at each position is...

|                    | G       | A           | S              | P                 |
|--------------------|---------|-------------|----------------|-------------------|
| Mass               | 57      | 71          | 87             | 97                |
| Prefix sum of mass | 57=57   | 57+71=128   | 57+71+87=215   | 57+71+87+97=312   |

```python
prefixsum_masses[0] = mass['']     = 0             = 0   # Artificially added
prefixsum_masses[1] = mass['G']    = 0+57          = 57
prefixsum_masses[2] = mass['GA']   = 0+57+71       = 128
prefixsum_masses[3] = mass['GAS']  = 0+57+71+87    = 215
prefixsum_masses[4] = mass['GASP'] = 0+57+71+87+97 = 312
```

The mass for each subpeptide can be derived from just these prefix sums. For example, ...

```python
mass['GASP'] = mass['GASP'] - mass['']    = prefixsum_masses[4] - prefixsum_masses[0]
mass['ASP']  = mass['GASP'] - mass['G']   = prefixsum_masses[4] - prefixsum_masses[1]
mass['AS']   = mass['GAS']  - mass['G']   = prefixsum_masses[3] - prefixsum_masses[1]
mass['A']    = mass['GA']   - mass['G']   = prefixsum_masses[2] - prefixsum_masses[1]
mass['S']    = mass['GAS']  - mass['GA']  = prefixsum_masses[3] - prefixsum_masses[2]
mass['P']    = mass['GASP'] - mass['GAS'] = prefixsum_masses[4] - prefixsum_masses[3]
# etc...
```
   
If the peptide is a cyclic peptide, some subpeptides will wrap around. For example, PG is a valid subpeptide if GASP is a cyclic peptide:

```{svgbob}
S ---> P
^      |
|      v
A <--- G 
```

The prefix sum can be used to calculate these wrapping subpeptides as well. For example...

```python
mass['PG'] = mass['GASP'] - mass['AS']
           = mass['GASP'] - (mass['GAS'] - mass['G'])    # SUBSTITUTE IN mass['AS'] CALC FROM ABOVE
           = prefixsum_masses[4] - (prefixsum_masses[3] - prefixsum_masses[1])
```

This algorithm is faster than the bruteforce algorithm, but most use-cases won't notice a performance improvement unless either the...

 * peptide is very long (likely won't happen since peptides by definition aren't larger than 50 to 100 amino acids)
 * algorithm runs often.

```{output}
ch4_code/src/TheoreticalSpectrum_PrefixSum.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch4}
TheoreticalSpectrum_PrefixSum
NQY
linear
G: 57, A: 71, S: 87, P: 97, V: 99, T: 101, C: 103, I: 113, L: 113, N: 114, D: 115, K: 128, Q: 128, E: 129, M: 131, H: 137, F: 147, R: 156, Y: 163, W: 186
```

```{note}
The algorithm above is serial, but it can be made parallel to get even more speed:

 1. Parallelized prefix sum (e.g. Hillis-Steele / Blelloch).
 2. Parallelized iteration instead of nested for-loops.
 3. Parallelized sorting (e.g. Parallel merge sort / Parallel brick sort / Bitonic sort).
```

### Spectrum Convolution

`{bm} /(Algorithms\/Peptide Sequence\/Spectrum Convolution)_TOPIC/`

```{prereq}
Algorithms/Peptide Sequence/Experimental Spectrum_TOPIC
Algorithms/Peptide Sequence/Theoretical Spectrum_TOPIC
```

**WHAT**: Given an experimental spectrum, subtract its masses from each other. The differences are a set of potential amino acid masses for the peptide that generated that experimental spectrum.

For example, the following experimental spectrum is for the linear peptide NQY:

[0.0Da, 113.9Da, 115.1Da, 136.2Da, 162.9Da, 242.0Da, 311.1Da, 346.0Da, 405.2Da]

Performing 242.0 - 113.9 results in 128.1, which is very close to the mass for amino acid Q. The mass for Q was derived even though no experimental spectrum masses are near Q's mass:

 * Mass of N is 114Da, 2 experimental spectrum masses are near: \[113.9, 115.1\]
 * Mass of Q is 128Da, 0 experimental spectrum masses are near: \[\]
 * Mass of Y is 163Da, 1 experimental spectrum mass is near: \[162.9\]

**WHY**: The closer a theoretical spectrum is to an experimental spectrum, the more likely it is that the peptide sequence used to generate that theoretical spectrum is related to the peptide sequence that produced that experimental spectrum. However, before being able to build a theoretical spectrum, a list of potential amino acids need to be inferred from the experimental spectrum. In addition to the 20 proteinogenic amino acids, there are many other non-proteinogenic amino acids that may be part of the peptide.

This operation infers a list of potential amino acid masses, which can be mapped back to amino acids themselves.

**ALGORITHM**:

Consider an experimental spectrum with masses that don't contain any noise. That is, the experimental spectrum may have faulty masses and may be missing masses, but any correct masses it does have are exact / noise-free. To derive a list of potential amino acid masses for this experimental spectrum:

 1. Subtract experimental spectrum masses from each other (each mass gets subtracted from every mass).
 2. Filter differences to those between 57Da and 200Da (generally accepted range for the mass of an amino acid).
 3. Filter differences to that don't occur at least n times (n is user-defined).

The result is a list of potential amino acid masses for the peptide that produced that experimental spectrum. For example, consider the following experimental spectrum for the linear peptide NQY:

[0Da, 114Da, 136Da, 163Da, 242Da, 311Da, 346Da, 405Da]

The experimental spectrum masses...

 * [163Da, 291Da] are missing.
 * [136Da, 311Da, 346Da] are faulty.
 * [114Da, 163Da, 242Da, 405Da] are correct and free of noise.

Subtract the experimental spectrum masses:

|     | 0   | 114  | 136  | 163  | 242  | 311  | 346  | 405  |
|-----|-----|------|------|------|------|------|------|------|
| 0   | 0   | -114 | -136 | -163 | -242 | -311 | -346 | -405 |
| 114 | 114 | 0    | -22  | -49  | -128 | -197 | -231 | -291 |
| 136 | 136 | 22   | 0    | -27  | -106 | -175 | -210 | -269 |
| 163 | 163 | 49   | 27   | 0    | -79  | -148 | -183 | -242 |
| 242 | 242 | 128  | 106  | 79   | 0    | -69  | -104 | -163 |
| 311 | 311 | 197  | 175  | 148  | 69   | 0    | -35  | -94  |
| 346 | 346 | 232  | 210  | 183  | 104  | 35   | 0    | -59  |
| 405 | 405 | 291  | 269  | 242  | 163  | 94   | 59   | 0    |

Then, remove differences that aren't between 57Da and 200Da:

|     | 0   | 114  | 136  | 163  | 242  | 311  | 346  | 405  |
|-----|-----|------|------|------|------|------|------|------|
| 0   |     |      |      |      |      |      |      |      |
| 114 | 114 |      |      |      |      |      |      |      |
| 136 | 136 |      |      |      |      |      |      |      |
| 163 | 163 |      |      |      |      |      |      |      |
| 242 |     | 128  | 106  | 79   |      |      |      |      |
| 311 |     | 197  | 175  | 148  | 69   |      |      |      |
| 346 |     |      |      | 183  | 104  |      |      |      |
| 405 |     |      |      |      | 163  | 94   | 59   |      |

Then, filter out any differences occurring less than than n times. In this case, it makes sense to set n to 1 because almost all of the differences occur only once.

The final result is a list of potential amino acid masses for the peptide that produced the experimental spectrum:

[59Da, 69Da, 79Da, 94Da, 104Da, 106Da, 114Da, 128Da, 136Da, 148Da, 163Da, 175Da, 183Da, 197Da]

Note that the experimental spectrum is for the linear peptide NQY. The experimental spectrum contained the masses for N (114Da) and Y (163Da), but not Q (128Da). This operation was able to pull out the mass for Q: 128Da is in the final list of differences.

```{output}
ch4_code/src/SpectrumConvolution_NoNoise.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch4}
SpectrumConvolution_NoNoise
0 114 136 163 242 311 346 405
```

```{note}
The following section isn't from the Pevzner book or any online resources. I came up with it in an effort to solve the final assignment for Chapter 4 (the chapter on non-ribosomal peptide sequencing). As such, it might not be entirely correct / there may be better ways to do this.
```

The algorithm described above is for experimental spectrums that have exact masses (no noise). However, real experimental spectrums will have noisy masses. Since a real experimental spectrum has noisy masses, the amino acid masses derived from it will also be noisy. For example, consider an experimental spectrum that has ±1Da noise per mass. A real mass of...

 * 242Da will show up in the experimental spectrum anywhere between 241Da to 243Da.
 * 114Da will show up in the experimental spectrum anywhere between 113Da to 115Da.

Subtract the opposite extremes from these two ranges: 243Da - 113Da = 130Da. That's 2Da away from the real mass difference: 128Da. As such, the maximum noise per amino acid mass is 2 times the maximum noise for the experimental spectrum that it was derived from: ±2Da for this example.

```{output}
ch4_code/src/SpectrumConvolutionNoise.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch4}
SpectrumConvolutionNoise
1
```

Extending the algorithm to handle noisy experimental spectrum masses requires one extra step: group together differences that are within some tolerance of each other, where this tolerance is the maximum amino acid mass noise calculation described above. For example, consider the following experimental spectrum for linear peptide NQY that has up to ±1Da noise per mass:

[0.0Da, 113.9Da, 115.1Da, 136.2Da, 162.9Da, 242.0Da, 311.1Da, 346.0Da, 405.2Da]

Just as before, subtract the experimental spectrum masses and differences that aren't between 57Da and 200Da:

|       | 0.0    | 113.9  | 115.1  | 136.2  | 162.9  | 242.0  | 311.1  | 346.0  | 405.2  |
|-------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| 0.0   |        |        |        |        |        |        |        |        |        |
| 113.9 | 113.9  |        |        |        |        |        |        |        |        |
| 115.1 | 115.1  |        |        |        |        |        |        |        |        |
| 136.2 | 136.2  |        |        |        |        |        |        |        |        |
| 162.9 | 162.9  |        |        |        |        |        |        |        |        |
| 242.0 |        | 128.1  | 126.9  | 105.8  | 79.1   |        |        |        |        |
| 311.1 |        | 197.2  | 196.0  | 174.9  | 142.9  | 69.1   |        |        |        |
| 346.0 |        |        |        |        | 183.1  | 104.0  |        |        |        |
| 405.2 |        |        |        |        |        | 163.0  | 94.1   | 59.2   |        |

Then, group differences that are within ±2Da of each other (2 times the experimental spectrum's maximum mass noise):

* \[104.0, 105.8\]
* \[113.9, 115.1\]
* \[128.1, 126.9\]
* \[162.9, 163.0\]
* \[196.0, 197.2\]
* \[59.2\]
* \[69.1\]
* \[79.1\]
* \[94.1\]
* \[136.2\]
* \[142.9\]
* \[174.9\]

Then, filter out any groups that have less than n occurrences. In this case, filtering to n=2 occurrences reveals that all amino acid masses are captured for NQY:

 * \[104.0, 105.8\] (junk)
 * \[113.9, 115.1\] (mass of N is 114)
 * \[128.1, 126.9\] (mass of Q is 128)
 * \[162.9, 163.0\] (mass of Y is 163)
 * \[196.0, 197.2\] (junk)

Note that the experimental spectrum is for the linear peptide NQY. The experimental spectrum contained the masses near N (113.Da and 115.1Da) and Y (162.9Da), but not Q. This operation was able to pull out masses near Q: \[128.1, 126.9\] is in the final list of differences.

```{output}
ch4_code/src/SpectrumConvolution.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch4}
SpectrumConvolution
113.9 115.1 136.2 162.9 242.0 311.1 346.0 405.2
2
1
```

### Spectrum Score

`{bm} /(Algorithms\/Peptide Sequence\/Spectrum Score)_TOPIC/`

```{prereq}
Algorithms/Peptide Sequence/Experimental Spectrum_TOPIC
Algorithms/Peptide Sequence/Theoretical Spectrum_TOPIC
Algorithms/Peptide Sequence/Spectrum Convolution_TOPIC
```

**WHAT**: Given an experimental spectrum and a theoretical spectrum, score them against each other by counting how many masses match between them.

**WHY**: The more matching masses between a theoretical spectrum and an experimental spectrum, the more likely it is that the peptide sequence used to generate that theoretical spectrum is related to the peptide sequence that produced that experimental spectrum. This is the basis for how non-ribosomal peptides are sequenced: an experimental spectrum is produced by a mass spectrometer, then that experimental spectrum is compared against a set of theoretical spectrums.

**ALGORITHM**:

Consider an experimental spectrum with masses that don't contain any noise. That is, the experimental spectrum may have faulty masses and may be missing masses, but any correct masses it does have are exact / noise-free. Scoring this experimental spectrum against a theoretical spectrum is simple: count the number of matching masses.

```{output}
ch4_code/src/SpectrumScore_NoNoise.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch4}
SpectrumScore_NoNoise
0 57 71 128 199 256 
0 57 71 128 128 199 256
```

Note that a theoretical spectrum may have multiple masses with the same value but an experimental spectrum won't. For example, the theoretical spectrum for GAK is ...

|           |     |   G   |   A   |   K   |  GA   |  AK   |  GAK  |
|-----------|-----|-------|-------|-------|-------|-------|-------|
| Mass      | 0Da | 57D a | 71Da  | 128Da | 128Da | 199Da | 256Da |

K and GA both have a mass of 128Da. Since experimental spectrums don't distinguish between where masses come from, an experimental spectrum for this linear peptide will only have 1 entry for 128Da.

```{note}
The following section isn't from the Pevzner book or any online resources. I came up with it in an effort to solve the final assignment for Chapter 4 (the chapter on non-ribosomal peptide sequencing). As such, it might not be entirely correct / there may be better ways to do this.
```

The algorithm described above is for experimental spectrums that have exact masses (no noise). However, real experimental spectrums have noisy masses. That noise needs to be accounted for when identifying matches.

Recall that each amino acid mass captured by a spectrum convolution has up to some amount of noise. This is what defines the tolerance for a matching mass between the experimental spectrum and the theoretical spectrum. Specifically, the maximum amount of noise for a captured amino acid mass is multiplied by the amino acid count of the subpeptide to determine the tolerance.

For example, imagine a case where it's determined that the noise tolerance for each captured amino acid mass is ±2Da. Given the theoretical spectrum for linear peptide NQY, the tolerances would be as follows:

|           |     |   N   |   Q   |   Y   |  NQ   |  QY   |  NQY  |
|-----------|-----|-------|-------|-------|-------|-------|-------|
| Mass      | 0Da | 114Da | 128Da | 163Da | 242Da | 291Da | 405Da |
| Tolerance | 0Da | ±2Da  | ±2Da  | ±2Da  | ±4Da  | ±4Da  | ±6Da  |

```{output}
ch4_code/src/TheoreticalSpectrumTolerances.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch4}
TheoreticalSpectrumTolerances
NQY
linear
2
```

Given a theoretical spectrum with tolerances, each experimental spectrum mass is checked to see if it fits within a theoretical spectrum mass tolerance. If it fits, it's considered a match. The score includes both the number of matches and how closely each match was to the ideal theoretical spectrum mass.

```{output}
ch4_code/src/SpectrumScore.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch4}
SpectrumScore
0 56.1 71.9 126.8 200.6 250.9
GAK
linear
G: 57, A: 71, S: 87, P: 97, V: 99, T: 101, C: 103, I: 113, L: 113, N: 114, D: 115, K: 128, Q: 128, E: 129, M: 131, H: 137, F: 147, R: 156, Y: 163, W: 186
2
```

### Spectrum Sequence

`{bm} /(Algorithms\/Peptide Sequence\/Spectrum Sequence)_TOPIC/`

```{prereq}
Algorithms/Peptide Sequence/Experimental Spectrum_TOPIC
Algorithms/Peptide Sequence/Theoretical Spectrum_TOPIC
Algorithms/Peptide Sequence/Spectrum Convolution_TOPIC
Algorithms/Peptide Sequence/Spectrum Score_TOPIC
```

**WHAT**: Given an experimental spectrum and a set of amino acid masses, generate theoretical spectrums and score them against the experimental spectrum in an effort to infer the peptide sequence of the experimental spectrum.

**WHY**: The more matching masses between a theoretical spectrum and an experimental spectrum, the more likely it is that the peptide sequence used to generate that theoretical spectrum is related to the peptide sequence that produced that experimental spectrum.

#### Bruteforce Algorithm

`{bm} /(Algorithms\/Peptide Sequence\/Spectrum Sequence\/Bruteforce Algorithm)_TOPIC/`

**ALGORITHM**:

Imagine if experimental spectrums were perfect just like theoretical spectrums: no missing masses, no faulty masses, no noise, and preserved repeat masses. To bruteforce the peptide that produced such an experimental spectrum, generate candidate peptides by branching out amino acids at each position and compare each candidate peptide's theoretical spectrum to the experimental spectrum. If the theoretical spectrum matches the experimental spectrum, it's reasonable to assume that peptide is the same as the peptide that generated the experimental spectrum.

The algorithm stops branching out once the mass of the candidate peptide exceeds the final mass in the experimental spectrum. For a perfect experimental spectrum, the final mass is always the mass of the peptide that produced it. For example, for the linear peptide GAK ...

|           |     |   G  |   A   |   K   |  GA   |  AK   |  GAK  |
|-----------|-----|------|-------|-------|-------|-------|-------|
| Mass      | 0Da | 57Da | 71Da  | 128Da | 128Da | 199Da | 256Da |

```{output}
ch4_code/src/SequencePeptide_Naive_Bruteforce.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch4}
SequencePeptide_Naive_Bruteforce
0 57 71 128 128 199 256
linear
G: 57, A: 71, S: 87, P: 97, V: 99, T: 101, C: 103, I: 113, L: 113, N: 114, D: 115, K: 128, Q: 128, E: 129, M: 131, H: 137, F: 147, R: 156, Y: 163, W: 186
```

```{note}
The following section isn't from the Pevzner book or any online resources. I came up with it in an effort to solve the final assignment for Chapter 4 (the chapter on non-ribosomal peptide sequencing). As such, it might not be entirely correct / there may be better ways to do this.
```

Even though real experimental spectrums aren't perfect, the high-level algorithm remains the same: Create candidate peptides by branching out amino acids and capture the best scoring ones until the mass goes too high. However, various low-level aspects of the algorithm need to be modified to handle the problems with real experimental spectrums.

For starters, since there are no preset amino acids to build candidate peptides with, amino acid masses are captured using spectrum convolution and used directly. For example, instead of representing a peptide as GAK, it's represented as 57-71-128.

|   G  |   A   |   K   |
|------|-------|-------|
| 57Da | 71Da  | 128Da |

Next, the last mass in a real experimental spectrum isn't guaranteed to be the mass of the peptide that produced it. Since real experimental spectrums have faulty masses and may be missing masses, it's possible that either the peptide's mass wasn't captured at all or was captured but at an index that isn't the last element.

If the experimental spectrum's peptide mass was captured and found, it'll have noise. For example, imagine an experimental spectrum for the peptide 57-57 with ±1Da noise. The exact mass of the peptide 57-57 is 114Da, but if that mass gets placed into the experimental spectrum it will show up as anywhere between 113Da to 115Da.

Given that same experimental spectrum, running a spectrum convolution to derive the amino acid masses ends up giving back amino acid masses with ±2Da noise. For example, the mass 57Da may be derived as anywhere between 55Da to 59Da. Assuming that you're building the peptide 57-57 with the low end of that range (55Da), its mass will be 55Da + 55Da = 110Da. Compared against the high end of the experimental spectrum's peptide mass (115Da), it's 5Da away.


```{output}
ch4_code/src/ExperimentalSpectrumPeptideMassNoise.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch4}
ExperimentalSpectrumPeptideMassNoise
1
2
```

Finally, given that real experimental spectrums contain faulty masses and may be missing masses, more often than not the peptides that score the best aren't the best candidates. Theoretical spectrum masses that are ...

 * incorrect but match faulty experimental spectrum masses
 * correct but are missing in the experimental spectrum

... may push poor peptide candidates forward. As such, it makes sense to keep a backlog of the last m scoring peptides. Any of these backlog peptides may be the correct peptide for the experimental spectrum.

```{output}
ch4_code/src/SequenceTester.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{output}
ch4_code/src/SequencePeptide_Bruteforce.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{note}
The experimental spectrum in the example below is for the peptide 114-128-163, which has the theoretical spectrum [0, 114, 128, 163, 242, 291, 405].
```

```{ch4}
SequencePeptide_Bruteforce
0.0 112.5 127.1 242.9 290.0 404.0
1.0
1
1
10
linear
3
0
```

#### Branch-and-bound Algorithm

`{bm} /(Algorithms\/Peptide Sequence\/Spectrum Sequence\/Branch-and-bound Algorithm)_TOPIC/`

```{prereq}
Algorithms/Peptide Sequence/Spectrum Sequence/Bruteforce Algorithm_TOPIC
```

**ALGORITHM**:

This algorithm extends the bruteforce algorithm into a more efficient branch-and-bound algorithm by adding one extra step: After each branch, any candidate peptides deemed to be untenable are discarded. In this case, untenable means that there's no chance / little chance of the peptide branching out to a correct solution.

Imagine if experimental spectrums were perfect just like theoretical spectrums: no missing masses, no faulty masses, no noise, and preserved repeat masses. For such an experimental spectrum, an untenable candidate peptide has a theoretical spectrum with at least one mass that don't exist in the experimental spectrum. For example, the peptide 57-71-128 has the theoretical spectrum [0Da, 57Da, 71Da, 128Da, 128Da, 199Da, 256Da]. If 71Da were missing from the experimental spectrum, that peptide would be untenable (won't move forward).

When testing if a candidate peptide should move forward, the candidate peptide be treated as a linear peptide even if the experimental spectrum is for a cyclic peptide. For example, testing the experimental spectrum for cyclic peptide NQYQ against the theoretical spectrum for candidate cyclic peptide NQY...

| Peptide | 0 | 1   | 2   | 3   | 4   | 5   | 6   | 7   | 8   | 9   | 10  | 11  | 12  | 13  | 14  |
|---------|---|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| NQYQ    | 0 | 114 | 128 | 128 | 163 | 242 | 242 |     | 291 | 291 | 370 | 405 | 405 | 419 | 533 |
| NQY     | 0 | 114 | 128 |     | 163 | 242 |     | 277 | 291 |     |     | 405 |     |     |     |

The theoretical spectrum contains 277, but the experimental spectrum doesn't. That means NQY won't branch out any further even though it should. As such, even if the experimental spectrum is for a cyclic peptide, treat candidate peptides as if they're linear segments of a cyclic peptide (essentially the same as linear peptides). If the theoretical spectrum for candidate linear peptide NQY were used...

| Peptide | 0 | 1   | 2   | 3   | 4   | 5   | 6   | 7   | 8   | 9   | 10  | 11  | 12  | 13  |
|---------|---|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| NQYQ    | 0 | 114 | 128 | 128 | 163 | 242 | 242 | 291 | 291 | 370 | 405 | 405 | 419 | 533 |
| NQY     | 0 | 114 | 128 |     | 163 | 242 |     | 291 |     |     | 405 |     |     |     |

All theoretical spectrum masses are in the experimental spectrum. As such, the candidate NQY would move forward.

```{output}
ch4_code/src/SequencePeptide_Naive_BranchAndBound.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch4}
SequencePeptide_Naive_BranchAndBound
0 114 128 128 163 242 242 291 291 370 405 405 419 533
cyclic
G: 57, A: 71, S: 87, P: 97, V: 99, T: 101, C: 103, I: 113, L: 113, N: 114, D: 115, K: 128, Q: 128, E: 129, M: 131, H: 137, F: 147, R: 156, Y: 163, W: 186
```

```{note}
The following section isn't from the Pevzner book or any online resources. I came up with it in an effort to solve the final assignment for Chapter 4 (the chapter on non-ribosomal peptide sequencing). As such, it might not be entirely correct / there may be better ways to do this.
```

The bounding step described above won't work for real experimental spectrums. For example, a real experimental spectrum may ...

 * have a faulty mass that allows candidate peptides that should be untenable.
 * be missing a mass that drops candidate peptides that should be good.
 * have noise that causes good candidate peptide to be dropped / untenable candidate peptide through.

A possible bounding step for real experimental spectrums is to mark a candidate peptide as untenable if it has a certain number or percentage of mismatches. This is a heuristic, meaning that it won't always lead to the correct peptide. In contrast, the algorithm described above for perfect experimental spectrums always leads to the correct peptide.

```{output}
ch4_code/src/SequencePeptide_BranchAndBound.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{note}
The experimental spectrum in the example below is for the peptide 114-128-163, which has the theoretical spectrum [0, 114, 128, 163, 242, 291, 405].
```

```{ch4}
SequencePeptide_BranchAndBound
0.0 112.5 127.1 242.9 290.0 404.0
1.0
1
1
10
linear
3
0
0.75
```

#### Leaderboard Algorithm

**ALGORITHM**:

`{bm} /(Algorithms\/Peptide Sequence\/Spectrum Sequence\/Leaderboard Algorithm)_TOPIC/`

```{prereq}
Algorithms/Peptide Sequence/Spectrum Sequence/Bruteforce Algorithm_TOPIC
Algorithms/Peptide Sequence/Spectrum Sequence/Branch-and-bound Algorithm_TOPIC
```

This algorithm is similar to the branch-and-bound algorithm, but the bounding step is slightly different: At each branch, rather than removing untenable candidate peptides, it only moves forward the best n scoring candidate peptides. These best scoring peptides are referred to as the leaderboard.

For a perfect experimental spectrum (no missing masses, no faulty masses, no noise, and preserved repeat masses), this algorithm isn't much different than the branch-and-bound algorithm. However, imagine if the perfect experimental spectrum wasn't exactly perfect in that it could have faulty masses and could be missing masses. In such a case, the branch-and-bound algorithm would always fail while this algorithm could still converge to the correct peptide -- it's a heuristic, meaning that it isn't guaranteed to lead to the correct peptide.

```{output}
ch4_code/src/SequencePeptide_Naive_Leaderboard.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{note}
The experimental spectrum in the example below is for the peptide NQYQ, which has the theoretical spectrum [0, 114, 128, 128, 163, 242, 242, 291, 291, 370, 405, 405, 419, 533].
```

```{ch4}
SequencePeptide_Naive_Leaderboard
0 114 163 242 291 370 405 419 480 533
cyclic
533
10
G: 57, A: 71, S: 87, P: 97, V: 99, T: 101, C: 103, I: 113, L: 113, N: 114, D: 115, K: 128, Q: 128, E: 129, M: 131, H: 137, F: 147, R: 156, Y: 163, W: 186
```

```{note}
The following section isn't from the Pevzner book or any online resources. I came up with it in an effort to solve the final assignment for Chapter 4 (the chapter on non-ribosomal peptide sequencing). As such, it might not be entirely correct / there may be better ways to do this.
```

For real experimental spectrums, the algorithm is very similar to the real experimental spectrum version of the branch-and-bound algorithm. The only difference is the bounding heuristic: At each branch, rather than moving forward candidate peptides that meet a certain score threshold, move forward the best n scoring candidate peptides. These best scoring peptides are referred to as the leaderboard.

```{output}
ch4_code/src/SequencePeptide_Leaderboard.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{note}
The experimental spectrum in the example below is for the peptide 114-128-163, which has the theoretical spectrum [0, 114, 128, 163, 242, 291, 405].
```

```{ch4}
SequencePeptide_Leaderboard
0.0 112.5 127.1 242.9 290.0 404.0
1.0
1
1
10
linear
3
0
100
```

```{note}
This was the version of the algorithm used to solve chapter 4's final assignment (sequence a real experimental spectrum for some unknown variant of Tyrocidine). Note how the parameters into sequence_peptide take an initial leaderboard. This initial leaderboard was primed with subpeptide sequences from other Tyrocidine variants discusses in chapter 4. The problem wasn't solvable without these subpeptide sequences. More information on this can be found in the Python file for the final assignment.

Before coming up with the above solution, I came up with another heuristic that I tried: Use basic genetic algorithms / evolutionary algorithms as the heuristic to move forward peptides. This performed even worse than leaderboard: If the mutation rate is too low, the candidates converge to a local optima and can't break out. If the mutation rate is too high, the candidates never converge to a solution. As such, it was removed from the code.
```

## Sequence Alignment

`{bm} /(Algorithms\/Sequence Alignment)_TOPIC/`

Many core biology constructs are represented as sequences. For example, ...

 * DNA strands are represented as a sequence (chained nucleotides),
 * proteins are represented as a sequence (chained amino acids),
 * etc..
 
Performing a sequence alignment on a set of sequences means to match up the elements of those sequences against each other using a set of basic operations:
 
 * insert/delete (also referred to as indel).
 * replace (also referred to as mismatch).
 * keep matching (also referred to as match).
 
There are many ways that a set of sequences can be aligned. For example, the sequences MAPLE and TABLE may be aligned by performing...

| String 1 | String 2 | Operation     |
|----------|----------|---------------|
|    M     |          | Insert/delete |
|          |     T    | Insert/delete |
|    A     |     A    | Keep matching |
|    P     |     B    | Replace       |
|    L     |     L    | Keep matching |
|    E     |     E    | Keep matching |

Or, MAPLE and TABLE may be aligned by performing...

| String 1 | String 2 | Operation     |
|----------|----------|---------------|
|    M     |     T    | Replace       |
|    A     |     A    | Keep matching |
|    P     |     B    | Replace       |
|    L     |     L    | Keep matching |
|    E     |     E    | Keep matching |

Typically the highest scoring sequence alignment is the one that's chosen, where the score is some custom function that best represents the type of sequence being worked with (e.g. proteins are scored differently than DNA). In the example above, if replacements are scored better than indels, the latter alignment would be the highest scoring. Sequences that strongly align are thought of as being related / similar (e.g. proteins that came from the same parent but diverged to 2 separate evolutionary paths).

The names of these operations make more sense if you were to think of alignment instead as __transformation__. The example above's first alignment in the context of __transforming__ MAPLE to TABLE may be thought of as:

| From | To | Operation       | Result |
|------|----|-----------------|--------|
|   M  |    | Delete M        |        |
|      | T  | Insert T        | T      |
|   A  | A  | Keep matching A | TA     |
|   P  | B  | Replace P to B  | TAB    |
|   L  | L  | Keep matching L | TABL   |
|   E  | E  | Keep matching E | TABLE  |

The shorthand form of representing sequence alignments is to stack each sequence. The example above may be written as...

|          | 0 | 1 | 2 | 3 | 4 | 5 |
|----------|---|---|---|---|---|---|
| String 1 | M |   | A | P | L | E |
| String 2 |   | T | A | B | L | E |

Typically, all possible sequence alignments are represented using an alignment graph: a graph that represents all possible alignments for a set of sequences. A path through an alignment graph from source node to sink node is called an alignment path: a path that represents one specific way the set of sequences may be aligned. For example, the alignment graph and alignment paths for the alignments above (MAPLE vs TABLE) ...

```{svgbob}
"* Each diagonal edge is a replacement / keep matching"
"* Each horizontal edge is an indel where the top is kept"
"* Each vertical edge is an indel where the left is kept"

    Complete graph                     Example alignment 1                Example alignment 2
                                             M-APLE                             MAPLE
                                             -TABLE                             TABLE

   T    A    B    L    E              T    A    B    L    E              T    A    B    L    E   
 o---▶o---▶o---▶o---▶o---▶o         o    o    o    o    o    o         o    o    o    o    o    o
 |\   |\   |\   |\   |\   |         |                                   \                        
M| \  | \  | \  | \  | \  |        M|                                 M  \                       
 |  \ |  \ |  \ |  \ |  \ |         |                                     \                      
 ▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼         ▼                                      ▼                     
 o---▶o---▶o---▶o---▶o---▶o         o---▶o    o    o    o    o         o    o    o    o    o    o
 |\   |\   |\   |\   |\   |               \                                  \                   
A| \  | \  | \  | \  | \  |        A       \                          A       \                  
 |  \ |  \ |  \ |  \ |  \ |                 \                                  \                 
 ▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼                  ▼                                  ▼                
 o---▶o---▶o---▶o---▶o---▶o         o    o    o    o    o    o         o    o    o    o    o    o
 |\   |\   |\   |\   |\   |                    \                                  \              
P| \  | \  | \  | \  | \  |        P            \                     P            \             
 |  \ |  \ |  \ |  \ |  \ |                      \                                  \            
 ▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼                       ▼                                  ▼           
 o---▶o---▶o---▶o---▶o---▶o         o    o    o    o    o    o         o    o    o    o    o    o
 |\   |\   |\   |\   |\   |                         \                                  \         
L| \  | \  | \  | \  | \  |        L                 \                L                 \        
 |  \ |  \ |  \ |  \ |  \ |                           \                                  \       
 ▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼                            ▼                                  ▼      
 o---▶o---▶o---▶o---▶o---▶o         o    o    o    o    o    o         o    o    o    o    o    o
 |\   |\   |\   |\   |\   |                              \                                  \    
E| \  | \  | \  | \  | \  |        E                      \           E                      \   
 |  \ |  \ |  \ |  \ |  \ |                                \                                  \  
 ▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼                                 ▼                                  ▼ 
 o---▶o---▶o---▶o---▶o---▶o         o    o    o    o    o    o         o    o    o    o    o    o
```

The example above is just one of many sequence alignment types. There are different types of alignment graphs, applications of alignment graphs, and different scoring models used in bioinformatics.

```{note}
The Pevzner book mentions a non-biology related problem to help illustrate alignment graphs: the Manhattan Tourist problem. Look it up if you're confused.
```

```{note}
The Pevzner book, in a later chapter (ch7 -- phylogeny), spends an entire section talking about character tables and how they can be thought of as sequences (character vectors). There's no good place to put this information. It seems non-critical so the only place it exists is in the terminology section.
```

### Find Maximum Path

`{bm} /(Algorithms\/Sequence Alignment\/Find Maximum Path)_TOPIC/`

**WHAT**: Given an arbitrary directed acyclic graph where each edge has a weight, find the path with the maximum weight between two nodes.

**WHY**: Finding a maximum path between nodes is fundamental to sequence alignments. That is, regardless of what type of sequence alignment is being performed, at its core it boils down to finding the maximum weight between two nodes in an alignment graph.

#### Bruteforce Algorithm

`{bm} /(Algorithms\/Sequence Alignment\/Find Maximum Path\/Bruteforce Algorithm)_TOPIC/`

**ALGORITHM**:

This algorithm finds a maximum path using recursion. To calculate the maximum path between two nodes, iterate over each of the source node's children and calculate `edge_weight + max_path(child, destination).weight`. The iteration with the highest value is the one with the maximum path to the destination node.

This is too slow to be used on anything but small DAGs.

```{output}
ch5_code/src/find_max_path/FindMaxPath_Bruteforce.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch5}
find_max_path.FindMaxPath_Bruteforce
A B 1, A C 1, B C 1, C D 1, C E 1
A
E
```

#### Cache Algorithm

`{bm} /(Algorithms\/Sequence Alignment\/Find Maximum Path\/Cache Algorithm)_TOPIC/`

```{prereq}
Algorithms/Sequence Alignment/Find Maximum Path/Bruteforce Algorithm_TOPIC
```

**ALGORITHM**:

This algorithm extends the bruteforce algorithm using dynamic programming: A technique that breaks down a problem into recursive sub-problems, where the result of each sub-problem is stored in some lookup table (cache) such that it can be re-used if that sub-problem were ever encountered again. The bruteforce algorithm already breaks down into recursive sub-problems. As such, the only change here is that the result of each sub-problem computation is cached such that it can be re-used if it were ever encountered again.

```{output}
ch5_code/src/find_max_path/FindMaxPath_DPCache.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch5}
find_max_path.FindMaxPath_DPCache
A B 1, A C 1, B C 1, C D 1, C E 1
A
E
```

#### Backtrack Algorithm

`{bm} /(Algorithms\/Sequence Alignment\/Find Maximum Path\/Backtrack Algorithm)_TOPIC/`

```{prereq}
Algorithms/Sequence Alignment/Find Maximum Path/Cache Algorithm_TOPIC
```

**ALGORITHM**:

This algorithm is a better but less obvious dynamic programming approach. The previous dynamic programming algorithm builds a cache containing the maximum path from each node encountered to the destination node. This dynamic programming algorithm instead builds out a smaller cache from the source node fanning out one step at a time.

In this less obvious algorithm, there are edge weights just as before but each node also has a weight and a selected incoming edge. The DAG starts off with all node weights and incoming edge selections being unset. The source node has its weight set to 0. Then, for any node where all of its parents have a weight set, select the incoming edge where `parent_weight + edge_weight` is the highest. That highest `parent_weight + edge_weight` becomes the weight of that node and the edge responsible for it becomes the selected incoming edge (backtracking edge).

Repeat until all nodes have a weight and backtracking edge set.

For example, imagine the following DAG...

```{svgbob}
  1       1
.----> B ----.
|            v   2
A ---------> C ----> D
      3      |
             `-----> E 
                 1
```

Set source nodes to have a weight of 0...

```{svgbob}
"* Node weight denoted in brackets next to node name"

  1       1
.----> B ----.
|            v   2
A(0) ------> C ----> D
      3      |
             `-----> E 
                 1
```

Then, iteratively set the weights and backtracking edges...

```{svgbob}
"* Node weight denoted in brackets next to node name"
"* Backtracking edge chosen for a node is denoted by double lines"

   "Iteration 1"                       "Iteration 2"                       "Iteration 3"
  1       1                          1       1                          1       1           
.==> B(1) ---.                     .==> B(1) ---.                     .==> B(1) ---.        
|            v   2                 |            v   2                 |            v   2    
A(0) ------> C ----> D             A(0) =====> C(3) --> D             A(0) =====> C(3) ==> D(5)
      3      |                           3      |                           3      |        
             `-----> E                          `-----> E                          `=====> E(4)
                 1                                  1                                  1    
```

```{note}
This process is walking the DAG in topological order.
```

To find the path with the maximum weight, simply walk backward using the backtracking edges from the destination node to the source node. For example, in the DAG above the maximum path that ends at E can be determined by following the backtracking edges from E until A is reached...

 * E came from C
 * C came from A

The maximum path from A to E is A -> C -> E and the weight of that path is 4 (the weight of E).

This variant of the dynamic programming algorithm uses less memory than the first. For each node encountered, ...

 * the first variant caches a path to the destination.
 * this variant only caches a weight and backtracking edge.

```{output}
ch5_code/src/find_max_path/FindMaxPath_DPBacktrack.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch5}
find_max_path.FindMaxPath_DPBacktrack
A B 1, A C 3, B C 1, C D 2, C E 1
A
E
```

```{note}
Note how ...

 * the first variant's cache is built out such that it's possible to find the maximum path between any walked node and the destination node.
 * this variant's cache is built out such that it's possible to find the maximum path between the source node and any walked node.

It's easy to flip this around by reversing the direction the algorithm walks.
```

### Global Alignment

`{bm} /(Algorithms\/Sequence Alignment\/Global Alignment)_TOPIC/`

```{prereq}
Algorithms/Sequence Alignment/Find Maximum Path_TOPIC
```

**WHAT**: Given two sequences, perform sequence alignment and pull out the highest scoring alignment.

**WHY**: A strong global alignment indicates that the sequences are likely homologous / related.

#### Graph Algorithm

`{bm} /(Algorithms\/Sequence Alignment\/Global Alignment\/Graph Algorithm)_TOPIC/`

**ALGORITHM**:

Determining the best scoring pairwise alignment can be done by generating a DAG of all possible operations at all possible positions in each sequence. Specifically, each operation (indel, match, mismatch) is represented as an edge in the graph, where that edge has a weight. Operations with higher weights are more desirable operations compared to operations with lower weights (e.g. a match is typically more favourable than an indel).

For example, consider a DAG that pits FOUR against CHOIR...

```{svgbob}
   C    H    O    I    R  
 o--->o--->o--->o--->o--->o
 |\   |\   |\   |\   |\   |
F| \  | \  | \  | \  | \  |
 |  \ |  \ |  \ |  \ |  \ |
 ▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼
 o--->o--->o--->o--->o--->o
 |\   |\   |\   |\   |\   |
O| \  | \  | \  | \  | \  |
 |  \ |  \ |  \ |  \ |  \ |
 ▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼
 o--->o--->o--->o--->o--->o
 |\   |\   |\   |\   |\   |
U| \  | \  | \  | \  | \  |
 |  \ |  \ |  \ |  \ |  \ |
 ▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼
 o--->o--->o--->o--->o--->o
 |\   |\   |\   |\   |\   |
R| \  | \  | \  | \  | \  |
 |  \ |  \ |  \ |  \ |  \ |
 ▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼
 o---▶o---▶o---▶o---▶o---▶o
```


Given this graph, each ...

 * diagonal edge is a replacement / keep matching.
 * horizontal edge is an indel where the top is kept.
 * vertical edge is an indel where the left is kept.

```{ch5}
global_alignment.GlobalAlignment_Graph_Visualize
CHOIR
FOUR

embedded_score_matrix
-1
   A  B  C  D  E  F  G  H  I  J  K  L  M  N  O  P  Q  R  S  T  U  V  W  X  Y  Z
A  1  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0
B  0  1  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0
C  0  0  1  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0
D  0  0  0  1  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0
E  0  0  0  0  1  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0
F  0  0  0  0  0  1  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0
G  0  0  0  0  0  0  1  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0
H  0  0  0  0  0  0  0  1  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0
I  0  0  0  0  0  0  0  0  1  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0
J  0  0  0  0  0  0  0  0  0  1  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0
K  0  0  0  0  0  0  0  0  0  0  1  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0
L  0  0  0  0  0  0  0  0  0  0  0  1  0  0  0  0  0  0  0  0  0  0  0  0  0  0
M  0  0  0  0  0  0  0  0  0  0  0  0  1  0  0  0  0  0  0  0  0  0  0  0  0  0
N  0  0  0  0  0  0  0  0  0  0  0  0  0  1  0  0  0  0  0  0  0  0  0  0  0  0
O  0  0  0  0  0  0  0  0  0  0  0  0  0  0  1  0  0  0  0  0  0  0  0  0  0  0
P  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  1  0  0  0  0  0  0  0  0  0  0
Q  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  1  0  0  0  0  0  0  0  0  0
R  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  1  0  0  0  0  0  0  0  0
S  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  1  0  0  0  0  0  0  0
T  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  1  0  0  0  0  0  0
U  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  1  0  0  0  0  0
V  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  1  0  0  0  0
W  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  1  0  0  0
X  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  1  0  0
Y  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  1  0
Z  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  1
```

This graph is called an alignment graph. A path through the alignment graph from source (top-left) to sink (bottom-right) represents a single alignment, referred to as an alignment path. For example the alignment path representing...

```
CH-OIR
--FOUR
```

... is as follows...

```{ch5}
global_alignment.GlobalAlignment_Graph_Visualize
CHOIR
FOUR
0,0->0,1|0,1->0,2|0,2->1,2|1,2->2,3|2,3->3,4|3,4->4,5
embedded_score_matrix
-1
   A  B  C  D  E  F  G  H  I  J  K  L  M  N  O  P  Q  R  S  T  U  V  W  X  Y  Z
A  1  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0
B  0  1  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0
C  0  0  1  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0
D  0  0  0  1  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0
E  0  0  0  0  1  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0
F  0  0  0  0  0  1  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0
G  0  0  0  0  0  0  1  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0
H  0  0  0  0  0  0  0  1  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0
I  0  0  0  0  0  0  0  0  1  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0
J  0  0  0  0  0  0  0  0  0  1  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0
K  0  0  0  0  0  0  0  0  0  0  1  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0
L  0  0  0  0  0  0  0  0  0  0  0  1  0  0  0  0  0  0  0  0  0  0  0  0  0  0
M  0  0  0  0  0  0  0  0  0  0  0  0  1  0  0  0  0  0  0  0  0  0  0  0  0  0
N  0  0  0  0  0  0  0  0  0  0  0  0  0  1  0  0  0  0  0  0  0  0  0  0  0  0
O  0  0  0  0  0  0  0  0  0  0  0  0  0  0  1  0  0  0  0  0  0  0  0  0  0  0
P  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  1  0  0  0  0  0  0  0  0  0  0
Q  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  1  0  0  0  0  0  0  0  0  0
R  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  1  0  0  0  0  0  0  0  0
S  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  1  0  0  0  0  0  0  0
T  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  1  0  0  0  0  0  0
U  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  1  0  0  0  0  0
V  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  1  0  0  0  0
W  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  1  0  0  0
X  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  1  0  0
Y  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  1  0
Z  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  1
```

The weight of an alignment path is the sum of its operation weights. Since operations with higher weights are more desirable than those with lower weights, alignment paths with higher weights are more desirable than those with lower weights. As such, out of all the alignment paths possible, the one with the highest weight is the one with the most desirable set of operations.

The highlighted path in the example path above has a weight of -1: -1 + -1 + -1 + 1 + 0 + 1.

```{output}
ch5_code/src/global_alignment/GlobalAlignment_Graph.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch5}
global_alignment.GlobalAlignment_Graph
TAAT
GAT
embedded_score_matrix
-1
   A  C  T  G
A  1  0  0  0
C  0  1  0  0
T  0  0  1  0
G  0  0  0  1
```

#### Matrix Algorithm

`{bm} /(Algorithms\/Sequence Alignment\/Global Alignment\/Matrix Algorithm)_TOPIC/`

```{prereq}
Algorithms/Sequence Alignment/Global Alignment/Graph Algorithm_TOPIC
Algorithms/Sequence Alignment/Find Maximum Path/Backtrack Algorithm_TOPIC
```

**ALGORITHM**:

The following algorithm is essentially the same as the graph algorithm, except that the implementation is much more sympathetic to modern hardware. The alignment graph is represented as a 2D matrix where each element in the matrix represents a node in the alignment graph. The elements are then populated in a predefined topological order, where each element gets populated with the node weight, the chosen backtracking edge, and the elements from that backtracking edge.

Since the alignment graph is a grid, the node weights may be populated either...

 * row-by-row, starting from the left column and walking to the right column.
 * column-by-column, starting from the top row and walking to the bottom row.

In either case, the nodes being walked are guaranteed to have their parent node weights already set.

```{svgbob}
       "Create graph"                   "Calc row 1"                      "Calc row 2"                    "Calc row 3"       
*---▶*---▶*---▶*---▶*---▶*       o---▶o---▶o---▶o---▶o---▶o       o---▶o---▶o---▶o---▶o---▶o       o---▶o---▶o---▶o---▶o---▶o
|\   |\   |\   |\   |\   |       |\   |\   |\   |\   |\   |       |\   |\   |\   |\   |\   |       |\   |\   |\   |\   |\   |
| \  | \  | \  | \  | \  |       | \  | \  | \  | \  | \  |       | \  | \  | \  | \  | \  |       | \  | \  | \  | \  | \  |
|  \ |  \ |  \ |  \ |  \ |       |  \ |  \ |  \ |  \ |  \ |       |  \ |  \ |  \ |  \ |  \ |       |  \ |  \ |  \ |  \ |  \ |
▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼       ▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼       ▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼       ▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼
*---▶*---▶*---▶*---▶*---▶*       *---▶*---▶*---▶*---▶*---▶*       o---▶o---▶o---▶o---▶o---▶o       o---▶o---▶o---▶o---▶o---▶o
|\   |\   |\   |\   |\   |       |\   |\   |\   |\   |\   |       |\   |\   |\   |\   |\   |       |\   |\   |\   |\   |\   |
| \  | \  | \  | \  | \  |       | \  | \  | \  | \  | \  |       | \  | \  | \  | \  | \  |       | \  | \  | \  | \  | \  |
|  \ |  \ |  \ |  \ |  \ |       |  \ |  \ |  \ |  \ |  \ |       |  \ |  \ |  \ |  \ |  \ |       |  \ |  \ |  \ |  \ |  \ |      "do the rest..."
▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼       ▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼       ▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼       ▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼
*---▶*---▶*---▶*---▶*---▶*       *---▶*---▶*---▶*---▶*---▶*       *---▶*---▶*---▶*---▶*---▶*       o---▶o---▶o---▶o---▶o---▶o
|\   |\   |\   |\   |\   |       |\   |\   |\   |\   |\   |       |\   |\   |\   |\   |\   |       |\   |\   |\   |\   |\   |
| \  | \  | \  | \  | \  |       | \  | \  | \  | \  | \  |       | \  | \  | \  | \  | \  |       | \  | \  | \  | \  | \  |
|  \ |  \ |  \ |  \ |  \ |       |  \ |  \ |  \ |  \ |  \ |       |  \ |  \ |  \ |  \ |  \ |       |  \ |  \ |  \ |  \ |  \ |
▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼       ▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼       ▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼       ▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼
*---▶*---▶*---▶*---▶*---▶*       *---▶*---▶*---▶*---▶*---▶*       *---▶*---▶*---▶*---▶*---▶*       *---▶*---▶*---▶*---▶*---▶*
|\   |\   |\   |\   |\   |       |\   |\   |\   |\   |\   |       |\   |\   |\   |\   |\   |       |\   |\   |\   |\   |\   |
| \  | \  | \  | \  | \  |       | \  | \  | \  | \  | \  |       | \  | \  | \  | \  | \  |       | \  | \  | \  | \  | \  |
|  \ |  \ |  \ |  \ |  \ |       |  \ |  \ |  \ |  \ |  \ |       |  \ |  \ |  \ |  \ |  \ |       |  \ |  \ |  \ |  \ |  \ |
▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼       ▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼       ▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼       ▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼
*---▶*---▶*---▶*---▶*---▶*       *---▶*---▶*---▶*---▶*---▶*       *---▶*---▶*---▶*---▶*---▶*       *---▶*---▶*---▶*---▶*---▶*
```

```{output}
ch5_code/src/global_alignment/GlobalAlignment_Matrix.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch5}
global_alignment.GlobalAlignment_Matrix
TATTATTAT
AAA
embedded_score_matrix
-1
   A  C  T  G
A  1  0  0  0
C  0  1  0  0
T  0  0  1  0
G  0  0  0  1
```

```{note}
The standard Levenshtein distance algorithm using a 2D array you remember from over a decade ago is this algorithm: Matrix-based global alignment where matches score 0 but mismatches and indels score -1. The final weight of the alignment is the minimum number of operations required to convert one sequence to another (e.g. swap, insert, delete) -- it'll be negative, ignore the sign.
```

#### Divide-and-Conquer Algorithm

`{bm} /(Algorithms\/Sequence Alignment\/Global Alignment\/Divide-and-Conquer Algorithm)_TOPIC/`

```{prereq}
Algorithms/Sequence Alignment/Global Alignment/Matrix Algorithm_TOPIC
Algorithms/Sequence Alignment/Find Maximum Path/Backtrack Algorithm_TOPIC
```

**ALGORITHM**:

The following algorithm extends the matrix algorithm such that it can process much larger graphs at the expense of duplicating some computation work (trading time for space). It relies on two ideas.

Recall that in the matrix implementation of global alignment, node weights are populated in a pre-defined topological order (either row-by-row or column-by-column). Imagine that you've chosen to populate the matrix column-by-column.

The first idea is that, if all you care about is the final weight of the sink node, the matrix implementation technically only needs to keep 2 columns in memory: the column having its node weights populated as well as the previous column.

In other words, the only data needed to calculate the weights of the next column is the weights in the previous column.

```{svgbob}
       "Calc col 1"                     "Calc col 2"                     "Calc col 3"                     "Calc col 4"       
o---▶*---▶*---▶*---▶*---▶*       o---▶o---▶*---▶*---▶*---▶*       *---▶o---▶o---▶*---▶*---▶*       *---▶*---▶o---▶o---▶*---▶*
|\   |\   |\   |\   |\   |       |\   |\   |\   |\   |\   |       |\   |\   |\   |\   |\   |       |\   |\   |\   |\   |\   |
| \  | \  | \  | \  | \  |       | \  | \  | \  | \  | \  |       | \  | \  | \  | \  | \  |       | \  | \  | \  | \  | \  |
|  \ |  \ |  \ |  \ |  \ |       |  \ |  \ |  \ |  \ |  \ |       |  \ |  \ |  \ |  \ |  \ |       |  \ |  \ |  \ |  \ |  \ |
▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼       ▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼       ▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼       ▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼
o---▶*---▶*---▶*---▶*---▶*       o---▶o---▶*---▶*---▶*---▶*       *---▶o---▶o---▶*---▶*---▶*       *---▶*---▶o---▶o---▶*---▶*
|\   |\   |\   |\   |\   |       |\   |\   |\   |\   |\   |       |\   |\   |\   |\   |\   |       |\   |\   |\   |\   |\   |
| \  | \  | \  | \  | \  |       | \  | \  | \  | \  | \  |       | \  | \  | \  | \  | \  |       | \  | \  | \  | \  | \  |
|  \ |  \ |  \ |  \ |  \ |       |  \ |  \ |  \ |  \ |  \ |       |  \ |  \ |  \ |  \ |  \ |       |  \ |  \ |  \ |  \ |  \ |      "do the rest..."
▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼       ▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼       ▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼       ▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼
o---▶*---▶*---▶*---▶*---▶*       o---▶o---▶*---▶*---▶*---▶*       *---▶o---▶o---▶*---▶*---▶*       *---▶*---▶o---▶o---▶*---▶*
|\   |\   |\   |\   |\   |       |\   |\   |\   |\   |\   |       |\   |\   |\   |\   |\   |       |\   |\   |\   |\   |\   |
| \  | \  | \  | \  | \  |       | \  | \  | \  | \  | \  |       | \  | \  | \  | \  | \  |       | \  | \  | \  | \  | \  |
|  \ |  \ |  \ |  \ |  \ |       |  \ |  \ |  \ |  \ |  \ |       |  \ |  \ |  \ |  \ |  \ |       |  \ |  \ |  \ |  \ |  \ |
▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼       ▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼       ▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼       ▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼
o---▶*---▶*---▶*---▶*---▶*       o---▶o---▶*---▶*---▶*---▶*       *---▶o---▶o---▶*---▶*---▶*       *---▶*---▶o---▶o---▶*---▶*
|\   |\   |\   |\   |\   |       |\   |\   |\   |\   |\   |       |\   |\   |\   |\   |\   |       |\   |\   |\   |\   |\   |
| \  | \  | \  | \  | \  |       | \  | \  | \  | \  | \  |       | \  | \  | \  | \  | \  |       | \  | \  | \  | \  | \  |
|  \ |  \ |  \ |  \ |  \ |       |  \ |  \ |  \ |  \ |  \ |       |  \ |  \ |  \ |  \ |  \ |       |  \ |  \ |  \ |  \ |  \ |
▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼       ▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼       ▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼       ▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼
o---▶*---▶*---▶*---▶*---▶*       o---▶o---▶*---▶*---▶*---▶*       *---▶o---▶o---▶*---▶*---▶*       *---▶*---▶o---▶o---▶*---▶*
                                                                                            
✔    ✗    ✗    ✗    ✗    ✗       ✔    ✔    ✗    ✗    ✗    ✗       ✗    ✔    ✔    ✗    ✗    ✗       ✗    ✗    ✔    ✔    ✗    ✗

"* ✗ = column not in memory"
"* ✔ = column in memory"
```

```{output}
ch5_code/src/global_alignment/Global_ForwardSweeper.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch5}
global_alignment.Global_ForwardSweeper
TACT
GACGT
embedded_score_matrix
-1
   A  C  T  G
A  1  0  0  0
C  0  1  0  0
T  0  0  1  0
G  0  0  0  1
```

The second idea is that, for a column, it's possible to find out which node in that column a maximum alignment path travels through without knowing that path beforehand.

```{svgbob}
  0    1    2    3    4    5
0 o---▶o---▶o---▶o---▶o---▶o
  |\   |\   |\   |\   |\   |
  | \  | \  | \  | \  | \  |
  |  \ |  \ |  \ |  \ |  \ |
  ▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼
1 o---▶o---▶o---▶o---▶o---▶o
  |\   |\   |\   |\   |\   |
  | \  | \  | \  | \  | \  |
  |  \ |  \ |  \ |  \ |  \ |
  ▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼
2 o---▶o---▶O---▶o---▶o---▶o
  |\   |\   |\   |\   |\   |
  | \  | \  | \  | \  | \  |
  |  \ |  \ |  \ |  \ |  \ |
  ▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼
3 o---▶o---▶o---▶o---▶o---▶o
  |\   |\   |\   |\   |\   |
  | \  | \  | \  | \  | \  |
  |  \ |  \ |  \ |  \ |  \ |
  ▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼
4 o---▶o---▶o---▶o---▶o---▶o

* "I don't know what the maximum alignment path is, but"
  "I know it travels through the node at (2, 2) (denoted by"
  "a larger circle)."
```

Knowing this, a divide-and-conquer algorithm may be used to find that maximum alignment path. Any alignment path must travel from the source node (top-left) to the sink node (bottom-right). If you're able to find a node between the source node and sink node that a maximum alignment path travels through, you can sub-divide the alignment graph into 2.

That is, if you know that a maximum alignment path travels through some node, it's guaranteed that...

 * prior parts of the path travel through the region that's to the top-left of that node.
 * subsequent parts of that path travel through the region that's to the bottom-right of that node.

```{svgbob}
o---▶o---▶o---▶o---▶o---▶o                            o---▶o---▶o                  
|\   |\   |\   |\   |\   |                            |\   |\   |                  
| \  | \  | \  | \  | \  |                            | \  | \  |                  
|  \ |  \ |  \ |  \ |  \ |                            |  \ |  \ |                  
▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼                            ▼   ▼▼   ▼▼                  
o---▶o---▶o---▶o---▶o---▶o                            o---▶o---▶o                  
|\   |\   |\   |\   |\   |                            |\   |\   |                  
| \  | \  | \  | \  | \  |                            | \  | \  |                  
|  \ |  \ |  \ |  \ |  \ |                            |  \ |  \ |                  
▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼                            ▼   ▼▼   ▼▼                  
o---▶o---▶O---▶o---▶o---▶o "sub-divide to..."         o---▶o---▶O    O---▶o---▶o---▶o
|\   |\   |\   |\   |\   |                            "sub-graph1"   |\   |\   |\   |
| \  | \  | \  | \  | \  |                                           | \  | \  | \  |
|  \ |  \ |  \ |  \ |  \ |                                           |  \ |  \ |  \ |
▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼                                           ▼   ▼▼   ▼▼   ▼▼
o---▶o---▶o---▶o---▶o---▶o                                           o---▶o---▶o---▶o
|\   |\   |\   |\   |\   |                                           |\   |\   |\   |
| \  | \  | \  | \  | \  |                                           | \  | \  | \  |
|  \ |  \ |  \ |  \ |  \ |                                           |  \ |  \ |  \ |
▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼                                           ▼   ▼▼   ▼▼   ▼▼
o---▶o---▶o---▶o---▶o---▶o                                           o---▶o---▶o---▶o
                                                                        "sub-graph2" 

* "I know the maximum alignment path travels through the node at (2, 2)"
  "(denoted by a larger circle). Sub-divide the graph at that node. Prior"
  "parts of the path must travel through the top-left, while subsequent"
  "parts must travel through the bottom-right.""
```

By recursively performing this operation, you can pull out all nodes that make up a maximum alignment path:

 * Pick a column, find a node, and sub-divide.
 * For each sub-division from last step: Pick a column, find a node, and sub-divide. 
 * For each sub-division from last step: Pick a column, find a node, and sub-divide. 
 * etc..

Finding the edges between these nodes yields the maximum alignment path. To find the edges between the node found at column n and the node found at column n + 1, isolate the alignment graph between those nodes and perform the standard matrix variant of global alignment. The graph will likely be very small, so the computation and space requirements will likely be very low.

```{output}
ch5_code/src/global_alignment/GlobalAlignment_DivideAndConquer_NodeVariant.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch5}
global_alignment.GlobalAlignment_DivideAndConquer_NodeVariant
TACT
GACGT
embedded_score_matrix
-1
   A  C  T  G
A  1  0  0  0
C  0  1  0  0
T  0  0  1  0
G  0  0  0  1
```

To understand how to find which node in a column a maximum alignment path travels through, consider what happens when edge directions are reversed in an alignment graph. When edge directions are reversed, the alignment graph essentially becomes the alignment graph for the reversed sequences. For example, reversing the edges for the alignment graph of SNACK and AJAX is essentially the same as the alignment graph for KCANS (reverse of SNACK) and XAJA (reverse of AJAX)...

```{svgbob}
        "Original"                     "Reversed strings"              "Reversed edges"      
   S    N    A    C    K            K    C    A    N    S                                    
 o---▶o---▶o---▶o---▶o---▶o       o---▶o---▶o---▶o---▶o---▶o      o◀---o◀---o◀---o◀---o◀---o 
 |\   |\   |\   |\   |\   |       |\   |\   |\   |\   |\   |      ▲▲   ▲▲   ▲▲   ▲▲   ▲▲   ▲ 
A| \  | \  | \  | \  | \  |      X| \  | \  | \  | \  | \  |      | \  | \  | \  | \  | \  | 
 |  \ |  \ |  \ |  \ |  \ |       |  \ |  \ |  \ |  \ |  \ |      |  \ |  \ |  \ |  \ |  \ |A 
 ▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼       ▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼      |   \|   \|   \|   \|   \| 
 o---▶o---▶o---▶o---▶o---▶o       o---▶o---▶o---▶o---▶o---▶o      o◀---o◀---o◀---o◀---o◀---o 
 |\   |\   |\   |\   |\   |       |\   |\   |\   |\   |\   |      ▲▲   ▲▲   ▲▲   ▲▲   ▲▲   ▲ 
J| \  | \  | \  | \  | \  |      A| \  | \  | \  | \  | \  |      | \  | \  | \  | \  | \  | 
 |  \ |  \ |  \ |  \ |  \ |       |  \ |  \ |  \ |  \ |  \ |      |  \ |  \ |  \ |  \ |  \ |J
 ▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼       ▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼      |   \|   \|   \|   \|   \| 
 o---▶o---▶o---▶o---▶o---▶o       o---▶o---▶o---▶o---▶o---▶o      o◀---o◀---o◀---o◀---o◀---o 
 |\   |\   |\   |\   |\   |       |\   |\   |\   |\   |\   |      ▲▲   ▲▲   ▲▲   ▲▲   ▲▲   ▲ 
A| \  | \  | \  | \  | \  |      J| \  | \  | \  | \  | \  |      | \  | \  | \  | \  | \  | 
 |  \ |  \ |  \ |  \ |  \ |       |  \ |  \ |  \ |  \ |  \ |      |  \ |  \ |  \ |  \ |  \ |A
 ▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼       ▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼      |   \|   \|   \|   \|   \| 
 o---▶o---▶o---▶o---▶o---▶o       o---▶o---▶o---▶o---▶o---▶o      o◀---o◀---o◀---o◀---o◀---o 
 |\   |\   |\   |\   |\   |       |\   |\   |\   |\   |\   |      ▲▲   ▲▲   ▲▲   ▲▲   ▲▲   ▲ 
X| \  | \  | \  | \  | \  |      A| \  | \  | \  | \  | \  |      | \  | \  | \  | \  | \  | 
 |  \ |  \ |  \ |  \ |  \ |       |  \ |  \ |  \ |  \ |  \ |      |  \ |  \ |  \ |  \ |  \ |X
 ▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼       ▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼      |   \|   \|   \|   \|   \| 
 o---▶o---▶o---▶o---▶o---▶o       o---▶o---▶o---▶o---▶o---▶o      o◀---o◀---o◀---o◀---o◀---o 
                                                                     S    N    A    C   K   

* "The alignment graph for reversed strings and reversed edges are the"
  "same. They just look different because reversed strings starts at the"
  "top-left and flows towards down-right, while reversed edges starts"
  "bottom-right and flows towards top-left."
```

Between an alignment graph and its reversed edge variant, a maximum alignment path should travel through the same set of nodes. Notice how in the following example, ...

 1. the maximum alignment path in both alignment graphs have the same edges.

 2. the sink node weight in both alignment graphs are the same.

 3. for any node that the maximum alignment path travels through, taking the weight of that node from both alignment graphs and adding them together results in the sink node weight.

 4. for any node that the maximum alignment path *DOES NOT* travel through, taking the weight of that node from both alignment graphs and adding them together results in *LESS THAN* the sink node weight.

```{ch5}
global_alignment.GlobalAlignment_DivideAndConquer_Visualize_EdgeReverseAdd
TACT
GACGT
embedded_score_matrix
-1
   A  C  T  G
A  1  0  0  0
C  0  1  0  0
T  0  0  1  0
G  0  0  0  1
```

Insights #3 and #4 in the list above are the key for this algorithm. Consider an alignment graph getting split down a column into two. The first half has edges traveling in the normal direction but the second half has its edges reversed...

```{svgbob}
0    1    2    3    4    5           0    1    2     2    3    4    5
o---▶o---▶o---▶o---▶o---▶o           o---▶o---▶o     o◀---o◀---o◀---o
|\   |\   |\   |\   |\   |           |\   |\   |     ▲▲   ▲▲   ▲▲   ▲
| \  | \  | \  | \  | \  |           | \  | \  |     | \  | \  | \  |
|  \ |  \ |  \ |  \ |  \ |           |  \ |  \ |     |  \ |  \ |  \ |
▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼           ▼   ▼▼   ▼▼     |   \|   \|   \|
o---▶o---▶o---▶o---▶o---▶o           o---▶o---▶o     o◀---o◀---o◀---o
|\   |\   |\   |\   |\   |           |\   |\   |     ▲▲   ▲▲   ▲▲   ▲
| \  | \  | \  | \  | \  |           | \  | \  |     | \  | \  | \  |
|  \ |  \ |  \ |  \ |  \ |           |  \ |  \ |     |  \ |  \ |  \ |
▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼  split... ▼   ▼▼   ▼▼     |   \|   \|   \|
o---▶o---▶o---▶o---▶o---▶o           o---▶o---▶o     o◀---o◀---o◀---o
|\   |\   |\   |\   |\   |           |\   |\   |     ▲▲   ▲▲   ▲▲   ▲
| \  | \  | \  | \  | \  |           | \  | \  |     | \  | \  | \  |
|  \ |  \ |  \ |  \ |  \ |           |  \ |  \ |     |  \ |  \ |  \ |
▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼           ▼   ▼▼   ▼▼     |   \|   \|   \|
o---▶o---▶o---▶o---▶o---▶o           o---▶o---▶o     o◀---o◀---o◀---o
|\   |\   |\   |\   |\   |           |\   |\   |     ▲▲   ▲▲   ▲▲   ▲
| \  | \  | \  | \  | \  |           | \  | \  |     | \  | \  | \  |
|  \ |  \ |  \ |  \ |  \ |           |  \ |  \ |     |  \ |  \ |  \ |
▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼           ▼   ▼▼   ▼▼     |   \|   \|   \|
o---▶o---▶o---▶o---▶o---▶o           o---▶o---▶o     o◀---o◀---o◀---o
                                        "Half 1"          "Half 2"
                                                     "Reversed edges"   

* "Notice that the column 2 is duplicated when split (half 1's"
  "last column and half 2's first column are both column 2)."
```

Populate node weights for both halves. Then, pair up half 1's last column with half 2's first column. For each row in the pair, add together the node weights in that row. The row with the maximum sum is for a node that a maximum alignment path travels through (insight #4 above). That maximum sum will always end up being the weight of the sink node in the original non-split alignment graph (insight #3 above).

```{ch5}
global_alignment.GlobalAlignment_DivideAndConquer_Visualize_SplitAdd
TACT
GACGT
3
embedded_score_matrix
-1
   A  C  T  G
A  1  0  0  0
C  0  1  0  0
T  0  0  1  0
G  0  0  0  1
```

One way to think about what's happening above is that the algorithm is converging on to the same answer but at a different spot in the alignment graph (the same edge weights are being added). Normally the algorithm converges on to the bottom-right node of the alignment graph. If it were to instead converge on the column just before, the answer would be the same, but the node's position in that column may be different -- it may be any node that ultimately drives to the bottom-right node.

Given that there may be multiple maximum alignment paths for an alignment graph, there may be multiple nodes found per column. Each found node may be for a different maximum alignment path or the same maximum alignment path.

Ultimately, this entire process may be combined with the first idea (only need the previous column in memory to calculate the next column) such that the algorithm requires much lower memory requirements. That is, to find the nodes in a column which maximum alignment paths travel through, the...

 * forward sweep only requires holding on to the weights from column n-1.
 * reverse sweep only requires holding on to the weights from column n+1.

```{output}
ch5_code/src/global_alignment/Global_SweepCombiner.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch5}
global_alignment.Global_SweepCombiner
TACT
GACGT
3
embedded_score_matrix
-1
   A  C  T  G
A  1  0  0  0
C  0  1  0  0
T  0  0  1  0
G  0  0  0  1
```

To recap, the full divide-and-conquer algorithm is as follows: For the middle column in an alignment graph, find a node that a maximum alignment path travels through. Then, sub-divide the alignment graph based on that node. Recursively repeat this process on each sub-division until you have a node from each column -- these are the nodes in a maximum alignment path. The edges between these found nodes can be determined by finding a maximum alignment path between each found node and its neighbouring found node. Concatenate these edges to construct the path.

```{output}
ch5_code/src/global_alignment/Global_FindNodeThatMaxAlignmentPathTravelsThroughAtColumn.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch5}
global_alignment.Global_FindNodeThatMaxAlignmentPathTravelsThroughAtColumn
TACT
GACGT
3
embedded_score_matrix
-1
   A  C  T  G
A  1  0  0  0
C  0  1  0  0
T  0  0  1  0
G  0  0  0  1
```

```{output}
ch5_code/src/global_alignment/GlobalAlignment_DivideAndConquer_NodeVariant.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch5}
global_alignment.GlobalAlignment_DivideAndConquer_NodeVariant
TACT
GACGT
embedded_score_matrix
-1
   A  C  T  G
A  1  0  0  0
C  0  1  0  0
T  0  0  1  0
G  0  0  0  1
```

A slightly more complicated but also more elegant / efficient solution is to extend the algorithm to find the edges for the nodes that it finds. In other words, rather than finding just nodes that maximum alignment paths travel through, find the edges where those nodes are the edge source (node that the edge starts from). 

The algorithm finds all nodes that a maximum alignment path travels through at both column n and column n + 1. For a found node in column n, it's guaranteed that at least one of its immediate neighbours is also a found node. It may be that the node immediately to the ...

 * right of it (same row but column n + 1) is also a found node.
 * bottom of it (1 row down and column n) is also a found node.
 * bottom-right of it (1 row down and column n + 1) is also a found node.

Of the immediate neighbours that are also found nodes, the one forming the edge with the highest weight is the edge that a maximum alignment path travels through.

```{output}
ch5_code/src/global_alignment/Global_FindEdgeThatMaxAlignmentPathTravelsThroughAtColumn.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch5}
global_alignment.Global_FindEdgeThatMaxAlignmentPathTravelsThroughAtColumn
TACT
GACGT
3
embedded_score_matrix
-1
   A  C  T  G
A  1  0  0  0
C  0  1  0  0
T  0  0  1  0
G  0  0  0  1
```

The recursive sub-division process happens just as before, but this time with edges. Finding the maximum alignment path from edges provides two distinct advantages over the previous method of finding the maximum alignment path from nodes:

 * Each sub-division results in one of the sub-graphs being smaller.
   
   ```{svgbob}
   o---▶o---▶o---▶o---▶o---▶o                            o---▶o---▶o               
   |\   |\   |\   |\   |\   |                            |\   |\   |               
   | \  | \  | \  | \  | \  |                            | \  | \  |               
   |  \ |  \ |  \ |  \ |  \ |                            |  \ |  \ |               
   ▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼                            ▼   ▼▼   ▼▼               
   o---▶o---▶o---▶o---▶o---▶o                            o---▶o---▶o               
   |\   |\   |\   |\   |\   |                            |\   |\   |               
   | \  | \  | \  | \  | \  |                            | \  | \  |               
   |  \ |  \ |  \ |  \ |  \ |                            |  \ |  \ |               
   ▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼                            ▼   ▼▼   ▼▼               
   o---▶o---▶O---▶o---▶o---▶o "sub-divide to..."         o---▶o---▶O               
   |\   |\   |\   |\   |\   |                            "sub-graph1"              
   | \  | \  | \  | \  | \  |                                                      
   |  \ |  \ |  \ |  \ |  \ |                                                      
   ▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼                                                      
   o---▶o---▶o---▶O---▶o---▶o                                           O---▶o---▶o
   |\   |\   |\   |\   |\   |                                           |\   |\   |
   | \  | \  | \  | \  | \  |                                           | \  | \  |
   |  \ |  \ |  \ |  \ |  \ |                                           |  \ |  \ |
   ▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼                                           ▼   ▼▼   ▼▼
   o---▶o---▶o---▶o---▶o---▶o                                           o---▶o---▶o
                                                                        "sub-graph2"

   * "I know the maximum alignment path travels through the edge at (2, 2) (3, 3)"
     "(denoted by larger circles). This is what the sub-division based on that edge"
     "looks like. Imagine the size of sub-graph 2 if it sub-division was based on"
     "just the node at (2,2) or (3, 3)."
   ```

 * Since edges are being pulled out, the step that path finds between two neighbouring found nodes is no longer required. This is because sub-division of the alignment graph happens on edges rather than nodes -- eventually all edges in the path will be walked as part of the recursive subdivision.

```{output}
ch5_code/src/global_alignment/GlobalAlignment_DivideAndConquer_EdgeVariant.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch5}
global_alignment.GlobalAlignment_DivideAndConquer_EdgeVariant
TACT
GACGT
embedded_score_matrix
-1
   A  C  T  G
A  1  0  0  0
C  0  1  0  0
T  0  0  1  0
G  0  0  0  1
```

```{note}
The other types of sequence alignment detailed in the sibling sections below don't implement a version of this algorithm. It's fairly straight forward to adapt this algorithm to support those sequence alignment types, but I didn't have the time to do it -- I almost completed a local alignment version but backed out. The same high-level logic applies to those other alignment types: Converge on positions to find nodes/edges in the maximal alignment path and sub-divide on those positions.
```

### Fitting Alignment

`{bm} /(Algorithms\/Sequence Alignment\/Fitting Alignment)_TOPIC/`

```{prereq}
Algorithms/Sequence Alignment/Find Maximum Path/Backtrack Algorithm_TOPIC
Algorithms/Sequence Alignment/Global Alignment_TOPIC
```

**WHAT**: Given two sequences, for all possible substrings of the first sequence, pull out the highest scoring alignment between that substring that the second sequence.

In other words, find the substring within the second sequence that produces the highest scoring alignment with the first sequence. For example, given the sequences GGTTTTTAA and TTCTT, it may be that TTCTT (second sequence) has the highest scoring alignment with TTTTT (substring of the first sequence)...

```
TTC-TT
TT-TTT
```

**WHY**: Searching for a gene's sequence in some larger genome may be problematic because of mutation. The gene sequence being searched for may be slightly off from the gene sequence in the genome.

In the presence of minor mutations, a standard search will fail where a fitting alignment will still be able to find that gene.

#### Graph Algorithm

`{bm} /(Algorithms\/Sequence Alignment\/Fitting Alignment\/Graph Algorithm)_TOPIC/`

```{prereq}
Algorithms/Sequence Alignment/Find Maximum Path_TOPIC
Algorithms/Sequence Alignment/Global Alignment/Graph Algorithm_TOPIC
```

The graph algorithm for fitting alignment is an extension of the graph algorithm for global alignment. Construct the DAG as you would for global alignment, but for each node...

* in the first column that isn't the source node, construct a 0 weight edge from the source node to that node.
* in the last column that isn't the sink node, construct a 0 weight edge from that node to the sink node.

```{ch5}
fitting_alignment.FittingAlignment_Visualize
TAAT
GAAG

embedded_score_matrix
-1
   A  C  T  G
A  1  0  0  0
C  0  1  0  0
T  0  0  1  0
G  0  0  0  1
```

These newly added edges represent hops in the graph -- 0 weight "free rides" to other nodes. The nodes at the destination of each one of these edges will never go below 0: When selecting a backtracking edge, the "free ride" edge will always be chosen over other edges that make the node weight negative.

When finding a maximum alignment path, these "free rides" make it so that the path ...

 * starts from the most appropriate part of the second sequence
 * stops at the most appropriate part of the second sequence

such that if the first sequence is wedged somewhere within the second sequence, that maximum alignment path will be targeted in such a way that it homes in on it.

```{output}
ch5_code/src/fitting_alignment/FittingAlignment_Graph.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch5}
fitting_alignment.FittingAlignment_Graph
AGAC
TAAGAACT
embedded_score_matrix
-1
    A   C   T   G
A   1  -1  -1  -1
C  -1   1  -1  -1
T  -1  -1   1  -1
G  -1  -1  -1   1
```

#### Matrix Algorithm

`{bm} /(Algorithms\/Sequence Alignment\/Fitting Alignment\/Matrix Algorithm)_TOPIC/`

```{prereq}
Algorithms/Sequence Alignment/Fitting Alignment/Graph Algorithm_TOPIC
Algorithms/Sequence Alignment/Global Alignment/Matrix Algorithm_TOPIC
```

**ALGORITHM**:

The following algorithm is an extension to global alignment's matrix algorithm to properly account for the "free ride" edges required by fitting alignment. It's essentially the same as the graph algorithm, except that the implementation is much more sympathetic to modern hardware.

```{output}
ch5_code/src/fitting_alignment/FittingAlignment_Matrix.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch5}
fitting_alignment.FittingAlignment_Matrix
AGAC
TAAGAACT
embedded_score_matrix
-1
    A   C   T   G
A   1  -1  -1  -1
C  -1   1  -1  -1
T  -1  -1   1  -1
G  -1  -1  -1   1
```

### Overlap Alignment

`{bm} /(Algorithms\/Sequence Alignment\/Overlap Alignment)_TOPIC/`

```{prereq}
Algorithms/Sequence Alignment/Find Maximum Path/Backtrack Algorithm_TOPIC
Algorithms/Sequence Alignment/Global Alignment_TOPIC
Algorithms/DNA Assembly_TOPIC
```

**WHAT**: Given two sequences, for all possible substrings that ...

 * end at the first sequence (tail)
 * start at the second sequence (head)

... , pull out the highest scoring alignment.

In other words, find the overlap between the two sequences that produces the highest scoring alignment. For example, given the sequences CCAAGGCT and GGTTTTTAA, it may be that the substrings with the highest scoring alignment are GGCT (tail of the first sequence) and GGT (head of the second sequence)...

```
GGCT
GG-T
```

**WHY**: DNA sequencers frequently produce fragment_SEQs with sequencing errors. Overlap alignments may be used to detect if those fragment_SEQ overlap even in the presence of sequencing errors and minor mutations, making assembly less tedious (overlap graphs / de Bruijn graphs may turn out less tangled).

#### Graph Algorithm

`{bm} /(Algorithms\/Sequence Alignment\/Overlap Alignment\/Graph Algorithm)_TOPIC/`

```{prereq}
Algorithms/Sequence Alignment/Find Maximum Path_TOPIC
Algorithms/Sequence Alignment/Global Alignment/Graph Algorithm_TOPIC
```

The graph algorithm for overlap alignment is an extension of the graph algorithm for global alignment. Construct the DAG as you would for global alignment, but for each node...

* in the first column that isn't the source node, construct a 0 weight edge from the source node to that node.
* in the last row that isn't the sink node, construct a 0 weight edge from that node to the sink node.

```{ch5}
overlap_alignment.OverlapAlignment_Visualize
TAGT
GAGG

embedded_score_matrix
-1
   A  C  T  G
A  1  0  0  0
C  0  1  0  0
T  0  0  1  0
G  0  0  0  1
```

These newly added edges represent hops in the graph -- 0 weight "free rides" to other nodes. The nodes at the destination of each one of these edges will never go below 0: When selecting a backtracking edge, the "free ride" edge will always be chosen over other edges that make the node weight negative. 

When finding a maximum alignment path, these "free rides" make it so that the path ...

* starts from the most appropriate part of the second sequence
* stops at the most appropriate part of the first sequence

such that if there is a matching overlap between the sequences, that maximum alignment path will be targeted in such a way that maximizes that overlap.

```{output}
ch5_code/src/overlap_alignment/OverlapAlignment_Graph.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch5}
overlap_alignment.OverlapAlignment_Graph
AGACAAAT
GGGGAAAC
embedded_score_matrix
-1
    A   C   T   G
A   1  -1  -1  -1
C  -1   1  -1  -1
T  -1  -1   1  -1
G  -1  -1  -1   1
```

#### Matrix Algorithm

`{bm} /(Algorithms\/Sequence Alignment\/Overlap Alignment\/Matrix Algorithm)_TOPIC/`

```{prereq}
Algorithms/Sequence Alignment/Overlap Alignment/Graph Algorithm_TOPIC
Algorithms/Sequence Alignment/Global Alignment/Matrix Algorithm_TOPIC
```

**ALGORITHM**:

The following algorithm is an extension to global alignment's matrix algorithm to properly account for the "free ride" edges required by overlap alignment. It's essentially the same as the graph algorithm, except that the implementation is much more sympathetic to modern hardware.

```{output}
ch5_code/src/overlap_alignment/OverlapAlignment_Matrix.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch5}
overlap_alignment.OverlapAlignment_Matrix
AGACAAAT
GGGGAAAC
embedded_score_matrix
-1
    A   C   T   G
A   1  -1  -1  -1
C  -1   1  -1  -1
T  -1  -1   1  -1
G  -1  -1  -1   1
```

### Local Alignment

`{bm} /(Algorithms\/Sequence Alignment\/Local Alignment)_TOPIC/`

```{prereq}
Algorithms/Sequence Alignment/Find Maximum Path/Backtrack Algorithm_TOPIC
Algorithms/Sequence Alignment/Global Alignment_TOPIC
```

**WHAT**: Given two sequences, for all possible substrings of those sequences, pull out the highest scoring alignment. For example, given the sequences GGTTTTTAA and CCTTCTTAA, it may be that the substrings with the highest scoring alignment are TTTTT (substring of first sequence) and TTCTT (substring of second sequence) ...

```
TTC-TT
TT-TTT
```

**WHY**: Two biological sequences may have strongly related parts rather than being strongly related in their entirety. For example, a class of proteins called NRP synthetase creates peptides without going through a ribosome (non-ribosomal peptides). Each NRP synthetase outputs a specific peptide, where each amino acid in that peptide is pumped out by the unique part of the NRP synthetase responsible for it.

These unique parts are referred to adenylation domains (multiple adenylation domains, 1 per amino acid in created peptide). While the overall sequence between two types of NRP synthetase differ greatly, the sequences between their adenylation domains are similar -- only a handful of positions in an adenylation domain sequence define the type of amino acid it pumps out. As such, local alignment may be used to identify these adenylation domains across different types of NRP synthetase.

```{note}
The WHY section above is giving a high-level use-case for local alignment. If you actually want to perform that use-case you need to get familiar with the protein scoring section: Algorithms/Sequence Alignment/Protein Scoring_TOPIC.
```

#### Graph Algorithm

`{bm} /(Algorithms\/Sequence Alignment\/Local Alignment\/Graph Algorithm)_TOPIC/`

```{prereq}
Algorithms/Sequence Alignment/Find Maximum Path_TOPIC
Algorithms/Sequence Alignment/Global Alignment/Graph Algorithm_TOPIC
```

**ALGORITHM**:

The graph algorithm for local alignment is an extension of the graph algorithm for global alignment. Construct the DAG as you would for global alignment, but for each node...

* that isn't the source node, construct a 0 weight edge from the source node to that node.
* that isn't the sink node, construct a 0 weight edge from that node to the sink node.

```{ch5}
local_alignment.LocalAlignment_Visualize
TAAT
GAAG

embedded_score_matrix
-1
   A  C  T  G
A  1  0  0  0
C  0  1  0  0
T  0  0  1  0
G  0  0  0  1
```

These newly added edges represent hops in the graph -- 0 weight "free rides" to other nodes. The nodes at the destination of each one of these edges will never go below 0: When selecting a backtracking edge, the "free ride" edge will always be chosen over other edges that make the node weight negative.

When finding a maximum alignment path, these "free rides" make it so that if either the...

* prefix of the path sinks the path's weight below zero, there's a "free ride" from the source node that'll supersede it and as such that prefix will get skipped.
* suffix of the path sinks the path's weight below zero, there's a "free ride" to the sink node that'll supersede it and as such that suffix will get skipped.

The maximum alignment path will be targeted in such a way that it homes on the substring within each sequence that produces the highest scoring alignment.

```{output}
ch5_code/src/local_alignment/LocalAlignment_Graph.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch5}
local_alignment.LocalAlignment_Graph
TAGAACT
CGAAG
embedded_score_matrix
-1
    A   C   T   G
A   1  -1  -1  -1
C  -1   1  -1  -1
T  -1  -1   1  -1
G  -1  -1  -1   1
```

#### Matrix Algorithm

`{bm} /(Algorithms\/Sequence Alignment\/Local Alignment\/Matrix Algorithm)_TOPIC/`

```{prereq}
Algorithms/Sequence Alignment/Local Alignment/Graph Algorithm_TOPIC
Algorithms/Sequence Alignment/Global Alignment/Matrix Algorithm_TOPIC
```

**ALGORITHM**:

The following algorithm is an extension to global alignment's matrix algorithm to properly account for the "free ride" edges required by local alignment. It's essentially the same as the graph algorithm, except that the implementation is much more sympathetic to modern hardware.

```{output}
ch5_code/src/local_alignment/LocalAlignment_Matrix.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch5}
local_alignment.LocalAlignment_Matrix
TAGAACT
CGAAG
embedded_score_matrix
-1
    A   C   T   G
A   1  -1  -1  -1
C  -1   1  -1  -1
T  -1  -1   1  -1
G  -1  -1  -1   1
```

### Protein Scoring

`{bm} /(Algorithms\/Sequence Alignment\/Protein Scoring)_TOPIC/`

```{prereq}
Algorithms/Sequence Alignment/Global Alignment_TOPIC
Algorithms/Sequence Alignment/Local Alignment_TOPIC
Algorithms/Sequence Alignment/Fitting Alignment_TOPIC
Algorithms/Sequence Alignment/Overlap Alignment_TOPIC
```

**WHAT**: Given a pair of protein sequences, score those sequences against each other based on the similarity of the amino acids. In this case, similarity is defined as how probable it is that one amino acid mutates to the other while still having the protein remain functional.

**WHY**: Before performing a pair-wise sequence alignment, there needs to be some baseline for how elements within those sequences measure up against each other. In the simplest case, elements are compared using equality: matching elements score 1, while mismatches or indels score 0. However, there are many other cases where element equality isn't a good measure.

Protein sequences are one such case. Biological sequences such as proteins and DNA undergo mutation. Two proteins may be very closely related (e.g. evolved from same parent protein, perform the same function, etc..) but their sequences may have mutated to a point where they appear as being wildly different. To appropriately align protein sequences, amino acid mutation probabilities need to be derived and factored into scoring. For example, there may be good odds that some random protein would still continue to function as-is if some of its Y amino acids were swapped with F.

#### PAM Scoring Matrix

`{bm} /(Algorithms\/Sequence Alignment\/Protein Scoring\/PAM Scoring Matrix)_TOPIC/`

Point accepted mutation (PAM) is a scoring matrix used for sequence alignments of proteins. The scoring matrix is calculated by inspecting / extrapolating mutations as homologous proteins evolve. Specifically, mutations in the DNA sequence that encode some protein may change the resulting amino acid sequence for that protein. Those mutations that...

 * impair the ability of the protein to function aren't likely to survive, and as such are given a low score. 
 * keep the protein functional are likely to survive, and as such are given a normal or high score.
 
PAM matrices are developed iteratively. An initial PAM matrix is calculated by aligning extremely similar protein sequences using a simple scoring model (1 for match, 0 for mismatch / indel). That sequence alignment then provides the scoring model for the next iteration. For example, the alignment for the initial iteration may have determined that D may be a suitable substitution for W. As such, the sequence alignment for the next iteration will score more than 0 (e.g. 1) if it encounters D being compared to W.

Other factors are also brought into the mix when developing scores for PAM matrices. For example, the ...

 * likelihood of amino acid mutations (e.g. Cys and Trp are the least mutable amino acids).
 * speed of evolution (e.g. some mutations were more probably in species 100 million years ago vs 1 million years ago).

It's said that PAM is focused on tracking the evolutionary origins of proteins. Sequences that are 99% similar are said to be 1 PAM unit diverged, where a PAM unit is the amount of time it takes an "average" protein to mutate 1% of its amino acids. PAM1 (the initial scoring matrix) was defined by performing many sequence alignments between proteins that are 99% similar (1 PAM unit diverged).

```{note}
[Here](http://www.compbio.dundee.ac.uk/papers/rev93_1/subsection3_3_5.html) and [here](https://en.wikipedia.org/w/index.php?title=Point_accepted_mutation&oldid=1002281881#Comparing_PAM_and_BLOSUM) both seem to say that BLOSUM supersedes PAM as a scoring matrix for protein sequences.

> Although both matrices produce similar scoring outcomes they were generated using differing methodologies. The BLOSUM matrices were generated directly from the amino acid differences in aligned blocks that have diverged to varying degree_NORMs the PAM matrices reflect the extrapolation of evolutionary information based on closely related sequences to longer timescales

> Henikoff and Henikoff [16] have compared the BLOSUM matrices to PAM, PET, Overington, Gonnet [17] and multiple PAM matrices by evaluating how effectively the matrices can detect known member_NORMs of a protein family from a database when searching with the ungapped local alignment program BLAST [18]. They conclude that overall the BLOSUM 62 matrix is the most effective.
```

PAM250 is the most commonly used variant:

```{output}
ch5_code/src/PAM250.txt

([\s\S]+)
```

```{note}
The above matrix was supplied by the Pevzner book. You can find it online [here](https://swift.cmbi.umcn.nl/teach/aainfo/pam250.shtml), but the indel scores on that website are set to -8 Whereas in the Pevzner book I've also seen them set to -5. I don't know which is correct. I don't know if PAM250 defines a constant for indels.
```

#### BLOSUM Scoring Matrix

`{bm} /(Algorithms\/Sequence Alignment\/Protein Scoring\/BLOSUM Scoring Matrix)_TOPIC/`

Blocks amino acid substitution matrix (BLOSUM) is a scoring matrix used for sequence alignments of proteins. The scoring matrix is calculated by scanning a protein database for highly conserved regions between similar proteins, where the mutations between those highly conserved regions define the scores. Specifically, those highly conserved regions are identified based on local alignments without support for indels (gaps not allowed). Non-matching positions in that alignment define potentially acceptable mutations.

Several sets of BLOSUM matrices exist, each identified by a different number. This number defines the similarity of the sequences used to create the matrix: The protein database sequences used to derive the matrix are filtered such that only those with >= n% similarity are used, where n is the number. For example, ...
   
 * BLOSUM80 is created from sequences that are >= 80% similar.
 * BLOSUM45 is created from sequences that are >= 45% similar.
    
As such, BLOSUM matrices with higher numbers are designed to compare more closely related sequences while those with lower numbers are designed to score more distant related sequences.

BLOSUM62 is the most commonly used variant since "experimentation has shown that it's among the best for detecting weak similarities":

```{output}
ch5_code/src/BLOSUM62.txt

([\s\S]+)
```

```{note}
The above matrix was supplied by the Pevzner book. You can find it online [here](https://www.ncbi.nlm.nih.gov/Class/FieldGuide/BLOSUM62.txt), but the indel scores on that website are set to -4 whereas in the Pevzner book I've seen them set to -5. I don't know which is correct. I don't know if BLOSUM62 defines a constant for indels.
```

### Extended Gap Scoring

`{bm} /(Algorithms\/Sequence Alignment\/Extended Gap Scoring)_TOPIC/`

```{prereq}
Algorithms/Sequence Alignment/Global Alignment_TOPIC
Algorithms/Sequence Alignment/Local Alignment_TOPIC
Algorithms/Sequence Alignment/Fitting Alignment_TOPIC
Algorithms/Sequence Alignment/Overlap Alignment_TOPIC
Algorithms/Sequence Alignment/Protein Scoring_TOPIC
```

**WHAT**: When performing sequence alignment, prefer contiguous indels in a sequence vs individual indels. This is done by scoring contiguous indels differently than individual indels:

 * Individual indels are penalized by choosing the normal indel score (e.g. score of -5).
 * Contiguous indels are penalized by choosing the normal indel score for the first indel in the list (e.g. score of -5), then all other indels are scored using a better *extended* indel score (e.g. score of -0.1).

For example, given an alignment region where one of the sequences has 3 contiguous indels, the traditional method would assign a score of -15 (-5 for each indel) while this method would assign a score of -5.2 (-5 for starting indel, -0.1 for each subsequent indel)...

```
AAATTTAATA
AAA---AA-A

Score from indels using traditional scoring:   -5   + -5   + -5   + -5   = -20
Score from indels using extended gap scoring:  -5   + -0.1 + -0.1 + -5   = -10.2
```

**WHY**: DNA mutations are more likely to happen in chunks rather than point mutations (e.g. transposons). Extended gap scoring helps account for that fact. Since DNA encode proteins (codons), this effects proteins as well.

#### Naive Algorithm

`{bm} /(Algorithms\/Sequence Alignment\/Extended Gap Scoring\/Naive Algorithm)_TOPIC/`

**ALGORITHM**:

The naive way to perform extended gap scoring is to introduce a new edge for each contiguous indel. For example, given the alignment graph...

```{svgbob}
   T    A    A   
 o---▶o---▶o---▶o
 |\   |\   |\   |
G| \  | \  | \  |
 |  \ |  \ |  \ |
 ▼   ▼▼   ▼▼   ▼▼
 o---▶o---▶o---▶o
 |\   |\   |\   |
A| \  | \  | \  |
 |  \ |  \ |  \ |
 ▼   ▼▼   ▼▼   ▼▼
 o---▶o---▶o---▶o
 |\   |\   |\   |
G| \  | \  | \  |
 |  \ |  \ |  \ |
 ▼   ▼▼   ▼▼   ▼▼
 o---▶o---▶o---▶o
```

 * each row would have an edge added to represent a contiguous indels.

   ```{svgbob}
   "Row before:"                    "Row after:"
                                    
       T       A       A                       TAA
   o------▶o------▶o------▶o           ,-----------------.
                                      /     TA            \
                                     /  ,-------.   AA     \
                                    ,  /       ,-\-------.  .
                                    | /       /   \       \ |
                                    |/  T    /  A  ▼    A  ▼▼
                                    o------▶o------▶o------▶o
   ```

 * each column would have an edge added to represent a contiguous indels.

   ```{svgbob}
   "Column before:"     "Column after:"
                        
    o                    o---.
    |                    |\   \
   G|                   G| \   \
    |                    |  \   \
    ▼                    ▼   .   .
    o                    o   |GA |
    |                    |\  ,   |
   A|                   A| \/    |GAG 
    |                    | /.    |
    ▼                    ▼▼ |    |
    o                    o  |AG  |
    |                    |  |    .
   G|                   G|  .   /
    |                    | /   /
    ▼                    ▼▼   /
    o                    o◀--'
   ```

Each added edge represents a contiguous set of indels. Contiguous indels are penalized by choosing the normal indel score for the first indel in the list (e.g. score of -5), then all other indels are scored using a better *extended* indel score (e.g. score of -0.1). As such, the maximum alignment path will choose one of these contiguous indel edges over individual indel edges or poor substitution choices such as those in PAM / BLOSUM scoring matrices.

```{ch5}
affine_gap_alignment.AffineGapAlignment_Basic_Visualize
TAA
GAG

embedded_score_matrix
-1
-0.1
   A  C  T  G
A  1  0  0  0
C  0  1  0  0
T  0  0  1  0
G  0  0  0  1
```

The problem with this algorithm is that as the sequence lengths grow, the number of added edges explodes. It isn't practical for anything other than short sequences.

```{output}
ch5_code/src/affine_gap_alignment/AffineGapAlignment_Basic_Graph.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch5}
affine_gap_alignment.AffineGapAlignment_Basic_Graph
TAGGCGGAT
TACCCCCAT
embedded_score_matrix
-1
-0.1
    A   C   T   G
A   1  -1  -1  -1
C  -1   1  -1  -1
T  -1  -1   1  -1
G  -1  -1  -1   1
```

```{note}
The algorithm above was applied on global alignment, but it should be obvious how to apply it to the other alignment types discussed.
```

#### Layer Algorithm

`{bm} /(Algorithms\/Sequence Alignment\/Extended Gap Scoring\/Layer Algorithm)_TOPIC/`

```{prereq}
Algorithms/Sequence Alignment/Extended Gap Scoring/Naive Algorithm_TOPIC
```

**ALGORITHM**:

Recall that the problem with the naive algorithm algorithm is that as the sequence lengths grow, the number of added edges explodes. It isn't practical for anything other than short sequences. A better algorithm that achieves the exact same result is the layer algorithm. The layer algorithm breaks an alignment graph into 3 distinct layers:

 1. horizontal edges go into their own layer.
 2. diagonal edges go into their own layer.
 3. vertical edges go into their own layer.

The edge weights in the horizontal and diagonal layers are updated such that they use the *extended* indel score (e.g. -0.1). Then, for each node (x, y) in the diagonal layer, ...

 * an edge is added to node (x+1, y) in the horizontal layer with a normal indel score (e.g. -5).
 * an edge is added to node (x, y+1) in the vertical layer with a normal indel score (e.g. -5).

Similarly, for each node (x, y) in both the horizontal and vertical layers that an edge from the diagonal layer points to, create a 0 weight "free ride" edge back to node (x, y) in the diagonal layer. These "free ride" edges are the same as the "free ride" edges in local alignment / fitting alignment / overlap alignment -- they hop across the alignment graph without adding anything to the sequence alignment.

The source node and sink node are at the top-left node and bottom-right node (respectively) of the diagonal layer.

```{ch5}
affine_gap_alignment.AffineGapAlignment_Layer_Visualize
TAA
GAG

embedded_score_matrix
-1
-0.1
   A  C  T  G
A  1  0  0  0
C  0  1  0  0
T  0  0  1  0
G  0  0  0  1
```

The way to think about this layered structure alignment graph is that the hop from a node in the diagonal layer to a node in the horizontal/vertical layer will always have a normal indel score (e.g. -5). From there it either has the option to hop back to the diagonal layer (via the "free ride" edge) or continue pushing through indels using the less penalizing *extended* indel score (e.g. -0.1).

This layered structure produces 3 times the number of nodes, but for longer sequences it has far less edges than the naive method.

```{output}
ch5_code/src/affine_gap_alignment/AffineGapAlignment_Layer_Graph.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch5}
affine_gap_alignment.AffineGapAlignment_Layer_Graph
TGGCGG
TCCCCC
embedded_score_matrix
-1
-0.1
    A   C   T   G
A   1  -1  -1  -1
C  -1   1  -1  -1
T  -1  -1   1  -1
G  -1  -1  -1   1
```

```{note}
The algorithm above was applied on global alignment, but it should be obvious how to apply it to the other alignment types discussed.
```

### Multiple Alignment

`{bm} /(Algorithms\/Sequence Alignment\/Multiple Alignment)_TOPIC/`

```{prereq}
Algorithms/Sequence Alignment/Global Alignment_TOPIC
Algorithms/Sequence Alignment/Local Alignment_TOPIC
Algorithms/Sequence Alignment/Fitting Alignment_TOPIC
Algorithms/Sequence Alignment/Overlap Alignment_TOPIC
Algorithms/Sequence Alignment/Protein Scoring_TOPIC
Algorithms/Sequence Alignment/Extended Gap Scoring_TOPIC
```

**WHAT**: Given *more than* two sequences, perform sequence alignment and pull out the highest scoring alignment.

**WHY**: Proteins that perform the same function but are distantly related are likely to have similar regions. The problem is that a 2-way sequence alignment may have a hard time identifying those similar regions, whereas an n-way sequence alignment (n > 2) will likely reveal much more / more accurate regions.

```{note}
Quote from Pevzner book: "Bioinformaticians sometimes say that pairwise alignment whispers and multiple alignment shouts."
```

#### Graph Algorithm

`{bm} /(Algorithms\/Sequence Alignment\/Multiple Alignment\/Graph Algorithm)_TOPIC/`

**ALGORITHM**:

Thinking about sequence alignment geometrically, adding another sequence to a sequence alignment graph is akin to adding a new dimension. For example, a sequence alignment graph with...

 * 2 sequences is represented as a 2D square.
 * 3 sequences is represented as a 3D cube.
 * 4 sequences is represented as a 4D hypercube.
 * etc..

```{svgbob}
                  "3 sequences"
                    +---------+
"2 sequences"      /|        /|
                  / |       / |
+---------+      +--+------+  |
|         |      |  |      |  |
|         |      |  +------+--+
|         |      | /       | /
|         |      |/        |/
+---------+      +---------+
```

The alignment possibilities at each step of a sequence alignment may be thought of as a vertex shooting out edges to all other vertices in the geometry. For example, in a sequence alignment with 2 sequences, the vertex (0, 0) shoots out an edge to vertices ...

 * (1, 0) - represents keep first but skip second.
 * (0, 1) - represents skip first but keep second.
 * (1, 1) - represents keep both.

The vertex coordinates may be thought of as analogs of whether to keep or skip an element. Each coordinate position corresponds to a sequence element (first coordinate = first sequence's element, second coordinate = second sequence's element). If a coordinate is set to ...

 * 1, the element is kept.
 * 0, the element is skipped.

```{latex}
\documentclass{standalone}
\usepackage{pgf, tikz, pagecolor}
\usetikzlibrary{arrows, automata}
\begin{document}
    \pagecolor{white}
    \begin{tikzpicture}
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (0, 0)    (N00) {(0, 0)};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (0, -10)  (N01) {(0, 1)};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (10, 0)   (N10) {(1, 0)};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (10, -10) (N11) {(1, 1)};

        \draw[line width = 1px, black, dotted] (N01) -- (N11);
        \draw[line width = 1px, black, dotted] (N10) -- (N11);
        \draw[->, >=stealth, line width = 2px, gray!40] (N00) to [] node [align=center, midway, color=black] {—\\ B} (N01);
        \draw[->, >=stealth, line width = 2px, gray!40] (N00) to [] node [align=center, midway, color=black] {A\\ —} (N10);
        \draw[->, >=stealth, line width = 2px, gray!40] (N00) to [] node [align=center, midway, color=black] {A\\ B} (N11);
    \end{tikzpicture}
\end{document}
```

This same logic extends to sequence alignment with 3 or more sequences. For example, in a sequence alignment with 3 sequences, the vertex (0, 0, 0) shoots out an edge to all other vertices in the cube. The vertex coordinates define which sequence elements should be kept or skipped based on the same rules described above.

```{latex}
\documentclass{standalone}
\usepackage{pgf, tikz, pagecolor}
\usetikzlibrary{arrows, automata}
\begin{document}
    \pagecolor{white}
    \begin{tikzpicture}
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (0, 0)    (N000) {(0, 0, 0)};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (2, 3)    (N001) {(0, 0, 1)};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (0, -10)  (N010) {(0, 1, 0)};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (2, -7)   (N011) {(0, 1, 1)};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (10, 0)   (N100) {(1, 0, 0)};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (12, 3)   (N101) {(1, 0, 1)};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (10, -10) (N110) {(1, 1, 0)};
        \node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at (12, -7)  (N111) {(1, 1, 1)};

        \draw[line width = 1px, black, dotted] (N001) -- (N101);
        \draw[line width = 1px, black, dotted] (N001) -- (N011);
        \draw[line width = 1px, black, dotted] (N011) -- (N111);
        \draw[line width = 1px, black, dotted] (N010) -- (N011);
        \draw[line width = 1px, black, dotted] (N010) -- (N110);
        \draw[line width = 1px, black, dotted] (N101) -- (N100);
        \draw[line width = 1px, black, dotted] (N101) -- (N111);
        \draw[line width = 1px, black, dotted] (N110) -- (N111);
        \draw[->, >=stealth, line width = 2px, gray!40] (N000) to [] node [align=center, midway, color=black] {—\\ —\\ C} (N001);
        \draw[->, >=stealth, line width = 2px, gray!40] (N000) to [] node [align=center, midway, color=black] {—\\ B\\ —} (N010);
        \draw[->, >=stealth, line width = 2px, gray!40] (N000) to [] node [align=center, midway, color=black] {—\\ B\\ C} (N011);
        \draw[->, >=stealth, line width = 2px, gray!40] (N000) to [] node [align=center, midway, color=black] {A\\ —\\ —} (N100);
        \draw[->, >=stealth, line width = 2px, gray!40] (N000) to [] node [align=center, midway, color=black] {A\\ —\\ C} (N101);
        \draw[->, >=stealth, line width = 2px, gray!40] (N000) to [] node [align=center, midway, color=black] {A\\ B\\ —} (N110);
        \draw[->, >=stealth, line width = 2px, gray!40] (N000) to [] node [align=center, midway, color=black] {A\\ B\\ C} (N111);
        \draw[line width = 1px, black, dotted] (N100) -- (N110);
    \end{tikzpicture}
\end{document}
```

```{output}
ch5_code/src/graph/GraphGridCreate.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{output}
ch5_code/src/global_alignment/GlobalMultipleAlignment_Graph.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch5}
global_alignment.GlobalMultipleAlignment_Graph
3
TATTATTAT
GATTATGATTAT
TACCATTACAT
embedded_score_matrix
-1
A A A 1
A A C -1
A A T -1
A A G -1
A C A -1
A C C -1
A C T -1
A C G -1
A T A -1
A T C -1
A T T -1
A T G -1
A G A -1
A G C -1
A G T -1
A G G -1
C A A -1
C A C -1
C A T -1
C A G -1
C C A -1
C C C 1
C C T -1
C C G -1
C T A -1
C T C -1
C T T -1
C T G -1
C G A -1
C G C -1
C G T -1
C G G -1
T A A -1
T A C -1
T A T -1
T A G -1
T C A -1
T C C -1
T C T -1
T C G -1
T T A -1
T T C -1
T T T 1
T T G -1
T G A -1
T G C -1
T G T -1
T G G -1
G A A -1
G A C -1
G A T -1
G A G -1
G C A -1
G C C -1
G C T -1
G C G -1
G T A -1
G T C -1
G T T -1
G T G -1
G G A -1
G G C -1
G G T -1
G G G 1
```

```{note}
The multiple alignment algorithm displayed above was specifically for on global alignment on a graph implementation, but it should be obvious how to apply it to most of the other alignment types (e.g. local alignment).
```

#### Matrix Algorithm

`{bm} /(Algorithms\/Sequence Alignment\/Multiple Alignment\/Matrix Algorithm)_TOPIC/`

```{prereq}
Algorithms/Sequence Alignment/Multiple Alignment/Graph Algorithm_TOPIC
Algorithms/Sequence Alignment/Global Alignment/Matrix Algorithm_TOPIC
```

The following algorithm is essentially the same as the graph algorithm, except that the implementation is much more sympathetic to modern hardware. The alignment graph is represented as an N-dimensional matrix where each element in the matrix represents a node in the alignment graph. This is similar to the 2D matrix used for global alignment's matrix implementation.

```{output}
ch5_code/src/global_alignment/GlobalMultipleAlignment_Matrix.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch5}
global_alignment.GlobalMultipleAlignment_Matrix
3
TATTATTAT
GATTATGATTAT
TACCATTACAT
embedded_score_matrix
-1
A A A 1
A A C -1
A A T -1
A A G -1
A C A -1
A C C -1
A C T -1
A C G -1
A T A -1
A T C -1
A T T -1
A T G -1
A G A -1
A G C -1
A G T -1
A G G -1
C A A -1
C A C -1
C A T -1
C A G -1
C C A -1
C C C 1
C C T -1
C C G -1
C T A -1
C T C -1
C T T -1
C T G -1
C G A -1
C G C -1
C G T -1
C G G -1
T A A -1
T A C -1
T A T -1
T A G -1
T C A -1
T C C -1
T C T -1
T C G -1
T T A -1
T T C -1
T T T 1
T T G -1
T G A -1
T G C -1
T G T -1
T G G -1
G A A -1
G A C -1
G A T -1
G A G -1
G C A -1
G C C -1
G C T -1
G C G -1
G T A -1
G T C -1
G T T -1
G T G -1
G G A -1
G G C -1
G G T -1
G G G 1
```

```{note}
The multiple alignment algorithm displayed above was specifically for on global alignment on a graph implementation, but it should be obvious how to apply it to most of the other alignment types (e.g. local alignment). With a little bit of effort it can also be converted to using the divide-and-conquer algorithm discussed earlier (there aren't that many leaps in logic).
```

#### Greedy Algorithm

```{prereq}
Algorithms/Sequence Alignment/Multiple Alignment/Graph Algorithm_TOPIC
Algorithms/Sequence Alignment/Multiple Alignment/Matrix Algorithm_TOPIC
Algorithms/Sequence Alignment/Sum-of-Pairs Scoring_TOPIC
Algorithms/Sequence Alignment/Global Alignment/Divide-and-Conquer Algorithm_TOPIC
Algorithms/Motif/Motif Matrix Profile_TOPIC
```

```{note}
The Pevzner book challenged you to come up with a greedy algorithm for multiple alignment using profile matrices. This is what I was able to come up with. I have no idea if my logic is correct / optimal, but with toy sequences that are highly related it seems to perform well. 

UPDATE: This algorithm seems to work well for the final assignment. ~380 a-domain sequences were aligned in about 2 days and it produced an okay/good looking alignment. Aligning those sequences using normal multiple alignment would be impossible -- nowhere near enough memory or speed available.
```

For an n-way sequence alignment, the greedy algorithm starts by finding the 2 sequences that produce the highest scoring 2-way sequence alignment. That alignment is then used to build a profile matrix. For example, the alignment of TRELLO and MELLOW results in the following alignment:

| 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| T | R | E | L | L | O | - |
| - | M | E | L | L | O | W |

That alignment then turns into the following profile matrix:

|                  |  0  |  1  |  2  |  3  |  4  |  5  |  6  |
|------------------|-----|-----|-----|-----|-----|-----|-----|
| Probability of T | 0.5 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Probability of R | 0.0 | 0.5 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Probability of M | 0.0 | 0.5 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Probability of E | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Probability of L | 0.0 | 0.0 | 0.0 | 1.0 | 1.0 | 0.0 | 0.0 |
| Probability of O | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 |
| Probability of W | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.5 |

Then, 2-way sequence alignments are performed between the *profile matrix* and the remaining sequences. For example, if the letter V is scored against column 1 of the profile matrix, the algorithm would score W against each letter stored in the profile matrix using the same scoring matrix as the initial 2-way sequence alignment. Each score would then get weighted by the corresponding probability in column 2 and the highest one would be chosen as the final score.

```python
max(
    score('W', 'T') * profile_mat[1]['T'],
    score('W', 'R') * profile_mat[1]['R'],
    score('W', 'M') * profile_mat[1]['M'],
    score('W', 'E') * profile_mat[1]['E'],
    score('W', 'L') * profile_mat[1]['L'],
    score('W', 'O') * profile_mat[1]['O'],
    score('W', 'W') * profile_mat[1]['W']
)
```

Of all the remaining sequences, the one with the highest scoring alignment is removed and its alignment is added to the profile matrix. The process repeats until no more sequences are left.

````{note}
The logic above is what was used to solve the final assignment. But, after thinking about it some more it probably isn't entirely correct. Elements that haven't been encountered yet should be left unset in the profile matrix. If this change were applied, the example above would end up looking more like this...

|                  |  0  |  1  |  2  |  3  |  4  |  5  |  6  |
|------------------|-----|-----|-----|-----|-----|-----|-----|
| Probability of T | 0.5 |     |     |     |     |     |     |
| Probability of R |     | 0.5 |     |     |     |     |     |
| Probability of M |     | 0.5 |     |     |     |     |     |
| Probability of E |     |     | 1.0 |     |     |     |     |
| Probability of L |     |     |     | 1.0 | 1.0 |     |     |
| Probability of O |     |     |     |     |     | 1.0 |     |
| Probability of W |     |     |     |     |     |     | 0.5 |

Then, when scoring an element against a column in the profile matrix, ignore the unset elements in the column. The score calculation in the example above would end up being...

```python
max(
    score('W', 'R') * profile_mat[1]['R'],
    score('W', 'M') * profile_mat[1]['M']
)
```
````

For n-way sequence alignments where n is large (e.g. n=300) and the sequences are highly related, the greedy algorithm performs well but it may produce sub-optimal results. In contrast, the amount of memory and computation required for an n-way sequence alignment using the standard graph algorithm goes up exponentially as n grows linearly. For realistic biological sequences, the normal algorithm will likely fail for any n past 3 or 4. Adapting the divide-and-conquer algorithm for n-way sequence alignment will help, but even that only allows for targeting a slightly larger n (e.g. n=6).

```{output}
ch5_code/src/global_alignment/GlobalMultipleAlignment_Greedy.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch5}
global_alignment.GlobalMultipleAlignment_Greedy
4
TATTATTAT
GATTATGATTAT
TACCATTACAT
CTATTAGGAT
embedded_score_matrix
-1
    A   C   T   G
A   1  -1  -1  -1
C  -1   1  -1  -1
T  -1  -1   1  -1
G  -1  -1  -1   1
```

### Sum-of-Pairs Scoring

`{bm} /(Algorithms\/Sequence Alignment\/Sum-of-Pairs Scoring)_TOPIC/`

```{prereq}
Algorithms/Sequence Alignment/Protein Scoring_TOPIC
Algorithms/Sequence Alignment/Multiple Alignment_TOPIC
```

**WHAT**: If a scoring model already exists for 2-way sequence alignments, that scoring model can be used as the basis for n-way sequence alignments (where n > 2). For a possible alignment position, generate all possible pairs between the elements at that position and score them. Then, sum those scores to get the final score for that alignment position.

**WHY**: Traditionally, scoring an n-way alignment requires an n-dimensional scoring matrix. For example, protein sequences have 20 possible element types (1 for each proteinogenic amino acid). That means a...

 * 2-way alignment with protein sequences requires `{kt} 20^2` scores.
 * 3-way alignment with protein sequences requires `{kt} 20^3` scores.
 * 4-way alignment with protein sequences requires `{kt} 20^4` scores.
 * 5-way alignment with protein sequences requires `{kt} 20^5` scores.
 * ...

Creating probabilistic scoring models such a BLOSUM and PAM for n-way alignments where n > 2 is impractical. Sum-of-pairs scoring is a viable alternative.

**ALGORITHM**:

```{output}
ch5_code/src/scoring/SumOfPairsWeightLookup.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch5}
scoring.SumOfPairsWeightLookup
6
M
E
A

L
Y
file_score_matrix
-1
BLOSUM62.txt
```

### Entropy Scoring

`{bm} /(Algorithms\/Sequence Alignment\/Entropy Scoring)_TOPIC/`

```{prereq}
Algorithms/Motif/Motif Matrix Score/Entropy Algorithm_TOPIC
Algorithms/Sequence Alignment/Multiple Alignment_TOPIC
```

**WHAT**: When performing an n-way sequence alignment, score each possible alignment position based on entropy.

**WHY**: Entropy is a measure of uncertainty. The idea is that the more "certain" an alignment position is, the more likely it is to be correct.

**ALGORITHM**:

```{output}
ch5_code/src/scoring/EntropyWeightLookup.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch5}
scoring.EntropyWeightLookup
5
A
A
A
A
C
-2
```

## Synteny

`{bm} /(Algorithms\/Synteny)_TOPIC/`

```{prereq}
Algorithms/K-mer_TOPIC
```

A form of DNA mutation, called genome rearrangement, is when chromosomes go through structural changes such as ...

* shuffling segments (translocation, fission, fusion) 
* flipping direction (reversal).
* duplicating segments.
* deleting segments.

When a new species branches off from an existing one, genome rearrangements are responsible for at least some of the divergence. That is, the two related genomes will share long stretches of similar genes, but these long stretches will appear as if they had been randomly cut-and-paste and / or randomly reversed when compared to the other.

```{svgbob}
                                    "translocate"
                 .---------------------------------------------------.
                 |                              "reverse"            |
                 |                    .---------------------------.  |
            .----+---.        .-------+------.                    |  |
"GENOME1:"   G1 -> G2 -> G3 -> G4 -> G5 -> G6 -> G7 -> G8 -> G9   |  |
"GENOME2:"   G3 -> G6 <- G5 <- G4 -> G7 -> G8 -> G9 -> G1 -> G2   |  |
                  '-------+------'                    '----+---'  |  |
                          `--------------------------------+------'  |
                                                           `---------'
```

These long stretches of similar genes are called synteny blocks. The example above has 4 synteny blocks:

 * \[G1, G2\]
 * \[G3\]
 * \[G4, G5, G6\], although they're reversed
 * \[G7, G8, G9\]


```{svgbob}
3'|                          
  |                 ^       
  |                / "[G7, G8, G9]"
  |               /          
 g|              *           
 e|         *              
 n|        / "[G4, G5, G6]"
 o|       /                 
 m|      v                  
 e|  ^                     
 1| / "[G3]"                  
  |*                       
  |                       ^
  |                      / 
  |                     / "[G1, G2]"
5'|                    *   
  +--------------------------
   5'        genome2       3'
```

Real-life examples of species that share synteny blocks include ...

 * mouse and human, which share ~280 synteny blocks across their chromosomes.
 * Escherichia coli and Salmonella enterica, which share ~5 synteny blocks.

### Genomic Dot Plot

`{bm} /(Algorithms\/Synteny\/Genomic Dot Plot)_TOPIC/`

**WHAT**: Given two genomes, create a 2D plot where each axis is assigned to one of the genomes and a dot is placed at each coordinate containing a match, where a match is either a shared k-mer or a k-mer and its reverse complement. These plots are called genomic dot plots.

```{svgbob}
"Consider each shared 5-mer, shown as a line, to be a dot."
* "N = normal match"
* "R = reverse complement match"

  3' 5'|   
   G C |                                     ^            
       |                                    /
   G C |                                   /                
       |                                  /
   T A |                                 / N: "ACTGG vs ACTGG"         
       |                                /  
   C G |                               /                   
       |                              /      
   A T |                             *                    
       |   
   C C |                                                     ^
       |                                                    /
   G A |                                                   /
       |                                                  /
   T G |                                                 / N: "CATGC vs CATGC"
       |                                                /  
 g A T |                                               /         *
 e     |                                              /           \
 n C G |                                             *             \
 o     |                                                            \
 m C G |                                                             \ R: "CCCCA vs TGGGG"
 e     |                                                              \
 1 C G |   *                                                           \
       |    \                                                           \
   C G |     \                                                           v
       |      \  
   A T |       \ R: "AAACC vs GGTTT"                                      
       |        \
   A T |         \                                          
       |          \
   A T |           v                                     
       |   
   G C |                                                                   ^
       |                                                                  /
   G C |                                                                 / 
       |                                                                / 
   G C |                                                               / N: "GGGGG vs GGGGG" 
       |                                                              /  
   G C |                                                             /    
       |                                                            /      
   G C |                                                           *        
  5' 3'|                                                                   
       +-----------------------------------------------------------------------
        5' G G T T T A G G T G A C T T A C T G G A A C A T G C T T G G G G G 3'
        3' C C A A A T C C A C T G A A T G A C C T T G T C A G T T C C C C C 5'
                                       genome2
```

**WHY**: Genomic dot plots are used for identifying synteny blocks between two genomes.   

**ALGORITHM**:

The following algorithm finds direct matches. However, a better solution may be to consider anything with some hamming distance as a match. Doing so would require non-trivial changes to the algorithm (e.g. modifying the lookup to use bloom filters).

```{output}
ch6_code/src/synteny_graph/Match.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch6}
synteny_graph.Match
5
linear
A0, GGGGGAAACCCCATGCACTGG
B0, GGTTTAGGTGACTTACTGGAACATGCTTGGGGG
```

```{note}
Rather than just showing dots at matches, the plot below draws a line over the entire match.
```

### Synteny Graph

`{bm} /(Algorithms\/Synteny\/Synteny Graph)_TOPIC/`

```{prereq}
Algorithms/Synteny/Genomic Dot Plot_TOPIC
```

**WHAT**: Given the genomic dot-plot for two genomes, connect dots that are close together and going in the same direction. This process is commonly referred to as clustering. A clustered genomic dot plot is called a synteny graph.

**WHY**:  Clustering together matches reveals synteny blocks.

```{svgbob}
 * "N = normal k-mer match"
 * "R = reverse complement k-mer match"

  ^                                                                                    ^
3'|                                                                                  3'|                                                                 
  |  R                              R                                                  |  *                                                              
  |   R           N                                                                    |   \                                                             
  |    R               R                                                               |    \                                                            
  |      R                           R           N                                     |     \                                                           
  |       R                                                                            |      \                                                          
  |       R               N                                                            |     A \                                                         
 g|        R                                                                          g|        \                                                        
 e|          R                   R           N                                        e|         \                                                      
 n|           R                                                                       n|          \                                                     
 o|            R                                     R                   ------->     o|           v                                                    
 m|   N                        N                                         CLUSTER      m|                           ^                                    
 e|                          N            N                                           e|                        C /                                      
 1|      N                  N                                                         1|                         /                                      
  |                        N               N         N                                 |                        *                                          
  |                 R                                                                  |                 *                                               
  |                   R                                                                |                  \                                             
  |                    R                                                               |                 B \                                           
  |    R                R                                                              |                    v                                               
  |                                           R              R                         |                                           *                     
  |             N              N                R                                      |                                            \                    
  |                                              R           R                         |                                           D \                    
5'|       R             R                   R     R                                  5'|                                              v                  
  +----------------------------------------------------------------->                  +----------------------------------------------------------------->
   5'                          genome2                            3'                    5'                          genome2                            3'

 * "Remember that the direction of DNA is 5' to 3'."
```

```{svgbob}
"For each genome, prefix the synteny block with..."
* "+ if match goes in forward direction"
* "- if match goes in forward direction"

     -D        -B       +C               -A                              +A           +B       +C               +D
--<<<<<<<<--<<<<<<<<-->>>>>>>>--<<<<<<<<<<<<<<<<<<<<--     vs.     --->>>>>>>>>>>>--->>>>>>--->>>>>>----------->>>>>>--------------
 5'                  genome1                       3'               5'                          genome2                         3'
```

**ALGORITHM**:

The following synteny graph algorithm relies on three non-trivial components:

 1. A spatial indexing algorithm bins points that are close together, such that it's fast to look up the set of dots that are within the proximity of some other dot. The spatial indexing algorithm used by this implementation is called a quad tree.
 2. A clustering algorithm connects dots going in the same direction to reveal synteny blocks. The clustering algorithm used by this implementation is iterative, doing multiple rounds of connecting within a set of constraints (e.g. the neighbouring dot has to be within some limit / in some angle for it to connect).
 3. A filtering algorithm that trims/merges overlapping synteny blocks as well as removes superfluous synteny blocks returned by the clustering algorithm. The filtering algorithm used by this implementation is simple off-the-cuff heuristics.

These components are complicated and not specific to bioinformatics. As such, this section doesn't discuss them in detail but the source code is available (entrypoint is displayed below)).

```{note}
This is code I came up with to solve the ch 6 final assignment in the Pevzner book. I came up with / fleshed out the ideas myself -- the book only hinted at specific bits. I believe the fundamentals are correct but the implementation is finicky and requires a lot of knob twisting to get decent results.
```

```{output}
ch6_code/src/synteny_graph/MatchMerger.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch6}
synteny_graph.MatchMerger
7
linear
A0, GGATGGTGTCCTCATCTAATGATGTCGGTAAAGAGTCTACCCCGAATGATTATCTGAGTCTCCCATGAACCAAGTCCGTGGTATAGTCCATACTCTGAACCAAAACAGATAAACCAGCAAGATACATTGCAGAAGCTTGCCACCTTAGCAGGTTGTCAGATATCCGTTTCTGGAACTCCCGGGAGGACGATCGGAAGTTGAGCACAGGTACAAACACTTCAGGAATGATCTACTAAACTTTAGGGTCCGTACCTTTTATAATCCTTGCTAGCATCATGTTGAAGGTTAGAGGATTCCGAAACCAGAAGTGGCGATCTCGCTAAAGCAGGTCACCACGGTCAGCGGGTGGCCATTTACTCGTGAAAACCATAGTCCGTGAAAGCTGGGCAACTTTAGTTGGGACCCTTAAGGCGACTGAGGGAAGCAACTATCGGAAGTATCGTACAGGTCGTAAAGTACCAGTACGGAAGAAGCAGGGAGTTATAATATTCACTACCACAATTACCCGAGTTCACTTGTTTCAATCGCCCTCCCTTGACAGAACGTGCGTTACGTAGGAGTGCTTGACATACGGCGGCCGTCTGAGCTAGGACTATCGGAGCGTAATAATGGGATTTCAAATTTACCAGTTCCAGGTTGTCCAAGGGCTTGGCGGTGAGTCGACATGGAAAGATAAATTCCTCAGGTGCTGGCGCTCCCGTGGGGCCGCAGACACTACCTATTGGAGGGTGCTTAAACTATACAGCGCGCTAATTGTTAACTACTCCTTTGTGTCATAAGGGAGGGGAAACACGCGAGGACCGCCTTTGATCTGGTTCAAACGCCTAGAAGTATCTCCATTCTGTCCATTACGCCACCGCCCCGTCGAATGGTACCGGTATCGCTTGACATCTGCTTCTATACTAGAACAACTAATGCCGGCTTCTGGAGTGAAGGCACCATCCCACCAGAGCATTGAAGATTCGCTCGTTGGATTGATAGGAGTGAATATTCTGTCATCTCCTAACTTTTTGGGCACAGCTAG
B0, CGGCATGGTGTCCTTCATGTGACCTGATGTCCGATAAGGGGGTTCTACGAAGGGCCCTCCACAGGTCCTTTGCCTAAGGATTGTTGGGTCGCATTCAACTGTTACGGAGACGTTACTAGGACGACCTAATAGAACACAACCAAGTTACGTACGCTATATCCTGTCCTGACCCAGTACCCTCTGGGTCTATATAAGTAAGCGGGTACGATTCGAGAGGGGAGCAACCAGTTACAAACACTTCAGGAATCGATCTTACTTAAACTTTTGGGTCCGATACTTTATAATCCTTGCTAGCCTACGATGTTGAGTTGAGGATTCGCGAACCAGAACAATTGCCGATACTCGCTATTAGAGGTCTCCAACGGTCACCGGGTGGGCCATTGACTCGTGAAACCAATAACCGGTGCCATTCGGACAGGGTGCTGTGGCTAGTGAAGTGAATGGCAGATTACGTCTACTGCGTTTGCAACCCAGATCCAAAGGCGTGGCTTCTACGCGTGTTTCCCATCCCTTATCACACAAGAGGGAGTAGTTAACAATTAGCGTGCTGAAGTAGTAAGCCACCCCAATGTTTAGTTCTGCGTGCCCACGGGAGCCAAGCCATCCTGAGGATTTTATGTGTCCATGTCGACAACTACACGGCAAGCACTTAGACAAGCCTGGCAACTGCGTAGAATTATGAAAGCCCACTTATTGCTCCGTATGGTCCGAGCTCAGACGGCCGCCGCTATGTCAAGCACCCCTACGGTTAACGCACGTGTTGTCCAAGGGAAGAGCGGATTGGAGACAAACGTGATCTGCGGGTTAATTGTGGTTAGTGACTATTATTAACCTCCCGTCTTCCTTCCGTCACGGGTAACCTTTACGACCTCATTACGATACTCTCCGATAGGTTGCCTTACCTTCAGTCGCCTAACGGGTCCCAATAAAGTTGCCCGCGTTCTAGGCGAATCATCGCTTGACATCTTGCTTCTTATATACAACCAACCAAATCCCGGCTTCTGGAGCTGAGGCACGCATCCCACCCAGAGGCATTGAAGATTACGCCTCGTTCGGATTGATAGTAGTGCGATATTCTGTATCTCCCTAACTATTTTCGGGCACACTACG
merge, 10, 45
merge, 15, 45
merge, 25, 45
merge, 35, 45
filter, 35, 35
merge, 100, 45
filter, 65, 65
cull, 15
```

### Reversal Path

`{bm} /(Algorithms\/Synteny\/Reversal Path)_TOPIC/`

```{prereq}
Algorithms/Synteny/Synteny Graph_TOPIC
```

**WHAT**: Given two genomes that share synteny blocks, where one genome has the synteny blocks in desired form while the other does not, determine the minimum number of genome rearrangement reversals (reversal distance) required to get the undesired genome's synteny blocks to match those in the desired genome.

```{svgbob}
* "Synteny blocks going in the forward direction (5' to 3') are prefixed with +."
* "Synteny blocks going in the backward direction (3' to 5') are prefixed with -."

   +A     +B      +C       +D       +E                         +B     +C       -A      +D       -E    
-->>>>>-->>>>>--->>>>>-->>>>>>>>>-->>>>>--        vs        -->>>>>-->>>>>---<<<<<-->>>>>>>>>--<<<<<--
                DESIRED                                                     UNDESIRED



                                         "Parsimonious reversal path"
                                                                  .-----.
                                   +B     +C      -A       +D       -E    
                                -->>>>>-->>>>>---<<<<<-->>>>>>>>>--<<<<<--
                                
                                 .--------------------.
                                   +B     +C      -A       +D       +E    
                                -->>>>>-->>>>>---<<<<<-->>>>>>>>>-->>>>>--
                                
                                        .-------------.
                                   +A     -C      -B       +D       +E    
                                -->>>>>--<<<<<---<<<<<-->>>>>>>>>-->>>>>--
                                

                                   +A     +B      +C       +D       +E    
                                -->>>>>-->>>>>--->>>>>-->>>>>>>>>-->>>>>--
```

**WHY**: The theory is that the genome rearrangements between two species take the parsimonious path (or close to it). Since genome reversals are the most common form of genome rearrangement mutation, by calculating a parsimonious reversal path (smallest set of reversals) it's possible to get an idea of how the two species branched off. In the example above, it may be that one of the genomes in the reversal path is the parent that both genomes are based off of.

```{svgbob}
* "Synteny blocks going in the forward direction (5' to 3') are prefixed with +."
* "Synteny blocks going in the backward direction (3' to 5') are prefixed with -."

                                   +A     -C      -B       +D       +E    
                                -->>>>>--<<<<<---<<<<<-->>>>>>>>>-->>>>>--
                                                 PARENT

                                                   |
                   .-------------------------------+-------------------------------.
                   |                                                               v
                   |
                   |                                         .--------------------.
                   |                                           +A     -C      -B       +D       +E    
                   v                                        -->>>>>--<<<<<---<<<<<-->>>>>>>>>-->>>>>--

        .-------------.                                                                       .-----.
   +A     -C      -B       +D       +E                         +B     +C      -A       +D       +E    
-->>>>>--<<<<<---<<<<<-->>>>>>>>>-->>>>>--                  -->>>>>-->>>>>---<<<<<-->>>>>>>>>-->>>>>--


   +A    "+B      +C       +D       +E                         +B     +C      -A       +D       -E    
-->>>>>-->>>>>--->>>>>-->>>>>>>>>-->>>>>--                  -->>>>>-->>>>>---<<<<<-->>>>>>>>>--<<<<<--
                DESIRED                                                     UNDESIRED
```

#### Breakpoint List Algorithm

`{bm} /(Algorithms\/Synteny\/Reversal Path\/Breakpoint List Algorithm)_TOPIC/`

**ALGORITHM**:

This algorithm is a simple best effort heuristic to estimate the parsimonious reversal path. It isn't guaranteed to generate a reversal path in every case: The point of this algorithm isn't so much to be a robust solution as much as it is to be a foundation / provide intuition for better algorithms that determine reversal paths.

The algorithm relies on the concept of breakpoint_GRs and adjacencies_GR...

 * Adjacency_GR: Two neighbouring synteny blocks in the undesired genome that follow each other just as they do in the desired genome. For example, ...

   * this undesired genome has B and C next to each other and the tail of B is followed by the head of C, just as in the desired genome.
  
     ```{svgbob}
                                .---------------------------------------------------.
                       .--------+--------.                                 .--------+-------.                          
            +A            +B        +C          +D                            +B       +C       +D          -A         
     -->>>>>>>>>>>>>>--->>>>>>>--->>>>>>>----->>>>>>>------      vs       -->>>>>>>--->>>>>>-->>>>>>>--<<<<<<<<<<<<<<--
      5'                      DESIRED                   3'                 5'       ^       UNDESIRED               3' 
                                                                                    |
                                                                                adjacency
     ```
  
   * this undesired genome has B and C next to each other and the tail of B is followed by the tail of C, just as in the desired genome.
  
     ```{svgbob}
                                .---------------------------------------------------.
                       .--------+--------.                                 .--------+-------.                          
            +A            +B        -C          +D                            +B       -C       +D          -A         
     -->>>>>>>>>>>>>>--->>>>>>>---<<<<<<<----->>>>>>>------      vs       -->>>>>>>--<<<<<<<-->>>>>>>--<<<<<<<<<<<<<<--
      5'                      DESIRED                   3'                 5'       ^       UNDESIRED               3' 
                                                                                    |
                                                                                adjacency
     ```

   * this undesired genome has B and C next to each other and the tail of B is followed by the head of C, just as in the desired genome. Note that their placement has been swapped when compared to the desired genome. As long as they follow each other as they do in the desired genome, it's considered an adjacency_GR.

     ```{svgbob}
                                .--------------------------------------------.
                       .--------+--------.                          .--------+-------.                          
            +A            +B        +C          +D                     -C       -B       +D          -A         
     -->>>>>>>>>>>>>>--->>>>>>>--->>>>>>>----->>>>>>>------   vs   --<<<<<<<--<<<<<<<-->>>>>>>--<<<<<<<<<<<<<<--
      5'                      DESIRED                   3'          5'       ^       UNDESIRED               3' 
                                                                             |
                                                                         adjacency
     ```

 * Breakpoint_GR: Two neighbouring synteny blocks in the undesired genome don't fit the definition of an adjacency_GR. For example, ...

   * this undesired genome has B and C next to each other but the tail of B is NOT followed by the head of C, as it is in the desired genome.
  
     ```{svgbob}
                                .--------------------------------------------.
                       .--------+--------.                          .--------+-------.                          
            +A            +B        +C          +D                     +B       -C       +D          -A         
     -->>>>>>>>>>>>>>--->>>>>>>--->>>>>>>----->>>>>>>------   vs   -->>>>>>>---<<<<<<-->>>>>>>--<<<<<<<<<<<<<<--
      5'                      DESIRED                   3'          5'       ^       UNDESIRED               3' 
                                                                             |
                                                                         breakpoint
     ```
  
   * this undesired genome does NOT have B and C next to each other.
  
     ```{svgbob}
                                .---------------------------------------+---------------------------------.
                       .--------+--------.                          .---+---.                         .---+---.
            +A            +B        +C          +D                     +B        -D         -A           +C     
     -->>>>>>>>>>>>>>--->>>>>>>--->>>>>>>----->>>>>>>------   vs   -->>>>>>>---<<<<<<--<<<<<<<<<<<<<<-->>>>>>>--
      5'                      DESIRED                   3'          5'       ^       UNDESIRED        ^      3' 
                                                                             |                        |
                                                                         breakpoint               breakpoint
     ```

Breakpoint_GRs and adjacencies_GR are useful because they identify desirable points for reversals. This algorithm takes advantage of that fact to estimate the reversal distance. For example, a contiguous train of adjacencies_GR in an undesired genome may identify the boundaries for a single reversal that gets the undesired genome closer to the desired genome.

```{svgbob}
* "The contiguous segment comprising D, C, and B may be reversed as"
  "a single genome reversal."

                                                                      breakpoint  adjacency   adjacency   breakpoint    
                                                                          |           |           |           |         
    +A          +B         +C          +D        +E                 +A    v     -D    v    -C     v    -B     v   -E     
-->>>>>>>----->>>>>>>---->>>>>>>----->>>>>>----->>>>>>--   vs   -->>>>>>>-----<<<<<<<----<<<<<<<-----<<<<<<-----<<<<<<--
 5'                      DESIRED                     3'          5'                     UNDESIRED                    3' 
```

The algorithm starts by assigning integers to synteny blocks. The synteny blocks in the...

 * desired genome are represented as +1 to +n.
 * undesired genome are represented by the integers of the corresponding synteny block in the desired genome, where the integer is negated if the synteny block is reversed.

For example, ...

```{svgbob}
     +A      +B       +C       +D      -E                +A        -D      -C       -B     +E   
-->>>>>>>-->>>>>>>-->>>>>>>-->>>>>>--<<<<<<--   vs   -->>>>>>>--<<<<<<<--<<<<<<<--<<<<<<-->>>>>>--
 5'                 DESIRED               3'          5'                UNDESIRED              3' 

                                  
                                          "CONVERTS TO..."


     +1      +2       +3       +4      +5                +1        -4      -3       -2     -5   
-->>>>>>>-->>>>>>>-->>>>>>>-->>>>>>--<<<<<<--   vs   -->>>>>>>--<<<<<<<--<<<<<<<--<<<<<<-->>>>>>--
 5'                 DESIRED               3'          5'                UNDESIRED              3' 


* "+A maps to +1, -A maps to -1"
* "+B maps to +2, -B maps to -2"
* "+C maps to +3, -C maps to -3"
* "+D maps to +4, -D maps to -4"
* "-E maps to +5, +E maps to -5"
```

The synteny blocks in each genomes of the above example may be represented as lists...

 * `[+1, +2, +3, +4, +5]` (DESIRED)
 * `[+1, -4, -3, -2, -5]` (UNDESIRED)

Artificially add a 0 prefix and a length + 1 suffix to both lists. In the above example, the length is 5, so each list gets a prefix of 0 and a suffix of 6...

 * `[0, +1, +2, +3, +4, +5, +6]` (DESIRED)
 * `[0, +1, -4, -3, -2, -5, +6]` (UNDESIRED)

In this modified list, consecutive elements `{kt}(p_i, p_{i+1})` are considered a...

 * adjacency_GR if `{kt}p_i + 1 = p_{i+1}`.
 * breakpoint_GR if `{kt}p_i + 1 \neq p_{i+1}`.

In the undesired version of the example above, the breakpoint_GRs and adjacencies_GR are...

```{svgbob}
    bp       bp bp
    |        |  |
    v        v  v
0 +1 -4 -3 -2 -5 +6
 ^     ^  ^
 |     |  |
 a     a  a     
    
* "a = adjacency"
* "b = breakpoint"
```

This algorithm continually applies genome rearrangement reversal operations on portions of the list in the hopes of reducing the number of breakpoint_GRs at each reversal, ultimately hoping to get it to the desired list. It targets portions of contiguous adjacencies_GR sandwiched between breakpoint_GRs. In the example above, the reversal of `[-4, -3, -2]` reduces the number of breakpoint_GRs by 1...

```{svgbob}
* "Genome reversal of -4 -3 -2 is +2 +3 +4"

             bp bp
             |  |
             v  v
0 +1 +2 +3 +4 -5 +6
 ^  ^  ^  ^
 |  |  |  |
 a  a  a  a
    
* "a = adjacency"
* "b = breakpoint"
```

Following that up with a reversal of `[-5]` reduces the number of breakpoint_GRs by 2...

```{svgbob}
* "Genome reversal of -5 is +5"

0 +1 +2 +3 +4 +5 +6
 ^  ^  ^  ^  ^  ^
 |  |  |  |  |  |
 a  a  a  a  a  a

* "a = adjacency"
* "b = breakpoint"
```

Leaving the undesired list in the same state as the desired list. As such, the reversal distance for this example is 2 reversals.

In the best case, a single reversal will remove 2 breakpoint_GRs (one on each side of the reversal). In the worst case, there is no single reversal that drives down the number of breakpoint_GRs. For example, there is no single reversal for the list `[+2, +1]` that reduces the number of breakpoint_GRs...

```{svgbob}
 bp bp bp                         bp bp bp
 |  |  |                          |  |  | 
 v  v  v                          v  v  v 
0 +2 +1 +3                       0 -1 -2 +3
 '--+--'           reverse        '--+--'
    '--------------------------------'
            
 bp bp bp                         bp bp bp
 |  |  |                          |  |  | 
 v  v  v                          v  v  v 
0 +2 +1 +3                       0 -2 +1 +3
 '-+'              reverse        '-+'
   '--------------------------------'

 bp bp bp                         bp bp bp
 |  |  |                          |  |  | 
 v  v  v                          v  v  v 
0 +2 +1 +3                       0 +2 -1 +3
    '-+'           reverse           '-+'
      '--------------------------------'

* "a = adjacency"
* "b = breakpoint"
```

In such worst case scenarios, the algorithm fails. However, the point of this algorithm isn't so much to be a robust solution as much as it is to be a foundation for better algorithms that determine reversal paths.

```{output}
ch6_code/src/breakpoint_list/BreakpointList.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch6}
breakpoint_list.BreakpointList
+1, -4, -3, -2, -5
```

Since each reversal can at most reduce the number of breakpoint_GRs by 2, the reversal distance must be at least half the number of breakpoint_GRs (lower bound): `{kt} d_{rev}(p) >= \frac{bp(p)}{2}`. In other words, the minimum number of reversals to transform a permutation_GRs to an identity permutation_GR will never be less than `{kt} \frac{bp(p)}{2}`.

#### Breakpoint Graph Algorithm

`{bm} /(Algorithms\/Synteny\/Reversal Path\/Breakpoint Graph Algorithm)_TOPIC/`

```{prereq}
Algorithms/Synteny/Reversal Path/Breakpoint List Algorithm_TOPIC
```

**ALGORITHM**:

This algorithm calculates a parsimonious reversal path by constructing an undirected graph representing the synteny blocks between genomes. Unlike the breakpoint_GR list algorithm, this algorithm...

 * determines a full parsimonious reversal path every time (there may be multiple such paths).
 * handles multiple chromosomes (genome rearrangement chromosomal fusions and fissions).
 * handles both linear and circular chromosomes.

This algorithm begins by constructing an undirected graphs containing both the desired and undesired genomes, referred to as a breakpoint graph_GR. It then performs a set of re-wiring operations on the breakpoint graph_GR to determine a parsimonious reversal path (including fusion and fission), where each re-wiring operation is referred to as a two-break.

__BREAKPOINT GRAPH_GR REPRESENTATION__

Construction of a breakpoint graph_GR is as follows:

 1. Set the ends of synteny blocks as nodes. The arrow end should have a _t_ suffix (for tail) while the non-arrow end should have a _h_ suffix (for head)...
 
    ```{dot}
    graph G {
    layout=neato
    node [shape=plain];
    _D_t_ [pos="0.0,2.0!"];
    _D_h_ [pos="1.4142135623730951,1.414213562373095!"];
    }
    ```

    If the genome has linear chromosomes, add a termination node as well to represent chromosome ends. Only one termination node is needed -- all chromosome ends are represented by the same termination node.

    ```{dot}
    graph G {
    layout=neato
    node [shape=plain];
    TERM [pos="0.0,0.0!"];
    }
    ```

 1. Set the synteny blocks themselves as _undirected_ edges, represented by dashed edges.
    
    ```{dot}
    graph G {
    layout=neato
    node [shape=plain];
    _D_t_ [pos="0.0,2.0!"];
    _D_h_ [pos="1.4142135623730951,1.414213562373095!"];
    _D_t_ -- _D_h_ [style=dashed, dir=back];
    }
    ```
 
    Note that the arrow heads on these dashed edges represent the direction of the synteny match (e.g. head-to-tail for a normal match vs tail-to-head for a reverse complement match), not edge directions in the graph (graph is undirected). Since the _h_ and _t_ suffixes on nodes already convey the match direction information, the arrows may be omitted to reduce confusion.

    ```{dot}
    graph G {
    layout=neato
    node [shape=plain];
    _D_t_ [pos="0.0,2.0!"];
    _D_h_ [pos="1.4142135623730951,1.414213562373095!"];
    _D_t_ -- _D_h_ [style=dashed];
    }
    ```
 
 1. Set the regions between synteny blocks as _undirected_ edges, represented by colored edges. Regions of ...
    
    * desired genome that border a pair of synteny blocks are represented as blue edges.
    * undesired genome that border a pair of synteny blocks are represented as red edges.
 
    ```{dot}
    graph G {
    layout=neato
    node [shape=plain];
    _C_h_ [pos="1.4142135623730947,-1.4142135623730954!"];
    _B_t_ [pos="0.0,-2.0!"];
    _B_h_ [pos="-1.4142135623730954,-1.414213562373095!"];
    _B_t_ -- _C_h_ [color=blue];
    _B_h_ -- _C_h_ [color=red];
    }
    ```

    For linear chromosomes, the region between a chromosome end and the synteny node just before it is also represented by the appropriate colored edge.

    ```{dot}
    graph G {
    layout=neato
    node [shape=plain];
    _A_t_ [label="_A_t_", pos="3.0,0.0!"];
    _A_h_ [label="_A_h_", pos="3.585786438,1.4142135623730951!"];
    _D_t_ [label="_D_t_", pos="5,2.0!"];
    _D_h_ [label="_D_h_", pos="6.4142135623730951,1.414213562373095!"];
    TERM [pos="4.9,0.5!"];
    _A_t_ -- TERM [color=red];
    _A_h_ -- TERM [color=blue];
    _D_t_ -- TERM [color=blue];
    _D_h_ -- TERM [color=red];
    }
    ```

For example, the following two genomes share the synteny blocks A, B, C, and D between them ...

```{svgbob}
       +A              +B        +C                  +D                               -D       -B       +C          -A         
-->>>>>>>>>>>>>>----->>>>>>>--->>>>>>>------------->>>>>>>---------      vs       --<<<<<<<--<<<<<<<-->>>>>>>--<<<<<<<<<<<<<<--
 5'                          desired                            3'                 5'                  undesired            3' 
```

Converting the above genomes to both a circular and linear breakpoint graph_GR is as follows...

```{dot}
graph G {
layout=neato
labelloc="t";
label="CIRCULAR vs LINEAR";
node [shape=plain];

_C1_t_ [pos="2.0,0.0!"];
_C1_h_ [pos="1.4142135623730947,-1.4142135623730954!"];
_B1_t_ [pos="0.0,-2.0!"];
_B1_h_ [pos="-1.4142135623730954,-1.414213562373095!"];
_A1_t_ [pos="-2.0,0.0!"];
_A1_h_ [pos="-1.414213562373095,1.4142135623730951!"];
_D1_t_ [pos="0.0,2.0!"];
_D1_h_ [pos="1.4142135623730951,1.414213562373095!"];
_C1_t_ -- _C1_h_ [style=dashed];
_B1_t_ -- _B1_h_ [style=dashed];
_A1_t_ -- _A1_h_ [style=dashed];
_D1_t_ -- _D1_h_ [style=dashed];
_C1_t_ -- _D1_h_ [color=blue];
_A1_h_ -- _D1_t_ [color=blue];
_B1_t_ -- _C1_h_ [color=blue];
_A1_t_ -- _B1_h_ [color=blue];
_B1_h_ -- _C1_h_ [color=red];
_A1_t_ -- _C1_t_ [color=red];
_A1_h_ -- _D1_t_ [color=red];
_B1_t_ -- _D1_h_ [color=red];


_C2_t_ [label="_C_t_", pos="7.0,0.0!"];
_C2_h_ [label="_C_h_", pos="6.4142135623730947,-1.4142135623730954!"];
_B2_t_ [label="_B_t_", pos="5,-2.0!"];
_B2_h_ [label="_B_h_", pos="3.585786438,-1.414213562373095!"];
_A2_t_ [label="_A_t_", pos="3.0,0.0!"];
_A2_h_ [label="_A_h_", pos="3.585786438,1.4142135623730951!"];
_D2_t_ [label="_D_t_", pos="5,2.0!"];
_D2_h_ [label="_D_h_", pos="6.4142135623730951,1.414213562373095!"];
TERM [pos="4.9,0.5!"];
_C2_t_ -- _C2_h_ [style=dashed];
_B2_t_ -- _B2_h_ [style=dashed];
_A2_t_ -- _A2_h_ [style=dashed];
_D2_t_ -- _D2_h_ [style=dashed];
_C2_t_ -- _D2_h_ [color=blue];
_B2_t_ -- _C2_h_ [color=blue];
_A2_t_ -- _B2_h_ [color=blue];
_A2_h_ -- TERM [color=blue];
_D2_t_ -- TERM [color=blue];
_B2_h_ -- _C2_h_ [color=red];
_A2_t_ -- _C2_t_ [color=red];
_B2_t_ -- _D2_h_ [color=red];
_A2_h_ -- TERM [color=red];
_D2_t_ -- TERM [color=red];
}
```

As shown in the example above, the convention for drawing a breakpoint graph_GR is to position nodes and edges as they appear in the desired genome (synteny edges should be neatly sandwiched between blue edges). Note how both breakpoint graph_GRs in the example above are just another representation of their linear diagram counterparts. The ...

 * dashed edges represent the synteny blocks (suffix of _t_ denotes arrow end / _h_ denotes opposite end).
 * blue edges represent the gaps between synteny block and chromosome end nodes in the desired genome.
 * red edges represent the gaps between synteny block and chromosome end nodes in the undesired genome.

The reason for this convention is that it helps conceptualize the algorithms that operate on breakpoint graph_GRs (described further down). Ultimately, a breakpoint graph_GR is simply a merged version of the linear diagrams for both the desired and undesired genomes.

For example, if the circular genome version of the breakpoint graph_GR example above were flattened based on the blue edges (desired genome), the synteny blocks would be ordered as they are in the linear diagram for the desired genome...

```{svgbob}
       +A              +B        +C                  +D            
-->>>>>>>>>>>>>>----->>>>>>>--->>>>>>>------------->>>>>>>---------
 5'                          desired                            3' 
```

```{dot}
graph G {
layout=neato
labelloc="t";
label="CIRCULAR flattened on desired genome (blue edges)";
node [shape=plain];

_C1_t_ [pos="6,0!"];
_C1_h_ [pos="5,0!"];
_B1_t_ [pos="4,0!"];
_B1_h_ [pos="3,0!"];
_A1_t_ [pos="2,0!"];
_A1_h_ [pos="0,0!"];
_D1_t_ [pos="9,0!"];
_D1_h_ [pos="8,0!"];
_C1_t_:w -- _C1_h_:e [style=dashed];
_B1_t_:w -- _B1_h_:e [style=dashed];
_A1_t_:w -- _A1_h_:e [style=dashed];
_D1_t_:w -- _D1_h_:e [style=dashed];

_C1_t_:e -- _D1_h_:w [color=blue];
_A1_h_:n -- _D1_t_:n [color=blue];
_B1_t_:e -- _C1_h_:w [color=blue];
_A1_t_:e -- _B1_h_:w [color=blue];

splines="curved";
_B1_h_:n -- _C1_h_:n [color=red];
_A1_t_:s -- _C1_t_:s [color=red];
_A1_h_:s -- _D1_t_:s [color=red];
_B1_t_:s -- _D1_h_:s [color=red];
}
```

Likewise, if the circular genome version of the breakpoint graph_GR example above were flattened based on red edges (undesired genome), the synteny blocks would be ordered as they are in the linear diagram for the undesired genome...

```{svgbob}
    -D       -B       +C          -A         
--<<<<<<<--<<<<<<<-->>>>>>>--<<<<<<<<<<<<<<--
 5'                  undesired            3' 
```

```{dot}
graph G {
layout=neato
labelloc="t";
label="CIRCULAR flattened on undesired genome (red edges)";
node [shape=plain];

_C1_t_ [pos="5,0!"];
_C1_h_ [pos="4,0!"];
_B1_t_ [pos="2,0!"];
_B1_h_ [pos="3,0!"];
_A1_t_ [pos="7,0!"];
_A1_h_ [pos="9,0!"];
_D1_t_ [pos="0,0!"];
_D1_h_ [pos="1,0!"];
_C1_h_:e -- _C1_t_:w [style=dashed];
_B1_t_:e -- _B1_h_:w [style=dashed];
_A1_t_:e -- _A1_h_:w [style=dashed];
_D1_t_:e -- _D1_h_:w [style=dashed];

_B1_h_:e -- _C1_h_:w [color=red];
_A1_t_:w -- _C1_t_:e [color=red];
_A1_h_:s -- _D1_t_:s [color=red];
_B1_t_:w -- _D1_h_:e [color=red];

splines="curved";
_C1_t_:s -- _D1_h_:s [color=blue];
_A1_h_:n -- _D1_t_:n [color=blue];
_B1_t_:n -- _C1_h_:n [color=blue];
_A1_t_:n -- _B1_h_:n [color=blue];
}
```

```{note}
If you're confused at this point, don't continue. Go back and make sure you understand because in the next section builds on the above content.
```

__DATA STRUCTURE REPRESENTATION__

The data structure used to represent a breakpoint graph_GR can simply be two adjacency lists: one for the red edges and one for the blue edges.

```{output}
ch6_code/src/breakpoint_graph/ColoredEdgeSet.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

The edges representing synteny blocks technically don't need to be tracked because they're easily derived from either set of colored edges (red or blue). For example, given the following circular breakpoint graph_GR ...

```{dot}
graph G {
layout=neato
node [shape=plain];
_C_t_ [pos="2.0,0.0!"];
_C_h_ [pos="1.4142135623730947,-1.4142135623730954!"];
_B_t_ [pos="0.0,-2.0!"];
_B_h_ [pos="-1.4142135623730954,-1.414213562373095!"];
_A_t_ [pos="-2.0,0.0!"];
_A_h_ [pos="-1.414213562373095,1.4142135623730951!"];
_D_t_ [pos="0.0,2.0!"];
_D_h_ [pos="1.4142135623730951,1.414213562373095!"];
_C_t_ -- _C_h_ [style=dashed];
_B_t_ -- _B_h_ [style=dashed];
_A_t_ -- _A_h_ [style=dashed];
_D_t_ -- _D_h_ [style=dashed];
_C_t_ -- _D_h_ [color=blue];
_A_h_ -- _D_t_ [color=blue];
_B_t_ -- _C_h_ [color=blue];
_A_t_ -- _B_h_ [color=blue];
_B_h_ -- _C_h_ [color=red];
_A_t_ -- _C_t_ [color=red];
_A_h_ -- _D_t_ [color=red];
_B_t_ -- _D_h_ [color=red];
}
```

..., walk the blue edges starting from the node B_t. The opposite end of the blue edge at B_t is C_h. The next edge to walk must be a synteny edge, but synteny edges aren't tracked in this data structure. However, since it's known that the nodes of a synteny edge...

 * must either end in _t_ or _h_
 * share the same name

, ... it's easy to derive that the opposite end of the synteny edge at node C_h is node C_t. As such, get the blue edge for C_t and repeat. Keep repeating until a cycle is detected.

For linear breakpoint graph_GRs, the process must start and end at the termination node (no cycle).

```{output}
ch6_code/src/breakpoint_graph/ColoredEdgeSet.py
python
# WALK_MARKDOWN\s*\n([\s\S]+)\n\s*# WALK_MARKDOWN
```

```{ch6}
breakpoint_graph.ColoredEdgeSet
[[C_h, D_t], [B_h, C_t], [A_h, B_t], [A_t, D_h], [X_h, Z_t], [X_t, Z_h]]
```

```{note}
If you're confused at this point, don't continue. Go back and make sure you understand because in the next section builds on the above content.
```

__PERMUTATION_GR REPRESENTATION__

A common textual representation of a breakpoint graph_GR is writing out each of the two genomes as a set of lists. Each list, referred to as a permutation_GR, describes one of the chromosomes in a genome.

To convert a chromosome within a breakpoint graph_GR to a permutation_GR, simply walk the edges for that chromosome...

 * desired genome: blue edges and synteny edges.
 * undesired genome: red edges and synteny edges.

Each synteny edge walked is appended to the list with a prefix of ...
   
 * _\+_ if it's walked from head to tail.
 * _\-_ if it's walked from tail to head.
 
For example, given the following breakpoint graph_GR ...

```{dot}
graph G {
layout=neato
node [shape=plain];
_C_t_ [label="_C_t_", pos="2.0,0.0!"];
_C_h_ [label="_C_h_", pos="1.4142135623730947,-1.4142135623730954!"];
_B_t_ [label="_B_t_", pos="0.0,-2.0!"];
_B_h_ [label="_B_h_", pos="-1.4142135623730954,-1.414213562373095!"];
_A_t_ [label="_A_t_", pos="-2.0,0.0!"];
_A_h_ [label="_A_h_", pos="-1.414213562373095,1.4142135623730951!"];
_D_t_ [label="_D_t_", pos="0.0,2.0!"];
_D_h_ [label="_D_h_", pos="1.4142135623730951,1.414213562373095!"];
_C_t_ -- _C_h_ [style=dashed];
_B_t_ -- _B_h_ [style=dashed];
_A_t_ -- _A_h_ [style=dashed];
_D_t_ -- _D_h_ [style=dashed];
_C_t_ -- _D_h_ [color=blue];
_A_h_ -- _D_t_ [color=blue];
_B_t_ -- _C_h_ [color=blue];
_A_t_ -- _B_h_ [color=blue];
_B_t_ -- _A_h_ [color=red];
_A_t_ -- _B_h_ [color=red];
_C_h_ -- _D_t_ [color=red];
_C_t_ -- _D_h_ [color=red];
}
```

, ... walking the edges for the undesired genome (red) from node D_t in the ...

 * clockwise direction results in the permutation_GR `[-D, -C]`.
 * counter-clockwise direction results in the permutation_GR `[+C, +D]`.

For circular chromosomes, the walk direction is irrelevant, meaning that both example permutation_GRs above represent the same chromosome. Likewise, the starting node is also irrelevant, meaning that the following permutation_GRs are all equivalent to the ones in the above example: `[+C, +D]`, and `[+D, +C]`.

For linear chromosomes, the walk direction is irrelevant but the walk must start from and end at the termination node (representing the ends of the chromosome). The termination nodes aren't included in the permutation_GR.

In the example breakpoint graph_GR above, the permutation_GR set representing the undesired genome (red) may be written as either...

 * `{[+C, +D], [+A, +B]}`
 * `{[+A, +B], [-C, _D]}`
 * `{[-A, -B], [-C, -D]}`
 * ...

Likewise, the permutation_GR set representing the desired genome (blue) in the example above may be written as either...

 * `{[+A, +B, +C, +D]}`
 * `{[-D, -C, -B, -A]}`
 * `{[+B, +C, +D, +A]}`
 * ...

```{output}
ch6_code/src/breakpoint_graph/Permutation.py
python
# MARKDOWN_FROM\s*\n([\s\S]+)\n\s*# MARKDOWN_FROM
```

Converting from a permutation_GR set back to a breakpoint graph_GR is basically just reversing the above process. For each permutation_GR, slide a window of size two to determine the colored edges that permutation_GR is for. The node chosen for the window element at index ...

 0. should be tail if sign is _\-_ or head if sign is _\+_.
 1. should be head if sign is _\-_ or tail if sign is _\+_.

For circular chromosomes, the sliding window is cyclic. For example, sliding the window over permutation_GR `[+A, +C, -B, +D]` results in ...

 * `[+A, +C]` which produces the colored edge `(A_h, C_t)`.
 * `[+C, -B]` which produces the colored edge `(C_h, B_h)`.
 * `[-B, +D]` which produces the colored edge `(B_t, D_t)`.
 * `[+D, +A]` which produces the colored edge `(D_h, A_t)`.

For linear chromosomes, the sliding window is not cyclic and the chromosomes always start and end at the termination node. For example, the permutation_GR `[+A, +C, -B, +D]` would actually be treated as `[TERM, +A, +C, -B, +D, TERM]`, resulting in ...

 * `[TERM, +A]` which produces the colored edge `(TERM, A_h)`.
 * `[+A, +C]` which produces the colored edge `(A_h, C_t)`.
 * `[+C, -B]` which produces the colored edge `(C_h, B_h)`.
 * `[-B, +D]` which produces the colored edge `(B_t, D_t)`.
 * `[+D, TERM]` which produces the colored edge `(D_h, TERM)`.

```{output}
ch6_code/src/breakpoint_graph/Permutation.py
python
# MARKDOWN_TO\s*\n([\s\S]+)\n\s*# MARKDOWN_TO
```

```{note}
If you're confused at this point, don't continue. Go back and make sure you understand because in the next section builds on the above content.
```

__TWO-BREAK ALGORITHM__

Now that breakpoint graph_GRs have been adequately described, the goal of this algorithm is to iteratively re-wire the red edges of a breakpoint graph_GR such that they match its blue edges. At each step, the algorithm finds a pair of red edges that share nodes with a blue edge and re-wires those red edges such that one of them matches the blue edge.

For example, the two red edges highlighted below share the same nodes as a blue edge (D_h and C_t). These two red edges can be broken and re-wired such that one of them matches the blue edge...

```{dot}
graph G {
layout=neato
labelloc="t";
label="BEFORE to AFTER...";
node [shape=plain];

_C1_t_ [label="_C_t_", pos="2.0,0.0!"];
_C1_h_ [label="_C_h_", pos="1.4142135623730947,-1.4142135623730954!"];
_B1_t_ [label="_B_t_", pos="0.0,-2.0!"];
_B1_h_ [label="_B_h_", pos="-1.4142135623730954,-1.414213562373095!"];
_A1_t_ [label="_A_t_", pos="-2.0,0.0!"];
_A1_h_ [label="_A_h_", pos="-1.414213562373095,1.4142135623730951!"];
_D1_t_ [label="_D_t_", pos="0.0,2.0!"];
_D1_h_ [label="_D_h_", pos="1.4142135623730951,1.414213562373095!"];
_C1_t_ -- _C1_h_ [style=dashed];
_B1_t_ -- _B1_h_ [style=dashed];
_A1_t_ -- _A1_h_ [style=dashed];
_D1_t_ -- _D1_h_ [style=dashed];
_C1_t_ -- _D1_h_ [color=blue];
_A1_h_ -- _D1_t_ [color=blue];
_B1_t_ -- _C1_h_ [color=blue];
_A1_t_ -- _B1_h_ [color=blue];
_B1_h_ -- _C1_h_ [color=red];
_A1_t_ -- _C1_t_ [color=red, penwidth="4"];
_A1_h_ -- _D1_t_ [color=red];
_B1_t_ -- _D1_h_ [color=red, penwidth="4"];

_C2_t_ [label="_C_t_", pos="7.0,0.0!"];
_C2_h_ [label="_C_h_", pos="6.4142135623730947,-1.4142135623730954!"];
_B2_t_ [label="_B_t_", pos="5,-2.0!"];
_B2_h_ [label="_B_h_", pos="3.585786438,-1.414213562373095!"];
_A2_t_ [label="_A_t_", pos="3.0,0.0!"];
_A2_h_ [label="_A_h_", pos="3.585786438,1.4142135623730951!"];
_D2_t_ [label="_D_t_", pos="5,2.0!"];
_D2_h_ [label="_D_h_", pos="6.4142135623730951,1.414213562373095!"];
_C2_t_ -- _C2_h_ [style=dashed];
_B2_t_ -- _B2_h_ [style=dashed];
_A2_t_ -- _A2_h_ [style=dashed];
_D2_t_ -- _D2_h_ [style=dashed];
_C2_t_ -- _D2_h_ [color=blue];
_A2_h_ -- _D2_t_ [color=blue];
_B2_t_ -- _C2_h_ [color=blue];
_A2_t_ -- _B2_h_ [color=blue];
_B2_h_ -- _C2_h_ [color=red];
_A2_t_ -- _B2_t_ [color=red, penwidth="4"];
_A2_h_ -- _D2_t_ [color=red];
_C2_t_ -- _D2_h_ [color=red, penwidth="4"];
}
```

Each re-wiring operation is called a 2-break and represents either a chromosome fusion, chromosome fission, or reversal mutation (genome rearrangement). For example, ...

 * fusion:

   ```{svgbob}
           +A       +B                             +C          +D        
   ------>>>>>>>-->>>>>>>--------            ---->>>>>>>-->>>>>>>>>>>>>----
    5'  circular chromosome1  3'              5'  circular chromosome2  3' 


                          "FUSE AT [+B, +C] BOUNDARY..."

                +A       +B                 +C          +D        
        ------>>>>>>>-->>>>>>>------------>>>>>>>-->>>>>>>>>>>>>-----
         5'                 circular chromosome                   3' 
   ```

   ```{dot}
   graph G {
   layout=neato
   labelloc="t";
   label="BEFORE to AFTER...";
   node [shape=plain];

   _C1_t_ [label="_C_t_", pos="2.0,0.0!"];
   _C1_h_ [label="_C_h_", pos="1.4142135623730947,-1.4142135623730954!"];
   _B1_t_ [label="_B_t_", pos="0.0,-2.0!"];
   _B1_h_ [label="_B_h_", pos="-1.4142135623730954,-1.414213562373095!"];
   _A1_t_ [label="_A_t_", pos="-2.0,0.0!"];
   _A1_h_ [label="_A_h_", pos="-1.414213562373095,1.4142135623730951!"];
   _D1_t_ [label="_D_t_", pos="0.0,2.0!"];
   _D1_h_ [label="_D_h_", pos="1.4142135623730951,1.414213562373095!"];
   _C1_t_ -- _C1_h_ [style=dashed];
   _B1_t_ -- _B1_h_ [style=dashed];
   _A1_t_ -- _A1_h_ [style=dashed];
   _D1_t_ -- _D1_h_ [style=dashed];
   _C1_t_ -- _D1_h_ [color=blue];
   _A1_h_ -- _D1_t_ [color=blue];
   _B1_t_ -- _C1_h_ [color=blue];
   _A1_t_ -- _B1_h_ [color=blue];
   _B1_t_ -- _A1_h_ [color=red, penwidth="4"];
   _A1_t_ -- _B1_h_ [color=red];
   _C1_h_ -- _D1_t_ [color=red, penwidth="4"];
   _C1_t_ -- _D1_h_ [color=red];

   _C2_t_ [label="_C_t_", pos="7.0,0.0!"];
   _C2_h_ [label="_C_h_", pos="6.4142135623730947,-1.4142135623730954!"];
   _B2_t_ [label="_B_t_", pos="5,-2.0!"];
   _B2_h_ [label="_B_h_", pos="3.585786438,-1.414213562373095!"];
   _A2_t_ [label="_A_t_", pos="3.0,0.0!"];
   _A2_h_ [label="_A_h_", pos="3.585786438,1.4142135623730951!"];
   _D2_t_ [label="_D_t_", pos="5,2.0!"];
   _D2_h_ [label="_D_h_", pos="6.4142135623730951,1.414213562373095!"];
   _C2_t_ -- _C2_h_ [style=dashed];
   _B2_t_ -- _B2_h_ [style=dashed];
   _A2_t_ -- _A2_h_ [style=dashed];
   _D2_t_ -- _D2_h_ [style=dashed];
   _C2_t_ -- _D2_h_ [color=blue];
   _A2_h_ -- _D2_t_ [color=blue];
   _B2_t_ -- _C2_h_ [color=blue];
   _A2_t_ -- _B2_h_ [color=blue];
   _D2_t_ -- _A2_h_ [color=red, penwidth="4"];
   _A2_t_ -- _B2_h_ [color=red];
   _C2_h_ -- _B2_t_ [color=red, penwidth="4"];
   _C2_t_ -- _D2_h_ [color=red];
   }
   ```

 * fission:

   ```{svgbob}
                +A       +B                 +C          +D        
        ------>>>>>>>-->>>>>>>------------>>>>>>>-->>>>>>>>>>>>>-----
         5'                 circular chromosome                   3' 


                       "BREAK AT [+B, +C] BOUNDARY..."

           +A       +B                             +C          +D        
   ------>>>>>>>-->>>>>>>--------            ---->>>>>>>-->>>>>>>>>>>>>----
    5'  circular chromosome1  3'              5'  circular chromosome2  3' 
   ```

   ```{dot}
   graph G {
   layout=neato
   labelloc="t";
   label="BEFORE to AFTER...";
   node [shape=plain];

   _C1_t_ [label="_C_t_", pos="2.0,0.0!"];
   _C1_h_ [label="_C_h_", pos="1.4142135623730947,-1.4142135623730954!"];
   _B1_t_ [label="_B_t_", pos="0.0,-2.0!"];
   _B1_h_ [label="_B_h_", pos="-1.4142135623730954,-1.414213562373095!"];
   _A1_t_ [label="_A_t_", pos="-2.0,0.0!"];
   _A1_h_ [label="_A_h_", pos="-1.414213562373095,1.4142135623730951!"];
   _D1_t_ [label="_D_t_", pos="0.0,2.0!"];
   _D1_h_ [label="_D_h_", pos="1.4142135623730951,1.414213562373095!"];
   _C1_t_ -- _C1_h_ [style=dashed];
   _B1_t_ -- _B1_h_ [style=dashed];
   _A1_t_ -- _A1_h_ [style=dashed];
   _D1_t_ -- _D1_h_ [style=dashed];
   _C1_t_ -- _D1_h_ [color=blue];
   _A1_h_ -- _B1_t_ [color=blue];
   _D1_t_ -- _C1_h_ [color=blue];
   _A1_t_ -- _B1_h_ [color=blue];
   _D1_t_ -- _A1_h_ [color=red, penwidth="4"];
   _A1_t_ -- _B1_h_ [color=red];
   _C1_h_ -- _B1_t_ [color=red, penwidth="4"];
   _C1_t_ -- _D1_h_ [color=red];

   _C2_t_ [label="_C_t_", pos="7.0,0.0!"];
   _C2_h_ [label="_C_h_", pos="6.4142135623730947,-1.4142135623730954!"];
   _B2_t_ [label="_B_t_", pos="5,-2.0!"];
   _B2_h_ [label="_B_h_", pos="3.585786438,-1.414213562373095!"];
   _A2_t_ [label="_A_t_", pos="3.0,0.0!"];
   _A2_h_ [label="_A_h_", pos="3.585786438,1.4142135623730951!"];
   _D2_t_ [label="_D_t_", pos="5,2.0!"];
   _D2_h_ [label="_D_h_", pos="6.4142135623730951,1.414213562373095!"];
   _C2_t_ -- _C2_h_ [style=dashed];
   _B2_t_ -- _B2_h_ [style=dashed];
   _A2_t_ -- _A2_h_ [style=dashed];
   _D2_t_ -- _D2_h_ [style=dashed];
   _C2_t_ -- _D2_h_ [color=blue];
   _A2_h_ -- _B2_t_ [color=blue];
   _D2_t_ -- _C2_h_ [color=blue];
   _A2_t_ -- _B2_h_ [color=blue];
   _B2_t_ -- _A2_h_ [color=red, penwidth="4"];
   _A2_t_ -- _B2_h_ [color=red];
   _C2_h_ -- _D2_t_ [color=red, penwidth="4"];
   _C2_t_ -- _D2_h_ [color=red];
   }
   ```

 * reversal:

   ```{svgbob}
       -B       -A          +C          +D        
   --<<<<<<<--<<<<<<<----->>>>>>>-->>>>>>>>>>>>>-----
    5'              circular chromosome           3' 
   
      
                   "REVERSE [-B, -A] ..."
      
       +A       +B          +C          +D        
   -->>>>>>>-->>>>>>>----->>>>>>>-->>>>>>>>>>>>>-----
    5'              circular chromosome           3' 
   ```

   ```{dot}
   graph G {
   layout=neato
   labelloc="t";
   label="BEFORE to AFTER...";
   node [shape=plain];

   _C1_t_ [label="_C_t_", pos="2.0,0.0!"];
   _C1_h_ [label="_C_h_", pos="1.4142135623730947,-1.4142135623730954!"];
   _B1_t_ [label="_B_t_", pos="0.0,-2.0!"];
   _B1_h_ [label="_B_h_", pos="-1.4142135623730954,-1.414213562373095!"];
   _A1_t_ [label="_A_t_", pos="-2.0,0.0!"];
   _A1_h_ [label="_A_h_", pos="-1.414213562373095,1.4142135623730951!"];
   _D1_t_ [label="_D_t_", pos="0.0,2.0!"];
   _D1_h_ [label="_D_h_", pos="1.4142135623730951,1.414213562373095!"];
   _C1_t_ -- _C1_h_ [style=dashed];
   _B1_t_ -- _B1_h_ [style=dashed];
   _A1_t_ -- _A1_h_ [style=dashed];
   _D1_t_ -- _D1_h_ [style=dashed];
   _C1_t_ -- _D1_h_ [color=blue];
   _A1_h_ -- _D1_t_ [color=blue];
   _B1_t_ -- _C1_h_ [color=blue];
   _A1_t_ -- _B1_h_ [color=blue];
   _A1_h_ -- _C1_h_ [color=red, penwidth="4"];
   _A1_t_ -- _B1_h_ [color=red];
   _D1_t_ -- _B1_t_ [color=red, penwidth="4"];
   _C1_t_ -- _D1_h_ [color=red];

   _C2_t_ [label="_C_t_", pos="7.0,0.0!"];
   _C2_h_ [label="_C_h_", pos="6.4142135623730947,-1.4142135623730954!"];
   _B2_t_ [label="_B_t_", pos="5,-2.0!"];
   _B2_h_ [label="_B_h_", pos="3.585786438,-1.414213562373095!"];
   _A2_t_ [label="_A_t_", pos="3.0,0.0!"];
   _A2_h_ [label="_A_h_", pos="3.585786438,1.4142135623730951!"];
   _D2_t_ [label="_D_t_", pos="5,2.0!"];
   _D2_h_ [label="_D_h_", pos="6.4142135623730951,1.414213562373095!"];
   _C2_t_ -- _C2_h_ [style=dashed];
   _B2_t_ -- _B2_h_ [style=dashed];
   _A2_t_ -- _A2_h_ [style=dashed];
   _D2_t_ -- _D2_h_ [style=dashed];
   _C2_t_ -- _D2_h_ [color=blue];
   _A2_h_ -- _D2_t_ [color=blue];
   _B2_t_ -- _C2_h_ [color=blue];
   _A2_t_ -- _B2_h_ [color=blue];
   _D2_t_ -- _A2_h_ [color=red, penwidth="4"];
   _A2_t_ -- _B2_h_ [color=red];
   _C2_h_ -- _B2_t_ [color=red, penwidth="4"];
   _C2_t_ -- _D2_h_ [color=red];
   }
   ```

Genome rearrangement duplications and deletions aren't representable as 2-breaks. Genome rearrangement translocations can't be reliably represented as a single 2-break either. For example, the following translocation gets modeled as two 2-breaks, one that breaks the undesired chromosome (fission) and another that glues it back together (fusion)...

```{svgbob}
    +C       +B          +A          +D        
-->>>>>>>-->>>>>>>----->>>>>>>-->>>>>>>>>>>>>-----
 5'              circular chromosome           3' 

   
                  "SWAP C AND A..."

    +A       +B          +C          +D        
-->>>>>>>-->>>>>>>----->>>>>>>-->>>>>>>>>>>>>-----
 5'              circular chromosome           3' 
```

```{dot}
graph G {
layout=neato
labelloc="t";
label="Step 1: BEFORE to AFTER (fission)...";
node [shape=plain];

_C1_t_ [label="_C_t_", pos="2.0,0.0!"];
_C1_h_ [label="_C_h_", pos="1.4142135623730947,-1.4142135623730954!"];
_B1_t_ [label="_B_t_", pos="0.0,-2.0!"];
_B1_h_ [label="_B_h_", pos="-1.4142135623730954,-1.414213562373095!"];
_A1_t_ [label="_A_t_", pos="-2.0,0.0!"];
_A1_h_ [label="_A_h_", pos="-1.414213562373095,1.4142135623730951!"];
_D1_t_ [label="_D_t_", pos="0.0,2.0!"];
_D1_h_ [label="_D_h_", pos="1.4142135623730951,1.414213562373095!"];
_C1_t_ -- _C1_h_ [style=dashed];
_B1_t_ -- _B1_h_ [style=dashed];
_A1_t_ -- _A1_h_ [style=dashed];
_D1_t_ -- _D1_h_ [style=dashed];
_C1_t_ -- _D1_h_ [color=blue];
_A1_h_ -- _D1_t_ [color=blue];
_B1_t_ -- _C1_h_ [color=blue];
_A1_t_ -- _B1_h_ [color=blue];
_C1_t_ -- _B1_h_ [color=red, penwidth="4"];
_B1_t_ -- _A1_h_ [color=red];
_A1_t_ -- _D1_h_ [color=red, penwidth="4"];
_D1_t_ -- _C1_h_ [color=red];

_C2_t_ [label="_C_t_", pos="7.0,0.0!"];
_C2_h_ [label="_C_h_", pos="6.4142135623730947,-1.4142135623730954!"];
_B2_t_ [label="_B_t_", pos="5,-2.0!"];
_B2_h_ [label="_B_h_", pos="3.585786438,-1.414213562373095!"];
_A2_t_ [label="_A_t_", pos="3.0,0.0!"];
_A2_h_ [label="_A_h_", pos="3.585786438,1.4142135623730951!"];
_D2_t_ [label="_D_t_", pos="5,2.0!"];
_D2_h_ [label="_D_h_", pos="6.4142135623730951,1.414213562373095!"];
_C2_t_ -- _C2_h_ [style=dashed];
_B2_t_ -- _B2_h_ [style=dashed];
_A2_t_ -- _A2_h_ [style=dashed];
_D2_t_ -- _D2_h_ [style=dashed];
_C2_t_ -- _D2_h_ [color=blue];
_A2_h_ -- _D2_t_ [color=blue];
_B2_t_ -- _C2_h_ [color=blue];
_A2_t_ -- _B2_h_ [color=blue];
_C2_t_ -- _D2_h_ [color=red, penwidth="4"];
_B2_t_ -- _A2_h_ [color=red];
_A2_t_ -- _B2_h_ [color=red, penwidth="4"];
_D2_t_ -- _C2_h_ [color=red];
}
```

```{dot}
graph G {
layout=neato
labelloc="t";
label="Step 2: BEFORE to AFTER (fusion)...";
node [shape=plain];

_C1_t_ [label="_C_t_", pos="2.0,0.0!"];
_C1_h_ [label="_C_h_", pos="1.4142135623730947,-1.4142135623730954!"];
_B1_t_ [label="_B_t_", pos="0.0,-2.0!"];
_B1_h_ [label="_B_h_", pos="-1.4142135623730954,-1.414213562373095!"];
_A1_t_ [label="_A_t_", pos="-2.0,0.0!"];
_A1_h_ [label="_A_h_", pos="-1.414213562373095,1.4142135623730951!"];
_D1_t_ [label="_D_t_", pos="0.0,2.0!"];
_D1_h_ [label="_D_h_", pos="1.4142135623730951,1.414213562373095!"];
_C1_t_ -- _C1_h_ [style=dashed];
_B1_t_ -- _B1_h_ [style=dashed];
_A1_t_ -- _A1_h_ [style=dashed];
_D1_t_ -- _D1_h_ [style=dashed];
_C1_t_ -- _D1_h_ [color=blue];
_A1_h_ -- _D1_t_ [color=blue];
_B1_t_ -- _C1_h_ [color=blue];
_A1_t_ -- _B1_h_ [color=blue];
_C1_t_ -- _D1_h_ [color=red];
_B1_t_ -- _A1_h_ [color=red, penwidth="4"];
_A1_t_ -- _B1_h_ [color=red];
_D1_t_ -- _C1_h_ [color=red, penwidth="4"];

_C2_t_ [label="_C_t_", pos="7.0,0.0!"];
_C2_h_ [label="_C_h_", pos="6.4142135623730947,-1.4142135623730954!"];
_B2_t_ [label="_B_t_", pos="5,-2.0!"];
_B2_h_ [label="_B_h_", pos="3.585786438,-1.414213562373095!"];
_A2_t_ [label="_A_t_", pos="3.0,0.0!"];
_A2_h_ [label="_A_h_", pos="3.585786438,1.4142135623730951!"];
_D2_t_ [label="_D_t_", pos="5,2.0!"];
_D2_h_ [label="_D_h_", pos="6.4142135623730951,1.414213562373095!"];
_C2_t_ -- _C2_h_ [style=dashed];
_B2_t_ -- _B2_h_ [style=dashed];
_A2_t_ -- _A2_h_ [style=dashed];
_D2_t_ -- _D2_h_ [style=dashed];
_C2_t_ -- _D2_h_ [color=blue];
_A2_h_ -- _D2_t_ [color=blue];
_B2_t_ -- _C2_h_ [color=blue];
_A2_t_ -- _B2_h_ [color=blue];
_C2_t_ -- _D2_h_ [color=red];
_D2_t_ -- _A2_h_ [color=red, penwidth="4"];
_A2_t_ -- _B2_h_ [color=red];
_B2_t_ -- _C2_h_ [color=red, penwidth="4"];
}
```

```{output}
ch6_code/src/breakpoint_graph/ColoredEdge.py
python
# 2BREAK_MARKDOWN\s*\n([\s\S]+)\n\s*# 2BREAK_MARKDOWN
```

```{ch6}
breakpoint_graph.CyclicBreakpointGraph
[[+A, -B, -C, +D], [+E]]
[[+A, +B, -D], [-C, -E]]
graph_show
```

```{note}
It isn't discussed here, but the Pevzner book put an emphasis on calculating the parsimonious number of reversals (reversal distance) without having to go through and apply two-breaks in the breakpoint graph_GR. The basic idea is to count the number of red-blue cycles in the graph.

For a cyclic breakpoint graph_GRs, a single red-blue cycle is when you pick a node, follow the blue edge, then follow the red edge, then follow the blue edge, then follow the red edge, ..., until you arrive back at the same node. If the blue and red genomes match perfectly, the number of red-blue cycles should equal the number of synteny blocks. Otherwise, you can calculate the number of reversals needed to get them to equal by subtracting the number of red-blue cycles by the number of synteny blocks.

For a linear breakpoint graph_GRs, a single red-blue cycle isn't actually a cycle because: Pick the termination node, follow a blue edge, then follow the red edge, then follow the blue edge, then follow the red edge, ... until you arrive back at the termination node (what if there are actual cyclic red-blue loops as well like in cyclic breakpoint graph_GRs?). If the blue and red genomes match perfectly, the number of red-blue cycles should equal the number of synteny blocks + 1. Otherwise, you can **ESTIMATE** the number of reversals needed to get them to equal by subtracting the number of red-blue cycles by the number of synteny blocks + 1.

To calculate the real number of reversals need for linear breakpoint graph_GRs (not estimate), there's a [paper on ACM DL](https://dl.acm.org/doi/10.1145/300515.300516) that goes over the algorithm. I glanced through it but I don't have the time / wherewithal to go through it. Maybe do it in the future.

UPDATE: Calculating the number of reversals quickly is important because the number of reversals can be used as a distance metric when computing a phylogenetic tree across a set of species (a tree that shows how closely a set of species are related / how they branched out). See distance matrix definition.
```

## Phylogeny

`{bm} /(Algorithms\/Phylogeny)_TOPIC/`

```{prereq}
Algorithms/K-mer_TOPIC
```

Phylogeny is the concept of inferring the evolutionary history of a set of biological entities (e.g. animal species, viruses, etc..) by inspecting properties of those entities for relatedness (e.g. phenotypic, genotypic, etc..).
 
```{svgbob}
                      * "Ancestor Animal"
                     / \
                    /   \
                   /     \
"Ancestor Feline" *       \
                 / \       \
                /   \       \
               /     \       \
              *       *       *
             Cat     Lion    Bear
```

Evolutionary history is often displayed as a tree called a phylogenetic tree, where leaf nodes represent known entities and internal nodes represent inferred ancestor entities. The example above shows a phylogenetic tree for the species cat, lion, and bear based on phenotypic inspection. Cats and lions are inferred as descending from the same ancestor because both have deeply shared physical and behavioural characteristics (felines). Similarly, that feline ancestor and bears are inferred as descending from the same ancestor because all descendants walk on 4 legs.

The typical process for phylogeny is to first measure how related a set of entities are to each other, where each measure is referred to as a distance (e.g. `dist(cat, lion) = 2`), then work backwards to find a phylogenetic tree that fits / maps to those distances. The distance may be any metric so long as ...

 * it computes the distance to itself as 0 (e.g. `dist(cat, cat) = 0`)
 * it computes the distance to any other entity as > 0 (e.g. `dist(cat, lion) = 2`)
 * it computes the same distance for the same pair regardless of order (e.g. `dist(cat, lion) = dist(lion, cat)`)
 * computed distances don't leapfrog each other (e.g. `dist(cat, lion) + dist(lion, dog) >= dist(cat, dog)`)

````{note}
The leapfrogging point may be confusing. All it's saying is that taking an indirect path between two species should produce a distance that's >= the direct path. For example, the direct path between cat and dog is 6: `dist(cat, dog) = 6`. If you were to instead jump from cat to lion `dist(cat, lion) = 2`, then from lion to dog `dist(lion, dog) = 5`, that combined distance should be >= to 6...

```
dist(cat, dog)  = 6
dist(cat, lion) = 2
dist(lion, dog) = 5

dist(cat, lion) + dist(lion, dog) >= dist(cat, dog)
        2       +        5        >=       6
                7                 >=       6
```

The Pevzner book refers to this as the triangle inequality.

```{svgbob}
      2
cat ------ lion
   \        |
    \       |
     \      |
    6 \     | 5
       \    |
        \   |
         \  |
          \ |
          dog
```

Later on non-conforming distance matrices are discussed called non-additive distance matrices. I don't know if non-additive distance matrices are required to have this specific property, but they should have all others.
````

Examples of metrics that may be used as distance, referred to as distance metrics, include...

 * hamming distance between DNA / protein sequences.
 * global alignment score between DNA / protein sequences.
 * two-break count (reversal distance).
 * number of similar physical or behavioural attributes.
 * etc..

Distances for a set of entities are typically represented as a 2D matrix that contains all possible pairings, called a distance matrix. The distance matrix for the example Cat/Lion/Bear phylogenetic tree is ...

|      | Cat | Lion | Bear |
|------|-----|------|------|
| Cat  | 0   | 2    | 23   |
| Lion | 2   | 0    | 23   |
| Bear | 23  | 23   | 0    |

```{svgbob}
                      * "Ancestor Animal"
                     / \
                 6  /   \
                   /     \
"Ancestor Feline" *       \ 16
                 / \       \
              1 /   \ 1     \
               /     \       \
              *       *       *
             Cat     Lion    Bear

* "The same tree as shown above, but with distances"
  "assigned to edge weights"
```

Note how the distance matrix has the distance for each pair slotted twice, mirrored across the diagonal of 0s (self distances). For example, the distance between bear and lion is listed twice.

```{note}
Just to make it explicit: The ultimate point of this section is to work backwards from a distance matrix to a phylogenetic tree (essentially the concept of phylogeny -- inferring evolutionary history of a set of known / present-day organisms based on how different they are).
```

```{note}
The best way to move forward with this, assuming that you're brand new to it, is to first understand the following four subsections...

* Algorithms/Phylogeny/Tree to Additive Distance Matrix_TOPIC
* Algorithms/Phylogeny/Tree to Simple Tree_TOPIC
* Algorithms/Phylogeny/Additive Distance Matrix Cardinality_TOPIC

Then jump to the algorithm you want to learn (subsection) within Algorithms/Phylogeny/Distance Matrix to Tree_TOPIC and work from the prerequisites to the algorithm. Otherwise all the sections in between come off as disjointed because it's building the intermediate knowledge required for the final algorithms.
```

### Tree to Additive Distance Matrix

`{bm} /(Algorithms\/Phylogeny\/Tree to Additive Distance Matrix)_TOPIC/`

**WHAT**: Given a tree, the distance matrix generated from that tree is said to be an additive distance matrix.

**WHY**: The term additive distance matrix is derived from the fact that edge weights within the tree are being _added_ together to generate the distances in the distance matrix. For example, in the following tree ...

```{svgbob}
       * B      
    1 / \       
     /   \      
  A *     \ 2   
 1 / \ 1   \    
  /   \     \   
 *     *     *  
Cat   Lion  Bear
```

 * `dist(Cat, Lion)  = dist(Cat, A) + dist(A, Lion)               = 1 + 1     = 2`
 * `dist(Cat, Bear)  = dist(Cat, A) + dist(A, B) + dist(B, Bear)  = 1 + 1 + 2 = 4`
 * `dist(Lion, Bear) = dist(Lion, A) + dist(A, B) + dist(B, Bear) = 1 + 1 + 2 = 4`

|      | Cat | Lion | Bear |
|------|-----|------|------|
| Cat  |  0  |  2   |  4   |
| Lion |  2  |  0   |  4   |
| Bear |  4  |  4   |  0   |

However, distance matrices aren't commonly generated from trees. Rather, they're generated by comparing present-day entities to each other to see how diverged they are (their distance from each other). There's no guarantee that a distance matrix generated from comparisons will be an additive distance matrix. That is, there must exist a tree with edge weights that satisfy that distance matrix for it to be an additive distance matrix (commonly referred to as a tree that fits the distance matrix).

In other words, while a...

 * distance matrix generated from a tree will always be an additive distance matrix, not all distance matrices are additive distance matrices. For example, a tree doesn't exist that maps to the following distance matrix ...

   |        | Cat | Lion | Bear | Racoon |
   |--------|-----|------|------|--------|
   | Cat    |  0  |  1   |  1   |    1   |
   | Lion   |  1  |  0   |  1   |    1   |
   | Bear   |  1  |  1   |  0   |    9   |
   | Racoon |  1  |  1   |  9   |    0   |

 * tree maps to exactly one additive distance matrix, that additive distance matrix maps to many different trees. For example, the following additive distance matrix may map to any of the following trees ...

   |      | Cat | Lion | Bear |
   |------|-----|------|------|
   | Cat  |  0  |  2   |  4   |
   | Lion |  2  |  0   |  4   |
   | Bear |  4  |  4   |  0   |

   ```{svgbob}
          *                        *                        *        
       1 / \                    1 / \ 1                0.5 / \       
        /   \                    /   \                    /   \      
       *     \ 2                *     *                  *     \ 1.5 
    1 / \ 1   \              1 / \ 1   \ 1            1 / \ 1   \    
     /   \     \              /   \     \              /   \     \   
    *     *     *            *     *     *            *     *     *  
   Cat   Lion  Bear         Cat   Lion  Bear         Cat   Lion  Bear
   ```

**ALGORITHM**:

```{output}
ch7_code/src/phylogeny/TreeToAdditiveDistanceMatrix.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch7}
phylogeny.TreeToAdditiveDistanceMatrix
[[v0,i0,11], [v1,i0,2], [v2,i0,10], [i0,i1,4], [i1,i2,3], [i2,v3,3], [i2,v4,4], [i1,v5,7]]
```

### Tree to Simple Tree

`{bm} /(Algorithms\/Phylogeny\/Tree to Simple Tree)_TOPIC/`

```{prereq}
Algorithms/Phylogeny/Tree to Additive Distance Matrix_TOPIC
```

**WHAT**: Convert a tree into a simple tree. A simple tree is an unrooted tree where ...

 * every internal node has a degree_GRAPH > 2.
 * every edge has a weight of > 0.
 
The first point just means that the tree can't contain non-splitting internal nodes. By definition a tree's leaf nodes each have a degree_GRAPH of 1, and this restriction makes it so that each internal node must have a degree_GRAPH > 2 instead of >= 2...

```{svgbob}
"splitting (GOOD)"             "non-splitting (BAD)"

     *   *                              *
      \ /                              /   
       *                              *  
       |                              |    
       *                              *    

* "Note how in the non-splitting version, the"
  "node in-between has a degree of 2."
```

```{svgbob}
"non-simple tree"             "simple tree"

         *                             
        / 1                            
   *   *                               
  1 \ / 1                       *   * 
     *                         1 \ / 2
   3 |                            *   
     *                          4 |   
   1 |                            *   
     *                         3 / \ 2
  1 / \ 2                       *   * 
   *   *                               
2 /                                    
 *                                        

* "Non-simple tree transformed into a simple tree. Edges"
  "that were merged had their weights summed."
```

In the context of phylogeny, a simple tree's ...

 * leaf nodes represent known entities.
 * internal nodes represent inferred ancestor entities.
 * edge weights represent distances between entities.

**WHY**: Simple trees have properties / restrictions that simplify the process of working backwards from a distance matrix to a tree. In other words, when constructing a tree from a distance matrix, the process is simpler if the tree is restricted to being a simple tree.

The first property is that a unique simple tree exists for a unique additive distance matrix (one-to-one mapping). That is, it isn't possible for...

 * two different simple trees to map to the same distance matrix.
 * two different distance matrices to map to the same simple tree.
 
For example, the following additive distance matrix will only ever map to the following simple tree (and vice-versa)...

|   | w | u | y | z |
|---|---|---|---|---|
| w | 0 | 3 | 8 | 7 |
| u | 3 | 0 | 9 | 8 |
| y | 8 | 9 | 0 | 5 |
| z | 7 | 8 | 5 | 0 |

```{svgbob}
"simple-tree"

 w   u       
1 \ / 2      
   a         
 4 |         
   b         
3 / \ 2      
 y   z       
```

However, that same additive distance matrix can map to an infinite number of non-simple trees (and vice-versa)...

```{svgbob}
"non-simple tree 1"  "non-simple tree 2"  "non-simple tree 2"

          u                     u                  
         / 1                   / 1.5               
    w   c                 w   c               w   u     
   1 \ / 1               1 \ / 0.5           1 \ / 2    
      a                     a                   a       
    3 |                   2 |                 4 |                etc...  
      d                     d                   b         
    1 |                   2 |                3 / \ 1.5  
      b                     b                 y   f     
   1 / \ 2               0 / \ 2                   \ 0.5
    e   z                 e   z                     z   
 2 /                   3 /                                 
  y                     y                             
```

```{note}
To clarify: This property / restriction is important because when reconstructing a tree from the distance matrix, if you restrict yourself to a simple tree you'll only ever have 1 tree to reconstruct to. This makes the algorithms simpler. This is discussed further in the cardinality subsection.
```

The second property is that the direction of evolution isn't maintained in a simple tree: It's an unrooted tree with undirected edges. This is a useful property because, while a distance matrix may provide enough information to infer common ancestry, it doesn't provide enough information to know the true parent-child relationships between those ancestors. For example, any of the internal nodes in the following simple tree may be the top-level entity that all other entities are descendants of ...

```{svgbob}
UNROOTED            "c AS ROOT"            "d AS ROOT"            "f AS ROOT"

 a   b                 c                        d                    f
  \ /                 /|\                      /|\                  /|\
   c                 a b d                    c e f                g h d
   |                    / \                  /|   |\                  / \  
   d                   e   f                a b   g h                e   c
  / \                     / \                                           / \
 e   f                   g   h                                         a   b
    / \                                                              
   g   h                                                             

* "Either c, d, or f could be the root."
```

The third property is that weights must be > 0, which is because of the restriction on distance metrics specified in the parent section: The distance between any two entities must be > 0. That is, it doesn't make sense for the distance between two entities to be ...

 * < 0 because distance represents how diverged the entities are from each other. Having a negative amount of divergence doesn't make sense.
 * = 0 because then the two nodes between the edge would represent the same entity. Having more than one representation of the same entity in the tree doesn't make sense.

```{svgbob}
 a   c                        a                         
1 \ / 0                      1 \                            a 
   d         "... to ..."       d       "... to ..."      2 |
 1 |                          1 |                           b
   b                            b                      


* "Nodes c and d represent the same entity (distance of 0 means"
  "no divergence / same entity). It would make sense to merge c"
  "and d into just d. Doing so would make it so that d has a"
  "degree of 2, meaning that the two edges its connected to need"
  "to merged into a single edge to make this a valid simple tree."
```

**ALGORITHM**:

The following examples show various real evolutionary paths and their corresponding simple trees. Note how the simple trees neither fully represent the true lineage nor the direction of evolution (simple trees are unrooted and undirected).

```{svgbob}
   "REAL EVOLUTIONARY PATH"                         "SIMPLE TREE"
                                                                   
                                                       entity1
entity1  ---> entity2                                    |
                                                       entity2
                                                                   
                                                                   
                                                                   
                                                       entity1
entity2  ---> entity1                                    |
                                                       entity2
                                                                   
                                                                   
                                                                   
         .---> entity1                                 entity1
parent1 -+                                               |
         '---> entity2                                 entity2
                                                                   
                                                                   
                                                                   
         .---> entity1                                 entity1
         |                                               |
parent1 -+---> entity2                                 parent1
         |                                              /   \
         '---> entity3                             entity2   entity3
                                                                   

                                                                   
                                                       entity1
         .---> entity1 ---> entity2                      |
parent1 -+                                             parent1
         '---> entity3                                  /   \
                                                   entity2   entity3
                                                                   
                                                                   
                                                                   
                        .---> entity1                  entity1
         .---> parent2 -+                                |
parent1 -+              '---> entity2                  parent1
         '---> entity3                                  /   \
                                                   entity2   entity3
                                                                   
                                                                   
                                                                   
                        .---> entity1              entity1    entity2
         .---> parent2 -+                                \   /       
         |              '---> entity2                   parent2      
parent1 -+                                                 |         
         |              .---> entity3                   parent3      
         '---> parent3 -+                                /   \       
                        '---> entity4              entity3    entity4
```

In the first two examples, one present-day entity branched off from another present-day entity. Both entities are still present-day entities (the entity branched off from isn't extinct).

In the fifth example, parent1 split off to the present-day entities entity1 and entity3, then entity2 branched off entity1. All three entities are present-day entities (neither entity1, entity2, nor entity3 is extinct).

In the third and last two examples, the top-level parent doesn't show up because adding it would break the requirement that internal nodes must be splitting (degree_GRAPH > 2). For example, adding parent1 into the simple tree of the last example above causes parent1 to have a degree_GRAPH = 2...

```{svgbob}
entity1    entity2
      \   /       
     parent2      
        |         
     parent1      
        |         
     parent3      
      /   \       
entity3    entity4

* "parent1 has a degree of 2, meaning this is not a valid"
  "simple tree."
```

The following algorithm removes nodes of degree_GRAPH = 2, merging its two edges together. This makes it so every internal edge has a degree_GRAPH of > 2...

```{output}
ch7_code/src/phylogeny/TreeToSimpleTree.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch7}
phylogeny.TreeToSimpleTree
simplify
[[v0,i0,11], [v1,i0,2], [v2,i0,10], [i0,i1,4], [i1,i2,3], [i2,v3,3], [i1,v4,7]]
```

The following algorithm tests a tree to see if it meets the requirements of being a simple tree...

```{output}
ch7_code/src/phylogeny/TreeToSimpleTree.py
python
# MARKDOWN_TREE_TEST\s*\n([\s\S]+)\n\s*# MARKDOWN_TREE_TEST
```

```{ch7}
phylogeny.TreeToSimpleTree
test
[[v0,i0,11], [v1,i0,2], [v2,i0,10], [i0,i1,4], [i1,i2,3], [i2,v3,3], [i1,v4,7]]
```

### Additive Distance Matrix Cardinality

`{bm} /(Algorithms\/Phylogeny\/Additive Distance Matrix Cardinality)_TOPIC/`

```{prereq}
Algorithms/Phylogeny/Tree to Simple Tree_TOPIC
Algorithms/Phylogeny/Tree to Additive Distance Matrix_TOPIC
```

```{note}
This was discussed briefly in the simple tree section, but it's being discussed here in its own section because it's important.
```

**WHAT**: Determine the cardinality of between an additive distance matrix and a type of tree. For, ...

 * simple trees, there's a 1-to-1 mapping for tree to / from additive distance matrix. That is, a unique simple tree will map to a unique additive distance and vice-versa.
 * non-simple trees, there's a 1-to-many mapping for tree to / from additive distance matrix. That is, a non-simple tree will only ever generate one additive distance matrix but that additive distance matrix will map to many non-simple trees.

**WHY**: Non-simple trees are essentially derived from simple trees by splicing nodes in between edges (breaking up an edge into multiple edges). For example, any of the following non-simple trees...

```{svgbob}
           *                                 *                                 *           
          / \                               / \                               / \          
     0.5 /   \                         1.0 /   \                             /   \ 0.5     
        /     \                           *     \                           /     *       
       *       \ 2.0                     / \     \ 1.5                     *       \               etc...
      / \       \                   1.0 /   \     \                       / \       \      
 1.5 /   \ 0.5   \                     *     \ 0.5 \                 1.5 /   \ 0.5   \ 1.0 
    /     \       \               0.5 /       \     \                   /     \       \    
   *       *       *                 *         *     *                 *       *       *   
  Cat     Lion    Bear              Cat       Lion  Bear              Cat     Lion    Bear 
```

... will collapse to the following simple tree (edges connected by nodes of degree_GRAPH 2 merged by adding weights) ...

```{svgbob}
           * Bear
          /
     2.5 /
        /
       *
      / \ 
 1.5 /   \ 0.5
    /     \
   *       *
  Cat     Lion
```

All of the trees above, both the non-simple trees and the simple tree, will generate the following additive distance matrix ...

|      | Cat | Lion | Bear |
|------|-----|------|------|
| Cat  |  0  |  2   |  4   |
| Lion |  2  |  0   |  3   |
| Bear |  4  |  3   |  0   |

Similarly, this additive distance matrix will only ever map to the simple tree shown above or one of its many non-simple tree derivatives (3 of which are shown above). There is no other simple tree that this additive distance matrix can map to / no other simple tree that will generate this distance matrix. In other words, it isn't possible for...

 * two different simple trees to map to the same distance matrix.
 * two different distance matrices to map to the same simple tree.
 
Working backwards from a distance matrix to a tree is less complex when limiting the tree to a simple tree, because there's only one simple tree possible (vs many non-simple trees).

**ALGORITHM**:

This section is more of a concept than an algorithm. The following just generates an additive distance matrix from a tree and says if that tree is unique to that additive distance matrix (it should be if it's a simple tree). There is no code to show for it because it's just calling things from previous sections (generating an additive distance matrix and checking if a simple tree).

```{output}
ch7_code/src/phylogeny/CardinalityTest.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch7}
phylogeny.CardinalityTest
[[v0,i0,11], [v1,i0,2], [v2,i0,10], [i0,i1,4], [i1,i2,3], [i2,v3,3], [i2,v4,4], [i1,v5,7]]
```

### Test Additive Distance Matrix

`{bm} /(Algorithms\/Phylogeny\/Test Additive Distance Matrix)_TOPIC/`

```{prereq}
Algorithms/Phylogeny/Tree to Additive Distance Matrix_TOPIC
Algorithms/Phylogeny/Tree to Simple Tree_TOPIC
Algorithms/Phylogeny/Additive Distance Matrix Cardinality_TOPIC
```

**WHAT**: Determine if a distance matrix is an additive distance matrix.

**WHY**: Knowing if a distance matrix is additive helps determine how the tree for that distance matrix should be constructed. For example, since it's impossible for a non-additive distance matrix to fit a tree, different algorithms are needed to approximate a tree that somewhat fits.

**ALGORITHM**:

This algorithm, called the four point condition algorithm, tests pairs within each quartet of leaf nodes to ensure that they meet a certain set of conditions. For example, the following tree has the quartet of leaf nodes (v0, v2, v4, v6) ...

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
 subgraph cluster_one {
  v0 [style=filled, fillcolor="gray"]
  v1
  v2 [style=filled, fillcolor="gray"]
  v3
  v4 [style=filled, fillcolor="gray"]
  v5
  v6 [style=filled, fillcolor="gray"]
  v0 -- i0
  v1 -- i0
  i0 -- i1
  v2 -- i1
  v3 -- i1
  i1 -- i2
  v4 -- i2
  i2 -- i3
  i3 -- v5
  i3 -- v6
 }
}
```

A quartet makes up 3 different pair combinations (pairs of pairs). For example, the example quartet above has the 3 pair combinations ...

 * ((v0, v2), (v4, v6))
 * ((v0, v4), (v2, v6))
 * ((v0, v6), (v2, v4))

```{note}
Order of the pairing doesn't matter at either level. For example, ((v0, v2), (v4, v6)) and ((v6, v4), (v2, v0)) are the same. That's why there are only 3.
```

Of these 3 pair combinations, the test checks to see that ...

 1. the sum of distances for one is == the sum of distances for another.
 2. the sum of distances for the remaining is <= the sums from the point above.

In a tree with edge weights >= 0, every leaf node quartet will pass this test. For example, for leaf node quartet (v0, v2, v4, v6) highlighted in the example tree above ...

```{dot}
graph G {
graph[rankdir=LR]
node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
 subgraph cluster_two2 {
  fontname="Courier-Bold"
  fontsize=10
  label="dist(v0, v2) + dist(v4, v6)"
  z_v0 -- z_i0 [color=violet, penwidth=2.5]
  z_v1 -- z_i0
  z_i0 -- z_i1 [color=violet, penwidth=2.5]
  z_v2 -- z_i1 [color=violet, penwidth=2.5]
  z_v3 -- z_i1
  z_i1 -- z_i2
  z_v4 -- z_i2 [color=tan, penwidth=2.5]
  z_i2 -- z_i3 [color=tan, penwidth=2.5]
  z_i3 -- z_v5
  z_i3 -- z_v6 [color=tan, penwidth=2.5]
  z_v0 [label= "v0", style=filled, fillcolor="violet"] 
  z_v1 [label= "v1"] 
  z_i0 [label= "i0"] 
  z_i1 [label= "i1"] 
  z_v2 [label= "v2", style=filled, fillcolor="violet"] 
  z_v3 [label= "v3"] 
  z_i2 [label= "i2"] 
  z_i3 [label= "i3"] 
  z_v4 [label= "v4", style=filled, fillcolor="tan"] 
  z_v5 [label= "v5"] 
  z_v6 [label= "v6", style=filled, fillcolor="tan"]
 }
 subgraph cluster_two {
  fontname="Courier-Bold"
  fontsize=10
  label="dist(v0, v6) + dist(v2, v4)"
  y_v0 -- y_i0 [color=gold, penwidth=2.5]
  y_v1 -- y_i0
  y_i0 -- y_i1 [color=gold, penwidth=2.5]
  y_v2 -- y_i1 [color=pink, penwidth=2.5]
  y_v3 -- y_i1
  y_i1 -- y_i2 [color="pink:invis:gold", penwidth=2.5]
  y_v4 -- y_i2 [color=pink, penwidth=2.5]
  y_i2 -- y_i3 [color=gold, penwidth=2.5]
  y_i3 -- y_v5
  y_i3 -- y_v6 [color=gold, penwidth=2.5]
  y_v0 [label= "v0", style=filled, fillcolor="gold"] 
  y_v1 [label= "v1"] 
  y_i0 [label= "i0"] 
  y_i1 [label= "i1"] 
  y_v2 [label= "v2", style=filled, fillcolor="pink"] 
  y_v3 [label= "v3"] 
  y_i2 [label= "i2"] 
  y_i3 [label= "i3"] 
  y_v4 [label= "v4", style=filled, fillcolor="pink"] 
  y_v5 [label= "v5"] 
  y_v6 [label= "v6", style=filled, fillcolor="gold"]
 }
 subgraph cluster_one {
  fontname="Courier-Bold"
  fontsize=10
  label="dist(v0, v4) + dist(v2, v6)"
  x_v0 -- x_i0 [color=turquoise, penwidth=2.5]
  x_v1 -- x_i0
  x_i0 -- x_i1 [color=turquoise, penwidth=2.5]
  x_v2 -- x_i1 [color=orange, penwidth=2.5]
  x_v3 -- x_i1
  x_i1 -- x_i2 [color="orange:invis:turquoise", penwidth=2.5]
  x_v4 -- x_i2 [color=turquoise, penwidth=2.5]
  x_i2 -- x_i3 [color=orange, penwidth=2.5]
  x_i3 -- x_v5
  x_i3 -- x_v6 [color=orange, penwidth=2.5]
  x_v0 [label= "v0", style=filled, fillcolor="turquoise"] 
  x_v1 [label= "v1"] 
  x_i0 [label= "i0"] 
  x_i1 [label= "i1"] 
  x_v2 [label= "v2", style=filled, fillcolor="orange"] 
  x_v3 [label= "v3"] 
  x_i2 [label= "i2"] 
  x_i3 [label= "i3"] 
  x_v4 [label= "v4", style=filled, fillcolor="turquoise"] 
  x_v5 [label= "v5"] 
  x_v6 [label= "v6", style=filled, fillcolor="orange"]
 }
}
```

`{h}violet dist(v0,v2)` + `{h}tan dist(v4,v6)` <= `{h}gold dist(v0,v6)` + `{h}pink dist(v2,v4)` == `{h}turquoise dist(v0,v4)` + `{h}orange dist(v2,v6)`

Note how the same set of edges are highlighted between the first two diagrams (same distance contributions) while the third diagram has less edges highlighted (missing some distance contributions). This is where the inequality comes from.

```{note}
I'm almost certain this inequality should be < instead of <=, because in a phylogenetic tree you can't have an edge weight of 0, right? An edge weight of 0 would indicate that the nodes at each end of an edge are the same entity.
```

All of the information required for the above calculation is available in the distance matrix...

```{output}
ch7_code/src/phylogeny/FourPointCondition.py
python
# MARKDOWN_QUARTET_TEST\s*\n([\s\S]+)\n\s*# MARKDOWN_QUARTET_TEST
```

If a distance matrix was derived from a tree / fits a tree, its leaf node quartets will also pass this test. That is, if all leaf node quartets in a distance matrix pass the above test, the distance matrix is an additive distance matrix ...

```{output}
ch7_code/src/phylogeny/FourPointCondition.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch7}
phylogeny.FourPointCondition
[0, 3, 8, 7]
[3, 0, 9, 8]
[8, 9, 0, 5]
[7, 8, 5, 0]
```

```{note}
Could the differences found by this algorithm help determine how "close" a distance matrix is to being an additive distance matrix?
```

### Find Limb Length

`{bm} /(Algorithms\/Phylogeny\/Find Limb Length)_TOPIC/`

```{prereq}
Algorithms/Phylogeny/Tree to Additive Distance Matrix_TOPIC
Algorithms/Phylogeny/Tree to Simple Tree_TOPIC
Algorithms/Phylogeny/Additive Distance Matrix Cardinality_TOPIC
```

**WHAT**: Given an additive distance matrix, there exists a unique simple tree that fits that matrix. Compute the limb length of any leaf node in that simple tree just from the additive distance matrix.

**WHY**: This is one of the operations required to construct the unique simple tree for an additive distance matrix.

**ALGORITHM**:

To conceptualize how this algorithm works, consider the following simple tree and its corresponding additive distance matrix...

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
 subgraph cluster_one {
  fontname="Courier-Bold"
  fontsize=10
  v0 -- i0
  v1 -- i0
  i0 -- i1
  v2 -- i1
  v3 -- i1
  i1 -- i2
  v4 -- i2
  i2 -- i3
  i3 -- v5
  i3 -- v6
 }
}
```

|    | v0 | v1 | v2 | v3 | v4 | v5 | v6 |
|----|----|----|----|----|----|----|----|
| v0 | 0  | 13 | 19 | 20 | 29 | 40 | 36 |
| v1 | 13 | 0  | 10 | 11 | 20 | 31 | 27 |
| v2 | 19 | 10 | 0  | 11 | 20 | 31 | 27 |
| v3 | 20 | 11 | 11 | 0  | 21 | 32 | 28 |
| v4 | 29 | 20 | 20 | 21 | 0  | 17 | 13 |
| v5 | 40 | 31 | 31 | 32 | 17 | 0  | 6  |
| v6 | 36 | 27 | 27 | 28 | 13 | 6  | 0  |

In this simple tree, consider a path between leaf nodes that travels over v2's parent (v2 itself excluded). For example, `{h}pink path(v1,v5)` travels over v2's parent...

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
 subgraph cluster_one {
  fontname="Courier-Bold"
  fontsize=10
  label="path(v1,v5)"
  v0 -- i0
  v1 -- i0 [color="pink", penwidth="2.5"]
  i0 -- i1 [color="pink", penwidth="2.5"]
  v2 -- i1
  v3 -- i1
  i1 -- i2 [color="pink", penwidth="2.5"]
  v4 -- i2
  i2 -- i3 [color="pink", penwidth="2.5"]
  i3 -- v5 [color="pink", penwidth="2.5"]
  i3 -- v6
  i1 [fillcolor="gray", style="filled"]
 }
}
```

Now, consider the paths between each of the two nodes in the path above (v1 and v5) and v2: `{h}orange path(v1,v2)` + `{h}blue path(v2,v5)` ...

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
 subgraph cluster_one {
  fontname="Courier-Bold"
  fontsize=10
  label="path(v1,v2) + path(v2,v5)"
  v0 -- i0
  v1 -- i0 [color="orange", penwidth="2.5"]
  i0 -- i1 [color="orange", penwidth="2.5"]
  v2 -- i1 [color="blue:invis:orange", penwidth="2.5"]
  v3 -- i1
  i1 -- i2 [color="blue", penwidth="2.5"]
  v4 -- i2
  i2 -- i3 [color="blue", penwidth="2.5"]
  i3 -- v5 [color="blue", penwidth="2.5"]
  i3 -- v6
  i1 [fillcolor="gray", style="filled"]
 }
}
```

Notice how the edges highlighted between `{h}pink path(v1,v5)` and `{h}orange path(v1,v2)` + `{h}blue path(v2,v5)` would be the same had it not been for the two highlights on v2's limb. Adding `{h}red 2 * path(v2,i0)` to `{h}pink path(v1,v5)` makes it so that each edge is highlighted an equal number of times ...

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
 subgraph cluster_two {
  fontname="Courier-Bold"
  fontsize=10
  label="path(v1,v5) + 2 * path(v2,i1)"
  y_v0 [label=v0]
  y_v1 [label=v1]
  y_v2 [label=v2]
  y_v3 [label=v3]
  y_v4 [label=v4]
  y_v5 [label=v5]
  y_v6 [label=v6]
  y_i0 [label=i0]
  y_i1 [label=i1]
  y_i2 [label=i2]
  y_i3 [label=i3]
  y_v0 -- y_i0
  y_v1 -- y_i0 [color="pink", penwidth="2.5"]
  y_i0 -- y_i1 [color="pink", penwidth="2.5"]
  y_v2 -- y_i1 [color="red:invis:red", penwidth="2.5"]
  y_v3 -- y_i1
  y_i1 -- y_i2 [color="pink", penwidth="2.5"]
  y_v4 -- y_i2
  y_i2 -- y_i3 [color="pink", penwidth="2.5"]
  y_i3 -- y_v5 [color="pink", penwidth="2.5"]
  y_i3 -- y_v6
  y_i1 [fillcolor="gray", style="filled"]
 }
 subgraph cluster_one {
  fontname="Courier-Bold"
  fontsize=10
  label="path(v1,v2) + path(v2,v5)"
  x_v0 [label=v0]
  x_v1 [label=v1]
  x_v2 [label=v2]
  x_v3 [label=v3]
  x_v4 [label=v4]
  x_v5 [label=v5]
  x_v6 [label=v6]
  x_i0 [label=i0]
  x_i1 [label=i1]
  x_i2 [label=i2]
  x_i3 [label=i3]
  x_v0 -- x_i0
  x_v1 -- x_i0 [color="orange", penwidth="2.5"]
  x_i0 -- x_i1 [color="orange", penwidth="2.5"]
  x_v2 -- x_i1 [color="blue:invis:orange", penwidth="2.5"]
  x_v3 -- x_i1
  x_i1 -- x_i2 [color="blue", penwidth="2.5"]
  x_v4 -- x_i2
  x_i2 -- x_i3 [color="blue", penwidth="2.5"]
  x_i3 -- x_v5 [color="blue", penwidth="2.5"]
  x_i3 -- x_v6
  x_i1 [fillcolor="gray", style="filled"]
 }
}
```

`{h}orange path(v1,v2)` + `{h}blue path(v2,v5)` = `{h}pink path(v1,v5)` + `{h}red 2 * path(v2,i1)`

Contrast the above to what happens when the pair of leaf nodes selected DOESN'T travel through v2's parent. For example, `{h}purple path(v4,v5)` doesn't travel through v2's parent ...

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
 subgraph cluster_two {
  fontname="Courier-Bold"
  fontsize=10
  label="path(v4,v5) + 2 * path(v2,i1)"
  y_v0 [label=v0]
  y_v1 [label=v1]
  y_v2 [label=v2]
  y_v3 [label=v3]
  y_v4 [label=v4]
  y_v5 [label=v5]
  y_v6 [label=v6]
  y_i0 [label=i0]
  y_i1 [label=i1]
  y_i2 [label=i2]
  y_i3 [label=i3]
  y_v0 -- y_i0
  y_v1 -- y_i0
  y_i0 -- y_i1
  y_v2 -- y_i1 [color="red:invis:red", penwidth="2.5"]
  y_v3 -- y_i1
  y_i1 -- y_i2 
  y_v4 -- y_i2 [color="purple", penwidth="2.5"]
  y_i2 -- y_i3 [color="purple", penwidth="2.5"]
  y_i3 -- y_v5 [color="purple", penwidth="2.5"]
  y_i3 -- y_v6
  y_i1 [fillcolor="gray", style="filled"]
 }
 subgraph cluster_one {
  fontname="Courier-Bold"
  fontsize=10
  label="path(v4,v2) + path(v2,v5)"
  x_v0 [label=v0]
  x_v1 [label=v1]
  x_v2 [label=v2]
  x_v3 [label=v3]
  x_v4 [label=v4]
  x_v5 [label=v5]
  x_v6 [label=v6]
  x_i0 [label=i0]
  x_i1 [label=i1]
  x_i2 [label=i2]
  x_i3 [label=i3]
  x_v0 -- x_i0
  x_v1 -- x_i0
  x_i0 -- x_i1
  x_v2 -- x_i1 [color="brown:invis:blue", penwidth="2.5"]
  x_v3 -- x_i1
  x_i1 -- x_i2 [color="brown:invis:blue", penwidth="2.5"]
  x_v4 -- x_i2 [color="brown", penwidth="2.5"]
  x_i2 -- x_i3 [color="blue", penwidth="2.5"]
  x_i3 -- x_v5 [color="blue", penwidth="2.5"]
  x_i3 -- x_v6
  x_i1 [fillcolor="gray", style="filled"]
 }
}
```

`{h}brown path(v4,v2)` + `{h}blue path(v2,v5)` > `{h}purple path(v4,v5)` + `{h}red 2 * path(v2,i1)`

Even when `{h}purple path(v4,v5)` includes `{h}red 2 * path(v2,i1)`, less edges are highlighted when compared to `{h}brown path(v4,v2)` + `{h}blue path(v2,v5)`. Specifically, edge(i1,i2) is highlighted zero times vs two times.

The above two examples give way to the following two formulas: Given a simple tree with distinct leaf nodes {L, A, B} and L's parent Lp ...

 * path(L,A) + path(L,B) = path(A,B) + 2 * path(L,Lp) -- if path(A,B) travels through Lp
 * path(L,A) + path(L,B) > path(A,B) + 2 * path(L,Lp) -- if path(A,B) doesn't travel through Lp

These two formulas work just as well with distances instead of paths...

 * dist(L,A) + dist(L,B) = dist(A,B) + 2 * dist(L,Lp) -- if path(A,B) travels through Lp
 * dist(L,A) + dist(L,B) > dist(A,B) + 2 * dist(L,Lp) -- if path(A,B) doesn't travel through Lp

The reason distances work has to do with the fact that simple trees require edges weights of > 0, meaning traversing over an edge always increases the overall distance. If ...

 * less edges are highlighted, the distance will be less.
 * same edges are highlighted, the distance will be equal.
 * more edges are highlighted, the distance will be more.

```{note}
The Pevzner book has the 2nd formula above as >= instead of >.

I'm assuming they did this because they're letting edge weights be >= 0 instead of > 0, which doesn't make sense because an edge with a weight of 0 means the same entity exists on both ends of the edge. If an edge weight is 0, it'll contribute nothing to the distance, meaning that more edges being highlighted doesn't necessarily mean a larger distance.
```

In the above formulas, L's limb length is represented as dist(L,Lp). Except for dist(L,Lp), all distances in the formulas are between leaf nodes and as such are found in the distance matrix. Therefore, the formulas need to be isolated to dist(L,Lp) in order to derive what L's limb length is ...

 * dist(L,A) + dist(L,B) = dist(A,B) + 2 * dist(L,Lp) -- if path(A,B) travels through Lp

   ```
   dist(L,A) + dist(L,B) = dist(A,B) + 2 * dist(L,Lp)
   dist(L,A) + dist(L,B) - dist(A,B) = 2 * dist(L,Lp)
   (dist(L,A) + dist(L,B) - dist(A,B)) / 2 = dist(L,Lp)
   ```

   The following is a conceptualization of the isolation of dist(L,Lp) happening above using the initial equality example from above. Notice how, in the end, v2's limb is highlighted exactly once and nothing else.

   ```{dot}
   graph G {
    graph[rankdir=LR]
    node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
    edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
    subgraph cluster_three {
     fontname="Courier-Bold"
     fontsize=10
     label="(path(v1,v2) + path(v2,v5) - path(v1,v5)) / 2"
     z_v0 [label=v0]
     z_v1 [label=v1]
     z_v2 [label=v2]
     z_v3 [label=v3]
     z_v4 [label=v4]
     z_v5 [label=v5]
     z_v6 [label=v6]
     z_i0 [label=i0]
     z_i1 [label=i1]
     z_i2 [label=i2]
     z_i3 [label=i3]
     z_v0 -- z_i0
     z_v1 -- z_i0
     z_i0 -- z_i1
     z_v2 -- z_i1 [color="blue", penwidth="2.5"]
     z_v3 -- z_i1
     z_i1 -- z_i2
     z_v4 -- z_i2
     z_i2 -- z_i3
     z_i3 -- z_v5
     z_i3 -- z_v6
     z_i1 [fillcolor="gray", style="filled"]
    }
    subgraph cluster_two {
     fontname="Courier-Bold"
     fontsize=10
     label="path(v1,v2) + path(v2,v5) - path(v1,v5)"
     y_v0 [label=v0]
     y_v1 [label=v1]
     y_v2 [label=v2]
     y_v3 [label=v3]
     y_v4 [label=v4]
     y_v5 [label=v5]
     y_v6 [label=v6]
     y_i0 [label=i0]
     y_i1 [label=i1]
     y_i2 [label=i2]
     y_i3 [label=i3]
     y_v0 -- y_i0
     y_v1 -- y_i0
     y_i0 -- y_i1
     y_v2 -- y_i1 [color="blue:invis:blue", penwidth="2.5"]
     y_v3 -- y_i1
     y_i1 -- y_i2
     y_v4 -- y_i2
     y_i2 -- y_i3
     y_i3 -- y_v5
     y_i3 -- y_v6
     y_i1 [fillcolor="gray", style="filled"]
    }
    subgraph cluster_one {
     fontname="Courier-Bold"
     fontsize=10
     label="path(v1,v2) + path(v2,v5)"
     x_v0 [label=v0]
     x_v1 [label=v1]
     x_v2 [label=v2]
     x_v3 [label=v3]
     x_v4 [label=v4]
     x_v5 [label=v5]
     x_v6 [label=v6]
     x_i0 [label=i0]
     x_i1 [label=i1]
     x_i2 [label=i2]
     x_i3 [label=i3]
     x_v0 -- x_i0
     x_v1 -- x_i0 [color="blue", penwidth="2.5"]
     x_i0 -- x_i1 [color="blue", penwidth="2.5"]
     x_v2 -- x_i1 [color="blue:invis:blue", penwidth="2.5"]
     x_v3 -- x_i1
     x_i1 -- x_i2 [color="blue", penwidth="2.5"]
     x_v4 -- x_i2
     x_i2 -- x_i3 [color="blue", penwidth="2.5"]
     x_i3 -- x_v5 [color="blue", penwidth="2.5"]
     x_i3 -- x_v6
     x_i1 [fillcolor="gray", style="filled"]
    }
   }
   ```

 * dist(L,A) + dist(L,B) > dist(A,B) + 2 * dist(L,Lp) -- if path(A,B) doesn't travel through Lp
   
   ```
   dist(L,A) + dist(L,B) > dist(A,B) + 2 * dist(L,Lp)
   dist(L,A) + dist(L,B) - dist(A,B) > 2 * dist(L,Lp)
   (dist(L,A) + dist(L,B) - dist(A,B)) / 2 > dist(L,Lp)
   ```

   The following is a conceptualization of the isolation of dist(L,Lp) happening above using the initial inequality example from above. Notice how, in the end, v2's limb is highlighted exactly once but other edges are also highlighted. That's why it's > instead of =.

   ```{dot}
   graph G {
    graph[rankdir=LR]
    node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
    edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
    subgraph cluster_three {
     fontname="Courier-Bold"
     fontsize=10
     label="(path(v2,v4) + path(v2,v5) - path(v4,v5)) / 2"
     z_v0 [label=v0]
     z_v1 [label=v1]
     z_v2 [label=v2]
     z_v3 [label=v3]
     z_v4 [label=v4]
     z_v5 [label=v5]
     z_v6 [label=v6]
     z_i0 [label=i0]
     z_i1 [label=i1]
     z_i2 [label=i2]
     z_i3 [label=i3]
     z_v0 -- z_i0
     z_v1 -- z_i0
     z_i0 -- z_i1
     z_v2 -- z_i1 [color="blue", penwidth="2.5"]
     z_v3 -- z_i1
     z_i1 -- z_i2 [color="blue", penwidth="2.5"]
     z_v4 -- z_i2
     z_i2 -- z_i3
     z_i3 -- z_v5
     z_i3 -- z_v6
     z_i1 [fillcolor="gray", style="filled"]
    }
    subgraph cluster_two {
     fontname="Courier-Bold"
     fontsize=10
     label="path(v2,v4) + path(v2,v5) - path(v4,v5)"
     y_v0 [label=v0]
     y_v1 [label=v1]
     y_v2 [label=v2]
     y_v3 [label=v3]
     y_v4 [label=v4]
     y_v5 [label=v5]
     y_v6 [label=v6]
     y_i0 [label=i0]
     y_i1 [label=i1]
     y_i2 [label=i2]
     y_i3 [label=i3]
     y_v0 -- y_i0
     y_v1 -- y_i0
     y_i0 -- y_i1
     y_v2 -- y_i1 [color="blue:invis:blue", penwidth="2.5"]
     y_v3 -- y_i1
     y_i1 -- y_i2 [color="blue:invis:blue", penwidth="2.5"]
     y_v4 -- y_i2
     y_i2 -- y_i3
     y_i3 -- y_v5
     y_i3 -- y_v6
     y_i1 [fillcolor="gray", style="filled"]
    }
    subgraph cluster_one {
     fontname="Courier-Bold"
     fontsize=10
     label="path(v2,v5) + path(v2,v4)"
     x_v0 [label=v0]
     x_v1 [label=v1]
     x_v2 [label=v2]
     x_v3 [label=v3]
     x_v4 [label=v4]
     x_v5 [label=v5]
     x_v6 [label=v6]
     x_i0 [label=i0]
     x_i1 [label=i1]
     x_i2 [label=i2]
     x_i3 [label=i3]
     x_v0 -- x_i0
     x_v1 -- x_i0
     x_i0 -- x_i1
     x_v2 -- x_i1 [color="blue:invis:blue", penwidth="2.5"]
     x_v3 -- x_i1
     x_i1 -- x_i2 [color="blue:invis:blue", penwidth="2.5"]
     x_v4 -- x_i2 [color="blue", penwidth="2.5"]
     x_i2 -- x_i3 [color="blue", penwidth="2.5"]
     x_i3 -- x_v5 [color="blue", penwidth="2.5"]
     x_i3 -- x_v6
     x_i1 [fillcolor="gray", style="filled"]
    }
   }
   ```

Notice the left-hand side of both solved formulas are the same: (dist(L,A) + dist(L,B) - dist(A,B)) / 2

The algorithm for finding limb length is essentially an exhaustive test. Of all leaf node pairs (L not included), the one producing the smallest left-hand side result is guaranteed to be L's limb length. Anything larger will include weights from more edges than just L's limb.

````{note}
From the book:

> Exercise Break: The algorithm proposed on the previous step computes LimbLength(j) in O(n2) time (for an n x n distance matrix). Design an algorithm that computes LimbLength(j) in O(n) time.

The answer to this is obvious now that I've gone through and reasoned about things above.

For the limb length formula to work, you need to find leaf nodes (A, B) whose path travels through leaf node L's parent (Lp). Originally, the book had you try all combinations of leaf nodes (L excluded) and take the minimum. That works, but you don't need to try all possible pairs. Instead, you can just pick any leaf (that isn't L) for A and test against every other node (that isn't L) to find B -- as with the original method, you pick the B that produces the minimum value.
   
Because a phylogenetic tree is a connected graph (a path exists between each node and all other nodes), at least 1 path will exist starting from A that travels through Lp.

```python
leaf_nodes.remove(L)  # remove L from the set
A = leaf_nodes.pop()  # removes and returns an arbitrary leaf node
B = min(leafs, key=lambda x: (dist(L, A) + dist(L, x) - dist(A, x)) / 2)
```

For example, imagine that you're trying to find v2's limb length in the following graph...

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
 subgraph cluster_one {
  fontname="Courier-Bold"
  fontsize=10
  v0 -- i0
  v1 -- i0
  i0 -- i1
  v2 -- i1
  v3 -- i1
  i1 -- i2
  v4 -- i2
  i2 -- i3
  i3 -- v5
  i3 -- v6
 }
}
```

Pick v4 as your A node, then try the formula with every other leaf node as B (except v2 because that's the node you're trying to get limb length for + v4 because that's your A node). At least one of path(A, B)'s will cross through v2's parent. Take the minimum, just as you did when you were trying every possible node pair across all leaf nodes in the graph.
````

```{output}
ch7_code/src/phylogeny/FindLimbLength.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch7}
phylogeny.FindLimbLength
v2
[0 , 13, 19, 20, 29, 40, 36]
[13, 0 , 10, 11, 20, 31, 27]
[19, 10, 0 , 11, 20, 31, 27]
[20, 11, 11, 0 , 21, 32, 28]
[29, 20, 20, 21, 0 , 17, 13]
[40, 31, 31, 32, 17, 0 , 6 ]
[36, 27, 27, 28, 13, 6 , 0 ]
```

### Test Same Subtree

`{bm} /(Algorithms\/Phylogeny\/Test Same Subtree)_TOPIC/`

```{prereq}
Algorithms/Phylogeny/Find Limb Length_TOPIC
```

**WHAT**: Splitting a simple tree on the parent of one of its leaf nodes breaks it up into several subtrees. For example, the following simple tree has been split on v2's parent, resulting in 4 different subtrees ...

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
 subgraph cluster_one {
  fontname="Courier-Bold"
  fontsize=10
  label="split on i1"
  v0 -- i0
  v1 -- i0 
  i0 -- i1 [style="dashed"]
  v2 -- i1 [style="dashed"]
  v3 -- i1 [style="dashed"]
  i1 -- i2 [style="dashed"]
  v4 -- i2
  i2 -- i3 
  i3 -- v5 
  i3 -- v6
  v0 [style="filled", fillcolor="green"]
  v1 [style="filled", fillcolor="green"]
  i0 [style="filled", fillcolor="green"]
  i1 [style="filled", fillcolor="gray"]
  v2 [style="filled", fillcolor="yellow"]
  v3 [style="filled", fillcolor="pink"]
  i2 [style="filled", fillcolor="cyan"]
  i3 [style="filled", fillcolor="cyan"]
  v4 [style="filled", fillcolor="cyan"]
  v5 [style="filled", fillcolor="cyan"]
  v6 [style="filled", fillcolor="cyan"]
 }
}
```

 * `{h}green  v0, v1, i0`
 * `{h}yellow v2`
 * `{h}pink   v3`
 * `{h}cyan   v4, i2, i3, v5, v6`


Given just the additive distance matrix for a simple tree (not the simple tree itself), determine if two *leaf nodes* belong to the same subtree had that simple tree been split on some leaf node's parent.

**WHY**: This is one of the operations required to construct the unique simple tree for an additive distance matrix.

**ALGORITHM**:

The algorithm is essentially the formulas from the limb length algorithm. Recall that those formulas are ...

 * dist(L,A) + dist(L,B) = dist(A,B) + 2 * dist(L,Lp) -- if path(A,B) travels through Lp

   ```
   dist(L,A) + dist(L,B) = dist(A,B) + 2 * dist(L,Lp)
   dist(L,A) + dist(L,B) - dist(A,B) = 2 * dist(L,Lp)
   (dist(L,A) + dist(L,B) - dist(A,B)) / 2 = dist(L,Lp)
   ```

 * dist(L,A) + dist(L,B) > dist(A,B) + 2 * dist(L,Lp) -- if path(A,B) doesn't travel through Lp
   
   ```
   dist(L,A) + dist(L,B) > dist(A,B) + 2 * dist(L,Lp)
   dist(L,A) + dist(L,B) - dist(A,B) > 2 * dist(L,Lp)
   (dist(L,A) + dist(L,B) - dist(A,B)) / 2 > dist(L,Lp)
   ```

To conceptualize how this algorithm works, consider the following simple tree and its corresponding additive distance matrix...

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
 subgraph cluster_one {
  fontname="Courier-Bold"
  fontsize=10
  v0 -- i0
  v1 -- i0
  i0 -- i1
  v2 -- i1
  v3 -- i1
  i1 -- i2
  v4 -- i2
  i2 -- i3
  i3 -- v5
  i3 -- v6
 }
}
```

|    | v0 | v1 | v2 | v3 | v4 | v5 | v6 |
|----|----|----|----|----|----|----|----|
| v0 | 0  | 13 | 19 | 20 | 29 | 40 | 36 |
| v1 | 13 | 0  | 10 | 11 | 20 | 31 | 27 |
| v2 | 19 | 10 | 0  | 11 | 20 | 31 | 27 |
| v3 | 20 | 11 | 11 | 0  | 21 | 32 | 28 |
| v4 | 29 | 20 | 20 | 21 | 0  | 17 | 13 |
| v5 | 40 | 31 | 31 | 32 | 17 | 0  | 6  |
| v6 | 36 | 27 | 27 | 28 | 13 | 6  | 0  |

Consider what happens when you break the edges on v2's parent (i1). The tree breaks into 4 distinct subtrees (colored below as green, yellow, pink, and cyan)...

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
 subgraph cluster_one {
  fontname="Courier-Bold"
  fontsize=10
  label="split on i1"
  v0 -- i0
  v1 -- i0 
  i0 -- i1 [style="dashed"]
  v2 -- i1 [style="dashed"]
  v3 -- i1 [style="dashed"]
  i1 -- i2 [style="dashed"]
  v4 -- i2
  i2 -- i3 
  i3 -- v5 
  i3 -- v6
  v0 [style="filled", fillcolor="green"]
  v1 [style="filled", fillcolor="green"]
  i0 [style="filled", fillcolor="green"]
  i1 [style="filled", fillcolor="gray"]
  v2 [style="filled", fillcolor="yellow"]
  v3 [style="filled", fillcolor="pink"]
  i2 [style="filled", fillcolor="cyan"]
  i3 [style="filled", fillcolor="cyan"]
  v4 [style="filled", fillcolor="cyan"]
  v5 [style="filled", fillcolor="cyan"]
  v6 [style="filled", fillcolor="cyan"]
 }
}
```

If the two leaf nodes chosen are ...

 * within the same subtree, the path will _never_ travel through v2's parent (i1), meaning that the second formula evaluates to true. For example, since `{h}cyan v4` and `{h}cyan v5` are within the same subset, `{h}purple path(v4,v5)` doesn't travel through v2's parent ...

   ```{dot}
   graph G {
    graph[rankdir=LR]
    node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
    edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
    subgraph cluster_two {
     fontname="Courier-Bold"
     fontsize=10
     label="dist(v4,v5) + 2 * dist(v2,i1)"
     y_v0 -- y_i0
     y_v1 -- y_i0 
     y_i0 -- y_i1
     y_v2 -- y_i1 [color="red:invis:red", penwidth="2.5"]
     y_v3 -- y_i1
     y_i1 -- y_i2
     y_v4 -- y_i2 [color="purple", penwidth="2.5"]
     y_i2 -- y_i3 [color="purple", penwidth="2.5"]
     y_i3 -- y_v5 [color="purple", penwidth="2.5"]
     y_i3 -- y_v6
     y_v0 [label= "v0", style="filled", fillcolor="green"]
     y_v1 [label= "v1", style="filled", fillcolor="green"]
     y_i0 [label= "i0", style="filled", fillcolor="green"]
     y_i1 [label= "i1", style="filled", fillcolor="gray"]
     y_v2 [label= "v2", style="filled", fillcolor="yellow"]
     y_v3 [label= "v3", style="filled", fillcolor="pink"]
     y_i2 [label= "i2", style="filled", fillcolor="cyan"]
     y_i3 [label= "i3", style="filled", fillcolor="cyan"]
     y_v4 [label= "v4", style="filled", fillcolor="cyan"]
     y_v5 [label= "v5", style="filled", fillcolor="cyan"]
     y_v6 [label= "v6", style="filled", fillcolor="cyan"]
    }
    subgraph cluster_one {
     fontname="Courier-Bold"
     fontsize=10
     label="dist(v4,v2) + dist(v5,v2)"
     x_v0 -- x_i0
     x_v1 -- x_i0 
     x_i0 -- x_i1
     x_v2 -- x_i1 [color="blue:invis:orange", penwidth="2.5"]
     x_v3 -- x_i1
     x_i1 -- x_i2 [color="blue:invis:orange", penwidth="2.5"]
     x_v4 -- x_i2 [color="blue", penwidth="2.5"]
     x_i2 -- x_i3 [color="orange", penwidth="2.5"]
     x_i3 -- x_v5 [color="orange", penwidth="2.5"]
     x_i3 -- x_v6
     x_v0 [label= "v0", style="filled", fillcolor="green"]
     x_v1 [label= "v1", style="filled", fillcolor="green"]
     x_i0 [label= "i0", style="filled", fillcolor="green"]
     x_i1 [label= "i1", style="filled", fillcolor="gray"]
     x_v2 [label= "v2", style="filled", fillcolor="yellow"]
     x_v3 [label= "v3", style="filled", fillcolor="pink"]
     x_i2 [label= "i2", style="filled", fillcolor="cyan"]
     x_i3 [label= "i3", style="filled", fillcolor="cyan"]
     x_v4 [label= "v4", style="filled", fillcolor="cyan"]
     x_v5 [label= "v5", style="filled", fillcolor="cyan"]
     x_v6 [label= "v6", style="filled", fillcolor="cyan"]
    }
   }
   ```
   
   `{h}blue dist(v2,v4)` + `{h}orange dist(v2,v5)` > `{h}purple dist(v4,v5)` + `{h}red 2 * dist(v2,i1)`

 * not within the same subtree, the path will _always_ travel through v2's parent (i1), meaning that the first formula evaluates to true. For example, since `{h}green v1` and `{h}cyan v5` are within different subsets, `{h}pink path(v1,v5)` doesn't travel through v2's parent ...

   ```{dot}
   graph G {
    graph[rankdir=LR]
    node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
    edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
    subgraph cluster_two {
     fontname="Courier-Bold"
     fontsize=10
     label="dist(v1,v5) + 2 * dist(v2,i1)"
     y_v0 [label= "v0", style="filled", fillcolor="green"]
     y_v1 [label= "v1", style="filled", fillcolor="green"]
     y_i0 [label= "i0", style="filled", fillcolor="green"]
     y_i1 [label= "i1", style="filled", fillcolor="gray"]
     y_v2 [label= "v2", style="filled", fillcolor="yellow"]
     y_v3 [label= "v3", style="filled", fillcolor="pink"]
     y_i2 [label= "i2", style="filled", fillcolor="cyan"]
     y_i3 [label= "i3", style="filled", fillcolor="cyan"]
     y_v4 [label= "v4", style="filled", fillcolor="cyan"]
     y_v5 [label= "v5", style="filled", fillcolor="cyan"]
     y_v6 [label= "v6", style="filled", fillcolor="cyan"]
     y_v0 -- y_i0
     y_v1 -- y_i0 [color="pink", penwidth="2.5"]
     y_i0 -- y_i1 [color="pink", penwidth="2.5"]
     y_v2 -- y_i1 [color="red:invis:red", penwidth="2.5"]
     y_v3 -- y_i1
     y_i1 -- y_i2 [color="pink", penwidth="2.5"]
     y_v4 -- y_i2
     y_i2 -- y_i3 [color="pink", penwidth="2.5"]
     y_i3 -- y_v5 [color="pink", penwidth="2.5"]
     y_i3 -- y_v6
     y_i1 [fillcolor="gray", style="filled"]
    }
    subgraph cluster_one {
     fontname="Courier-Bold"
     fontsize=10
     label="dist(v1,v2) + dist(v2,v5)"
     x_v0 [label= "v0", style="filled", fillcolor="green"]
     x_v1 [label= "v1", style="filled", fillcolor="green"]
     x_i0 [label= "i0", style="filled", fillcolor="green"]
     x_i1 [label= "i1", style="filled", fillcolor="gray"]
     x_v2 [label= "v2", style="filled", fillcolor="yellow"]
     x_v3 [label= "v3", style="filled", fillcolor="pink"]
     x_i2 [label= "i2", style="filled", fillcolor="cyan"]
     x_i3 [label= "i3", style="filled", fillcolor="cyan"]
     x_v4 [label= "v4", style="filled", fillcolor="cyan"]
     x_v5 [label= "v5", style="filled", fillcolor="cyan"]
     x_v6 [label= "v6", style="filled", fillcolor="cyan"]
     x_v0 -- x_i0
     x_v1 -- x_i0 [color="orange", penwidth="2.5"]
     x_i0 -- x_i1 [color="orange", penwidth="2.5"]
     x_v2 -- x_i1 [color="blue:invis:orange", penwidth="2.5"]
     x_v3 -- x_i1
     x_i1 -- x_i2 [color="blue", penwidth="2.5"]
     x_v4 -- x_i2
     x_i2 -- x_i3 [color="blue", penwidth="2.5"]
     x_i3 -- x_v5 [color="blue", penwidth="2.5"]
     x_i3 -- x_v6
     x_i1 [fillcolor="gray", style="filled"]
    }
   }
   ```
   
   `{h}orange path(v1,v2)` + `{h}blue path(v2,v5)` = `{h}pink path(v1,v5)` + `{h}red 2 * path(v2,i1)`

```{output}
ch7_code/src/phylogeny/SubtreeDetect.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch7}
phylogeny.SubtreeDetect
v2
v1 v5
[0 , 13, 19, 20, 29, 40, 36]
[13, 0 , 10, 11, 20, 31, 27]
[19, 10, 0 , 11, 20, 31, 27]
[20, 11, 11, 0 , 21, 32, 28]
[29, 20, 20, 21, 0 , 17, 13]
[40, 31, 31, 32, 17, 0 , 6 ]
[36, 27, 27, 28, 13, 6 , 0 ]
```

### Trim

`{bm} /(Algorithms\/Phylogeny\/Trim)_TOPIC/`

```{prereq}
Algorithms/Phylogeny/Tree to Additive Distance Matrix_TOPIC
Algorithms/Phylogeny/Tree to Simple Tree_TOPIC
Algorithms/Phylogeny/Additive Distance Matrix Cardinality_TOPIC
```

**WHAT**: Remove a limb from an additive distance matrix, just as it would get removed from its corresponding unique simple tree.

**WHY**: This is one of the operations required to construct the unique simple tree for an additive distance matrix.

**ALGORITHM**:

Recall that for any additive distance matrix, there exists a unique simple tree that fits that matrix. For example, the following simple tree is unique to the following distance matrix...

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
 ranksep=0.25
 subgraph cluster_rhs {
  v0 -- i0 [label=11]
  v1 -- i0 [label=2]
  i0 -- i1 [label=4]
  i1 -- v2 [label=6]
  i1 -- v3 [label=7]
 }
}
```

|    | v0 | v1 | v2 | v3 |
|----|----|----|----|----|
| v0 | 0  | 13 | 21 | 22 |
| v1 | 13 | 0  | 12 | 13 |
| v2 | 21 | 12 | 0  | 13 |
| v3 | 22 | 13 | 13 | 0  |

Trimming v2 off that simple tree would result in ...

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
 ranksep=0.25
 subgraph cluster_rhs {
  fontname="Courier-Bold"
  fontsize=10
  label="v3 trimmed"
  v0 -- i0 [label=11]
  v1 -- i0 [label=2]
  i0 -- v3 [label=11]
 }
}
```

|    | v0 | v1 | v3 |
|----|----|----|----|
| v0 | 0  | 13 | 22 |
| v1 | 13 | 0  | 13 |
| v3 | 22 | 13 | 0  |

Notice how when v2 gets trimmed off, the ...

 * simple tree merges path(i0, v2) into a single edge. Simple trees can't have nodes with degree_GRAPH 2 (train of non-branching edges not allowed).
 * additive distance matrix row and column for v3 disappear. All other leaf nodes remain with the same distances.
   
As such, removing the row and column for some leaf node in an additive distance matrix is equivalent to removing its limb from the corresponding unique simple tree then merging together any edges connected by nodes of degree_GRAPH 2.

```{output}
ch7_code/src/phylogeny/Trimmer.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch7}
phylogeny.Trimmer
v2
[0 , 13, 21, 22]
[13, 0 , 12, 13]
[21, 12, 0 , 13]
[22, 13, 13, 0 ]
```

### Bald

`{bm} /(Algorithms\/Phylogeny\/Bald)_TOPIC/`

```{prereq}
Algorithms/Phylogeny/Find Limb Length_TOPIC
```

`{bm-disable} 5'` <!-- Needs to be disabled because v3's is conflicting with 3' -->
`{bm-disable} 3'` <!-- Needs to be disabled because v5's is conflicting with 5' -->

**WHAT**: Set a limb length to 0 in an additive distance matrix, just as it would be set to 0 in its corresponding unique simple tree. Technically, a simple tree can't have edge weights that are <= 0. This is a special case, typically used as an intermediate operation of some larger algorithm.

**WHY**: This is one of the operations required to construct the unique simple tree for an additive distance matrix.

**ALGORITHM**:

Recall that for any additive distance matrix, there exists a unique simple tree that fits that matrix. For example, the following simple tree is unique to the following distance matrix...

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
 ranksep=0.25
 subgraph cluster_rhs {
  v0 -- i0 [label=11]
  v1 -- i0 [label=2]
  v2 -- i0 [label=10]
  i0 -- i2 [label=4]
  i2 -- i1 [label=3]
  i1 -- v3 [label=3]
  i1 -- v4 [label=4]
  i2 -- v5 [label=7]
 }
}
```

|    | v0 | v1 | v2 | v3 | v4 | v5 |
|----|----|----|----|----|----|----|
| v0 | 0  | 13 | 21 | 21 | 22 | 22 |
| v1 | 13 | 0  | 12 | 12 | 13 | 13 |
| v2 | 21 | 12 | 0  | 20 | 21 | 21 |
| v3 | 21 | 12 | 20 | 0  | 7  | 13 |
| v4 | 22 | 13 | 21 | 7  | 0  | 14 |
| v5 | 22 | 13 | 21 | 13 | 14 | 0  |

Setting v5's limb length to 0 (balding v5) would result in ...

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
 ranksep=0.25
 subgraph cluster_rhs {
  fontname="Courier-Bold"
  fontsize=10
  label="v5 balded"
  v0 -- i0 [label=11]
  v1 -- i0 [label=2]
  v2 -- i0 [label=10]
  i0 -- i2 [label=4]
  i2 -- i1 [label=3]
  i1 -- v3 [label=3]
  i1 -- v4 [label=4]
  i2 -- v5 [label=0 style=dashed]
 }
}
```

|    | v0 | v1 | v2 | v3 | v4 | v5 |
|----|----|----|----|----|----|----|
| v0 | 0  | 13 | 21 | 21 | 22 | 15 |
| v1 | 13 | 0  | 12 | 12 | 13 | 6  |
| v2 | 21 | 12 | 0  | 20 | 21 | 14 |
| v3 | 21 | 12 | 20 | 0  | 7  | 6  |
| v4 | 22 | 13 | 21 | 7  | 0  | 7  |
| v5 | 15 | 6  | 14 | 6  | 7  | 0  |

```{note}
Can a limb length be 0 in a simple tree? I don't think so, but the book seems to imply that it's possible. But, if the distance between the two nodes on an edge is 0, wouldn't that make them the same organism? Maybe this is just a temporary thing for this algorithm.
```

Notice how of the two distance matrices, all distances are the same except for v5's distances. Each v5 distance in the balded distance matrix is equivalent to the corresponding distance in the original distance matrix subtracted by v5's original limb length...

|    |     v0      |     v1      |     v2      |     v3      |     v4      |     v5      |
|----|-------------|-------------|-------------|-------------|-------------|-------------|
| v0 |     0       |     13      |     21      |     21      |     22      | 22 - 7 = 15 |
| v1 |     13      |     0       |     12      |     12      |     13      | 13 - 7 = 6  |
| v2 |     21      |     12      |     0       |     20      |     21      | 21 - 7 = 14 |
| v3 |     21      |     12      |     20      |     0       |     7       | 13 - 7 = 6  |
| v4 |     22      |     13      |     21      |     7       |     0       | 14 - 7 = 7  |
| v5 | 22 - 7 = 15 | 13 - 7 = 6  | 21 - 7 = 14 | 13 - 7 = 6  | 14 - 7 = 7  | 0           |

Whereas v5 was originally contributing 7 to distances, after balding it contributes 0.

As such, subtracting some leaf node's limb length from its distances in an additive distance matrix is equivalent to balding that leaf node's limb in its corresponding simple tree.

```{output}
ch7_code/src/phylogeny/Balder.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch7}
phylogeny.Balder
v5
[0,  13, 21, 21, 22, 22]
[13, 0,  12, 12, 13, 13]
[21, 12, 0,  20, 21, 21]
[21, 12, 20, 0,  7,  13]
[22, 13, 21, 7,  0,  14]
[22, 13, 21, 13, 14, 0 ]
```

`{bm-enable} 5'` <!-- Re-enabling. Needed to be disabled because v3's is conflicting with 3' -->
`{bm-enable} 3'` <!-- Re-enabling. Needed to be disabled because v5's is conflicting with 5' -->

### Un-trim Tree

`{bm} /(Algorithms\/Phylogeny\/Un-trim Tree)_TOPIC/`

```{prereq}
Algorithms/Phylogeny/Find Limb Length_TOPIC
Algorithms/Phylogeny/Test Same Subtree_TOPIC
Algorithms/Phylogeny/Trim_TOPIC
Algorithms/Phylogeny/Bald_TOPIC
```

**WHAT**: Given an ...

 1. additive distance matrix for simple tree T
 2. simple tree T with limb L `{bm-target} trimmed/trimmed distance matrix` off

... this algorithm determines where limb L should be added in the given simple tree such that it fits the additive distance matrix. For example, the following simple tree would map to the following additive distance matrix had v2's limb branched out from some specific location...

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
 ranksep=0.25
 subgraph cluster_rhs {
  fontname="Courier-Bold"
  fontsize=10
  label="v2 trimmed"
  v0 -- i0 [label=11]
  v1 -- i0 [label=2]
  i0 -- v3 [label=11]
 }
}
```

|    | v0 | v1 | v2 | v3 |
|----|----|----|----|----|
| v0 | 0  | 13 | 21 | 22 |
| v1 | 13 | 0  | 12 | 13 |
| v2 | 21 | 12 | 0  | 13 |
| v3 | 22 | 13 | 13 | 0  |

That specific location is what this algorithm determines. It could be that v2's limb needs to branch from either ...

 * an internal node ...

   ```{dot}
   graph G {
    graph[rankdir=LR]
    node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
    edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
    ranksep=0.25
    subgraph cluster_0 {
     fontname="Courier-Bold"
     fontsize=10
     label="v2 added at i0"
     v0 -- i0 [label=11]
     v1 -- i0 [label=2]
     i0 -- v2 [label="?", color=tan, penwidth=2.5]
     i0 -- v3 [label=4]
     v0 [label=v0]
     v1 [label=v1]
     v2 [label=v2, style=filled, fillcolor=tan]
     v3 [label=v3]
     i0 [label=i0]
    }
   }
   ```

 * an edge, breaking that edge into two by attaching an internal node in between...

   ```{dot}
   graph G {
    graph[rankdir=LR]
    node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
    edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
    ranksep=0.25
    subgraph cluster_0 {
     fontname="Courier-Bold"
     fontsize=10
     label="v2 added along edge(i0,v3)"
     v0 -- i0 [label=11]
     v1 -- i0 [label=2]
     i0 -- i1 [label="?"]
     i1 -- v2 [label="?", color=tan, penwidth=2.5]
     i1 -- v3 [label="?"]
     i0 [label=i0]
     i1 [label=i1, style=filled, fillcolor=tan]
     v2 [label=v2, style=filled, fillcolor=tan]
    }
   }
   ```

```{note}
Attaching a new limb to an existing leaf node is never possible because...

1. it'll turn that existing leaf node to an internal node, which doesn't make sense because in the context of phylogenetic trees leaf nodes identify known entities.
2. it will cease to be a simple tree -- simple trees can't have nodes of degree_GRAPH 2 (train of edges not allowed).
```

**WHY**: This is one of the operations required to construct the unique simple tree for an additive distance matrix.

**ALGORITHM**:

`{bm-disable} 5'` <!-- Needs to be disabled because v5's is conflicting with 5' -->

The simple tree below would fit the additive distance matrix below had v5's limb been added to it somewhere ...
   
```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
 ranksep=0.25
 subgraph cluster_rhs {
  v0 -- i0 [label=11]
  v1 -- i0 [label=2]
  v2 -- i0 [label=10]
  i0 -- i2 [label=7]
  i2 -- v3 [label=2]
  i2 -- v4 [label=4]
 }
}
```

|    | v0 | v1 | v2 | v3 | v4 | v5 |
|----|----|----|----|----|----|----|
| v0 | 0  | 13 | 21 | 21 | 22 | 22 |
| v1 | 13 | 0  | 12 | 12 | 13 | 13 |
| v2 | 21 | 12 | 0  | 20 | 21 | 21 |
| v3 | 21 | 12 | 20 | 0  | 7  | 13 |
| v4 | 22 | 13 | 21 | 7  | 0  | 14 |
| v5 | 22 | 13 | 21 | 13 | 14 | 0  |

There's enough information available in this additive distance matrix to determine ...

* v5's limb length: 7 (calculated using the limb length algorithm)
* a pair of nodes whose path travels over v5's parent: v0 and v3 (calculated using the same subset algorithm)

```{note}
Recall that same subset algorithm says that two leaf nodes in DIFFERENT subsets are guaranteed to travel over v5's parent.
```

The key to this algorithm is figuring out where along that path (v0 to v3) v5's limb (limb length of 7) should be injected. Imagine that you already had the answer in front of you: v5's limb should be added 4 units from i0 towards i2 ...

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
 ranksep=0.25
 subgraph cluster_rhs {
  fontname="Courier-Bold"
  fontsize=10
  label="v5 attached"
  v0 -- i0 [label=11]
  v1 -- i0 [label=2]
  v2 -- i0 [label=10]
  i0 -- i1 [label=4]
  i1 -- i2 [label=3]
  i2 -- v3 [label=3]
  i2 -- v4 [label=4]
  i1 -- v5 [label=7, color=tan, penwidth=2.5]
  i1 [style=filled, fillcolor=tan]
  v5 [style=filled, fillcolor=tan]
 }
}
```

Consider the answer above with v5's limb `{bm-target} balded/balded distance matrix`...

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
 ranksep=0.25
 subgraph cluster_rhs {
  fontname="Courier-Bold"
  fontsize=10
  label="v5 balded"
  v0 -- i0 [label=11]
  v1 -- i0 [label=2]
  v2 -- i0 [label=10]
  i0 -- i1 [label=4]
  i1 -- i2 [label=3]
  i2 -- v3 [label=3]
  i2 -- v4 [label=4]
  i1 -- v5 [label=0, color=tan, style=dashed, penwidth=2.5]
  i1 [style=filled, fillcolor=tan]
  v5 [style=filled, fillcolor=tan]
 }
}
```

|    | v0          | v1          | v2          | v3          | v4          | v5          |
|----|-------------|-------------|-------------|-------------|-------------|-------------|
| v0 |          0  |          13 |          21 |          21 |          22 | 22 - 7 = 15 |
| v1 |          13 |          0  |          12 |          12 |          13 | 13 - 7 = 6  |
| v2 |          21 |          12 |          0  |          20 |          21 | 21 - 7 = 14 |
| v3 |          21 |          12 |          20 |          0  |          7  | 13 - 7 = 6  |
| v4 |          22 |          13 |          21 |          7  |          0  | 14 - 7 = 7  |
| v5 | 22 - 7 = 15 | 13 - 7 = 6  | 21 - 7 = 14 | 13 - 7 = 6  | 14 - 7 = 7  |          0  |

Since v5's limb length is 0, it doesn't contribute to the distance of any path to / from v5. As such, the distance of any path to / from v5 is actually the distance to / from its parent. For example, ...

* dist(v0,v5) = dist(v0,i1) + 0 = dist(v0,i1)
* dist(v4,v5) = dist(v4,i1) + 0 = dist(v4,i1)
* dist(v2,v5) = dist(v2,i1) + 0 = dist(v2,i1)
* etc..

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
 ranksep=0.25
 subgraph cluster_rhs {
  fontname="Courier-Bold"
  fontsize=10
  label="dist(v0,v5) = dist(v0,i1) + 0 = dist(v0,i1)"
  v0 -- i0 [label=11, color="blue:invis:violet", penwidth=2.5]
  v1 -- i0 [label=2]
  v2 -- i0 [label=10]
  i0 -- i1 [label=4, color="blue:invis:violet", penwidth=2.5]
  i1 -- i2 [label=3]
  i2 -- v3 [label=3]
  i2 -- v4 [label=4]
  i1 -- v5 [label=0, color=violet, style=dashed, penwidth=2.5]
 }
}
```

Essentially, the balded distance matrix is enough to tell you that the path from v0 to v5's parent has a distance of 15. The balded tree itself isn't required.

```{output}
ch7_code/src/phylogeny/UntrimTree.py
python
# MARKDOWN_DIST_TO_PARENT\s*\n([\s\S]+)\n\s*# MARKDOWN_DIST_TO_PARENT
no_preamble
```

In the original simple tree, walking a distance of 15 on the path from v0 to v3 takes you to where v5's parent should be. Since there is no internal node there, one is first added by breaking the edge before attaching v5's limb to it ...

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
 ranksep=0.25
 subgraph cluster_rhs {
  fontname="Courier-Bold"
  fontsize=10
  label="path(v0,v3) from v0, v5 attached 15 units in"
  v0_y -- i0_y [label=11, dir=forward, color=purple, penwidth=2.5]
  v1_y -- i0_y [label=2]
  v2_y -- i0_y [label=10]
  i0_y -- i1_y [label=4, dir=forward, color=purple, penwidth=2.5]
  i1_y -- i2_y [label=3, dir=forward, color=purple, penwidth=2.5]
  i2_y -- v3_y [label=3, dir=forward, color=purple, penwidth=2.5]
  i2_y -- v4_y [label=4]
  i1_y -- v5_y [label=7, style=dashed, color=purple, penwidth=2.5]
  v0_y [label=v0]
  v1_y [label=v1]
  v2_y [label=v2]
  v3_y [label=v3]
  v4_y [label=v4]
  v5_y [label=v5]
  i0_y [label=i0]
  i1_y [label=i1, style=filled, fillcolor=gray]
  i2_y [label=i2]
  i2_y [label=i2]
  i1_y [label=i1]
 }
 subgraph cluster_lhs {
  fontname="Courier-Bold"
  fontsize=10
  label="path(v0,v3) from v0"
  v0_x -- i0_x [label=11, dir=forward, color=purple, penwidth=2.5]
  v1_x -- i0_x [label=2]
  v2_x -- i0_x [label=10]
  i0_x -- i2_x [label=7, dir=forward, color=purple, penwidth=2.5]
  i2_x -- v3_x [label=3, dir=forward, color=purple, penwidth=2.5]
  i2_x -- v4_x [label=4]
  v0_x [label=v0]
  v1_x [label=v1]
  v2_x [label=v2]
  v3_x [label=v3]
  v4_x [label=v4]
  i0_x [label=i0]
  i2_x [label=i2]
 }
}
```

Had there been an internal node already there, the limb would get attached to that existing internal node.

```{output}
ch7_code/src/phylogeny/UntrimTree.py
python
# MARKDOWN_WALK_TO_PARENT\s*\n([\s\S]+)\n\s*# MARKDOWN_WALK_TO_PARENT
no_preamble
```

```{output}
ch7_code/src/phylogeny/UntrimTree.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch7}
phylogeny.UntrimTree
[[v0,i0,11], [v1,i0,2], [v2,i0,10], [i0,i2,7], [i2,v3,3], [i2,v4,4]]
[0,  13, 21, 21, 22, 22]
[13, 0,  12, 12, 13, 13]
[21, 12, 0,  20, 21, 21]
[21, 12, 20, 0,  7,  13]
[22, 13, 21, 7,  0,  14]
[22, 13, 21, 13, 14, 0 ]
```

`{bm-enable} 5'` <!-- Re-enable 5' now that section is finished -->

### Find Neighbours

`{bm} /(Algorithms\/Phylogeny\/Find Neighbours)_TOPIC/`

```{prereq}
Algorithms/Phylogeny/Tree to Additive Distance Matrix_TOPIC
Algorithms/Phylogeny/Tree to Simple Tree_TOPIC
Algorithms/Phylogeny/Additive Distance Matrix Cardinality_TOPIC
```

**WHAT**: Given a distance matrix, if the distance matrix is ...

 * an additive distance matrix, this algorithm finds a pair of leaf nodes guaranteed to be neighbours in its corresponding unique simple tree.
 * a non-additive distance matrix (but close to being additive), this algorithm approximates a pair of leaf nodes that are likely to be neighbours.

**WHY**: This operation is required for _approximating_ a simple tree for a non-additive distance matrix.

**ALGORITHM**: 

The algorithm essentially boils down to edge counting. Consider the following example simple tree...

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
 ranksep=0.25
 fontname="Courier-Bold"
 fontsize=10
 subgraph cluster_one {
  label="original"
  v0_x -- i0_x [label=11]
  v1_x -- i0_x [label=2]
  v2_x -- i0_x [label=10]
  i0_x -- i1_x [label=4]
  i1_x -- i2_x [label=3]
  i2_x -- v3_x [label=3]
  i2_x -- v4_x [label=4]
  i1_x -- v5_x [label=7]
  v0_x [label=v0]
  v1_x [label=v1]
  v2_x [label=v2]
  v3_x [label=v3]
  v4_x [label=v4]
  v5_x [label=v5]
  i0_x [label=i0]
  i1_x [label=i1]
  i2_x [label=i2]
  i2_x [label=i2]
  i1_x [label=i1]
 }
}
```

If you were to choose a leaf node, then gather the paths from that leaf node to all other leaf nodes, the limb for ...
   
* the chosen leaf node gets encountered  `leaf_count - 1` times.
* each non-chosen leaf node gets encountered once.

```{output}
ch7_code/src/phylogeny/NeighbourJoiningMatrix_EdgeCountExplainer.py
python
# MARKDOWN_COUNT\s*\n([\s\S]+)\n\s*# MARKDOWN_COUNT
no_preamble
```

For example, given that the tree has 6 leaf nodes, `edge_count(v1)` counts v1's limb 5 times while all other limbs are counted once...

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
 ranksep=0.25
 subgraph cluster_one {
  fontname="Courier-Bold"
  fontsize=10
  label="edge_count(v1)"
  v0_x -- i0_x [label=" ", penwidth=2.5, color="#ff0300"]
  v1_x -- i0_x [label=" ", penwidth=2.5, color="#03ff00:invis:#42c000:invis:#818100:invis:#c04200:invis:#ff0300"]
  v2_x -- i0_x [label=" ", penwidth=2.5, color="#03ff00"]
  i0_x -- i1_x [label=" ", penwidth=2.5, color="#42c000:invis:#818100:invis:#c04200"]
  i1_x -- i2_x [label=" ", penwidth=2.5, color="#42c000:invis:#818100"]
  i2_x -- v3_x [label=" ", penwidth=2.5, color="#42c000"]
  i2_x -- v4_x [label=" ", penwidth=2.5, color="#818100"]
  i1_x -- v5_x [label=" ", penwidth=2.5, color="#c04200"]
  v0_x [label=v0, style=filled, fillcolor="#ff0300"]
  v1_x [label=v1, penwidth=5]
  v5_x [label=v5, style=filled, fillcolor="#c04200"]
  v4_x [label=v4, style=filled, fillcolor="#818100"]
  v3_x [label=v3, style=filled, fillcolor="#42c000"]
  v2_x [label=v2, style=filled, fillcolor="#03ff00"]
  i0_x [label=i0]
  i1_x [label=i1]
  i2_x [label=i2]
  i2_x [label=i2]
 }
}
```

|                | (i0,i1) | (i1,i2) | (v0,i0) | (v1,i0) | (v2,i0) | (v3,i2) | (v4,i2) | (v5,i1) |
|----------------|---------|---------|---------|---------|---------|---------|---------|---------|
| edge_count(v1) |    3    |    2    |    1    |    5    |    1    |    1    |    1    |    1    |

If you were to choose a pair of leaf nodes and add their `edge_count()`s together, the limb for ...
   
* each chosen leaf node gets encountered  `leaf_count` times.
* each non-chosen leaf node gets encountered twice.

```{output}
ch7_code/src/phylogeny/NeighbourJoiningMatrix_EdgeCountExplainer.py
python
# MARKDOWN_COMBINE_COUNT\s*\n([\s\S]+)\n\s*# MARKDOWN_COMBINE_COUNT
no_preamble
```

For example, `combine_edge_count(v1,v2)` counts v1's limb 6 times, v2's limb 6 times, and every other limb 2 times ...

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
 ranksep=0.25
 subgraph cluster_3 {
  fontname="Courier-Bold"
  fontsize=10
  label="combine_edge_count(v1,v2)"
  v0_x -- i0_x:n [label=" ", penwidth=2.5, color="orange:invis:purple"]
  v1_x -- i0_x [label=" ", penwidth=2.5, color="purple:invis:purple:invis:purple:invis:purple:invis:purple:invis:orange"]
  v2_x -- i0_x:s [label=" ", penwidth=2.5, color="orange:invis:orange:invis:orange:invis:orange:invis:orange:invis:purple"]
  i0_x -- i1_x [label=" ", penwidth=2.5, color="purple:invis:purple:invis:purple:invis:orange:invis:orange:invis:orange"]
  i1_x -- i2_x [label=" ", penwidth=2.5, color="purple:invis:purple:invis:orange:invis:orange"]
  i2_x -- v3_x [label=" ", penwidth=2.5, color="purple:invis:orange"]
  i2_x -- v4_x [label=" ", penwidth=2.5, color="purple:invis:orange"]
  i1_x -- v5_x [label=" ", penwidth=2.5, color="purple:invis:orange"]
  v0_x [label=v0]
  v1_x [label=v1, style=filled, fillcolor=purple]
  v2_x [label=v2, style=filled, fillcolor=orange]
  v3_x [label=v3]
  v4_x [label=v4]
  v5_x [label=v5]
  i0_x [label=i0]
  i1_x [label=i1]
  i2_x [label=i2]
  i2_x [label=i2]
  i1_x [label=i1]
 }
 subgraph cluster_1 {
  fontname="Courier-Bold"
  fontsize=10
  label="edge_count(v2)"
  v0_z -- i0_z [label=" ", penwidth=2.5, color=orange]
  v1_z -- i0_z [label=" ", penwidth=2.5, color=orange]
  v2_z -- i0_z [label=" ", penwidth=2.5, color="orange:invis:orange:invis:orange:invis:orange:invis:orange"]
  i0_z -- i1_z [label=" ", penwidth=2.5, color="orange:invis:orange:invis:orange"]
  i1_z -- i2_z [label=" ", penwidth=2.5, color="orange:invis:orange"]
  i2_z -- v3_z [label=" ", penwidth=2.5, color=orange]
  i2_z -- v4_z [label=" ", penwidth=2.5, color=orange]
  i1_z -- v5_z [label=" ", penwidth=2.5, color=orange]
  v0_z [label=v0]
  v1_z [label=v1]
  v2_z [label=v2, style=filled, fillcolor=orange]
  v3_z [label=v3]
  v4_z [label=v4]
  v5_z [label=v5]
  i0_z [label=i0]
  i1_z [label=i1]
  i2_z [label=i2]
  i2_z [label=i2]
  i1_z [label=i1]
 }
 subgraph cluster_2 {
  fontname="Courier-Bold"
  fontsize=10
  label="edge_count(v1)"
  v0_y -- i0_y [label=" ", penwidth=2.5, color=purple]
  v1_y -- i0_y [label=" ", penwidth=2.5, color="purple:invis:purple:invis:purple:invis:purple:invis:purple"]
  v2_y -- i0_y [label=" ", penwidth=2.5, color=purple]
  i0_y -- i1_y [label=" ", penwidth=2.5, color="purple:invis:purple:invis:purple"]
  i1_y -- i2_y [label=" ", penwidth=2.5, color="purple:invis:purple"]
  i2_y -- v3_y [label=" ", penwidth=2.5, color=purple]
  i2_y -- v4_y [label=" ", penwidth=2.5, color=purple]
  i1_y -- v5_y [label=" ", penwidth=2.5, color=purple]
  v0_y [label=v0]
  v1_y [label=v1, style=filled, fillcolor=purple]
  v2_y [label=v2]
  v3_y [label=v3]
  v4_y [label=v4]
  v5_y [label=v5]
  i0_y [label=i0]
  i1_y [label=i1]
  i2_y [label=i2]
  i2_y [label=i2]
  i1_y [label=i1]
 }
}
```

|                | (i0,i1) | (i1,i2) | (v0,i0) | (v1,i0) | (v2,i0) | (v3,i2) | (v4,i2) | (v5,i1) |
|----------------|---------|---------|---------|---------|---------|---------|---------|---------|
| edge_count(v1) |    3    |    2    |    1    |    5    |    1    |    1    |    1    |    1    |
| edge_count(v2) |    3    |    2    |    1    |    1    |    5    |    1    |    1    |    1    |
|                | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- |
|                |    6    |    4    |    2    |    6    |    6    |    2    |    2    |    2    |

The key to this algorithm is to normalize limb counts returned by `combine_counts()` such that each chosen limb's count equals to each non-chosen limb's count. That is, each chosen limb count needs to be reduced from `leaf_count` to 2.

To do this, each edge in the path between the chosen pair must be subtracted `leaf_count - 2` times from `combine_edge_count()`'s result.

```{output}
ch7_code/src/phylogeny/NeighbourJoiningMatrix_EdgeCountExplainer.py
python
# MARKDOWN_NORMALIZED_COMBINE_COUNT\s*\n([\s\S]+)\n\s*# MARKDOWN_NORMALIZED_COMBINE_COUNT
no_preamble
```

Continuing with the example above, the chosen pair (v1 and v2) each have a limb count of 6 while all other limbs have a count of 2. `combine_edge_count_and_normalize(v1,v2)` subtracts each edge in path(v1,v2) 4 times from the counts...

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
 ranksep=0.25
 subgraph cluster_2 {
  fontname="Courier-Bold"
  fontsize=10
  label="combine_edge_count_and_normalize(v1,v2)"
  v0_x -- i0_x [label=" ", penwidth=2.5, color="orange:invis:purple"]
  v1_x -- i0_x [label=" ", penwidth=2.5, color="purple:invis:orange"]
  v2_x -- i0_x [label=" ", penwidth=2.5, color="orange:invis:purple"]
  i0_x -- i1_x [label=" ", penwidth=2.5, color="purple:invis:purple:invis:purple:invis:orange:invis:orange:invis:orange"]
  i1_x -- i2_x [label=" ", penwidth=2.5, color="purple:invis:purple:invis:orange:invis:orange"]
  i2_x -- v3_x [label=" ", penwidth=2.5, color="purple:invis:orange"]
  i2_x -- v4_x [label=" ", penwidth=2.5, color="purple:invis:orange"]
  i1_x -- v5_x [label=" ", penwidth=2.5, color="purple:invis:orange"]
  v0_x [label=v0]
  v1_x [label=v1, style=filled, fillcolor=purple]
  v2_x [label=v2, style=filled, fillcolor=orange]
  v3_x [label=v3]
  v4_x [label=v4]
  v5_x [label=v5]
  i0_x [label=i0]
  i1_x [label=i1]
  i2_x [label=i2]
  i2_x [label=i2]
  i1_x [label=i1]
 }
 subgraph cluster_1 {
  fontname="Courier-Bold"
  fontsize=10
  label="combine_edge_count(v1,v2)"
  v0_y -- i0_y:n [label=" ", penwidth=2.5, color="orange:invis:purple"]
  v1_y -- i0_y [label=" ", penwidth=2.5, color="purple:invis:purple:invis:purple:invis:purple:invis:purple:invis:orange"]
  v2_y -- i0_y:s [label=" ", penwidth=2.5, color="orange:invis:orange:invis:orange:invis:orange:invis:orange:invis:purple"]
  i0_y -- i1_y [label=" ", penwidth=2.5, color="purple:invis:purple:invis:purple:invis:orange:invis:orange:invis:orange"]
  i1_y -- i2_y [label=" ", penwidth=2.5, color="purple:invis:purple:invis:orange:invis:orange"]
  i2_y -- v3_y [label=" ", penwidth=2.5, color="purple:invis:orange"]
  i2_y -- v4_y [label=" ", penwidth=2.5, color="purple:invis:orange"]
  i1_y -- v5_y [label=" ", penwidth=2.5, color="purple:invis:orange"]
  v0_y [label=v0]
  v1_y [label=v1, style=filled, fillcolor=purple]
  v2_y [label=v2, style=filled, fillcolor=orange]
  v3_y [label=v3]
  v4_y [label=v4]
  v5_y [label=v5]
  i0_y [label=i0]
  i1_y [label=i1]
  i2_y [label=i2]
  i2_y [label=i2]
  i1_y [label=i1]
 }
}
```

|                  | (i0,i1) | (i1,i2) | (v0,i0) | (v1,i0) | (v2,i0) | (v3,i2) | (v4,i2) | (v5,i1) |
|------------------|---------|---------|---------|---------|---------|---------|---------|---------|
| edge_count(v1)   |    3    |    2    |    1    |    5    |    1    |    1    |    1    |    1    |
| edge_count(v2)   |    3    |    2    |    1    |    1    |    5    |    1    |    1    |    1    |
| -4 * path(v1,v2) |         |         |         |   -4    |   -4    |         |         |         |
|                  | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- |
|                  |    6    |    4    |    2    |    2    |    2    |    2    |    2    |    2    |

The insight here is that, if the chosen pair ...

 * are neighbours, the path between them will only ever have 2 edges: their limbs.
 * aren't neighbours, the path between them will have more than 2 edges: their limbs AND internal edges.
    
```{output}
ch7_code/src/phylogeny/NeighbourJoiningMatrix_EdgeCountExplainer.py
python
# MARKDOWN_NEIGHBOUR_PATH_EDGE_COUNT_CHECK\s*\n([\s\S]+)\n\s*# MARKDOWN_NEIGHBOUR_PATH_EDGE_COUNT_CHECK
no_preamble
```

For example, ...

 * v1 and v2 are neighbours and as such path(v1,v2) contains only their limbs: [(v1,i0), (v2,i0)].
 * v1 and v5 aren't neighbours and as such path(v1,v5) has internal edges in addition to their limbs: [(v1,i0), (i0,i1), (v5,i1)].

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
 ranksep=0.25
 subgraph cluster_2 {
  fontname="Courier-Bold"
  fontsize=10
  label="path(v1,v5)"
  v0_x -- i0_x [label=" "]
  v1_x -- i0_x [label=" ", penwidth=2.5, color=red]
  v2_x -- i0_x [label=" "]
  i0_x -- i1_x [label=" ", penwidth=2.5, color=red]
  i1_x -- i2_x [label=" "]
  i2_x -- v3_x [label=" "]
  i2_x -- v4_x [label=" "]
  i1_x -- v5_x [label=" ", penwidth=2.5, color=red]
  v0_x [label=v0]
  v1_x [label=v1, style=filled, fillcolor=gray]
  v2_x [label=v2]
  v3_x [label=v3]
  v4_x [label=v4]
  v5_x [label=v5, style=filled, fillcolor=gray]
  i0_x [label=i0]
  i1_x [label=i1]
  i2_x [label=i2]
  i2_x [label=i2]
  i1_x [label=i1]
 }
 subgraph cluster_1 {
  fontname="Courier-Bold"
  fontsize=10
  label="path(v1,v2)"
  v0_y -- i0_y [label=" "]
  v1_y -- i0_y [label=" ", penwidth=2.5, color=red]
  v2_y -- i0_y [label=" ", penwidth=2.5, color=red]
  i0_y -- i1_y [label=" "]
  i1_y -- i2_y [label=" "]
  i2_y -- v3_y [label=" "]
  i2_y -- v4_y [label=" "]
  i1_y -- v5_y [label=" "]
  v0_y [label=v0]
  v1_y [label=v1, style=filled, fillcolor=gray]
  v2_y [label=v2, style=filled, fillcolor=gray]
  v3_y [label=v3]
  v4_y [label=v4]
  v5_y [label=v5]
  i0_y [label=i0]
  i1_y [label=i1]
  i2_y [label=i2]
  i2_y [label=i2]
  i1_y [label=i1]
 }
}
```

That means if the pair aren't neighbours, `combine_edge_count_and_normalize()` will normalize limb counts for the pair in addition to reducing internal edge counts. For example, since v1 and v5 aren't neighbours, `combine_edge_count_and_normalize(v1,v5)` subtracts 4 from the limb counts of v1 and v5 as well as (i0,i1)'s count ...

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
 ranksep=0.25
 subgraph cluster_4 {
  fontname="Courier-Bold"
  fontsize=10
  label="combine_edge_count_and_normalize(v1,v5)"
  v0_w -- i0_w [label=" ", penwidth=2.5, color="pink:invis:tan"]
  v1_w -- i0_w [label=" ", penwidth=2.5, color="pink:invis:tan"]
  v2_w -- i0_w [label=" ", penwidth=2.5, color="tan:invis:pink"]
  i0_w -- i1_w [label=" ", penwidth=2.5, color="pink:invis:tan"]
  i1_w -- i2_w [label=" ", penwidth=2.5, color="pink:invis:pink:invis:tan:invis:tan"]
  i2_w -- v3_w [label=" ", penwidth=2.5, color="pink:invis:tan"]
  i2_w -- v4_w [label=" ", penwidth=2.5, color="pink:invis:tan"]
  i1_w -- v5_w [label=" ", penwidth=2.5, color="pink:invis:tan"]
  v0_w [label=v0]
  v1_w [label=v1, style=filled, fillcolor=pink]
  v2_w [label=v2]
  v3_w [label=v3]
  v4_w [label=v4]
  v5_w [label=v5, style=filled, fillcolor=tan]
  i0_w [label=i0]
  i1_w [label=i1]
  i2_w [label=i2]
  i2_w [label=i2]
  i1_w [label=i1]
 }
 subgraph cluster_3 {
  fontname="Courier-Bold"
  fontsize=10
  label="combine_edge_count(v1,v5)"
  v0_x -- i0_x:n [label=" ", penwidth=2.5, color="pink:invis:tan"]
  v1_x -- i0_x [label=" ", penwidth=2.5, color="pink:invis:pink:invis:pink:invis:pink:invis:pink:invis:tan"]
  v2_x -- i0_x:s [label=" ", penwidth=2.5, color="tan:invis:pink"]
  i0_x -- i1_x [label=" ", penwidth=2.5, color="pink:invis:pink:invis:pink:invis:tan:invis:tan:invis:tan"]
  i1_x -- i2_x [label=" ", penwidth=2.5, color="pink:invis:pink:invis:tan:invis:tan"]
  i2_x -- v3_x [label=" ", penwidth=2.5, color="pink:invis:tan"]
  i2_x -- v4_x [label=" ", penwidth=2.5, color="pink:invis:tan"]
  i1_x:n -- v5_x [label=" ", penwidth=2.5, color="pink:invis:tan:invis:tan:invis:tan:invis:tan:invis:tan"]
  v0_x [label=v0]
  v1_x [label=v1, style=filled, fillcolor=pink]
  v2_x [label=v2]
  v3_x [label=v3]
  v4_x [label=v4]
  v5_x [label=v5, style=filled, fillcolor=tan]
  i0_x [label=i0]
  i1_x [label=i1]
  i2_x [label=i2]
  i2_x [label=i2]
  i1_x [label=i1]
 }
 subgraph cluster_1 {
  fontname="Courier-Bold"
  fontsize=10
  label="edge_count(v5)"
  v0_z -- i0_z [label=" ", penwidth=2.5, color=tan]
  v1_z -- i0_z [label=" ", penwidth=2.5, color=tan]
  v2_z -- i0_z [label=" ", penwidth=2.5, color=tan]
  i0_z -- i1_z [label=" ", penwidth=2.5, color="tan:invis:tan:invis:tan"]
  i1_z -- i2_z [label=" ", penwidth=2.5, color="tan:invis:tan"]
  i2_z -- v3_z [label=" ", penwidth=2.5, color=tan]
  i2_z -- v4_z [label=" ", penwidth=2.5, color=tan]
  i1_z -- v5_z [label=" ", penwidth=2.5, color="tan:invis:tan:invis:tan:invis:tan:invis:tan"]
  v0_z [label=v0]
  v1_z [label=v1]
  v2_z [label=v2]
  v3_z [label=v3]
  v4_z [label=v4]
  v5_z [label=v5, style=filled, fillcolor=tan]
  i0_z [label=i0]
  i1_z [label=i1]
  i2_z [label=i2]
  i2_z [label=i2]
  i1_z [label=i1]
 }
 subgraph cluster_2 {
  fontname="Courier-Bold"
  fontsize=10
  label="edge_count(v1)"
  v0_y -- i0_y [label=" ", penwidth=2.5, color=pink]
  v1_y -- i0_y [label=" ", penwidth=2.5, color="pink:invis:pink:invis:pink:invis:pink:invis:pink"]
  v2_y -- i0_y [label=" ", penwidth=2.5, color=pink]
  i0_y -- i1_y [label=" ", penwidth=2.5, color="pink:invis:pink:invis:pink"]
  i1_y -- i2_y [label=" ", penwidth=2.5, color="pink:invis:pink"]
  i2_y -- v3_y [label=" ", penwidth=2.5, color=pink]
  i2_y -- v4_y [label=" ", penwidth=2.5, color=pink]
  i1_y -- v5_y [label=" ", penwidth=2.5, color=pink]
  v0_y [label=v0]
  v1_y [label=v1, style=filled, fillcolor=pink]
  v2_y [label=v2]
  v3_y [label=v3]
  v4_y [label=v4]
  v5_y [label=v5]
  i0_y [label=i0]
  i1_y [label=i1]
  i2_y [label=i2]
  i2_y [label=i2]
  i1_y [label=i1]
 }
}
```

|                  | (i0,i1) | (i1,i2) | (v0,i0) | (v1,i0) | (v2,i0) | (v3,i2) | (v4,i2) | (v5,i1) |
|------------------|---------|---------|---------|---------|---------|---------|---------|---------|
| edge_count(v1)   |    3    |    2    |    1    |    5    |    1    |    1    |    1    |    1    |
| edge_count(v5)   |    3    |    2    |    1    |    1    |    1    |    1    |    1    |    5    |
| -4 * path(v1,v5) |   -4    |         |         |   -4    |         |         |         |   -4    |
|                  | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- |
|                  |    2    |    4    |    2    |    2    |    2    |    2    |    2    |    2    |

Notice how (i0,i1) was reduced to 2 in the example above. It turns out that any internal edges in the path between the chosen pair get reduced to a count of 2, just like the chosen pair's limb counts.

```{output}
ch7_code/src/phylogeny/NeighbourJoiningMatrix_EdgeCountExplainer.py
python
# MARKDOWN_REDUCE_TO_2_TEST\s*\n([\s\S]+)\n\s*# MARKDOWN_REDUCE_TO_2_TEST
no_preamble
```
   
To understand why, consider what's happening in the example. For `edge_count(v1)`, notice how the count of each internal edge is consistent with the number of leaf nodes it leads to ...

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
 ranksep=0.25
 subgraph cluster_one {
  fontname="Courier-Bold"
  fontsize=10
  label="edge_count(v1)"
  v0_x -- i0_x [label=" ", penwidth=2.5, color="#ff0300"]
  v1_x -- i0_x [label=" ", penwidth=2.5, color="#03ff00:invis:#42c000:invis:#818100:invis:#c04200:invis:#ff0300"]
  v2_x -- i0_x [label=" ", penwidth=2.5, color="#03ff00"]
  i0_x -- i1_x [label=" ", penwidth=2.5, color="#42c000:invis:#818100:invis:#c04200"]
  i1_x -- i2_x [label=" ", penwidth=2.5, color="#42c000:invis:#818100"]
  i2_x -- v3_x [label=" ", penwidth=2.5, color="#42c000"]
  i2_x -- v4_x [label=" ", penwidth=2.5, color="#818100"]
  i1_x -- v5_x [label=" ", penwidth=2.5, color="#c04200"]
  v0_x [label=v0, style=filled, fillcolor="#ff0300"]
  v1_x [label=v1, penwidth=5]
  v5_x [label=v5, style=filled, fillcolor="#c04200"]
  v4_x [label=v4, style=filled, fillcolor="#818100"]
  v3_x [label=v3, style=filled, fillcolor="#42c000"]
  v2_x [label=v2, style=filled, fillcolor="#03ff00"]
  i0_x [label=i0]
  i1_x [label=i1]
  i2_x [label=i2]
  i2_x [label=i2]
 }
}
```

That is, `edge_count(v1)` counts the internal edge ...

* (i0,i1) 3 times, which is the number of nodes it leads to: [v5, v4, v3].
* (i1,i2) 2 times, which is the number of nodes it leads to: [v4, v3].
   
Breaking an internal edge divides a tree into two sub-trees. In the case of (i1,i2), the tree separates into two sub-trees where the...
   
* i1 side has 4 leaf nodes: [v0, v1, v2, v5].
* i2 side has 2 leaf nodes: [v4, v3].

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
 ranksep=0.25
 subgraph cluster_one {
  fontname="Courier-Bold"
  fontsize=10
  label="sub-trees separated by (i1,i2)"
  v0_x -- i0_x [label=" ", color=red]
  v1_x -- i0_x [label=" ", color=red]
  v2_x -- i0_x [label=" ", color=red]
  i0_x -- i1_x [label=" ", color=red]
  i1_x -- i2_x [label=" ", style=dashed]
  i2_x -- v3_x [label=" ", color=blue]
  i2_x -- v4_x [label=" ", color=blue]
  i1_x -- v5_x [label=" ", color=red]
  v0_x [label=v0, color=red]
  v1_x [label=v1, color=red]
  v2_x [label=v2, color=red]
  v3_x [label=v3, color=blue]
  v4_x [label=v4, color=blue]
  v5_x [label=v5, color=red]
  i0_x [label=i0, color=red]
  i1_x [label=i1, color=red]
  i2_x [label=i2, color=blue]
  i2_x [label=i2, color=blue]
 }
}
```

Running `edge_count()` for any leaf node on the...

* i1 side will count (i1,i2) exactly 2 times (the number of leaf nodes on the i2 side).
* i2 side will count (i1,i2) exactly 4 times (the number of leaf nodes on the i1 side).

For example, since ...
   
* v0 is on the i1 side, `edge_count(v0)` counts (i1,i2) 2 times.
* v1 is on the i1 side, `edge_count(v1)` counts (i1,i2) 2 times.
* v2 is on the i1 side, `edge_count(v2)` counts (i1,i2) 2 times.
* v3 is on the i2 side, `edge_count(v3)` counts (i1,i2) 4 times.
* v4 is on the i2 side, `edge_count(v4)` counts (i1,i2) 4 times.
* v5 is on the i1 side, `edge_count(v5)` counts (i1,i2) 2 times.

```{output}
ch7_code/src/phylogeny/NeighbourJoiningMatrix_EdgeCountExplainer.py
python
# MARKDOWN_SEGREGATE_BY_EDGE\s*\n([\s\S]+)\n\s*# MARKDOWN_SEGREGATE_BY_EDGE
no_preamble
```

If the chosen pair are on opposite sides, `combine_edge_count()` will count (i1,i2) 6 times, which is the same number of times that the chosen pair's limbs get counted (the number of leaf nodes in the tree). For example, `combine_edge_count(v1,v3)` counts (i1,i2) 6 times, because v1 sits on the i1 side (adds 2 to the count) and v3 sits on the i2 side (adds 4 to the count)...

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
 ranksep=0.25
 subgraph cluster_3 {
  fontname="Courier-Bold"
  fontsize=10
  label="combine_edge_count(v1,v3)"
  v0_x -- i0_x:n [label=" ", penwidth=2.5, color="orange:invis:brown"]
  v1_x -- i0_x [label=" ", penwidth=2.5, color="orange:invis:orange:invis:orange:invis:orange:invis:orange:invis:brown"]
  v2_x -- i0_x:s [label=" ", penwidth=2.5, color="brown:invis:orange"]
  i0_x -- i1_x [label=" ", penwidth=2.5, color="orange:invis:orange:invis:orange:invis:brown:invis:brown:invis:brown"]
  i1_x -- i2_x [label=" ", penwidth=2.5, color="orange:invis:orange:invis:brown:invis:brown:invis:brown:invis:brown"]
  i2_x -- v3_x [label=" ", penwidth=2.5, color="orange:invis:brown:invis:brown:invis:brown:invis:brown:invis:brown"]
  i2_x:n -- v4_x [label=" ", penwidth=2.5, color="brown:invis:orange"]
  i1_x:n -- v5_x [label=" ", penwidth=2.5, color="brown:invis:orange"]
  v0_x [label=v0]
  v1_x [label=v1, style=filled, fillcolor=orange]
  v2_x [label=v2]
  v3_x [label=v3, style=filled, fillcolor=brown]
  v4_x [label=v4]
  v5_x [label=v5]
  i0_x [label=i0]
  i1_x [label=i1]
  i2_x [label=i2]
  i2_x [label=i2]
 }
 subgraph cluster_1 {
  fontname="Courier-Bold"
  fontsize=10
  label="edge_count(v3)"
  v0_z -- i0_z [label=" ", penwidth=2.5, color=brown]
  v1_z -- i0_z [label=" ", penwidth=2.5, color=brown]
  v2_z -- i0_z [label=" ", penwidth=2.5, color=brown]
  i0_z -- i1_z [label=" ", penwidth=2.5, color="brown:invis:brown:invis:brown"]
  i1_z -- i2_z [label=" ", penwidth=2.5, color="brown:invis:brown:invis:brown:invis:brown"]
  i2_z -- v3_z [label=" ", penwidth=2.5, color="brown:invis:brown:invis:brown:invis:brown:invis:brown"]
  i2_z -- v4_z [label=" ", penwidth=2.5, color=brown]
  i1_z -- v5_z [label=" ", penwidth=2.5, color=brown]
  v0_z [label=v0]
  v1_z [label=v1]
  v2_z [label=v2]
  v3_z [label=v3, style=filled, fillcolor=brown]
  v4_z [label=v4]
  v5_z [label=v5]
  i0_z [label=i0]
  i1_z [label=i1]
  i2_z [label=i2]
  i2_z [label=i2]
 }
 subgraph cluster_2 {
  fontname="Courier-Bold"
  fontsize=10
  label="edge_count(v1)"
  v0_y -- i0_y [label=" ", penwidth=2.5, color=orange]
  v1_y -- i0_y [label=" ", penwidth=2.5, color="orange:invis:orange:invis:orange:invis:orange:invis:orange"]
  v2_y -- i0_y [label=" ", penwidth=2.5, color=orange]
  i0_y -- i1_y [label=" ", penwidth=2.5, color="orange:invis:orange:invis:orange"]
  i1_y -- i2_y [label=" ", penwidth=2.5, color="orange:invis:orange"]
  i2_y -- v3_y [label=" ", penwidth=2.5, color=orange]
  i2_y -- v4_y [label=" ", penwidth=2.5, color=orange]
  i1_y -- v5_y [label=" ", penwidth=2.5, color=orange]
  v0_y [label=v0]
  v1_y [label=v1, style=filled, fillcolor=orange]
  v2_y [label=v2]
  v3_y [label=v3]
  v4_y [label=v4]
  v5_y [label=v5]
  i0_y [label=i0]
  i1_y [label=i1]
  i2_y [label=i2]
  i2_y [label=i2]
 }
}
```

|                | (i0,i1) | (i1,i2) | (v0,i0) | (v1,i0) | (v2,i0) | (v3,i2) | (v4,i2) | (v5,i1) |
|----------------|---------|---------|---------|---------|---------|---------|---------|---------|
| edge_count(v1) |    3    |    2    |    1    |    5    |    1    |    1    |    1    |    1    |
| edge_count(v3) |    3    |    4    |    1    |    1    |    1    |    5    |    1    |    1    |
|                | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- |
|                |    6    |    6    |    2    |    6    |    2    |    6    |    2    |    2    |

This will always be the case for any simple tree: If a chosen pair aren't neighbours, the path between them always travels over at least one internal edge. `combine_edge_count()` will always count each edge in the path `leaf_count` times. In the above example, path(v1,v3) travels over internal edges (i0,i1) and (i1,i2) and as such both those edges in addition to the limbs of v1 and v3 have a count of 6.
   
Just like how `combine_edge_count_and_normalize()` reduces the counts of the chosen pair's limbs to 2, so will it reduce the count of the internal edges in the path of the chosen pair to 2. That is, all edges in the path between the chosen pair get reduced to a count of 2.

For example, path(v1,v3) has the edges [(v1,i0), (i0,i1), (i1, i2), (v3, i2)]. `combine_edge_count_and_normalize(v1,v3)` reduces the count of each edge in that path to 2 ...

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
 ranksep=0.25
 subgraph cluster_5 {
  fontname="Courier-Bold"
  fontsize=10
  label="combine_edge_count_and_normalize(v1,v3)"
  v0_x -- i0_x [label=" ", penwidth=2.5, color="orange:invis:brown"]
  v1_x -- i0_x [label=" ", penwidth=2.5, color="orange:invis:brown"]
  v2_x -- i0_x [label=" ", penwidth=2.5, color="brown:invis:orange"]
  i0_x -- i1_x [label=" ", penwidth=2.5, color="orange:invis:brown"]
  i1_x -- i2_x [label=" ", penwidth=2.5, color="orange:invis:brown"]
  i2_x -- v3_x [label=" ", penwidth=2.5, color="orange:invis:brown"]
  i2_x -- v4_x [label=" ", penwidth=2.5, color="orange:invis:brown"]
  i1_x -- v5_x [label=" ", penwidth=2.5, color="brown:invis:orange"]
  v0_x [label=v0]
  v1_x [label=v1, style=filled, fillcolor=orange]
  v2_x [label=v2]
  v3_x [label=v3, style=filled, fillcolor=brown]
  v4_x [label=v4]
  v5_x [label=v5]
  i0_x [label=i0]
  i1_x [label=i1]
  i2_x [label=i2]
  i2_x [label=i2]
  i1_x [label=i1]
 }
 subgraph cluster_3 {
  fontname="Courier-Bold"
  fontsize=10
  label="combine_edge_count(v1,v3)"
  v0_y -- i0_y:n [label=" ", penwidth=2.5, color="orange:invis:brown"]
  v1_y -- i0_y [label=" ", penwidth=2.5, color="orange:invis:orange:invis:orange:invis:orange:invis:orange:invis:brown"]
  v2_y -- i0_y:s [label=" ", penwidth=2.5, color="brown:invis:orange"]
  i0_y -- i1_y [label=" ", penwidth=2.5, color="orange:invis:orange:invis:orange:invis:brown:invis:brown:invis:brown"]
  i1_y -- i2_y [label=" ", penwidth=2.5, color="orange:invis:orange:invis:brown:invis:brown:invis:brown:invis:brown"]
  i2_y -- v3_y [label=" ", penwidth=2.5, color="orange:invis:brown:invis:brown:invis:brown:invis:brown:invis:brown"]
  i2_y:n -- v4_y [label=" ", penwidth=2.5, color="brown:invis:orange"]
  i1_y:n -- v5_y [label=" ", penwidth=2.5, color="brown:invis:orange"]
  v0_y [label=v0]
  v1_y [label=v1, style=filled, fillcolor=orange]
  v2_y [label=v2]
  v3_y [label=v3, style=filled, fillcolor=brown]
  v4_y [label=v4]
  v5_y [label=v5]
  i0_y [label=i0]
  i1_y [label=i1]
  i2_y [label=i2]
  i2_y [label=i2]
 }
}
```

|                  | (i0,i1) | (i1,i2) | (v0,i0) | (v1,i0) | (v2,i0) | (v3,i2) | (v4,i2) | (v5,i1) |
|------------------|---------|---------|---------|---------|---------|---------|---------|---------|
| edge_count(v1)   |    3    |    2    |    1    |    5    |    1    |    1    |    1    |    1    |
| edge_count(v3)   |    3    |    4    |    1    |    1    |    1    |    5    |    1    |    1    |
| -4 * path(v1,v3) |   -4    |   -4    |         |   -4    |         |   -4    |         |         |
|                  | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- |
|                  |    2    |    2    |    2    |    2    |    2    |    2    |    2    |    2    |

The ultimate idea is that, for any leaf node pair in a simple tree, `combine_edge_count_and_normalize()` will have a count of ...

* 2 for limbs.
* \> 2 for internal edges.
   
In other words, internal edges are the only differentiating factor in `combine_edge_count_and_normalize()`'s result. Non-neighbouring pairs will have certain internal edge counts reduced to 2 while neighbouring pairs keep internal edge counts > 2. In a ...
   
* worst case scenario, all internal edges get reduced to 2.
* best case scenario, all internal edges are kept > 2.
   
The pair with the highest total count is guaranteed to be a neighbouring pair because lesser total counts may have had their internal edges reduced.

```{output}
ch7_code/src/phylogeny/NeighbourJoiningMatrix_EdgeCountExplainer.py
python
# MARKDOWN_NEIGHBOUR_DETECT\s*\n([\s\S]+)\n\s*# MARKDOWN_NEIGHBOUR_DETECT
```

```{note}
The graph in the example run below is the same as the graph used above. It may look different because node positions may have shifted around.
```

```{ch7}
phylogeny.NeighbourJoiningMatrix_EdgeCountExplainer
[[v0,i0], [v1,i0], [v2,i0], [i0,i1], [i1,i2], [i2,v3], [i2,v4], [i1,v5]]
```

This same reasoning is applied to edge weights. That is, instead of just counting edges, the reasoning works the same if you were to multiply edge weights by those counts.

In the edge count version of this algorithm, `edge_count()` gets the paths from a leaf node to all other leaf nodes and counts up the number of times each edge is encountered. In the edge weight multiplicity version, instead of counting how many times each edge gets encountered, each time an edge gets encountered it increases the multiplicity of its weight ...

```{output}
ch7_code/src/phylogeny/NeighbourJoiningMatrix_EdgeMultiplicityExplainer.py
python
# MARKDOWN_EDGE_MULTIPLE\s*\n([\s\S]+)\n\s*# MARKDOWN_EDGE_MULTIPLE
no_preamble
```

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
 fontname="Courier-Bold"
 fontsize=10
 ranksep=0.25
 subgraph cluster_three {
  label="edge_multiple(v1)"
  v0_z -- i0_z [label="(1*11)\n11"]
  v1_z -- i0_z [label="(5*2)\n10"]
  v2_z -- i0_z [label="(1*10)\n10"]
  i0_z -- i1_z [label="(3*4)\n12"]
  i1_z -- i2_z [label="(2*3)\n6"]
  i2_z -- v3_z [label="(1*3)\n3"]
  i2_z -- v4_z [label="(1*4)\n4"]
  i1_z -- v5_z [label="(1*7)\n7"]
  v0_z [label=v0]
  v1_z [label=v1, penwidth=5]
  v2_z [label=v2]
  v3_z [label=v3]
  v4_z [label=v4]
  v5_z [label=v5]
  i0_z [label=i0]
  i1_z [label=i1]
  i2_z [label=i2]
  i2_z [label=i2]
  i1_z [label=i1]
 }
 subgraph cluster_two {
  label="edge_count(v1)"
  v0_y -- i0_y [label=" ", penwidth=2.5, color="#ff0300"]
  v1_y -- i0_y [label=" ", penwidth=2.5, color="#03ff00:invis:#42c000:invis:#818100:invis:#c04200:invis:#ff0300"]
  v2_y -- i0_y [label=" ", penwidth=2.5, color="#03ff00"]
  i0_y -- i1_y [label=" ", penwidth=2.5, color="#42c000:invis:#818100:invis:#c04200"]
  i1_y -- i2_y [label=" ", penwidth=2.5, color="#42c000:invis:#818100"]
  i2_y -- v3_y [label=" ", penwidth=2.5, color="#42c000"]
  i2_y -- v4_y [label=" ", penwidth=2.5, color="#818100"]
  i1_y -- v5_y [label=" ", penwidth=2.5, color="#c04200"]
  v0_y [label=v0, style=filled, fillcolor="#ff0300"]
  v1_y [label=v1, penwidth=5]
  v5_y [label=v5, style=filled, fillcolor="#c04200"]
  v4_y [label=v4, style=filled, fillcolor="#818100"]
  v3_y [label=v3, style=filled, fillcolor="#42c000"]
  v2_y [label=v2, style=filled, fillcolor="#03ff00"]
  i0_y [label=i0]
  i1_y [label=i1]
  i2_y [label=i2]
  i2_y [label=i2]
 }
 subgraph cluster_one {
  label="original"
  v0_x -- i0_x [label=11]
  v1_x -- i0_x [label=2]
  v2_x -- i0_x [label=10]
  i0_x -- i1_x [label=4]
  i1_x -- i2_x [label=3]
  i2_x -- v3_x [label=3]
  i2_x -- v4_x [label=4]
  i1_x -- v5_x [label=7]
  v0_x [label=v0]
  v1_x [label=v1]
  v2_x [label=v2]
  v3_x [label=v3]
  v4_x [label=v4]
  v5_x [label=v5]
  i0_x [label=i0]
  i1_x [label=i1]
  i2_x [label=i2]
  i2_x [label=i2]
  i1_x [label=i1]
 }
}
```

|                   | (i0,i1) | (i1,i2) | (v0,i0)  | (v1,i0) | (v2,i0)  | (v3,i2) | (v4,i2) | (v5,i1) |
|-------------------|---------|---------|----------|---------|----------|---------|---------|---------|
| edge_count(v1)    | 3       | 2       | 1        | 5       | 1        | 1       | 1       | 1       |
| edge_multiple(v1) | 3\*4=12 | 2\*3=6  | 1\*11=11 | 5\*2=10 | 1\*10=10 | 1\*3=3  | 1\*4=4  | 1\*7=7  |

Similarly, where in the edge count version `combine_edge_count()` adds together the `edge_count()`s for two leaf nodes, the edge weight multiplicity version should add together the `edge_multiple()`s for two leaf nodes instead...

```{output}
ch7_code/src/phylogeny/NeighbourJoiningMatrix_EdgeMultiplicityExplainer.py
python
# MARKDOWN_COMBINE_EDGE_MULTIPLE\s*\n([\s\S]+)\n\s*# MARKDOWN_COMBINE_EDGE_MULTIPLE
no_preamble
```

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
 ranksep=0.25
 fontname="Courier-Bold"
 fontsize=10
 subgraph cluster_three {
  label="combine_edge_multiple(v1,v2)"
  v0_z -- i0_z [label="(2*11)\n22"]
  v1_z -- i0_z [label="(6*2)\n12"]
  v2_z -- i0_z [label="(6*10)\n60"]
  i0_z -- i1_z [label="(6*4)\n24"]
  i1_z -- i2_z [label="(4*3)\n12"]
  i2_z -- v3_z [label="(2*3)\n6"]
  i2_z -- v4_z [label="(2*4)\n8"]
  i1_z -- v5_z [label="(2*7)\n14"]
  v0_z [label=v0]
  v1_z [label=v1, penwidth=5]
  v2_z [label=v2, penwidth=5]
  v3_z [label=v3]
  v4_z [label=v4]
  v5_z [label=v5]
  i0_z [label=i0]
  i1_z [label=i1]
  i2_z [label=i2]
  i2_z [label=i2]
  i1_z [label=i1]
 }
 subgraph cluster_two {
  label="combine_edge_count(v1,v2)"
  v0_y -- i0_y:n [label=" ", penwidth=2.5, color="orange:invis:purple"]
  v1_y -- i0_y [label=" ", penwidth=2.5, color="purple:invis:purple:invis:purple:invis:purple:invis:purple:invis:orange"]
  v2_y -- i0_y:s [label=" ", penwidth=2.5, color="orange:invis:orange:invis:orange:invis:orange:invis:orange:invis:purple"]
  i0_y -- i1_y [label=" ", penwidth=2.5, color="purple:invis:purple:invis:purple:invis:orange:invis:orange:invis:orange"]
  i1_y -- i2_y [label=" ", penwidth=2.5, color="purple:invis:purple:invis:orange:invis:orange"]
  i2_y -- v3_y [label=" ", penwidth=2.5, color="purple:invis:orange"]
  i2_y -- v4_y [label=" ", penwidth=2.5, color="purple:invis:orange"]
  i1_y -- v5_y [label=" ", penwidth=2.5, color="purple:invis:orange"]
  v0_y [label=v0]
  v1_y [label=v1, style=filled, fillcolor=purple]
  v2_y [label=v2, style=filled, fillcolor=orange]
  v3_y [label=v3]
  v4_y [label=v4]
  v5_y [label=v5]
  i0_y [label=i0]
  i1_y [label=i1]
  i2_y [label=i2]
  i2_y [label=i2]
  i1_y [label=i1]
 }
}
```

|                           | (i0,i1) | (i1,i2) | (v0,i0)  | (v1,i0) | (v2,i0)  | (v3,i2) | (v4,i2) | (v5,i1) |
|---------------------------|---------|---------|----------|---------|----------|---------|---------|---------|
| combine_edge_count(v1)    | 6       | 4       | 2        | 6       | 6        | 2       | 2       | 2       |
| combine_edge_multiple(v1) | 6\*4=24 | 4\*3=12 | 2\*11=22 | 6\*2=20 | 6\*10=60 | 2\*3=6  | 2\*4=8  | 2\*7=14 |

Similarly, where in the edge count version `combine_edge_count_and_normalize()` reduces all limbs and possibly some internal edges from `combine_edge_count()` to a count of 2, the edge multiplicity version reduces weights for those same limbs and edges to a multiple of 2...

```{output}
ch7_code/src/phylogeny/NeighbourJoiningMatrix_EdgeMultiplicityExplainer.py
python
# MARKDOWN_NORMALIZED_COMBINE_EDGE_MULTIPLE\s*\n([\s\S]+)\n\s*# MARKDOWN_NORMALIZED_COMBINE_EDGE_MULTIPLE
no_preamble
```

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
 ranksep=0.25
 fontname="Courier-Bold"
 fontsize=10
 subgraph cluster_three {
  label="combine_edge_multiple_and_normalize(v1,v2)"
  v0_z -- i0_z [label="(2*11)\n22"]
  v1_z -- i0_z [label="(2*2)\n4"]
  v2_z -- i0_z [label="(2*10)\n20"]
  i0_z -- i1_z [label="(6*4)\n24"]
  i1_z -- i2_z [label="(4*3)\n12"]
  i2_z -- v3_z [label="(2*3)\n6"]
  i2_z -- v4_z [label="(2*4)\n8"]
  i1_z -- v5_z [label="(2*7)\n14"]
  v0_z [label=v0]
  v1_z [label=v1, penwidth=5]
  v2_z [label=v2, penwidth=5]
  v3_z [label=v3]
  v4_z [label=v4]
  v5_z [label=v5]
  i0_z [label=i0]
  i1_z [label=i1]
  i2_z [label=i2]
  i2_z [label=i2]
  i1_z [label=i1]
 }
 subgraph cluster_two {
  label="combine_edge_count_and_normalize(v1,v2)"
  v0_y -- i0_y [label=" ", penwidth=2.5, color="orange:invis:purple"]
  v1_y -- i0_y [label=" ", penwidth=2.5, color="purple:invis:orange"]
  v2_y -- i0_y [label=" ", penwidth=2.5, color="orange:invis:purple"]
  i0_y -- i1_y [label=" ", penwidth=2.5, color="purple:invis:purple:invis:purple:invis:orange:invis:orange:invis:orange"]
  i1_y -- i2_y [label=" ", penwidth=2.5, color="purple:invis:purple:invis:orange:invis:orange"]
  i2_y -- v3_y [label=" ", penwidth=2.5, color="purple:invis:orange"]
  i2_y -- v4_y [label=" ", penwidth=2.5, color="purple:invis:orange"]
  i1_y -- v5_y [label=" ", penwidth=2.5, color="purple:invis:orange"]
  v0_y [label=v0]
  v1_y [label=v1, style=filled, fillcolor=purple]
  v2_y [label=v2, style=filled, fillcolor=orange]
  v3_y [label=v3]
  v4_y [label=v4]
  v5_y [label=v5]
  i0_y [label=i0]
  i1_y [label=i1]
  i2_y [label=i2]
  i2_y [label=i2]
  i1_y [label=i1]
 }
}
```

|                                            | (i0,i1) | (i1,i2) | (v0,i0)  | (v1,i0) | (v2,i0)  | (v3,i2) | (v4,i2) | (v5,i1) |
|--------------------------------------------|---------|---------|----------|---------|----------|---------|---------|---------|
| combine_edge_count_and_normalize(v1,v2)    | 6       | 4       | 2        | 2       | 2        | 2       | 2       | 2       |
| combine_edge_multiple_and_normalize(v1,v2) | 6\*4=24 | 4\*3=12 | 2\*11=22 | 2\*2=20 | 2\*10=60 | 2\*3=6  | 2\*4=8  | 2\*7=14 |

Similar to `combine_edge_count_and_normalize()`, for any leaf node pair in a simple tree `combine_edge_multiple_and_normalize()` will have an *edge weight multiple* of ...

* 2 for limbs.
* \> 2 for internal edges.
   
In other words, internal edge weight multiples are the only differentiating factor in `combine_edge_multiple_and_normalize()`'s result. Non-neighbouring pairs will have certain internal edge weight multiples reduced to 2 while neighbouring pairs keep internal edge weight multiples > 2. In a ...
   
* worst case scenario, all internal edge weight multiples get reduced to 2.
* best case scenario, all internal edge weight multiples are kept > 2.
   
The pair with the highest combined multiple is guaranteed to be a neighbouring pair because lesser combined multiples may have had their internal edge multiples reduced.

````{note}
Still confused?

Given a simple tree, `combine_edge_multiple(A, B)` will make it so that...

 * limb A has a weight multiplicity of `leaf_count`.
 * limb B has a weight multiplicity of `leaf_count`.
 * other limbs each have a weight multiplicity of 2.
 * internal edges each have a weight multiplicity of > 2.
 
For example, the following diagrams visualize edge weight multiplicities produced by `combine_edge_multiple()` for various pairs in a 4 leaf simple tree. Note how the selected pair's limbs have a multiplicity of 4, other limbs have a multiplicity of 2, and internal edges have a multiplicity of 4...

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
 ranksep=0.25
 subgraph cluster_4 {
  label="combine_edge_multiple(v1,v2)"
  fontname="Courier-Bold"
  fontsize=10
  v0_z -- i0_z [label=" ", penwidth=2.5, color="purple:invis:orange"]
  v1_z -- i0_z [label=" ", penwidth=2.5, color="purple:invis:purple:invis:purple:invis:orange"]
  i0_z -- i1_z [label=" ", penwidth=2.5, color="purple:invis:purple:invis:orange:invis:orange"]
  i1_z -- v2_z [label=" ", penwidth=2.5, color="purple:invis:orange"]
  i1_z -- v3_z [label=" ", penwidth=2.5, color="purple:invis:orange:invis:orange:invis:orange"]
  v0_z [label=v0]
  v1_z [label=v1, style=filled, fillcolor=purple]
  v2_z [label=v2]
  v3_z [label=v3, style=filled, fillcolor=orange]
  i0_z [label=i0]
  i1_z [label=i1]
 }
 subgraph cluster_3 {
  label="combine_edge_multiple(v1,v2)"
  fontname="Courier-Bold"
  fontsize=10
  v0_y -- i0_y [label=" ", penwidth=2.5, color="purple:invis:orange"]
  v1_y -- i0_y [label=" ", penwidth=2.5, color="purple:invis:purple:invis:purple:invis:orange"]
  i0_y -- i1_y [label=" ", penwidth=2.5, color="purple:invis:purple:invis:orange:invis:orange"]
  i1_y -- v2_y [label=" ", penwidth=2.5, color="purple:invis:orange:invis:orange:invis:orange"]
  i1_y -- v3_y [label=" ", penwidth=2.5, color="orange:invis:purple"]
  v0_y [label=v0]
  v1_y [label=v1, style=filled, fillcolor=purple]
  v2_y [label=v2, style=filled, fillcolor=orange]
  v3_y [label=v3]
  i0_y [label=i0]
  i1_y [label=i1]
 }
 subgraph cluster_2 {
  label="combine_edge_multiple(v0,v1)"
  fontname="Courier-Bold"
  fontsize=10
  v0_x -- i0_x [label=" ", penwidth=2.5, color="purple:invis:orange:invis:orange:invis:orange"]
  v1_x -- i0_x [label=" ", penwidth=2.5, color="purple:invis:purple:invis:purple:invis:orange"]
  i0_x -- i1_x [label=" ", penwidth=2.5, color="purple:invis:purple:invis:orange:invis:orange"]
  i1_x -- v2_x [label=" ", penwidth=2.5, color="purple:invis:orange"]
  i1_x -- v3_x [label=" ", penwidth=2.5, color="purple:invis:orange"]
  v0_x [label=v0, style=filled, fillcolor=orange]
  v1_x [label=v1, style=filled, fillcolor=purple]
  v2_x [label=v2]
  v3_x [label=v3]
  i0_x [label=i0]
  i1_x [label=i1]
 }
}
```

`combine_edge_multiple_and_normalize(A, B)` normalizes these multiplicities such that ...

 * limb A's weight multiplicity reduces to 2.
 * limb B's weight multiplicity reduces to 2.
 * other limbs keep their weight multiplicities at 2.
 * if the pair are neighbours, each internal edge multiplicity remains at > 2.
 * if the pair aren't neighbours, at least one internal edge multiplicity reduces to 2 while others remain at > 2.

|                        | limb multiplicity | internal edge multiplicity   |
|------------------------|-------------------|------------------------------|
| neighbouring pairs     |      all = 2      |          all >= 2            |
| non-neighbouring pairs |      all = 2      | at least one = 2, others > 2 | 

Since limbs always contribute the same regardless of whether the pair is neighbouring or not (2*weight), they can be ignored. That leaves internal edge contributions as the only thing differentiating between neighbouring and non-neighbouring pairs.

A simple tree with 2 or more leaf nodes is guaranteed to have at least 1 neighbouring pair. The pair producing the largest result is the one with maxed out contributions from its multiplied internal edges weights, meaning that none of those contributions were for internal edges reduced to 2\*weight. Lesser results MAY be lesser because normalization reduced some of their internal edge weights to 2\*weight, but the largest result you know for certain has all of its internal edge weights > 2\*weight.
````

```{output}
ch7_code/src/phylogeny/NeighbourJoiningMatrix_EdgeMultiplicityExplainer.py
python
# MARKDOWN_NEIGHBOUR_DETECT\s*\n([\s\S]+)\n\s*# MARKDOWN_NEIGHBOUR_DETECT
```

```{note}
The graph in the example run below is the same as the graph used above. It may look different because node positions may have shifted around.
```

```{ch7}
phylogeny.NeighbourJoiningMatrix_EdgeMultiplicityExplainer
[[v0,i0,11], [v1,i0,2], [v2,i0,10], [i0,i1,4], [i1,i2,3], [i2,v3,3], [i2,v4,4], [i1,v5,7]]
```

The matrix produced in the example above is called a neighbour joining matrix. The summation of `combine_edge_multiple_and_normalize()` performed in each matrix slot is rewritable as a set of addition and subtraction operations between leaf node distances. For example, recall that `combine_edge_multiple_and_normalize(v1,v2)` in the example graph breaks down to `edge_multiple(v1) + edge_multiple(v2) - (leaf_count - 2) * path(v1,v2)`. The sum of ...
  
* `edge_multiple(v1)` breaks down to...

  ```
  dist(v1,v0) + dist(v1,v2) + dist(v1,v3) + dist(v1,v4) + dist(v1,v5)
  ```
* `edge_multiple(v2)` breaks down to...

  ```
  dist(v2,v0) + dist(v2,v1) + dist(v2,v3) + dist(v2,v4) + dist(v2,v5)
  ```
* `combine_edge_multiple(v2)` is simply the sum of the two summations above:

  ```
  dist(v1,v0) + dist(v1,v2) + dist(v1,v3) + dist(v1,v4) + dist(v1,v5) +
  dist(v2,v0) + dist(v2,v1) + dist(v2,v3) + dist(v2,v4) + dist(v2,v5)
  ```
*  `combine_edge_multiple_and_normalize(v1,v2)` is simply the above summation but with `dist(v1,v2)` removed 4 times:

  ```
  dist(v1,v0) + dist(v1,v2) + dist(v1,v3) + dist(v1,v4) + dist(v1,v5) +
  dist(v2,v0) + dist(v2,v1) + dist(v2,v3) + dist(v2,v4) + dist(v2,v5) -
  dist(v1,v2) - dist(v1,v2) - dist(v1,v2) - dist(v1,v2)
  ```

Since only leaf node distances are being used in the summation calculation, a distance matrix suffices as the input. The actual simple tree isn't required.

```{output}
ch7_code/src/phylogeny/NeighbourJoiningMatrix.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch7}
phylogeny.NeighbourJoiningMatrix
[[0,13,21,21,22,22],[13,0,12,12,13,13],[21,12,0,20,21,21],[21,12,20,0,7,13],[22,13,21,7,0,14],[22,13,21,13,14,0]]
```

### Find Neighbour Limb Lengths

`{bm} /(Algorithms\/Phylogeny\/Find Neighbour Limb Lengths)_TOPIC/`

```{prereq}
Algorithms/Phylogeny/Find Limb Length_TOPIC
```

**WHAT**: Given a distance matrix and a pair of leaf nodes identified as being neighbours, if the distance matrix is ...

 * an additive distance matrix, this algorithm finds the limb lengths of those neighbours.
 * a non-additive distance matrix (but close to being additive), this algorithm approximates the limb lengths of those neighbours.

**WHY**: This operation is required for _approximating_ a simple tree for a non-additive distance matrix.

Recall that the standard limb length finding algorithm determines the limb length of L by testing distances between leaf nodes to deduce a pair whose path crosses over L's parent. That won't work here because non-additive distance matrices have inconsistent distances -- non-additive means no tree exists that fits its distances.

#### Average Algorithm

`{bm} /(Algorithms\/Phylogeny\/Find Neighbour Limb Lengths\/Average Algorithm)_TOPIC/`

**ALGORITHM**: 

The algorithm is an extension of the standard limb length finding algorithm, essentially running the same computation multiple times and averaging out the results. For example, v1 and v2 are neighbours in the following simple tree...

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
 ranksep=0.25
 fontname="Courier-Bold"
 fontsize=10
 subgraph cluster_one {
  label="original"
  v0_x -- i0_x [label=11]
  v1_x -- i0_x [label=2]
  v2_x -- i0_x [label=10]
  i0_x -- i1_x [label=4]
  i1_x -- i2_x [label=3]
  i2_x -- v3_x [label=3]
  i2_x -- v4_x [label=4]
  i1_x -- v5_x [label=7]
  v0_x [label=v0]
  v1_x [label=v1]
  v2_x [label=v2]
  v3_x [label=v3]
  v4_x [label=v4]
  v5_x [label=v5]
  i0_x [label=i0]
  i1_x [label=i1]
  i2_x [label=i2]
  i2_x [label=i2]
  i1_x [label=i1]
 }
}
```

Since they're neighbours, they share the same parent node, meaning that the path from...

 * v1 to any other leaf node travels over v2's parent.
 * v2 to any other leaf node travels over v1's parent.

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
 ranksep=0.25
 subgraph cluster_one {
  fontname="Courier-Bold"
  fontsize=10
  label="path from v1 to all other nodes"
  v0_x -- i0_x [label=" ", penwidth=2.5, color="#ff0300"]
  v1_x -- i0_x [label=" ", penwidth=2.5, color="#03ff00:invis:#42c000:invis:#818100:invis:#c04200:invis:#ff0300"]
  v2_x -- i0_x [label=" ", penwidth=2.5, color="#03ff00"]
  i0_x -- i1_x [label=" ", penwidth=2.5, color="#42c000:invis:#818100:invis:#c04200"]
  i1_x -- i2_x [label=" ", penwidth=2.5, color="#42c000:invis:#818100"]
  i2_x -- v3_x [label=" ", penwidth=2.5, color="#42c000"]
  i2_x -- v4_x [label=" ", penwidth=2.5, color="#818100"]
  i1_x -- v5_x [label=" ", penwidth=2.5, color="#c04200"]
  v0_x [label=v0, style=filled, fillcolor="#ff0300"]
  v1_x [label=v1, penwidth=5]
  v5_x [label=v5, style=filled, fillcolor="#c04200"]
  v4_x [label=v4, style=filled, fillcolor="#818100"]
  v3_x [label=v3, style=filled, fillcolor="#42c000"]
  v2_x [label=v2, style=filled, fillcolor="#03ff00", penwidth=5]
  i0_x [label=i0, style=filled, fillcolor="gray"]
  i1_x [label=i1]
  i2_x [label=i2]
  i2_x [label=i2]
 }
}
```

Recall that to find the limb length for L, the standard limb length algorithm had to perform a minimum test to find a pair of leaf nodes whose path travelled over the L's parent. Since this algorithm takes in two _neighbouring_ leaf nodes, that test isn't required here. The path from L's neighbour to every other node always travels over L's parent.

Since the path from L's neighbour to every other node always travels over L's parent, the core computation from the standard algorithm is performed multiple times and averaged to produce an approximate limb length: 0.5 * (dist(L,N) + dist(L,X) - dist(N,X)),  where ...

 * N is L's neighbour.
 * X is a leaf node that isn't L or N.
 
The averaging makes it so that if the input distance matrix were ...

 * additive, it'd produce the correct limb length.
 * non-additive, it'd approximate a limb length that's probably good enough (assuming the distance matrix is close to being additive).

```{note}
Still confused? Think about it like this: When the distance matrix is non-additive, each X has a different "view" of what the limb length should be. You're averaging their views to get a single limb length value.
```

```{output}
ch7_code/src/phylogeny/FindNeighbourLimbLengths.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch7}
phylogeny.FindNeighbourLimbLengths
v1
v2
[0,  13, 21, 21, 22, 22]
[13, 0,  12, 12, 13, 13]
[21, 12, 0,  20, 21, 21]
[21, 12, 20, 0,  7,  13]
[22, 13, 21, 7,  0,  14]
[22, 13, 21, 13, 14, 0 ]
```

#### Optimized Average Algorithm

`{bm} /(Algorithms\/Phylogeny\/Find Neighbour Limb Lengths\/Optimized Average Algorithm)_TOPIC/`

```{prereq}
Algorithms/Phylogeny/Find Neighbour Limb Lengths/Average Algorithm_TOPIC
```

**ALGORITHM**: 

The unoptimized algorithm performs the computation once for each leaf node in the pair. This is inefficient in that it's repeating a lot of the same operations twice. This algorithm removes a lot of that duplicate work.

The unoptimized algorithm maps to the formula ...

```{kt}
\frac{1}{n-2} \cdot \sum_{k \isin S-\{l1,l2\}}{\frac{D_{l1,l2} + D_{l1,k} - D_{l2,k}}{2}}
```

... where ...

 * l1 and l2 are the neighbouring leaf nodes,
 * S is the set of leaf nodes in the distance matrix,
 * n is the size of S.

Just like the code, the formula removes l1 and l2 from the set of leaf nodes (S) for the average's summation. The number of leaf nodes (n) is subtracted by 2 for the average's division because l1 and l2 aren't included. To optimize, consider what happens when you re-organize the formula as follows...

 1. Break up the division in the summation...

    ```{kt}
    \frac{1}{n-2} \cdot \sum_{k \isin S-\{l1,l2\}}{(\frac{D_{l1,l2}}{2} + \frac{D_{l1,k}}{2} - \frac{D_{l2,k}}{2})}
    ```

 1. Pull out `{kt} \frac{D_{l1,l2}}{2}` as a term of its own...

    ```{kt}
    \frac{D_{l1,l2}}{2} + \frac{1}{n-2} \cdot \sum_{k \isin S-\{l1,l2\}}{(\frac{D_{l1,k}}{2} - \frac{D_{l2,k}}{2})}
    ```
    
    ```{note}
    Confused about what's happening above? Think about it like this...
    
    * mean([0+0.5, 0+1, 0+0.25]) = 0.833 = 0+mean([0.5, 1, 0.25])
    * mean([1+0.5, 1+1, 1+0.25]) = 1.833 = 1+mean([0.5, 1, 0.25])
    * mean([2+0.5, 2+1, 2+0.25]) = 2.833 = 2+mean([0.5, 1, 0.25])
    * mean([3+0.5, 3+1, 3+0.25]) = 3.833 = 3+mean([0.5, 1, 0.25])
    * ...
    
    If you're including some constant amount for each element in the averaging, the result of the average will include that constant amount. In the case above, `{kt} \frac{D_{l1,l2}}{2}` is a     constant being added at each element of the average.
    ```

 1. Combine the terms in the summation back together ...

    ```{kt}
    \frac{D_{l1,l2}}{2} + \frac{1}{n-2} \cdot \sum_{k \isin S-\{l1,l2\}}{\frac{D_{l1,k} - D_{l2,k}}{2}}
    ```

 1. Factor out `{kt} \frac{1}{2}` from the entire equation...

    ```{kt}
    \frac{1}{2} \cdot (D_{l1,l2} + \frac{1}{n-2} \cdot \sum_{k \isin S-\{l1,l2\}}{D_{l1,k} - D_{l2,k}})
    ```

    ```{note}
    Confused about what's happening above? It's just distributing and pulling out. For example, given the formula 5/2 + x*(3/2 + 5/2 + 9/2) ...

    1. 5/2 + 3x/2 + 5x/2 + 9x/2 -- distribute x
    1. 1/2 * (5 + 3x + 5x + 9x) -- all terms are divided by 2 now, so pull out 1/2
    1. 1/2 * (5 + x*(3 + 5 + 9)) -- pull x back out
    ```

 1. Break up the summation into two simpler summations ...
    
    ```{kt}
    \frac{1}{2} \cdot (D_{l1,l2} + \frac{1}{n-2} \cdot (\sum_{k \isin S-\{l1,l2\}}{D_{l1,k}} - \sum_{k \isin S-\{l1,l2\}}{D_{l2,k}}))
    ```

    ```{note}
    Confused about what's happening above? Think about it like this...

    (9-1)+(8-2)+(7-3) = 9+8+7-1-2-3 = 24+(-6) = 24-6 = sum([9,8,7])-sum([1,2,3])

    It's just re-ordering the operations so that it can be represented as two sums. It's perfectly valid.
    ```

The above formula calculates the limb length for l1. To instead find the formula for l2, just swap l1 and l2 ...

```{kt}
len(l1) = \frac{1}{2} \cdot (D_{l1,l2} + \frac{1}{n-2} \cdot (\sum_{k \isin S-\{l1,l2\}}{D_{l1,k}} - \sum_{k \isin S-\{l1,l2\}}{D_{l2,k}}))
\\[0.5em]
len(l2) = \frac{1}{2} \cdot (D_{l2,l1} + \frac{1}{n-2} \cdot (\sum_{k \isin S-\{l2,l1\}}{D_{l2,k}} - \sum_{k \isin S-\{l2,l1\}}{D_{l1,k}}))
```

Note how the two are almost exactly the same. `{kt} D_{l1,l2} = D_{l2,l1}`, and `{kt} S-\{l1,l2\} = S-\{l2,l1\}`, and both summations are still there. The only exception is the order in which the summations are being subtracted ...

```{kt}
len(l1) = \frac{1}{2} \cdot (D_{l1,l2} + \frac{1}{n-2} \cdot (\textcolor{#7f7f00}{\sum_{k \isin S-\{l1,l2\}}{D_{l1,k}}} - \textcolor{#007f7f}{\sum_{k \isin S-\{l1,l2\}}{D_{l2,k}}}))
\\[0.5em]
len(l2) = \frac{1}{2} \cdot (D_{l1,l2} + \frac{1}{n-2} \cdot (\textcolor{#007f7f}{\sum_{k \isin S-\{l1,l2\}}{D_{l2,k}}} - \textcolor{#7f7f00}{\sum_{k \isin S-\{l1,l2\}}{D_{l1,k}}}))
```

Consider what happens when you re-organize the formula for l2 as follows...

 1. Convert the summation subtraction to an addition of a negative...

    ```{kt}
    len(l2) = \frac{1}{2} \cdot (D_{l1,l2} + \frac{1}{n-2} \cdot (\textcolor{#007f7f}{\sum_{k \isin S-\{l1,l2\}}{D_{l2,k}}} + (- \textcolor{#7f7f00}{\sum_{k \isin S-\{l1,l2\}}{D_{l1,k}}}))
    ```

 1. Swap the order of the summation addition...
  
    ```{kt}
    len(l2) = \frac{1}{2} \cdot (D_{l1,l2} + \frac{1}{n-2} \cdot (-\textcolor{#007f7f}{\sum_{k \isin S-\{l1,l2\}}{D_{l1,k}}} + \textcolor{#7f7f00}{\sum_{k \isin S-\{l1,l2\}}{D_{l2,k}}}))
    ```

 1. Factor out -1 from summation addition ...

    ```{kt}
    len(l2) = \frac{1}{2} \cdot (D_{l1,l2} + \frac{1}{n-2} \cdot -1 \cdot (\textcolor{#7f7f00}{\sum_{k \isin S-\{l1,l2\}}{D_{l1,k}}} - \textcolor{#007f7f}{\sum_{k \isin S-\{l1,l2\}}{D_{l2,k}}}))
    ```

 1. Simplify ...

    ```{kt}
    len(l2) = \frac{1}{2} \cdot (D_{l1,l2} + - \frac{1}{n-2} \cdot (\textcolor{#7f7f00}{\sum_{k \isin S-\{l1,l2\}}{D_{l1,k}}} - \textcolor{#007f7f}{\sum_{k \isin S-\{l1,l2\}}{D_{l2,k}}}))
    ```

 1. Simplify ...

    ```{kt}
    len(l2) = \frac{1}{2} \cdot (D_{l1,l2} - \frac{1}{n-2} \cdot (\textcolor{#7f7f00}{\sum_{k \isin S-\{l1,l2\}}{D_{l1,k}}} - \textcolor{#007f7f}{\sum_{k \isin S-\{l1,l2\}}{D_{l2,k}}}))
    ```

After this reorganization, the two match up almost exactly. The only difference is that an addition has been swapped to a subtraction...

```{kt}
len(l1) = \frac{1}{2} \cdot (D_{l1,l2} \textcolor{#ff0000}{+} \frac{1}{n-2} \cdot (\textcolor{#7f7f00}{\sum_{k \isin S-\{l1,l2\}}{D_{l1,k}}} - \textcolor{#007f7f}{\sum_{k \isin S-\{l1,l2\}}{D_{l2,k}}}))
\\[0.5em]
len(l2) = \frac{1}{2} \cdot (D_{l1,l2} \textcolor{#ff0000}{-} \frac{1}{n-2} \cdot (\textcolor{#7f7f00}{\sum_{k \isin S-\{l2,l1\}}{D_{l1,k}}} - \textcolor{#007f7f}{\sum_{k \isin S-\{l2,l1\}}{D_{l2,k}}}))
```

The point of this optimization is that the summation calculation only needs to be performed once. The result can be used to calculate the limb length for both of the neighbouring leaf nodes...

```{kt}
res = \frac{1}{n-2} \cdot (\textcolor{#7f7f00}{\sum_{k \isin S-\{l1,l2\}}{D_{l1,k}}} - \textcolor{#007f7f}{\sum_{k \isin S-\{l1,l2\}}{D_{l2,k}}})
\\[0.5em]
len(l1) = \frac{1}{2} \cdot (D_{l1,l2} \textcolor{#ff0000}{+} res)
\\[0.5em]
len(l2) = \frac{1}{2} \cdot (D_{l1,l2} \textcolor{#ff0000}{-} res)
```

Depending on your architecture, this optimized form can be tweaked even further for better performance. Recall that the distance of anything to itself is always zero, meaning that...

 * `{kt} D_{l1,l1}` doesn't contribute anything to the first summation.
 * `{kt} D_{l2,l2}` doesn't contribute anything to the second summation.
 
If the cost of removing those terms from their respective summations is higher than the cost of keeping them in (adding that extra 0), you might as well not remove them...

```{kt}
res = \frac{1}{n-2} \cdot (\textcolor{#7f7f00}{\sum_{k \isin S-\{l2\}}{D_{l1,k}}} - \textcolor{#007f7f}{\sum_{k \isin S-\{l1\}}{D_{l2,k}}})
\\[0.5em]
len(l1) = \frac{1}{2} \cdot (D_{l1,l2} \textcolor{#ff0000}{+} res)
\\[0.5em]
len(l2) = \frac{1}{2} \cdot (D_{l1,l2} \textcolor{#ff0000}{-} res)
```

Similarly, removing both l2 from the first summation and l1 from the second summation doesn't actually change the result. The first summation will add `{kt} D_{l1,l2}` but the second summation will remove `{kt} D_{l1,l2}`, resulting in an overall contribution of 0. If the cost of removing those terms from their respective summations is higher than the cost of keeping them in, you might as well not remove them...

```{kt}
res = \frac{1}{n-2} \cdot (\textcolor{#7f7f00}{\sum_{k \isin S}{D_{l1,k}}} - \textcolor{#007f7f}{\sum_{k \isin S}{D_{l2,k}}})
\\[0.5em]
len(l1) = \frac{1}{2} \cdot (D_{l1,l2} \textcolor{#ff0000}{+} res)
\\[0.5em]
len(l2) = \frac{1}{2} \cdot (D_{l1,l2} \textcolor{#ff0000}{-} res)
```

```{output}
ch7_code/src/phylogeny/FindNeighbourLimbLengths_Optimized.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch7}
phylogeny.FindNeighbourLimbLengths_Optimized
v1
v2
[0,  13, 21, 21, 22, 22]
[13, 0,  12, 12, 13, 13]
[21, 12, 0,  20, 21, 21]
[21, 12, 20, 0,  7,  13]
[22, 13, 21, 7,  0,  14]
[22, 13, 21, 13, 14, 0 ]
```

### Expose Neighbour Parent

`{bm} /(Algorithms\/Phylogeny\/Expose Neighbour Parent)_TOPIC/`

```{prereq}
Algorithms/Phylogeny/Bald_TOPIC
Algorithms/Phylogeny/Find Neighbour Limb Lengths/Average Algorithm_TOPIC
```

**WHAT**: Given a distance matrix and a pair of leaf nodes identified as being neighbours, this algorithm removes those neighbours from the distance matrix and brings their parent to the forefront (as a leaf node in the distance matrix). If the distance matrix is a non-additive distance matrix (but close to being additive), this algorithm approximates the shared parent.

**WHY**: This operation is required for _approximating_ a simple tree for a non-additive distance matrix.

#### Average Algorithm

`{bm} /(Algorithms\/Phylogeny\/Merge Neighbours\/Average Algorithm)_TOPIC/`

**ALGORITHM**: 

At a high-level, this algorithm essentially boils down to balding each of the neighbours and combining them together. For example, v0 and v1 are neighbours in the following simple tree...

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
 ranksep=0.25
 fontname="Courier-Bold"
 fontsize=10
 subgraph cluster_one {
  label="original"
  v0_x -- i0_x [label=11]
  v1_x -- i0_x [label=2]
  v2_x -- i0_x [label=10]
  i0_x -- i1_x [label=4]
  i1_x -- i2_x [label=3]
  i2_x -- v3_x [label=3]
  i2_x -- v4_x [label=4]
  i1_x -- v5_x [label=7]
  v0_x [label=v0]
  v1_x [label=v1]
  v2_x [label=v2]
  v3_x [label=v3]
  v4_x [label=v4]
  v5_x [label=v5]
  i0_x [label=i0]
  i1_x [label=i1]
  i2_x [label=i2]
  i2_x [label=i2]
  i1_x [label=i1]
 }
}
```

|    | v0 | v1 | v2 | v3 | v4 | v5 |
|----|----|----|----|----|----|----|
| v0 | 0  | 13 | 21 | 21 | 22 | 22 |
| v1 | 13 | 0  | 12 | 12 | 13 | 13 |
| v2 | 21 | 12 | 0  | 20 | 21 | 21 |
| v3 | 21 | 12 | 20 | 0  | 7  | 13 |
| v4 | 22 | 13 | 21 | 7  | 0  | 14 |
| v5 | 22 | 13 | 21 | 13 | 14 | 0  |

Balding both v0 and v1 results in ...

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
 ranksep=0.25
 fontname="Courier-Bold"
 fontsize=10
 subgraph cluster_one {
  label="v0 and v1 balded"
  v0_x -- i0_x [label=0, style=dashed]
  v1_x -- i0_x [label=0, style=dashed]
  v2_x -- i0_x [label=10]
  i0_x -- i1_x [label=4]
  i1_x -- i2_x [label=3]
  i2_x -- v3_x [label=3]
  i2_x -- v4_x [label=4]
  i1_x -- v5_x [label=7]
  v0_x [label=v0]
  v1_x [label=v1]
  v2_x [label=v2]
  v3_x [label=v3]
  v4_x [label=v4]
  v5_x [label=v5]
  i0_x [label=i0]
  i1_x [label=i1]
  i2_x [label=i2]
  i2_x [label=i2]
  i1_x [label=i1]
 }
}
```

|    |     v0      |     v1      |     v2      |     v3      |      v4     |     v5      |
|----|-------------|-------------|-------------|-------------|-------------|-------------|
| v0 | `{h}red 0 ` | `{h}red 0 ` | `{h}red 10` | `{h}red 10` | `{h}red 11` | `{h}red 11` |
| v1 | `{h}red 0 ` | `{h}red 0 ` | `{h}red 10` | `{h}red 10` | `{h}red 11` | `{h}red 11` |
| v2 | `{h}red 10` | `{h}red 10` |         0   |         20  |         21  |         21  |
| v3 | `{h}red 10` | `{h}red 10` |         20  |         0   |         7   |         13  |
| v4 | `{h}red 11` | `{h}red 11` |         21  |         7   |         0   |         14  |
| v5 | `{h}red 11` | `{h}red 11` |         21  |         13  |         14  |         0   |

Merging together balded v0 and balded v1 is done by iterating over the other leaf nodes and averaging their balded distances (e.g. the merged distance to v2 is calculated as dist(v0,v2) + dist(v1,v2) / 2)...

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
 ranksep=0.25
 fontname="Courier-Bold"
 fontsize=10
 subgraph cluster_one {
  label="v0 and v1 balded and merged"
  M_x -- i0_x [label=0, style=dashed]
  v2_x -- i0_x [label=10]
  i0_x -- i1_x [label=4]
  i1_x -- i2_x [label=3]
  i2_x -- v3_x [label=3]
  i2_x -- v4_x [label=4]
  i1_x -- v5_x [label=7]
  M_x [label=M]
  v2_x [label=v2]
  v3_x [label=v3]
  v4_x [label=v4]
  v5_x [label=v5]
  i0_x [label=i0]
  i1_x [label=i1]
  i2_x [label=i2]
  i2_x [label=i2]
  i1_x [label=i1]
 }
}
```

|    |           M           |          v2           |          v3           |           v4          |          v5           |
|----|-----------------------|-----------------------|-----------------------|-----------------------|-----------------------|
| M  |           `{h}red 0 ` | `{h}red (10+10)/2=10` | `{h}red (10+10)/2=10` | `{h}red (11+11)/2=11` | `{h}red (11+11)/2=11` |
| v2 | `{h}red (10+10)/2=10` |                   0   |                   20  |                   21  |                   21  |
| v3 | `{h}red (10+10)/2=10` |                   20  |                   0   |                   7   |                   13  |
| v4 | `{h}red (11+11)/2=11` |                   21  |                   7   |                   0   |                   14  |
| v5 | `{h}red (11+11)/2=11` |                   21  |                   13  |                   14  |                   0   |

```{note}
Notice how when both v0 and v1 are balded, their distances to other leaf nodes are exactly the same. So, why average it instead of just taking the distinct value? Because averaging helps with understanding the revised form of the algorithm explained in another section.
```

This algorithm is essentially removing two neighbouring leaf nodes and bringing their shared parent to the forefront (into the distance matrix as a leaf node). In the example above, the new leaf node M represents internal node i0 because the distance between M and i0 is 0.

```{output}
ch7_code/src/phylogeny/ExposeNeighbourParent_AdditiveExplainer.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch7}
phylogeny.ExposeNeighbourParent_AdditiveExplainer
v0
v1
[0,  13, 21, 21, 22, 22]
[13, 0,  12, 12, 13, 13]
[21, 12, 0,  20, 21, 21]
[21, 12, 20, 0,  7,  13]
[22, 13, 21, 7,  0,  14]
[22, 13, 21, 13, 14, 0 ]
```

The problem with the above algorithm is that balding a limb can't be done on a non-additive distance matrix. That is, since a tree doesn't exist for a non-additive distance matrix, it's impossible to get a definitive limb length to use for balding. In such cases, a limb length for each path being balded can be approximated. For example, the following non-additive distance matrix is a slightly tweaked version of the additive distance matrix in the initial example where v0 and v1 are neighbours...

|    | v0 | v1 | v2 | v3 | v4 | v5 |
|----|----|----|----|----|----|----|
| v0 | 0  | 14 | 22 | 20 | 23 | 22 |
| v1 | 14 | 0  | 12 | 10 | 12 | 14 |
| v2 | 22 | 12 | 0  | 20 | 22 | 20 |
| v3 | 20 | 10 | 20 | 0  | 8  | 12 |
| v4 | 23 | 12 | 22 | 8  | 0  | 15 |
| v5 | 22 | 14 | 20 | 12 | 15 | 0  |

`{bm-disable} 3'`
`{bm-disable} 5'`

Assuming v0 and v1 are still neighbours, the limb length for v0 based on ...

 * v2's view: 0.5 * (dist(v0,v1) + dist(v0,v2) - dist(v1,v2)) = 0.5 * (14 + 22 - 12) = 12
 * v3's view: 0.5 * (dist(v0,v1) + dist(v0,v3) - dist(v1,v3)) = 0.5 * (14 + 20 - 10) = 12
 * v4's view: 0.5 * (dist(v0,v1) + dist(v0,v4) - dist(v1,v4)) = 0.5 * (14 + 23 - 12) = 12.5
 * v5's view: 0.5 * (dist(v0,v1) + dist(v0,v5) - dist(v1,v5)) = 0.5 * (14 + 22 - 14) = 11

Similarly, assuming v0 and v1 are still neighbours, the limb length for v1 based on ...

 * v2's view: 0.5 * (dist(v0,v1) + dist(v1,v2) - dist(v0,v2)) = 0.5 * (14 + 12 - 22) = 2
 * v3's view: 0.5 * (dist(v0,v1) + dist(v1,v3) - dist(v0,v3)) = 0.5 * (14 + 10 - 20) = 2
 * v4's view: 0.5 * (dist(v0,v1) + dist(v1,v4) - dist(v0,v4)) = 0.5 * (14 + 12 - 23) = 1.5
 * v5's view: 0.5 * (dist(v0,v1) + dist(v1,v5) - dist(v0,v5)) = 0.5 * (14 + 14 - 22) = 3

`{bm-enable} 3'`
`{bm-enable} 5'`

Note how the limb lengths above are very close to the corresponding limb lengths in the original un-tweaked additive distance matrix: 12 for v0, 2 for v1.

```{note}
Confused where the above computations are coming from? See "view" of a limb length is described in Algorithms/Phylogeny/Find Neighbour Limb Lengths/Average Algorithm_TOPIC.
```

To bald a limb in the distance matrix, each leaf node needs its view of the limb length subtracted from its distance. Balding v0 and v1 results in ...

|    |          v0           |          v1          |        v2         |        v3        |          v4           |        v5         |
|----|-----------------------|----------------------|-------------------|------------------|-----------------------|-------------------|
| v0 | `{h}red 0 `           | `{h}red ?????`       | `{h}red 22-12=10` | `{h}red 20-12=8` | `{h}red 23-12.5=10.5` | `{h}red 22-11=11` |
| v1 | `{h}red ?????`        | `{h}red 0 `          | `{h}red 12-2=10`  | `{h}red 10-2=8`  | `{h}red 12-1.5=10.5`  | `{h}red 14-3=11`  |
| v2 | `{h}red 22-12=10`     | `{h}red 12-2=10`     |                0  |               20 |                    22 |                20 |
| v3 | `{h}red 20-12=8`      | `{h}red 10-2=8`      |                20 |               0  |                    8  |                12 |
| v4 | `{h}red 23-12.5=10.5` | `{h}red 12-1.5=10.5` |                22 |               8  |                    0  |                15 |
| v5 | `{h}red 22-11=11`     | `{h}red 14-3=11`     |                20 |               12 |                    15 |                0  |

Merging together v0 and v1 happens just as it did before, by averaging together the balded distances for each leaf node...

|    |             M               |        v2         |        v3        |          v4           |        v5         |
|----|-----------------------------|-------------------|------------------|-----------------------|-------------------|
| M  | `{h}red 0 `                 | `{h}red 22-12=10` | `{h}red 20-12=8` | `{h}red 23-12.5=10.5` | `{h}red 22-11=11` |
| v2 | `{h}red (10+10)/2=10`       |                0  |               20 |                    22 |                20 |
| v3 | `{h}red (8+8)/2=8`          |                20 |               0  |                    8  |                12 |
| v4 | `{h}red (10.5+10.5)/2=10.5` |                22 |               8  |                    0  |                15 |
| v5 | `{h}red (11+11)/2=11`       |                20 |               12 |                    15 |                0  |

Note that dist(v0,v1) is unknown in the balded matrix (denoted by a bunch of question marks). That doesn't matter because dist(v0,v1) merges into dist(M,M), which must always be 0 (the distance from anything to itself is always 0).

```{output}
ch7_code/src/phylogeny/ExposeNeighbourParent.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch7}
phylogeny.ExposeNeighbourParent
v0
v1
[0 , 14, 22, 20, 23, 22]
[14, 0 , 12, 10, 12, 14]
[22, 12, 0 , 20, 22, 20]
[20, 10, 20, 0 , 8 , 12]
[23, 12, 22, 8 , 0 , 15]
[22, 14, 20, 12, 15, 0 ]
```

#### Inverse Algorithm

`{bm} /(Algorithms\/Phylogeny\/Merge Neighbours\/Inverse Algorithm)_TOPIC/`

```{prereq}
Algorithms/Phylogeny/Merge Neighbours/Average Algorithm_TOPIC
```

**ALGORITHM**: 

This algorithm flips around the idea of finding a limb length to perform the same thing as the averaging algorithm. Instead of finding a limb length, it finds everything in the path EXCEPT for the limb length.

For example, consider the following simple tree and corresponding additive distance matrix ...

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
 ranksep=0.25
 fontname="Courier-Bold"
 fontsize=10
 subgraph cluster_one {
  label="original"
  v0_x -- i0_x [label=11]
  v1_x -- i0_x [label=2]
  v2_x -- i0_x [label=10]
  i0_x -- i1_x [label=4]
  i1_x -- i2_x [label=3]
  i2_x -- v3_x [label=3]
  i2_x -- v4_x [label=4]
  i1_x -- v5_x [label=7]
  v0_x [label=v0]
  v1_x [label=v1]
  v2_x [label=v2]
  v3_x [label=v3]
  v4_x [label=v4]
  v5_x [label=v5]
  i0_x [label=i0]
  i1_x [label=i1]
  i2_x [label=i2]
  i2_x [label=i2]
  i1_x [label=i1]
 }
}
```

|    | v0 | v1 | v2 | v3 | v4 | v5 |
|----|----|----|----|----|----|----|
| v0 | 0  | 13 | 21 | 21 | 22 | 22 |
| v1 | 13 | 0  | 12 | 12 | 13 | 13 |
| v2 | 21 | 12 | 0  | 20 | 21 | 21 |
| v3 | 21 | 12 | 20 | 0  | 7  | 13 |
| v4 | 22 | 13 | 21 | 7  | 0  | 14 |
| v5 | 22 | 13 | 21 | 13 | 14 | 0  |

Assume that you hadn't already seen the tree but somehow already knew that v0 and v1 are neighbours. Consider what happens when you use the standard limb length algorithm to find v0's limb length from v3 ...

 * len(v0) = (dist(v0,v1) + dist(v0,v3) - dist(v1,v3)) / 2
 * len(v0) = (13 + 21 - 12) / 2
 * len(v0) = 11

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
 ranksep=0.25
 fontname="Courier-Bold"
 fontsize=10
 subgraph cluster_three {
  label="(path(v0,v1) + path(v0,v3) - path(v1,v3)) / 2"
  v0_z -- i0_z [label=" ", color="blue", penwidth="2.5"]
  v1_z -- i0_z [label=" "]
  v2_z -- i0_z [label=" "]
  i0_z -- i1_z [label=" "]
  i1_z -- i2_z [label=" "]
  i2_z -- v3_z [label=" "]
  i2_z -- v4_z [label=" "]
  i1_z -- v5_z [label=" "]
  v0_z [label=v0]
  v1_z [label=v1]
  v2_z [label=v2]
  v3_z [label=v3]
  v4_z [label=v4]
  v5_z [label=v5]
  i0_z [label=i0]
  i1_z [label=i1]
  i2_z [label=i2]
  i2_z [label=i2]
  i1_z [label=i1]
 }
 subgraph cluster_two {
  label="path(v0,v1) + path(v0,v3) - path(v1,v3)"
  v0_y -- i0_y [color="blue:invis:blue", penwidth="2.5"]
  v1_y -- i0_y [label=" "]
  v2_y -- i0_y [label=" "]
  i0_y -- i1_y [label=" "]
  i1_y -- i2_y [label=" "]
  i2_y -- v3_y [label=" "]
  i2_y -- v4_y [label=" "]
  i1_y -- v5_y [label=" "]
  v0_y [label=v0]
  v1_y [label=v1]
  v2_y [label=v2]
  v3_y [label=v3]
  v4_y [label=v4]
  v5_y [label=v5]
  i0_y [label=i0]
  i1_y [label=i1]
  i2_y [label=i2]
  i2_y [label=i2]
  i1_y [label=i1]
 }
 subgraph cluster_one {
  label="path(v0,v1) + path(v0,v3)"
  v0_x -- i0_x [label=" ", color="blue:invis:blue", penwidth="2.5"]
  v1_x -- i0_x [label=" ", color="blue", penwidth="2.5"]
  v2_x -- i0_x [label=" "]
  i0_x -- i1_x [label=" ", color="blue", penwidth="2.5"]
  i1_x -- i2_x [label=" ", color="blue", penwidth="2.5"]
  i2_x -- v3_x [label=" ", color="blue", penwidth="2.5"]
  i2_x -- v4_x [label=" "]
  i1_x -- v5_x [label=" "]
  v0_x [label=v0]
  v1_x [label=v1]
  v2_x [label=v2]
  v3_x [label=v3]
  v4_x [label=v4]
  v5_x [label=v5]
  i0_x [label=i0]
  i1_x [label=i1]
  i2_x [label=i2]
  i2_x [label=i2]
  i1_x [label=i1]
 }
}
```

By slightly tweaking the terms in the expression above, it's possible to instead find the distance between the neighbouring pair's parent (i0) and v3 ...

 * inverse_len(v3) = (dist(v0,v3) + dist(v1,v3) - dist(v0,v1)) / 2
 * inverse_len(v3) = (21 + 12 - 13) / 2
 * inverse_len(v3) = 10 = dist(v0,v3) - len(v0) = dist(v1,v3) - len(v1)

```{note}
All the same distances are being used in this new computation, they're just being added / subtracted in a different order.
```

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
 ranksep=0.25
 fontname="Courier-Bold"
 fontsize=10
 subgraph cluster_three {
  label="(dist(v0,v3) + dist(v1,v3) - dist(v0,v1)) / 2"
  v0_z -- i0_z [label=" "]
  v1_z -- i0_z [label=" "]
  v2_z -- i0_z [label=" "]
  i0_z -- i1_z [label=" ", color="blue", penwidth="2.5"]
  i1_z -- i2_z [label=" ", color="blue", penwidth="2.5"]
  i2_z -- v3_z [label=" ", color="blue", penwidth="2.5"]
  i2_z -- v4_z [label=" "]
  i1_z -- v5_z [label=" "]
  v0_z [label=v0]
  v1_z [label=v1]
  v2_z [label=v2]
  v3_z [label=v3]
  v4_z [label=v4]
  v5_z [label=v5]
  i0_z [label=i0]
  i1_z [label=i1]
  i2_z [label=i2]
  i2_z [label=i2]
  i1_z [label=i1]
 }
 subgraph cluster_two {
  label="dist(v0,v3) + dist(v1,v3) - dist(v0,v1)"
  v0_y -- i0_y [label=" "]
  v1_y -- i0_y [label=" "]
  v2_y -- i0_y [label=" "]
  i0_y -- i1_y [label=" ", color="blue:invis:blue", penwidth="2.5"]
  i1_y -- i2_y [label=" ", color="blue:invis:blue", penwidth="2.5"]
  i2_y -- v3_y [label=" ", color="blue:invis:blue", penwidth="2.5"]
  i2_y -- v4_y [label=" "]
  i1_y -- v5_y [label=" "]
  v0_y [label=v0]
  v1_y [label=v1]
  v2_y [label=v2]
  v3_y [label=v3]
  v4_y [label=v4]
  v5_y [label=v5]
  i0_y [label=i0]
  i1_y [label=i1]
  i2_y [label=i2]
  i2_y [label=i2]
  i1_y [label=i1]
 }
 subgraph cluster_one {
  label="dist(v0,v3) + dist(v1,v3)"
  v0_x -- i0_x [label=" ", color="blue", penwidth="2.5"]
  v1_x -- i0_x [label=" ", color="blue", penwidth="2.5"]
  v2_x -- i0_x [label=" "]
  i0_x -- i1_x [label=" ", color="blue:invis:blue", penwidth="2.5"]
  i1_x -- i2_x [label=" ", color="blue:invis:blue", penwidth="2.5"]
  i2_x -- v3_x [label=" ", color="blue:invis:blue", penwidth="2.5"]
  i2_x -- v4_x [label=" "]
  i1_x -- v5_x [label=" "]
  v0_x [label=v0]
  v1_x [label=v1]
  v2_x [label=v2]
  v3_x [label=v3]
  v4_x [label=v4]
  v5_x [label=v5]
  i0_x [label=i0]
  i1_x [label=i1]
  i2_x [label=i2]
  i2_x [label=i2]
  i1_x [label=i1]
 }
}
```

The inverse_len function above in abstracted form is 0.5 * (dist(L,X) + dist(N,X) - dist(L,N)), where ...

 * L and N are neighbours.
 * X is a leaf node that isn't L or N.

Note that the distance calculated by the inverse_len example above is exactly the same distance you'd get for v3 when balding and merging v0 and v1 using the averaging algorithm. That is, instead of using the averaging algorithm to bald and merge the neighbouring pair, you can just inject inverse_len's result for each leaf node into the distance matrix and remove the neighbouring pair.

The inverse_len for leaf node ...

 * v2: 0.5 * (dist(v0,v2) + dist(v1,v2) - dist(v0,v1)) = 0.5 * (21 + 12 - 13) = 10
 * v3: 0.5 * (dist(v0,v3) + dist(v1,v3) - dist(v0,v1)) = 0.5 * (21 + 12 - 13) = 10
 * v4: 0.5 * (dist(v0,v4) + dist(v1,v4) - dist(v0,v1)) = 0.5 * (22 + 13 - 13) = 11
 * v5: 0.5 * (dist(v0,v5) + dist(v1,v5) - dist(v0,v1)) = 0.5 * (22 + 13 - 13) = 11

|    |             M            |             v2           |            v3            |             v4           |            v5            |
|----|--------------------------|--------------------------|--------------------------|--------------------------|--------------------------|
| M  | `{h}red 0 `              | `{h}red (21+12-13)/2=10` | `{h}red (21+12-13)/2=10` | `{h}red (21+12-13)/2=10` | `{h}red (21+12-13)/2=10` |
| v2 | `{h}red (21+12-13)/2=10` |                      0   |                      20  |                      21  |                      21  |
| v3 | `{h}red (21+12-13)/2=10` |                      20  |                      0   |                      7   |                      13  |
| v4 | `{h}red (21+12-13)/2=10` |                      21  |                      7   |                      0   |                      14  |
| v5 | `{h}red (22+13-13)/2=11` |                      21  |                      13  |                      14  |                      0   |

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
 ranksep=0.25
 fontname="Courier-Bold"
 fontsize=10
 subgraph cluster_one {
  label="v0 and v1 balded and merged"
  M_x -- i0_x [label=0, style=dashed]
  v2_x -- i0_x [label=10]
  i0_x -- i1_x [label=4]
  i1_x -- i2_x [label=3]
  i2_x -- v3_x [label=3]
  i2_x -- v4_x [label=4]
  i1_x -- v5_x [label=7]
  M_x [label=M]
  v2_x [label=v2]
  v3_x [label=v3]
  v4_x [label=v4]
  v5_x [label=v5]
  i0_x [label=i0]
  i1_x [label=i1]
  i2_x [label=i2]
  i2_x [label=i2]
  i1_x [label=i1]
 }
}
```

In fact, inverse_len is just the simplified expression form of the averaging algorithm. Consider the steps you have to go through for each leaf node to bald and merge the neighbouring pair v0 and v1 using the averaging algorithm. For example, to figure out the balded distance between v3 and the merged node, the steps are ...

`{bm-disable} 3'`

 1. Get v3's view of v0's limb length:
 
    len(v0) = 0.5 * (dist(v0,v1) + dist(v0,v3) - dist(v1,v3))

 2. Get v3's view of v1's limb length:
 
    len(v1) = 0.5 * (dist(v1,v0) + dist(v1,v3) - dist(v0,v3))

 3. Bald v0 for v3 using step 1's result:
 
    bald_dist(v0,v5) = dist(v0,v3) - len(v0)

 4. Bald v1 for v3 using step 2's result:
 
    bald_dist(v1,v5) = dist(v1,v3) - len(v1)

 5. Average results from step 3 and 4 to produce the merged node's distance for v3:
 
    merge(v0,v1) = (bald_dist(v0,v5) + bald_dist(v1,v5)) / 2

`{bm-enable} 3'`

Consider what happens when you combine all of the above steps together as a single expression ...

```{kt}
\frac{D_{v0,v3} - (0.5 \cdot (D_{v0,v1} + D_{v0,v3} - D_{v1,v3})) + D_{v1,v3} - (0.5 \cdot (D_{v1,v0} + D_{v1,v3} - D_{v0,v3}))}{2}
```

Simplifying that expression results in ...

```{kt}
\frac{D_{v0,v3} - (0.5 \cdot (D_{v0,v1} + D_{v0,v3} - D_{v1,v3})) + D_{v1,v3} - (0.5 \cdot (D_{v1,v0} + D_{v1,v3} - D_{v0,v3}))}{2}
\\[0.5em]
\frac{D_{v0,v3} - (0.5 \cdot D_{v0,v1} + 0.5 \cdot D_{v0,v3} - 0.5 \cdot D_{v1,v3})) + (D_{v1,v3} - (0.5 \cdot D_{v1,v0} + 0.5 \cdot D_{v1,v3} - 0.5 \cdot D_{v0,v3})}{2}
\\[0.5em]
\frac{D_{v0,v3} - 0.5 \cdot D_{v0,v1} - 0.5 \cdot D_{v0,v3} + 0.5 \cdot D_{v1,v3} + D_{v1,v3} - 0.5 \cdot D_{v1,v0} - 0.5 \cdot D_{v1,v3} + 0.5 \cdot D_{v0,v3}}{2}
\\[0.5em]
\frac{D_{v0,v3} - 0.5 \cdot D_{v0,v1} + 0.5 \cdot D_{v1,v3} + D_{v1,v3} - 0.5 \cdot D_{v1,v0} - 0.5 \cdot D_{v1,v3}}{2}
\\[0.5em]
\frac{D_{v0,v3} - 0.5 \cdot D_{v0,v1} + D_{v1,v3} - 0.5 \cdot D_{v1,v0}}{2}
\\[0.5em]
\frac{D_{v0,v3} + D_{v1,v3} - 1 \cdot D_{v1,v0}}{2}
\\[0.5em]
\frac{D_{v0,v3} + D_{v1,v3} - D_{v1,v0}}{2}
```

The simplified form of the expression is exactly the computation that the inverse_len example ran for v3 ...

 * inverse_len(v3) = (dist(v0,v3) + dist(v1,v3) - dist(v0,v1)) / 2
 * inverse_len(v3) = (21 + 12 - 13) / 2
 * inverse_len(v3) = 10 = dist(v0,v3) - len(v0) = dist(v1,v3) - len(v1)

Since this algorithm is doing the same thing as the averaging algorithm, it'll work on non-additive distance matrices in the exact same way as the averaging algorithm. It's just the averaging algorithm in simplified / optimized form. For example, the following non-additive distance matrix is a slightly tweaked version of the additive distance matrix in the initial example where v0 and v1 are neighbours...

|    | v0 | v1 | v2 | v3 | v4 | v5 |
|----|----|----|----|----|----|----|
| v0 | 0  | 14 | 22 | 20 | 23 | 22 |
| v1 | 14 | 0  | 12 | 10 | 12 | 14 |
| v2 | 22 | 12 | 0  | 20 | 22 | 20 |
| v3 | 20 | 10 | 20 | 0  | 8  | 12 |
| v4 | 23 | 12 | 22 | 8  | 0  | 15 |
| v5 | 22 | 14 | 20 | 12 | 15 | 0  |

Assuming v0 and v1 are still neighbours, the merged distance for ...

 * v2: 0.5 * (dist(v0,v2) + dist(v1,v2) - dist(v0,v1)) = 0.5 * (22 + 12 - 14) = 10
 * v3: 0.5 * (dist(v0,v3) + dist(v1,v3) - dist(v0,v1)) = 0.5 * (20 + 10 - 14) = 8
 * v4: 0.5 * (dist(v0,v4) + dist(v1,v4) - dist(v0,v1)) = 0.5 * (23 + 12 - 14) = 10.5
 * v5: 0.5 * (dist(v0,v5) + dist(v1,v5) - dist(v0,v1)) = 0.5 * (22 + 14 - 14) = 11

|    |             M              |             v2           |            v3            |             v4             |            v5            |
|----|----------------------------|--------------------------|--------------------------|----------------------------|--------------------------|
| M  | `{h}red 0 `                | `{h}red (22+12-14)/2=10` | `{h}red (20+10-14)/2=8`  | `{h}red (23+12-14)/2=10.5` | `{h}red (22+14-14)/2=11` |
| v2 | `{h}red (22+12-14)/2=10`   |                      0   |                      20  |                      22    |                      20  |
| v3 | `{h}red (20+10-14)/2=8`    |                      20  |                      0   |                      8     |                      12  |
| v4 | `{h}red (23+12-14)/2=10.5` |                      22  |                      8   |                      0     |                      15  |
| v5 | `{h}red (22+14-14)/2=11`   |                      20  |                      12  |                      15    |                      0   |

```{output}
ch7_code/src/phylogeny/ExposeNeighbourParent_Optimized.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch7}
phylogeny.ExposeNeighbourParent_Optimized
v0
v1
[0 , 14, 22, 20, 23, 22]
[14, 0 , 12, 10, 12, 14]
[22, 12, 0 , 20, 22, 20]
[20, 10, 20, 0 , 8 , 12]
[23, 12, 22, 8 , 0 , 15]
[22, 14, 20, 12, 15, 0 ]
```

### Distance Matrix to Tree

`{bm} /(Algorithms\/Phylogeny\/Distance Matrix to Tree)_TOPIC/`

```{prereq}
Algorithms/Phylogeny/Tree to Additive Distance Matrix_TOPIC
Algorithms/Phylogeny/Tree to Simple Tree_TOPIC
Algorithms/Phylogeny/Additive Distance Matrix Cardinality_TOPIC
```

**WHAT**: Given a distance matrix, convert that distance matrix into an evolutionary tree. Different algorithms are presented that either ...

* find the unique simple tree for an additive distance matrix,
* approximate a simple tree for a non-additive distance matrix,
* approximate a tree for a distance matrix regardless of if it's additive or not.

**WHY**: Recall that converting a distance matrix to a tree is the end goal of phylogeny. Given the distances between a set of known / present-day entities, these algorithms will infer their evolutionary relationships.

#### UPGMA Algorithm

`{bm} /(Algorithms\/Phylogeny\/Distance Matrix to Tree\/UPGMA Algorithm)_TOPIC/`

**ALGORITHM**:

Unweighted pair group method with arithmetic mean (UPGMA) is a heuristic algorithm used to estimate a binary ultrametric tree for some distance matrix.

```{note}
A binary ultrametric tree is an ultrametric tree where each internal node only branches to two children. In other words, a binary ultrametric tree is a rooted binary tree where all leaf nodes are equidistant from the root.
```

The algorithm assumes that the rate of mutation is consistent (molecular clock). For example, ...
   
 * every minute, around n of m nucleotides mutate.
 * every hour, around n genome rearrangement reversals occur per genome segment of size m.
 * etc..

 This assumption is what makes the tree ultrametric. A set of present day species (leaf nodes) are assumed to all have the same amount of mutation (distance) from their shared ancestor (shared internal node).

```{svgbob}
            g      <-- "shared ancestor"
           / \
          /   \
     2.5 /     \
        /       \ 3
       /         \
      f           \
     / \           \
1.5 /   \ 1.5       e
   /     \       1 / \ 1
  /       \       /   \
 a         b     c     d      <-- "present day species"
   
* "a, b, c, and d share ancestor g:   dist(a,g) = dist(b,g) = dist(c,g) = dist(d,g) = 4"
```
   
For example, assume the present year is 2000. Four present day species share a common ancestor from the year 1800. The age difference between each of these four species and their shared ancestor is the same: 2000 - 1800 = 200 years.
   
Since the rate of mutation is assumed to be consistent, all four present day species should have roughly the same amount of mutation when compared against their shared ancestor: 200 years worth of mutation. Assume the number of genome rearrangement reversals is being used as the measure of mutation. If the rate of reversals expected per 100 years is 2, the distance between each of the four present day species and their shared ancestor would be 4: 2 reversals per century * 2 centuries = 4 reversals.

```{svgbob}
                      g (mut=4)      <-- "shared ancestor"
                     / \
                    /   \
               2.5 /     \
                  /       \ 3
                 /         \
      (mut=1.5) f           \
               / \           \
          1.5 /   \ 1.5       e (mut=1)
             /     \       1 / \ 1
            /       \       /   \
   (mut=0) a         b     c     d (mut=0) a      <-- "present day species"
                (mut=0)   (mut=0)
   
* "a and b share ancestor f:   dist(a,f) = dist(b,f) = 1.5"
* "c and d share ancestor e:   dist(c,e) = dist(d,e) = 1"
* "a, b, c, and d share ancestor g:   dist(a,g) = dist(b,g) = dist(c,g) = dist(d,g) = 4"

* "mut is the amount of mutation required to get any of the leaf nodes to that ancestor"
  "and vice-versa."
```

In the example above, ...

 * present day species a and b (leaf nodes) have the same amount of mutation (distance) from shared ancestor f (shared internal node): 1.5 reversals
 * present day species c and d (leaf nodes) have the same amount of mutation (distance) from shared ancestor e (shared internal node): 1 reversal
 * present day species a and c (leaf nodes) have the same amount of mutation (distance) from shared ancestor g (shared internal node): 4 reversals
 * present day species a and d (leaf nodes) have the same amount of mutation (distance) from shared ancestor g (shared internal node): 4 reversals
 * etc..
 
Given a distance matrix, UPGMA estimates an ultrametric tree for that matrix by iteratively picking two available nodes and connecting them with a new internal node, where available node is defined as a node without a parent. The process stops once a single available node remains (that node being the root node).

```{svgbob}
                                                                                                          g           
                                                                                                         / \          
                                                                                                        /   \         
                                                                                                   2.5 /     \        
                                                                                                      /       \ 3     
                                                                                                     /         \      
                                                                 f                                  f           \     
                                                                / \                                / \           \    
                                           e               1.5 /   \ 1.5      e               1.5 /   \ 1.5       e   
                                        1 / \ 1               /     \      1 / \ 1               /     \       1 / \ 1
                                         /   \               /       \      /   \               /       \       /   \ 
 a    b    c    d             a    b    c     d             a         b    c     d             a         b     c     d

      STEP1                          STEP2                           STEP3                               STEP4        
  "(no connections)"              "(connect c, d)"                "(connect a, b)"                     "(connect e, f)"
```
   
Which two nodes are selected per iteration is based on clustering. In the beginning, each leaf node in the distance matrix is its own cluster: Ca={a}, Cb={b}, Cc={c}, and Cd={d}.

|        | Ca={a} | Cb={b} | Cc={c} | Cd={d} |
|--------|--------|--------|--------|--------|
| Ca={a} |   0    |   3    |   4    |   3    |
| Cb={b} |   3    |   0    |   4    |   5    |
| Cc={c} |   4    |   4    |   0    |   2    |
| Cd={d} |   3    |   5    |   2    |   0    |

The two clusters with the minimum distance are chosen to connect in the tree. In the example distance matrix above, the minimum distance is between Cc and Cd (distance of 2), meaning that Cc and Cd should be connected together with a new internal node.

```{svgbob}
   e
  / \
 /   \
c     d
```

````{note}
Note what's happening here. The assumption being made that the leaf nodes for the minimum distance matrix value are always neighbours. Not always true, but probably good enough as a starting point. For example, the following distance matrix and tree would identify v0 and v2 as neighbours when in fact they aren't ...

```{svgbob}
 a             b
  \           /
 1 \         / 1
    e ----- f
90 /    1    \ 90
  /           \
 d             c
```

|   | a  |  b  | c  |  d  |
|---|----|-----|----|-----|
| a | 0  | 91  | 3  | 92  |
| b | 91 | 0   | 92 | 181 |
| c | 3  | 92  | 0  | 91  |
| d | 92 | 181 | 91 | 0   |

It may be a good idea to use Algorithms/Phylogeny/Find Neighbours_TOPIC to short circuit this restriction, possibly producing a better heuristic. But, the original algorithm doesn't call for it.
````
   
This new internal node represents a shared ancestor. The distance of 2 represents the total amount of mutation that any species in Cc must undergo to become a species in Cd (and vice-versa). Since the assumption is that the rate of mutation is steady, it's assumed that the species in Cc and species in Cd all have an equal amount of mutation from their shared ancestor:

* mut(Ce) = dist(Cc, Cd) / 2 = 2 / 2 = 1
* dist(Ce, Cc) = mut(Ce) - mut(Cc) = 1 - 0 = 1
* dist(Ce, Cd) = mut(Ce) - mut(Cd) = 1 - 0 = 1

```{svgbob}
                                                                                                          e (mut=1)   
                                                                                                       1 / \ 1        
                                                     "(connect c, d)"                                   /   \         
(mut=0) a        b        c        d (mut=0)         ------------>           (mut=0) a        b        c     d (mut=0)
           (mut=0)        (mut=0)                                                       (mut=0)        (mut=0)        
```

The distance matrix then gets modified by merging together the recently connected clusters. The new cluster combines the leaf nodes from both clusters: Ce={c,d}, where new distance matrix distances for that cluster are computed using the formula...
    
```{kt}
D_{C_1,C_2} = \frac{
  \sum_{i \in C_1} \sum_{j \in C_2} D_{i,j}
  }{
    |C_1| \cdot |C_2|
  }
```

```{output}
ch7_code/src/phylogeny/UPGMA.py
python
# MARKDOWN_DIST\s*\n([\s\S]+)\n\s*# MARKDOWN_DIST
```

|          | Ca={a} | Cb={b} | Ce={c,d} |
|----------|--------|--------|----------|
| Ca={a}   |   0    |   3    |    3.5   |
| Cb={b}   |   3    |   0    |    7.5   |
| Ce={c,d} |  3.5   |  7.5   |     0    |

This process repeats at each iteration until a single cluster remains. At the next iteration, Ca and Cb have the minimum distance in the previous distance matrix (distance of 3), meaning that Ca and Cb should be connected with a new internal internal node:
   
 * mut(Cf) = dist(Ca, Cb) / 2 = 3 / 2 = 1.5
 * dist(Cf, Ca) = mut(Cf) - mut(Ca) = 1.5 - 0 = 1.5
 * dist(Cf, Cb) = mut(Cf) - mut(Cb) = 1.5 - 0 = 1.5

```{svgbob}
                                                                              (mut=1.5) f                   
                                                                                       / \                           
                             e (mut=1)                                            1.5 /   \ 1.5          e (mut=1)   
                          1 / \ 1                                                    /     \          1 / \ 1        
                           /   \                  "(connect a, b)"                  /       \          /   \         
(mut=0) a        b        c     d (mut=0)         ------------>           (mut=0)  a         b        c     d (mut=0)
           (mut=0)        (mut=0)                                                       (mut=0)      (mut=0)         
```

|          | Cf={a,b} | Ce={c,d} |
|----------|----------|----------|
| Cf={a,b} |     0    |     4    |
| Ce={c,d} |     4    |     0    |

At the next iteration, Ce and Cf have the minimum distance in the previous distance matrix (distance of 4), meaning that Ce and Cf should be connected together with a new internal node:
   
 * mut(Cg) = dist(Cf, Ce) / 2 = 4 / 2 = 2
 * dist(Cg, Cf) = mut(Cg) - mut(Cf) = 2 - 1.5 = 0.5
 * dist(Cg, Ce) = mut(Cg) - mut(Ce) = 2 - 1 = 1

```{svgbob}
                                                                                                g (mut=2)
                                                                                               / \
                                                                                              /   \
                                                                                         0.5 /     \ 1
                                                                                            /       \
                                                                                           /         \
              f (mut=1.5)                                                       (mut=1.5) f           \             
             / \                                                                         / \           \            
        1.5 /   \ 1.5          e (mut=1)                                            1.5 /   \ 1.5       e (mut=1)   
           /     \          1 / \ 1                                                    /     \       1 / \ 1        
          /       \          /   \                  "(connect e, f)"                  /       \       /   \         
(mut=0)  a         b        c     d (mut=0)         ------------>           (mut=0)  a         b     c     d (mut=0)
              (mut=0)      (mut=0)                                                        (mut=0)   (mut=0)         
```

|              | Cg={a,b,c,d} |
|--------------|--------------|
| Cg={a,b,c,d} |       0      |
   
The process is complete. Only a single cluster remains (representing the root) / the ultrametric tree is fully generated.

```{svgbob}
                    g (mut=2)
                   / \
                  /   \
             0.5 /     \ 1
                /       \
               /         \
    (mut=1.5) f           \             
             / \           \            
        1.5 /   \ 1.5       e (mut=1)   
           /     \       1 / \ 1        
          /       \       /   \         
(mut=0)  a         b     c     d (mut=0)
              (mut=0)   (mut=0)         
```

Note that the generated ultrametric tree above is an estimation. The distance matrix for the example above isn't an additive distance matrix, meaning a unique simple tree doesn't exist for it. Even if it were an additive distance matrix, an ultrametric tree is a rooted tree, meaning it'll never qualify as the simple tree unique to that additive distance matrix (root node has degree_GRAPH of 2 which isn't allowed in a simple tree).
   
In addition, some distances in the generated ultrametric tree are wildly off from the original distance matrix distances. For example, ...

 * dist(a,d)=8 in the generated ultrametric tree.
 * dist(a,d)=5 in the original distance matrix.

Part of this may have to do with the assumption that the closest two nodes in the distance matrix are neighbors in the ultrametric tree.

```{output}
ch7_code/src/phylogeny/UPGMA.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch7}
phylogeny.UPGMA
[0,  13, 21, 21, 22, 22]
[13, 0,  12, 12, 13, 13]
[21, 12, 0,  20, 21, 21]
[21, 12, 20, 0,  7,  13]
[22, 13, 21, 7,  0,  14]
[22, 13, 21, 13, 14, 0 ]
```

#### Additive Phylogeny Algorithm

`{bm} /(Algorithms\/Phylogeny\/Distance Matrix to Tree\/Additive Phylogeny Algorithm)_TOPIC/`

```{prereq}
Algorithms/Phylogeny/Trim_TOPIC
Algorithms/Phylogeny/Un-trim Tree_TOPIC
```

**ALGORITHM**:

Additive phylogeny is a recursive algorithm that finds the unique simple tree for some additive distance matrix. At each recursive step, the algorithm trims off a single leaf node from the distance matrix, stopping once the distance matrix consists of only two leaf nodes. The simple tree for any 2x2 distance matrix is obvious as ...
   
 * it only consists of 2 nodes
 * it only consists of a single edge (nodes of degree_GRAPH 2 not allowed in simple trees, meaning train of non-branching edges not allowed)

For example, the following 2x2 distance matrix has the following simple tree...

|    | v0 | v1 |
|----|----|----|
| v0 | 0  | 14 |
| v1 | 14 | 0  |

```{svgbob}
v0
  \
   \ 14
    \
     v1 
```

```{output}
ch7_code/src/phylogeny/AdditivePhylogeny.py
python
# MARKDOWN_OBVIOUS_TREE\s*\n([\s\S]+)\n\s*# MARKDOWN_OBVIOUS_TREE
```

As the algorithm returns from each recursive step, it has 2 pieces of information:

 * an additive distance matrix containing trimmed leaf node L.
 * a simple tree not containing trimmed leaf node L.

That's enough information to know where on the returned tree L's limb should be added and what L's limb length should be (un-trimming the tree). At the end, the algorithm will have constructed the entire simple tree for the additive distance matrix.

```{output}
ch7_code/src/phylogeny/AdditivePhylogeny.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch7}
phylogeny.AdditivePhylogeny_Verbose
[0,  13, 21, 21, 22, 22]
[13, 0,  12, 12, 13, 13]
[21, 12, 0,  20, 21, 21]
[21, 12, 20, 0,  7,  13]
[22, 13, 21, 7,  0,  14]
[22, 13, 21, 13, 14, 0 ]
```

```{note}
The book is inconsistent about whether simple trees can have internal edges of weight 0. Early in the book it says that it can and later on it says that it goes back on that and says internal edges of weight 0 aren't actually allowed. I'd already implied as much given that they'd be the same organism at both ends, and this algorithm explicitly won't allow it in that if it walks up to a node, it'll branch off that node (an additional edge weight of 0 won't extend past that node).
```

#### Neighbour Joining Phylogeny Algorithm

`{bm} /(Algorithms\/Phylogeny\/Distance Matrix to Tree\/Neighbour Joining Phylogeny Algorithm)_TOPIC/`

```{prereq}
Algorithms/Phylogeny/Find Neighbours_TOPIC
Algorithms/Phylogeny/Find Neighbour Limb Lengths_TOPIC
Algorithms/Phylogeny/Expose Neighbour Parent_TOPIC
```

**ALGORITHM**:

Neighbour joining phylogeny is a recursive algorithm that either...

 * finds the unique simple tree for some additive distance matrix.
 * approximates a simple tree for some non-additive distance matrix (close to being additive).
 
At each recursive step, the algorithm finds a pair of neighbouring leaf nodes in the distance matrix and exposes their shared parent (neighbours replaced with parent in the distance matrix), stopping once the distance matrix consists of only two leaf nodes. The simple tree for any 2x2 distance matrix is obvious as ...
   
 * it only consists of 2 nodes
 * it only consists of a single edge (nodes of degree_GRAPH 2 not allowed in simple trees, meaning train of non-branching edges not allowed)

For example, the following 2x2 distance matrix has the following simple tree...

|    | v0 | v1 |
|----|----|----|
| v0 | 0  | 14 |
| v1 | 14 | 0  |

```{svgbob}
v0
  \
   \ 14
    \
     v1 
```

```{output}
ch7_code/src/phylogeny/NeighbourJoiningPhylogeny.py
python
# MARKDOWN_OBVIOUS_TREE\s*\n([\s\S]+)\n\s*# MARKDOWN_OBVIOUS_TREE
```

As the algorithm returns from each recursive step, it has 3 pieces of information:

 * there exists two neighbouring leaf nodes L and N.
 * a distance matrix containing L and N.
 * a simple tree missing L and N, but containing their shared parent P.

That's enough information to know where L and N should be added on to the tree (node P) and what their limb lengths are. At the end, the algorithm will have constructed the entire simple tree for the additive distance matrix.

```{output}
ch7_code/src/phylogeny/NeighbourJoiningPhylogeny.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch7}
phylogeny.NeighbourJoiningPhylogeny_Verbose
[0 , 14, 22, 20, 23, 22]
[14, 0 , 12, 10, 12, 14]
[22, 12, 0 , 20, 22, 20]
[20, 10, 20, 0 , 8 , 12]
[23, 12, 22, 8 , 0 , 15]
[22, 14, 20, 12, 15, 0 ]
```

```{note}
The book is inconsistent about whether simple trees can have internal edges of weight 0. Early in the book it says that it can and later on it says that it goes back on that and says internal edges of weight 0 aren't actually allowed. I'd already implied as much given that they'd be the same organism at both ends, but I'm unsure if this algorithm will allow it if fed in a non-additive distance matrix. It should never happend with an additive distance matrix.
```


#### Evolutionary Algorithm

`{bm} /(Algorithms\/Phylogeny\/Distance Matrix to Tree\/Evolutionary Algorithm)_TOPIC/`

**ALGORITHM**:

```{note}
This is essentially a hammer, ignoring much of the logic and techniques derived in prior sections. There is no code for this section because writing it involves doing things like writing a generic linear systems solver, evolutionary algorithms framework, etc... There are Python packages you can use if you really want to do this, but this section is more describing the overarching idea.

The logic and techniques in prior sections typically work much better and much faster than doing something like this, but this doesn't require as much reasoning / thinking. This idea was first hinted at in the Pevzner book when first describing how to assign weights for non-additive distance matrices.
```

Given an additive distance matrix, if you already know the structure of the tree, with edge weights that satisfy that tree are derivable from that distance matrix. For example, given the following distance matrix and tree structure...
   
|      | Cat | Lion | Bear |
|------|-----|------|------|
| Cat  |  0  |  2   |  4   |
| Lion |  2  |  0   |  3   |
| Bear |  4  |  3   |  0   |

```{svgbob}
           * A2
          / \
         /   \
        /     \
    A1 *       \
      / \       \
     /   \       \
    /     \       \
   *       *       *
  Cat     Lion    Bear
```

... the distances between species must have been calculated as follows:

* dist(Cat, Lion) = dist(Cat, A1) + dist(A1, Lion)`
* dist(Cat, Bear) = dist(Cat, A1) + dist(A1, A2) + dist(A2, Bear)`
* dist(Lion, Bear) = dist(Lion, A1) + dist(A1, A2) + dist(A2, Bear)`

This is a system of linear equations that may be solved using standard algebra. For example, each `dist()` above is representable as either a variable or a constant...

* 2 = dist(Cat, Lion)  = dist(Lion, Cat)
* 4 = dist(Cat, Bear)  = dist(Bear, Cat)
* 3 = dist(Lion, Bear) = dist(Bear, Lion)
* w = dist(Cat, A1)    = dist(A1, Cat)
* x = dist(Lion, A1)   = dist(A1, Lion)
* y = dist(A1, A2)     = dist(A2, A1)
* z = dist(A2, Bear)   = dist(Bear, A2)

... , which converts each calculation above to the following equations ...

* 2 = w + x
* 4 = w + y + z
* 3 = x + y + z

```{svgbob}
           * A2
          / \
       y /   \
        /     \
    A1 *       \ z
      / \       \
  w  /   \ x     \
    /     \       \
   *       *       *
  Cat     Lion    Bear
```

Solving this system of linear equations results in. ..

* x = 0.5
* w = 1.5
* z = 2.5 - y`

As such, the example distance matrix is an additive matrix because there exists a tree that satisfies it. Any of the following edge weights will work with this distance matrix...

* x = 0.5, w = 1.5, y = 0.5, z = 2.0
* x = 0.5, w = 1.5, y = 1.0, z = 1.5
* x = 0.5, w = 1.5, y = 1.5, z = 1.0
* ...

The example above tests against a tree that's a non-simple tree (A2 is an internal node with degree_GRAPH of 2). If you limit your search to simple trees and find nothing, there won't be any non-simple trees either: Non-simple trees are essentially simple trees that have had edges broken up by splicing nodes in between (degree_GRAPH 2 nodes).

The non-simple tree example above collapsed into a simple tree:

```{svgbob}
           * Bear
          /
       a /
        /
       * A2
      / \ 
   w /   \ x
    /     \
   *       *
  Cat     Lion
```

````{note}
The path A1-A2-Bear has been collapsed into A1-Bear, where the weight of the newly collapsed edge is represented by a (formerly y+z). Using the same additive distance matrix, the simple tree above gets solved to `w = 2, x = 1, a = 2`.  
````

If the distance matrix isn't additive, something like sum of errors squared may be used to converge on an approximate set of weights that work. Similarly, evolutionary algorithms may be used in addition to approximating weights to find a simple tree that's close enough to the  

### Sequence Inference

`{bm} /(Algorithms\/Phylogeny\/Sequence Inference)_TOPIC/`

```{prereq}
Algorithms/Phylogeny/Distance Matrix to Tree_TOPIC
Algorithms/Sequence Alignment_TOPIC
```

**WHAT**: It's possible to infer the sequences for shared ancestors in a phylogenetic tree. Specifically, given a phylogenetic tree, each node in may have a sequence assigned to it, where a ...

 * leaf node is assigned the sequence of the known entity it's for.
 * internal node is assigned an inferred sequence based on neighbouring nodes.

```{svgbob}
         .-----------.
         | AncestorA |
         |  ATTGCC   |
         '-----+-----'
              / \
             /   \
            /     \
     .-----+-----. \
     | AncestorB |  \
     |  ACTGCT   |   \
     '-----+-----'    \
          / \          \
         /   \          \
        /     \          \
.------+-. .---+----. .---+----.
|   Cat  | |  Lion  | |  Bear  |
| ACTGGT | | ACTGCT | | ATTCCC |
'--------' '--------' '--------'
```

**WHY**: Inferring ancestral sequences may help provide additional insight / clues as to the evolution that took place.

#### Small Parsimony Algorithm

`{bm} /(Algorithms\/Phylogeny\/Sequence Inference\/Small Parsimony Algorithm)_TOPIC/`

**ALGORITHM**:

Given a phylogenetic tree and the sequences for its leaf nodes (known entities), this algorithm infers sequences for its internal nodes (ancestor entities) based on how likely it is for sequence elements to change from one type to another. The sequence / sequence element most likely to be there is said to be the most parsimonious.

The algorithm only works on sequences of matching length.

```{note}
If you're interested to see why it's called small parsimony, see the next section which describes small parsimony vs large parsimony.
```

````{note}
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
````

The algorithm works by building a distance map for each index of each node's sequence. Each map defines the distance if that specific index were to contain that specific element. The shorter the distance, the more likely it is for that index to contain that specific element. For example, ...

|   |    A    |    C    |    T    |    G    |
|---|---------|---------|---------|---------|
| 0 |   1.0   | **0.0** |   4.0   |   3.0   |
| 1 |   2.0   |   2.0   | **1.0** |   3.0   |
| 2 |   1.0   |   1.0   | **0.0** |   1.0   |
| 3 |   2.0   |   3.0   |   1.0   | **0.0** |
| 4 |   1.0   |   1.0   | **0.0** |   1.0   |
| 5 |   1.0   | **0.0** |   1.0   |   2.0   |

These maps are built from the ground up, starting at leaf nodes and working their way "upward" through the internal nodes of the tree. Since the sequences at leaf nodes are known (leaf nodes represent known entities), building their maps is fairly straightforward: 0.0 distance for the element at that index and ∞ distance for all other elements. For example, the sequence ACTGCT would generate the following mappings at each index ...

|   |  A  |  C  |  T  |  G  |
|---|-----|-----|-----|-----|
| 0 | 0.0 |  ∞  |  ∞  |  ∞  |
| 1 |  ∞  | 0.0 |  ∞  |  ∞  |
| 2 |  ∞  |  ∞  | 0.0 |  ∞  |
| 3 |  ∞  |  ∞  |  ∞  | 0.0 |
| 4 |  ∞  | 0.0 |  ∞  |  ∞  |
| 5 |  ∞  |  ∞  | 0.0 |  ∞  |

```{output}
ch7_code/src/sequence_phylogeny/SmallParsimony.py
python
# MARKDOWN_LEAF_DIST_SET\s*\n([\s\S]+)\n\s*# MARKDOWN_LEAF_DIST_SET
```

Once all the downstream neighbours of an internal node have mappings, its mappings can be built by determining the minimized distance to reach each element. For example, imagine an internal node with 3 downstream neighbours...

```{svgbob}
                                              |
                                .-------------+-------------.
                                |             N1            |
                                |                           |
                                | "idx0: {A=?,C=?,T=?,G=?}" |
                                | "idx1: {A=?,C=?,T=?,G=?}" |
                                | "idx2: {A=?,C=?,T=?,G=?}" |
                                | "idx3: {A=?,C=?,T=?,G=?}" |
                                | "idx4: {A=?,C=?,T=?,G=?}" |
                                | "idx5: {A=?,C=?,T=?,G=?}" |
                                '-------------+-------------'
                                             /|\
               .----------------------------' | '----------------------------.
               |                              |                              |
.--------------+------------.   .-------------+-------------.   .------------+--------------.
|              N2           |   |             N3            |   |            N4             |
|                           |   |                           |   |                           |
| "idx0: {A=1,C=1,T=0,G=1}" |   | "idx0: {A=1,C=0,T=2,G=1}" |   | "idx0: {A=1,C=4,T=1,G=2}" |
| "idx1: {A=1,C=1,T=5,G=1}" |   | "idx1: {A=4,C=2,T=0,G=1}" |   | "idx1: {A=1,C=0,T=1,G=2}" |
| "idx2: {A=0,C=2,T=3,G=1}" |   | "idx2: {A=3,C=1,T=1,G=3}" |   | "idx2: {A=1,C=2,T=1,G=2}" |
| "idx3: {A=2,C=4,T=1,G=4}" |   | "idx3: {A=2,C=3,T=1,G=0}" |   | "idx3: {A=1,C=3,T=1,G=0}" |
| "idx4: {A=4,C=2,T=2,G=3}" |   | "idx4: {A=1,C=2,T=2,G=1}" |   | "idx4: {A=1,C=1,T=0,G=2}" |
| "idx5: {A=0,C=1,T=1,G=2}" |   | "idx5: {A=1,C=1,T=3,G=1}" |   | "idx5: {A=1,C=3,T=2,G=2}" |
'---------------------------'   '---------------------------'   '---------------------------'
```

To determine A's value for the mapping at index 3, pull in index 3 from all downstream nodes...

```{svgbob}
                                              |
                                .-------------+-------------.
                                |             N1            |
                                |                           |
                                | "idx3: {A=?            }" |
                                '-------------+-------------'
                                             /|\
               .----------------------------' | '----------------------------.
               |                              |                              |
.--------------+------------.   .-------------+-------------.   .------------+--------------.
|              N2           |   |             N3            |   |            N4             |
|                           |   |                           |   |                           |
| "idx3: {A=2,C=4,T=1,G=4}" |   | "idx3: {A=2,C=3,T=1,G=0}" |   | "idx3: {A=1,C=3,T=1,G=0}" |
'---------------------------'   '---------------------------'   '---------------------------'
```

For each downstream index 3 mapping, walk over each element and add in the distance from A to that element, then select the minimum value ...

```python
n2_val = min(
    N2[3]['A'] + dist_metric('A', 'A'),  # N2[3]['A']=2
    N2[3]['C'] + dist_metric('A', 'C'),  # N2[3]['C']=4
    N2[3]['T'] + dist_metric('A', 'T'),  # N2[3]['T']=1
    N2[3]['G'] + dist_metric('A', 'G')   # N2[3]['G']=4
)
n3_val = min(
    N3[3]['A'] + dist_metric('A', 'A'),  # N3[3]['A']=2
    N3[3]['C'] + dist_metric('A', 'C'),  # N3[3]['C']=3
    N3[3]['T'] + dist_metric('A', 'T'),  # N3[3]['T']=1
    N3[3]['G'] + dist_metric('A', 'G')   # N3[3]['G']=0
)
n4_val = min(
    N4[3]['A'] + dist_metric('A', 'A'),  # N4[3]['A']=1
    N4[3]['C'] + dist_metric('A', 'C'),  # N4[3]['C']=3
    N4[3]['T'] + dist_metric('A', 'T'),  # N4[3]['T']=1
    N4[3]['G'] + dist_metric('A', 'G')   # N4[3]['G']=0
)
```

The sum of all values generated above produces the distance for A in the mapping. You can think of this distance as the minimum cost of transitioning to / from A ...

```python
N1[3]['A'] = n2_val + n3_val + n4_val
```

This same process is repeated for the remaining elements in the mapping (C, T, and G) to generate the full mapping for index 3.

```{output}
ch7_code/src/sequence_phylogeny/SmallParsimony.py
python
# MARKDOWN_INTERNAL_DIST_SET\s*\n([\s\S]+)\n\s*# MARKDOWN_INTERNAL_DIST_SET
```

The algorithm builds these maps from the ground up, starting at leaf nodes and working their way "upward" through the internal nodes of the tree. Since phylogenetic trees are typically unrooted trees, a node needs to be selected as the root such that the algorithm can work upward to that root. The inferred sequences for internal nodes will very likely be different depending on which node is selected as root.

```{svgbob}
         .-----------.                            .-----------.          
         | AncestorA |                            | AncestorB |          
         '-----+-----'                            '-----+-----'          
              / \                                      /|\               
             /   \                                    / | \              
            /     \                                  /  |  \             
     .-----+-----. \                                /   |   \            
     | AncestorB |  \                              /    | .--+--------.  
     '-----+-----'   \                            /     | | AncestorA |  
          / \         \                          /      | '-----+-----'  
         /   \         \                        /       |        \        
        /     \         \                      /        |         \       
.------+-. .---+----. .--+-----.         .----+---. .---+----. .---+----.
|   Cat  | |  Lion  | |  Bear  |         |   Cat  | |  Lion  | |  Bear  |
'--------' '--------' '--------'         '--------' '--------' '--------'
```

```{note}
The Pevzner book claims this is dynamic programming. This is somewhat similar to how the backtracking sequence alignment path finding algorithm works (they're both graphs).
```

````{note}
If the tree is unrooted, the Pevzner book says to pick an edge and inject a fake root into it, then remove it once the sequences have been inferred. It says that if the tree is a binary tree and hamming distance is used as the metric, the same element type will win at every index of every node (lowest distance) regardless of which edge the fake root was injected into. At least I think that's what it says -- maybe it means the parsimony score will be the same (parsimony score discussed in next section).

If the tree isn't binary and/or something other than hamming distance is chosen as the metric, will this still be the case? If it isn't, I can't see how doing that is any better than just picking some internal node to be the root.

So which node should be selected as root? The tree structure being used for this algorithm very likely came from a phylogenetic tree built using distances (e.g. additive phylogeny, neighbour joining phylogeny, UPGMA, etc..). Here are a couple of ideas I just thought up: 

 * For each leaf node, count the number of nodes in the path to reach that internal node. Sum up the counts and pick the internal node with the largest sum as the root.
 * For each leaf node, calculate the distance to reach that internal node. Sum up the distances and pick the internal node with the largest sum as the root.

I think the second one might not work because all sums will be the same? Maybe instead average the distances to leaf nodes and pick the one with the largest average?
````

```{note}
The algorithm doesn't factor in distances (edge weights). For example, if an internal node has 3 children, and one has a much shorter distance than the others, shouldn't the shorter one's sequence elements be given more of a preference over the highers (e.g. higher probability of showing up)?
```

```{note}
In addition to small parsimony, there's large parsimony.

Small parsimony: When a tree structure and its leaf node sequences are given, derive the internal node sequences with the lowest possible distance (most parsimonious).

Large parsimony: When only the leaf node sequences are given, derive the combination of tree structure and internal node sequences with the lowest possible distance (most parsimonious).

Trying to do large parsimony explodes the search space (e.g. NP-complete), meaning it isn't realistic to attempt.
```

```{output}
ch7_code/src/sequence_phylogeny/SmallParsimony.py
python
# MARKDOWN_POPULATE\s*\n([\s\S]+)\n\s*# MARKDOWN_POPULATE
```

```{ch7}
sequence_phylogeny.SmallParsimony
[[n,Cat,ACTGGT], [n,Lion,ACTGCT], [n,Bear,ATTCCC], [n,i0], [n,i1], [e,Cat,i0], [e,Lion,i0], [e,i0,i1], [e,Bear,i1]]
i0
[ , A, C, T, G]
[A, 0, 1, 1, 1]
[C, 1, 0, 1, 1]
[T, 1, 1, 0, 1]
[G, 1, 1, 1, 0]
```

```{note}
The distance metric used in the example execution above is hamming distance. If you're working with proteins, a more appropriate matrix might be a BLOSUM matrix (e.g. BLOSUM62). Whatever you use, just make sure to negate the values if appropriate -- it should be such that the lower the distance the stronger the affinity.
```

#### Nearest Neighbour Interchange Algorithm

`{bm} /(Algorithms\/Phylogeny\/Sequence Inference\/Nearest Neighbour Algorithm)_TOPIC/`

```{prereq}
Algorithms/Phylogeny/Sequence Inference/Small Parsimony Algorithm_TOPIC
```

**ALGORITHM**:

The problem with small parsimony is that inferred sequences vary greatly based on both the given tree structure and the element distance metric used. Specifically, there are many ways in which...

 1. a phylogenetic tree structure can be generated (e.g. UPGMA, neighbour joining phylogeny, etc..).
 2. a distance can be generated between two elements of a sequence (e.g. PAM250, BLOSUM62, hamming distance, etc...).

Oftentimes the combination of tree structure and internal node sequences may be reasonable, but they likely aren't optimal (see large parsimony).

Given a phylogenetic tree where small parsimony has been applied, it's possible to derive a parsimony score: a measure of how likely the scenario is based on parsimony. For each edge, compute a weight by taking the two sequences at its ends and summing the distances between the element pairs at each index. For example, ...

```{svgbob}
.-----------.
|   Node1   |
|  ATTGCC   |
'-----+-----'        dist(A,A)=0
      |              dist(T,C)=1
    2 |              dist(T,T)=0
      |              dist(G,G)=0
.-----+-----.        dist(C,C)=0
|   Node2   |        dist(C,T)=1
|  ACTGCT   |
'-----------'
```

The sum of edge weights is the parsimony score of the tree (lower sum is better). For example, the following tree has a parsimony score of 4...

```{svgbob}
         .-----------.
         | AncestorA |
         |  ATTGCC   |
         '-----+-----'
              / \
           2 /   \
            /     \
     .-----+-----. \
     | AncestorB |  \ 1
     |  ACTGCT   |   \
     '-----+-----'    \
          / \          \
       1 /   \ 0        \
        /     \          \
.------+-. .---+----. .---+----.
|   Cat  | |  Lion  | |  Bear  |
| ACTGGT | | ACTGCT | | ATTCCC |
'--------' '--------' '--------'

"Parsimony score = 2+1+1+0 = 4"
```

```{output}
ch7_code/src/sequence_phylogeny/NearestNeighbourInterchange.py
python
# MARKDOWN_SCORE\s*\n([\s\S]+)\n\s*# MARKDOWN_SCORE
```

```{ch7}
sequence_phylogeny.NearestNeighbourInterchange main_parsimony_score
[[n,Cat,ACTGGT], [n,Lion,ACTGCT], [n,Bear,ATTCCC], [n,i0], [n,i1], [e,Cat,i0], [e,Lion,i0], [e,i0,i1], [e,Bear,i1]]
i0
[ , A, C, T, G]
[A, 0, 1, 1, 1]
[C, 1, 0, 1, 1]
[T, 1, 1, 0, 1]
[G, 1, 1, 1, 0]
```

The nearest neighbour interchange algorithm is a greedy heuristic which attempts to perturb the tree to produce a lower parsimony score. The core operation of this algorithm is to pick an internal edge within the tree and swap neighbours between the nodes at each end ...

```{svgbob}
                                   original
                                    1   2
                                    *   *
                                     \ / 
                                      *  
                                      |  
                                      *  
                                     /|\ 
                                    * * *
                                    7 8 9

                            "possible interchanges"
9   2    8   2    7   2    1   9    1   8    1   7    8   9    7   8    7   9
*   *    *   *    *   *    *   *    *   *    *   *    *   *    *   *    *   * 
 \ /      \ /      \ /      \ /      \ /      \ /      \ /      \ /      \ / 
  *        *        *        *        *        *        *        *        *  
  |        |        |        |        |        |        |        |        |  
  *        *        *        *        *        *        *        *        *  
 /|\      /|\      /|\      /|\      /|\      /|\      /|\      /|\      /|\ 
* * *    * * *    * * *    * * *    * * *    * * *    * * *    * * *    * * *
7 8 1    7 1 9    1 8 9    7 8 2    7 2 9    2 8 9    7 1 2    1 2 9    1 8 2
```

These swaps aren't just the nodes themselves, but the entire sub-trees under those nodes. For example, ...

```{svgbob}
   original                            "interchange on edge(G,H), swap D"
                                       "branch with K branch"
A   B      C                                              C     
*   *      *                                              *     
 \ /       |                                     K        |     
  * D    E *--* F                                *      E *--* F
   \      /                                       \      /      
  G *----* H                                     G *----* H     
   /     |\                                       /     |\      
  *      * *                                     *    J * * D   
  I      J K                                     I       / \
                                                        *   *
                                                        A   B     
```

```{output}
ch7_code/src/sequence_phylogeny/NearestNeighbourInterchange.py
python
# MARKDOWN_SWAP\s*\n([\s\S]+)\n\s*# MARKDOWN_SWAP
```

```{ch7}
sequence_phylogeny.NearestNeighbourInterchange main_nn_swap
[[n,Cat,ACTGGT], [n,Lion,ACTGCT], [n,Bear,ATTCCC], [n,Kangaroo,ATTCCT], [n,Elephant,TTTCCC], [n,i0], [n,i1], [n,i2], [e,Cat,i0], [e,Lion,i0], [e,i0,i1], [e,Bear,i1], [e,Kangaroo,i2], [e,Elephant,i2], [e,i0,i2]]
i0-i1
```

Given a tree, this algorithm goes over each internal edge and tries all possible neighbour swaps on that edge in the hopes of driving down the parsimony score. After all possible swaps are performed on every internal edge, the swap that produced the lowest parsimony score is chosen. If that parsimony score is lower than the parsimony score for the original tree, the swap is applied to the original and the process repeats.

```{output}
ch7_code/src/sequence_phylogeny/NearestNeighbourInterchange.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch7}
sequence_phylogeny.NearestNeighbourInterchange
[[n,Cat,ACTGGT], [n,Lion,ACTGCT], [n,Bear,ATTCCC], [n,Kangaroo,ATTCCT], [n,Elephant,TTTCCC], [n,i0], [n,i1], [n,i2], [e,Cat,i0], [e,Lion,i0], [e,i0,i1], [e,Bear,i1], [e,Kangaroo,i2], [e,Elephant,i2], [e,i0,i2]]
i0
[ , A, C, T, G]
[A, 0, 1, 1, 1]
[C, 1, 0, 1, 1]
[T, 1, 1, 0, 1]
[G, 1, 1, 1, 0]
```

## Gene Clustering

`{bm} /(Algorithms\/Gene Clustering)_TOPIC/`

Gene expression is the biological process by which a gene (segment of DNA) is synthesized into a gene product (e.g. protein).

```{svgbob}
       .----------------> mRNA --------------> "protein"
       | "transcribe"           "translate"    "(gene product)"
DNA   -+
(gene) |
       '----------------> "functional RNA"
         "transcribe"     "(gene product)"
```

When a gene encodes for ...

 * a protein, that gene is transcribed to mRNA which in turn is translated to that protein.
 * functional RNA, that gene is transcribed to a type of RNA that isn't mRNA (only mRNA is translated to a protein).

A snapshot of all RNA transcripts within a cell at a given point in time, called a transcriptome, can be captured using RNA sequencing technology. Both the RNA sequences and the counts of those transcripts (number of instances) are captured. Given that an RNA transcript is simply a transcribed "copy" of the DNA it came from (it identifies the gene), a snapshot indirectly shows the amount of gene expression taking place for each gene at the time that snapshot was taken.

|               | Count |
|---------------|-------|
| Gene / RNA A  |  100  |
| Gene / RNA B  |   70  |
| Gene / RNA C  |  110  |
| ...           |  ...  |

Differential expression analysis is the process of capturing multiple snapshots to help identify which genes are influenced by / responsible for some change. The counts from each snapshot are placed together to form a matrix called a gene expression matrix, where each row in the matrix is called a gene expression vector. Gene expression matrices typically come in two forms:

 * A time-course gene expression matrix captures snapshots at different points in time. For example, the following gene expression matrix captures snapshots at regular intervals to help identify which genes are affected by a drug. Notice that the gene expression vector for B lowers after the drug is administered while C's elevates ...

   |          | 1hr before drug given | 0hr before/after drug given | 1hr after drug given | ... |
   |----------|-----------------------|-----------------------------|----------------------|-----|
   | Gene A   | 100                   | 100                         | 100                  | ... |
   | Gene B   | 100                   |  70                         | 50                   | ... |
   | Gene C   | 100                   | 110                         | 140                  | ... |
   | ...      | ...                   | ...                         | ...                  | ... |

   If a gene expression vector elevates/lowers across the set of snapshots, it may indicate that the gene is either responsible for or influenced by what happened.

   ```{svgbob}
            "GENE X"                              "GENE Y"                             "GENE Z"      
   |                                    |                                    |                       
   |  *----*                            |                 *                  |                       
   |        \                           |                /                   |                        
   |         \                          |               /                    |                       
   |          *---*                     |          *---*                     |  *---*---*---*---*        
   |               \                    |         /                          |                       
   |                \                   |        /                           |                       
   |                 *                  |  *----*                            |                       
   |                                    |                                    |                       
   +-----------------------             +-----------------------             +-----------------------
   ```

   Similarly, if two or more gene expression vectors elevate/lower in a similar pattern, it could mean that the genes they represent either perform similar functions or are co-regulated (e.g. each gene is influenced by the same transcription factor).

   ```{svgbob}
        "GENES W and X"                  "GENES U and T"    
   |                                |                       
   |  *----*                        |  *             
   |  *----*\                       |  *\            
   |        \\                      |   \\           
   |         \*---*                 |    \*        
   |          *---*\                |     *\       
   |               \\               |      \\      
   |                \*              |       \*---*----*
   |                 *              |        *---*----*  
   +-----------------------         +-----------------------
   ```

   With time-course gene expression matrices, biologists typically determine which genes _may_ be related to a change by grouping together similar gene expression vectors. The goal is for the gene expression vectors in each group to be more similar to each other than to those in other groups. The process of grouping items together in this way is called clustering, and each group formed by the process is called a cluster. For example, the gene expression matrix below clearly forms two clusters if the similarity metric is the euclidean distance between points...

   |        | 1hr before | 1hr after |
   |--------|------------|-----------|
   | Gene A |     5      |     1     |
   | Gene B |     20     |     1     |
   | Gene C |     24     |     4     |
   | Gene D |     1      |     2     |
   | Gene E |     3      |     4     |
   | Gene F |     22     |     4     |

   ```{svgbob}
    cluster1         cluster2
   |
   |   E                F C
   |D  A              B        
   +---------------------------
   ```

   ```{note}
   The goal described above is referred to as the good clustering principle.
   ```

   In the above example, cluster 1 reveals genes that weren't impacted while cluster 2 reveals genes that had their expression drastically lowered.

 * A conditional gene expression matrix captures snapshots in different states / conditions. For example, there exists some set of genes that are transcribed more / less when comparing a ...

    * cancerous blood cell vs non-cancerous blood cell.
    * rose cell that's bloomed vs rose cell that's unbloomed.
    * bacteria cell when flagella is moving vs bacteria cell when flagella is still.
    * mouse cell that's inflamed vs mouse cell that's un-inflamed.

   |          | patient1 (cancer) | patient2 (cancer) | patient3 (non-cancer) | ... |
   |----------|-------------------|-------------------|-----------------------|-----|
   | Gene A   | 100               | 100               | 100                   | ... |
   | Gene B   | 100               | 110               | 50                    | ... |
   | Gene C   | 100               | 110               | 140                   | ... |
   | ...      | ...               | ...               | ...                   | ... |

   The goal is to find the relationship between genes and the conditions in question. The idea is that a set of genes are likely influenced by / responsible for the condition, where those genes have different gene expression patterns depending on the condition. In the example above, gene B has double the gene expression when cancerous.
   
   One typical scenario for this type of analysis is to devise a test for some condition that isn't immediately visible: Snapshots are taken for each possibility (e.g. leukemia vs non-leukemia cells) and the appropriate genes along with their gene expression patterns are identified (e.g. maybe 15 out of 5000 genes are related to leukemia). Then, a new never before seen snapshot can be tested by comparing the gene expression levels of those genes.
   
   Whereas with time-course gene expression the primary form of analysis is clustering, the analysis for conditional gene expression is more loose: it may or may not involve clustering in addition to other statistical analyses.

```{note}
This section mostly details clustering algorithms with time-course gene expression matrix examples.
```

Real-world gene expression matrices are often much more complex than the examples shown above. Specifically, ...

 1. there are often more than two columns to a gene expression matrix (more than two dimensions), meaning that the clustering becomes non-trivial.
 2. RNA sequencing is an inherently biased / noisy process, meaning that certain RNA transcript counts elevating or lowering could be bad data.
 3. RNA transcript counts can fluctuate due to normal cell operations (e.g. genes regulated by circadian clock), meaning that certain RNA transcript counts elevating or lowering doesn't necessarily mean that they're relevant. This especially becomes a problem in state-based gene expression matrices where variables can't be as tightly controlled (e.g. in the blood cancer example above,the samples include people at different stages of cancer, could have been taken at different times of day, etc..).
 
Prior to clustering, RNA sequencing outputs typically have to go through several rounds of processing (cleanup / normalization) to limit the impact of the last two points above. For example, biologists often take the logarithm of a count rather than the count itself. 

```{svgbob}
   "no log"             "log"
                    
  |                               
  |                            
  |                 
  |                 
  |                 
  |   |   |            |
| | | | | | |          |           
| | | | | | |        | | | | | | |   
+-+-+-+-+-+-+        +-+-+-+-+-+-+
```

```{note}
The Pevzner book says taking the logarithm is common. It never said why taking the logarithm is important. Some of the NCBI gene expression omnibus datasets that I've looked at also use logarithms while others use raw counts or "normalized counts".

This section doesn't cover de-noising or de-biasing. It only covers clustering and common similarity / distance metrics for real-valued vectors (which are what gene expression vectors are). Note that clustering can be used with data types other than vectors. For example, you can cluster protein sequences where the similarity metric is the BLOSUM62 score.
```

### Euclidean Distance Metric

`{bm} /(Algorithms\/Gene Clustering\/Euclidean Distance Metric)_TOPIC/`

**WHAT**: Given two n-dimensional vectors, compute the distance between those vectors if traveling directly from one to the other in a straight line, referred to as the euclidean distance.

```{svgbob}
   *
    \
     \ d
      \
       * 
```

**WHY**: This is one of many common metrics used for clustering gene expression vectors. One way to think about it is that it checks to see how closely component plots of the vectors match up. For example, ...

|        | hour0 | hour1 | hour2 | hour3 |
|--------|-------|-------|-------|-------|
| Gene A |  2    | 10    | 2     | 10    |
| Gene B |  2    | 8     | 2     | 8     |
| Gene C |  2    | 2     | 2     | 10    |

```{svgbob}
"plot of (2,10,2,10)'s"          "plot of (2,8,2,8)'s"            "plot of (2,2,2,10)'s"
"components by index"            "components by index"            "components by index"
                                                                                
  10|     *       *               10|                              10|             *
v  8|    / \     /              v  8|    *     *                 v  8|            / 
a  6|   /   \   /               a  6|   / \   /                  a  6|           /  
l  4|  /     \ /                l  4|  /   \ /                   l  4|          /   
u  2| *       *                 u  2| *     *                    u  2| *---*---*      
e  0|                           e  0|                            e  0|              
    +--------------                 +-----------                     +--------------
      0   1   2   3                   0  1  2  3                       0   1   2   3
         index                           index                            index     
```

* `dist((2,10,2,10), (2,8,2,8)) = 2.82`
* `dist((2,10,2,10), (2,2,2,10)) = 8`
* `dist((2,8,2,8), (2,2,2,10)) = 6.325`

**ALGORITHM**:

The algorithm extends the basic 2D distance formula from highschool math to multiple dimensions. Recall that two compute the distance between two...

 * 2D points is `{kt} \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}`.
 * 3D points is `{kt} \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2 + (z_2 - z_1)^2}`.

In n dimensional space, this is calculated as `{kt} \sqrt{\sum_{i=1}^n{(v_i - w_i)^2}}`, where v and w are two n dimensional points.

```{output}
ch8_code/src/metrics/EuclideanDistance.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch8}
metrics.EuclideanDistance
[
  [0.0, 1.0, 2.0],
  [2.0, 1.0, 0.0]
]
```

### Manhattan Distance Metric

`{bm} /(Algorithms\/Gene Clustering\/Manhattan Distance Metric)_TOPIC/`

**WHAT**: Given two n-dimensional vectors, compute the distance between those vectors if traveling only via the axis of the coordinate system, referred to as the manhattan distance.

```{svgbob}
   *
   | 
 dx|
   |  
   +--* 
    dy
```

**WHY**: This is one of many common metrics used for clustering gene expression vectors.  One way to think about it is that it checks to see how closely component plots of the vectors match up. For example, ...

|        | hour0 | hour1 | hour2 | hour3 |
|--------|-------|-------|-------|-------|
| Gene A |  2    | 10    | 2     | 10    |
| Gene B |  2    | 8     | 2     | 8     |
| Gene C |  2    | 2     | 2     | 10    |

```{svgbob}
"plot of (2,10,2,10)'s"          "plot of (2,8,2,8)'s"            "plot of (2,2,2,10)'s"
"components by index"            "components by index"            "components by index"
                                                                                
  10|     *       *               10|                              10|             *
v  8|    / \     /              v  8|    *     *                 v  8|            / 
a  6|   /   \   /               a  6|   / \   /                  a  6|           /  
l  4|  /     \ /                l  4|  /   \ /                   l  4|          /   
u  2| *       *                 u  2| *     *                    u  2| *---*---*      
e  0|                           e  0|                            e  0|              
    +--------------                 +-----------                     +--------------
      0   1   2   3                   0  1  2  3                       0   1   2   3
         index                           index                            index     
```

* `dist((2,10,2,10), (2,8,2,8)) = 4`
* `dist((2,10,2,10), (2,2,2,10)) = 8`
* `dist((2,8,2,8), (2,2,2,10)) = 8`

**ALGORITHM**:

The algorithm sums the absolute differences between the elements at each index: `{kt} \sum_{i=1}^n{|v_i - w_i|}`, where v and w are two n dimensional points. The absolute differences are used because a distance can't be negative.

```{output}
ch8_code/src/metrics/ManhattanDistance.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch8}
metrics.ManhattanDistance
[
  [0.0, 1.0, 2.0],
  [2.0, 1.0, 0.0]
]
```

### Cosine Similarity Metric

`{bm} /(Algorithms\/Gene Clustering\/Cosine Similarity Metric)_TOPIC/`

**WHAT**: Given two n-dimensional vectors, compute the cosine of the single between them, referred to as the cosine similarity.

```{svgbob}
    ^
   /
  /
 / a 
+---------------> 
```

This metric only factors in the angles between vectors, not their magnitudes (lengths). For example, imagine the following 2-dimensional gene expression vectors ...

|        | before | after |
|--------|--------|-------|
| Gene U |  9     | 9     |
| Gene T |  15    | 32    |
| Gene C |  3     | 0     |
| Gene J |  21    | 21    |

 * Gene U's count remained unchanged while gene C's count lowered to zero. The angle between those vectors is 45deg.

   ```{svgbob}
   "angle between U and C"
   "U=(9, 9)"
   "C=(3, 0)"

         .' 
     U .' 
     .' 
   .' 45
    ---
     C
   ```

 * Gene U's count remained unchanged while gene T's count approximately doubled. The angle between those vectors is roughly 20deg. 

   ```{svgbob}
   "angle between U and T"
   "U=(9, 9)"
   "T=(15, 32)"

           /
          /
         /
      T /
       /     
      / 20   
     /   .'
    /  .'  
     .' U
   .'
   ```

 * Gene C's count lowered to zero but gene T's count approximately doubled. The angle between those vectors is roughly 65deg. 

   ```{svgbob}
   "angle between C and T"
   "C=(3, 0)"
   "T=(15, 32)"

           /
          /
         /
      T /
       /     
      /     
     /                               
    /  65
    ---
     C
   ```

 * Gene U and gene J's counts are different but both remained unchanged. The angle between those vectors is 0deg.

   ```{svgbob}
   "angle between U and J"
   "U=(9, 9)"
   "J=(21, 21)"

                                  .'
                                .'
                              .'
                         J  .'
                          .'
         .'             .' 
     U .'             .'   
     .'             .'    
   .'             .'      

   "Note: Separate because not possible to"
   "differentiate between vectors if overlapping."
   ```

What's being compared is the trajectory at which the counts changed (angle between vectors), not the counts themselves (vector magnitudes). Given two gene expression vectors, if they grew/shrunk at ...

 * exactly the same trajectory (angle of 0deg), they'll have maximum similarity: 0deg.
 * completely opposite trajectories, they'll have maximum dissimilarity: 180deg.

Since the algorithm is calculating the cosine of the angle, the metric returns a result from from 1 to -1 instead of 0deg to 180deg, where ...

 * maximum similarity is cos(0deg) = 1.
 * minimum similarity is cos(180deg) = -1.

**WHY**: Imagine the following two 4-dimensional gene expression vectors...

|        | hour0 | hour1 | hour2 | hour3 |
|--------|-------|-------|-------|-------|
| Gene A |  2    | 10    | 2     | 10    |
| Gene B |  1    | 5     | 1     | 5     |

Plotting out each component of the gene expression vectors above reveals that gene B's expression is a scaled down version of gene A's expression ...

```{svgbob}
"plot of (2,10,2,10)'s components by index"    "plot of (1,5,1,5)'s components by index"

  10|     *       *
v  8|    / \     /                              v  9|
a  6|   /   \   /                               a  7|
l  4|  /     \ /                                l  5|   *   *
u  2| *       *                                 u  3|  / \ /
e  0|                                           e  1| *   *  
    +--------------                                 +---------
      0   1   2   3                                   0 1 2 3
         index                                         index
```

The cosine of the angle between gene A's expression and gene B's expression is 1.0 (maximum similarity). This will always be the case as long as one gene's expression is a linearly scaled version of the other gene's expression. For example, the cosine similarity of ...

 * (1, 5, 1, 5) and (1, 5, 1, 5) is 1.0 -- scaled 1x from first to second
 * (1, 5, 1, 5) and (2, 10, 2, 10) is 1.0 -- scaled 2x from first to second
 * (1, 5, 1, 5) and (3, 15, 3, 15) is 1.0 -- scaled 3x from first to second
 * (1, 5, 1, 5) and (1.5, 7.5, 1.5, 7.5) is 1.0 -- scaled 1.5x from first to second
 * (1, 5, 1, 5) and (0.5, 2.5, 0.5, 2.5) is 1.0 -- scaled 0.5x from first to second

````{note}
Still confused? Scaling makes sense if you think of it in terms of angles. The vectors (5,5) vs (10,10) have the same angle. Any vector with the same angle is just a scaled version of the other -- each of its components are scaled by the same constant...

* (10,10) is (5,5) with each component scaled by 2.0x
* (5,5) is (10,10) with each component scaled by 0.5x

```{svgbob}
                              "(10,10)"
                               .'
                             .'
                           .'
                         .'
      "(5,5)"          .'
      .'             .' 
    .'             .'   
  .'             .'    
.' 45          .'  45  
--------       ----------
```
````

While cosine similarity does take into account scaling of components, _it doesn't support shifting of components_. Imagine the following 4-dimensional gene expression vectors...

|        | hour0 | hour1 | hour2 | hour3 |
|--------|-------|-------|-------|-------|
| Gene A |  2    | 10    | 2     | 10    |
| Gene B |  1    | 5     | 1     | 5     |
| Gene C |  5    | 9     | 5     | 9     |

Plotting out each component of the gene expression vectors above reveals that...

 * B is a scaled down version of A (by 0.5x).
 * C is a shifted version of B (by +4).
 * C is a scaled down and shifted version of A (by 0.5x and +4).

```{svgbob}
"plot of (2,10,2,10)'s components by index"    "plot of (1,5,1,5)'s components by index"    "plot of (5,9,5,9)'s components by index"
                                                                                                           
  10|     *       *                                                                                        
v  8|    / \     /                              v  9|                                        v  9|   *   * 
a  6|   /   \   /                               a  7|                                        a  7|  / \ /  
l  4|  /     \ /                                l  5|   *   *                                l  5| *   *   
u  2| *       *                                 u  3|  / \ /                                 u  3|         
e  0|                                           e  1| *   *                                  e  1|         
    +--------------                                 +---------                                   +---------
      0   1   2   3                                   0 1 2 3                                      0 1 2 3 
         index                                         index                                        index  
```

All gene expression vectors follow the same pattern, notice that ...

 * B is A where each component has been scaled by 0.5x, cosine similarity is 1.0 (maximum similarity).
 * C is A where each component has been scaled by 0.5x then shifted up by 4, cosine similarity is 0.992.
 * C is B where each component has been shifted up by 4, cosine similarity is 0.992.

Even though the patterns are the same across all three gene expression vectors, cosine similarity gets thrown off in the presence of shifting.

```{note}
If you're trying to determine if the components of the gene expression vectors follow the same pattern regardless of scale, the lack of shift support seems to make this unusable. The gene expression vectors may follow similarly scaled patterns but it seems likely that each pattern is at an arbitrary offset (shift). So then what's the point of this? Why did the book mention it for gene expression analysis?

Pearson similarity seems to factor in both scaling and shifting. Use that instead.
```

**ALGORITHM**:

Given the vectors A and B, the formula for the algorithm is as follows ...

```{kt}
cos(\theta) = \frac{A \cdot B}{||A|| \: ||B||}
```

The formula is confusing in that the ...

 * central dot is the dot-product between vectors: `{kt} A \cdot B = \sum_{i=1}^n {A_i \cdot B_i}`.
 * double pipe encapsulation represents the magnitude of a vector: `{kt} ||A|| = \sqrt{\sum_{i=1}^{n} {A_i^2}}`.
 * two double pipe encapsulations is a multiplication of vector magnitudes: `{kt} ||A|| \: ||B|| = ||A|| \cdot ||B||`

```{kt}
cos(\theta) = \frac{\sum_{i=1}^n {A_i \cdot B_i}}{\sqrt{\sum_{i=1}^n {A_i^2}} \cdot \sqrt{\sum_{i=1}^n {B_i^2}}}
```

```{note}
What is the formula actually calculating / what's the reasoning behind the formula? The only part I understand is the magnitude calculation, which is just the euclidean distance between the origin and the coordinates of a vector. For example, the magnitude between (0,0) and (5,7) is calculated as sqrt((5-0)^2 + (7-0)^2). Since the components of the origin are all always going to be 0, it can be shortened to sqrt(5^2 + 7^2).

The rest of it I don't understand. What is the dot product actually calculating? And why multiply the magnitudes and divide? How does that result in the cosine of the angle?
```

```{output}
ch8_code/src/metrics/CosineSimilarity.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch8}
metrics.CosineSimilarity
[
  [9.0, 9.0, 9.0],
  [90.0, 90.0, 95.0]
]
```

### Pearson Similarity Metric

`{bm} /(Algorithms\/Gene Clustering\/Pearson Similarity Metric)_TOPIC/`

```{prereq}
Algorithms/Gene Clustering/Cosine Similarity Metric_TOPIC
```

```{note}
A lot of what's below is my understanding of what's going on, which I'm almost certain is flawed. I've put up a [question asking for help](https://stats.stackexchange.com/q/558913).
```

**WHAT**: Given two n-dimensional vectors, ...

1. pair together each index to produce a set of 2D points.

   ```{svgbob}
   "vector A =" (1, 6, 5, 9)
   "vector B =" (3, 8, 4, 8)
                 |  |  |  |
                 |  |  |  '-- "(9, 8)"
                 |  |  '----- "(5, 4)"
                 |  '-------- "(6, 8)"
                 '----------- "(1, 3)"
   ```

2. fit a straight line to those points.

   ```{svgbob}
   "vector A =" (1, 6, 5, 9)
   "vector B =" (3, 8, 4, 8)
                 |  |  |  |
                 |  |  |  '-- "(9, 8)"
                 |  |  '----- "(5, 4)"
                 |  '-------- "(6, 8)"
                 '----------- "(1, 3)"

     9|                .'
      |           ●  .' ● 
     7|            .'   
      |          .'      
   B 5|        .'        
      |      .' ●         
     3| ●  .'            
      |  .'              
     1|.'                
      +-------------------
        1   3   5   7   9
                A
   ```

3. quantify the proximity of those points to the fitted line, where the proximity of larger points contribute more to a strong similarity than smaller points. The quantity ranges from 0.0 (loose proximity) and 1.0 (tight proximity), negating the if the slope of the fitted line is negative.

   ```{svgbob}
   "* r is the proximity quantity described above."

   "vector A = (0, 1, 1, 0, 5,  2, 1, 6)"            "vector A = (1,  2.5, 3, 6.5, 8, 8.5, 9.5)"       "vector A = (1, 3, 5, 7, 9, 11, 13)"
   "vector B = (1, 0, 2, 0, 10, 0, 2, 14)"           "vector B = (14, 11,  13,  2, 3, 2,   2)"         "vector B = (5, 7, 5, 7, 5, 7,  5)"
                                                                                                                                                  
                    "r = 0.95"                                       "r = -0.95"                                      "r = 0.0"           
                                                                                                                                                  
     15|               /                               15|   \                                           15|                                        
       |             ●/                                  |   ●\                                            |                                        
     13|             /                                 13|     \ ●                                       13|                                        
       |            /                                    |      \                                          |                                        
     11|           /                                   11|      ●\                                       11|                                        
       |          /●                                     |        \                                        |                                        
      9|         /                                      9|         \                                      9|                                        
   B   |        /                                    B   |          \                                  B   |                                        
      7|       /                                        7|           \                                    7|       ●       ●       ●                
       |      /                                          |            \                                    |  ----------------------------          
      5|     /                                          5|             \                                  5|   ●       ●       ●       ●            
       |    /                                            |              \                                  |                                        
      3|   /                                            3|               \ ●                              3|                                        
       |  /●                                             |              ● \ ● ●                            |                                        
      1|●/   ●                                          1|                                                1|                                        
       |●  ●                                             |                                                 |                                        
       +----------------------------------               +----------------------------------               +----------------------------------      
           1   3   5   7   9   11  13  15                    1   3   5   7   9   11  13  15                    1   3   5   7   9   11  13  15       
                         A                                                 A                                                 A
   ```

**WHY**: Imagine the following 4-dimensional gene expression vectors...

|        | hour0 | hour1 | hour2 | hour3 |
|--------|-------|-------|-------|-------|
| Gene A |  2    | 10    | 2     | 10    |
| Gene B |  1    | 5     | 1     | 5     |
| Gene C |  5    | 9     | 5     | 9     |

Plotting out each component of the gene expression vectors above reveals that ...

 * B is a scaled down version of A (by 0.5x).
 * C is a shifted version of B (by +4).
 * C is a scaled down and shifted version of A (by 0.5x and +4).

```{svgbob}
"plot of (2,10,2,10)'s"          "plot of (1,5,1,5)'s"           "plot of (5,9,5,9)'s"
"components by index"            "components by index"           "components by index"
                                                                                
  10|     *       *                                                            
v  8|    / \     /               v  9|                           v  9|   *   * 
a  6|   /   \   /                a  7|                           a  7|  / \ /  
l  4|  /     \ /                 l  5|   *   *                   l  5| *   *   
u  2| *       *                  u  3|  / \ /                    u  3|         
e  0|                            e  1| *   *                     e  1|         
    +--------------                  +---------                      +---------
      0   1   2   3                    0 1 2 3                         0 1 2 3 
         index                          index                           index  
```

Pearson similarity returns 1.0 (maximum similarity) for all possible comparison of the three gene expression vectors above. Note that this isn't the case with cosine similarity. Cosine similarity gets thrown off in the presence of shifting while pearson similarity does not.

|        | Cosine similarity | Pearson similarity |
|--------|-------------------|--------------------|
| B vs A | 1.0               | 1.0                |
| C vs A | 0.992             | 1.0                |
| C vs B | 0.992             | 1.0                |

Similarly, comparing a gene expression vector with a mirror (across the X-axis) that has been scaled and / or shifted will result in a pearson similarity of -1.0.

```{svgbob}
"plot of (2,10,2,10)'s"          "plot of (9,5,9,5)'s"
"components by index"            "components by index"
                                                
  10|     *       *                             
v  8|    / \     /                v  9| *   * 
a  6|   /   \   /                 a  7|  \ / \  
l  4|  /     \ /                  l  5|   *   *  
u  2| *       *                   u  3|         
e  0|                             e  1|         
    +--------------                   +---------
      0   1   2   3                     0 1 2 3 
         index                           index  
```

````{note}
If you're trying to determine if the components of the gene expression vectors follow the same pattern regardless of scale OR offset, this is the similarity to use. They may have similar patterns even though they're scaled differently or offset differently. For example, both genes below may be influenced by the same transcription factor, but their base expression rates are different so the transcription factor influences their gene expression proportionally.

```{svgbob}
"gene A's expression"          "gene B's expression"
"across time-points"           "across time-points"
                               
   10|     *       *                                    
 v  8|    / \     /             v  9|         
 a  6|   /   \   /              a  7|   *   * 
 l  4|  /     \ /               l  5|  / \ / 
 u  2| *       *                u  3| *   *  
 e  0|                          e  1| 
     +--------------                +---------
       0   1   2   3                  0 1 2 3 
          index                        index  
```
````

**ALGORITHM**:

Given the vectors A and B, the formula for the algorithm is as follows ...

```{kt}
r_{AB} = \frac{\sum_{i=1}^n {(A_i - avg(A))(B_i - avg(B))}}{\sqrt{\sum_{i=1}^n {(A_i - avg(A))^2}} \cdot \sqrt{\sum_{i=1}^n {(B_i - avg(B))^2}}}
```

```{note}
Much like cosine similarity, I can't pinpoint exactly what it is that the formula is calculating / the reasoning behind the calculations. The only part I somewhat understand is where it's getting the euclidean distance to the average of each vector.

The rest of it I don't understand.
```

```{output}
ch8_code/src/metrics/PearsonSimilarity.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch8}
metrics.PearsonSimilarity
[
  [2, 10, 4, 12, 6, 14],
  [5, 9,  6, 10, 7, 11]
]
```

````{note}
What do you do on division by 0? Division by 0 means that the point pairings boil down to a  single point. There is no single line that "fits" through just 1 point (there are an infinite number of lines).

```{svgbob}
"* r is the proximity quantity described above."

"vector A = (5, 5, 5, 5)"
"vector B = (7, 7, 7, 7)"
                                           
                                           
  15|                                        
    |                                        
  13|                                        
    |                                        
  11|                                        
    |                                        
   9|                                        
B   |                                        
   7|           ●
    |  
   5|  
    |                                        
   3|                                        
    |                                        
   1|                                        
    |                                        
    +----------------------------------      
        1   3   5   7   9   11  13  15       
                      A
```

So what's the correct action to take in this situation? Assuming that both vectors consist of a single value repeating n times (can there be any other cases where this happens?), then maybe what you should do is set it as maximally correlated (1.0)? If you think about it in terms of the "pattern matching" component plots discussion, each vector's component plot is a straight line.

```{svgbob}
"plot of (5,5,5,5)'s"     "plot of (7,7,7,7)'s"   
"components by index"     "components by index"
                                               
                                               
 v  9|                    v  9|              
 a  7|                    a  7| *-*-*-*             
 l  5| *-*-*-*            l  5| 
 u  3|                    u  3|               
 e  1|                    e  1|               
     +---------               +---------      
       0 1 2 3                  0 1 2 3       
        index                    index        
```

It could just as well be interpreted as having no correlation (-1.0) because a mirror of a straight line (across the x-axis, as discussed above) is just the same straight line?

I don't know what the correct thing to do here is. My instinct is to mark it as maximum correlation (1.0) but I'm almost certain that that'd be wrong. The Internet isn't providing many answers -- they all say it's either undefined or context dependent.
````

### K-Centers Clustering

`{bm} /(Algorithms\/Gene Clustering\/K-Centers Clustering)_TOPIC/`

```{prereq}
Algorithms/Gene Clustering/Euclidean Distance Metric_TOPIC
```

**WHAT**: Given a list of n-dimensional points (vectors), choose a predefined number of points (k), called centers. Each center identifies a cluster, where the points closest to that center (euclidean distance) are that cluster's member_CLUSTERs. The goal is to choose centers such that, out of all possible cluster center to member_CLUSTER distances, the farthest distance is the minimum it could possibly be out of all possible choices for centers.

In terms of a scoring function, the score being minimized is ...

```{kt}
score = max(d(P_1, C), d(P_2, C), ..., d(P_n, C))
```

* P is the set of points.
* C is the set of centers.
* n is the number of points in P
* d returns the euclidean distance between a point and its closest center.
* max is the maximum function.

```python
# d() function from the formula
def dist_to_closest_center(data_pt, center_pts):
  center_pt = min(
    center_pts,
    key=lambda cp: dist(data_pt, cp)
  )
  return dist(center_pt, data_pt)

# scoring function (what's trying to be minimized)
def k_centers_score(data_pts, center_pts):
  return max(dist_to_closest_center(p, center_pts) for p in data_pts)
```

```{svgbob}
"Points are 2D gene expression vectors. Each point is represented as"
"a letter, where the letter defines which cluster it belongs to. Each"
"line is from a point to its cluster center."

           "bad centers"                                 "good centers"     
                                                                                 
|    C                                        |    C                             
|     \                                       |    |                             
|C ----●                                      |C --●                             
|     /                                       |    |                             
|    C                                        |    C                             
|                                             |                                  
|                                             |                                  
|                                             |                                  
|           ●                                 |                                  
|          /|\                                |                           
|         / | \                               |                           
|        D  |  D                              |        D     D                    
|           |                                 |         '. .'                    
|           |                                 |           ●                      
|           |                                 |           |                      
|           D                                 |           D                      
+----------------------------------           +----------------------------------
```

**WHY**: This is one of the methods used for clustering gene expression vectors. Because it's limited to use euclidean distance as the metric, it's essentially clustering by how close the component plots match up. For example, ...

|        | hour0 | hour1 | hour2 | hour3 |
|--------|-------|-------|-------|-------|
| Gene A |  2    | 10    | 2     | 10    |
| Gene B |  2    | 8     | 2     | 8     |
| Gene C |  2    | 2     | 2     | 10    |

```{svgbob}
"plot of (2,10,2,10)'s"          "plot of (2,8,2,8)'s"            "plot of (2,2,2,10)'s"
"components by index"            "components by index"            "components by index"
                                                                                
  10|     *       *               10|                              10|             *
v  8|    / \     /              v  8|    *     *                 v  8|            / 
a  6|   /   \   /               a  6|   / \   /                  a  6|           /  
l  4|  /     \ /                l  4|  /   \ /                   l  4|          /   
u  2| *       *                 u  2| *     *                    u  2| *---*---*      
e  0|                           e  0|                            e  0|              
    +--------------                 +-----------                     +--------------
      0   1   2   3                   0  1  2  3                       0   1   2   3
         index                           index                            index     
```

* `dist((2,10,2,10), (2,8,2,8)) = 2.82`
* `dist((2,10,2,10), (2,2,2,10)) = 8`
* `dist((2,8,2,8), (2,2,2,10)) = 6.325`

In addition to only being able to use euclidean distance, another limitation is that it requires knowing the number of clusters (k) beforehand. Other clustering algorithms exist that don't have either restriction.

**ALGORITHM**:

Solving k-centers for any non-trivial input isn't possible because the search space is too huge. Because of this, heuristics are used. A common k-centers heuristic is the farthest first traversal algorithm. The algorithm iteratively builds out more centers by inspecting the euclidean distances from points to existing centers. At each step, the algorithm ...

 1. gets the closest center for each point,
 1. picks the point with the farthest euclidean distance and sets it as the new center.

The algorithm initially primes the list of centers with a randomly chosen point and stops executing once it has k points.

```{output}
ch8_code/src/clustering/KCenters_FarthestFirstTraversal.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch8}
clustering.KCenters_FarthestFirstTraversal
[
  3,
  [
    [2,2], [2,4], [2.5,6], [3.5,2], [4,3], [4,5], [4.5,4],
    [7,2], [7.5,3], [8,1], [9,2],
    [8,7], [8.5,8], [9,6], [10,7]
  ]
]
```

One problem that should be noted with this heuristic is that, when outliers are present, it'll likely place those outliers into their own cluster. 

```{svgbob}
"Cluster membership is denoted using letters. Points"
"chosen as centers are in brackets"

"When k=3, each outlier may become become its own"
"cluster, leaving everything else as the last cluster."

          "no outliers"                                       "with outliers"       

|                                                |                                 [C] 
|                                                |                                       
|                                                |                                      
|                                                |                                      
|                C                               |                E                     
|               C  [C]                           |               E   E                  
|    D            C                              |    E            E                    
|       D                                        |       E                             
|  [D]   D                                       |  [E]   E                             
|       D      E                                 |       E      E                       
|   D  D      E   E                              |   E  E      E   E                    
|               [E]                              |               E                      
|                                                |                                      
|                                                |                                     
|                                                |                                     
|                                                |                                  [D] 
+--------------------------------------          +--------------------------------------
```

### K-Means Clustering

`{bm} /(Algorithms\/Gene Clustering\/K-Means Clustering)_TOPIC/`

```{prereq}
Algorithms/Gene Clustering/Euclidean Distance Metric_TOPIC
Algorithms/Gene Clustering/K-Centers Clustering_TOPIC
```

**WHAT**: Given a list of n-dimensional points (vectors), choose a predefined number of points (k), called centers. Each center identifies a cluster.

K-means is k-centers except the scoring function is different. Recall that the scoring function (what's trying to be minimized) for k-centers is ...

```{kt}
score = max(d(P_1, C), d(P_2, C), ..., d(P_n, C))
```

... where ...

* P is the set of points.
* C is the set of centers.
* n is the number of points in P
* d returns the euclidean distance between a point and its closest center.
* max is the maximum function.

The scoring function for k-means, called squared error distortion, is as follows ...

```{kt}
score = \frac{\sum_{i=1}^{n} {d(P_i, C)^2}}{n}
```

```{note}
The formula is taking the squares of d() and averaging them.
```

```python
# d() function from the formula
def dist_to_closest_center(data_pt, center_pts):
  center_pt = min(
    center_pts,
    key=lambda cp: dist(data_pt, cp)
  )
  return dist(center_pt, data_pt)

# scoring function (what's trying to be minimized)
def k_means_score(data_pts, center_pts):
  res = []
  for data_pt in data_pts:
    dist_to = dist_to_closest_center(data_pt, center_pts)
    res.append(dist_to ** 2)
  return sum(res) / len(res)
```

Compared to k-centers, cluster membership_NORM is still decided by the distance to its closest cluster (d in the formula above). It's the placement of centers that's different.

```{note}
There's a version of k-centers / k-means for similarity metrics / distance metrics other than euclidean distance. It's called k-medoids but I haven't had a chance to look at it yet and it wasn't covered by the book.

 * [link 1](https://stats.stackexchange.com/a/81496)
 * [link 2](https://stats.stackexchange.com/a/32942)
```

**WHY**: K-means is more resilient to outliers than k-centers. For example, consider finding a single center (k=1) for the following 1-D points: [0, 0.5, 1, 1.5, 10]. The last point (10) is an outlier. Without that outlier, k-centers has a center of 0.75 ...

```{svgbob}
   |                                       "center: 0.75"
   v                                     
*-*-*-*----------------------------------
0   1   2   3   4   5   6   7   8   9   10
```

With that outlier, the k-centers has a center of 5, which is a drastic shift from the original 0.75 shown above ...

```{svgbob}
                    |                      "center: 5"
                    v                    
*-*-*-*---------------------------------* 
0   1   2   3   4   5   6   7   8   9   10
```

K-means combats this shift by applying weighting: The idea is that the 4 real points should have a stronger influence on the center than the one outlier point, essentially dragging it back towards them. Using k-means, the center is 2.6 ...

```{svgbob}
          |                                "center: 2.6"
          v                              
*-*-*-*---------------------------------*
0   1   2   3   4   5   6   7   8   9   10
```

Note that the scoring functions for k-means and k-centers produce vastly different scores, but the scores themselves don't matter. What matters is the minimization of the score. The diagram below shows the scores for both k-means and k-centers as the center shifts from 10 to 0 ...

```{svgbob}
                                        |  "center: 10"
                                        v  "k-centers score: 10"
*-*-*-*---------------------------------*  "k-means score: 68.7"
0   1   2   3   4   5   6   7   8   9   10


                                    |      "center: 9"
                                    v      "k-centers score: 9"
*-*-*-*---------------------------------*  "k-means score: 54.9"
0   1   2   3   4   5   6   7   8   9   10


                                |          "center: 8"
                                v          "k-centers score: 8"
*-*-*-*---------------------------------*  "k-means score: 43.1"
0   1   2   3   4   5   6   7   8   9   10


                            |              "center: 7"
                            v              "k-centers score: 7"
*-*-*-*---------------------------------*  "k-means score: 33.3"
0   1   2   3   4   5   6   7   8   9   10


                        |                  "center: 6"
                        v                  "k-centers score: 6"
*-*-*-*---------------------------------*  "k-means score: 25.5"
0   1   2   3   4   5   6   7   8   9   10


                    |                      "center: 5"
                    v                      "k-centers score: 5  (LOWEST K-CENTERS SCORE IN SET)"
*-*-*-*---------------------------------*  "k-means score: 19.7"
0   1   2   3   4   5   6   7   8   9   10


                |                          "center: 4"
                v                          "k-centers score: 6"
*-*-*-*---------------------------------*  "k-means score: 15.9"
0   1   2   3   4   5   6   7   8   9   10


            |                              "center: 3"
            v                              "k-centers score: 7"
*-*-*-*---------------------------------*  "k-means score: 14.1  (LOWEST K-MEANS SCORE IN SET)"
0   1   2   3   4   5   6   7   8   9   10


        |                                  "center: 2"
        v                                  "k-centers score: 8"
*-*-*-*---------------------------------*  "k-means score: 14.3"
0   1   2   3   4   5   6   7   8   9   10


    |                                      "center: 1"
    v                                      "k-centers score: 9"
*-*-*-*---------------------------------*  "k-means score: 16.5"
0   1   2   3   4   5   6   7   8   9   10


|                                          "center: 0"
v                                          "k-centers score: 10"
*-*-*-*---------------------------------*  "k-means score: 20.7"
0   1   2   3   4   5   6   7   8   9   10
```

**ALGORITHM**:

Similar to k-centers, solving k-means for any non-trivial input isn't possible because the search space is too huge. Because of this, heuristics are used. A common k-means heuristic is Lloyd's algorithm. The algorithm randomly picks k points to set as the centers and iteratively refines those centers. At each step, the algorithm ...

 1. converts centers to clusters,
 
    The point closest to a center becomes a member_CLUSTER of that cluster. Ties are broken arbitrarily.

    ```{output}
    ch8_code/src/clustering/KMeans_Lloyds.py
    python
    # MARKDOWN_CLOSEST_CENTER\s*\n([\s\S]+)\n\s*# MARKDOWN_CLOSEST_CENTER
    no_preamble
    ```

 2. converts clusters to centers.

    The clusters from step 1 are turned into new centers. Each component of a center becomes the average of that component across cluster member_CLUSTERs, referred to as the center of gravity.

    ```{output}
    ch8_code/src/clustering/KMeans_Lloyds.py
    python
    # MARKDOWN_CENTER_OF_GRAVITY\s*\n([\s\S]+)\n\s*# MARKDOWN_CENTER_OF_GRAVITY
    no_preamble
    ```

The algorithm will converge to stable centers, at which point it stops iterating.

```{output}
ch8_code/src/clustering/KMeans_Lloyds.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN\s*[\n$]
```

```{ch8}
clustering.KMeans_Lloyds
[
  3,
  [
    [2,2], [2,4], [2.5,6], [3.5,2], [4,3], [4,5], [4.5,4],
    [17,12], [17.5,13], [18,11], [19,12],
    [18,-7], [18.5,-8], [19,-6], [20,-7]
  ],
# Remove the following element to have the system pick k random points
  [
    [2,2], [2,4], [2.5,6]
  ]
]
```

At each iteration, the cluster member_CLUSTERs captured (step 1) will drag the new center towards them (step 2). After so many iterations, each center will be at a point where further iterations won't capture a different set of member_CLUSTERs, meaning that the centers will stay where they're at (converged).

```{note}
I said "ties are broken arbitrarily" (step 1) because that's what the Pevzner book says. This isn't entirely true? I think it's possible to get into a situation where a tied point ping-pongs back and forth between clusters. So, maybe what actually needs to happen is you need to break ties consistently -- it doesn't matter how, just that it's consistent (e.g. the center closest to origin + smallest angle from origin always wins the tied member_CLUSTER).

Also, if the centers haven't converged, the dragged center is guaranteed to decrease the squared error distortion when compared to the previous center. But, does that mean that a set of converged centers are optimal in terms of squared error distortion? I don't think so. Even if a cluster converged to all the correct member_CLUSTERs, could it be that the center can be slightly tweaked to get the squared error distortion down even more? Probably.
```

The hope with the heuristic is that, at each iteration, enough true cluster member_CLUSTERs are captured (step 1) to drag the center (step 2) closer to where it should be. One way to increase the odds that this heuristic converges on a good solution is the initial center selection: You can increase the chance of converging to a good solution by _probabilistically_ selecting initial centers that are far from each other, referred to as k-means++ initializer.

 1. The 1st center is chosen from the list of points at random.
 2. The 2nd center is chosen by selecting a point that's likely to be much farther away from center 1 than most other points.
 3. The 3rd center is chosen by selecting a point that's likely to be much farther away from center 1 and 2 than most other points.
 4. ...

The probability of selecting a point as the next center is proportional to its squared distance to the existing centers.

```{output}
ch8_code/src/clustering/KMeans_Lloyds.py
python
# MARKDOWN_KMEANS_PP_INITIALIZER\s*\n([\s\S]+)\n\s*# MARKDOWN_KMEANS_PP_INITIALIZER\s*[\n$]
```

```{ch8}
clustering.KMeans_Lloyds main_WITH_k_means_PP_initializer
[
  3,
  [
    [2,2], [2,4], [2.5,6], [3.5,2], [4,3], [4,5], [4.5,4],
    [17,12], [17.5,13], [18,11], [19,12],
    [18,-7], [18.5,-8], [19,-6], [20,-7]
  ]
]
```

Even with k-means++ initializer, Lloyd's algorithm isn't guaranteed to always converge to a good solution. The typical workflow is to run it multiple times, where the run producing centers with the lowest squared error distortion is the one accepted.

Furthermore, Lloyd's algorithm may fail to converge to a good solution when the clusters aren't globular and / or aren't of similar densities. Below are example clusters that are obvious to a human but problematic for the algorithm.

```{note}
The Pevzner book explicitly calls out Lloyd's algorithm for this, but I'm thinking this is more to do with the scoring function for k-means (what's trying to be minimized)? I think the same problem applies to the scoring function for k-centers and the furthest first traveled heuristic?

The examples below are taken directly from the Pevzner book.
```

```{svgbob}
"Cluster membership is denoted using letters."
 
                                                  ELONGATED
                 .-----------------------------.              .-----------------------------.
                 |          EXPECTED           |              |           ACTUAL            |
                 |                             |              |                             |
                 |   C               E   E     |              |   C               C   C     |
                 | C     C             E     E |              | C     C             C     C |
                 |    C    C         E   E     |              |    C    C         C   C     |
                 | C     C                 E   |              | C     C                 C   |
                 |   C C             E   E     |              |   C C             C   C     |
                 |         C           E       |              |         C           C       |
                 |   C   C               E   E |              |   C   C               C   C |
                 | C   C   C           E       |              | C   C   C           C       |
                 |     C             E       E |              |     C             C       C |
                 |   C     C               E   |              |   C     C               C   |
                 |     C             E   E     |              |     C             C   C     |
                 | C     C           E     E   |              | E     E           E     E   |
                 |   C     C           E     E |              |   E     E           E     E |
                 |       C           E     E   |              |       E           E     E   |
                 |   C     C           E     E |              |   E     E           E     E |
                 | C     C                 E   |              | E     E                 E   |
                 |         C           E     E |              |         E           E     E |
                 | C     C               E     |              | E     E               E     |
                 |     C             E       E |              |     E             E       E |
                 | C     C             E       |              | E     E             E       |
                 |   C     C         E       E |              |   E     E         E       E |
                 '-----------------------------'              '-----------------------------'
 
 
 
                                             "ELONGATED ANE CURVED"
             
             .----------------------------------.             .----------------------------------.
             |           EXPECTED               |             |            ACTUAL                |
             |                                  |             |                                  |
             |                  E   E           |             |                  E   E           |
             |                 E   E   E        |             |                 E   E   E        |
             |                    E   E         |             |                    E   E         |
             |                           E      |             |                           E      |
             |                      E   E  E    |             |                      E   E  E    |
             |                         E        |             |                         E        |
             |                       E   E   E  |             |                       E   E   E  |
             |           C                E     |             |           E                E     | 
             |        C     C          E      E |             |        E     E          E      E |
             |          C    C           E  E   |             |          E    E           E  E   |
             |      C     C             E   E   |             |      E     E             E   E   |
             |    C  C C             E     E    |             |    E  E E             E     E    |
             |     C      C           E     E   |             |     E      E           E     E   |
             |     C   C             E  E  E    |             |     C   C             C  C  C    |
             |  C   C   C             E     E   |             |  C   C   C             C     C   |
             |     C                  E         |             |     C                  C         |
             |   C   C C            E  E  E     |             |   C   C C            C  C  C     |
             |     C   C           E            |             |     C   C           C            |
             |  C     C           E     E       |             |  C     C           C     C       |
             |   C  C  C        E    E          |             |   C  C  C        C    C          |
             |      C  C      E   E   E         |             |      C  C      C   C   C         |
             |     C  C  C                      |             |     C  C  C                      |
             |     C     C                      |             |     C     C                      |
             |    C   C    C                    |             |    C   C    C                    |
             |       C     C                    |             |       C     C                    |
             |       C   C                      |             |       C   C                      |
             |         C     C                  |             |         C     C                  |
             |        C  C     C                |             |        C  C     C                |
             '----------------------------------'             '----------------------------------'



                                       "GLOBULAR BUT DIFFERENT DENSITY"

.--------------------------------------------------.        .--------------------------------------------------.
|                      EXPECTED                    |        |                       ACTUAL                     |
|                                                  |        |                                                  |
|        M       M                      C C C      |        |        M       E                      C C C      |
|                                    C  CC C C C   |        |                                    C  CC C C C   |
|     M                M           CC CC  CC C CC  |        |     M                E           CC CC  CC C CC  |
|                                  C CC CC C C C C |        |                                  C CC CC C C C C |
|                  M                 C CC CC C C   |        |                  E                 C CC CC C C   |
| M            M        M               CCC C      |        | M            E        E               CCC C      |
|       M                                          |        |       M                                          |
|                                                  |        |                                                  |
|                 M                     EEE E      |        |                 E                     CCC C      |
|    M                               EE E  E E E   |        |    M                               CC C  C C C   |
|           M         M            E E EE E E E EE |        |           M         E            C C CC C C C CC |
|      M                           E E EE E E E E  |        |      M                           C C CC C C C C  |
|                  M                 E  E  E EE E  |        |                  E                 C  C  C CC C  |
|    M                M                 E E E      |        |    M                E                 C C C      |
'--------------------------------------------------'        '--------------------------------------------------'
```

### Soft K-Means Clustering

`{bm} /(Algorithms\/Gene Clustering\/Soft K-Means Clustering)_TOPIC/`

```{prereq}
Algorithms/Gene Clustering/K-Means Clustering_TOPIC
```

**WHAT**: Soft k-means clustering is the soft clustering variant of k-means. Whereas the original k-means definitively assigns each point to a cluster (hard clustering), this variant of k-means assigns each point to how likely it is to be a member_CLUSTER of each cluster (soft clustering).

```{svgbob}
       ●                                           ●       
  "A=0.9,B=0.1"                               "A=0.1,B=0.9"
                                                           
          ●                                    ●       
     "A=0.9,B=0.1"                        "A=0.1,B=0.9"
                                                           
       ●                                           ●       
  "A=0.9,B=0.1"                               "A=0.1,B=0.9"
```

The goal is to choose centers such that, out of all possible centers, you're maximizing the _likelihood_ of the points belonging to those centers (maximizing for definitiveness / minimizing for unsureness).

```{svgbob}
* "Plus sign denotes a center"
.-----------------------------------------------------------.
|                        "BAD CENTERS"                      |
|      ●                                           ●        |
| "A=0.5,B=0.5"                               "A=0.5,B=0.5" |
|                                                           |
|         ●                                    ●            |
|    "A=0.5,B=0.5"           "++"         "A=0.5,B=0.5"     |
|                                                           |
|      ●                                           ●        |
| "A=0.5,B=0.5"                               "A=0.5,B=0.5" |
'-----------------------------------------------------------'
.-----------------------------------------------------------.
|                       "GOOD CENTERS"                      |
|      ●                                           ●        |
| "A=0.9,B=0.1"                               "A=0.1,B=0.9" |
|                                                           |
|      +  ●                                    ●   +        |
|    "A=0.9,B=0.1"                        "A=0.1,B=0.9"     |
|                                                           |
|      ●                                           ●        |
| "A=0.9,B=0.1"                               "A=0.1,B=0.9" |
'-----------------------------------------------------------'
```

```{note}
There's some ambiguity here on what the function being minimized / maximized is and how probabilities are derived. It seems like squared error distortion isn't involved here at all, so how is this related in any way to k-means? My understanding is that squared error distortion is what makes k-means.

It seems like this is called soft k-means because the high-level steps of the algorithm for this are similar to the Lloyd's algorithm heuristic. That's where the similarity ends (as far as I can tell). So maybe it should be called soft lloyd's algorithm instead? It looks like the generic name for this is called the [Expectation-maximization algorithm](https://en.wikipedia.org/wiki/Expectation%E2%80%93maximization_algorithm).
```

**WHY**: Soft clustering is a way to suss out ambiguous points. For example, a point that sits exactly between two obvious clusters will be just as likely to be a member_CLUSTER of each...

```{svgbob}
       ●              "ambiguous point"             ●       
  "A=0.9,B=0.1"                |               "A=0.1,B=0.9"
                               v                            
          ●                    ●                ●       
     "A=0.9,B=0.1"        "A=0.5,B=0.5"    "A=0.1,B=0.9"
                                                            
       ●                                            ●       
  "A=0.9,B=0.1"                                "A=0.1,B=0.9"
```

**ALGORITHM**:

This algorithm is similar to the Lloyd's algorithm heuristic used for k-means clustering. It begins by randomly picking k points to set as the centers and iteratively refines those centers. At each step, the algorithm ...

 1. converts centers to clusters (referred to as E-step),
 2. converts clusters to centers (referred to as M-step).

The major difference between Lloyd's algorithm and this algorithm is that this algorithm produces *probabilities of cluster membership_CLUSTER assignments*. In contrast, the original Lloyd's algorithm produces *definitive cluster membership_CLUSTER assignments*.


```{svgbob}
* "Plus sign denotes a center"
.------------------------------------------------------------.
|               "ORIGINAL LLOYD'S ALGORITHM"                 |
|      ●                                            ●        |
|      A                                            B        |
|                                                            |
|      +  ●                                     ●   +        |
|         A                                     B            |
|                                                            |
|      ●                                            ●        |
|      A                                            B        |
'------------------------------------------------------------'
.------------------------------------------------------------.
|                  "SOFT LLOYD'S ALGORITHM"                  |
|      ●                                            ●        |
| "A=0.9,B=0.1"                                "A=0.1,B=0.9" |
|                                                            |
|      +  ●                                     ●   +        |
|    "A=0.9,B=0.1"                         "A=0.1,B=0.9"     |
|                                                            |
|      ●                                            ●        |
| "A=0.9,B=0.1"                                "A=0.1,B=0.9" |
'------------------------------------------------------------'
```

The steps being iterated here are essentially the same steps as in the original Lloyd's algorithm, except they've been modified to work with assignment probabilities instead of definitive assignments. As such, you can think of this as a soft Lloyd's algorithm (soft clustering version of Lloyd's algorithm).

`{h}blue STEP 1: CENTERS TO CLUSTERS (E-STEP)`

Recall that with the original Lloyd's algorithm, this step assigns each data point to exactly one center (whichever center is closest).
    
```{output}
ch8_code/src/clustering/KMeans_Lloyds.py
python
# MARKDOWN_CLOSEST_CENTER\s*\n([\s\S]+)\n\s*# MARKDOWN_CLOSEST_CENTER
no_preamble
```

With this algorithm, each data point is assigned a set of probabilities that define how likely it is to be assigned to each center, referred to as confidence values (and sometimes responsibility values).

```{svgbob}
* "Plus signs denote centers. Middle point is just as likely"
  "to belong to each center (equal confidence for each)."

     ●                                                          ●       
"A=0.9,B=0.1"                                              "A=0.1,B=0.9"
                                                                        
     +  ●                           ●                       ●   +   
   "A=0.9,B=0.1"               "A=0.5,B=0.5"           "A=0.1,B=0.9"
                                                                        
     ●                                                          ●       
"A=0.9,B=0.1"                                              "A=0.1,B=0.9"
```

The general concept behind assigning confidence values is that the closer a center is to a data point, the more affinity it has to that data point (higher confidence for closer points). This concept can be implemented in multiple different ways: raw distance comparisons, Newtonian inverse-square law of gravitation, partition function from statistical physics, etc..

The partition function is the preferred implementation.

```{kt}
confidence(P, C_i) = \frac{
  e^{-\beta \cdot d(P, C_i)}
}{
  \sum_{t=1}^{n}{e^{-\beta \cdot d(P, C_t)}}
}
```

* P is a point.
* C is a set of centers.
* Ci is the center for which the confidence is being calculated.
* n is the number of centers in C.
* e is the base for natural logarithms (~2.72).
* b is a user-defined parameter (ranges from 0 to 1) that defines how decisive confidences will be.
* d() calculates the euclidean distance.

```{output}
ch8_code/src/clustering/Soft_KMeans_Lloyds.py
python
# MARKDOWN_E_STEP\s*\n([\s\S]+)\n\s*# MARKDOWN_E_STEP\s*[\n$]
no_preamble
```

```{ch8}
clustering.Soft_KMeans_Lloyds main_e_step
{
  points: [
    [1,0], [0,1], [0,-1],
    [9,0], [10,1], [10,-1],
    [5,0]
  ],
  centers: [[0, 0], [10, 0]],
  stiffness: 0.5
}
```

```{note}
The Pevzner book gives the analogy that centers are stars and points are planets. The closer a planet is to a star, the stronger that star's gravitational pull should be. This gravitational pull is the "confidence" -- a stronger pull means a stronger confidence. The analogy falls a bit flat because, in this case, it's the stars (centers) that are being pulled into the planets (points) -- normally it's the other way around (planets get pulled into stars).

I have no idea how the partition function actually works or know anything about statistical physics. The book also listed the formula for Newtonian inverse-square law of gravitation but mentioned that the partition function works better in practice. I think a simpler / more understandable metric may be used instead of either of these. The core thing it needs to do is assign a greater confidence to points that are closer than to those that are farther, where that confidence is between 0 and 1. Maybe some kind of re-worked / inverted version of squared error distortion would work here.
```

`{h}blue STEP 2: CLUSTERS TO CENTERS (M-STEP)`

Recall that with the original Lloyd's algorithm, this step generates new centers for clusters by calculating the center of gravity across the member_CLUSTERs of each cluster: Each component of a new center becomes the average of that component across its cluster member_CLUSTERs.

```{output}
ch8_code/src/clustering/KMeans_Lloyds.py
python
# MARKDOWN_CENTER_OF_GRAVITY\s*\n([\s\S]+)\n\s*# MARKDOWN_CENTER_OF_GRAVITY
no_preamble
```

This algorithm performs a similar center of gravity calculation. The difference is that, since there are no definitive cluster member_CLUSTERs here, all data points are included in the center of gravity calculation. However, each data point is appropriately scaled by its confidence value (0.0 to 1.0 -- also known as probability) before being added into the center of gravity.

```{output}
ch8_code/src/clustering/Soft_KMeans_Lloyds.py
python
# MARKDOWN_M_STEP\s*\n([\s\S]+)\n\s*# MARKDOWN_M_STEP\s*[\n$]
no_preamble
```

```{ch8}
clustering.Soft_KMeans_Lloyds main_m_step
{
  membership_confidences: [
    [   # center followed by (point, confidence) pairs
        [-1, 0],
        [[1,1], 0.9],  [[2,2], 0.8],  [[3,3], 0.7],
        [[9,1], 0.03], [[8,2], 0.02], [[7,3], 0.01],
    ],
    [   # center followed by (point, confidence) pairs
        [11, 0],
        [[1,1], 0.03], [[2,2], 0.02], [[3,3], 0.01],
        [[9,1], 0.9],  [[8,2], 0.8],  [[7,3], 0.7],
    ]
  ]
}
```

````{note}
Think about what's happening here. With the original Lloyd's algorithm, you're averaging. For example, the points 5, 4, and 3 are calculated as ...

```
(5 + 4 + 3) / (1 + 1 + 1)
(5 + 4 + 3) / 3
12 / 3
4
```

With this algorithm, you're doing the same thing except weighting the points being averaged by their confidence values. For example, if the points above had the confidence values 0.9, 0.8, 0.95 respectively, they're calculated as ...

```
((5 * 0.9) + (4 * 0.8) + (3 * 0.95)) / (0.9 + 0.8 + 0.95)
(4.5 + 3.2 + 2.85) / 2.65
10.55 / 2.65
3.98
```

The original Lloyd's algorithm center of gravity calculation is just this algorithm's center of gravity calculation with all 1 confidence values ...

```
((5 * 1) + (4 * 1) + (3 * 1)) / (1 + 1 + 1)
(5 + 4 + 3) / (1 + 1 + 1)   <-- same as 1st expression in original Lloyd's example above
(5 + 4 + 3) / 3
12 / 3
4
```
````

`{h}blue ITERATING STEP 1 AND STEP 2`

Like with the original Lloyd's algorithm, this algorithm iterates over the two steps until the centers converge. The centers may start off by jumping around in wrong directions. The hope is that, as more iterations happen, eventually enough true cluster member_CLUSTERs gain appropriately high confidence values (step 1) to drag their center (step 2) closer to where it should be. One way to increase the odds that this algorithm converges on a good solution is the initial center selection: You can increase the chance of converging to a good solution by _probabilistically_ selecting initial centers that are far from each other via the k-means++ initializer (similar to the original Lloyd's algorithm).

Due to various issues with the computations involved and floating point rounding error, this algorithm likely won't fully stabilize at a specific set of centers (it converges, but the centers will continue to shift around slightly at each iteration). The typical workaround is to stop after a certain number of iterations and / or stop if the centers only moved by a tiny distance.

```{note}
The example run below has cherry-picked input to illustrate the "start off by jumping around in wrong directions" point described above. Note how center 0 jumps out towards the center but then gradually moves back near to where it originally started off at.
```

```{output}
ch8_code/src/clustering/Soft_KMeans_Lloyds.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN\s*[\n$]
no_preamble
```

```{ch8}
clustering.Soft_KMeans_Lloyds
{
  k: 3,
  points: [
    [2,2], [2,4], [2.5,6], [3.5,2], [4,3], [4,5], [4.5,4],
    [7,2], [7.5,3], [8,1], [9,2],
    [8,7], [8.5,8], [9,6], [10,7]
  ],
  centers: [[8.5, 8], [9, 6], [7.5, 3]], # remove to assign centers using k-means++ initializer
  stiffness: 0.75,                       # stiffness parameter for partition function
  show_every: 1,
  stop_instructions: {
    min_center_step_distance: 0.3,
    max_iterations: 50
  }
}
```

````{note}
I didn't cover it here, but the book dedicated a very large number of sections to introducing this algorithm using a "biased coin" flipping scenario. In the scenario, some guy has two coins, each with a different bias for turning up heads (coinA with biasA / coinB with biasB). At every 10 flip interval, he picks one of the coins at random (either keeps existing one or exchanges it) before using that coin to do another 10 flips.

Which coin he picks per 10 flip round and the coin biases are secret (you don't know them). The only information you have is the outcome of each 10 flip round. Your job is to guess the coin biases from observing those 10 flip rounds, not knowing which of the two coins were used per round.

In this scenario ...

 * TRUE CENTERS = What biasA and biasB actually are.

   (e.g. coinA has a 0.7 bias to turn up heads / coinB has a 0.2 bias to turn up heads)

 * ESTIMATED CENTERS = What you _estimate_ biasA and biasB are (not what they actually are).

   (e.g. coinA has a 0.67 bias to turn up heads / coinB has a 0.23 bias to turn up heads)

 * POINTS = Each 10 flip round's percentage that turned up heads.

   (e.g. HHTHHTHHTT = 6 / 10 = 0.6)

 * CONFIDENCE VALUES = Each 10 flip round's confidence that biasA vs biasB was used (_estimated_ biases).

   (e.g. for round1, 0.1 probability that _estimated_ biasA was used vs 0.9 probability that _estimated_ biasB was used)

In this scenario, the guy does 5 rounds of 10 coin flips (which coin he used per round is a secret). These rounds are your 1-dimensional POINTS ...

```
HTTTHTTHTH = 4 / 10 = 0.4
HHHHTHHHHH = 9 / 10 = 0.9
HTHHHHHTHH = 9 / 10 = 0.8
HTTTTTHHTT = 3 / 10 = 0.3
THHHTHHHTH = 7 / 10 = 0.7
```

You start off by picking two of these percentages as your guess for biasA and biasB (ESTIMATED CENTERS)...

```
biasA = 0.3, biasB = 0.8
```

From there, you're looping over the E-step and M-step...

 * E-step: For each 10 flip round (POINT) and estimated coin bias (ESTIMATED CENTER) pair, calculate the probability (CONFIDENCE VALUE) that that bias generated those 10 flips.
 * M-step: Adjust your estimate for biasA and biasB (ESTIMATED CENTERS) based on those probabilities (CONFIDENCE VALUES).
 
Note that you never actually know what the real coin biases (TRUE CENTERS) are, but you should get somewhere close given that ...

1. there are enough 10 flip rounds (POINTS),
2. you make a decent starting guess for biasA and biasB (initial ESTIMATED CENTERS),
3. and the metric you're using to derive coin usage probabilities (CONFIDENCE VALUES) make sense -- in this scenario it wasn't the partition function but the "conditional probability" that the 10 flip outcome was generated by a coin with the guessed bias.

This scenario was difficult to wrap my head around because the explanations were obtuse and it doesn't make one key concept explicit: The heads average for a 10 flip round (POINT) is representative of the actual heads bias of the coin used (TRUE CENTER). For example, if the coin being used has an actual heads bias of 0.7 (TRUE CENTER of 0.7), most of its 10 flip rounds will have a heads percentage of around 0.7 (POINTS near 0.7). A few might not, but most will (e.g. there's a small chance that the 10 flips could come out to all tails).

If you think about it, this is exactly what's happening with clustering: The points in a cluster are representative of some ideal center point, and you're trying to find what that center point is.

Other things that made the coin flipping example not good:

 1. There's absolutely a chance that the algorithm will veer towards guesses that are far off than true coin biases (an example of this happening would have been helpful).
 2. It should have somehow been emphasized that poor initial coin bias guesses or weak / little coin flip representations can screw you (an example of this happening would have been helpful).
 3. The mathy way in which things were described made everything incredibly obtuse: obtuse naming (e.g. "hidden matrix"), vector notation, dot product, formula representations, etc.. (better naming and more text representation would have made things easier to understand).
 4. Some mathy portions were just papered over (e.g. it was never explained in layman's terms what the partition function actually does -- does it mimic gravity?).

Points 1 and 2 have similar analogs in Lloyd's algorithm. Lloyd's algorithm can give you bad centers + Lloyd's algorithm can screw you if your initial centers are bad / not enough points representative of actual clusters are available.
````

### Hierarchical Clustering     

`{bm} /(Algorithms\/Gene Clustering\/Hierarchical Clustering)_TOPIC/`

```{prereq}
Algorithms/Gene Clustering/Euclidean Distance Metric_TOPIC
Algorithms/Gene Clustering/Manhattan Distance Metric_TOPIC
Algorithms/Gene Clustering/Cosine Similarity Metric_TOPIC
Algorithms/Gene Clustering/Pearson Similarity Metric_TOPIC
Algorithms/Phylogeny/Distance Matrix to Tree/UPGMA Algorithm_TOPIC
```

**WHAT**: Given a list of n-dimensional vectors, convert those vectors into a distance matrix and build a phylogenetic tree (must be a rooted tree). Each internal node represents a sub-cluster, and sub-clusters combine to form larger sub-clusters (a hierarchy of clusters).

```{svgbob}
                                                                                     "HIERARCHY OF CLUSTERS"

                                                                          .--------------------------------------------------.
                                                                          |                                                  |
                                                                          |  .--------------------------------------------.  |
                                                                          |  |                            .------------.  |  |
                                                                          |  | .--------------------.     |            |  |  |
                 "PHYLOGENETIC TREE (ROOTED)"                             |  | |     .------------. |     |       g7   |  |  |
                                                                          |  | | g9  |         g1 | |     |            |  |  |
                                                                          |  | |     | .------.   | |     | .-----.    |  |  |
                              |                                           |  | |     | | g2   |   | |     | | g6  |    |  |  |
                  .-----------*-----------.                               |  | |     | |   g4 |   | |     | | g10 |    |  |  |
                  |                       |                               |  | |     | '------'   | |     | '-----'    |  |  |
      .-----------*----------.            |                               |  | |     '------------' |     '------------'  |  |
      |                      |            |                               |  | |                    |                     |  |
.-----*-----.                |            |                               |  | '--------------------'                     |  |
|           |                |            |                               |  '--------------------------------------------'  |
|       .---*---.       .----*---.    .---*---.                           |                                                  |
|       |       |       |        |    |       |                           |                                                  |
|    .--*--.    |    .--*--.     |    |    .--*--.                        |                                                  |
|    |     |    |    |     |     |    |    |     |                        |                                                  |
g9   g4    g2   g1   g6    g10   g7   g8   g5    g3                       |                                                  |
                                                                          |          .--------------.                        |
                                                                          |          |  .--------.  |                        |
                                                                          |          |  | g5  g3 |  |                        |
                                                                          |          |  '--------'  |                        |
                                                                          |          |              |                        |
                                                                          |          |     g8       |                        |
                                                                          |          '--------------'                        |
                                                                          |                                                  |
                                                                          '--------------------------------------------------'
```

**WHY**: In phylogeny, the goal is to take a distance matrix and use it to generate a tree that represents shared ancestry (phylogenetic tree). Each shared ancestor is represented as an internal node, and nodes that have the same parent node are _more similar to each other than to any other nodes in the tree_. In the example phylogenetic tree below, nodes A4 and A2 share their parent node, meaning they share more with each other than any other node in the tree (are more similar to each other than any other node in the tree).

```{svgbob}
      |           
.-----*-----.     
|           |     
|       .---*---. 
|       |       | 
|    .--*--.    | 
|    |     |    | 
A3   A4    A2   A1
```

In clustering, the goal is to group items in such a way that items in the same group are _more similar to each other than items in other groups_ (good clustering principle). In the example below, A3 has been placed into its own group because it isn't occupying the same general vicinity as the other items.

```{svgbob}
  CLUSTER1   
   .----.              CLUSTER2
   | A3 |           .-----------.
   '----'           |      A1   |
                    |           |
                    |  A2       |
                    |    A4     |
                    |           |
                    '-----------'
```

If you squint a bit, phylogeny and clustering are essentially doing the same thing:

* Phylogeny: nodes that have the same parent node are _more similar to each other than to any other nodes in the tree_.
* Clustering: items in the same group are _more similar to each other than items in other groups_.

A phylogenetic tree (that's also a rooted tree) is essentially a form of recursive clustering / hierarchical clustering. Each internal node represents a sub-cluster, and sub-clusters combine to form larger sub-clusters.

```{svgbob}
"REPRESENTATION AS TREE"               "REPRESENTATION AS HIERARCHY OF CLUSTER"   
    
          |                              .--------------------------------.
    .-----*-----.                        | .----.                         |
    |           |                        | | A3 |           .-----------. |
    |       .---*---.                    | '----'           |      A1   | |
    |       |       |                    |                  |.------.   | |
    |    .--*--.    |                    |                  || A2   |   | |
    |    |     |    |                    |                  ||   A4 |   | |
    A3   A4    A2   A1                   |                  |'------'   | |
                                         |                  '-----------' |
                                         '--------------------------------'
```

**ALGORITHM**:

This algorithm uses UPGMA, but you can swap that out for any other phylogenetic tree generation algorithm so long as it generates a rooted tree.

```{output}
ch8_code/src/clustering/HierarchialClustering_UPGMA.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN\s*[\n$]
```

```{ch8}
clustering.HierarchialClustering_UPGMA
{
  metric: euclidean,  # OPTIONS: euclidean, manhattan, cosine, pearson
  vectors: {
    VEC1: [5,6,5],
    VEC2: [5,7,5],
    VEC3: [30,31,30],
    VEC4: [29,30,31],
    VEC5: [31,30,31],
    VEC6: [15,14,14]
  }
}
```

### Soft Hierarchical Clustering

`{bm} /(Algorithms\/Gene Clustering\/Soft Hierarchical Clustering)_TOPIC/`

```{prereq}
Algorithms/Gene Clustering/Hierarchical Clustering_TOPIC
Algorithms/Phylogeny/Distance Matrix to Tree/Neighbour Joining Phylogeny Algorithm_TOPIC
```

```{note}
This isn't from the Pevzner book. I reasoned about it myself and implemented it here. My thought process might not be entirely correct.
```

**WHAT**: In normal Hierarchical clustering, a rooted tree represents a hierarchy of clusters. Internal nodes represent sub-clusters, where those sub-clusters combine together to form larger sub-clusters.

```{svgbob}
"REPRESENTATION AS TREE"               "REPRESENTATION AS HIERARCHY OF CLUSTER"   
    
          |                              .--------------------------------.
    .-----*-----.                        | .----.                         |
    |           |                        | | A3 |           .-----------. |
    |       .---*---.                    | '----'           |      A1   | |
    |       |       |                    |                  |.------.   | |
    |    .--*--.    |                    |                  || A2   |   | |
    |    |     |    |                    |                  ||   A4 |   | |
    A3   A4    A2   A1                   |                  |'------'   | |
                                         |                  '-----------' |
                                         '--------------------------------'
```

In this soft clustering variant of Hierarchical clustering, an unrooted tree is used instead. An internal node in an unrooted tree doesn't have a parent or children, it only has neighbours. If there is some kind of a parent-child relationship, that information isn't represented in the unrooted tree (e.g. the tree doesn't tell you which branch goes to the parent vs which branches go to children).

```{svgbob}
                 A3
A2              /
  \            /  
   \          /
    *--------*
   /          \  
 A4            \
                A1  
```

Rather than thinking of an unrooted tree's internal nodes as sub-clusters that combine together, it's more appropriate to think of them as points of commonality. An internal node captures the shared features of its neighbours and represents the degree_NORM of similarity between it and its neighbours via the distances to those neighbours. A very close neighbour is very similar while a farther away neighbour is not as similar.

In the example above, the internal node that connects A2 and A4 has three neighbours: A2, A4, and the other internal node in the tree. Of those three neighbours, it's most similar to A4 (closest) and least similar to the other internal node (farthest).

**WHY**: Traditional soft clustering has a _distinct set of clusters_ where each item has a probability of being a member_CLUSTER of one of those clusters. The set of membership_CLUSTER probabilities for each _item_ should sum to 1.

|        | Cluster 1 | Cluster 2 | Sum     |
|--------|-----------|-----------|---------|
| Item 1 | 0.25      | 0.75      | **1.0** |
| Item 2 | 0.7       | 0.3       | **1.0** |
| Item 3 | 0.8       | 0.2       | **1.0** |
| Item 4 | 0.1       | 0.9       | **1.0** |

In this scenario, that doesn't make sense because there are no distinct clusters. As described above, it's more appropriate to think of internal nodes as points of commonality rather than as clusters. Points of commonality can feed into each other (an internal node can have other internal nodes as neighbours). As such, rather than each item having a probability of being a member_CLUSTER of a cluster, each point of commonality has a probability of having an item as its member_CLUSTER (based on how close an item is to it). The set of membership_CLUSTER probabilities for each point of commonality should sum to 1.

|                 | Item 1 | Item 2 | Item 3 | Item 4 | Sum     |
|-----------------|--------|--------|--------|--------|---------|
| Internal Node 1 | 0.4    | 0.3    | 0.2    | 0.1    | **1.0** |
| Internal Node 2 | 0.1    | 0.1    | 0.1    | 0.7    | **1.0** |

**ALGORITHM**:

To determine the set of membership_CLUSTER probabilities for an internal node of the unrooted tree, the algorithm first gathers the distances from that internal node to each leaf node. Those distances are then converted to a set of probabilities using a formula known as inverse distance weighting ...

```{kt}
probability =
\frac{
  1 / D_j
}{
  1 / \sum_{i=1}^n{D_i}
}
```

... where ...

 * D is the set of distances for the internal node
 * n is D's count.
 * Dj is the distance for which the probability is being computed.

```{output}
ch8_code/src/clustering/Soft_HierarchialClustering_NeighbourJoining.py
python
# MARKDOWN_PROBABILITY\s*\n([\s\S]+)\n\s*# MARKDOWN_PROBABILITY\s*[\n$]
```

```{note}
I'm thinking that the probability isn't what you want here. Instead what you want is likely just the distances themselves or the distances normalized between 0 and 1: `{kt} \frac{D_j}{\sum_{i=1}^n{D_i}}`. Those will allow you to figure out more interesting things about the clustering. For example, if a set of leaf nodes are all roughly the equidistant to the same internal node and that distance is greater than some threshold, they're likely things you should be interested in.
```

Neighbour joining phylogeny is used to generate the unrooted tree (simple tree), but the algorithm could just as well take any rooted tree and convert it to an unrooted tree. Neighbour joining phylogeny is the most appropriate phylogeny algorithm because it reliably reconstructs the unique simple tree for an additive distance matrix / approximates a simple tree for a non-additive distance matrix.

````{note}
Recall that neighbour joining phylogeny doesn't reconstruct a rooted tree because distance matrices don't capture hierarchy information. Also recall that edges broken up by a node (internal nodes of degree_GRAPH 2) also aren't reconstructed because distance matrices don't capture that information either. If the original tree that the distance matrix is for was a rooted tree but the root node only had two children, that node won't show up at all in the reconstructed tree (simple tree).

```{svgbob}
ORIGINAL           RECONSTRUCTED   

   R (root)             2
1 / \ 1              A-----B
 /   \
A     B
```

In the example above, the root node had degree_GRAPH of 2, meaning it won't appear in the reconstructed simple tree. Even if it did, the reconstruction would be an unrooted tree -- the node would be there but nothing would identify it as the root.
````

```{output}
ch8_code/src/clustering/Soft_HierarchialClustering_NeighbourJoining.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN\s*[\n$]
```

```{ch8}
clustering.Soft_HierarchialClustering_NeighbourJoining
{
  metric: euclidean,  # OPTIONS: euclidean, manhattan, cosine, pearson
  vectors: {
    VEC1: [5,6,5],
    VEC2: [5,7,5],
    VEC3: [30,31,30],
    VEC4: [29,30,31],
    VEC5: [31,30,31],
    VEC6: [15,14,14]
  },
  edge_scale: 0.2
}
```

Another potentially more useful metric is to estimate an ideal edge weight for the tree. Assuming the ...

 1. vectors being clustered have some type of "cluster-able" relationship to each other (not junk data),
 2. distance metric used is appropriate for capturing that "cluster-able" relationship

..., the unrooted tree generated by neighbour joining phylogeny will likely have some form of blossoming: A blossom is a region of the tree that has at least 2 leaf nodes, where those leaf nodes are all a short distance from one one another.

```{svgbob}
  * * * * *                   
   \|/  |/                 
*---*---*                  
   / \                     
  *   \                *   
       \              /   
        *---*--------*---*
       /     \        \  |\
      /       \        * * *
     /         \
    /           \
*--*--*          \
   |\             *
   * *
```

Since the leaf nodes within a blossom are a short distance from one another, they represent highly related vectors. As such, it's safe to assume that a blossom represents a cluster. Edges within a blossom are typically short (low weight), whereas longer edges (high weight) are either used for connecting together blossoms or are limbs that represent outliers.

In the example above and below, the three blossoming regions represent individual clusters and there's 1 outlier.

```{svgbob}

 "CLUSTER 2"              
  o o o o o               
   \|/  |/                
o---o---o                 
   / \                    
  o   \                o  
       \              /   
        *---*--------o---o
       /     \        \  |\
      /       \        o o o
     /         \       "CLUSTER 3"
    /           \
o--o--o          \
   |\             *
   o o         "OUTLIER"
"CLUSTER 1"

"* Cluster nodes denoted by empty circle"
```

One heuristic for identifying blossoms is to statistically infer an "ideal" edge weight and then perform a fan out process. For each internal node, recursively fan out along all paths until either  ...

 * a path's accumulated edge weights reaches at most the "ideal" edge weight.
 * a path reaches a leaf node.

```{output}
ch8_code/src/clustering/Soft_HierarchialClustering_NeighbourJoining_v2.py
python
# MARKDOWN_ESTIMATE_OWNERSHIP\s*\n([\s\S]+)\n\s*# MARKDOWN_ESTIMATE_OWNERSHIP\s*[\n$]
```

Any internal node fan outs that touch a leaf node potentially identify some region of a blossom. If any of these "leaf node touching" fan outs overlap (walk over any of the same nodes), they're merged together. The final set of merged fan outs should capture the blossoms within a tree.

```{output}
ch8_code/src/clustering/Soft_HierarchialClustering_NeighbourJoining_v2.py
python
# MARKDOWN_MERGE_OVERLAPS\s*\n([\s\S]+)\n\s*# MARKDOWN_MERGE_OVERLAPS\s*[\n$]
```

There is no definitive algorithm for calculating the "ideal" edge weight. One heuristic is to collect the trees' edge weights, sort them, then attempt to use each one as the "ideal" edge weight (from smallest to largest). At some point in the attempts, the number of blossoms returned by the algorithm will peak. The "ideal" edge weight should be somewhere around the peak.

Depending on how big the tree is, it may be too expensive to try each edge weight. One workaround is to create buckets of averages. For example, split the sorted edge weights into 10 buckets and average each bucket. Try each of the 10 averages as the "ideal" edge weight.

```{note}
The concept of an "ideal" edge weight is similar to the concept of a similarity graph's threshold value (described in Algorithms/Gene Clustering/Similarity Graph Clustering_TOPIC): Items within the same cluster should be closer together than items in different clusters.
```

```{output}
ch8_code/src/clustering/Soft_HierarchialClustering_NeighbourJoining_v2.py
python
# MARKDOWN_MEAN_RANGE\s*\n([\s\S]+)\n\s*# MARKDOWN_MEAN_RANGE\s*[\n$]
```

````{note}
I had also thought up this metric: distorted average. That's the name I gave it but the official name for this may be something different.

```{kt}
d\_avg(D) = (\sum_{i=1}^{n}{{D_i}^{\frac{1}{e}}})^e
```

 * D is list of all edge weights in the graph
 * n is the elements in D
 * e is some number >= 1, typically set to 2 (higher means more resilient to outliers)

The distorted average is a concept similar to squared error distortion (k-means optimization metric). It calculates the average, but lessens the influence of outliers. For example, given the inputs [3, 3, 3, 3, 3, 3, 3, 3, 15], the last element (15) is an outlier. The following table shows the distorted average for both outlier included and outlier removed with different values of e ...

| e | without 15 | with 15 |
|---|------------|---------|
| 1 | 3          | 4.33    |
| 2 | 3          | 3.88    |
| 3 | 3          | 3.76    |
| 4 | 3          | 3.71    |

The idea is that most of the edges in the graph will be in the blossoming regions. The much larger edges that connect together those blossoming regions will be much fewer, meaning that they'll get treated as if they're outliers and their influence will be reduced.

In practice, with real-world data, distorted average performed poorly.

* There's noise.
* There are more than a handful of outliers.
* One outlier could be so disproportionately huge that it throws off the distorted average anyway (having less influence doesn't mean it has no influence).
* etc..
````

```{output}
ch8_code/src/clustering/Soft_HierarchialClustering_NeighbourJoining_v2.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN\s*[\n$]
```

```{ch8}
clustering.Soft_HierarchialClustering_NeighbourJoining_v2
{
  metric: euclidean,  # OPTIONS: euclidean, manhattan, cosine, pearson
  vectors: {
    VEC1: [5,6,5],
    VEC2: [5,7,5],
    VEC3: [30,31,30],
    VEC4: [29,30,31],
    VEC5: [31,30,31],
    VEC6: [15,14,14]
  },
  dist_capture: 5.0,
  edge_scale: 0.2
}
```

### Similarity Graph Clustering

`{bm} /(Algorithms\/Gene Clustering\/Similarity Graph Clustering)_TOPIC/`

```{prereq}
Algorithms/Gene Clustering/Euclidean Distance Metric_TOPIC
Algorithms/Gene Clustering/Manhattan Distance Metric_TOPIC
Algorithms/Gene Clustering/Cosine Similarity Metric_TOPIC
Algorithms/Gene Clustering/Pearson Similarity Metric_TOPIC
```

**WHAT**: Given a list of n-dimensional vectors, ...

1. convert those vectors into a similarity matrix
2. build a graph where nodes represent vectors and an edge connects a pair of nodes only if the similarity between the vectors they represent exceeds some threshold.

This type of graph is called a similarity graph.

**WHY**: Recall the definition of the good clustering principle: Items within the same cluster should be more similar to each other than items in other clusters. If the vectors being clustered aren't noisy and the similarity metric used is appropriate for the type of data the vectors represent (it captures clusters), some threshold value should exist where the graph formed only consists of cliques (clique graph).

For example, consider the following similarity matrix...

|   | a | b | c | d | e | f | g |
|---|---|---|---|---|---|---|---|
| a | 9 | 8 | 9 | 1 | 0 | 1 | 1 |
| b | 8 | 9 | 9 | 1 | 1 | 0 | 2 |
| c | 9 | 9 | 8 | 2 | 1 | 1 | 1 |
| d | 1 | 1 | 2 | 9 | 8 | 9 | 9 |
| e | 0 | 1 | 1 | 8 | 8 | 8 | 9 |
| f | 1 | 0 | 1 | 9 | 8 | 9 | 9 |
| g | 1 | 2 | 1 | 9 | 9 | 9 | 8 |

Choosing a threshold of 7 will generate the following clique graph...

```{svgbob}
g---e
|\ /|
| X |
|/ \|
d---f   c
       / \
      a---b
```

When working with real-world data, similarity graphs often end up with corrupted cliques. The reason this happens is that real-world data is typically noisy and / or the similarity metrics being used might not perfectly capture clusters.

```{svgbob}
e---g     
|\ /|\    
| X | \   
|/ \|  \  
d   f   c 
       / \
      a   b

* "Previous graph but cliques are corrupted."
```

These corrupted cliques may be fixed using heuristic algorithms. The algorithm for this section is one such algorithm.

**ALGORITHM**:

As described above, a similarity graph represents vectors as nodes where an edge connects a pair of nodes only if the similarity between the vectors they represent exceeds some threshold.

```{output}
ch8_code/src/clustering/SimilarityGraph_CAST.py
python
# MARKDOWN_SIM_GRAPH\s*\n([\s\S]+)\n\s*# MARKDOWN_SIM_GRAPH\s*[\n$]
```

```{ch8}
clustering.SimilarityGraph_CAST main_similarity_graph
{
  metric: euclidean,  # OPTIONS: euclidean, manhattan, cosine, pearson
  vectors: {
    VEC1: [5,6,5],
    VEC2: [5,7,5],
    VEC3: [30,31,30],
    VEC4: [29,30,31],
    VEC5: [31,30,31],
    VEC6: [15,14,14]
  },
  threshold: -10
}
```

If the resulting similarity graph isn't a clique graph but is close to being one (corrupted cliques), a heuristic algorithm called cluster affinity search technique (CAST) can correct it. At its core, the algorithm attempts to re-create each corrupted clique in its corrected form by iteratively finding the ...
 
1. closest node not in the clique/cluster and including it _if it exceeds the similarity graph threshold_.
2. farthest node within the clique/cluster and removing it _if it doesn't exceed the similarity graph threshold_.
   
```{svgbob}
"original:"

  a---d
 /|\  |
t | \ |
  |  \|
  b---c
 


"step1:"            "step2:"            "step3:"
"prime with a"      "add t"             "add b, remove t"

  a                   a                   a
                     /                    |
                    t                     |
                                          |
                                          b


"step4:"            "step4:"            "step5:   (done)"
"add c"             "add d"             "nothing to add/remove"
                    
  a                   a---d               a---d
  |\                  |\ /|               |\ /|
  | \                 | X |               | X |
  |  \                |/ \|               |/ \|
  b---c               b---c               b---c
```

How close or far a gene is from the clique/cluster is defined as the average similarity between that node and all nodes in the clique/cluster

```{output}
ch8_code/src/clustering/SimilarityGraph_CAST.py
python
# MARKDOWN_ADJUST\s*\n([\s\S]+)\n\s*# MARKDOWN_ADJUST\s*[\n$]
no_preamble
```

```{note}
Removal is testing a node from _within_ the cluster itself. That is, the removal node for which the average similarity is being calculated has the similarity to itself included in the averaging.
```

While the similarity graph has nodes, the algorithm picks the node with the highest degree_GRAPH from the similarity graph to prime a clique/cluster. It then loops the add and remove process described above until there's an iteration where nothing changes. At that point, that cluster/clique is said to be consistent and its nodes are removed from the original similarity graph. 

```{note}
What's the significance of picking the node with the highest degree_GRAPH as the starting point? It was never explained, but I suspect it's a heuristic of some kind. Something like, the node with the highest degree_GRAPH is assumed to have most of its edges to other nodes in the same clique and as such it's the most "representative" member_CLUSTER of the cluster that clique represents.

Something like that.
```

```{output}
ch8_code/src/clustering/SimilarityGraph_CAST.py
python
# MARKDOWN_CAST\s*\n([\s\S]+)\n\s*# MARKDOWN_CAST\s*[\n$]
```

```{ch8}
clustering.SimilarityGraph_CAST main_cast
{
  metric: euclidean,  # OPTIONS: euclidean, manhattan, cosine, pearson
  vectors: {
    VEC1: [5,6,5],
    VEC2: [5,7,5],
    VEC3: [30,31,30],
    VEC4: [29,30,31],
    VEC5: [31,30,31],
    VEC6: [15,14,14]
  },
  threshold: -15.2
}
```

# Stories

## Bacterial Genome Replication

`{bm} /(Stories\/Bacterial Genome Replication)_TOPIC/`

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

`{bm} /(Stories\/Bacterial Genome Replication\/Find Ori and Ter)_TOPIC/`

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

`{bm} /(Stories\/Bacterial Genome Replication\/Find the DnaA Box)_TOPIC/`

```{prereq}
Stories/Bacterial Genome Replication/Find Ori and Ter_TOPIC
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

`{bm} /(Stories\/Transcription Factors)_TOPIC/`

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

`{bm} /(Stories\/Transcription Factors\/Find Regulatory Motif)_TOPIC/`

```{prereq}
Algorithms/Motif/Find Motif Matrix_TOPIC
```

Given an organism, it's suspected that some physical change in that organism is linked to a transcription factor. However, it isn't known ...

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

## Non-ribosomal Peptides

`{bm} /(Stories\/Non-ribosomal Peptides)_TOPIC/`

A peptide is a miniature protein consisting of a chain of amino acids anywhere between 2 to 100 amino acids in length. 

```{svgbob}
G - N - S - K - N - ...
```

Most peptides are synthesized through the central dogma of molecular biology: a segment of the DNA that encodes the peptide is transcribed to mRNA, which in turn is translated to a peptide by a ribosome.

```{svgbob}
  DNA
   |
   | transcribed
   |
   v
 mRNA
   |
   | translated
   |
   v
peptide
```

Non-ribosomal peptides (NRP) however, aren't synthesized via the central dogma of molecular biology. Instead, giant proteins typically found in bacteria and fungi called NRP synthetase build out these peptides by growing them one amino acid at a time.

```{svgbob}
.------------.   .------------.   .------------.   .------------.   .------------.
|   NRP      |   |   NRP      |   |   NRP      |   |   NRP      |   |   NRP      |
| synthetase |   | synthetase |   | synthetase |   | synthetase |   | synthetase |
`----. .-----'   `----. .-----'   `----. .-----'   `----. .-----'   `----. .-----'
      N                K                S                N                G       
                       |                |                |                |
                       N                K                S                N
                                        |                |                |
                                        N                K                S
                                                         |                |
                                                         N                K
                                                                          |
                                                                          N
```

Each segment of an NRP synthetase protein responsible for the outputting a single amino acid is called an adenylation domain. The example above has 5 adenylation domains, each of which is responsible for outputting a single amino acid of the peptide it produces.

NRPs may be `{bm-target} cyclic/cyclopeptide`. Common use-cases for NRPs:

 * antibiotics
 * anti-tumor agents
 * immunosuppressors
 * communication between bacteria (quorum sensing)

```{note}
According to the Wikipedia article on NRPs, there exist a wide range of peptides that are not synthesized by ribosomes but the term non-ribosomal peptide typically refers to the ones synthesized by NRP synthetases.
```

### Find Sequence

`{bm} /(Stories\/Non-ribosomal Peptides\/Find Sequence)_TOPIC/`

```{prereq}
Algorithms/Peptide Sequence/Spectrum Sequence_TOPIC
```

Unlike ribosomal peptides, NRPs aren't encoded in the organism's DNA. As such, their sequence can't be inferred by directly by looking through the organism's DNA sequence.

Instead, a sample of the NRP needs to be isolated and passed through a mass spectrometer. A mass spectrometer is a device that shatters and bins molecules by their mass-to-charge ratio: Given a sample of molecules, the device randomly shatters each molecule in the sample (forming ions), then bins each ion by its mass-to-charge ratio (`{kt} \frac{m}{z}`).

The output of a mass spectrometer is a plot called a spectrum_MS. The plot's ...

 * x-axis is the mass-to-charge ratio.
 * y-axis is the intensity of that mass-to-charge ratio (how much more / less did that mass-to-charge appear compared to the others).

```{svgbob}
    y
    ^
    |
    |        |
    |        |
"%" |        |
    |        | |           |
    |        | |           |
    | |      | | |         |        |
    | | | |  | | |     |   |    | | |
    +-+-+-+--+-+-+-----+---+----+-+-+--> x
                     "m/z"
```

For example, given a sample containing multiple instances of the linear peptide NQY, the mass spectrometer will take each instance of NQY and randomly break the bonds between its amino acids:

```{svgbob}
N ---- Q ---- Y   "(NQY not broken)"

N -//- Q ---- Y   "(NQY broken to N and QY)"

N ---- Q -//- Y   "(NQY broken to NQ and Y)"

N -//- Q -//- Y   "(NQY broken to N, Q, and Y)"
```

Each subpeptide then will have its mass-to-charge ratio measured, which in turn gets converted to a set of potential masses by performing basic math. With these potential masses, it's possible to infer which amino acids make up the peptide as well as the peptide sequence.

In the example below, peptide sequences are inferred from a noisy spectrum_MS for the cyclopeptide Viomycin. The elements of each inferred peptide sequence are amino acid masses rather than the amino acids themselves (e.g. instead of S being output at a position, the mass of S is output -- 87). Since the spectrum_MS is noisy, the inferred peptide sequences are also noisy (e.g. instead of an amino acid mass 87 showing up as exactly 87 in the peptide sequence, it may show up as 87.2, 86.9, etc...).

Note that the correct peptide sequence isn't guaranteed to be inferred. Also, since Viomycin is a cyclopeptide, the correct peptide may be inferred in a wrapped form (e.g. the cyclopeptide 128-113-57 may show up as 128-113-57, 113-57-128, or 57-128-113).

```{note}
I artificially generated a spectrum_MS for Viomycin from the sequence listed on [KEGG](https://www.genome.jp/dbget-bin/www_bget?cpd:C01540). 

> Sequence 	 0 beta-Lys  1 Dpr  2 Ser  3 Ser  4 Ala  5 Cpd  (Cyclization: 1-5)
>
> Gene 	0 vioO [UP:Q6WZ98] vioM [UP:Q6WZA0]; 1 vioF [UP:Q6WZA7]; 2-3 vioA
[UP:Q6WZB2]; 4 vioI [UP:Q6WZA4]; 5 vioG [UP:Q84CG4]
>
> Organism 	 Streptomyces vinaceus
>
> Type 	NRP

The problem is that I have no idea what the 5th amino acid is: Cpd (I arbitrarily put it's mass as 200) and I'm unsure of the mapping I found for Dpr (2,3-diaminopropionic acid has mass of 104). The peptide sequence being searched for in the example below is 128-104-87-87-71-200.
```

```{ch4}
SequencePeptide_Leaderboard
0.0 71.2 87.1 104.0 127.9 158.0 174.0 191.0 200.0 232.0 245.0 271.0 319.0 328.0 358.0 399.0 406.0 432.0 445.0 477.1 490.0 492.0 503.1 530.5 548.7 572.9 590.1 606.1 677.0
0.3
1
1
24
cyclic
6
0
30
```

## Genome Rearrangement

`{bm} /(Stories\/Genome Rearrangement)_TOPIC/`

Genome rearrangement is form of mutation where chromosomes go through structural changes. These structural changes include chromosome segments getting ... 

 * shuffled into a different order (translocation, fission, fusion) or direction (reversal).
 
   For example, a segment of chromosome breaks off and rejoins, but each end of that segment joins back up at a different point.

   ```{svgbob}
   "Reversal Example"

                                  .--------------.
   "BEFORE:"    A1 ->  A2 -> A3 -> A4 -> A5 -> A6 -> A7 -> A8 -> A9
   "AFTER:"     A1 ->  A2 -> A3 -> A7 <- A6 <- A5 -> A7 -> A8 -> A9
                                  '--------------'
   ```

   ```{svgbob}
   "Translocation Example"

                     .--------------.
   "BEFORE:"    A1 -> A2 -> A3 -> A4 -> A5 -> A6 -> A7 -> A8 -> A9
   "AFTER:"     A1 -> A5 -> A6 -> A7 -> A8 -> A2 -> A3 -> A4 -> A9
                                             '--------------'
   ```

   ```{svgbob}
   "Chromosome Fusion Example"

                                             .--------.
   "BEFORE:"    A1 -> A2 -> A3 -> A4 -> A5 -> A6    B1 -> B2 -> B3
   "AFTER:"     A1 -> A2 -> A3 -> A4 -> A5 -> A6 -> B1 -> B2 -> B3
                                             '--------'
   ```

   ```{svgbob}
   "Chromosome Fission Example"

                                             .--------.
   "BEFORE:"    A1 -> A2 -> A3 -> A4 -> A5 -> A6 -> B1 -> B2 -> B3
   "AFTER:"     A1 -> A2 -> A3 -> A4 -> A5 -> A6    B1 -> B2 -> B3
                                             '--------'
   ```

 * deleted.
 
   For example, a segment of a chromosome breaks off and DNA repair mechanisms close the gap.

   ```{svgbob}
   "Deletion Example"

                     .--------------.
   "BEFORE:"    A1 -> A2 -> A3 -> A4 -> A5 -> A6 -> A7 -> A8 -> A9
   "AFTER:"     A1 -> A5 -> A6 -> A7 -> A8 -> A9
   ```

 * duplicated.
 
   For example, a segment of a chromosome breaks off and DNA repair mechanisms close the gap, but that broken off segment may still re-attach at a different location.

   ```{svgbob}
   "Duplication Example"

                     .--------.
   "BEFORE:"    A1 -> A2 -> A3 -> A4 -> A5 -> A6 -> A7 -> A8 -> A9
   "AFTER:"     A1 -> A2 -> A3 -> A4 -> A5 -> A6 -> A7 -> A8 -> A2 -> A3 -> A9
                                                               '--------'
   ```

There are fragile regions of chromosomes where breakages are more likely to occur. For example, the ABL-BCR fusion protein, a protein implicated in the development of a cancer known as chronic myeloid leukemia, is the result of human chromosomes 9 and 22 breaking and fusing back together in a different order: Chromosome 9 contains the gene for ABL while chromosome 22 contains the gene for BCR and both genes are in fragile regions of their respective chromosome. If those fragile chromosome regions both break but fuse back together in the wrong order, the ABL-BCR chimeric gene is formed.

As shown with the ABL-BCR fusion protein example above, genome rearrangements often result in the sterility or death of the organism. However, when a species branches off from an existing one, genome rearrangements are likely responsible for at least some of the divergence. That is, the two related genomes will share long stretches of similar genes, but these long stretches will appear as if they had been randomly cut-and-paste and / or randomly reversed when compared to the other. For example, humans and mice have a shared ancestry and as such share a vast number of long stretches (around 280).

These long stretches of similar genes are called synteny blocks. For example, the following genome rearrangement mutations result in 4 synteny blocks shared between the two genomes ...

```{svgbob}
                                    "translocate"
                 .---------------------------------------------------.
                 |                              "reverse"            |
                 |                    .---------------------------.  |
            .----+---.        .-------+------.                    |  |
"GENOME1:"   G1 -> G2 -> G3 -> G4 -> G5 -> G6 -> G7 -> G8 -> G9   |  |
"GENOME2:"   G3 -> G6 <- G5 <- G4 -> G7 -> G8 -> G9 -> G1 -> G2   |  |
                  '-------+------'                    '----+---'  |  |
                          `--------------------------------+------'  |
                                                           `---------'
```

 * Synteny block 1: `[G1, G2]`
 * Synteny block 2: `[G3]`
 * Synteny block 3: `[G4, G5, G6]` (although they're reversed)
 * Synteny block 4: `[G7, G8, G9]`

### Find Synteny Blocks

`{bm} /(Stories\/Genome Rearrangement\/Find Synteny Blocks)_TOPIC/`

```{prereq}
Algorithms/Synteny/Genomic Dot Plot_TOPIC
Algorithms/Synteny/Synteny Graph_TOPIC
```

Synteny blocks are identified by first finding matching k-mers and reverse complement matching k-mers, then combining matches that are close together (clustering) to reveal the long stretches of matches that make up synteny blocks.

The visual manifestation of this concept is the genomic dot-plot and synteny graph. A genomic dot-plot is a 2D plot where each axis is assigned to one of the genomes and a dot is placed at each coordinate containing a match, while a synteny graph is the clustered form of a genomic dot-plot that reveals synteny blocks.

```{svgbob}
 * "N = normal k-mer match"
 * "R = reverse complement k-mer match"

3'|                                                                                  3'|                                                                 
  |  R                              R                                                  |  *                                                              
  |   R           N                                                                    |   \                                                             
  |    R               R                                                               |    \                                                            
  |      R                           R           N                                     |     \                                                           
  |       R                                                                            |      \                                                          
  |       R               N                                                            |     A \                                                         
 g|        R                                                                          g|        \                                                        
 e|          R                   R           N                                        e|         \                                                      
 n|           R                                                                       n|          \                                                     
 o|            R                                     R                   ------->     o|           v                                                    
 m|   N                        N                                         CLUSTER      m|                           ^                                    
 e|                          N            N                                           e|                        C /                                      
 1|      N                  N                                                         1|                         /                                      
  |                        N               N         N                                 |                        *                                          
  |                 R                                                                  |                 *                                               
  |                   R                                                                |                  \                                             
  |                    R                                                               |                 B \                                           
  |    R                R                                                              |                    v                                               
  |                                           R              R                         |                                           *                     
  |             N              N                R                                      |                                            \                    
  |                                              R           R                         |                                           D \                    
5'|       R             R                   R     R                                  5'|                                              v                  
  +-----------------------------------------------------------------                   +-----------------------------------------------------------------
   5'                          genome2                            3'                    5'                          genome2                            3'

 * "Remember that the direction of DNA is 5' to 3'."
```

The synteny graph above reveals that 4 synteny blocks are shared between the genomes. One of the synteny blocks is a normal match (C) while three are matching against their reverse complements (A, B, and D).

```{svgbob}
* "Synteny blocks projected on to each axis."

     -D       -B      +C          -A                               +A              +B        +C                  +D   
--<<<<<<<--<<<<<<<-->>>>>>>--<<<<<<<<<<<<<<--      vs       -->>>>>>>>>>>>>>----->>>>>>>--->>>>>>>------------->>>>>>>---------
 5'                  genome1              3'                 5'                          genome2                            3'
```

In the example below, two species of the Mycoplasma bacteria are analyzed to find the synteny blocks between them. The output reveals that pretty much the entirety of both genomes are shared, just in a different order.

```{ch6}
FindSyntenyBlocksBetweenGenomes
[[G1C1, /input/ch6_code/src/Mycoplasma bovis - GCA_000696015.1_ASM69601v1_genomic.fna.xz]]
[[G2C1, /input/ch6_code/src/Mycoplasma agalactiae 14628 - GCA_000266865.1_ASM26686v1_genomic.fna.xz]]
cyclic
20
graph_show
[merge, 25, 90]
[merge, 50, 90]
[merge, 100, 90]
[merge, 200, 90]
[merge, 400, 90]
[merge, 800, 90]
[merge, 1600, 90]
[merge, 3200, 90]
[filter, 3200, 20000]
[merge, 6400, 90]
[merge, 12800, 90]
[cull, 10000]
```

### Find Reversal Path

`{bm} /(Stories\/Genome Rearrangement\/Find Reversal Path)_TOPIC/`

```{prereq}
Stories/Genome Rearrangement/Find Synteny Blocks_TOPIC
Algorithms/Synteny/Reversal Path/Breakpoint Graph Algorithm_TOPIC
```

A reversal is the most common type of genome rearrangement mutation: A segment of chromosome breaks off and ends up re-attaching, but with the ends swapped.

```{svgbob}
            "Scenario 1"                                                     "Scenario 2"

"Original:"                                                    "Original:"
-->-->-->-->-->-->-->-->-->-->-->-->--                         -->-->-->-->-->-->-. .->-->-->-->-->-->--
                                                                                  | |                   
                                                                              .-<-' '-<-.               
                                                                              '->-->-->-'               

"Interval breaks:"                                             "Interval breaks:"
             ->-->-->-->-                                      -->-->-->-->-->-->-. .->-->-->-->-->-->--
-->-->-->-->-            ->-->-->-->--                                                                  
                                                                              .-<-' '-<-.               
                                                                              '->-->-->-'               

"Interval flips around:"                                       "Interval ends re-attach in swapped order:"
             -<--<--<--<-                                      -->-->-->-->-->-->-. .->-->-->-->-->-->--
-->-->-->-->-            ->-->-->-->--                                             X                    
                                                                              .-<-' '-<-.               
                                                                              '->-->-->-'

"Reversed interval re-attaches:"                                                           
-->-->-->-->--<--<--<--<-->-->-->-->--               
```

The theory is that genome rearrangements between two species take the parsimonious path (or close to it). Since reversals are the most common form of genome rearrangement mutation, by calculating a parsimonious reversal path (smallest set of reversals) it's possible to get an idea of how the two species branched off.

Note that there may be many parsimonious reversal paths between two genomes with shared synteny blocks.

```{svgbob}
                              +B     +C       -A      +D       -E                        +A     +B      +C       +D       +E                      
                           -->>>>>-->>>>>---<<<<<-->>>>>>>>>--<<<<<--       vs        -->>>>>-->>>>>--->>>>>-->>>>>>>>>-->>>>>--



         "Parsimonious reversal path 1"                          "Parsimonious reversal path 2"                          "Parsimonious reversal path 3"  
                                                                                                                                                          
                                  .-----.                .--------------------.                                  .------------.                           
   +B     +C      -A       +D       -E                     +B     +C      -A       +D       -E                     +B     +C      -A       +D       -E    
-->>>>>-->>>>>---<<<<<-->>>>>>>>>--<<<<<--              -->>>>>-->>>>>---<<<<<-->>>>>>>>>-->>>>>--              -->>>>>-->>>>>---<<<<<-->>>>>>>>>-->>>>>--
                                                                                                                                                          
 .--------------------.                                                                   .-----.                                                 .-----.
   +B     +C      -A       +D       +E                     +A     -C      -B       +D       -E                     -C     -B      -A       +D       -E   
-->>>>>-->>>>>---<<<<<-->>>>>>>>>-->>>>>--              -->>>>>-->>>>>---<<<<<-->>>>>>>>>--<<<<<--              -->>>>>-->>>>>---<<<<<-->>>>>>>>>--<<<<<-
                                                                                                                                                        
        .-------------.                                         .-------------.                                         .-------------.                   
   +A     -C      -B       +D       +E                     +A     -C      -B       +D       +E                     +A     -C      -B       +D       +E    
-->>>>>--<<<<<---<<<<<-->>>>>>>>>-->>>>>--              -->>>>>--<<<<<---<<<<<-->>>>>>>>>-->>>>>--              -->>>>>--<<<<<---<<<<<-->>>>>>>>>-->>>>>--
                                                                                                                                                          
                                                                                                                                                          
   +A     +B      +C       +D       +E                     +A     +B      +C       +D       +E                     +A     +B      +C       +D       +E    
-->>>>>-->>>>>--->>>>>-->>>>>>>>>-->>>>>--              -->>>>>-->>>>>--->>>>>-->>>>>>>>>-->>>>>--              -->>>>>-->>>>>--->>>>>-->>>>>>>>>-->>>>>--
```

Given a parsimonious reversal path, it may be that one of the genomes in the reversal path is the parent species (or close to it).

```{svgbob}
                                   +A     -C      -B       +D       +E    
                                -->>>>>--<<<<<---<<<<<-->>>>>>>>>-->>>>>--
                                                 PARENT

                                                   |
                   .-------------------------------+-------------------------------.
                   |                                                               v
                   |
                   |                                         .--------------------.
                   |                                           +A     -C      -B       +D       +E    
                   v                                        -->>>>>--<<<<<---<<<<<-->>>>>>>>>-->>>>>--

        .-------------.                                                                       .-----.
   +A     -C      -B       +D       +E                         +B     +C      -A       +D       +E    
-->>>>>--<<<<<---<<<<<-->>>>>>>>>-->>>>>--                  -->>>>>-->>>>>---<<<<<-->>>>>>>>>-->>>>>--


   +A    "+B      +C       +D       +E                         +B     +C      -A       +D       -E    
-->>>>>-->>>>>--->>>>>-->>>>>>>>>-->>>>>--                  -->>>>>-->>>>>---<<<<<-->>>>>>>>>--<<<<<--
```

In the example below, two species of the Mycoplasma bacteria are analyzed to find a parsimonious reversal path using the breakpoint graph_GR algorithm. The output reveals that only 1 reversal is responsible for the change in species. As such, it's very likely that one species broke off from the other rather than there being a shared parent species.

```{ch6}
FindReversalPathBetweenGenomes
[[G1C1, /input/ch6_code/src/Mycoplasma bovis - GCA_000696015.1_ASM69601v1_genomic.fna.xz]]
[[G2C1, /input/ch6_code/src/Mycoplasma agalactiae 14628 - GCA_000266865.1_ASM26686v1_genomic.fna.xz]]
cyclic
20
graph_show
[merge, 25, 90]
[merge, 50, 90]
[merge, 100, 90]
[merge, 200, 90]
[merge, 400, 90]
[merge, 800, 90]
[merge, 1600, 90]
[merge, 3200, 90]
[filter, 3200, 20000]
[merge, 6400, 90]
[merge, 12800, 90]
[cull, 10000]
```

## Evolutionary History

`{bm} /(Stories\/Evolutionary History)_TOPIC/`

When scientists work with biological entities, those entities are either present day entities or relics of extinct entities (paleontology). In certain cases, it's reasonable to assume the shared ancestry of a set of present day entities by comparing their features to those of extinct relics. For example, ...

 * modern day big cats (e.g. leopards and tigers) probably derived from saber-toothed tigers.
 * modern day elephants (e.g. african elephants and indian elephants) probably derived from mammoths.

```{svgbob}
                         * "Unknown Ancestor"
                        / \
               .-------'   '-------.       
               |                   |
Saber-toothed  *                   *  Mammoth  
Tiger         / \                 / \    
          .--'   '--.         .--'   '--.
          |         |         |         | 
          *         *         *         *
       Leopard    Tiger   African     Indian
                          Elephant    Elephant
```

In most cases however, there are no relics. For example, extinct viruses or bacteria typically don't leave much evidence around in the same way that ...

 * extinct dinosaur species have their bones found underground.
 * extinct insect species are found encased in amber.
 * extinct arctic species are found encased in ice.

In such cases, it's still possible to infer the evolutionary history of a set of present day species by comparing their features to see how diverged they are. Those features could be phenotypic features (e.g. behavioural or physical features) or molecular features (e.g. DNA sequences, protein sequences, organelles and other cell features).

The process of inferring evolutionary history by comparing features for divergence is called phylogeny. Phylogeny algorithms provide insight into ...

 * the shared ancestry of a set of present day entities.
 * how similar each present day entity is to its ancestor.
 * what the features of the ancestor likely were.

```{svgbob}
                         * "Ancestor A" "(4 legs, teeth)"
                        / \ 
               .-------'   '-------.       
               |                   |
               |                   *  "Ancestor C"
               |                  / \ "(trunk, tusks, flat teeth, 4 legs)"
 "Ancestor B"  *              .--'   '--.
 "(4 legs,"   / \             |         | 
 "furry," .--'   '--.         |         |
 "sharp"  |         |         *         *
 "teeth)" |         *     African     Indian
          |       Tiger   Elephant    Elephant
          |               
          *               
       Leopard

"* vertical edge length denotes similarity to ancestor (closer = more similar)"
"* ancestor features in brackets"
"* ancestors not assumed to be a particular species (e.g. saber-toothed tiger)"
```

Oftentimes, phylogeny produces much more accurate results than simply eye-balling it (as was done in the initial example), but ultimately the quality of the result is dependent on what features are being measured and the metric used for measurement. Prior to sequencing technology, most phylogeny was done by comparing phenotypic features (e.g. character tables). Common practice now is to use molecular features (e.g. DNA sequencing) since those have more information that's definitive and less biased (e.g. phenotypic features are subject to human interpretation).

### Find Evolutionary Tree

`{bm} /(Stories\/Evolutionary History\/Find Evolutionary Tree)_TOPIC/`

```{prereq}
Algorithms/Phylogeny/Distance Matrix to Tree_TOPIC
Algorithms/Sequence Alignment/Global Alignment_TOPIC
Algorithms/Sequence Alignment/Protein Scoring/BLOSUM Scoring Matrix_TOPIC
```

Evolutionary history is often displayed as a tree called a phylogenetic tree, where leaf nodes represent known entities and internal nodes represent inferred ancestor entities. Depending on the phylogeny algorithm used, the tree may be either a rooted tree or an unrooted tree. The difference is that a rooted tree infers parent-child relationships of ancestors while an unrooted tree does not.

```{svgbob}
                      ROOTED                                                   UNROOTED

                         * "Ancestor A"           
                        / \                                          Entity1               Entity3
               .-------'   '-------.                                    *---.           .----*
               |                   |                                         \         /
 "Ancestor B"  *                   *  "Ancestor C"               "Ancestor B" *-------* "Ancestor C"
              / \                 / \                                        /         \
          .--'   '--.         .--'   '--.                               *---'           '----*
          |         |         |         |                            Entity2               Entity4
          *         *         *         *         
       Entity1   Entity2   Entity3   Entity4      
```

In the example above, the rooted tree (left diagram) shows ancestors B and C as branching off (evolving) from their common ancestor A. The unrooted tree (right diagram) shows ancestors B and C but doesn't provide infer which branched off the other. It could be that ancestor B ultimately descended from C or vice versa.

SARS-CoV-2 is the virus that causes COVID-19. The example below measures SARS-CoV-2 spike protein sequences collected from different patients to produce its evolutionary history. The metric used to measure how diverged two sequences are from each other is global alignment using a BLOSUM80 scoring matrix. Once divergences (distances) are calculated, the neighbour joining phylogeny algorithm is used to generate a phylogenetic tree.

```{note}
BLOSUM80 was chosen because SARS-CoV-2 is a relatively new virus (~2 years). I don't know if it was a good choice because I've been told viruses mutate more rapidly, so maybe BLOSUM62 would have been a better choice.

The original NCBI dataset had 30k to 40k unique spike sequences. I couldn't justify sticking all of that into the git repo (too large) so I whittled it down to a random sample of 1000.

From that 1000, only a small sample are selected to run the code. The problem is that sequence alignments are computationally expensive and Python is slow. Doing a sequence alignment between two spike protein sequences on my VM takes a long time (~4 seconds per alignment), so for the full 1000 sequences the total running time would end up being ~4 years (if I calculated it correctly - single core).
```

```{ch7}
PracticalSARSCoV2PhylogenyTree
1000_unique_sarscov2_spike_seqs.json.xz
6
0.1
   A  R  N  D  C  Q  E  G  H  I  L  K  M  F  P  S  T  W  Y  V  B  J  Z  X  *
A  5 -2 -2 -2 -1 -1 -1  0 -2 -2 -2 -1 -1 -3 -1  1  0 -3 -2  0 -2 -2 -1 -1 -6
R -2  6 -1 -2 -4  1 -1 -3  0 -3 -3  2 -2 -4 -2 -1 -1 -4 -3 -3 -1 -3  0 -1 -6
N -2 -1  6  1 -3  0 -1 -1  0 -4 -4  0 -3 -4 -3  0  0 -4 -3 -4  5 -4  0 -1 -6
D -2 -2  1  6 -4 -1  1 -2 -2 -4 -5 -1 -4 -4 -2 -1 -1 -6 -4 -4  5 -5  1 -1 -6
C -1 -4 -3 -4  9 -4 -5 -4 -4 -2 -2 -4 -2 -3 -4 -2 -1 -3 -3 -1 -4 -2 -4 -1 -6
Q -1  1  0 -1 -4  6  2 -2  1 -3 -3  1  0 -4 -2  0 -1 -3 -2 -3  0 -3  4 -1 -6
E -1 -1 -1  1 -5  2  6 -3  0 -4 -4  1 -2 -4 -2  0 -1 -4 -3 -3  1 -4  5 -1 -6
G  0 -3 -1 -2 -4 -2 -3  6 -3 -5 -4 -2 -4 -4 -3 -1 -2 -4 -4 -4 -1 -5 -3 -1 -6
H -2  0  0 -2 -4  1  0 -3  8 -4 -3 -1 -2 -2 -3 -1 -2 -3  2 -4 -1 -4  0 -1 -6
I -2 -3 -4 -4 -2 -3 -4 -5 -4  5  1 -3  1 -1 -4 -3 -1 -3 -2  3 -4  3 -4 -1 -6
L -2 -3 -4 -5 -2 -3 -4 -4 -3  1  4 -3  2  0 -3 -3 -2 -2 -2  1 -4  3 -3 -1 -6
K -1  2  0 -1 -4  1  1 -2 -1 -3 -3  5 -2 -4 -1 -1 -1 -4 -3 -3 -1 -3  1 -1 -6
M -1 -2 -3 -4 -2  0 -2 -4 -2  1  2 -2  6  0 -3 -2 -1 -2 -2  1 -3  2 -1 -1 -6
F -3 -4 -4 -4 -3 -4 -4 -4 -2 -1  0 -4  0  6 -4 -3 -2  0  3 -1 -4  0 -4 -1 -6
P -1 -2 -3 -2 -4 -2 -2 -3 -3 -4 -3 -1 -3 -4  8 -1 -2 -5 -4 -3 -2 -4 -2 -1 -6
S  1 -1  0 -1 -2  0  0 -1 -1 -3 -3 -1 -2 -3 -1  5  1 -4 -2 -2  0 -3  0 -1 -6
T  0 -1  0 -1 -1 -1 -1 -2 -2 -1 -2 -1 -1 -2 -2  1  5 -4 -2  0 -1 -1 -1 -1 -6
W -3 -4 -4 -6 -3 -3 -4 -4 -3 -3 -2 -4 -2  0 -5 -4 -4 11  2 -3 -5 -3 -3 -1 -6
Y -2 -3 -3 -4 -3 -2 -3 -4  2 -2 -2 -3 -2  3 -4 -2 -2  2  7 -2 -3 -2 -3 -1 -6
V  0 -3 -4 -4 -1 -3 -3 -4 -4  3  1 -3  1 -1 -3 -2  0 -3 -2  4 -4  2 -3 -1 -6
B -2 -1  5  5 -4  0  1 -1 -1 -4 -4 -1 -3 -4 -2  0 -1 -5 -3 -4  5 -4  0 -1 -6
J -2 -3 -4 -5 -2 -3 -4 -5 -4  3  3 -3  2  0 -4 -3 -1 -3 -2  2 -4  3 -3 -1 -6
Z -1  0  0  1 -4  4  5 -3  0 -4 -3  1 -1 -4 -2  0 -1 -3 -3 -3  0 -3  5 -1 -6
X -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -6
* -6 -6 -6 -6 -6 -6 -6 -6 -6 -6 -6 -6 -6 -6 -6 -6 -6 -6 -6 -6 -6 -6 -6 -6  1
```

### Find Ancestral Features

`{bm} /(Stories\/Evolutionary History\/Find Ancestral Features)_TOPIC/`

```{prereq}
Stories/Evolutionary History/Find Evolutionary Tree_TOPIC
Algorithms/Sequence Alignment/Multiple Alignment_TOPIC
Algorithms/Phylogeny/Sequence Inference_TOPIC
```

An unknown ancestor's features are probabilistically inferrable via the features of entities that descend from it.

```{svgbob}
   .-------------------------------------------------------------.
   |                          "Ancestor"                         |
   | "100% 4 legs"                                               |
   | "100% furry"                                                |
   | "100% sharp teeth"                                          |
   | "50% striped coat pattern"  vs   "50% spotted coat pattern" |
   | "50% >= 143 lbs"            vs   "50% <= 70 lbs"            |
   '------------------------------+------------------------------'
                                 / \
                .---------------'   '-----------------.
                |                                     |
.---------------+-------------.        .--------------+--------------.
|           "Leopard"         |        |            "Tiger"          |
| "100% 4 legs"               |        | "100% 4 legs"               |
| "100% furry"                |        | "100% furry"                |
| "100% sharp teeth"          |        | "100% sharp teeth"          |
| "100% spotted coat pattern" |        | "100% striped coat pattern" |
| "100% 50-70 lbs"            |        | "100% 143-660 lbs"          |
'-----------------------------'        '-----------------------------'
```

The example above infers phenotypic features for the common ancestor of leopard and tiger. If a feature is present and the same in both, it's safe to assume that it was present in their common ancestor as well (e.g. 4 legs). Otherwise, there's still some smaller chance that the feature was present, possibly with some variability in how it manifested (e.g. type of coat pattern).

With the advent of sequencing technology, the practice of using phenotypic features for phylogeny was superseded by sequencing data. When sequences are used, the features are the sequences themselves, meaning that the sequence of the common ancestor is what gets inferred.

```{svgbob}
   .-------------------------------------------------------------.
   |                          "Ancestor"                         |
   | "idx0: 100% A"                                              |
   | "idx1: 100% A"                                              |
   | "idx2: 50% C"  vs  "50% T"                                  |
   | "idx3: 50% C"  vs  "50% T"                                  |
   | "idx4: 100% T"                                              |
   '------------------------------+------------------------------'
                                 / \
                .---------------'   '-----------------.
                |                                     |
.---------------+-------------.        .--------------+--------------.
|           "Leopard"         |        |            "Tiger"          |
| "idx0: 100% A"              |        | "idx0: 100% A"              |
| "idx1: 100% A"              |        | "idx1: 100% A"              |
| "idx2: 100% C"              |        | "idx2: 100% T"              |
| "idx3: 100% C"              |        | "idx3: 100% T"              |
| "idx4: 100% T"              |        | "idx4: 100% T"              |
'-----------------------------'        '-----------------------------'

* "An example using a small region of DNA that codes"
  "for the same thing in both leopard and tiger"
```

The example below infers the spike protein sequences for the ancestors of SARS-CoV-2 variants. First, a phylogenetic tree is generated using BLOSUM80 as the distance metric. Then, the sequences are all aligned together using BLOSUM80 (multiple alignment, not pairwise alignment as was used for the distance metric). The sequences of ancestors are inferred using those aligned sequences.

```{note}
This is badly cobbled together code. It's taking the code from the previous section's example and embedding/duct-taping even more pieces from the sequence alignment module just to get a running example. In a perfect world I would just import the sequence alignment module, but that module lives in a separate container. This is the best I can do.

Running this is even slower than the previous section's example, so the sample size has been reduced even further.
```

```{ch7}
PracticalSARSCoV2PhylogenyTreeWithSequenceInference
1000_unique_sarscov2_spike_seqs.json.xz
3
0.1
-6
   A  R  N  D  C  Q  E  G  H  I  L  K  M  F  P  S  T  W  Y  V  B  J  Z  X
A  5 -2 -2 -2 -1 -1 -1  0 -2 -2 -2 -1 -1 -3 -1  1  0 -3 -2  0 -2 -2 -1 -1
R -2  6 -1 -2 -4  1 -1 -3  0 -3 -3  2 -2 -4 -2 -1 -1 -4 -3 -3 -1 -3  0 -1
N -2 -1  6  1 -3  0 -1 -1  0 -4 -4  0 -3 -4 -3  0  0 -4 -3 -4  5 -4  0 -1
D -2 -2  1  6 -4 -1  1 -2 -2 -4 -5 -1 -4 -4 -2 -1 -1 -6 -4 -4  5 -5  1 -1
C -1 -4 -3 -4  9 -4 -5 -4 -4 -2 -2 -4 -2 -3 -4 -2 -1 -3 -3 -1 -4 -2 -4 -1
Q -1  1  0 -1 -4  6  2 -2  1 -3 -3  1  0 -4 -2  0 -1 -3 -2 -3  0 -3  4 -1
E -1 -1 -1  1 -5  2  6 -3  0 -4 -4  1 -2 -4 -2  0 -1 -4 -3 -3  1 -4  5 -1
G  0 -3 -1 -2 -4 -2 -3  6 -3 -5 -4 -2 -4 -4 -3 -1 -2 -4 -4 -4 -1 -5 -3 -1
H -2  0  0 -2 -4  1  0 -3  8 -4 -3 -1 -2 -2 -3 -1 -2 -3  2 -4 -1 -4  0 -1
I -2 -3 -4 -4 -2 -3 -4 -5 -4  5  1 -3  1 -1 -4 -3 -1 -3 -2  3 -4  3 -4 -1
L -2 -3 -4 -5 -2 -3 -4 -4 -3  1  4 -3  2  0 -3 -3 -2 -2 -2  1 -4  3 -3 -1
K -1  2  0 -1 -4  1  1 -2 -1 -3 -3  5 -2 -4 -1 -1 -1 -4 -3 -3 -1 -3  1 -1
M -1 -2 -3 -4 -2  0 -2 -4 -2  1  2 -2  6  0 -3 -2 -1 -2 -2  1 -3  2 -1 -1
F -3 -4 -4 -4 -3 -4 -4 -4 -2 -1  0 -4  0  6 -4 -3 -2  0  3 -1 -4  0 -4 -1
P -1 -2 -3 -2 -4 -2 -2 -3 -3 -4 -3 -1 -3 -4  8 -1 -2 -5 -4 -3 -2 -4 -2 -1
S  1 -1  0 -1 -2  0  0 -1 -1 -3 -3 -1 -2 -3 -1  5  1 -4 -2 -2  0 -3  0 -1
T  0 -1  0 -1 -1 -1 -1 -2 -2 -1 -2 -1 -1 -2 -2  1  5 -4 -2  0 -1 -1 -1 -1
W -3 -4 -4 -6 -3 -3 -4 -4 -3 -3 -2 -4 -2  0 -5 -4 -4 11  2 -3 -5 -3 -3 -1
Y -2 -3 -3 -4 -3 -2 -3 -4  2 -2 -2 -3 -2  3 -4 -2 -2  2  7 -2 -3 -2 -3 -1
V  0 -3 -4 -4 -1 -3 -3 -4 -4  3  1 -3  1 -1 -3 -2  0 -3 -2  4 -4  2 -3 -1
B -2 -1  5  5 -4  0  1 -1 -1 -4 -4 -1 -3 -4 -2  0 -1 -5 -3 -4  5 -4  0 -1
J -2 -3 -4 -5 -2 -3 -4 -5 -4  3  3 -3  2  0 -4 -3 -1 -3 -2  2 -4  3 -3 -1
Z -1  0  0  1 -4  4  5 -3  0 -4 -3  1 -1 -4 -2  0 -1 -3 -3 -3  0 -3  5 -1
X -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1
```

## Gene Expression Analysis

`{bm} /(Stories\/Gene Expression Analysis)_TOPIC/`

Gene expression is the biological process by which a gene (segment of DNA) is synthesized into a gene product (e.g. protein).

```{svgbob}
       .----------------> mRNA --------------> "protein"
       | "transcribe"           "translate"    "(gene product)"
DNA   -+
(gene) |
       '----------------> "functional RNA"
         "transcribe"     "(gene product)"
```

As an organism changes state, its gene expression levels change as well. For example, when a bacteria's flagella initially starts moving, a gene may have either an ...

 * increased rate of gene expression.
 * decreased rate of gene expression.
 * unchanged rate of gene expression.
 
The subset of genes whose gene expression either increase or decrease are somehow linked to initial flagella movement. It could be that a linked gene is either responsible for a byproduct of the flagella movement.

```{svgbob}
'-.-'-.-'-.-'-.-'-. .-----------------------.
                  '-+                       |
'-.-'-.-'-.-'-.-'---+                       |
                  .-+                       |
'-.-'-.-'-.-'-.-'-' '-----------------------'

"Flagella is a protruding strand / tail"
```

The same idea extends to diseases and treatments. For example, a cancerous human blood cell may have a subset of genes where gene expression is vastly different from its non-cancerous counterpart. Identifying the genes linked to human blood cancer could lead to ...

 * screening (e.g. is gene expression for those genes at their cancerous levels?)
 * measuring treatment effectiveness (e.g. is the drug reducing gene expression to its non-cancerous levels?)
 * identifying preventative measures (e.g. mutation to a diseased allele more likely to occur if exposed to some chemical)

The common way to measure gene expression is to inspect the RNA within a cell. A snapshot of all RNA transcripts within a cell at a given point in time, called a transcriptome, can be captured using RNA sequencing technology. Both the RNA sequences and the counts of those transcripts (number of instances) are captured. Given that an RNA transcript is simply a transcribed "copy" of the DNA it came from (it identifies the gene), a snapshot indirectly shows the amount of gene expression taking place for each gene at the time that snapshot was taken.

Differential gene expression analysis is the process of capturing and comparing multiple RNA snapshots for an organism in different states. The comparisons help identify which genes are influenced by / responsible for the relevant state changes.

There are two broad categories of differential gene expression analysis: time-course and conditional. For some population, ...

 * time-course captures RNA snapshots at different points (e.g. apply drug to culture of cancerous blood cells, then measure gene expression levels once per hour).

   |          | hour 0 | hour 1 | hour 2 | ... |
   |----------|--------|--------|--------|-----|
   | Gene A   | 100    | 100    | 100    | ... |
   | Gene B   | 100    |  70    | 50     | ... |
   | Gene C   | 100    | 110    | 140    | ... |
   | ...      | ...    | ...    | ...    | ... |

 * conditional captures RNA snapshots across different conditions (e.g. compare gene expression levels across 50 blood cancer patients vs 50 cancer-free patients).

   |          | patient1 (cancer) | patient2 (cancer) | patient3 (non-cancer) | ... |
   |----------|-------------------|-------------------|-----------------------|-----|
   | Gene X   | 100               | 100               | 100                   | ... |
   | Gene Y   | 100               | 110               | 50                    | ... |
   | Gene Z   | 100               | 110               | 140                   | ... |
   | ...      | ...               | ...               | ...                   | ... |

```{note}
The sub-section describes how to deal with time-courses. There is no sub-section describing how to deal with conditionals. The Pevzner book never went over it. But, the final challenge question did throw a conditional dataset at you and asked you to solve some problem. It seems that for conditional datasets, the key thing you need to do is filter out unrelated genes before doing anything. For the challenge in the Pevzner book, I simply compared a gene's average gene expression between cancer vs non-cancer to determine if it was relevant (if the offset was large enough, I decided it was relevant).
```

### Cluster Genes

`{bm} /(Stories\/Gene Expression Analysis\/Cluster Genes)_TOPIC/`

```{prereq}
Stories/Transcription Factors_TOPIC
Algorithms/Gene Clustering/Soft Hierarchical Clustering_TOPIC
```

A time-course experiment captures RNA snapshots at different points in time. For example, a biologist infects a cell culture with a pathogen, then measures gene expression levels within that culture every hour.

|          | hour 0 | hour 1 | hour 2 | hour 3 | hour 4 |
|----------|--------|--------|--------|--------|--------|
| Gene X   | 100    | 100    | 50     | 50     | 20     |
| Gene Y   | 20     | 50     | 50     | 100    | 100    |
| Gene Z   | 50     | 50     | 50     | 50     | 50     |
| ...      | ...    | ...    | ...    | ...    | ...    |

```{svgbob}
         "GENE X"                              "GENE Y"                             "GENE Z"      
|                                    |                                    |                       
|  *----*                            |                 *                  |                       
|        \                           |                /                   |                        
|         \                          |               /                    |                       
|          *---*                     |          *---*                     |  *---*---*---*---*        
|               \                    |         /                          |                       
|                \                   |        /                           |                       
|                 *                  |  *----*                            |                       
|                                    |                                    |                       
+-----------------------             +-----------------------             +-----------------------
```

If two genes have similar gene expression vectors, it could be that they're related in some way (e.g. regulated by the same transcription factor). Clustering a set of genes by their gene expression vectors helps identify these relationships. If done properly, genes within the same cluster should have gene expression vectors that are more similar to each other than to those in other clusters (good clustering principle).

Gene clusters can then be passed off to a biologist for further investigation (e.g. to confirm if they're actually influenced by the same transcription factor).

```{svgbob}
     "GENES W and X"                  "GENES U and T"    
|                                |                       
|  *----*                        |  *             
|  *----*\                       |  *\            
|        \\                      |   \\           
|         \*---*                 |    \*        
|          *---*\                |     *\       
|               \\               |      \\      
|                \*              |       \*---*----*
|                 *              |        *---*----*  
+-----------------------         +-----------------------
```

The example below clusters a time-course for astrocyte cells infected with H5N1 bird flu. The time-course measures gene expression at 6, 12, and 24 hours into infection. The clustering process builds a phylogenetic tree, where a simple heuristic determines parts of the tree that represent clusters (e.g. regions of interest).

```{note}
This dataset is from the NCBI gene expression omnibus (GEO): [Influenza virus H5N1 infection of U251 astrocyte cell line: time course](https://www.ncbi.nlm.nih.gov/sites/GDSbrowser?acc=GDS6010). You may be able to use other datasets from the GEO with this same code -- use the [GDS browser](https://www.ncbi.nlm.nih.gov/sites/GDSbrowser) if you want to find more.

> GDS6010
>
> Title: Influenza virus H5N1 infection of U251 astrocyte cell line: time course
>
> Summary: Analysis of U251 astrocyte cells infected with the influenza H5N1 virus for up to 24 hours. Results provide insight into the immune response of astrocytes to H5N1 infection.
>
> Organism: Homo sapiens
>
> Platform: GPL6480: Agilent-014850 Whole Human Genome Microarray 4x44K G4112F (Probe Name version)
>
> Citation: Lin X, Wang R, Zhang J, Sun X et al. Insights into Human Astrocyte Response to H5N1 Infection by Microarray Analysis. Viruses 2015 May 22;7(5):2618-40. PMID: 26008703
>
> Reference Series: GSE66597
>
> Sample count: 18
>
> Value type: transformed count
>
> Series published: 2016/01/04

There are too many genes here for the clustering algorithm (Python is slow). As such, standard deviation is used to filter out gene expression vectors that don't dramatically change during the time-course. The experiment did come with a control group: a second population of the same cell line but uninfected. Maybe instead of standard deviation, a better filtering approach would be to only include genes whose gene expression pattern is vastly different between control group vs experimental group.

The original data set was too large. I removed the replicates and only kept hour 24 of the control group.
```

```{ch8}
PracticalGEODatasetClustering
{
  filename: GDS6010.soft_no_replicates_single_control.xz,
  gene_column: ID_REF,  # col name for gene ID
  sample_columns: [
    GSM1626001,  # col name for control @ 24 hrs (treat this as a measure of "before infection")
    GSM1626004,  # col name for infection @ 6 hrs
    GSM1626007,  # col name for infection @ 12 hrs
    GSM1626010   # col name for infection @ 24 hrs
  ],
  std_dev_limit: 1.6,  # reject anything with std dev less than this
  metric: euclidean,  # OPTIONS: euclidean, manhattan, cosine, pearson
  dist_capture: 0.5,
  edge_scale: 3.0
}
```

# Ideas

 * CPU optimized C++ global alignment - Simple global alignment is C++ with all optimizations turned on AND multi-threading or fibers that optimize work size to fit in cache lines.

 * GPU optimized C++ global alignment - Simple global alignment in Nvidia's HPC SDK C++ where GPU "thread" is optimized to fit in caches. Maybe do the divide-and-conquer variant as well. (divide and conquer might be a good idea because it'll work on super fat sequences)

 * GPU optimized C++ probabilistic multiple alignment - Probabilistic multiple alignment in Nvidia's HPC SDK C++ where GPU "thread" is optimized to fit in caches.

 * Deep-learning Regulatory Motif Detection - Try training a deep learning model to "find" regulatory motifs for new transcription factors based on past training data.

 * Global alignment that takes genome rearrangements into account - multiple chromosomes, chromosomes becoming circular or linear, reversals, fissions, fusions, copies, etc..

 * Organism lookup by k-mer - Two-tiered database containing k-mers. The first tier is an "inverse index" of k-mers that rarely appear across all organisms (unique or almost unique to the genome) exposed as either a trie / hashtable (for exact lookups) or possibly as a list where highly optimized miniature alignments get performed (for fuzzy lookups -- SIMD + things fit nicely into cache lines). It widdles down the list of organism for the second tier, which is a full on database search for each matches across all k-mers.

 * K-mer hierarchical clustering - Hierarchical cluster together similar k-mers using either pearson similarity/pearson distance [between one/zero vector of sub-k-mers] or sequence alignment distance to form its distance matrix / similarity matrix. This is useful for when you're trying to identify which organism a sequence belongs to by searching for its k-mers in a database. The k-mers that make up the database would be clustered, and k-mers that closely cluster together under a branch of the hierarchical cluster tree are those you'd be more cautious with -- the k-mer may have matched but it could have actually been a corrupted form of one of the other k-mers in the cluster (sequencing error).

   This logic also applies to spell checking. Words that cluster together closely are more likely to be mis-identified by a standard spellchecker, meaning individual clusters should have their own spell checking strategies? If you're going to do this with words, use a factor in QWERTY keyboard key distances into the similarity / distance matrix.

 * Hierarchical clustering explorer - Generate a neighbour joining phylogeny tree based on pearson distance of sequence alignment distance, then visualize the tree and provide the user with "interesting" internal nodes (clusters). In this case, "interesting" would be any internal node where the distance to most leaf nodes is within some threshold / average / variance / etc... Also, maybe provide an "idealized" view of the clustered data for each internal node (e.g. average the vectors for the leaves to produce the vector for the internal node).

   Another idea is to take the generated tree and convert it back into distance matrix. If the data isn't junk, the distance metric isn't junk, and the data is clusterable on that distance metric, the generated distance matrix should match closely to the input distance metric. The tool can warn the user if it doesn't.

 * Soft hierarchical clustering - Build out a neighbour joining phylogeny tree. Each internal node is a cluster. The distance between that internal node to all leaf nodes can be used to define the probability that the leaf node belongs to that cluster? This makes sense because neighbour joining phylogeny produces unrooted trees (simple trees). If it were a rooted tree, you could say that internal node X leaf nodes A, B, and C -- meaning that A, B and C are member_CLUSTERs of cluster X. But, because it's unrooted, technically any leaf node in the graph could be a member_CLUSTER of cluster X.
   
   This relates to the idea above (hierarchical clustering explorer) -- You can identify "interesting clusters" using this (e.g. a small group tightly clustered together) and return it to the user for inspection.

 * Hierarchical clustering as a means of detecting outliers - Cluster data using neighbouring join phylogeny. How far is each leaf node to its parent internal node? Find any that are grossly over the average / squared error distortion / some other metric? Report it. Try other ways as well (e.g. pick a root and see how far it is from the root -- root picked using some metric like avg distance between leaf nodes / 2 or squared error distortion).

   This relates to the idea above (soft hierarchical clustering) -- You may be able to identify outliers using soft hierarchical clustering using this (e.g. the probability of being a part of some internal node is way farther than any of the other leaf nodes).

# Terminology

 * `{bm} k-mer/(\d+-mer|k-mer|kmer)/i` - A substring of length k within some larger biological sequence (e.g. DNA or amino acid chain). For example, in the DNA sequence GAAATC, the following k-mer's exist:

   | k | k-mers          |
   |---|-----------------|
   | 1 | G A A A T C     |
   | 2 | GA AA AA AT TC  |
   | 3 | GAA AAA AAT ATC |
   | 4 | GAAA AAAT AATC  |
   | 5 | GAAAT AAATC     |
   | 6 | GAAATC          |

 * `{bm} kd-mer/(\(\d+,\s*\d+\)-mer|kd-mer|kdmer|\(k,\s*d\)-mer)/i` - A substring of length 2k + d within some larger biological sequence (e.g. DNA or amino acid chain) where the first k elements and the last k elements are known but the d elements in between isn't known.
 
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

 * `{bm} leading half-strand` / `{bm} lagging half-strand` - Given the 2 strands that make up a DNA molecule, the strand that goes in the...

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

 * `{bm} double stranded DNA/(double stranded DNA|double-stranded DNA)/i` - Two strands of DNA bound together, where each strand is the reverse complement of the other.

   ```{svgbob}
   3' . . . T <- T <- T <- G <- C <- T <- T <- T <- T <- G <- . . . 5'
            |    |    |    |    |    |    |    |    |    | 
   5' . . . A -> A -> A -> C -> G -> A -> A -> A -> A -> C -> . . . 3'    
   ```

 * `{bm} reverse complement/(reverse complement)/i` - Given double-stranded DNA, each ...

    * strand's direction is opposite of the other,
    * strand position has a nucleotide that complements the nucleotide at that same position on the other stand (A ⟷ T and C ⟷ G)

   ```{svgbob}
   3' . . . T <- T <- T <- G <- C <- T <- T <- T <- T <- G <- . . . 5'
            |    |    |    |    |    |    |    |    |    | 
   5' . . . A -> A -> A -> C -> G -> A -> A -> A -> A -> C -> . . . 3'    
   ```

   The reverse complement means that a stretch of single-stranded DNA has its direction reversed (5' and 3' switched) and nucleotides complemented.

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

   * a protein, the gene is transcribed to mRNA which in turn is translated to a protein.
   * functional RNA, the gene is transcribed to a type of RNA that isn't mRNA (only mRNA is translated to a protein).

   ```{svgbob}
          .----------------> mRNA --------------> "protein"
          | "transcribe"           "translate"    "(gene product)"
   DNA   -+
   (gene) |
          '----------------> "functional RNA"
            "transcribe"     "(gene product)"
   ```

 * `{bm} regulatory gene` / `{bm} regulatory protein` - The proteins encoded by these genes affect gene expression for certain other genes. That is, a regulatory protein can cause certain other genes to be expressed more (promote gene expression) or less (repress gene expression).

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

 * `{bm} motif member` `{bm} /\b(membership|member)_MOTIF/i` - A specific nucleotide sequence that matches a motif. For example, given a motif represented by the regex `[AT]TT[GC]C`, the sequences ATTGC, ATTCC, TTTGC, and TTTCC would be its member_MOTIFs.

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

 * `{bm} complementary DNA (cDNA)/(complementary DNA)/i` `{bm} /(cDNA)/` - A single strand of DNA generated from mRNA. The enzyme reverse transcriptase scans over the mRNA and creates the complementing single DNA strand.

   ```{svgbob}
   3' . . . U <- U <- U <- G <- C <- U <- U <- U <- U <- G <- . . . 5'   mRNA  
            |    |    |    |    |    |    |    |    |    | 
   5' . . . A -> A -> A -> C -> G -> G -> A -> A -> A -> C -> . . . 3'   cDNA  
   ```

   The mRNA portion breaks off, leaving the single-stranded DNA.

   ```{svgbob}
   5' . . . A -> A -> A -> C -> G -> G -> A -> A -> A -> C -> . . . 3'   cDNA  
   ```

 * `{bm} DNA microarray` - A device used to compare gene expression. This works by measuring 2 mRNA samples against each other: a control sample and an experimental sample. The samples could be from...
 
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
  
 * `{bm} Cromwell's rule` - When a probability is based on past events, 0.0 and 1.0 shouldn't be used. That is, if you've...
 
   * never seen an even occur in the past, it doesn't mean that there's a 0.0 probability of it occurring next.
   * always seen an event occur in the past, it doesn't mean that there's a 1.0 probability of it occurring next.
 
   Unless you're dealing with hard logical statements where prior occurrences don't come in to play (e.g. 1+1=2), you should include a small chance that some extremely unlikely event may happen. The example tossed around is "the probability that the sun will not rise tomorrow." Prior recorded observations show that the sun has always risen, but that doesn't mean that there's a 1.0 probability of the sun rising tomorrow (e.g. some extremely unlikely cataclysmic event may prevent the sun from rising).

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

   The generated k-mer may also use a hybrid alphabet. The consensus string for the same matrix above using IUPAC nucleotide codes: `WTTSS`.
  
 * `{bm} entropy` - The uncertainty associated with a random variable. Given some set of outcomes for a variable, it's calculated as `{kt} -\sum_{i=1}^{n} P(x_i) log P(x_i)`.

   This definition is for information theory. In other contexts (e.g. physics, economics), this term has a different meaning.

 * `{bm} genome` - In the context of a ...
 
    * specific organism, genome refers to all of the DNA for that organism (e.g. a specific E. coli cell).
    * specific species, genome refers to the idealized DNA for that species (e.g. all E. coli).

   DNA of individual cells mutate all the time. For example, even in multi-cell organism, two cells from the same mouse may not have the exact same DNA. 

 * `{bm} sequence` - The ordered elements that make up some biological entity. For example, a ...

   * DNA sequence contains the set of nucleotides and their positions for that DNA strand.
   * peptide sequence contains the set of amino acids and their positions for that peptide.

 * `{bm} sequencing/(sequencing|sequenced)/i` - The process of determining which nucleotides are assigned to which positions in a strand of DNA or RNA.

   The machinery used for DNA sequencing is called a sequencer. A sequencer takes multiple copies of the same DNA, breaks that DNA up into smaller fragment_NORMs, and scans in those fragment_SEQs. Each fragment_SEQ is typically the same length but has a unique starting offset. Because the starting offsets are all different, the original larger DNA sequence can be guessed at by finding fragment_SEQ with overlapping regions and stitching them together.

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

   ```{note}
   This term may also be used in reference to homopolymer errors, known to happen with nanopore technology. From [here](https://news.ycombinator.com/item?id=25459670)...

   > A homopolymer is when you have stretches of the same nucleotide, and the error is miscounting the number of them. e.g: GAAAC could be called as "GAAC" or "GAAAAC" or even "GAAAAAAAC".
   ```

 * `{bm} read/\b(read)_SEQ/i` - A segment of genome scanned in during the process of sequencing.

 * `{bm} read-pair/(read-pair|read pair)/i` - A segment of genome scanning in during the process of sequencing, where the middle of the segment is unknown. That is, the first k elements and the last k elements are known, but the d elements in between aren't known. The total size of the segment is 2k + d.

   Sequencers provide read-pairs as an alternative to longer read_SEQs because the longer a read_SEQ is the more errors it contains.

   See kd-mer.

 * `{bm} fragment/(fragment)_SEQ/i` - A scanned sequence returned by a sequencer. Represented as either a read_SEQ or a read-pair.

 * `{bm} assembly/(assembly|assemble)/i` - The process of stitching together overlapping fragment_SEQs to guess the sequence of the original larger DNA sequence that those fragment_SEQs came from.

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
  
   Oftentimes, transposons cause disease. For example, ...

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

 * `{bm} Eulerian graph` `{bm} /(Eulerian)_GRAPH/i` - For a graph to be Eulerian_GRAPH, it must have an Eulerian cycle: a path in a graph that is a cycle and visits every edge exactly once. For a graph to have an Eulerian cycle, it must be both balanced_GRAPH and strongly connected.
 
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
   What purpose does this actually serve? Mimicking 1 long read_SEQ as n shorter read_SEQs isn't equivalent to actually having sequenced those n shorter read_SEQs. For example, what if the longer read_SEQ being broken up has an error? That error replicates when breaking into n shorter read_SEQs, which gives a false sense of having good coverage_SEQ and makes it seem as if it wasn't an error.
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
   What purpose does this actually serve? Mimicking 1 long read-pair as n shorter read-pairs isn't equivalent to actually having sequenced those n shorter read-pairs. For example, what if the longer read-pair being broken up has an error? That error replicates when breaking into n shorter read-pairs, which gives a false sense of having good coverage_SEQ and makes it seem as if it wasn't an error.
   ```

 * `{bm} contig/(contig)s?\b/i/true/true` - An unambiguous stretch of DNA derived by searching an overlap graph / de Bruijn graph for paths that are the longest possible stretches of non-branching nodes (indegree and outdegree of 1). Each stretch will be a path that's either  ...
  
    * a line: each node has an indegree and outdegree of 1.
   
      ```{svgbob}
      GT --> TG --> GG
      ```
   
    * a cycle: each node has an indegree and outdegree of 1 and it loops.
   
      ```{svgbob}
      CA ---> AC ---> CC 
      ^                |
      |                |
      `----------------'
      ```
   
    * a line sandwiched between branching nodes: nodes in between have an indegree and outdegree of 1 but either...
      * starts at a node where indegree != 1 but outdegree == 1 (incoming branch),
      * or ends at a node where indegree == 1 but outdegree != 1 (outgoing branch),
      * or both.
   
      ```{svgbob}
      -.                 
       |              .->
       v              |
       GT --> TG --> GG
       ^              |
       |              `->
      -'
      ```
   
   Real-world complications with DNA sequencing make de Bruijn / overlap graphs too tangled to guess a full genome: both strands of double-stranded DNA are sequenced and mixed into the graph, sequencing errors make into the graph, repeats regions of the genome can't be reliably handled by the graph, poor coverage_SEQ, etc.. As such, biologists / bioinformaticians have no choice but to settle on contigs.
   
   ```{svgbob}
       "Original"                "1: GTGG"             "2: GGT"          "3: GGT"             "4: CACCA"
   
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

 * `{bm} ribonucleotide` - Elements that make up RNA, similar to how nucleotides are the elements that make up DNA.

   * A = Adenine (same as nucleotide)
   * C = Cytosine (same as nucleotide)
   * G = Guanine (same as nucleotide)
   * U = Uracil (replace nucleotide Thymine)
  
 * `{bm} antibiotic` - A substance (typically an enzyme) for killing, preventing, or inhibiting the grow of bacterial infections.

 * `{bm} amino acid` - The building blocks of peptides / proteins, similar to how nucleotides are the building blocks of DNA.

    See proteinogenic amino acid for the list of 20 amino acids used during the translation.

 * `{bm} proteinogenic amino acid` - Amino acids that are used during translation. These are the 20 amino acids that the ribosome translates from codons. In contrast, there are many other non-proteinogenic amino acids that are used for non-ribosomal peptides.
 
    The term "proteinogenic" means "protein creating". 

    | 1 Letter Code | 3 Letter Code | Amino Acid                  | Mass (daltons) |
    |---------------|---------------|-----------------------------|----------------|
    | A             | Ala           | Alanine                     | 71.04          |
    | C             | Cys           | Cysteine                    | 103.01         |
    | D             | Asp           | Aspartic acid               | 115.03         |
    | E             | Glu           | Glutamic acid               | 129.04         |
    | F             | Phe           | Phenylalanine               | 147.07         |
    | G             | Gly           | Glycine                     | 57.02          |
    | H             | His           | Histidine                   | 137.06         |
    | I             | Ile           | Isoleucine                  | 113.08         |
    | K             | Lys           | Lysine                      | 128.09         |
    | L             | Leu           | Leucine                     | 113.08         |
    | M             | Met           | Methionine                  | 131.04         |
    | N             | Asn           | Asparagine                  | 114.04         |
    | P             | Pro           | Proline                     | 97.05          |
    | Q             | Gln           | Glutamine                   | 128.06         |
    | R             | Arg           | Arginine                    | 156.1          |
    | S             | Ser           | Serine                      | 87.03          |
    | T             | Thr           | Threonine                   | 101.05         |
    | V             | Val           | Valine                      | 99.07          |
    | W             | Trp           | Tryptophan                  | 186.08         |
    | Y             | Tyr           | Tyrosine                    | 163.06         |
 
    ```{note}
    The masses are monoisotopic masses.
    ```

 * `{bm} peptide` - A short amino acid chain of at least size two. Peptides are considered miniature proteins, but when something should be called a peptide vs a protein is loosely defined: the cut-off is anywhere between 50 to 100 amino acids.
 
 * `{bm} polypeptide` - A peptide of at least size 10.

 * `{bm} amino acid residue` - The part of an amino acid that makes it unique from all others.
 
   When two or more amino acids combine to make a peptide/protein, specific elements are removed from each amino acid. What remains of each amino acid is the amino acid residue.

 * `{bm} cyclopeptide/(cyclopeptide|cyclic peptide)/i` - A peptide that doesn't have a start / end. It loops.

   ```{svgbob}
   N ----> Q 
   ^       |
   |       |
   `-- Y <-'
   ```

 * `{bm} linear peptide` - A peptide that has a start and an end. It doesn't loop.

   ```{svgbob}
   N --> Q --> Y 
   ```

 * `{bm} subpeptide` - A peptide derived taking some contiguous piece of a larger peptide.
 
   A subpeptide can have a length == 1 where a peptide must have a length > 1. As such, in the case where the subpeptide has a length ...
    * == 1, it isn't considered a peptide.
    * \> 1, it is considered a peptide.

 * `{bm} central dogma of molecular biology` - The overall concept of transcription and translation: Instructions for making a protein are copied from DNA to RNA, then RNA feeds into the ribosome to make that protein (DNA → RNA → Protein).

   Most, not all, peptides are synthesized as described above. Non-ribosomal peptides are synthesized outside of the transcription and translation.

 * `{bm} non-ribosomal peptide` `{bm} /\b(NRP)s?\b//true/true` - A peptide that was synthesized by a protein called NRP synthetase rather than synthesized by a ribosome. NRP synthetase builds peptides one amino acid at a time without relying on transcription or translation.

   Non-ribosomal peptides may be cyclic. Common use-cases for non-ribosomal peptides:

   * antibiotics
   * anti-tumor agents
   * immunosuppressors
   * communication between bacteria (quorum sensing)

 * `{bm} non-ribosomal peptide synthetase/(non-ribosomal peptide synthetase|NRP synthetase)/i` - A protein responsible for the production of a non-ribosomal peptide.

 * `{bm} adenylation domain/(adenylation domain|A domain|A-domain)/i` - A segment of an NRP synthetase protein responsible for the outputting a single amino acid. For example, the NRP synthetase responsible for producing Tyrocidine has 10 adenylation domains, each of which is responsible for outputting a single amino acid of Tyrocidine.

 * `{bm} mass spectrometer/(mass spectrometer|mass spectrometry)/i` - A device that randomly shatters molecules into pieces and measures the mass-to-charge of those pieces. The output of the device is a plot called a spectrum_MS.

   Note that mass spectrometers have various real-world practical problems. Specifically, they ...

    * may not capture all possible pieces from the intended molecules (missing mass-to-charge ratios).
    * may capture pieces from unintended molecules (faulty mass-to-charge ratios).
    * will likely introduce noise into the pieces they capture.

 * `{bm} spectrum/(spectrum)_MS/i` - The output of a mass spectrometer. The...

    * x-axis is the mass-to-charge ratio.
    * y-axis is the intensity of that mass-to-charge ratio (how much more / less did that mass-to-charge appear compared to the others).
   
   ```{svgbob}
       y
       ^
       |
       |        |
       |        |
   "%" |        |
       |        | |           |
       |        | |           |
       | |      | | |         |        |
       | | | |  | | |     |   |    | | |
       +-+-+-+--+-+-+-----+---+----+-+-+--> x
                        "m/z"
   ```

   Note that mass spectrometers have various real-world practical problems. Specifically, they ...

    * may not capture all possible pieces from the intended molecules (missing mass-to-charge ratios).
    * may capture pieces from unintended molecules (faulty mass-to-charge ratios).
    * will likely introduce noise into the pieces they capture.

   As such, these plots aren't exact.

 * `{bm} experimental spectrum` - List of potential fragment_NORM masses derived from a spectrum_MS. That is, the molecules fed into the mass spectrometer were randomly fragment_NORMed and each fragment_NORM had its mass-to-charge ratio measured. From there, each mass-to-charge ratio was converted to a set of potential masses.
 
   The masses in an experimental spectrum ...

    * may not capture all possible fragment_NORMs for the intended molecule (missing masses).
    * may capture fragment_NORMs from unintended molecules (faulty masses).
    * will likely contain noise.

    In the context of peptides, the mass spectrometer is expected to fragment_NORM based on the bonds holding the individual amino acids together. For example, given the linear peptide NQY, the experimental spectrum may include the masses for [N, Q, ?, ?, QY, ?, NQY] (? indicate faulty masses, Y and NQ missing).

 * `{bm} theoretical spectrum` - List of all of possible fragment_NORM masses for a molecule in addition to 0 and the mass of the entire molecule. This is what the experimental spectrum would be in a perfect world: no missing masses, no faulty masses, no noise, only a single possible mass for each mass-to-charge ratio.

   In the context of peptides, the mass spectrometer is expected to fragment_NORM based on the bonds holding the individual amino acids together. For example, given the linear peptide NQY, the theoretical spectrum will include the masses for [0, N, Q, Y, NQ, QY, NQY]. It shouldn't include masses for partial amino acids. For example, it shouldn't include NQY breaking into 2 pieces by splitting Q, such that one half has N and part of Q, and the other has the remaining part of Q with Y.

 * `{bm} spectrum convolution` - An operation used to derive amino acid masses that probably come from the peptide used to generate that experimental spectrum. That is, it generates a list of amino acid masses that could have been for the peptide that generated the experimental spectrum.
 
   The operation derives amino acid masses by subtracting experimental spectrum masses from each other. For example, the following experimental spectrum is for the linear peptide NQY: [113.9, 115.1, 136.2, 162.9, 242.0, 311.1, 346.0, 405.2]. Performing 242.0 - 113.9 results in 128.1, which is very close to the mass for amino acid Y.
   
   Note how the mass for Y was derived from the masses in experimental spectrum even though it's missing from the experimental spectrum itself:
   
   * Mass of N is 114. 2 masses are close to 114 in the experimental spectrum: \[113.9, 115.1\].
   * Mass of Q is 163. 1 mass is close to 163 in the experimental spectrum: \[162.9\].
   * Mass of Y is 128. 0 masses are close to 128 in the experimental spectrum: \[\].

 * `{bm} dalton` `{bm} /\b\d+(?:\.\d+)?(Da)\b/i/true/false` - A unit of measurement used in physics and chemistry. 1 Dalton is approximately the mass of a single proton / neutron, derived by taking the mass of a carbon-12 atom and dividing it by 12.

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
 
   For example, given the string ATGTTCCATTAA, the following codon division are possible:

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

 * `{bm} subsequence` - A sequence derived by traversing some other sequence in order and choosing which elements to keep vs delete. For example, can is a subsequence of cation.

   ```{svgbob}
   C -----------> C 
   A -----------> A
   T ----o
   I ----o
   O ----o
   N -----------> N
   ```

   Not to be confused with substring. A substring may also be a subsequence, but a subsequence won't necessarily be a substring.

 * `{bm} substring` - A sequence derived by taking a contiguous part of some other sequence (order of elements maintained). For example, cat is a substring of cation.

   ```{svgbob}
   C -----------> C 
   A -----------> A
   T -----------> T
   I 
   O 
   N 
   ```

   Not to be confused with subsequence. A substring may also be a subsequence, but a subsequence won't necessarily be a substring.

 * `{bm} topological order` - A 1-dimensional ordering of nodes in a directed acyclic graph in which each node is ahead of all of its predecessors / parents. In other words, the node is ahead of all other nodes that connect to it.

   For example, the graph ...

   ```{svgbob}
                  ,----> E 
                  |
                  |
   A --->  B ---> C ---> D 
           |             ^ 
           |             | 
           `-------------' 
   ```

   ... the topological order is either [A, B, C, D, E] or [A, B, C, E, D]. Both are correct.

 * `{bm} longest common subsequence`  `{bm} /\b(LCS)es?\b//true/true` - A common subsequence between a set of strings of which is the longest out of all possible common subsequences. There may be more than one per set.
 
   For example, AACCTTGG and ACACTGTGA share a longest common subsequence of...
  
    * ACCTGG...

      ```{svgbob}
      A A C C T T G G
      │ │ | | | | | |
      | o | | | o | |
      | .-' | |   | |
      | | .-' |   | |
      | | | .-'   | |
      | | | | .---' |
      | | | | | .---'
      | | | | | |
      v v v v v v
      A C C T G G
      ^ ^ ^ ^ ^ ^
      | | | | | |
      | | | | | `---.
      | | | | `-.   |
      | | | `-. |   |
      | | `-. | |   |
      | | o | | | o | o
      | | | | | | | | |
      A C A C T G T G A
      ```

    * AACTGG...

      ```{svgbob}
      A A C C T T G G
      │ │ | | | | | |
      | | o | | o | |
      | | .-' |   | |
      | | | .-'   | |
      | | | | .---' |
      | | | | | .---'
      | | | | | |
      v v v v v v
      A A C T G G
      ^ ^ ^ ^ ^ ^
      | | | | | |
      | | | | | `---.
      | | | | `-.   |
      | | | `-. |   |
      | | `-. | |   |
      | `-. | | |   | 
      | o | | | | o | o
      | | | | | | | | |
      A C A C T G T G A
      ```

    * etc..

 * `{bm} sequence alignment` - Given a set of sequences, a sequence alignment is a set of operations applied to each position in an effort to line up the sequences. These operations include:
 
   * insert/delete (indel for short).
   * replace (also referred to as mismatch).
   * keep matching (also referred to as match).
 
   For example, the sequences MAPLE and TABLE may be aligned by performing...

   | String 1 | String 2 | Operation     |
   |----------|----------|---------------|
   |    M     |          | Insert/delete |
   |          |     T    | Insert/delete |
   |    A     |     A    | Keep matching |
   |    P     |     B    | Replace       |
   |    L     |     L    | Keep matching |
   |    E     |     E    | Keep matching |

   Or, MAPLE and TABLE may be aligned by performing...

   | String 1 | String 2 | Operation     |
   |----------|----------|---------------|
   |    M     |     T    | Replace       |
   |    A     |     A    | Keep matching |
   |    P     |     B    | Replace       |
   |    L     |     L    | Keep matching |
   |    E     |     E    | Keep matching |

   The names of these operations make more sense if you were to think of alignment instead as __transformation__. The first example above in the context of __transforming__ MAPLE to TABLE may be thought of as:

   | From | To | Operation       | Result |
   |------|----|-----------------|--------|
   |   M  |    | Delete M        |        |
   |      | T  | Insert T        | T      |
   |   A  | A  | Keep matching A | TA     |
   |   P  | B  | Replace P to B  | TAB    |
   |   L  | L  | Keep matching L | TABL   |
   |   E  | E  | Keep matching E | TABLE  |

   The shorthand form of representing sequence alignments is to stack each sequence. The example above may be written as...

   |          | 0 | 1 | 2 | 3 | 4 | 5 |
   |----------|---|---|---|---|---|---|
   | String 1 | M |   | A | P | L | E |
   | String 2 |   | T | A | B | L | E |

   All possible sequence alignments are represented using an alignment graph. A path through the alignment graph (called alignment path) represents one possible way to align the set of sequences. 

 * `{bm} alignment graph/(alignment graph|sequence alignment graph)/i` - A directed graph representing all possible sequence alignments for some set of sequences. For example, the graph showing all the different ways that MAPLE and TABLE may be aligned ...

   ```{svgbob}
      T    A    B    L    E   
    o---▶o---▶o---▶o---▶o---▶o
    |\   |\   |\   |\   |\   |   "* each diagonal edge is a replacement / keep matching"
   M| \  | \  | \  | \  | \  |   "* each horizontal edge is an indel where the top is kept"
    |  \ |  \ |  \ |  \ |  \ |   "* each vertical edge is an indel where the left is kept"
    ▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼
    o---▶o---▶o---▶o---▶o---▶o
    |\   |\   |\   |\   |\   |
   A| \  | \  | \  | \  | \  |
    |  \ |  \ |  \ |  \ |  \ |
    ▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼
    o---▶o---▶o---▶o---▶o---▶o
    |\   |\   |\   |\   |\   |
   P| \  | \  | \  | \  | \  |
    |  \ |  \ |  \ |  \ |  \ |
    ▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼
    o---▶o---▶o---▶o---▶o---▶o
    |\   |\   |\   |\   |\   |
   L| \  | \  | \  | \  | \  |
    |  \ |  \ |  \ |  \ |  \ |
    ▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼
    o---▶o---▶o---▶o---▶o---▶o
    |\   |\   |\   |\   |\   |
   E| \  | \  | \  | \  | \  |
    |  \ |  \ |  \ |  \ |  \ |
    ▼   ▼▼   ▼▼   ▼▼   ▼▼   ▼▼
    o---▶o---▶o---▶o---▶o---▶o
   ```

   A path in this graph from source (top-left) to sink (bottom-right) represents an alignment.

 * `{bm} alignment path/(sequence alignment graph path|sequence alignment path|alignment graph path|alignment path)/i` - A path in an alignment graph that represents one possible sequence alignment. For example, the following alignment path ...
   
   ```{svgbob}
      T    A    B    L    E
    o---▶o---▶o    o    o    o
              |                    "* each diagonal edge is a replacement / keep matching"
   M          |                    "* each horizontal edge is an indel where the top is kept"
              |                    "* each vertical edge is an indel where the left is kept"
              ▼               
    o    o    o    o    o    o   
               \              
   A            \             
                 \            
                  ▼           
    o    o    o    o    o    o
                    \         
   P                 \        
                      \       
                       ▼      
    o    o    o    o    o---▶o
                             |
   L                         |
                             |
                             ▼
    o    o    o    o    o    o
                             |
   E                         |
                             |
                             ▼
    o    o    o    o    o    o
   ```

   is for the sequence alignment...

   |          | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
   |----------|---|---|---|---|---|---|---|---|
   | String 1 | - | - | M | A | P | - | L | E |
   | String 2 | T | A | - | B | L | E | - | - |

 * `{bm} indel` - In the context of sequence alignment, indel is short-hand for insert/delete. For example, the following sequence alignment has 2 indels in the very beginning...

   | String 1 | String 2 | Operation     |
   |----------|----------|---------------|
   |     M    |          | Indel         |
   |          |     T    | Indel         |
   |     A    |     A    | Keep matching |
   |     P    |     B    | Replace       |
   |     L    |     L    | Keep matching |
   |     E    |     E    | Keep matching |

   The term insert/delete makes sense if you were to think of the set of operations as a __transformation__ rather than an alignment. For example, the example above in the context of __transforming__ MAPLE to TABLE:

   | From | To    | Operation       | Result |
   |------|-------|-----------------|--------|
   |   M  |       | Delete M        |        |
   |      |   T   | Insert T        | T      |
   |   A  |   A   | Keep matching A | TA     |
   |   P  |   B   | Replace P to B  | TAB    |
   |   L  |   L   | Keep matching L | TABL   |
   |   E  |   E   | Keep matching E | TABLE  |

 * `{bm} oncogene` - A gene that has the potential to cause cancer. In tumor cells, these genes are often mutated or expressed at higher levels.

   Most normal cells will undergo apoptosis when critical functions are altered and malfunctioning. Activated oncogenes may cause those cells to survive and proliferate instead.

 * `{bm} hamming distance` - Given two strings, the hamming distance is the number of positional mismatches between them. For example, the hamming distance between ACTTTGTT and AGTTTCTT is 2.

   |          | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
   |----------|---|---|---|---|---|---|---|---|
   | String 1 | A | C | T | T | T | G | T | T |
   | String 2 | A | G | T | T | T | C | T | T |
   | Results  | ✓ | ✗ | ✓ | ✓ | ✓ | ✗ | ✓ | ✓ |

 * `{bm} dynamic programming/(dynamic programming algorithm|dynamic programming)/i` - An algorithm that solves a problem by recursively breaking it down into smaller sub-problems, where the result of each recurrence computation is stored in some lookup table such that it can be re-used if it were ever encountered again (essentially trading space for speed). The lookup table may be created beforehand or as a cache that gets filled as the algorithm runs.
 
   For example, imagine a money system where coins are represented in 1, 12, and 13 cent denominations. You can use recursion to find the minimum number of coins to represent some monetary value such as $0.17:
   
   ```python
   def min_coins(value):
     if value == 0.01 or value == 0.12 or value == 0.13:
       return 1
     else:
       return min([
         min_coins(value - 0.01) + 1,
         min_coins(value - 0.12) + 1,
         min_coins(value - 0.13) + 1
       ])
   ```

   ```{svgbob}
   "Recursive breaking down into smaller problems."

                      13
                     /
                   14--2--1
                  /  \
                 /    1
                /
              15--3--2--1
             /  \
            /    2--1
           /
         16--4--3--2--1
        /  \
       /    \ 
      /      3--2--1
     /
   17--5--4--3--2--1
     \
      4--3--2--1
   ```

   The recursive graph above shows how $0.17 can be produced from a minimum of 5 coins: 1 x 13 cent denomination and 4 x 1 cent denomination. However, it recomputes identical parts of the graph multiple times. For example, `min_coins(3)` is independently computed 5 times. With dynamic programming, it would only be computed once and the result would be re-used each subsequent time `min_coins(3)` gets encountered.

 * `{bm} manhattan tourist problem` - The Manhattan tourist problem is an allegory to help explain sequence alignment graphs. Whereas in sequence alignments you're finding a path through the graph from source to sink that has the maximum weight, in the Manhattan tourist problem you're finding a path from 59th St and 8th Ave to 42nd St and 3rd Ave with the most tourist sights to see. It's essentially the same problem as global alignment: 
 
   * The graph is the street layout of Manhattan.
   * The only options at each intersection are to move right or down.
   * The source node is the intersection of 59th St and 8th Ave.
   * The sink node is the intersection of 42nd St and 3rd Ave.
   * The number of tourist sights from one intersection to the next is the weight of an edge.


   ```{svgbob}
                             L
                             e
         8   7   6   5       x   3
                       
         A   A   A   A       A   A
         v   v   v   v       v   v
         e   e   e   e       e   e
   59 St o-->o-->o-->o- - - -o-->o 
         |   |   |   |       |   |
         |   |   |   |       |   |
         |   |   |   |       |   |
         v   v   v   v       v   v
   57 St o-->o-->o-->o- - - -o-->o
         |   | T |   |       |   |
         |   |   |   |       |   |
         |   |   |   |       |   |
         v   v   v   v       v   v
   55 St o-->o-->o-->o- - - -o-->o
         |   |   |   |       |   |
         |   |  T|   |       |   |
         |   |   |   |       |   |
         v   v   v   v       v   v
   53 St o-->o-->o-->o- - - -o-->o
         |   |   |   |       |   |
         |   |   |   |       |   |
         |   |   |   |       |   |
         v   v   v   v       v   v
   51 St o-->o-->o-->o- - - -o-->o
         :   :   :   :       :   :
         :   :   :   :       :   :
         :   :   :   :       :   :
         :   :   :   :       :   :
         :   :   :   :       :   :
         v   v   v   v       v   v
   43 St o-->o-->o-->o- - - -o-->o
         | T |   |   |       |   |
         |   |   |   |       |   |
         |   |   |   |       |   |
         v   v   v T v       v   v
   42 St o-->o-->o-->o- - - -o-->o
   ```

 * `{bm} point accepted mutation/(point accepted mutation|percent accepted mutation)/i` `{bm} /\b(PAM)\d*\b//false/true` - A scoring matrix used for sequence alignments of proteins. The scoring matrix is calculated by inspecting / extrapolating mutations as homologous proteins evolve. Specifically, mutations in the DNA sequence that encode some protein may change the resulting amino acid sequence for that protein. Those mutations that...

    * impair the ability of the protein to function aren't likely to survive, and as such are given a low score. 
    * keep the protein functional are likely to survive, and as such are given a normal or high score.

 * `{bm} blocks amino acid substitution matrix/(blocks substitution matrix|blocks substitution matrices|blocks amino acid substitution matrices|blocks amino acid substitution matrix)/i` `{bm} /\b(BLOSUM)\d*\b//false/true` - A scoring matrix used for sequence alignments of proteins. The scoring matrix is calculated by scanning a protein database for highly conserved regions between similar proteins, where the mutations between those highly conserved regions define the scores. Specifically, those highly conserved regions are identified based on local alignments without support for indels (gaps not allowed). Non-matching positions in that alignment define potentially acceptable mutations.

 * `{bm} point mutation` - A mutation in DNA (or RNA) where a single nucleotide base is either changed, inserted, or deleted.

 * `{bm} directed acyclic graph` `{bm} /\b(DAG)\b/` - A graph where the edges are directed (have a direction) and no cycles exist in the graph.

   For example, the following is a directed acyclic graph...

   ```{svgbob}
   .----> B ----.
   |            v
   A ---------> C ----> D
                |
                `-----> E 
   ```

   The following graph isn't a directed acyclic graph because the edges don't have a direction (no arrowhead means you can travel in either direction)...

   ```{svgbob}
   .----- B ----.
   |            |
   A ---------- C ----- D
                |
                `------ E 
   ```

   The following graph isn't a directed acyclic graph because it contains a cycle between D and B...

   ```{svgbob}
          .-------------.
          v             |
   .----> B ----.       |
   |            v       |
   A ---------> C ----> D
                |
                `-----> E 
   ```

 * `{bm} divide-and-conquer algorithm/(divide-and-conquer algorithm|divide and conquer algorithm)/i` - An algorithm that solves a problem by recursively breaking it down into two or more smaller sub-problems, up until the point where each sub-problem is small enough / simple enough to solve. Examples include quicksort and merge sort.

   See dynamic programming.

 * `{bm} global alignment/(global alignment|global sequence alignment)/i` - A form of sequence alignment that finds the highest scoring alignment between a set of sequences. The sequences are aligned in their entirety. For example, the sequences TRELLO and MELLOW have the following global alignment...

   | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
   |---|---|---|---|---|---|---|
   | T | R | E | L | L | O | - |
   | - | M | E | L | L | O | W |

   This is the form of sequence alignment that most people think about when they hear "sequence alignment."

 * `{bm} local alignment/(local alignment|local sequence alignment)/i` - A form of sequence alignment that isolates the alignment to a substring of each sequence. The substrings that score the highest are the ones selected. For example, the sequences TRELLO and MELLOW have the following local alignment...

   | 0 | 1 | 2 | 3 |
   |---|---|---|---|
   | E | L | L | O |
   | E | L | L | O |

   ... because out of all substrings in TRELLO and all substrings in MELLOW, ELLO (from TRELLO) scores the highest against ELLO (from MELLOW).

 * `{bm} fitting alignment/(fitting alignment|fitting sequence alignment)/i` - A form of 2-way sequence alignment that isolates the alignment such that the entirety of one sequence is aligned against a substring of the other sequence. The substring producing the highest score is the one that's selected. For example, the sequences ELO and MELLOW have the following fitting alignment...

   | 0 | 1 | 2 | 3 |
   |---|---|---|---|
   | E | L | - | O |
   | E | L | L | O |

   ... because out of all the substrings in MELLOW, the substring ELLO scores the highest against ELO.

 * `{bm} overlap alignment/(overlap alignment|overlap sequence alignment)/i` - A form of 2-way sequence alignment that isolates the alignment to a suffix of the first sequences and a prefix of the second sequence. The prefix and suffix producing the highest score are the ones selected . For example, the sequences BURRITO and RICOTTA have the following overlap alignment...

   | 0 | 1 | 2 | 3 | 4 |
   |---|---|---|---|---|
   | R | I | T | - | O |
   | R | I | - | C | O |
  
   ... because out of all the suffixes in BURRITO and the prefixes in RICOTTA, RITO and RICO score the highest.

 * `{bm} Levenshtein distance/(levenshtein distance|string distance)/i` - An application of global alignment where the final weight represents the minimum number of operations required to transform one sequence to another (via swaps, insertions, and deletions). Matches are scored 0, while mismatches and indels are scored -1. For example, TRELLO and MELLOW have the Levenshtein distance of 3...

   |       | 0  | 1  | 2  | 3  | 4  | 5  | 6  |           |
   |-------|----|----|----|----|----|----|----|-----------|
   |       | T  | R  | E  | L  | L  | O  | -  |           |
   |       | -  | M  | E  | L  | L  | O  | W  |           |
   | Score | -1 | -1 | 0  | 0  | 0  | 0  | -1 | Total: -3 |

   Negate the total score to get the minimum number of operations. In the example above, the final score of -3 maps to a minimum of 3 operations.

 * `{bm} genome rearrangement/(genome rearrangement|chromosomal rearrangement|chromosome rearrangement)/i` - A type of mutation where chromosomes go through structural changes, typically caused by either
 
   * breakages in the chromosome, where the broken ends possibly rejoin but in a different order / direction.
   * DNA replication error.
   * DNA repair error.
   
   The different classes of rearrangement include...
 
   * reversal / inversion: A break at two different locations followed by rejoining of the broken ends in different order. and rejoin in different order
  
     ```{svgbob}
                                    .--------------.
     "BEFORE:"    A1 ->  A2 -> A3 -> A4 -> A5 -> A6 -> A7 -> A8 -> A9
     "AFTER:"     A1 ->  A2 -> A3 -> A7 <- A6 <- A5 -> A7 -> A8 -> A9
                                    '--------------'
     ```

   * translocation:

     ```{svgbob}
                       .--------------.
     "BEFORE:"    A1 -> A2 -> A3 -> A4 -> A5 -> A6 -> A7 -> A8 -> A9
     "AFTER:"     A1 -> A5 -> A6 -> A7 -> A8 -> A2 -> A3 -> A4 -> A9
                                               '--------------'
     ```

   * deletion:

     ```{svgbob}
                       .--------------.
     "BEFORE:"    A1 -> A2 -> A3 -> A4 -> A5 -> A6 -> A7 -> A8 -> A9
     "AFTER:"     A1 -> A5 -> A6 -> A7 -> A8 -> A9
     ```

   * duplication:

     ```{svgbob}
                       .--------.
     "BEFORE:"    A1 -> A2 -> A3 -> A4 -> A5 -> A6 -> A7 -> A8 -> A9
     "AFTER:"     A1 -> A2 -> A3 -> A4 -> A5 -> A6 -> A7 -> A8 -> A2 -> A3 -> A9
                                                                 '--------'
     ```

   * chromosome fusion:

     ```{svgbob}
                                               .--------.
     "BEFORE:"    A1 -> A2 -> A3 -> A4 -> A5 -> A6    B1 -> B2 -> B3
     "AFTER:"     A1 -> A2 -> A3 -> A4 -> A5 -> A6 -> B1 -> B2 -> B3
                                               '--------'
     ```

   * chromosome fission:

     ```{svgbob}
                                               .--------.
     "BEFORE:"    A1 -> A2 -> A3 -> A4 -> A5 -> A6 -> B1 -> B2 -> B3
     "AFTER:"     A1 -> A2 -> A3 -> A4 -> A5 -> A6    B1 -> B2 -> B3
                                               '--------'
     ```

   The segments of the genome that were moved around are referred to as synteny blocks.

 * `{bm} chimeric gene` - A gene born from two separate genes getting fused together. A chimeric gene may have been created via genome rearrangement translocations.

   An example of a chimeric gene is the gene coding for ABL-BCR fusion protein: A fusion of two smaller genes (coding for ABL and BCR individually) caused by chromosomes 9 and 22 breaking and re-attaching in a different order. The ABL-BCR fusion protein has been implicated in the development of a cancer known as chronic myeloid leukemia.

 * `{bm} reversal distance` - The *minimum* number of genome rearrangement reversals required to transform genome P to genome Q. The minimum is chosen because of parsimony. 
 
   The short-hand for this is `{kt} d_{rev}(P, Q)`.

 * `{bm} dosage compensation/(sex-chromosome dosage compensation|sex chromosome dosage compensation|dosage compensation)/i` - The mechanism by which sex chromosome gene expression is equalized between different sexes of the same species.
 
   For example, mammals have two sexes...
   
    * males, identified by one X chromosome and one Y chromosome.
    * females, identified by two X chromosomes.
    
   Since females have two X chromosomes, it would make sense for females to have double the gene expression for X chromosome genes. However, many X chromosome genes have nothing to do with sex and if their expression were doubled it would lead to disease. As such, female mammals randomly shut down one of two X chromosomes so as to keep X chromosome gene expression levels roughly equivalent to that of males.

   For mammals, this mechanism means that X chromosomes are mostly conserved because an X chromosome that's gone through genome rearrangement likely won't survive: If a gene jumps off an X chromosome its gene expression may double, leading to problems.
  
   Different species have different mechanisms for equalization. For example, some species will double the gene expression on the male's single X chromosome rather than deactivating one of the female's two X chromosomes. Other hermaphroditic species may scale down X chromosome gene expression when multiple X chromosomes are present.

 * `{bm} synteny/(synteny block|synteny region|syntenic region|synteny|syntenic|syntenies)/i` - Intervals within two sets of chromosomes that have similar genes which are either in ...
 
   * the same order.
     
     ```{svgbob}
     "Region of chromosome set 1:"
     .------------..--------..----------------..------------.
     | > > A1 > > || > B1 > || > > > C1 > > > || > > D1 > > |
     `------------'`--------'`----------------'`------------'

     "Region of chromosome set 2:"
     .------------..--------..------------..----------------.
     | > > A2 > > || > B2 > || > > C2 > > || > > > D2 > > > |
     `------------'`--------'`------------'`----------------'

     * "A1 and A2 are similar genes."
     * "B1 and B2 are similar genes."
     * "C1 and C2 are similar genes."
     * "D1 and D2 are similar genes."
     ```

   * reverse order, where each gene's sequence is also reversed.

     ```{svgbob}
     "Region of chromosome set 1:"
     .------------..--------..----------------..------------.
     | > > A1 > > || > B1 > || > > > C1 > > > || > > D1 > > |
     `------------'`--------'`----------------'`------------'
     
     "Region of chromosome set 2:"
     .----------------..------------..--------..------------.
     | < < < D2 < < < || < < C2 < < || < B2 < || < < A2 < < |
     `----------------'`------------'`--------'`------------'

     * "A1 and A2 are similar genes, but with reversed sequences."
     * "B1 and B2 are similar genes, but with reversed sequences."
     * "C1 and C2 are similar genes, but with reversed sequences."
     * "D1 and D2 are similar genes, but with reversed sequences."
     ```

   The idea is that as evolution branches out a single ancestor species to different sub-species, genome rearrangements (reversals, translocations, etc..) are responsible for some of those mutations. As chromosomes break and rejoin back together in different order, the stretches between breakage points remain largely the same. For example, it's assumed that mice and humans have the same ancestor species because of the high number of synteny blocks between their genomes (most human genes have a mouse counterpart).

   ```{svgbob}
       -W       -U       +V          -T                               +T              +U        +V                  +W   
   --<<<<<<<--<<<<<<<-->>>>>>>--<<<<<<<<<<<<<<--      vs       -->>>>>>>>>>>>>>----->>>>>>>--->>>>>>>------------->>>>>>>---------
    5'                  genome1              3'                 5'                          genome2                            3'
   ```

 * `{bm} parsimony/(parsimony|parsimonious)/i` - The scientific concept of choosing the fewest number of steps / shortest path / simplest scenario / simplest explanation that fits the evidence available.

 * `{bm} genomic dot-plot/(genomic dot-plot|genomic dot plot)/i` - Given two genomes, create a 2D plot where each axis is assigned to one of the genomes and a dot is placed at each coordinate containing a match, where a match is either a shared k-mer or a k-mer and its reverse complement. Matches may also be fuzzily found (e.g. within some hamming distance rather).
    
   For example, ...

   ```{svgbob}
   "Consider each shared 5-mer, shown as a line, to be a dot."
   * "N = normal match"
   * "R = reverse complement match"

     3' 5'|   
      G C |                                     ^            
          |                                    /
      G C |                                   /                
          |                                  /
      T A |                                 / N: "ACTGG vs ACTGG"         
          |                                /  
      C G |                               /                   
          |                              /      
      A T |                             *                    
          |   
      C C |                                                     ^
          |                                                    /
      G A |                                                   /
          |                                                  /
      T G |                                                 / N: "CATGC vs CATGC"
          |                                                /  
    g A T |                                               /         *
    e     |                                              /           \
    n C G |                                             *             \
    o     |                                                            \
    m C G |                                                             \ R: "CCCCA vs TGGGG"
    e     |                                                              \
    1 C G |   *                                                           \
          |    \                                                           \
      C G |     \                                                           v
          |      \  
      A T |       \ R: "AAACC vs GGTTT"                                      
          |        \
      A T |         \                                          
          |          \
      A T |           v                                     
          |   
      G C |                                                                   ^
          |                                                                  /
      G C |                                                                 / 
          |                                                                / 
      G C |                                                               / N: "GGGGG vs GGGGG" 
          |                                                              /  
      G C |                                                             /    
          |                                                            /      
      G C |                                                           *        
     5' 3'|                                                                   
          +-----------------------------------------------------------------------
           5' G G T T T A G G T G A C T T A C T G G A A C A T G C T T G G G G G 3'
           3' C C A A A T C C A C T G A A T G A C C T T G T C A G T T C C C C C 5'
                                          genome2
   ```

   Genomic dot-plots are typically used in building synteny graphs: Graphs that reveal shared synteny blocks (shared stretches of DNA). Synteny blocks exist because genome rearrangements account for a large percentage of mutations between two species that branched off from the same parent (given that they aren't too far removed -- e.g. mouse vs human).

 * `{bm} synteny graph/(synteny graph)/i` - Given the genomic dot-plot for two genomes, cluster together points so as to reveal synteny blocks. For example, ...

   ```{svgbob}
    * "N = normal k-mer match"
    * "R = reverse complement k-mer match"

   3'|                                                                                  3'|                                                                 
     |  R                              R                                                  |  *                                                              
     |   R           N                                                                    |   \                                                             
     |    R               R                                                               |    \                                                            
     |      R                           R           N                                     |     \                                                           
     |       R                                                                            |      \                                                          
     |       R               N                                                            |     A \                                                         
    g|        R                                                                          g|        \                                                        
    e|          R                   R           N                                        e|         \                                                      
    n|           R                                                                       n|          \                                                     
    o|            R                                     R                   ------->     o|           v                                                    
    m|   N                        N                                         CLUSTER      m|                           ^                                    
    e|                          N            N                                           e|                        C /                                      
    1|      N                  N                                                         1|                         /                                      
     |                        N               N         N                                 |                        *                                          
     |                 R                                                                  |                 *                                               
     |                   R                                                                |                  \                                             
     |                    R                                                               |                 B \                                           
     |    R                R                                                              |                    v                                               
     |                                           R              R                         |                                           *                     
     |             N              N                R                                      |                                            \                    
     |                                              R           R                         |                                           D \                    
   5'|       R             R                   R     R                                  5'|                                              v                  
     +-----------------------------------------------------------------                   +-----------------------------------------------------------------
      5'                          genome2                            3'                    5'                          genome2                            3'

    * "Remember that the direction of DNA is 5' to 3'."
   ```

   ... reveals that 4 synteny blocks are shared between the genomes. One of the synteny blocks is a normal match (C) while three are matching against their reverse complements (A, B, and D)...

   ```{svgbob}
   * "Synteny blocks projected on to each axis."

        -D       -B      +C          -A                               +A              +B        +C                  +D   
   --<<<<<<<--<<<<<<<-->>>>>>>--<<<<<<<<<<<<<<--      vs       -->>>>>>>>>>>>>>----->>>>>>>--->>>>>>>------------->>>>>>>---------
    5'                  genome1              3'                 5'                          genome2                            3'
   ```

 * `{bm} breakpoint/(adjacent|adjacency|adjacencies|breakpoint)_GR/i` - Given two genomes that share synteny blocks, where one genome has the synteny blocks in desired order and direction while the other does not, an ...
 
   * adjacency_GR is when two neighbouring synteny blocks in the undesired genome are following each other just as they do in the desired genome.

     ```{svgbob}
     * "In this example, the undesired genome has B and C next to each other and the"
       "tail of B is followed by the head of C, just as in the desired genome."

                                .---------------------------------------------------.
                       .--------+--------.                                 .--------+-------.                          
            +A            +B        +C          +D                            +B       +C       +D          -A         
     -->>>>>>>>>>>>>>--->>>>>>>--->>>>>>>----->>>>>>>------      vs       -->>>>>>>--->>>>>>-->>>>>>>--<<<<<<<<<<<<<<--
      5'                      DESIRED                   3'                 5'       ^       UNDESIRED               3' 
                                                                                    |
                                                                                adjacency
     ```

     ```{svgbob}
     * "In this example, the undesired genome has B and C next to each other and the"
       "tail of B is followed by the tail of C, just as in the desired genome."

                                .---------------------------------------------------.
                       .--------+--------.                                 .--------+-------.                          
            +A            +B        -C          +D                            +B       -C       +D          -A         
     -->>>>>>>>>>>>>>--->>>>>>>---<<<<<<<----->>>>>>>------      vs       -->>>>>>>--<<<<<<<-->>>>>>>--<<<<<<<<<<<<<<--
      5'                      DESIRED                   3'                 5'       ^       UNDESIRED               3' 
                                                                                    |
                                                                                adjacency
     ```

     ```{svgbob}
     * "In this example, the undesired genome has B and C next to each other and the"
       "tail of B is followed by the head of C, just as in the desired genome. Note"
       "that their placement has been swapped when compared to the desired genome."
       "This is fine. As long as they follow each other as they do in the desired"
       "genome, it's considered an adjacency."
     
                                .--------------------------------------------.
                       .--------+--------.                          .--------+-------.                          
            +A            +B        +C          +D                     -C       -B       +D          -A         
     -->>>>>>>>>>>>>>--->>>>>>>--->>>>>>>----->>>>>>>------   vs   --<<<<<<<--<<<<<<<-->>>>>>>--<<<<<<<<<<<<<<--
      5'                      DESIRED                   3'          5'       ^       UNDESIRED               3' 
                                                                             |
                                                                         adjacency
     ```

   * breakpoint_GR is when two neighbouring synteny blocks in the undesired genome don't fit the definition of an adjacency_GR: They aren't following each other just as they do in the desired genome.

     ```{svgbob}
     * "In this example, the undesired genome has B and C next to each other but the"
       "tail of B is NOT followed by the head of A, as it is in the desired genome."

                                .--------------------------------------------.
                       .--------+--------.                          .--------+-------.                          
            +A            +B        +C          +D                     +B       -C       +D          -A         
     -->>>>>>>>>>>>>>--->>>>>>>--->>>>>>>----->>>>>>>------   vs   -->>>>>>>---<<<<<<-->>>>>>>--<<<<<<<<<<<<<<--
      5'                      DESIRED                   3'          5'       ^       UNDESIRED               3' 
                                                                             |
                                                                         breakpoint
     ```

     ```{svgbob}
     * "In this example, the undesired genome does NOT have B and C next to each"
       "other."

                                .---------------------------------------+---------------------------------.
                       .--------+--------.                          .---+---.                         .---+---.
            +A            +B        +C          +D                     +B        -D          -A          +C     
     -->>>>>>>>>>>>>>--->>>>>>>--->>>>>>>----->>>>>>>------   vs   -->>>>>>>---<<<<<<--<<<<<<<<<<<<<<-->>>>>>>--
      5'                      DESIRED                   3'          5'       ^       UNDESIRED        ^      3' 
                                                                             |                        |
                                                                         breakpoint               breakpoint
     ```

   Breakpoint_GRs and adjacencies_GR are useful because they identify desirable points for reversals (genome rearrangement), giving way to algorithms that find / estimate the reversal distance. For example, a contiguous train of adjacencies_GR in an undesired genome may identify the boundaries for a single reversal that gets the undesired genome closer to the desired genome.

   ```{svgbob}
   * "The contiguous segment comprising D, C, and B may be reversed as"
     "a single genome reversal."

                                                                         breakpoint  adjacency   adjacency   breakpoint    
                                                                             |           |           |           |         
       +A          +B         +C          +D         +E                +A    v     -D    v    -C     v    -B     v   +E    
   -->>>>>>>----->>>>>>>---->>>>>>>----->>>>>>----->>>>>>--   vs   -->>>>>>>-----<<<<<<<----<<<<<<<-----<<<<<<----->>>>>>--
    5'                      DESIRED                     3'          5'                     UNDESIRED                    3' 
   ```
   
   The number of breakpoint_GRs and adjacencies_GR always equals one less than the number of synteny blocks.

   ```{svgbob}
   * "1 + 2 =  4 - 1"

                                                                        adjacency   breakpoint  breakpoint
                                                                            |           |           |
          +A            +B        -C          +D                      +B    v     -C    v    +D     v       -A         
   -->>>>>>>>>>>>>>--->>>>>>>---<<<<<<<----->>>>>>>------    vs   -->>>>>>>-----<<<<<<<---->>>>>>>-----<<<<<<<<<<<<<<--
    5'                      DESIRED                   3'           5'               UNDESIRED                       3' 
   ```

 * `{bm} breakpoint graph/(breakpoint graph)_GR/i` - An undirected graph representing the order and orientation of synteny blocks shared between two genomes.

   For example, the following two genomes share the synteny blocks A, B, C, and D...

   ```{svgbob}
       -D       -B       +C          -A                               +A              +B        +C                  +D   
   --<<<<<<<--<<<<<<<-->>>>>>>--<<<<<<<<<<<<<<--      vs       -->>>>>>>>>>>>>>----->>>>>>>--->>>>>>>------------->>>>>>>---------
    5'                  genome1              3'                 5'                          genome2                            3'
   ```

   The breakpoint graph_GR for the above two genomes is basically just a merge of the above diagrams. The set of synteny blocks shared between both genomes (A, B, C, and D) become dashed edges where each edge's...
   
    * arrow end is a tail node (t suffix).
    * non-arrow end is a head node (h suffix).
  
   Gap regions between synteny blocks are represented by solid colored edges, either red or blue depending on which genome it is.
   
   If the genomes are linear, gap region edges are created between the nodes and the edges and a special termination node.

   ```{dot}
   graph G {
   layout=neato
   labelloc="t";
   label="CIRCULAR vs LINEAR...";
   node [shape=plain];
   _C1_t_ [pos="2.0,0.0!"];
   _C1_h_ [pos="1.4142135623730947,-1.4142135623730954!"];
   _B1_t_ [pos="0.0,-2.0!"];
   _B1_h_ [pos="-1.4142135623730954,-1.414213562373095!"];
   _A1_t_ [pos="-2.0,0.0!"];
   _A1_h_ [pos="-1.414213562373095,1.4142135623730951!"];
   _D1_t_ [pos="0.0,2.0!"];
   _D1_h_ [pos="1.4142135623730951,1.414213562373095!"];
   _C1_t_ -- _C1_h_ [style=dashed];
   _B1_t_ -- _B1_h_ [style=dashed];
   _A1_t_ -- _A1_h_ [style=dashed];
   _D1_t_ -- _D1_h_ [style=dashed];
   _C1_t_ -- _D1_h_ [color=blue];
   _A1_h_ -- _D1_t_ [color=blue];
   _B1_t_ -- _C1_h_ [color=blue];
   _A1_t_ -- _B1_h_ [color=blue];
   _B1_h_ -- _C1_h_ [color=red];
   _A1_t_ -- _C1_t_ [color=red];
   _A1_h_ -- _D1_t_ [color=red];
   _B1_t_ -- _D1_h_ [color=red];
   
   
   _C2_t_ [label="_C_t_", pos="7.0,0.0!"];
   _C2_h_ [label="_C_h_", pos="6.4142135623730947,-1.4142135623730954!"];
   _B2_t_ [label="_B_t_", pos="5,-2.0!"];
   _B2_h_ [label="_B_h_", pos="3.585786438,-1.414213562373095!"];
   _A2_t_ [label="_A_t_", pos="3.0,0.0!"];
   _A2_h_ [label="_A_h_", pos="3.585786438,1.4142135623730951!"];
   _D2_t_ [label="_D_t_", pos="5,2.0!"];
   _D2_h_ [label="_D_h_", pos="6.4142135623730951,1.414213562373095!"];
   TERM [pos="4.9,0.5!"];
   _C2_t_ -- _C2_h_ [style=dashed];
   _B2_t_ -- _B2_h_ [style=dashed];
   _A2_t_ -- _A2_h_ [style=dashed];
   _D2_t_ -- _D2_h_ [style=dashed];
   _C2_t_ -- _D2_h_ [color=blue];
   _B2_t_ -- _C2_h_ [color=blue];
   _A2_t_ -- _B2_h_ [color=blue];
   _A2_h_ -- TERM [color=blue];
   _D2_t_ -- TERM [color=blue];
   _B2_h_ -- _C2_h_ [color=red];
   _A2_t_ -- _C2_t_ [color=red];
   _B2_t_ -- _D2_h_ [color=red];
   _A2_h_ -- TERM [color=red];
   _D2_t_ -- TERM [color=red];
   }
   ```

   In the above breakpoint graph_GR, the blue edges represent genome 2's gap regions while the red edges represent genome 1's gap regions. The set of edges representing synteny blocks is shared between them.
   
   Breakpoint graph_GRs build on the concept of breakpoint_GRs to compute a parsimonious path of fusion, fission, and reversal mutations (genome rearrangements) that transforms one genome into the other (see 2-break). Conventionally, blue edges represent the final desired path while red edges represent the path being transformed. As such, breakpoint graph_GRs typically order synteny blocks so that blue edges are uniformly sandwiched between synteny blocks / red edges get chaotically scattered around.

 * `{bm} 2-break/\b(2-break|2 break|two break|two-break)s?\b/i/false/true` - Given a breakpoint graph_GR, a 2-break operation breaks the two red edges at a synteny block boundary and re-wires them such that one of the red edges matches the blue edge at that boundary.
 
   For example, the two red edges highlighted below share the same synteny block boundary and can be re-wired such that one of the edges matches the blue edge at that synteny boundary ...

   ```{dot}
   graph G {
   layout=neato
   labelloc="t";
   label="BEFORE to AFTER...";
   node [shape=plain];

   _C1_t_ [label="_C_t_", pos="2.0,0.0!"];
   _C1_h_ [label="_C_h_", pos="1.4142135623730947,-1.4142135623730954!"];
   _B1_t_ [label="_B_t_", pos="0.0,-2.0!"];
   _B1_h_ [label="_B_h_", pos="-1.4142135623730954,-1.414213562373095!"];
   _A1_t_ [label="_A_t_", pos="-2.0,0.0!"];
   _A1_h_ [label="_A_h_", pos="-1.414213562373095,1.4142135623730951!"];
   _D1_t_ [label="_D_t_", pos="0.0,2.0!"];
   _D1_h_ [label="_D_h_", pos="1.4142135623730951,1.414213562373095!"];
   _C1_t_ -- _C1_h_ [style=dashed];
   _B1_t_ -- _B1_h_ [style=dashed];
   _A1_t_ -- _A1_h_ [style=dashed];
   _D1_t_ -- _D1_h_ [style=dashed];
   _C1_t_ -- _D1_h_ [color=blue];
   _A1_h_ -- _D1_t_ [color=blue];
   _B1_t_ -- _C1_h_ [color=blue];
   _A1_t_ -- _B1_h_ [color=blue];
   _B1_h_ -- _C1_h_ [color=red];
   _A1_t_ -- _C1_t_ [color=red, penwidth="4"];
   _A1_h_ -- _D1_t_ [color=red];
   _B1_t_ -- _D1_h_ [color=red, penwidth="4"];

   _C2_t_ [label="_C_t_", pos="7.0,0.0!"];
   _C2_h_ [label="_C_h_", pos="6.4142135623730947,-1.4142135623730954!"];
   _B2_t_ [label="_B_t_", pos="5,-2.0!"];
   _B2_h_ [label="_B_h_", pos="3.585786438,-1.414213562373095!"];
   _A2_t_ [label="_A_t_", pos="3.0,0.0!"];
   _A2_h_ [label="_A_h_", pos="3.585786438,1.4142135623730951!"];
   _D2_t_ [label="_D_t_", pos="5,2.0!"];
   _D2_h_ [label="_D_h_", pos="6.4142135623730951,1.414213562373095!"];
   _C2_t_ -- _C2_h_ [style=dashed];
   _B2_t_ -- _B2_h_ [style=dashed];
   _A2_t_ -- _A2_h_ [style=dashed];
   _D2_t_ -- _D2_h_ [style=dashed];
   _C2_t_ -- _D2_h_ [color=blue];
   _A2_h_ -- _D2_t_ [color=blue];
   _B2_t_ -- _C2_h_ [color=blue];
   _A2_t_ -- _B2_h_ [color=blue];
   _B2_h_ -- _C2_h_ [color=red];
   _A2_t_ -- _B2_t_ [color=red, penwidth="4"];
   _A2_h_ -- _D2_t_ [color=red];
   _C2_t_ -- _D2_h_ [color=red, penwidth="4"];
   }
   ```

   Each 2-break operation on a breakpoint graph_GR represents a fusion, fission, or reversal mutation (genome rearrangement). Continually applying 2-breaks until all red edges match blue edges reveals a parsimonious path of such mutations that transforms the red genome to the blue genome.

 * `{bm} permutation/(permutation)_GR/i` - A list representing a single chromosome in one of the two genomes that make up a breakpoint graph_GR. The entire breakpoint graph_GR is representable as two sets of permutation_GRs, where each genome in the breakpoint graph_GR is a set.
 
   Permutation_GR sets are commonly used for tersely representing breakpoint graph_GRs as text. For example, given the following breakpoint graph_GR ...

   ```{dot}
   graph G {
   layout=neato
   node [shape=plain];
   _C_t_ [pos="2.0,0.0!"];
   _C_h_ [pos="1.4142135623730947,-1.4142135623730954!"];
   _B_t_ [pos="0.0,-2.0!"];
   _B_h_ [pos="-1.4142135623730954,-1.414213562373095!"];
   _A_t_ [pos="-2.0,0.0!"];
   _A_h_ [pos="-1.414213562373095,1.4142135623730951!"];
   _D_t_ [pos="0.0,2.0!"];
   _D_h_ [pos="1.4142135623730951,1.414213562373095!"];
   _C_t_ -- _C_h_ [style=dashed];
   _B_t_ -- _B_h_ [style=dashed];
   _A_t_ -- _A_h_ [style=dashed];
   _D_t_ -- _D_h_ [style=dashed];
   _C_t_ -- _D_h_ [color=blue];
   _A_h_ -- _D_t_ [color=blue];
   _B_t_ -- _C_h_ [color=blue];
   _A_t_ -- _B_h_ [color=blue];
   _B_h_ -- _C_h_ [color=red];
   _A_t_ -- _C_t_ [color=red];
   _A_h_ -- _D_t_ [color=red];
   _B_t_ -- _D_h_ [color=red];
   }
   ```

   ... , the permutation_GR set representing the red genome may be any of the following ...

    * `{[-D, -B, +C, -A]}`
    * `{[+A, -C, +B, +D]}`
    * `{[-B, +C, -A, -D]}`
    * `{[-C, +B, +D, +A]}`
    * `{[+C, -A, -D, -B]}`
    * ...

   All representations above are equivalent.

   ```{note}
   See Algorithms/Synteny/Reversal Path/Breakpoint List Algorithm_TOPIC for a full explanation of how to read_NORM permutation_GRs / how to convert from and to breakpoint graph_GRs.
   ```

 * `{bm} fusion/(\bfusion|\bfuse)/i` - Joining two or more things together to form a single entity. For example, two chromosomes may join together to form a single chromosome (genome rearrangement).

 * `{bm} fission` - Splitting a single entity into two or more parts. For example, a single chromosome may break into multiple pieces where each piece becomes its own chromosome (genome rearrangement).

 * `{bm} translocation` - Changing location. For example, part of a chromosome may transfer to another chromosome (genome rearrangement).

 * `{bm} severe acute respiratory syndrome` `{bm} /(SARS)/` - A deadly coronavirus that emerged from China around early 2003. The virus transmits itself through droplets that enter the air when someone with the disease coughs.

 * `{bm} coronavirus` `{bm} /(COVID|CoV)/` - A family of viruses that attack the respiratory tracts of mammals and birds. The name comes from the fact that the outer spikes of the virus resemble the corona of the sun (crown of the sun / outermost part of the sun's atmosphere protruding out).
 
   The common cold, SARS, and COVID-19 are examples of coronaviruses.

 * `{bm} human immunodeficiency virus` `{bm} /(HIV|AIDS)/` - A virus that over time causes acquired immunodeficiency syndrome (AIDS).

 * `{bm} immunodeficiency/(immunodeficiency|immunocompromisation|immunocompromised)/i` - A state in which the immune system's ability to fight infectious disease and cancer is compromised or entirely absent.

 * `{bm} DNA virus` - A virus with a DNA genome. Depending on the type of virus, the genome may be single-stranded DNA or double-stranded DNA.

   Herpes, chickenpox, and smallpox are examples of DNA viruses.

 * `{bm} RNA virus` - A virus with a RNA genome. RNA replication has a higher rate than DNA replication, meaning that RNA viruses mutate faster than DNA viruses.

   Coronaviruses, HIV, and influenza are examples of RNA viruses.

 * `{bm} phylogeny/(phylogeny|phylogenetic)/i` - The concept of inferring the evolutionary history among some set of species (shared ancestry) by inspecting properties of those species (e.g. relatedness of phenotypic or genotypic characteristics).
 
   ```{svgbob}
                        * "Unknown Animal"
                       / \
                      /   \
                     /     \
   "Unknown Feline" *       \
                   / \       \
                  /   \       \
                 /     \       \
                *       *       *
               Cat     Lion    Bear
   ```

   In the example above, cat and lion are descendants of some shared ancestor species. Likewise, that ancestor and bears are likely descendants from some other higher up species.

 * `{bm} phylogenetic tree/(phylogenetic tree|phylogeny tree|phylogenies|evolutionary tree)/i` - A tree showing the degree_NORM in which biological species or entities (e.g. viruses) are related. Such trees help infer relationships such as common ancestry or which animal a virus jumped to humans from (e.g. virus A and B are related but A is only present in bats while B just showed up in humans).

   ```{svgbob}
               +--- "Mycoplasma mobile"
   +-----------+
   |           +--- "Mycoplasma arthritidis"
   |   
   |   +----------- "Mycoplasma pulmonis"
   |   |
   +---+   +------- "Mycoplasma synoviae"
       |   |
       +---+
           |   +--- "Mycoplasma bovis"
           +---+
               +--- "Mycoplasma agalactiae"
   ```

 * `{bm} distance metric/(distance metric)/i` - A metric used to measure how different a pair of entities are to each other. Examples include...

   * hamming distance between DNA / protein sequences.
   * global alignment score between DNA / protein sequences.
   * two-break count (reversal distance).
   * number of similar physical or behavioural attributes.
   * euclidean distance between two vectors.
   * pearson distance between two vectors.
   * etc..

   ```{note}
   See also: similarity metric.
   ```

 * `{bm} distance matrix/(distance matrix|distance matrices)/i` - Given a set of n different entities, a distance matrix is an n-by-n matrix where each element contains the distance between the entities for that cell. For example, for the species snake, lizard, bird, and crocodile ...

   |           | Snake | Lizard | Bird | Crocodile |
   |-----------|-------|--------|------|-----------|
   | Snake     |   0   |   2    |  6   |     4     |
   | Lizard    |   2   |   0    |  6   |     4     |
   | Bird      |   6   |   6    |  0   |     5     |
   | Crocodile |   4   |   4    |  5   |     0     |

   The distance metric can be anything so long as it meets the following properties:
   
    * Must produce a non-negative distance -- dist(A,B) >= 0
    * Must produce the same distance regardless of species order -- dist(A,B) == dist(B,A)
    * Must produce a distance that satisfies the triangle inequality property -- if dist(B,C) = x, then dist(A,B) + dist(A,C) >= x

   ````{note}
   I think what the last bullet point means is that the distance will be >= if you travel to it indirectly (hop over to it instead of taking a straight path). For example, if dist(B,C) = 5, then dist(A,B) + dist(A,C) must be >= 5.

   ```{svgbob}
        C
        *
       / \
    3 /   \ 3
     /     \
    *-------*
   A    5    B
   ```

   A, B, and C are species.
   ````

   Common distance metrics include...

    * hamming distance between the DNA sequences.
    * levenshtein distance between the DNA sequences.
    * two-break count (reversal distance).

   Distance matrices are used to generate phylogenetic trees. A single distance matrix may fit many different trees or it's possible that it fits no tree at all. For example, the distance matrix above fits the tree...

   ```{svgbob}
             1
         +------* Snake
      1  |
   +-----*
   |     |   1
   |     +------* Lizard
   |
   *
   |         1
   |     +------* Crocodile
   |  1  |
   +-----*
         |   3
         +------* Bird
   ```

 * `{bm} tree` - In graph theory, a tree is an acyclic undirected graph in which any two nodes are connected by exactly one path (nodes branch outward / never converge).
 
   Trees come in two forms: rooted trees and unrooted trees. In graph theory, a tree typically refers to an unrooted tree.

   ```{note}
   This is different from the computer science definition of tree, which is an abstract data type representing a hierarchy (always a single root that flows downwards), typically generalized as a *directed* acyclic graph as opposed to an undirected acyclic graph.
   ```
   
 * `{bm} unrooted tree/(un-rooted tree|unrooted tree)/i` - A tree without a root node...

   ```{svgbob}
   A   B      C
   *   *      *
    \ /       |
     * D    E *--* F
      \      /
     G *----* H
      /     |\
     *      * *
     I      J K
   ```

   An unrooted tree may be turned into a rooted tree by choosing any non-leaf node (internal node) to be the root node.

   ```{note{
   If injecting a node is a possibility, you can also convert an unrooted tree to a rooted tree by injecting a root node along one of its edges.
   ```

 * `{bm} rooted tree` - A tree with a root node...

   ```{svgbob}
     * D
    /|\
   * * \
   A B  * G
       / \
      *   \
      I    * H
          /|\
         * * \
         J K  * E
             / \
            *   *
            C   F
  
   * "D is the root, and"
     "as such is placed on"
     "top while everything"
     "else flows downward"
   ```

 * `{bm} subtree/(subtree|sub-tree)/i` - Given a node in a tree, that node and all of its descendants comprise a subtree. For example, the following tree has the subtree ...
 
   ```{svgbob}
        TREE                 "SUBTREE AT H"

     * D          
    /|\           
   * * \                          * H    
   A B  * G                      /|\     
       / \                      * * \    
      *   \                     J K  * E 
      I    * H                      / \  
          /|\                      *   * 
         * * \                     C   F 
         J K  * E 
             / \  
            *   * 
            C   F 
   ```

 * `{bm} degree/(degree)_GRAPH/i` - The number of edges leading into / out of a node of an undirected graph.

    The node below has a degree_GRAPH of 3.

    ```{svgbob}
           /
          /
    -----N
          \
           \
    ```

 * `{bm} simple tree` - An unrooted tree where ...
   
    * every internal node has a degree_GRAPH > 2.
    * every edge has a weight of > 0.

   ```{svgbob}
   "non-simple tree"             "simple tree"
   
            *                             
           / 1                            
      *   *                               
     1 \ / 1                       *   * 
        *                         1 \ / 2
      3 |                            *   
        *                          4 |   
      1 |                            *   
        *                         3 / \ 2
     1 / \ 2                       *   * 
      *   *                               
   2 /                                    
    *                                        
   
   * "Non-simple tree transformed into a simple tree. Edges"
     "that were merged had their weights summed."
   ```
   
   In the context of phylogeny, a simple tree's ...
   
    * leaf nodes represent known entities.
    * internal nodes represent inferred ancestor entities.
    * edge weights represent distances between entities.

   The restrictions placed on simple trees simplify the process of working backwards from a distance matrix to a phylogenetic tree.

 * `{bm} additive distance matrix/(additive matrix|additive matrices|additive distance matrix|additive distance matrices)/i` - Given a distance matrix, if there exists a tree with edge weights that satisfy that distance matrix (referred to as fit), that distance matrix is said to be an additive distance matrix.

   For example, the following tree fits the following distance matrix ...
   
   |      | Cat | Lion | Bear |
   |------|-----|------|------|
   | Cat  |  0  |  2   |  3   |
   | Lion |  2  |  0   |  3   |
   | Bear |  3  |  3   |  0   |

   ```{svgbob}
              *
             /|\
            / | \
           /  |  \
          /   |   \
         /    |    \
      1 /   1 |     \ 2
       /      |      \
      *       *       *
     Cat     Lion    Bear
   ```

   The term additive is used because the weights of all edges along the path between leaves (i, j) add to `dist(i, j)` in the distance matrix. Not all distance matrices are additive. For example, no simple tree exists that satisfies the following distance matrix...

   |    | S1 | S2 | S3 | S4 |
   |----|----|----|----|----|
   | S1 | 0  | 3  | 4  | 3  |
   | S2 | 3  | 0  | 4  | 5  |
   | S3 | 4  | 4  | 0  | 2  |
   | S4 | 3  | 5  | 2  | 0  |
   
    * Test simple tree 1:
      
      ```{svgbob}
                 S2
                 *
                 | x
                 |
           w     |     
      S1 *-------*-------* S3
                 |     y
                 |
               z |
                 *
                 S4
      ```
      
      ```
      dist(S1, S2) is 3 = w + x
      dist(S1, S3) is 4 = w + y
      dist(S1, S4) is 3 = w + z
      dist(S2, S3) is 4 = x + y
      dist(S2, S4) is 5 = x + z
      dist(S3, S4) is 2 = y + z
      ```
     
      Attempting to solve this produces inconsistent results. Solved values for each variable don't work across all equations present.
   
    * Test simple tree 2:
      
      ```{svgbob}
                 S2
                 *
               x |
                 |
           w     |
      S1 *-------*
                  \
                   \ u
                    \
                     *-------* S3
                     |     y
                     |
                     | z
                     *
                     S4
      ```
     
      ```
      dist(S1, S2) is 3 = w + x
      dist(S1, S3) is 4 = w + u + y
      dist(S1, S4) is 3 = w + u + z
      dist(S2, S3) is 4 = x + u + y
      dist(S2, S4) is 5 = x + u + z
      dist(S3, S4) is 2 = y + z
      ```
     
      Attempting to solve this produces inconsistent results. Solved values for each variable don't work across all equations present.
   
    * Test simple tree 3:
      
      ```{svgbob}
                 S3
                 *
               x |
                 |
           w     |
      S1 *-------*
                  \
                   \ u
                    \
                     *-------* S2
                     |     y
                     |
                     | z
                     *
                     S4
   
      * "Same structure to previous example"
        "but species assigned to different leafs."
      ```
     
      ```
      dist(S1, S2) is 4 = w + u + y
      dist(S1, S3) is 3 = w + x
      dist(S1, S4) is 3 = w + u + z
      dist(S2, S3) is 4 = x + u + y
      dist(S2, S4) is 2 = y + z
      dist(S3, S4) is 5 = x + u + z
      ```
     
      Attempting to solve this produces inconsistent results. Solved values for each variable don't work across all equations present.
   
    * etc..

 * `{bm} neighbour` - Given two leaf nodes in a tree, those leaf nodes are said to be neighbours if they share they connect to the same internal node. For example, leaf nodes A and B are neighbours in the following tree because they both connect to internal node D ...

   ```{svgbob}
   A   B
   *   *
    \ / 
     * D
      \
     G * 
      /
     *  
     I  
   ```

   ```{note}
   A leaf node will only ever have 1 parent, by definition of a tree.
   ```

 * `{bm} limb` - Given a leaf node in a tree, that leaf node's limb is the edge between it and its parent (node it's connected to). For example, the following tree has the following limbs ...

   ```{svgbob}
   A   B
   *   *
    \ / 
     * D
      \
     G * 
      /
     *  
     I  
   ```

   * (A, D)
   * (B, D)
   * (G, I)

   ```{note}
   A leaf node will only ever have 1 parent, by definition of a tree.
   ```

 * `{bm} limb length/(limb length|limb weight)/i` - Given a leaf node in a tree, the leaf node's limb length is the weight assigned to its limb. For example, node A has a limb length of 2 in the following tree...

   ```{svgbob}
                    * F
                   /
                  / 1
             2   /
         *------*
        / \      \
       /   \      \ 1
    2 /     \ 3    \
     /       \      * E
    *         *
    A         C
   ```

 * `{bm} four point condition/(four points? condition|four point theorem)/i` - An algorithm for determining if a distance matrix is an additive distance matrix. Given four leaf nodes, the algorithm checks different permutation_NORMs of those leaf nodes to see if any pass a test, where that test builds node pairings from the quartet and checks their distances to see if they meet a specific condition...

   ```python
   for a, b, c, d in permutations(quartet, r=4):  # find one perm that passes the following test
       s1 = dist_mat[a][b] + dist_mat[c][d]  # sum of dists for (a,b) and (c,d)
       s2 = dist_mat[a][c] + dist_mat[b][d]  # sum of dists for (a,c) and (b,d)
       s3 = dist_mat[a][d] + dist_mat[b][c]  # sum of dists for (a,d) and (b,c)
       if s1 <= s2 == s3:
           return True
   return False
   ```

   If all possible leaf node quartets pass the above test, the distance matrix is an additive distance matrix (was derived from a tree / fits a tree).

   ```{note}
   See Algorithms/Phylogeny/Test Additive Distance Matrix_TOPIC for a full explanation of how this algorithm works.
   ```

 * `{bm} trimmed distance matrix/(trim distance matrix|trimmed distance matrix|trim distance matrices|trimmed distance matrices)/i` - A distance matrix where a leaf node's row and column have been removed. This is equivalent to removing the leaf node's limb in the corresponding simple tree and merging together any edges connected by nodes of degree_GRAPH 2.
 
   For example, removing v2 from the following distance matrix... 

   |             | v0 | v1 | `{h}red v2` | v3 |
   |-------------|----|----|-------------|----|
   | v0          | 0  | 13 | 21          | 22 |
   | v1          | 13 | 0  | 12          | 13 |
   | `{h}red v2` | 21 | 12 | 0           | 13 |
   | v3          | 22 | 13 | 13          | 0  |

   ```{dot}
   graph G {
    graph[rankdir=LR]
    node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
    edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
    ranksep=0.25
    subgraph cluster_rhs {
     v0 -- i0 [label=11]
     v1 -- i0 [label=2]
     i0 -- i1 [label=4]
     i1 -- v2 [label=6]
     i1 -- v3 [label=7]
    }
   }
   ```

   ... results in v2's row and column being removed ...

   |    | v0 | v1 | v3 |
   |----|----|----|----|
   | v0 | 0  | 13 | 22 |
   | v1 | 13 | 0  | 13 |
   | v3 | 22 | 13 | 0  |

   ```{dot}
   graph G {
    graph[rankdir=LR]
    node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
    edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
    ranksep=0.25
    subgraph cluster_rhs {
     fontname="Courier-Bold"
     fontsize=10
     label="v3 trimmed"
     v0 -- i0 [label=11]
     v1 -- i0 [label=2]
     i0 -- v3 [label=11]
    }
   }
   ```

 * `{bm} balded distance matrix/(bald distance matrix|balded distance matrix|bald distance matrices|balded distance matrices)/i` - An additive distance matrix where the distances in a leaf node's row and column have been subtracted by that leaf node's limb length. This is equivalent to setting the leaf node's limb length to 0 in the corresponding simple tree.
 
   `{bm-disable} 5'` <!-- Needs to be disabled because v3's is conflicting with 3' -->

   For example, balding v5's limb length in the following distance matrix ...

   |    | v0 | v1 | v2 | v3 | v4 | v5 |
   |----|----|----|----|----|----|----|
   | v0 | 0  | 13 | 21 | 21 | 22 | 22 |
   | v1 | 13 | 0  | 12 | 12 | 13 | 13 |
   | v2 | 21 | 12 | 0  | 20 | 21 | 21 |
   | v3 | 21 | 12 | 20 | 0  | 7  | 13 |
   | v4 | 22 | 13 | 21 | 7  | 0  | 14 |
   | v5 | 22 | 13 | 21 | 13 | 14 | 0  |

   ```{dot}
   graph G {
    graph[rankdir=LR]
    node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
    edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
    ranksep=0.25
    subgraph cluster_rhs {
     v0 -- i0 [label=11]
     v1 -- i0 [label=2]
     v2 -- i0 [label=10]
     i0 -- i2 [label=4]
     i2 -- i1 [label=3]
     i1 -- v3 [label=3]
     i1 -- v4 [label=4]
     i2 -- v5 [label=7]
    }
   }
   ```

   ... results in ...


   |    | v0 | v1 | v2 | v3 | v4 | v5 |
   |----|----|----|----|----|----|----|
   | v0 | 0  | 13 | 21 | 21 | 22 | 15 |
   | v1 | 13 | 0  | 12 | 12 | 13 | 6  |
   | v2 | 21 | 12 | 0  | 20 | 21 | 14 |
   | v3 | 21 | 12 | 20 | 0  | 7  | 6  |
   | v4 | 22 | 13 | 21 | 7  | 0  | 7  |
   | v5 | 15 | 6  | 14 | 6  | 7  | 0  |

   ```{dot}
   graph G {
    graph[rankdir=LR]
    node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
    edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
    ranksep=0.25
    subgraph cluster_rhs {
     fontname="Courier-Bold"
     fontsize=10
     label="v5 balded"
     v0 -- i0 [label=11]
     v1 -- i0 [label=2]
     v2 -- i0 [label=10]
     i0 -- i2 [label=4]
     i2 -- i1 [label=3]
     i1 -- v3 [label=3]
     i1 -- v4 [label=4]
     i2 -- v5 [label=0 style=dashed]
    }
   }
   ```

   ```{note}
   Technically, an edge weight of 0 is a violation of the simple tree requirement of having edge weights > 0. This is a special case.
   ```

   ```{note}
   How do you know the limb length from just the distance matrix? See the algorithm to determine limb length for any leaf from just the distance matrix.
   ```
   
   `{bm-enable} 5'` <!-- Re-enabling. Needed to be disabled because v3's is conflicting with 3' -->

 * `{bm} additive phylogeny` - A recursive algorithm that finds the unique simple tree for some additive distance matrix. The algorithm `{bm-target} trim/trimmed distance matrix`s a single leaf node at each recursive step until the distance matrix has a size of two. The simple tree for any two leaf nodes is those two nodes connected by a single edge. Using that tree as its base, the algorithm recurses out of each step by finding where that step's trimmed node exists on the tree and attaching it on.
 
   At the end, the algorithm will have constructed the entire simple tree for the additive distance matrix. For example, ...
   
   * Initial distance matrix ...

     |    | v0 | v1 | v2 | v3 |
     |----|----|----|----|----|
     | v0 | 0  | 13 | 21 | 22 |
     | v1 | 13 | 0  | 12 | 13 |
     | v2 | 21 | 12 | 0  | 13 |
     | v3 | 22 | 13 | 13 | 0  |
   
   * Trim v1 to produce distance matrix ...
   
     |    | v0 | v2 | v3 |
     |----|----|----|----|
     | v0 | 0  | 21 | 22 |
     | v2 | 21 | 0  | 13 |
     | v3 | 22 | 13 | 0  |
   
   * Trim v0 to produce distance matrix ...
   
     |    | v2 | v3 |
     |----|----|----|
     | v2 | 0  | 13 |
     | v3 | 13 | 0  |
   
   * Distance matrix maps to the obvious simple tree...
   
     ```{dot}
     graph G {
      graph[rankdir=LR]
      node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
      edge[fontname="Courier-Bold", fontsize=10]
      v2
      v3
      v3 -- v2 [label="13.0"]
     }
     ```
   
   * Attach v0 to produce tree...
   
     ```{dot}
     graph G {
      graph[rankdir=LR]
      node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
      edge[fontname="Courier-Bold", fontsize=10]
      N1
      v0
      v2
      v3
      v3 -- N1 [label="7.0"]
      N1 -- v2 [label="6.0"]
      N1 -- v0 [label="15.0"]
     }
     ```
   
   
   * Attach v1 to produce tree...
   
     ```{dot}
     graph G {
      graph[rankdir=LR]
      node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
      edge[fontname="Courier-Bold", fontsize=10]
      N1
      N2
      v0
      v1
      v2
      v3
      v3 -- N1 [label="7.0"]
      N1 -- v2 [label="6.0"]
      v0 -- N2 [label="11.0"]
      N2 -- N1 [label="4.0"]
      N2 -- v1 [label="2.0"]
     }
     ```

   ```{note}
   See Algorithms/Phylogeny/Distance Matrix to Tree/Additive Phylogeny Algorithm_TOPIC for a full explanation of how this algorithm works.
   ```

 * `{bm} sum of squared errors/(sum of squared errors|sum of square error|sum of errors squared)/i` - Sum of errors squared is an algorithm used to quantify how far off some estimation / prediction is.
 
   Given a set of real values and a set of predicted values, the error is the difference between the real and predicted values at each data point. For example...

   |           |   |    |   |   |   |   |
   |-----------|---|----|---|---|---|---|
   | Real      | 5 | 4  | 7 | 8 | 5 | 4 |
   | Predicted | 4 | 5  | 7 | 6 | 4 | 4 |
   | Error     | 1 | -1 | 0 | 2 | 1 | 0 |

   The algorithm squares each error and sums them together:

   ```python
   res = 0
   for r_val, p_val in zip(real, predicted):
     err = r_val - p_val
     res += err ** 2
   ```

   The algorithm as a formula: `{kt} \sum_{i=0}^{n}{(r_i - p_i)^2}`

 * `{bm} speciation` - The evolutionary process by which a species splits into distinct child species.

   In phylogenetic trees, internal nodes branching are assumed to be speciation events. That is, an event where the ancestral species represented by that node splits into distinct child species.

 * `{bm} unrooted binary tree` - In the context of phylogeny, an unrooted binary tree is a simple tree where internal nodes must have a degree_GRAPH of 3...

   ```{svgbob}
                        2    
                       /     
   0      1           e -- 3 
    \     |          /       
     a -- b -- c -- d        
    /          |     \       
   4           5      6      
                             
   * "Letter are internal nodes"
   * "Numbers are leaf nodes"
   ```

   In other words, an edge leading to an internal node is guaranteed to branch _exactly_ twice.

   ```{svgbob}
      YES           NO           NO

          1            1
         /            /
   0 -- a       0 -- a -- 3     0 -- 1 
         \            \
          2            2
                             
   * "Letter are internal nodes"
   * "Numbers are leaf nodes"
   ```

   Contrast that to normal simple trees where internal nodes can have any degree_GRAPH greater than 2...

   ```{svgbob}
   0   1
    \ /
     a 
    / \
   4   3
                             
   * "Letter are internal nodes"
   * "Numbers are leaf nodes"
   ```

   ```{note}
   Recall that simple trees are unrooted to begin with and can't have nodes with degree_GRAPH 2 (train of non-branching edges not allowed).
   ```

 * `{bm} rooted binary tree` - In the context of phylogeny, a rooted binary tree is an unrooted binary tree with a root node injected in between one of its edges. The injected root node will always end up as an internal node of degree_GRAPH of 2, breaking the constraint of ...

   * unrooted binary trees that states internal nodes must have degree_GRAPH of exactly 3.
   * simple trees that states internal nodes must have degree_GRAPH of greater than 2.

   ```{svgbob}
                                                                          r
                                                                         / \ 
                                                                        /   \
                        2                                              /     \
                       /                                              a       b
   0      1           e -- 3                                         / \     / \
    \     |          /             "INJECT ROOT BETWEEN (a,b)"      0   4   1   c
     a -- b -- c -- d                                                          / \ 
    /          |     \                                                        5   d
   4           5      6                                                          / \
                                                                                6   e
                                                                                   / \
                                                                                  2   3 

   * "Letter are internal nodes"
   * "Numbers are leaf nodes"
   ```

 * `{bm} ultrametric tree/(ultrametric tree|ultrametric)/i` - A rooted tree where all leaf nodes are equidistant from the root.

   ```{svgbob}
               *
              / \
             /   \
        2.5 /     \
           /       \ 3
          /         \
         *           \
        / \           \
   1.5 /   \ 1.5       *
      /     \       1 / \ 1
     /       \       /   \
    a         b     c     d
   ```

   In the example above, all leaf nodes are a distance of 4 from the root.

   ```{note}
   Does an ultrametric tree have to be a rooted binary tree? I think the answer is no: UPGMA generated rooted binary trees, but ultrametric trees in general just have to be rooted trees / they don't have to be binary.
   ```

 * `{bm} molecular clock` - The assumption that the rate of mutation is more-or-less consistent. For example, ...
   
   * every minute, around n of m nucleotides get mutated.
   * every hour, around n genome rearrangement reversals occur per chromosome segment of size m.
   * etc..
   
   This assumption is used for some phylogeny algorithms (e.g. UPGMA).

 * `{bm} unweighted pair group method with arithmetic mean (UPGMA)/(unweighted pair group method with arithmetic mean|UPGMA)/i` - A heuristic algorithm used to estimate a binary ultrametric tree for some distance matrix.

   ```{note}
   A binary ultrametric tree is an ultrametric tree where each internal node only branches to two children. In other words, a binary ultrametric tree is a rooted binary tree where all leaf nodes are equidistant from the root.
   ```

   The algorithm assumes that the rate of mutation is consistent (molecular clock). This assumption is what makes the tree ultrametric. A set of present day species (leaf nodes) are assumed to all have the same amount of mutation (distance) from their shared ancestor (shared internal node).

   ```{svgbob}
               g      <-- "shared ancestor"
              / \
             /   \
        2.5 /     \
           /       \ 3
          /         \
         f           \
        / \           \
   1.5 /   \ 1.5       e
      /     \       1 / \ 1
     /       \       /   \
    a         b     c     d      <-- "present day species"
      
   * "a, b, c, and d share ancestor g:   dist(a,g) = dist(b,g) = dist(c,g) = dist(d,g) = 4"
   ```

   ```{note}
   See Algorithms/Phylogeny/Distance Matrix to Tree/UPGMA Algorithm_TOPIC for a full explanation of how this algorithm works.
   ```

 * `{bm} neighbour joining matrix` - A matrix produced by transforming a distance matrix such that each element is calculated as total_dist(a) + total_dist(b) - (n - 2) * dist(a, b), where...

   * n is the number of leaf nodes in the distance matrix.
   * a and b are the leaf nodes being referenced in the distance matrix.
   * dist(a, b) returns the distance between leaf nodes a and b in the distance matrix.
   * total dist(a) returns the sum of all distances to / from leaf node a.
   * total dist(b) returns the sum of all distances to / from leaf node b.

   The maximum element in the neighbour joining matrix is guaranteed to be for two neighbouring leaf nodes. For example, the following distance matrix produces the following neighbour joining matrix...

   |    | v0 | v1 | v2 | v3 | v4 | v5 |
   |----|----|----|----|----|----|----|
   | v0 | 0  | 13 | 21 | 21 | 22 | 22 |
   | v1 | 13 | 0  | 12 | 12 | 13 | 13 |
   | v2 | 21 | 12 | 0  | 20 | 21 | 21 |
   | v3 | 21 | 12 | 20 | 0  | 7  | 13 |
   | v4 | 22 | 13 | 21 | 7  | 0  | 14 |
   | v5 | 22 | 13 | 21 | 13 | 14 | 0  |


   |    | v0  | v1  | v2  | v3  | v4  | v5  |
   |----|-----|-----|-----|-----|-----|-----|
   | v0 | 0   | 110 | 110 | 88  | 88  | 94  |
   | v1 | 110 | 0   | 110 | 88  | 88  | 94  |
   | v2 | 110 | 110 | 0   | 88  | 88  | 94  |
   | v3 | 88  | 88  | 88  | 0   | 122 | 104 |
   | v4 | 88  | 88  | 88  | 122 | 0   | 104 |
   | v5 | 94  | 94  | 94  | 104 | 104 | 0   |

   The maximum element is for (v3, v4), meaning that v3 and v4 are neighbouring leaf nodes.

   ```{note}
   See Algorithms/Phylogeny/Find Neighbours_TOPIC for a full explanation of how this algorithm works.
   ```

 * `{bm} neighbour joining phylogeny` - A recursive algorithm that can either...
 
   * find the unique simple tree for an additive distance matrix.
   * approximate a simple tree for a non-additive distance matrix.

   The algorithm finds and `{bm-target} replace/trimmed distance matrix`s a pair of neighbouring leaf nodes in the distance matrix with their shared parent at each recursive step (parent is promoted to a leaf node) until the distance matrix has a size of two. The simple tree for any two leaf nodes is those two nodes connected by a single edge. Using that tree as its base, the algorithm recurses out of each step by attaching the neighbours removed from the distance at that step to their parent in the tree.

   ```{note}
   The term neighbouring means having a shared parent in the tree, not next to each other in the distance matrix.
   ```

   At the end, the algorithm will have constructed the entire simple tree for the additive distance matrix. For example, ...
   
   * Initial non-additive distance matrix ...

     |    | v0 | v1 | v2 | v3 |
     |----|----|----|----|----|
     | v0 | 0  | 16 | 22 | 22 |
     | v1 | 16 | 0  | 13 | 12 |
     | v2 | 22 | 13 | 0  | 11 |
     | v3 | 22 | 12 | 11 | 0  |

   * Replace neighbours (v1, v0) with their parent N1 to produce distance matrix ...

     |    | N1  | v2 | v3 |
     |----|-----|----|----|
     | N1 | 0   | 22 | 22 |
     | v2 | 9.5 | 0  | 11 |
     | v3 | 9   | 11 | 0  |

   * Replace neighbours (v2, v3) with their parent N2 to produce distance matrix ...

     |    |  N1  |  N2  |
     |----|------|------|
     | N1 | 0    | 3.75 |
     | N2 | 3.75 | 0    |

   * Distance matrix maps to the obvious simple tree...

     ```{dot}
     graph G {
      graph[rankdir=LR]
      node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
      edge[fontname="Courier-Bold", fontsize=10]
     N1
     N2
     N2 -- N1 [label="3.75"]
     }
     ```

   * Attach (v2, v3) to N2 to produce tree...

     ```{dot}
     graph G {
      graph[rankdir=LR]
      node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
      edge[fontname="Courier-Bold", fontsize=10]
     N1
     N2
     v2
     v3
     N2 -- N1 [label="3.75"]
     N2 -- v2 [label="5.75"]
     N2 -- v3 [label="5.25"]
     }
     ```

   * Attach (v1, v0) to N1 to produce tree...

     ```{dot}
     graph G {
      graph[rankdir=LR]
      node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
      edge[fontname="Courier-Bold", fontsize=10]
     N1
     N2
     v0
     v1
     v2
     v3
     N2 -- N1 [label="3.75"]
     N2 -- v2 [label="5.75"]
     N2 -- v3 [label="5.25"]
     N1 -- v1 [label="3.25"]
     N1 -- v0 [label="12.75"]
     }
     ```

   ```{note}
   See Algorithms/Phylogeny/Distance Matrix to Tree/Neighbour Joining Phylogeny Algorithm_TOPIC for a full explanation of how this algorithm works.
   ```


 * `{bm} paleontology/(paleontology|palaeontology|palæontology)/i` - The scientific study of ancient organisms: dinosaurs, prehistoric plants, prehistoric insects, prehistoric fungi, etc...

 * `{bm} anatomy/(anatomy|anatomical)/i` - The study of the identification and description of structures in organisms.

 * `{bm} physiology/(physiology|physiological)/i` - The study of organism function.

 * `{bm} character table/(character table|character vector)/i` - A matrix where the columns represent biological entities and the rows represent characteristics of those entities, where those characteristics are typically anatomically or physiologically.

   |           | wings | sucks blood | number of legs |
   |-----------|-------|-------------|----------------|
   | house fly |   2   |     no      |       6        |
   | mosquito  |   2   |     yes     |       6        |
   | snail     |   0   |     no      |       0        |

   Character tables were commonly used for phylogeny before discovering that DNA can be used to compare the relatedness of organisms.

   A row in a character table is referred to as a character vector. Prior to the advent of sequencers, scientists would treat character vectors as sequences for generating phylogenetic trees or doing comparisons between organisms.

 * `{bm} mitochondrial DNA/(mitochondrial DNA|mtDNA)/i` - DNA unique to the mitochondria. This DNA is unique to the mitochondria, different from the DNA of the cell that the mitochondria lives in. The mitochondria is suspected of being bacteria that made it into the cell and survived, forming a symbiotic relationship.
   
   Mitochondrial DNA is inherited fully from the mother. It isn't a mix of parental DNA as the cell DNA is.

 * `{bm} small parsimony/(small parsimony|large parsimony)/i` - In the context of phylogenetic trees, ...
 
   * small parsimony: When a tree structure and its leaf node sequences are given, derive the internal node sequences with the lowest possible distance (most parsimonious).
   * large parsimony: When only the leaf node sequences are given, derive the combination of tree structure and internal node sequences with the lowest possible distance (most parsimonious).

   ```{svgbob}
   "Phylogenetic tree with ancestral sequences inferred"
            .-----------.
            | AncestorA |
            |  ATTGCC   |
            '-----+-----'
                 / \
                /   \
               /     \
        .-----+-----. \
        | AncestorB |  \  
        |  ACTGCT   |   \
        '-----+-----'    \
             / \          \
            /   \          \
           /     \          \
   .------+-. .---+----. .---+----.
   |   Cat  | |  Lion  | |  Bear  |
   | ACTGGT | | ACTGCT | | ATTCCC |
   '--------' '--------' '--------'
   ```

   Large parsimony isn't a process that's normally done because the search space explodes in size (e.g. NP-complete). Instead, small parsimony is used on a tree generated using an algorithm like UPGMA or neighbour joining phylogeny.

   ```{note}
   The parsimony score algorithm is what's typically used to evaluate how well a combination of tree structure + ancestral sequences do.
   ```

 * `{bm} parsimony score` - Given a phylogenetic tree with sequences for both leaf nodes (known entities) and internal nodes (inferred ancestral entities), the parsimony score is a measure of how far off a parent's sequence is from its children (and vice versa). The idea is that the most parsimonious evolutionary path is the one that's most likely to have occurred. As such, the less far off sequences are, the more likely it is that the actual ancestral lineage and ancestral sequences match what's depicted in the tree.

   ```{svgbob}
   "Using hamming distance as the metric, the following"
   "tree has a parsimony score of 1 + 3 + 1 = 5"

            .-----------.
            | AncestorA |
            |  ATTGCC   |
            '-----+-----'
                 / \
              3 /   \
               /     \
        .-----+-----. \
        | AncestorB |  \ 1
        |  ACTGCT   |   \
        '-----+-----'    \
             / \          \
          1 /   \ 0        \
           /     \          \
   .------+-. .---+----. .---+----.
   |   Cat  | |  Lion  | |  Bear  |
   | ACTGGT | | ACTGCT | | ATTCCC |
   '--------' '--------' '--------'
   ```

 * `{bm} Saccharomyces` - A genus of yeast used for producing alcohol and bread.

 * `{bm} diauxic shift` - A change in the metabolism of Saccharomyces cerevisiae. When glucose is present, Saccharomyces cerevisiae consumes that glucose for energy and produces ethanol as a byproduct. Once all available glucose in the environment has been depleted, it inverts its metabolism to instead consume the ethanol byproduct it produced earlier.

   The consumption of ethanol only happens in the presence of oxygen. Without oxygen, Saccharomyces cerevisiae enters hibernation until either glucose or oxygen become available. This property is what allows for the making of wine: Wine production typically involves sealed barrels that prevent oxygen from entering.

 * `{bm} whole genome duplication` `{bm} /\b(WGD)s?\b//true/true` - A rare evolutionary event in which the entire genome of an organism is duplicated.
 
   After duplication, much of the functionality provided by the genome becomes redundant. The organism evolves much more rapidly because a mutation in one copy of a gene won't necessarily make the organism less fit (duplicate copy still exists). It's typical for a whole genome duplication to be quickly followed up by massive amounts of gene mutations, gene loss, and genome rearrangements.

 * `{bm} gene expression matrix/(gene expression matrix|expression matrix|gene expression matrices|expression matrices|gene expression data|expression data|gene expression vector|expression vector)/i` - A matrix where each column represents a point in time, each row represents a gene, and each cell is a number representing the amount of gene expression taking place for that gene (row) at that time (column).

   |        | 5 AM | 6 AM | 7 AM |
   |--------|------|------|------|
   | Gene 1 | 1.0  | 1.0  | 1.0  |
   | Gene 2 | 1.0  | 0.7  | 0.5  |
   | Gene 3 | 1.0  | 1.1  | 1.4  |

   Each row in a gene expression matrix is called a gene expression vector.

 * `{bm} co-regulate` - A set of genes whose gene expression is regulated by the same transcription factor.

 * `{bm} RNA transcript/(RNA transcript|transcript)/i` - RNA output of transcription.

 * `{bm} transcriptome` - All RNA transcripts within a cell at a specific point in time.

 * `{bm} good clustering principle` - The idea that items within the same cluster should be more similar to each other than items in other clusters.

   ```{note}
   This was originally introduced as "every pair of points within the same cluster should be closer to each other than any points each from different clusters", where "closer" was implying euclidean distance. I think the idea was intended to be abstracted out to the definition above since the items may not be thought of as "points" but as vectors or sequences + you can choose a similarity metric other than euclidean distance.
   ```

 * `{bm} euclidean distance` - The distance between two points if traveling directly from one to the other in a straight line.

   ```{svgbob}
      *
       \
        \ d
         \
          * 
   ```

   In 2 dimensional space, this is calculated as `{kt} \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}`.

   In 3 dimensional space, this is calculated as `{kt} \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2 + (z_2 - z_1)^2}`.

   In n dimensional space, this is calculated as `{kt} \sqrt{\sum_{i=1}^n{(v_i - w_i)^2}}`, where v and w are two n dimensional points.

 * `{bm} manhattan distance/(manhattan distance|taxi[\s\-]?cab distance|city[\s\-]block distance)/i` - The distance between two points if traveling only via the axis of the coordinate system.

   ```{svgbob}
      *
      | 
    dx|
      |  
      +--* 
       dy
   ```

   In n dimensional space, this is calculated as `{kt} \sum_{i=1}^n{|v_i - w_i|}`, where v and w are two n dimensional points.

   ```{note}
   The name manhattan distance is an allegory to the city blocks of manhattan, where your options (most of the time) are to move either left/right or up/down. Other names for this same metric are taxi-cab distance and city block distance.
   ```

 * `{bm} clustering/(cluster)/i` - Grouping together a set of objects such that objects within the same group are more similar to each other than objects in other groups. Each group is referred to as a cluster.

 * `{bm} member/(membership|member)_CLUSTER/i` - An object assigned to a cluster is said to be a member_CLUSTER of that cluster.

 * `{bm} k-centers clustering/(k-centers? clustering|\d+-centers? clustering|k-centers?|\d+-centers?)/i` - A form of clustering where a point, called a center, defines cluster membership_NORM. k different centers are chosen (one for each cluster), and the points closest to each center (euclidean distance) make up member_CLUSTERs of that cluster. The goal is to choose centers such that, out of all possible cluster center to member_CLUSTER distances, the farthest distance is the minimum it could possibly be out of all possible choices for centers.

   In terms of a scoring function, the score being minimized is ...

   ```{kt}
   score = max(d(P_1, C), d(P_2, C), ..., d(P_n, C))
   ```

   * P is the set of points.
   * C is the set of centers.
   * n is the number of points in P
   * d returns the euclidean distance between a point and its closest center.
   * max is the maximum function.

   ```python
   # d() function from the formula
   def dist_to_closest_center(data_pt, center_pts):
     center_pt = min(
       center_pts,
       key=lambda cp: dist(data_pt, cp)
     )
     return dist(center_pt, data_pt)
   
   # scoring function (what's trying to be minimized)
   def k_centers_score(data_pts, center_pts):
     return max(dist_to_closest_center(p, center_pts) for p in data_pts)
   ```

   ```{svgbob}
   "Points represented as letters, where each letter"
   "represents the cluster its assigned to. Each line is"
   "from a point to its cluster center."
   
              "bad centers"                                 "good centers"     
                                                                                    
   |    C                                        |    C                             
   |     \                                       |    |                             
   |C ----●                                      |C --●                             
   |     /                                       |    |                             
   |    C                                        |    C                             
   |                                             |                                  
   |                                             |                                  
   |                                             |                                  
   |           ●                                 |                                  
   |          /|\                                |                           
   |         / | \                               |                           
   |        D  |  D                              |        D     D                    
   |           |                                 |         '. .'                    
   |           |                                 |           ●                      
   |           |                                 |           |                      
   |           D                                 |           D                      
   +----------------------------------           +----------------------------------
   ```

   For a non-trivial input, the search space is too massive for a straight-forward algorithm to work. As such, heuristics are commonly used instead.

   ```{note}
   See farthest first traversal heuristic.
   ```

 * `{bm} farthest first traversal` - A heuristic commonly used for k-centers clustering. The algorithm iteratively builds out more centers by inspecting the euclidean distances from points to existing centers. At each step, the algorithm ...

   1. gets the closest center for each point,
   1. picks the point with the farthest euclidean distance and sets it as the new center.

   The algorithm initially primes the list of centers with a randomly chosen point and stops executing once it has k points.

   ```{svgbob}
   "k=3"
   " * Points represented as letters, where the letter denotes cluster assignment."
   " * Points chosen as centers are in brackets."
   
          "step1: pick random initial"                    "step2: pick next farthest"                       "step3: pick next farthest"
                                                                                                                                            
   |                                                |                                                |                                      
   |                                                |                                                |                                      
   |                                                |                                                |                                      
   |                                                |                                                |                                      
   |                  D                             |                  C                             |                  C                   
   |                 D   D                          |                 C  [C]                         |                 C  [C]               
   |    D              D                            |    D              C                            |    D              C                  
   |       D                                        |       D                                        |       D                              
   |  [D]   D                                       |  [D]   D                                       |  [D]   D                             
   |       D        D                               |       D        C                               |       D        E                     
   |   D  D        D   D                            |   D  D        C   C                            |   D  D        E   E                  
   |                  D                             |                  C                             |                 [E]                  
   |                                                |                                                |                                      
   |                                                |                                                |                                      
   |                                                |                                                |                                      
   |                                                |                                                |                                      
   +--------------------------------------          +--------------------------------------          +--------------------------------------
   ```

 * `{bm} k-means clustering/(k-means?|\d+-means?|squared error distortion)/i` - A form of clustering where a point, called a center, defines cluster membership_NORM. k different centers are chosen (one for each cluster), and the points closest to each center (euclidean distance) make up member_CLUSTERs of that cluster. The goal is to choose centers such that, out of all possible cluster center to member_CLUSTER distances, the formula below is the minimum it could possibly be out of all possible choices for centers.
 
   The formula below is referred to as squared error distortion.

   ```{kt}
   score = \frac{\sum_{i=1}^{n} {d(P_i, C)^2}}{n}
   ```
   
    * P is the set of points.
    * C is the set of centers.
    * n is the number of points in P
    * d returns the euclidean distance between a point and its closest center.
    * max is the maximum function.

   ```python
   # d() function from the formula
   def find_closest_center(data_pt, center_pts):
     center_pt = min(
       center_pts,
       key=lambda cp: dist(data_pt, cp)
     )
     return center_pt, dist(center_pt, data_pt)

   # scoring function (what's trying to be minimized) -- taking squares of d() and averaging
   def squared_error_distortion(data_pts, center_pts):
     res = []
     for data_pt in data_pts:
       closest_center_pt, dist_to = find_closest_center(data_pt, center_pts)
       res.append(dist_to ** 2)
     return sum(res) / len(res)
   ```

   Compared to k-centers, k-means more appropriately handles outliers. If outliers are present, k-centers's metric causes the cluster center to be wildly offset while k-mean's metric will only be mildly offset. In the example below, the best scoring cluster center for k-centers is wildly offset by outlier Z while k-means isn't offset as much.

   ```{svgbob}
   .-------------------.       .-------------------.       .-------------------.
   |    "no outlier"   |       |   "k-means w/ Z"  |       |  "k-centers w/ Z" |
   |                   |       |                   |       |                   |
   |        K          |       |         K         |       |          K        |
   |                   |       |                   |       |                   |
   |     J  ●  L       |       |      J     L      |       |       J     L     |
   '-------------------'       |                   |       |                   |
                               |         ●         |       |                   |
                               |                   |       |                   |
                               |                   |       |                   |
                               |                   |       |                   |
                               |                   |       |          ●        |
                               |                   |       |                   |
                               |                   |       |                   |
                               |                   |       |                   |
                               |                   |       |                   |
                               |                   |       |                   |
                               |                   |       |                   |
                               |                   |       |                   |
                               |         Z         |       |          Z        |
                               '-------------------'       '-------------------'
   ```

   For a non-trivial input, the search space is too massive for a straight-forward algorithm to work. As such, heuristics are commonly used instead.

   ```{note}
   See Lloyd's algorithm.
   ```

   ```{note}
   The Pevzner book states that k-means clustering often doesn't produce good results if the clumps have a non-globular shape (e.g. elongated) or have widely different densities. This probably applies to k-centers as well
   ```

 * `{bm} Lloyd's algorithm/(lloyd algorithm|lloyd's algorithm|k-means?\+\+ initializer|k-means?\+\+)/i` - A heuristic for determining centers in k-means clustering. The algorithm begins by choosing k arbitrary points from the points being clustered as the initial centers, then ...
 
   1. derives clusters from centers: Each point is assigned to its nearest center (ties broken arbitrarily).

   2. derives centers from clusters: Each center is updated to be the "center of gravity" of its points.

      The center of gravity for a set of points is the average of each individual coordinate. For example, for the 2D points (0,5), (1,3), and (2,2), the center of gravity is (1, 3.3333). The ...
   
      * first coordinate is calculated as `0+1+2/3 = 1`.
      * second coordinate is calculated as `5+3+2/3 = 3.3333`.

      ```python
      def center_of_gravity(data_pts, dim):
         center = []
         for i in range(dim):
           val = mean(pt[i] for pt in data_pts)
           center.append(val)
         return center
      ```

   The above two steps loop repeatedly until the new centers are the same as the centers from the previous iteration (stops converging).

   Since this algorithm is a heuristic, it doesn't always converge to a good solution. The algorithm typically runs multiple times, where the run producing centers with the lowest squared error distortion is accepted. An enhancement to the algorithm, called k-means++ initializer, increases the chances of converging to a good solution by _probabilistically_ selecting initial centers that are far from each other:
   
   1. The 1st center is chosen from the list of points at random.
   2. The 2nd center is chosen by selecting a point that's likely to be much farther away from center 1 than most other points.
   3. The 3rd center is chosen by selecting a point that's likely to be much farther away from center 1 and 2 than most other points.
   4. ...

   The probability of selecting a point as the next center is proportional to its squared distance to the existing centers.

   ```python
   def k_means_PP_initializer(data_pts, k):
     centers = [random.choice(data_pts)]
     while len(centers) < k:
       choice_points = []
       choice_weights = []
       for pt in data_pts:
         if pt in centers:
           continue
         _, d = find_closest_center(pt, centers)
         choice_weights.append(d)
         choice_points.append(pt)
       total = sum(choice_weights)
       choice_weights = [w / total for w in choice_weights]
       c_pt = random.choices(choice_points, weights=choice_weights, k=1).pop(0)
       centers.append(c_pt)
     return centers
   ```

 * `{bm} hard clustering \/ soft clustering/(hard clustering|soft clustering)/i` - In the context of clustering, ...
 
   * soft clustering algorithms assign each object to a set of probabilities, where each probability is how likely it is for that object to be assigned to a cluster.

     ```{svgbob}
          ●                                                                      ●       
     "A=0.9,B=0.1"                                                          "A=0.1,B=0.9"
                                                                                         
             ●                                ●                              ●       
        "A=0.9,B=0.1"                    "A=0.5,B=0.5"                  "A=0.1,B=0.9"
                                                                                         
          ●                                                                      ●       
     "A=0.9,B=0.1"                                                          "A=0.1,B=0.9"
     ```

   * hard clustering algorithms assign each object to exactly one cluster.

     ```{svgbob}
          ●                                                                      ●       
          A                                                                      B 
                                                                                         
             ●                                ●                              ●       
             A                                B                              B 
                                                                                         
          ●                                                                      ●       
          A                                                                      B
     ```

 * `{bm} dot product` - Given two equal sized vectors, the dot product of those vectors is calculated by first multiplying the pair at each index, then summing the result of those multiplications together. For example, the dot product (1, 2, 3) and (4, 5, 6) is 1\*4+2\*5+3\*6.

   The notation for dot product is a central dot in between the two vector: `{kt} a \cdot b`.

   ```{note}
   Central dot is also commonplace for standard multiplication.

   In geometry, the dot product of two vectors is used to get the angle between those vectors.
   ```

 * `{bm} conditional probability` - The probability of an event occurring given that another event has already occurred.

   The notation for conditional probability is Pr(B|A), where B is the event occurring and A is the event that's already occurred.
   
   If B and A are...
    * independent events, Pr(B|A) is simply Pr(B).
    * dependent events, Pr(B|A) is calculated as the probability that both B and A happen divided by the probability that just A happens: Pr(A∩B) / Pr(A).

 * `{bm} similarity metric` - A metric used to measure how similar a pair of entities are to each other. Whereas a distance metric must start at 0 for total similarity and grows based on how different the entities are, a similarity metric has no requirements for bounds on similarity or dissimilarity. Examples of similarity metrics include ...

   * pearson similarity for gene expression vectors.
   * cosine similarity for gene expression vectors.
   * BLOSUM / PAM matrices for protein sequence alignments.
   * etc..

   ```{note}
   This topic was only briefly discussed, so I don't know for sure what the properties/requirements are for a similarity metric other than higher = more similar. Contrast this to distance metrics, where it explicitly mentions the requirements that need to be followed (e.g. triangle inequality property). For similarity metrics, it didn't say if there's some upper-bound to similarity or if totally similar entities have to score the same. For example, does `similarity(snake,snake) == similarity(bird,bird)` have to be true or can it be that `similarity(snake,snake) > similarity(bird,bird)`?
   
   I saw on Wikipedia that sequence alignment scoring matrices like PAM and BLOSUM are similarity matrices, so that implies that totally similar entities don't have to be the same score. For example, in BLOSUM62 `similarity(A,A) = 4` but `similarity(R,R) = 5`.

   Also, does a similarity metric have to be symmetric? For example, `similarity(snake,bird) == similarity(bird,snake)`. I think it does have to be symmetric.
   ```

 * `{bm} similarity matrix/(similarity matrix|similarity matrices)/i` - Given a set of n different entities, a similarity matrix is an n-by-n matrix where each element contains the similarity measure between the entities for that cell. For example, for the species snake, lizard, bird, and crocodile ...

   |           | Snake | Lizard | Bird | Crocodile |
   |-----------|-------|--------|------|-----------|
   | Snake     |  1.0  |  0.8   | 0.4  |    0.6    |
   | Lizard    |  0.8  |  1.0   | 0.4  |    0.6    |
   | Bird      |  0.4  |  0.4   | 1.0  |    0.5    |
   | Crocodile |  0.6  |  0.6   | 0.5  |    1.0    |

   ```{note}
   This topic was only briefly discussed, so I have no idea what properties are required other than: 0 = completely dissimilar / orthogonal and anything higher than that is more similar. It didn't say if there's some upper-bound to similarity or if totally similar entities have to score the same. For example, does `similarity(snake,snake) == similarity(bird,bird)` have to be true or can it be that `similarity(snake,snake) > similarity(bird,bird)`? I saw on Wikipedia that sequence alignment scoring matrices like PAM and BLOSUM are similarity matrices, so that implies that totally similar entities don't have to be the same score. For example, in BLOSUM62 `similarity(A,A) = 4` but `similarity(R,R) =5`.

   There may be other properties involved, such as how the triangle inequality property is a thing for distance matrices / distance metrics.
   ```

 * `{bm} pearson correlation coefficient/(pearson correlation coefficient|pearson correlation|pearson distance|pearson similarity)/i` - A metric used to quantify how correlated two vectors are.

   ```{kt}
   \frac{
     \sum_{i=1}^{m}(x_i-avg(x))\cdot(y_i-avg(y))
   }{
     \sqrt{
       \sum_{i=1}^{m}(x_i-avg(x))^2\cdot\sum_{i=1}^{m}(y_i-avg(y))^2
     }
   }
   ```

   In the above formula, x and y are the two input vectors and avg is the average function. The result of the formula is a number between -1 and 1, where ...

   * -1 represents a total negative correlation.
   * 0 represents no correlation.
   * 1 represents a total positive correlation.

   The formula may be modified to become a distance metric as follows: `1 - pearson_correlation(x, y)`. Whereas the pearson correlation coefficient varies between -1 and 1, the pearson distance varies between 0 (totally similar) and 2 (totally dissimilar).

 * `{bm} similarity graph` - A transformation of a similarity matrix into a graph, where the entities that make up the similarity matrix are represented as nodes and edges between nodes are only made if the similarity exceeds a certain threshold.

   The similarity graph below was generated using the accompanying similarity matrix and threshold of 7.

   |   | a | b | c | d | e | f | g |
   |---|---|---|---|---|---|---|---|
   | a | 9 | 8 | 9 | 1 | 0 | 1 | 1 |
   | b | 8 | 9 | 9 | 1 | 1 | 0 | 2 |
   | c | 9 | 9 | 8 | 2 | 1 | 1 | 1 |
   | d | 1 | 1 | 2 | 9 | 8 | 9 | 9 |
   | e | 0 | 1 | 1 | 8 | 8 | 8 | 9 |
   | f | 1 | 0 | 1 | 9 | 8 | 9 | 9 |
   | g | 1 | 2 | 1 | 9 | 9 | 9 | 8 |

   ```{svgbob}
   "Only similarities of > 7 have an edge."

   g---e
   |\ /|
   | X |
   |/ \|
   d---f   c
          / \
         a---b
   ```

   Similarity graphs are used for clustering (e.g. gene expression vectors). Assuming clusters exist and the similarity metric used captures them, there should be some threshold where the edges produced in the similarity graph form cliques as in the example above.
   
   Since real-world data often has complications (e.g. noisy) / the similarity metric used may have complications, it could be that corrupted cliques are formed instead. Heuristic algorithms are often used to correct corrupted cliques.

   ```{svgbob}
   *---*      
   |\ /|\     
   | X | \    
   |/ \|  \   
   *   *   *  
          / \ 
         *   *
   ```

 * `{bm} clique` - A set of nodes in a graph where every possible node pairing has an edge.

   ```{svgbob}
   *---*
   |\ /|
   | X |
   |/ \|
   *---*
   ``` 

 * `{bm} corrupted clique` - A set of nodes and edges in a graph that almost form a clique. Some edges may be missing or extraneous.

   ```{svgbob}
   "CORRUPTED CLIQUES"            "CLIQUES"
   
       *---*                     *---*      
       |\ /|\                    |\ /|      
       | X | \                   | X |      
       |/ \|  \                  |/ \|      
       *   *   *                 *---*   *
              / \                       / \ 
             *   *                     *---*
   ```

 * `{bm} clique graph` - A graph consisting only of cliques.

   ```{svgbob}
   "Graph with 2 cliques"

     *
    / \     *---*
   *---*    |\ /|
            | X |
            |/ \|
            *---*
   ``` 

 * `{bm} cluster affinity search technique` `{bm} /(CAST)/` - A heuristic algorithm that corrects the corrupted cliques in a similarity graph.
 
    ```{svgbob}
   "CORRUPTED CLIQUES"            "CLIQUES"
   
       *---*                     *---*      
       |\ /|\                    |\ /|      
       | X | \                   | X |      
       |/ \|  \                  |/ \|      
       *   *   *                 *---*   *
              / \                       / \ 
             *   *                     *---*
   ```
   
   The algorithm attempts to re-create each corrupted clique in its corrected form by iteratively finding the ...
 
   1. closest node not in the clique/cluster and including it _if it exceeds the similarity graph threshold_.
   2. farthest node within the clique/cluster and removing it _if it doesn't exceed the similarity graph threshold_.
   
   How close or far a gene is from the clique/cluster is defined as the average similarity between that node and all nodes in the clique/cluster.

   While the similarity graph has nodes, the algorithm picks the node with the highest degree_GRAPH from the similarity graph to prime a clique/cluster. It then loops the add and remove process described above until there's an iteration where nothing changes. At that point, that cluster/clique is said to be consistent and its nodes are removed from the original similarity graph. 

   ```{svgbob}
   "original:"

     a---d
    /|\  |
   t | \ |
     |  \|
     b---c
    
   

   "step1:"            "step2:"            "step3:"
   "prime with a"      "add t"             "add b, remove t"

     a                   a                   a
                        /                    |
                       t                     |
                                             |
                                             b


   "step4:"            "step4:"            "step5:   (done)"
   "add c"             "add d"             "nothing to add/remove"
                       
     a                   a---d               a---d
     |\                  |\ /|               |\ /|
     | \                 | X |               | X |
     |  \                |/ \|               |/ \|
     b---c               b---c               b---c
   ```

 * `{bm} RNA sequencing` `{bm} /(RNA-Seq)/` - A technique which uses next-generation sequencing to reveal the presence and quantity of RNA in a biological sample at some given moment.

 * `{bm} hierarchical cluster` - A form of tiered clustering where clusters are represented as a tree. Each node represents a cluster (leaf nodes being a cluster of size 1), where the clusters represented by a parent node is the combination of the clusters represented by its children.

   ```{svgbob}
                                 |
                     .-----------*-----------.
                     |                       |
         .-----------*----------.            |
         |                      |            |
   .-----*-----.                |            |
   |           |                |            |
   |       .---*---.       .----*---.    .---*---.
   |       |       |       |        |    |       |
   |    .--*--.    |    .--*--.     |    |    .--*--.
   |    |     |    |    |     |     |    |    |     |  
   g9   g4    g2   g1   g6    g10   g7   g8   g5    g3
   ```

   ```{note}
   Hierarchical clustering has its roots in phylogeny. The similarity metric to build clusters is massaged into a distance metric, which is then used to form a tree that represents the clusters.
   ```

 * `{bm} cosine similarity/(cosine similarity|cosine distance)/i` - A similarity metric that measures if two vectors grew/shrunk in a similar trajectories (similar angles).

   ```{svgbob}
                                            .'
                                          .'
           /                            .'
          /                           .'
         /                          .'
      T /                         .'
       /                  /     .' 
      / 20             A / 20 .'  B
     /   .'             /   .' 
    /  .'              /  .'     
     .' U               .'   
   .'                 .'       
   ```

   The metric computes the trajectory as the cosine of an angle between vectors. In the example above, T and U have different magnitudes than A and B, but the angle between T and U is exactly the same as the angle between A and B: 20deg. The cosine similarity of both pairs is cos(20deg) = 0.939. Had the angle been ...

   * smaller (more similar trajectory), the cosine would get closer to 1.
   * larger (less similar trajectory), the cosine would get closer to -1.

   The formula may be modified to become a distance metric as follows: `1 - cosine_similarity(x, y)`. Whereas the cosine similarity varies between -1 and 1, the cosine distance varies between 0 (totally similar) and 2 (totally dissimilar).

 * `{bm} dendrogram` - A diagram of a tree. The term is most often used in the context of hierarchical clustering, where the tree that makes up the hierarchy of clusters is referred to as a dendrogram.

   ```{svgbob}
         |           
   .-----*-----.     
   |           |     
   |       .---*---. 
   |       |       | 
   |    .--*--.    | 
   |    |     |    | 
   g9   g4    g2   g1
   ```

   ```{note}
   It's tough to get a handle on what the requirements are, if any, to call a tree a dendrogram: Is it restricted to 2 children per internal node (or can there be more)? Do the edges extending from an internal node have to be of equal weight (e.g. equidistant)? Does the tree have to be ultrametric? Does it have to be a rooted tree (or can it be an unrooted tree)?

   It seems like you can call any tree, even unrooted trees, a dendrogram. This seems like a gate keeping term. "Draw the tree that makes up the hierarchical cluster" vs "Draw the dendrogram that makes up the hierarchical cluster".
   ```

 * `{bm} differential gene expression/(differential expression|differential gene expression)/i` - Given a set of transcriptome snapshots, where each snapshot is for the same species but in a different state, differential gene expression analyzes transcript abundances across the transcriptomes to see ...
 
   1. which genes are responsible for / influenced by the state,
   2. what the pattern of gene expression change is in those genes (transcript abundances).

   For example, differential expression analysis may be used to compare cancerous and non-cancerous blood cells to identify which genes are responsible for the cancer and their gene expression levels.

   |          | patient1 (cancer) | patient2 (cancer) | patient3 (non-cancer) | ... |
   |----------|-------------------|-------------------|-----------------------|-----|
   | Gene A   | 100               | 100               | 100                   | ... |
   | Gene B   | 100               | 110               | 50                    | ... |
   | Gene C   | 100               | 110               | 140                   | ... |
   | ...      | ...               | ...               | ...                   | ... |

   In the example above, gene B has roughly double the expression when cancerous.

   ```{note}
   Recall that genes are transcribed from DNA to mRNA, then translated to a protein. A transcript in a transcriptome is essentially a gene currently undergoing the process of gene expression.
   ```

   ```{note}
   I suspect the term transcript abundance is used instead of transcript count because oftentimes the counts are processed / normalized into some other form in an effort to denoise / de-bias (RNA sequencing is a noisy process).
   ```
 


`{bm-ignore} \b(read)_NORM/i`
`{bm-error} Apply suffix _NORM or _SEQ/\b(read)/i`

`{bm-ignore} \b(membership|member)_NORM/i`
`{bm-error} Apply suffix _NORM, _MOTIF, or _CLUSTER/\b(membership|member)/i`

`{bm-ignore} (balanced)_NORM/i`
`{bm-error} Apply suffix _NORM, _GRAPH, or _NODE/(balanced)/i`

`{bm-ignore} (coverage)_NORM/i`
`{bm-error} Apply suffix _NORM or _SEQ/(coverage)/i`

`{bm-ignore} (fragment)_NORM/i`
`{bm-error} Apply suffix _NORM or _SEQ/(fragment)/i`

`{bm-ignore} (Eulerian)_NORM/i`
`{bm-error} Apply suffix _PATH, _CYCLE, _GRAPH, or _NORM/(Eulerian)/i`
`{bm-error} Don't use a suffix here/(eulerian_PATH path|eulerian_CYCLE cycle|eulerian_GRAPH graph)/i`

`{bm-ignore} (spectrum)_NORM/i`
`{bm-error} Apply suffix _NORM or _MS/(spectrum)/i`

`{bm-ignore} (adjacent|adjacency|adjacencies|breakpoint)_NORM/i`
`{bm-error} Apply suffix _NORM or _GR/(adjacent|adjacency|adjacencies|breakpoint)/i`
`{bm-error} Use breakpoint graph_GR instead/(breakpoint_GR graph)/i`

`{bm-ignore} (permutation)_NORM/i`
`{bm-error} Apply suffix _NORM or _GR/(permutation)/i`

`{bm-ignore} (degree)_NORM/i`
`{bm-error} Apply suffix _NORM or _GRAPH/(degree)/i`

`{bm-error} Did you mean central dogma of molecular biology? You wrote microbiology./(central dogma of microbiology)/i`

`{bm-error} Did you mean neighbour joining matrix?/(neighbouring join matrix|neighbouring joining matrix|neighbouring-join matrix|neighbouring-joining matrix)/i`

`{bm-error} Did you mean co-regulate? (needs a dash)/(coregulate)/i`

`{bm-error} Did you mean noisy?/(noisey)/i`

`{bm-error} Did you mean hierarchiCal? The spell checker messes it up sometimes./(hierarchial)/i`

`{bm-error} Did you mean oftentimes (no space))?/(often times)/i`

`{bm-error} Missing topic reference/(_TOPIC)/i`
`{bm-error} Use you instead of we/\b(we)\b/i`