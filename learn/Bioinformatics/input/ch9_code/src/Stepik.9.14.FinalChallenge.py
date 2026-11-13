import tarfile

from sequence_search import BurrowsWheelerTransform_Deserialization, BurrowsWheelerTransform_Basic, \
    BurrowsWheelerTransform_Checkpointed


def main():
    # Extract original sequence from the problem's BWT last col.
    with tarfile.open('mycoplasma.tar.xz', 'r:xz') as t:
        with t.extractfile('mycoplasma/mycoplasma/myc_bwt.txt') as f:
            last_col = f.read().decode('utf-8').strip()
        bwt_records = BurrowsWheelerTransform_Deserialization.to_bwt_from_last_sequence(last_col, '$')
        orig_seq = BurrowsWheelerTransform_Basic.walk(bwt_records)
        with t.extractfile('mycoplasma/mycoplasma/myc_reads.txt') as f:
            reads = [l.decode().strip() for l in f.readlines()]
    # TESTING OVERRIDES
    # r = Random(0)
    # orig_seq = ''.join(r.sample(['A', 'C', 'T', 'G'], 1)[0] for _ in range(5000)) + '$'
    # reads = ['ACTGGG', 'ACCCCC']
    found_mismatches = BurrowsWheelerTransform_Checkpointed.mismatch_search(
        orig_seq[:-1],  # remove end marker
        reads,
        1,
        '$',
        '_',
        last_tallies_checkpoint_n=50,
        first_idxes_checkpoint_n=50
    )
    for found in found_mismatches:
        print(f'{found}')


if __name__ == '__main__':
    main()
