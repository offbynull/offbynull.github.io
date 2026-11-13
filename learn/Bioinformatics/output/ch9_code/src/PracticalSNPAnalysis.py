import lzma
import random
import textwrap
from sys import stdin

import yaml

from helpers.DnaUtils import dna_reverse_complement
from sequence_search.BurrowsWheelerTransform_Checkpointed import mismatch_search


def extract_contigs(fna_data: str):
    contig_id = ''
    contig_seq = ''
    contigs = []
    lines = fna_data.splitlines(keepends=False)
    for l in lines:
        if l.startswith('>'):
            contig_id = l[1:].strip()
            if contig_seq != '':
                contigs.append((contig_id, contig_seq))
            contig_seq = ''
        else:
            contig_seq += l
    contigs.append((contig_id, contig_seq))
    return contigs


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        reference_genome_filename = data['reference_genome_filename']
        reads_filename = data['reads_filename']
        max_mismatch = data['max_mismatch']
        pad_marker = data['pad_marker']
        end_marker = data['end_marker']
        last_tallies_checkpoint_n = data['last_tallies_checkpoint_n']
        first_indexes_checkpoint_n = data['first_indexes_checkpoint_n']
        print(f'Executing checkpointed BWT search algorithm using the following settings (reverse complements of reads automatically included)...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        with lzma.open(reference_genome_filename) as f:
            reference_genome = f.read().decode('utf8')
        with lzma.open(reads_filename) as f:
            reads = f.read().decode('utf8').splitlines(keepends=False)
            read_to_line = {r: i for i, r in enumerate(reads)}
            read_to_line.update({dna_reverse_complement(r): i for i, r in enumerate(reads)})  # add rev complements
        for contig_id, contig_seq in extract_contigs(reference_genome):
            found_set = mismatch_search(contig_seq, reads, max_mismatch, end_marker, pad_marker,
                                        last_tallies_checkpoint_n, first_indexes_checkpoint_n)
            print()
            print(f'{contig_id}')
            print()
            for found_idx, actual, found, dist in sorted(found_set):
                read_line = read_to_line[actual]
                print(f' * Matched read at line {read_line} ({actual[:10]}...) to'
                      f' index {found_idx} of current contig ({found[:10]}...)'
                      f' with {dist} mismatches')
            print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()

# blocks = []
# with open('/home/user/Downloads/Mycoplasma agalactiae 14628 - GCA_000266865.1_ASM26686v1_genomic.fna') as f_in:
#     lines = f_in.read().splitlines(keepends=False)
#     block = ''
#     for l in lines:
#         if l.startswith('>'):
#             if block != '':
#                 blocks.append(block)
#             block = ''
#         else:
#             block += l
#     selected = set()
# block_size = 100
# while len(selected) < 5000:
#     block = random.choice(blocks)
#     if len(block) < block_size:
#         continue
#     pos = random.randint(0, len(block) - block_size)
#     read = block[pos:pos+block_size]
#     selected.add(read)
# with lzma.open('Mycoplasma agalactiae - READS.txt.xz', 'wt') as f_out:
#     for r in selected:
#         f_out.write(r + '\n')
