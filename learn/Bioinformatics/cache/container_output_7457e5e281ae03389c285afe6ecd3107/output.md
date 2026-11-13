<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

It isn't discussed here, but the Pevzner book put an emphasis on calculating the parsimonious number of reversals (reversal distance) without having to go through and apply two-breaks in the breakpoint graph_GR. The basic idea is to count the number of red-blue cycles in the graph.

For a cyclic breakpoint graph_GRs, a single red-blue cycle is when you pick a node, follow the blue edge, then follow the red edge, then follow the blue edge, then follow the red edge, ..., until you arrive back at the same node. If the blue and red genomes match perfectly, the number of red-blue cycles should equal the number of synteny blocks. Otherwise, you can calculate the number of reversals needed to get them to equal by subtracting the number of red-blue cycles by the number of synteny blocks.

For a linear breakpoint graph_GRs, a single red-blue cycle isn't actually a cycle because: Pick the termination node, follow a blue edge, then follow the red edge, then follow the blue edge, then follow the red edge, ... until you arrive back at the termination node (what if there are actual cyclic red-blue loops as well like in cyclic breakpoint graph_GRs?). If the blue and red genomes match perfectly, the number of red-blue cycles should equal the number of synteny blocks + 1. Otherwise, you can **ESTIMATE** the number of reversals needed to get them to equal by subtracting the number of red-blue cycles by the number of synteny blocks + 1.

To calculate the real number of reversals need for linear breakpoint graph_GRs (not estimate), there's a [paper on ACM DL](https://dl.acm.org/doi/10.1145/300515.300516) that goes over the algorithm. I glanced through it but I don't have the time / wherewithal to go through it. Maybe do it in the future.

UPDATE: Calculating the number of reversals quickly is important because the number of reversals can be used as a distance metric when computing a phylogenetic tree across a set of species (a tree that shows how closely a set of species are related / how they branched out). See distance matrix definition.
</div>

