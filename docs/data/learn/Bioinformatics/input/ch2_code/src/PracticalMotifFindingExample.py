import re
import csv
import lzma

from RandomizedMotifMatrixSearchWithPsuedocounts import randomized_motif_search_with_psuedocounts
from ScoreMotif import score_motif


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        # *** THIS BLOCK LOADS IN THE SEQUENCE AND GENES FOR BAKER'S YEAST ***
        fasta_filepath = 'GCA_000146045.2_R64_genomic.fna.xz'
        with lzma.open(fasta_filepath, mode='rt', encoding='utf-8') as f:
            lines = f.read().splitlines()
            lines = [line for line in lines if not line.startswith('>')]
            seq = ''.join(lines).upper()

        genes_filepath = 'GCA_000146045.2_R64_gene_result.txt.xz'
        with lzma.open(genes_filepath, mode='rt', encoding='utf-8') as f:
            csv_reader = csv.reader(f, delimiter='\t')
            genes_data = []
            for row in csv_reader:
                genes_data.append(row)

        genes = []
        for row in genes_data[1:]:
            gene_start_pos_str = row[12].strip()
            if gene_start_pos_str == '':
                continue
            gene_name = row[5].strip()
            gene_start_pos = int(gene_start_pos_str)
            genes.append((gene_name, gene_start_pos))
        genes.sort(key=lambda g: g[1])

        # This is an artificial example. I went through yeast motifs in http://motifmap.ics.uci.edu/ and picked one out
        # (DIG1). Then I went through NCBI and tried to find the genome and gene list for this particular strain of
        # yeast. I searched through the sequence and known gene locations to pull out gene upstream regions that
        # contained this motif.
        #
        # This is the closest I could get to a practical example short of doing my own experiments, which I don't have
        # the equipment or wherewithal to do.
        #
        # Motifs: http://motifmap.ics.uci.edu/ (Click on motif search and select yeast -- it will display all motifs)
        # Sequence: https://www.ncbi.nlm.nih.gov/assembly/GCF_000146045.2
        # Gene list: https://www.ncbi.nlm.nih.gov/gene/?term=txid559292%5BOrganism%3Anoexp%5D+DIG1
        #
        # To speed the example up, I only used a subset of the found gene upstreams.

        # *** THIS BLOCK SEARCHES THE SEQUENCE FOR MOTIF MEMBERS OF DIG1 ***
        # search_locs = []
        # for m in re.finditer(r'AAA..[AG]AA.GA[AG][AG]AA.A[AG]', seq):  # This is the motif for DIG1
        #     start_idx, end_idx = m.span()
        #     motif_member = m.string[start_idx:end_idx]
        #     closest_gene =\
        #         min(
        #             map(
        #                 lambda g: (g[0], g[1] - start_idx, g[1]),
        #                 filter(
        #                     lambda g: g[1] > start_idx,
        #                     genes
        #                 )
        #             ),
        #             key=lambda g: g[1],
        #             default=None
        #         )
        #     if closest_gene is not None and closest_gene[1] <= 2000:
        #         print(f'Found {motif_member} {start_idx}, closest gene is {closest_gene}')
        #         search_locs.append((closest_gene[2] - 2000, closest_gene[2]))
        # for start_idx, end_idx in search_locs:
        #     print(f'seq[{start_idx}:{end_idx}]')
        # # Found AAAAGGAAGGAAAAATAG 14779, closest gene is ('THI12', 53, 14832)
        # # Found AAACAAAAAGAAAAAAAG 65682, closest gene is ('TOS6', 62, 65744)
        # # Found AAAAGAAAAGAGAAATAG 67732, closest gene is ('snR85', 36, 67768)
        # # Found AAAAAAAAGGAAAAAAAG 70180, closest gene is ('YHL017W', 96, 70276)
        # # Found AAAGAAAAAGAAAAAAAA 128183, closest gene is ('SYN8', 69, 128252)
        # # Found AAAAGAAAAGAAAAAAAG 172014, closest gene is ('YPL199C', 19, 172033)
        # # Found AAACGGAATGAGGAATAA 183306, closest gene is ('RPC53', 37, 183343)
        # # Found AAAAAAAACGAAAAAAAA 268978, closest gene is ('CDC5', 41, 269019)
        # # Found AAAAAAAAGGAAAAAGAA 293881, closest gene is ('YBR027C', 143, 294024)
        # # Found AAAGAAAAAGAAAAAGAA 404722, closest gene is ('YCK3', 91, 404813)
        # # Found AAACGGAATGAGGAATAA 451419, closest gene is ('MEH1', 15, 451434)
        # # Found AAACGGAATGAGGAATAA 457003, closest gene is ('KTR6', 115, 457118)
        # # Found AAAAAAAACGAGAAAAAG 488333, closest gene is ('MSK1', 53, 488386)
        # # Found AAACGGAATGAGGAATAA 489960, closest gene is ('VPS21', 236, 490196)
        # # Found AAACGGAATGAGGAATAA 495545, closest gene is ('SHE3', 47, 495592)
        # # Found AAACGGAATGAGGAATAA 557448, closest gene is ('TIF34', 33, 557481)
        # # Found AAAAAAAATGAAAAACAA 590680, closest gene is ('GRR1', 192, 590872)
        # # Found AAACGAAACGAAGAAAAA 645845, closest gene is ('YDR098C-B', 13, 645858)
        # # Found AAAGAAAAAGAGAAATAA 760834, closest gene is ('BSC5', 289, 761123)
        # # Found AAAAAGAAAGAAAAAAAG 779839, closest gene is ('IRC13', 31, 779870)
        # # Found AAAGCAAAAGAAGAAAAA 780606, closest gene is ('DFR1', 300, 780906)
        # # Found AAAACAAACGAAAAAAAA 783720, closest gene is ('ECL1', 503, 784223)
        # # Found AAAGAAAATGAAAAAAAA 791430, closest gene is ('STB3', 918, 792348)
        # # Found AAACGAAAGGAGAAATAA 873685, closest gene is ('FBP1', 61, 873746)
        # # Found AAAGAAAAGGAAAAAAAG 1116394, closest gene is ('YCG1', 732, 1117126)
        # # Found AAACGGAATGAGGAATAA 1126271, closest gene is ('UBX5', 1601, 1127872)
        # # Found AAACGGAATGAGGAATAA 1195086, closest gene is ('BCP1', 326, 1195412)
        # # Found AAACAAAAAGAAAAACAA 1195582, closest gene is ('TFC6', 1097, 1196679)
        # # Found AAACGGAATGAGGAATAA 1212779, closest gene is ('KEI1', 69, 1212848)

        # *** THIS BLOCK RUNS MOTIF FINDING ALGO ON THE GENE UPSTREAM REGIONS -- FOUND MOTIF SHOULD BE FOR DIG1 ***
        #  note: some gene upstream regions were commented out to speed up motif finding
        gene_upstreams = [
            seq[12832:14832],  # THI12
            # seq[63744:65744],
            # seq[65768:67768],
            seq[68276:70276],  # YHL017W
            seq[126252:128252],  # SYN8
            # seq[170033:172033],
            # seq[181343:183343],
            # seq[267019:269019],
            # seq[292024:294024],
            # seq[402813:404813],
            # seq[449434:451434],
            # seq[455118:457118],
            # seq[486386:488386],
            # seq[488196:490196],
            # seq[493592:495592],
            # seq[555481:557481],
            # seq[588872:590872],
            # seq[643858:645858],
            # seq[759123:761123],
            # seq[777870:779870],
            # seq[778906:780906],
            # seq[782223:784223],
            # seq[790348:792348],
            # seq[871746:873746],
            seq[1115126:1117126],  # YCG1
            seq[1125872:1127872],  # UBX5
            # seq[1193412:1195412],
            # seq[1194679:1196679],
            seq[1210848:1212848]  # KEI1
        ]
        k = 18  # If we searched for a slightly larger or smaller k, we would likely get some hits that contain parts of
                # the correct motif members (k=18). I think the correct course of action is to play with k and see what
                # parts of the upstream regions light up. If they're consistently lighting up within the same parts, you
                # may be on the right track?
                #
                # Since this is an artificial example, we already know that k=18.
        print(f'Organism is baker\'s yeast. Suspected genes influenced by transcription factor: THI12, YHL017W, SYN8,'
              f' YCG1, UBX5, and KEI1.', end="\n\n")
        print(f'Searching for {k}-mer across a set of {len(gene_upstreams)} gene upstream regions...', end="\n\n")
        best_motif_matrix = None
        for iteration in range(200):
            found_motif_matrix = randomized_motif_search_with_psuedocounts(k, gene_upstreams)
            if best_motif_matrix is None or score_motif(found_motif_matrix) < score_motif(best_motif_matrix):
                best_motif_matrix = found_motif_matrix
        print(f'{"<br>".join(best_motif_matrix)}', end="\n\n")
        print(f'Score is: {score_motif(best_motif_matrix)}', end="\n\n")
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()