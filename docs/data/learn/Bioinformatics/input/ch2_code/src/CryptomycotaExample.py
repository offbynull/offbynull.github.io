from GibbsSamplerMotifMatrixSearchWithPsuedocounts import gibbs_sampler_motif_search_with_psuedocounts
from ScoreMotif import score_motif

with open('/home/user/Downloads/cryptomycota_csf55/ncbi_dataset/data/GCA_000442015.1/unplaced.scaf.fna', mode='r', encoding='utf-8') as f:
    data = f.read()


genome = ''.join(filter(lambda x: not x.startswith('>'), data.split('\n')))

# https://www.reddit.com/r/bioinformatics/comments/ice1to/example_genomes_for_regulatory_motif_finding/   -- question leading to example
# https://mycocosm.jgi.doe.gov/mycocosm/proteins-browser/browse;MrUOhX?p=cryptomycota  -- list of genes for cryptomycota that are regulated by transciption factor pf00505 (HMG-box)
#   Transcription Factors » Rozella allomycis CSF55 » pf00505
#   Protein Id   Location                      Gene Length
#   Rozal1_1251  scaffold_1239:16,756-15,100   1,657
#   Rozal1_1445  scaffold_154:3,363-2,617      747
#   Rozal1_14337 scaffold_4031:101,971-98,685  3,287
#   Rozal1_16257 scaffold_878:33,576-34,434    859
#   Rozal1_1916  scaffold_214:52,117-50,045    2,073
# https://www.ncbi.nlm.nih.gov/datasets/genomes/?txid=1031332 -- genome of cryptomycota (you want the CSF55 one)
# https://journals.plos.org/plosgenetics/article?id=10.1371/journal.pgen.1003642 -- what could the motif be?
#    The regulatory network shown in Figure 6 consists of a cascade of HMG-box genes, suggesting that each gene may
#    contain a binding site for the upstream regulating HMG-box factor. A search for a conserved binding site using
#    MEME [78] identified a consensus motif (A/G)ACAAAGAA in KEF1, mtHMG1, PaHMG5, PaHMG8, and the FMR1 and FPR1
#    mating-type genes (Figure 7A). This consensus motif is very similar to the common core DNA motif A(A/T)CAA(A/T)G
#    that is recognized by HMG-box transcription factors [79] (reviewed in [2]). The remaining P. anserina HMG-box genes
#    either contained a sequence that displayed some differences to the A(A/T)CAA(A/T)G core sequence (PaHMG2, PaHMG3,
#    PaHMG4 and PaHMG6) (Figure 7A), or they did not contain any related sequence (PaHMG7 and SMR2). Further analyses of
#    mating-type target genes using MEME revealed that the mat+ pheromone receptor gene (PRE1), alternative oxydase gene
#    (AOX), phospho-enol pyruvate kinase gene (PEPCK), Pa_1_24410 and Pa_6_7350 also contained the core HMG-box binding
#    site ACAAAGA (Figure 7A). Interestingly, the two pheromone genes (MFM and MFP) displayed the same conserved core
#    sequence, ATCAAAG. The mat− pheromone receptor (PRE2), Pa_4_80, Pa_4_3858 and Pa_5_9770 did not contain the core
#    HMG-box binding site, suggesting that these genes are secondary targets of HMG-box genes. A total of eight genes
#    contained the (A/G)ACAAAGAA consensus site. The comparison with the distribution of this site in the P. anserina
#    genome indicated that the consensus site is significantly enriched in the selected set of genes examined here
#    (p-value = 0.016) (Materials and Methods).

gene_upstream_regions = [
    genome[15100-2000:15100].replace('N', 'A'),  # replace unknown (N) with A because it breaks the algorithm
    genome[2617-2000:2617].replace('N', 'A'),  # replace unknown (N) with A because it breaks the algorithm
    genome[98685-2000:98685].replace('N', 'A'),  # replace unknown (N) with A because it breaks the algorithm
    genome[34434-2000:34434].replace('N', 'A'),  # replace unknown (N) with A because it breaks the algorithm
    genome[50045-2000:50045].replace('N', 'A')    # replace unknown (N) with A because it breaks the algorithm
]
cycles = 200

for k in range(6,10):
    best_motif_matrix = None
    for i in range(20):
        found_motif_matrix = gibbs_sampler_motif_search_with_psuedocounts(k, gene_upstream_regions, cycles)
        if best_motif_matrix is None:
            best_motif_matrix = found_motif_matrix
        elif score_motif(found_motif_matrix) < score_motif(best_motif_matrix):
            best_motif_matrix = found_motif_matrix

    print(f'--------------')
    for i, motif in enumerate(best_motif_matrix):
        print(f'{motif} -- idx: {gene_upstream_regions[i].index(motif)}')
    print(f'K={k} Score={score_motif(motif)}')

# This isn't working. None of runs converge on any consensus motif that's similar to the ones discussed above.
