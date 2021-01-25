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

Never the less, in an ideal world where most of these problems don't exist, an overlap graph is a good way to guess the single-strand of DNA that a set of fragment_SEQs came from. An overlap graph assumes that the fragment_SEQs it's operating on ...

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

Never the less, in an ideal world where most of these problems don't exist, a de Bruijn graph is a good way to guess the single-strand of DNA that a set of fragment_SEQs came from. A de Bruijn graph assumes that the fragment_SEQs it's operating on ...

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

K and GA both have a mass of 128Da. Since, experimental spectrums don't distinguish between where masses come from, an experimental spectrum for this linear peptide will only have 1 entry for 128Da.

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

This algorithm extends the bruteforce algorithm into a more efficient branch-and-bound algorithm by adding one extra step: After each branch, any candidates peptides deemed to be untenable are discarded. In this case, untenable means that there's no chance / little chance of the peptide branching out to a correct solution.

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

    Complete graph               Example alignment 1           Example alignment 2
                                       M-APLE                        MAPLE
                                       -TABLE                        TABLE

   T   A   B   L   E             T   A   B   L   E             T   A   B   L   E  
 o-->o-->o-->o-->o-->o         o   o   o   o   o   o         o   o   o   o   o   o
 |\  |\  |\  |\  |\  |         |                              \                   
M| \ | \ | \ | \ | \ |        M|                            M  \                  
 |  \|  \|  \|  \|  \|         |                                \                 
 v   v   v   v   v   v         v                                 v                
 o-->o-->o-->o-->o-->o         o-->o   o   o   o   o         o   o   o   o   o   o
 |\  |\  |\  |\  |\  |              \                             \               
A| \ | \ | \ | \ | \ |        A      \                      A      \              
 |  \|  \|  \|  \|  \|                \                             \             
 v   v   v   v   v   v                 v                             v            
 o-->o-->o-->o-->o-->o         o   o   o   o   o   o         o   o   o   o   o   o
 |\  |\  |\  |\  |\  |                  \                             \           
P| \ | \ | \ | \ | \ |        P          \                  P          \          
 |  \|  \|  \|  \|  \|                    \                             \         
 v   v   v   v   v   v                     v                             v        
 o-->o-->o-->o-->o-->o         o   o   o   o   o   o         o   o   o   o   o   o
 |\  |\  |\  |\  |\  |                      \                             \       
L| \ | \ | \ | \ | \ |        L              \              L              \      
 |  \|  \|  \|  \|  \|                        \                             \     
 v   v   v   v   v   v                         v                             v    
 o-->o-->o-->o-->o-->o         o   o   o   o   o   o         o   o   o   o   o   o
 |\  |\  |\  |\  |\  |                          \                             \   
E| \ | \ | \ | \ | \ |        E                  \          E                  \  
 |  \|  \|  \|  \|  \|                            \                             \ 
 v   v   v   v   v   v                             v                             v
 o-->o-->o-->o-->o-->o         o   o   o   o   o   o         o   o   o   o   o   o
```

The example above is just one of many sequence alignment types. There are different types of alignment graphs, applications of alignment graphs, and different scoring models used in bioinformatics.

```{note}
The Pevzner book mentions a non-biology related problem to help illustrate alignment graphs: the Manhattan Tourist problem. Look it up if you're confused.
```

### Find Maximum Path

**WHAT**: Given an arbitrary directed acyclic graph where each edge has a weight, find the path with the maximum weight between two nodes.

**WHY**: Finding a maximum path between nodes is fundamental to sequence alignments. That is, regardless of what type of sequence alignment is being performed, at its core it boils down to finding the maximum weight between two nodes in the alignment graph.

#### Bruteforce Algorithm

**ALGORITHM**:

The following algorithm finds a maximum path in the most obvious way: iterate over all paths in the graph and pick the one with the highest weight. It's too slow to be used on anything but small graphs.

```{output}
ch5_code/src/FindMaxPath_Bruteforce.py
python
# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN
```

```{ch5}
FindMaxPath_Bruteforce
A B 1, A C 1, B C 1, C D 1, C E 1
A
E
```

# Stories

## Bacterial Genome Replication

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

## Non-ribosomal Peptides

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

NRPs may be `{bm-target} cyclic/(cyclopeptide|cyclic peptide)/i`. Common use-cases for NRPs:

 * antibiotics
 * anti-tumor agents
 * immunosuppressors
 * communication between bacteria (quorum sensing)

```{note}
According to the Wikipedia article on NRPs, there exist a wide range of peptides that are not synthesized by ribosomes but the term non-ribosomal peptide typically refers to the ones synthesized by NRP synthetases.
```

### Find Sequence

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
 
   Unless you're dealing with hard logical statements where prior occurrences don't come in to play (e.g. 1+1=2), you should include a small chance that some extremely unlikely event may happen. The example tossed around is "the probability that the sun will not rise tomorrow." Prior recorded observations show that sun has always risen, but that doesn't mean that there's a 1.0 probability of the sun rising tomorrow (e.g. some extremely unlikely cataclysmic event may prevent the sun from rising).

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

 * `{bm} genome` - All of the DNA for some organism.

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

 * `{bm} experimental spectrum` - List of potential fragment_NORM masses derived from a spectrum_MS. That is, the molecules fed into the mass spectrometer were randomly fragment_NORMed and each fragment_NORM had its mass-to-charge ratio measured. From there, each mass-to-charge ratio was converted a set of potential masses.
 
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
      T   A   B   L   E
    o-->o-->o-->o-->o-->o
    |\  |\  |\  |\  |\  |   "* each diagonal edge is a replacement / keep matching"
   M| \ | \ | \ | \ | \ |   "* each horizontal edge is an indel where the top is kept"
    |  \|  \|  \|  \|  \|   "* each vertical edge is an indel where the left is kept"
    v   v   v   v   v   v
    o-->o-->o-->o-->o-->o   
    |\  |\  |\  |\  |\  |
   A| \ | \ | \ | \ | \ |
    |  \|  \|  \|  \|  \|
    v   v   v   v   v   v
    o-->o-->o-->o-->o-->o
    |\  |\  |\  |\  |\  |
   P| \ | \ | \ | \ | \ |
    |  \|  \|  \|  \|  \|
    v   v   v   v   v   v
    o-->o-->o-->o-->o-->o
    |\  |\  |\  |\  |\  |
   L| \ | \ | \ | \ | \ |
    |  \|  \|  \|  \|  \|
    v   v   v   v   v   v
    o-->o-->o-->o-->o-->o
    |\  |\  |\  |\  |\  |
   E| \ | \ | \ | \ | \ |
    |  \|  \|  \|  \|  \|
    v   v   v   v   v   v
    o-->o-->o-->o-->o-->o
   ```

   A path in this graph from source (top-left) to sink (bottom-right) represents an alignment.

 * `{bm} alignment path/(sequence alignment graph path|sequence alignment path|alignment graph path|alignment path)/i` - A path in an alignment graph that represents one possible sequence alignment. For example, given the following alignment path ...
   
   ```{svgbob}
      T   A   B   L   E
    o-->o-->o   o   o   o
            |                 "* each diagonal edge is a replacement / keep matching"
   M        |                 "* each horizontal edge is an indel where the top is kept"
            |                 "* each vertical edge is an indel where the left is kept"
            v
    o   o   o   o   o   o   
             \
   A          \
               \
                v
    o   o   o   o   o   o
                 \
   P              \
                   \
                    v
    o   o   o   o   o-->o
                        |
   L                    |
                        |
                        v
    o   o   o   o   o   o
                        |
   E                    |
                        |
                        v
    o   o   o   o   o   o
   ```

   is represent as the alignment...

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

 * `{bm} dynamic programming/(dynamic programming algorithm|dynamic programming)/i` - An algorithm that solves a problem by recursively breaking it down into smaller sub-problems, where the result of each recurrence computation is stored in some lookup table such that it can be re-used if it were ever encountered again (essentially trading space for speed). The lookup table may be created before hand or as a cache that gets filled as the algorithm runs.
 
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

 * `{bm} manhattan tourist problem` - The Manhattan tourist problem is an allegory to help explain sequence alignment graphs. Where as in sequence alignments you're finding a path through the graph from source to sink that has the maximum weight, in the Manhattan tourist problem you're finding a path from 59th St and 8th Ave to 42nd St and 3rd Ave with the most tourist sights to see. It's essentially the same problem as global alignment: 
 
   * The graph is the street layout of Manhattan.
   * The only options at each intersection are to move right or down.
   * The source node is the intersection of 59th St and 8th Ave.
   * The sink node is the intersection of 42nd St and 3rd Ave.
   * The number of tourist sights from one intersection to the next is the weight of an edge.


   ```{svgbob}
           8   7   6   5           3
                         
           A   A   A   A           A
           v   v   v   v           v
           e   e   e   e           e
         o-->o-->o-->o-->o- - - -o-->o
         |   |   |   |   |       |   |
   59 St |   |   |   |   |       |   |
         |   |   |   |   |       |   |
         v   v   v   v   v       v   v
         o-->o-->o-->o-->o- - - -o-->o
         |   | T |   | T |       |   |
   57 St |   |   |   |   |       |   |
         |   |   |   |   |       |   |
         v   v   v   v   v       v   v
         o-->o-->o-->o-->o- - - -o-->o
         |   |   |   |   |       |   |
   55 St |   |  T|   |   |       |   |
         |   |   |   |   |       |   |
         v   v   v   v   v       v   v
         o-->o-->o-->o-->o- - - -o-->o
         |   |   |   |   |       |   |
   53 St |   |   |   |   |       |   |
         |   |   |   |   |       |   |
         v   v   v   v   v       v   v
         o-->o-->o-->o-->o- - - -o-->o
         |   |   |   | T |       |   |
   51 St |   |   |   |   |       |   |
         |   |   |   |   |       |   |
         v   v   v   v   v       v   v
         o-->o-->o-->o-->o- - - -o-->o
         :   :   :   :   :       :   :
         :   :   :   :   :       :   :
         :   :   :   :   :       :   :
         :   :   :   :   :       :   :
         :   :   :   :   :       :   :
         v   v   v   v   v       v   v
         o-->o-->o-->o-->o- - - -o-->o
         | T |   |   |   |       |   |
   43 St |   |   |   |   |       |   |
         |   |   |   |   |       |   |
         v   v   v T v   v       v   v
         o-->o-->o-->o-->o- - - -o-->o
         |   |   |   |   |       |   |
   42 St |   |   |   |   |       |   |
         |   |   |   |   |       |   |
         v   v   v   v   v       v   v
         o-->o-->o-->o-->o- - - -o-->o
   ```

 * `{bm} point accepted mutation/(point accepted mutation|percent accepted mutation)/i` `{bm} /\b(PAM)\d*\b//false/true` - A scoring matrix used for sequence alignments of proteins. The scoring matrix is calculated by inspecting / extrapolating mutations as homologous proteins evolve. Specifically, mutations in the DNA sequence that encode some protein may change the resulting amino acid sequence for that protein. Those mutations that...

    * impair the ability of the protein to function aren't likely to survive, and as such are given a low score. 
    * keep the protein functional are likely to survive, and as such are given a normal or high score.
 
   PAM matrices are developed iteratively. An initial PAM matrix is calculated by aligning extremely similar protein sequences using a simple scoring model (1 for match, 0 for mismatch / indel). That sequence alignment then provides the scoring model for the next iteration. For example, the alignment for the initial iteration may have determined that D may be a suitable substitution for W. As such, the sequence alignment for the next iteration will score more than 0 (e.g. 1) if it encounters D being compared to W.

   Other factors are also brought into the mix when developing scores for PAM matrices. For example, the ...

    * likelihood of amino acid mutations (e.g. Cys and Trp are the least mutable amino acids).
    * speed of evolution (e.g. some mutations were more probably in species 100 million years ago vs 1 million years ago).

   It's said that PAM is focused on tracking the evolutionary origins of proteins. Sequences that are 99% similar are said to be 1 PAM unit diverged, where a PAM unit is the amount of time it takes an "average" protein to mutate 1% of its amino acids. PAM1 (the initial scoring matrix) was defined by performing many sequence alignments between proteins that are 99% similar (1 PAM unit diverged).

   ```{note}
   [Here](http://www.compbio.dundee.ac.uk/papers/rev93_1/subsection3_3_5.html) and [here](https://en.wikipedia.org/w/index.php?title=Point_accepted_mutation&oldid=1002281881#Comparing_PAM_and_BLOSUM) both seem to say that BLOSUM supersedes PAM as a scoring matrix for protein sequences.

   > Although both matrices produce similar scoring outcomes they were generated using differing methodologies. The BLOSUM matrices were generated directly from the amino acid differences in aligned blocks that have diverged to varying degrees the PAM matrices reflect the extrapolation of evolutionary information based on closely related sequences to longer timescales

   > Henikoff and Henikoff [16] have compared the BLOSUM matrices to PAM, PET, Overington, Gonnet [17] and multiple PAM matrices by evaluating how effectively the matrices can detect known member_NORMs of a protein family from a database when searching with the ungapped local alignment program BLAST [18]. They conclude that overall the BLOSUM 62 matrix is the most effective.
   ```

   PAM250 is the most commonly used variant:

   |   |  A |  R |  N |  D |  C |  Q |  E |  G |  H |  I |  L |  K |  M |  F |  P |  S |  T |  W |  Y |  V |  B |  Z |  X |  - |
   |---|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
   | A |  2 | -2 |  0 |  0 | -2 |  0 |  0 |  1 | -1 | -1 | -2 | -1 | -1 | -3 |  1 |  1 |  1 | -6 | -3 |  0 |  0 |  0 |  0 | -8 |
   | R | -2 |  6 |  0 | -1 | -4 |  1 | -1 | -3 |  2 | -2 | -3 |  3 |  0 | -4 |  0 |  0 | -1 |  2 | -4 | -2 | -1 |  0 | -1 | -8 |
   | N |  0 |  0 |  2 |  2 | -4 |  1 |  1 |  0 |  2 | -2 | -3 |  1 | -2 | -3 |  0 |  1 |  0 | -4 | -2 | -2 |  2 |  1 |  0 | -8 |
   | D |  0 | -1 |  2 |  4 | -5 |  2 |  3 |  1 |  1 | -2 | -4 |  0 | -3 | -6 | -1 |  0 |  0 | -7 | -4 | -2 |  3 |  3 | -1 | -8 |
   | C | -2 | -4 | -4 | -5 | 12 | -5 | -5 | -3 | -3 | -2 | -6 | -5 | -5 | -4 | -3 |  0 | -2 | -8 |  0 | -2 | -4 | -5 | -3 | -8 |
   | Q |  0 |  1 |  1 |  2 | -5 |  4 |  2 | -1 |  3 | -2 | -2 |  1 | -1 | -5 |  0 | -1 | -1 | -5 | -4 | -2 |  1 |  3 | -1 | -8 |
   | E |  0 | -1 |  1 |  3 | -5 |  2 |  4 |  0 |  1 | -2 | -3 |  0 | -2 | -5 | -1 |  0 |  0 | -7 | -4 | -2 |  3 |  3 | -1 | -8 |
   | G |  1 | -3 |  0 |  1 | -3 | -1 |  0 |  5 | -2 | -3 | -4 | -2 | -3 | -5 |  0 |  1 |  0 | -7 | -5 | -1 |  0 |  0 | -1 | -8 |
   | H | -1 |  2 |  2 |  1 | -3 |  3 |  1 | -2 |  6 | -2 | -2 |  0 | -2 | -2 |  0 | -1 | -1 | -3 |  0 | -2 |  1 |  2 | -1 | -8 |
   | I | -1 | -2 | -2 | -2 | -2 | -2 | -2 | -3 | -2 |  5 |  2 | -2 |  2 |  1 | -2 | -1 |  0 | -5 | -1 |  4 | -2 | -2 | -1 | -8 |
   | L | -2 | -3 | -3 | -4 | -6 | -2 | -3 | -4 | -2 |  2 |  6 | -3 |  4 |  2 | -3 | -3 | -2 | -2 | -1 |  2 | -3 | -3 | -1 | -8 |
   | K | -1 |  3 |  1 |  0 | -5 |  1 |  0 | -2 |  0 | -2 | -3 |  5 |  0 | -5 | -1 |  0 |  0 | -3 | -4 | -2 |  1 |  0 | -1 | -8 |
   | M | -1 |  0 | -2 | -3 | -5 | -1 | -2 | -3 | -2 |  2 |  4 |  0 |  6 |  0 | -2 | -2 | -1 | -4 | -2 |  2 | -2 | -2 | -1 | -8 |
   | F | -3 | -4 | -3 | -6 | -4 | -5 | -5 | -5 | -2 |  1 |  2 | -5 |  0 |  9 | -5 | -3 | -3 |  0 |  7 | -1 | -4 | -5 | -2 | -8 |
   | P |  1 |  0 |  0 | -1 | -3 |  0 | -1 |  0 |  0 | -2 | -3 | -1 | -2 | -5 |  6 |  1 |  0 | -6 | -5 | -1 | -1 |  0 | -1 | -8 |
   | S |  1 |  0 |  1 |  0 |  0 | -1 |  0 |  1 | -1 | -1 | -3 |  0 | -2 | -3 |  1 |  2 |  1 | -2 | -3 | -1 |  0 |  0 |  0 | -8 |
   | T |  1 | -1 |  0 |  0 | -2 | -1 |  0 |  0 | -1 |  0 | -2 |  0 | -1 | -3 |  0 |  1 |  3 | -5 | -3 |  0 |  0 | -1 |  0 | -8 |
   | W | -6 |  2 | -4 | -7 | -8 | -5 | -7 | -7 | -3 | -5 | -2 | -3 | -4 |  0 | -6 | -2 | -5 | 17 |  0 | -6 | -5 | -6 | -4 | -8 |
   | Y | -3 | -4 | -2 | -4 |  0 | -4 | -4 | -5 |  0 | -1 | -1 | -4 | -2 |  7 | -5 | -3 | -3 |  0 | 10 | -2 | -3 | -4 | -2 | -8 |
   | V |  0 | -2 | -2 | -2 | -2 | -2 | -2 | -1 | -2 |  4 |  2 | -2 |  2 | -1 | -1 | -1 |  0 | -6 | -2 |  4 | -2 | -2 | -1 | -8 |
   | B |  0 | -1 |  2 |  3 | -4 |  1 |  3 |  0 |  1 | -2 | -3 |  1 | -2 | -4 | -1 |  0 |  0 | -5 | -3 | -2 |  3 |  2 | -1 | -8 |
   | Z |  0 |  0 |  1 |  3 | -5 |  3 |  3 |  0 |  2 | -2 | -3 |  0 | -2 | -5 |  0 |  0 | -1 | -6 | -4 | -2 |  2 |  3 | -1 | -8 |
   | X |  0 | -1 |  0 | -1 | -3 | -1 | -1 | -1 | -1 | -1 | -1 | -1 | -1 | -2 | -1 |  0 |  0 | -4 | -2 | -1 | -1 | -1 | -1 | -8 |
   | - | -8 | -8 | -8 | -8 | -8 | -8 | -8 | -8 | -8 | -8 | -8 | -8 | -8 | -8 | -8 | -8 | -8 | -8 | -8 | -8 | -8 | -8 | -8 |    |

   ```{note}
   The above matrix was extracted from [here](https://swift.cmbi.umcn.nl/teach/aainfo/pam250.shtml). The indel scores on that matrix are set to -8, but I've also seen them set to -5. I don't know if PAM250 defines a constant for indels?
   ```

 * `{bm} blocks amino acid substitution matrix/(blocks substitution matrix|blocks substitution matrices|blocks amino acid substitution matrices|blocks amino acid substitution matrix)/i` `{bm} /\b(BLOSUM)\d*\b//false/true` - A scoring matrix used for sequence alignments of proteins. The scoring matrix is calculated by scanning a protein database for highly conserved regions between similar proteins, where the mutations between those highly conserved regions define the scores. Specifically, those highly conserved regions are identified based on local alignments without support for indels (gaps not allowed). Non-matching positions in that alignment define potentially acceptable mutations.

   Several sets of BLOSUM matrices exist, each identified by a different number. This number defines the similarity of the sequences used to create the matrix: The protein database sequences used to derive the matrix are filtered such that only those with >= n% similarity are used, where n is the number. For example, ...
   
    * BLOSUM80 is created from sequences that are >= 80% similar.
    * BLOSUM45 is created from sequences that are >= 45% similar.
    
   As such, BLOSUM matrices with higher numbers are designed to compare more closely related sequences while those with lower numbers are designed to score more distant related sequences.

   BLOSUM62 is the most commonly used variant since "experimentation has shown that it's among the best for detecting weak similarities":

   |   |  A |  R |  N |  D |  C |  Q |  E |  G |  H |  I |  L |  K |  M |  F |  P |  S |  T |  W |  Y |  V |  B |  Z |  X |  - |
   |---|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
   | A |  4 | -1 | -2 | -2 |  0 | -1 | -1 |  0 | -2 | -1 | -1 | -1 | -1 | -2 | -1 |  1 |  0 | -3 | -2 |  0 | -2 | -1 |  0 | -4 | 
   | R | -1 |  5 |  0 | -2 | -3 |  1 |  0 | -2 |  0 | -3 | -2 |  2 | -1 | -3 | -2 | -1 | -1 | -3 | -2 | -3 | -1 |  0 | -1 | -4 | 
   | N | -2 |  0 |  6 |  1 | -3 |  0 |  0 |  0 |  1 | -3 | -3 |  0 | -2 | -3 | -2 |  1 |  0 | -4 | -2 | -3 |  3 |  0 | -1 | -4 | 
   | D | -2 | -2 |  1 |  6 | -3 |  0 |  2 | -1 | -1 | -3 | -4 | -1 | -3 | -3 | -1 |  0 | -1 | -4 | -3 | -3 |  4 |  1 | -1 | -4 | 
   | C |  0 | -3 | -3 | -3 |  9 | -3 | -4 | -3 | -3 | -1 | -1 | -3 | -1 | -2 | -3 | -1 | -1 | -2 | -2 | -1 | -3 | -3 | -2 | -4 | 
   | Q | -1 |  1 |  0 |  0 | -3 |  5 |  2 | -2 |  0 | -3 | -2 |  1 |  0 | -3 | -1 |  0 | -1 | -2 | -1 | -2 |  0 |  3 | -1 | -4 | 
   | E | -1 |  0 |  0 |  2 | -4 |  2 |  5 | -2 |  0 | -3 | -3 |  1 | -2 | -3 | -1 |  0 | -1 | -3 | -2 | -2 |  1 |  4 | -1 | -4 | 
   | G |  0 | -2 |  0 | -1 | -3 | -2 | -2 |  6 | -2 | -4 | -4 | -2 | -3 | -3 | -2 |  0 | -2 | -2 | -3 | -3 | -1 | -2 | -1 | -4 | 
   | H | -2 |  0 |  1 | -1 | -3 |  0 |  0 | -2 |  8 | -3 | -3 | -1 | -2 | -1 | -2 | -1 | -2 | -2 |  2 | -3 |  0 |  0 | -1 | -4 | 
   | I | -1 | -3 | -3 | -3 | -1 | -3 | -3 | -4 | -3 |  4 |  2 | -3 |  1 |  0 | -3 | -2 | -1 | -3 | -1 |  3 | -3 | -3 | -1 | -4 | 
   | L | -1 | -2 | -3 | -4 | -1 | -2 | -3 | -4 | -3 |  2 |  4 | -2 |  2 |  0 | -3 | -2 | -1 | -2 | -1 |  1 | -4 | -3 | -1 | -4 | 
   | K | -1 |  2 |  0 | -1 | -3 |  1 |  1 | -2 | -1 | -3 | -2 |  5 | -1 | -3 | -1 |  0 | -1 | -3 | -2 | -2 |  0 |  1 | -1 | -4 | 
   | M | -1 | -1 | -2 | -3 | -1 |  0 | -2 | -3 | -2 |  1 |  2 | -1 |  5 |  0 | -2 | -1 | -1 | -1 | -1 |  1 | -3 | -1 | -1 | -4 | 
   | F | -2 | -3 | -3 | -3 | -2 | -3 | -3 | -3 | -1 |  0 |  0 | -3 |  0 |  6 | -4 | -2 | -2 |  1 |  3 | -1 | -3 | -3 | -1 | -4 | 
   | P | -1 | -2 | -2 | -1 | -3 | -1 | -1 | -2 | -2 | -3 | -3 | -1 | -2 | -4 |  7 | -1 | -1 | -4 | -3 | -2 | -2 | -1 | -2 | -4 | 
   | S |  1 | -1 |  1 |  0 | -1 |  0 |  0 |  0 | -1 | -2 | -2 |  0 | -1 | -2 | -1 |  4 |  1 | -3 | -2 | -2 |  0 |  0 |  0 | -4 | 
   | T |  0 | -1 |  0 | -1 | -1 | -1 | -1 | -2 | -2 | -1 | -1 | -1 | -1 | -2 | -1 |  1 |  5 | -2 | -2 |  0 | -1 | -1 |  0 | -4 | 
   | W | -3 | -3 | -4 | -4 | -2 | -2 | -3 | -2 | -2 | -3 | -2 | -3 | -1 |  1 | -4 | -3 | -2 | 11 |  2 | -3 | -4 | -3 | -2 | -4 | 
   | Y | -2 | -2 | -2 | -3 | -2 | -1 | -2 | -3 |  2 | -1 | -1 | -2 | -1 |  3 | -3 | -2 | -2 |  2 |  7 | -1 | -3 | -2 | -1 | -4 | 
   | V |  0 | -3 | -3 | -3 | -1 | -2 | -2 | -3 | -3 |  3 |  1 | -2 |  1 | -1 | -2 | -2 |  0 | -3 | -1 |  4 | -3 | -2 | -1 | -4 | 
   | B | -2 | -1 |  3 |  4 | -3 |  0 |  1 | -1 |  0 | -3 | -4 |  0 | -3 | -3 | -2 |  0 | -1 | -4 | -3 | -3 |  4 |  1 | -1 | -4 | 
   | Z | -1 |  0 |  0 |  1 | -3 |  3 |  4 | -2 |  0 | -3 | -3 |  1 | -1 | -3 | -1 |  0 | -1 | -3 | -2 | -2 |  1 |  4 | -1 | -4 | 
   | X |  0 | -1 | -1 | -1 | -2 | -1 | -1 | -1 | -1 | -1 | -1 | -1 | -1 | -1 | -2 |  0 |  0 | -2 | -1 | -1 | -1 | -1 | -1 | -4 | 
   | - | -4 | -4 | -4 | -4 | -4 | -4 | -4 | -4 | -4 | -4 | -4 | -4 | -4 | -4 | -4 | -4 | -4 | -4 | -4 | -4 | -4 | -4 | -4 |    | 

   ```{note}
   The above matrix was extracted from [here](https://www.ncbi.nlm.nih.gov/Class/FieldGuide/BLOSUM62.txt). The indel scores on that matrix are set to -4, but I've also seen them set to -5. I don't know if BLOSUM62 defines a constant for indels?
   ```

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

`{bm-ignore} (spectrum)_NORM/i`
`{bm-error} Apply suffix _NORM, _MS/(spectrum)/i`

`{bm-error} Did you mean central dogma of molecular biology? You wrote microbiology./(central dogma of molecular microbiology)/i`

`{bm-error} Missing topic reference/(_TOPIC)/i`
`{bm-error} Use you instead of we/\b(we)\b/i`