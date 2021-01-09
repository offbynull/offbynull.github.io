`{anki}` offbynull anki -- JS must be enabled.<br/>`{ankiInfoPanel}`

```{comment}
The anki inline tag injects a special anki JS into the HTML. The anki JS will treat the items in the first
bullet list as anki cloze words questions.

The anki* inline tags generate HTML spans/divs with special class names that get processed by the anki JS:

ankiInfoPanel - Information about the question / questions / state. One allowed in entire file.
   ankiAnswer - Regex answer for the current question. Multiple allowed per question.
                  Text in question that matches the regex will be blacked out and users must answer them. The
                  content of this tag are the same as a 2 or 3 parameter bm tag with the 1st parameter (label)
                  removed. For example...
                  `{ankiAnswer}one`
                  `{ankiAnswer}two`
                  `{ankiAnswer}(three)/i`
     ankiHide - Regex hider for the current question. Multiple allowed per question.
                  Text in question that matches the regex will be blacked out. The content of this tag are the
                  same as the ankiAnswer tag.
     ankiDead - Marks a question as dead / to be skipped. One allowed per question. 
```

 * Question 1 one. `{ankiAnswer}one`

 * Question 2 two. `{ankiAnswer}two` `{ankiDead}`

 * Question 3 three. The word red should be hidden. `{ankiAnswer}three` `{ankiHide}red`

 * Question 4 four and beep or boop. `{ankiAnswer}four` `{ankiAnswer}beep` `{ankiAnswer}boop`

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
 
 * `{ankiAnswer} replication origin` `{ankiAnswer} \b(ori)\b/i`
 
   The point in DNA at which replication starts. May be shortened to ori.
 
 * `{ankiAnswer} replication terminus` `{ankiAnswer} \b(ter)\b/i`
   
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

   This nomenclature has to do with DNA polymerase. Since DNA polymerase can only walk in the reverse direction (3' to 5'), it synthesizes the leading half-strand in one shot. For the lagging half-strand (5' to 3'), multiple DNA polymerases have to used to synthesize DNA, each binding to the lagging strand and walking backwards a small amount to generate a small fragment_NORM of DNA (Okazaki fragment). the process is much slower for the lagging half-strand, that's why it's called lagging.

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

 * `{ankiAnswer} (cDNA)/i`
 
   A single strand of DNA generated from mRNA. The enzyme reverse transcriptase scans over the mRNA and creates the complementing single DNA strand.

   ```{svgbob}
   3' . . . U <- U <- U <- G <- C <- U <- U <- U <- U <- G <- . . . 5'   mRNA  
            |    |    |    |    |    |    |    |    |    | 
   5' . . . A -> A -> A -> C -> G -> G -> A -> A -> A -> C -> . . . 3'   cDNA  
   ```

   The mRNA portion breaks off, leaving the single-stranded DNA.

   ```{svgbob}
   5' . . . A -> A -> A -> C -> G -> G -> A -> A -> A -> C -> . . . 3'   cDNA  
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
  
 * `{ankiAnswer} (consensus string|consensus sequence)/i`
 
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
   |read_SEQ 1   | | | | |C|T|T|C|T|T|
   |read_SEQ 2   | | | |G|C|T|T|C|T| |
   |read_SEQ 3   | | |T|G|C|T|T|C| | |
   |read_SEQ 4   | |T|T|G|C|T|T| | | |
   |read_SEQ 5   |A|T|T|G|C|T| | | | |
   |reconstructed|A|T|T|G|C|T|T|C|T|T|

 * `{ankiAnswer} sequencer`
 
   A machine that performs DNA or RNA sequencing.

 * `{ankiAnswer} (sequencing error|sequencer error)/i`
 
   An error caused by a sequencer returning a fragment where a nucleotide was misinterpreted at one or more positions (e.g. offset 3 was actually a C but it got scanned in as a G).

   ```{note}
   This term may also be used in reference to homopolymer errors, known to happen with nanopore technology. From [here](https://news.ycombinator.com/item?id=25459670)...

   > A homopolymer is when you have stretches of the same nucleotide, and the error is miscounting the number of them. e.g: GAAAC could be called as "GAAC" or "GAAAAC" or even "GAAAAAAAC".
   ```

 * `{ankiAnswer} \b(read)/i`
 
   A segment of genome scanned in during the process of sequencing.

 * `{ankiAnswer} (read-pair|read pair)/i`
 
   A segment of genome scanning in during the process of sequencing, where the middle of the segment is unknown. That is, the first k elements and the last k elements are known, but the d elements in between aren't known. The total size of the segment is 2k + d.

   Sequencers provide read-pairs as an alternative to longer reads because the longer a read is the more errors it contains.

   See kd-mer.

 * `{ankiAnswer} (fragment)/i`
 
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