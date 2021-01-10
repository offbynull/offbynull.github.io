`{title} Anki`

`{anki}` offbynull anki -- JS must be enabled.<br/>`{ankiInfoPanel}`

```{comment}
The anki inline tag injects a special anki JS into the HTML. The anki JS will treat the items in the first
bullet list as anki cloze words questions.

The anki* inline tags generate HTML spans/divs with special class names that get processed by the anki JS:

ankiInfoPanel - Information about the question / questions / state. One allowed in entire file.
   ankiAnswer - Regex answer for the current question. Multiple allowed per question.
                  Text in question that matches the regex will be blacked out and users must answer them. The
                  content of this tag are the same as a 2 or 3 parameter bm tag WITHOUT the label. For
                  example...
                  `{ankiAnswer}one`
                  `{ankiAnswer}(two)/i`
                  The label (parameter 1 of the 3 parameter tag) isn't used.
     ankiHide - Regex hider for the current question. Multiple allowed per question.
                  Text in question that matches the regex will be blacked out. The content of this tag are the
                  same as the ankiAnswer tag. For example...
                  `{ankiHide}one`
                  `{ankiHide}(two)/i`
                  The label (parameter 1 of the 3 parameter tag) isn't used.
     ankiDead - Marks a question as dead / to be skipped. One allowed per question. 
```

 * Question 1 one and two. `{ankiAnswer}one` `{ankiAnswer}two`  `{ankiDead}`

 * Question 2 two. `{ankiAnswer}two` `{ankiDead}`

 * Question 3 three. The word red should be hidden. `{ankiAnswer}three` `{ankiHide}red` `{ankiDead}`

 * Question 4 four and beep or boop. `{ankiAnswer}four` `{ankiAnswer}beep` `{ankiAnswer}boop` `{ankiDead}`

 * `{ankiAnswer} (k-mer|kmer)/i`
 
   A substring of length k within some larger biological sequence (e.g. DNA or amino acid chain). For example, in the DNA sequence GAAATC, the following k-mer's exist:

   | k | k-mers          |
   |---|-----------------|
   | 1 | G A A A T C     |
   | 2 | GA AA AA AT TC  |
   | 3 | GAA AAA AAT ATC |
   | 4 | GAAA AAAT AATC  |
   | 5 | GAAAT AAATC     |
   | 6 | GAAATC          |

 * `{ankiAnswer} (kd-mer|kdmer|\(k,\s*d\)-mer)/i` `{ankiHide} (\(\d+,\s*\d+\)-mer)/i`
   
   A substring of length 2k + d within some larger biological sequence (e.g. DNA or amino acid chain) where the first k elements and the last k elements are known but the d elements in between isn't known.
 
   When identifying a kd-mer with a specific k and d, the proper syntax is (k, d)-mer. For example, (1, 2)-mer represents a kd-mer with k=1 and d=2. In the DNA sequence GAAATC, the following (1, 2)-mer's exist: `G--A`, `A--T`, `A--C`.

 * `{ankiAnswer} (5'|5 prime)/i` `{ankiAnswer} (3'|3 prime)/i`
 
   5' (5 prime) and 3' (3 prime) describe the opposite ends of DNA. The chemical structure at each end is what defines if it's 5' or 3' -- each end is guaranteed to be different from the other. The forward direction on DNA is defined as 5' to 3', while the backwards direction is 3' to 5'.

   Two complementing DNA strands will always be attached in opposite directions.
 
   ```{svgbob}
        forward
       --------->
   ? -+-+-+-+-+-+-+- ?
       | | | | | | |
   ? -+-+-+-+-+-+-+- ?
       <---------
        backward
   ```

 * `{ankiAnswer} DNA polymerase`
 
   An enzyme that replicates a strand of DNA. That is, DNA polymerase walks over a single strand of DNA bases (not the strand of base pairs) and  generates a strand of complements. Before DNA polymerase can attach itself and start replicating DNA, it requires a primer.
 
 
   ```{svgbob}
                           G <- C <- T <- T <- T <- T <- G <- . . .
                           |                            
              <-------- .- | ----------.                    
   5' . . . A -> A -> A -> C -> G -> A -> A -> A -> A -> C -> . . . 3'
                        `--------------`                    
   
                    "Forward direction of DNA:"         5' -----> 3'
                    "? moves in the reverse direction:" 5' <----- 3'
   ```
 
   DNA polymerase is unidirectional, meaning that it can only walk a DNA strand in one direction: reverse (3' to 5') 

 * `{ankiAnswer} replication fork`
 
   The process of DNA replication requires that DNA's 2 complementing strands be unwound and split open. The area where the DNA starts to  split is called the replication fork. In bacteria, the replication fork starts at the replication origin and keeps expanding until it reaches the replication terminus.  Special enzymes called DNA polymerases walk over each unwound strand and create complementing strands.
 
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
 
 * `{ankiAnswer} replication origin` `{ankiAnswer} ori`
 
   The point in DNA at which replication starts. May be shortened to ori.
 
 * `{ankiAnswer} replication terminus` `{ankiAnswer} ter`
   
   The point in DNA at which replication ends. May be shortened to ter.

 * `{ankiAnswer} forward half-strand` `{ankiAnswer} (reverse half-strand|backward half-strand|backwards half-strand)/i` `{ankiAnswer} lagging half-strand` `{ankiAnswer} leading half-strand`
 
   Bacteria are known to have a single chromosome of circular / looping DNA. In this DNA, the replication origin (ori) is the region of DNA where replication starts, while the replication terminus (ter) is where replication ends.

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

   Given the 2 strands tha make up a DNA molecule, the strand that goes in the...

   * forward half-strand (5' to 3') is called the lagging half-strand.
   * reverse half-strand (3' to 5') is called the leading half-strand.

   This nomenclature has to do with DNA polymerase. Since DNA polymerase can only walk in the reverse direction (3' to 5'), it synthesizes the leading half-strand in one shot. For the lagging half-strand (5' to 3'), multiple DNA polymerases have to used to synthesize DNA, each binding to the lagging strand and walking backwards a small amount to generate a small fragment of DNA (Okazaki fragment). the process is much slower for the lagging half-strand, that's why it's called lagging.

 * `{ankiAnswer} Okazaki fragment`
 
   A small fragment of DNA generated by DNA polymerase for forward half-strands. DNA synthesis for the forward half-strands can only happen in small pieces. As the fork open ups every ~2000 nucleotides, DNA polymerase attaches to the end of the fork on the forward half-strand and walks in reverse to generate that small segment (DNA polymerase can only walk in the reverse direction).

 * `{ankiAnswer} DNA ligase`
 
    An enzyme that sews together short segments of DNA called Okazaki fragments by binding the phosphate group on the end of one strand with the deoxyribose group on the other strand.

 * `{ankiAnswer} DnaA box`
 
   A sequence in the ori that the DnaA protein (responsible for DNA replication) binds to.

 * `{ankiAnswer} reverse complement`
 
   Two strands of DNA bound together, where each strand is the reverse complement of the other.

   ```{svgbob}
   3' . . . T <- T <- T <- G <- C <- T <- T <- T <- T <- G <- . . . 5'
            |    |    |    |    |    |    |    |    |    | 
   5' . . . A -> A -> A -> C -> G -> A -> A -> A -> A -> C -> . . . 3'    
   ```

 * `{ankiAnswer} gene`
 
   A segment of DNA that contains the instructions for either a protein or functional RNA.

 * `{ankiAnswer} gene product`
   
   The final synthesized material resulting from the instructions that make up a gene. That synthesized material either being a protein or functional RNA.

 * `{ankiAnswer} (transcription|transcribed|transcribe)/i`
 
   The process of copying a gene to mRNA. Specifically, the enzyme RNA polymerase copies the segment of DNA that makes up that gene to a strand of RNA.

   ```{svgbob}
        +--> mRNA
   DNA -+
        +--> "functional RNA"
   ```

 * `{ankiAnswer} (translation|translated|translate)/i`
   
   The process of turning mRNA to protein. Specifically, a ribosome takes in the mRNA generated by transcription and outputs the protein that it codes for.

   ```{svgbob}
        +--> mRNA ---> protein
   DNA -+
   ```

 * `{ankiAnswer} gene expression`
 
   The process by which a gene is synthesized into a gene product. When the gene product is...

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


 * `{ankiAnswer} (regulatory gene|regulatory protein)/i`
 
   The proteins encoded by these genes effect gene expression for certain other genes. That is, a regulatory protein can cause certain other genes to be expressed more (promote gene expression) or less (repress gene expression).

   Regulatory genes are often controlled by external factors (e.g. sunlight, nutrients, temperature, etc..)

 * `{ankiAnswer} negative feedback loop` `{ankiAnswer} positive feedback loop` `{ankiAnswer} feedback loop`
 
   A feedback loop is a system where the output (or some part of the output) is fed back into the system to either promote or repress further outputs.

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

 * `{ankiAnswer} (circadian clock|circadian oscillator)/i`
 
   A biological clock that synchronizes roughly around the earth's day-night cycle. This internal clock helps many species regulate their physical and behavioural attributes. For example, hunt during the night vs sleep during the day (e.g. nocturnal owls).

 * `{ankiAnswer} upstream region`
 
   The area just before some interval of DNA. Since the direction of DNA is 5' to 3', this area is towards the 5' end (upper end).

 * `{ankiAnswer} downstream region`
   
   The area just after some interval of DNA. Since the direction of DNA is 5' to 3', this area is towards the 3' end (lower end).

 * `{ankiAnswer} transcription factor`
 
   A regulatory protein that controls the rate of transcription for some gene that it has influence over (the copying of DNA to mRNA). The protein binds to a specific sequence in the gene's upstream region.

 * `{ankiAnswer} motif`
 
   A pattern that matches against many different k-mers, where those matched k-mers have some shared biological significance. The pattern matches a fixed k where each position may have alternate forms. The simplest way to think of a motif is a regex pattern without quantifiers. For example, the regex `[AT]TT[GC]C` may match to ATTGC, ATTCC, TTTGC, and TTTCC.

 * `{ankiAnswer} motif member`
 
   A specific nucleotide sequence that matches a motif. For example, given a motif represented by the regex `[AT]TT[GC]C`, the sequences ATTGC, ATTCC, TTTGC, and TTTCC would be its motif members.

 * `{ankiAnswer} (motif matrix|motif matrices)/i`
 
   A set of k-mers stacked on top of each other in a matrix, where the k-mers are either...

   * motif members of the same motif,
   * or suspected motif members of the same motif.
   
   For example, the motif `[AT]TT[GC]C` has the following matrix:

   |0|1|2|3|4|
   |-|-|-|-|-|
   |A|T|T|G|C|
   |A|T|T|C|C|
   |T|T|T|G|C|
   |T|T|T|C|C|

 * `{ankiAnswer} regulatory motif`
 
   The motif of a transcription factor, typically 8 to 12 nucleotides in length.

 * `{ankiAnswer} transcription factor binding site`
 
   The physical binding site for a transcription factor. A gene that's regulated by a transcription factor needs a sequence located in its upstream region that the transcription factor can bind to: a motif member of that transcription factor's regulatory motif.

   ```{note}
   A gene's upstream region is the 600 to 1000 nucleotides preceding the start of the gene.
   ```

 * `{ankiAnswer} (cDNA|complementary DNA)/i`
 
   A single strand of DNA generated from mRNA. The enzyme reverse transcriptase scans over the mRNA and creates the complementing single DNA strand.

   ```{svgbob}
   3' . . . U <- U <- U <- G <- C <- U <- U <- U <- U <- G <- . . . 5'   mRNA  
            |    |    |    |    |    |    |    |    |    | 
   5' . . . A -> A -> A -> C -> G -> G -> A -> A -> A -> C -> . . . 3'   ?  
   ```

   The mRNA portion breaks off, leaving the single-stranded DNA.

   ```{svgbob}
   5' . . . A -> A -> A -> C -> G -> G -> A -> A -> A -> C -> . . . 3'   ?  
   ```

 * `{ankiAnswer} (DNA microarray|DNA array)/i`
 
   A device used to compare gene expression. This works by measuring 2 mRNA samples against each other: a control sample and an experimental sample. The samples could be from...
 
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

 * `{ankiAnswer} greedy algorithm`
 
   An algorithm that tries to speed things up by taking the locally optimal choice at each step. That is, the algorithm doesn't look more than 1 step ahead.
 
   For example, imagine a chess playing AI that had a strategy of trying to eliminate the other player's most valuable piece at each turn. It would be considered greedy because it only looks 1 move ahead before taking action. Normal chess AIs / players look many moves ahead before taking action. As such, the greedy AI may be fast but it would very likely lose most matches. 
  
 * `{ankiAnswer} (Cromwell'?s? rule)/i`
 
   When a probability is based off past events, 0.0 and 1.0 shouldn't be used. That is, if you've...
 
   * never seen an even occur in the past, it doesn't mean that there's a 0.0 probability of it occurring next.
   * always seen an event occur in the past, it doesn't mean that there's a 1.0 probability of it occurring next.
 
   Unless you're dealing with hard logical statements where prior occurrences don't come in to play (e.g. 1+1=2), you should include a small chance that some extremely unlikely event may happen. The example tossed around is "the probability that the sun will not rise tomorrow." Prior recorded observations show that sun has always risen, but that doesn't mean that there's a 1.0 probability of the sun rising tomorrow (e.g. some extremely unlikely cataclysmic event may prevent the sun from rising).

 * `{ankiAnswer} (Laplace'?s? rule of succession|Laplace'?s? rule)/i`
 
   If some independent true/false event occurs n times, and s of those n times were successes, it's natural for people to assume the probability of success is `{kt} \frac{s}{n}`. However, if the number of successes is 0, the probability would be 0.0. Cromwell's rule states that when a probability is based off past events, 0.0 and 1.0 shouldn't be used. As such, a more appropriate / meaningful measure of probability is `{kt} \frac{s+1}{n+2}`.

   For example, imagine you're sitting on a park bench having lunch. Of the 8 birds you've seen since starting your lunch, all have been pigeons. If you were to calculate the probability that the next bird you'll see a crow, `{kt} \frac{0}{8}` would be flawed because it states that there's no chance that the next bird will be a crow (there obviously is a chance, but it may be a small chance). Instead, applying Laplace's rule allows for the small probability that a crow may be seen next: `{kt} \frac{0+1}{8+2}`.

   Laplace's rule of succession is more meaningful when the number of trials (n) is small.

 * `{ankiAnswer} pseudocount`
 
   When a zero is replaced with a small number to prevent unfair scoring. See Laplace's rule of succession.

 * `{ankiAnswer} Las Vegas algorithm`
 
   A randomized algorithm that delivers a guaranteed exact solution. That is, even though the algorithm makes random decisions it is guaranteed to converge on the exact solution to the problem its trying to solve (not an approximate solution).

   An example of a Las Vegas algorithm is randomized quicksort (randomness is applied when choosing the pivot).

 * `{ankiAnswer} Monte Carlo algorithm`
 
   A randomized algorithm that delivers an approximate solution. Because these algorithms are quick, they're typically run many times. The approximation considered the best out of all runs is the one that gets chosen as the solution.

   An example of a Monte Carlo algorithm is a genetic algorithm to optimize the weights of a deep neural network. That is, a step of the optimization requires running n different neural networks to see which gives the best result, then replacing those n networks with n copies of the best performing network where each copy has randomly tweaked weights. At some point the algorithm will stop producing incrementally better results.

   Perform the optimization (the entire thing, not just a single step) thousands of times and pick the best network.
  
 * `{ankiAnswer} (consensus string|consensus sequence|consensus)/i`
 
   The k-mer generated by selecting the most abundant column at each index of a motif matrix.

   |         |0|1|2|3|4|
   |---------|-|-|-|-|-|
   |k-mer 1  |A|T|T|G|C|
   |k-mer 2  |A|T|T|C|C|
   |k-mer 3  |T|T|T|G|C|
   |k-mer 4  |T|T|T|C|C|
   |k-mer 5  |A|T|T|C|G|
   |consensus|A|T|T|C|C|

   The generated k-mer may also use a hybrid alphabet. The consensus string for the same matrix above using IUPAC nucleotide codes: `WTTSS`.

 * `{ankiAnswer} entropy`
   
   The uncertainty associated with a random variable. Given some set of outcomes for a variable, it's calculated as `{kt} -\sum_{i=1}^{n} P(x_i) log P(x_i)`.

   This definition is for information theory. In other contexts (e.g. physics, economics), this term has a different meaning.

 * `{ankiAnswer} genome`
 
   All of the DNA for some organism.

 * `{ankiAnswer} sequence`
 
   The ordered elements that make up some biological entity. For example, a ...

   * DNA sequence contains the set of nucleotides and their positions for that DNA strand.
   * peptide sequence contains the set of amino acids and their positions for that peptide.

 * `{ankiAnswer} (sequencing|sequenced)/i`
 
   The process of determining which nucleotides are assigned to which positions in a strand of DNA or RNA.

   The machinery used for DNA sequencing is called a sequencer. A sequencer takes multiple copies of the same DNA, breaks that DNA up into smaller fragments, and scans in those fragments. Each fragment is typically the same length but has a unique starting offset. Because the starting offsets are all different, the original larger DNA sequence can be guessed at by finding fragment with overlapping regions and stitching them together.

   |             |0|1|2|3|4|5|6|7|8|9|
   |-------------|-|-|-|-|-|-|-|-|-|-|
   |read 1       | | | | |C|T|T|C|T|T|
   |read 2       | | | |G|C|T|T|C|T| |
   |read 3       | | |T|G|C|T|T|C| | |
   |read 4       | |T|T|G|C|T|T| | | |
   |read 5       |A|T|T|G|C|T| | | | |
   |reconstructed|A|T|T|G|C|T|T|C|T|T|

 * `{ankiAnswer} sequencer`
 
   A machine that performs DNA or RNA sequencing.

 * `{ankiAnswer} (sequencing error|sequencer error)/i`
 
   An error caused by a sequencer returning a fragment where a nucleotide was misinterpreted at one or more positions (e.g. offset 3 was actually a C but it got scanned in as a G).

   ```{note}
   This term may also be used in reference to homopolymer errors, known to happen with nanopore technology. From [here](https://news.ycombinator.com/item?id=25459670)...

   > A homopolymer is when you have stretches of the same nucleotide, and the error is miscounting the number of them. e.g: GAAAC could be called as "GAAC" or "GAAAAC" or even "GAAAAAAAC".
   ```

 * `{ankiAnswer} read`
 
   A segment of genome scanned in during the process of sequencing.

 * `{ankiAnswer} (read-pair|read pair)/i`
 
   A segment of genome scanning in during the process of sequencing, where the middle of the segment is unknown. That is, the first k elements and the last k elements are known, but the d elements in between aren't known. The total size of the segment is 2k + d.

   Sequencers provide read-pairs as an alternative to longer reads because the longer a read is the more errors it contains.

   See kd-mer.

 * `{ankiAnswer} fragment`
 
   A scanned sequence returned by a sequencer. Represented as either a read or a read-pair.

 * `{ankiAnswer} (assembly|assemble)/i`
 
   The process of stitching together overlapping fragments to guess the sequence of the original larger DNA sequence that those fragments came from.

 * `{ankiAnswer} (hybrid alphabet|alternate alphabet|alternative alphabet)/i`
 
   When representing a sequence that isn't fully conserved, it may be more appropriate to use an alphabet where each letter can represent more than 1 nucleotide. For example, the IUPAC nucleotide codes provides the following alphabet:

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
  
 * `{ankiAnswer} (IUPAC nucleotide code|IUPAC)/i`
 
   A hybrid alphabet with the following mapping:

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

 * `{ankiAnswer} (logo|sequence logo|motif logo)/i`
 
   A graphical representation of how conserved a sequence's positions are. Each position has its possible nucleotides stacked on top of each other, where the height of each nucleotide is based on how conserved it is. The more conserved a position is, the taller that column will be.
 
   Typically applied to DNA or RNA, and May also be applied to other biological sequence types (e.g. amino acids).

   The following is an example of a logo generated from a motif sequence:

   ![Example Image](motif_logo.svg)

 * `{ankiAnswer} (transposon|transposable element|jumping gene)/i`
 
   A DNA sequence that can change its position within a genome, altering the genome size. They come in two flavours:

   * Class I (retrotransposon) - Behaves similarly to copy-and-paste where the sequence is duplicated. DNA is transcribed to RNA, followed by that RNA being reverse transcribed back to DNA by an enzyme called reverse transcriptase.
   * Class II (DNA transposon) - Behaves similarly to cut-and-paste where the sequence is moved. DNA is physically cut out by an enzyme called transposases and placed back in at some other location.
  
   Often times, transposons cause disease. For example, ...

   * insertion of a transposon into a gene will likely disable that gene.
   * after a transposon leaves a gene, the gap likely won't be repaired correctly.

 * `{ankiAnswer} adjacency list`
 
   An internal representation of a graph where each node has a list of pointers to other nodes that it can forward to.

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

 * `{ankiAnswer} adjacency matrix`
 
   An internal representation of a graph where a matrix defines the number of times that each node forwards to every other node.

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

 * `{ankiAnswer} (Hamiltonian path|Hamilton path)/i`
   
    A path in a graph that visits every node exactly once.
 
   The graph below has the Hamiltonian path ABCEDF.

   ```{svgbob}
   A ---> B ---> C ---> D ---> F
                 |      ^      ^
                 |      |      |
                 +----> E -----+
   ```

 * `{ankiAnswer} Eulerian path`
 
   A path in a graph that visits every edge exactly once.
 
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

 * `{ankiAnswer} Eulerian cycle`
 
   An Eulerian path that forms a cycle. That is, a path in a graph that is a cycle and visits every edge exactly once.
 
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

 * `{ankiAnswer} Eulerian graph` `{ankiAnswer} Eulerian cycle`
 
   For a graph to be a Eulerian graph, it must have an Eulerian cycle: a path in a graph that is a cycle and visits every edge exactly once. For a graph to have an Eulerian cycle, it must be both balanced and strongly connected.
 
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
   * every node has an outdegree equal to its indegree (balanced).

     | Node | Indegree | Outdegree |
     |------|----------|-----------|
     | A    | 1        | 1         |
     | B    | 1        | 1         |
     | C    | 2        | 2         |
     | D    | 1        | 1         |
     | F    | 1        | 1         |

   In contrast, the following graphs are not Eulerian graphs (no Eulerian cycles exist):
   
   * Strongly connected but not balanced.

     ```{svgbob}
     A ---> B <--- D
     ^      |      ^
     |      v      |
     +----- C -----+

     "* B contains 2 indegree but only 1 outdegree."
     ```

   * Balanced but not strongly connected.

     ```{svgbob}
     A ---> B ---> E ---> F
     ^      |      ^      |
     |      v      |      v
     D <--- C      H <--- G

     "* It isn't possible to reach B from E, F, G, or H"
     ```

   * Balanced but disconnected (not strongly connected).

     ```{svgbob}
     A ---> B      E ---> F
     ^      |      ^      |
     |      v      |      v
     D <--- C      H <--- G

     "* It isn't possible to reach E, F, G, or H from A, B, C, or D (and vice versa)"
     ```

 * `{ankiAnswer} disconnected` `{ankiAnswer} connected`
   
   A graph is disconnected if you can break it out into 2 or more distinct sub-graphs without breaking any paths. In other words, the graph contains at least two nodes which aren't contained in any path.

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

 * `{ankiAnswer} strongly connected` - A graph is strongly connected if every node is reachable from every other node.

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

 * `{ankiAnswer} indegree` `{ankiAnswer} outdegree`
 
    The number of edges leading into / out of a node of a directed graph.

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

 * `{ankiAnswer} balanced node`
 
    A node of a directed graph that has an equal indegree and outdegree. That is, the number of edges coming in is equal to the number of edges going out.

    The node below has an indegree and outdegree of 1. It is a balanced node.

    ```{svgbob}
    ---> N --->
    ```

 * `{ankiAnswer} balanced graph`
 
   A directed graph where ever node is balanced.

   The graph below is balanced graph because each node has an equal indegree and outdegree.

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

 * `{ankiAnswer} overlap graph`
 
   A graph representing the k-mers making up a string. Specifically, the graph is built in 2 steps:
 
   1. Each node is a fragment.
 
      ```{svgbob}
      TTA     TAG     AGT     GTT 
      TAC     TTA     CTT     ACT 
      ```
 
   2. Each edge is between overlapping fragments (nodes), where the ...
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

 * `{ankiAnswer} de Bruijn graph`
 
   A special graph representing the k-mers making up a string. Specifically, the graph is built in 2 steps:
 
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

 * `{ankiAnswer} (k-universal string|k-universal)/i`
 
   For some alphabet and k, a string is considered k-universal if it contains every k-mer for that alphabet exactly once. For example, for an alphabet containing only 0 and 1 (binary) and k=3, a 3-universal string would be 0001110100 because it contains every 3-mer exactly once:

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

   "* ? string:" 0001110100
   ```

   There are multiple Eulerian cycles in the graph, meaning that there are multiple 3-universal strings:
  
   * 0001110100
   * 0011101000
   * 1110001011
   * 1100010111
   * ...
   
   For larger values of k (e.g. 20), finding k-universal strings would be too computationally intensive without De Bruijn graphs and Eulerian cycles.

 * `{ankiAnswer} coverage`
 
   Given a substring from some larger sequence that was reconstructed from a set of fragments, the coverage of that substring is the number of reads used to construct it. The substring length is typically 1: the coverage for each position of the sequence.

   ```{svgbob}
              "Read ? for each 1-mer"
   
   "1:"        A C T A A G A              
   "2:"          C T A A G A A            
   "3:"            T A A G A A C          
   "4:"                A G A A C C T                
   "5:"                    A A C C T A A            
   "6:"                          C T A A T T T      
   "7:"                              A A T T T A G  
   "8:"                                A T T T A G C
   "String:"   A C T A A G A A C C T A A T T T A G C
   
   "?:"        1 2 3 3 4 4 5 4 3 3 3 3 4 3 3 3 2 2 1
   ```


 * `{ankiAnswer} (read breaking|read-breaking|breaking reads)/i`
 
   The concept of taking multiple reads and breaking them up into smaller reads.

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

   When read breaking, smaller k-mers result in better coverage but also make the de Bruijn graph more tangled. The more tangled the de Bruijn graph is, the harder it is to infer the full sequence.

   In the example above, the average coverage...

    * for the left-hand side (original) is 2.1.
    * for the right-hand side (broken) is 4.

   See also: read-pair breaking.

   ```{note}
   What purpose does this actually serve? Mimicking 1 long read as n shorter reads isn't equivalent to actually having sequenced those n shorter reads. For example, what if the longer read being broken up has an error? That error replicates when breaking into n shorter reads, which gives a false sense of having good coverage and makes it seems as if it wasn't an error.
   ```

 * `{ankiAnswer} (read-pair breaking|read pair breaking|breaking read-pairs|breaking read pairs)/i`
 
   The concept of taking multiple read-pairs and breaking them up into read-pairs with a smaller k.

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

   When read-pair breaking, a smaller k results in better coverage but also make the de Bruijn graph more tangled. The more tangled the de Bruijn graph is, the harder it is to infer the full sequence.

   In the example above, the average coverage...

    * for the left-hand side (original) is 1.6.
    * for the right-hand side (broken) is 2.5.

   See also: read breaking.

   ```{note}
   What purpose does this actually serve? Mimicking 1 long read-pair as n shorter read-pairs isn't equivalent to actually having sequenced those n shorter read-pairs. For example, what if the longer read-pair being broken up has an error? That error replicates when breaking into n shorter read-pairs, which gives a false sense of having good coverage and makes it seems as if it wasn't an error.
   ```

 * `{ankiAnswer} contig`
 
   An unambiguous stretch of DNA derived by searching an overlap graph / de Bruijn graph for paths that are the longest possible stretches of non-branching nodes (indegree and outdegree of 1). Each stretch will be a path that's either  ...
  
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
   
   Real-world complications with DNA sequencing make de Bruijn / overlap graphs too tangled to guess a full genome: both strands of double-stranded DNA are sequenced and mixed into the graph, sequencing errors make into the graph, repeats regions of the genome can't be reliably handled by the graph, poor coverage, etc.. As such, biologists / bioinformaticians have no choice but to settle on contigs.
   
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

 * `{ankiAnswer} ribonucleotide`
 
   Elements that make up RNA, similar to how nucleotides are the elements that make up DNA.

   * A = Adenine (same as nucleotide)
   * C = Cytosine (same as nucleotide)
   * G = Guanine (same as nucleotide)
   * U = Uracil (replace nucleotide Thymine)
  
 * `{ankiAnswer} antibiotic`
 
   A substance (typically an enzyme) for killing, preventing, or inhibiting the grow of bacterial infections.

 * `{ankiAnswer} amino acid`
 
   The building blocks of peptides / proteins, similar to how nucleotides are the building blocks of DNA.

   See proteinogenic amino acid for the list of 20 amino acids used during the translation.

 * `{ankiAnswer} proteinogenic amino acid`
 
   Amino acids that are used during translation. These are the 20 amino acids that the ribosome translates from codons. In contrast, there are many other non-proteinogenic amino acids that are used for non-ribosomal peptides.
 
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
