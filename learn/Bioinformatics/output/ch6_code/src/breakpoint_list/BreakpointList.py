from typing import List, Optional

from helpers.Utils import slide_window


# MARKDOWN
def find_adjacencies_sandwiched_between_breakpoints(augmented_blocks: List[int]) -> List[int]:
    assert augmented_blocks[0] == 0
    assert augmented_blocks[-1] == len(augmented_blocks) - 1
    ret = []
    for (x1, x2), idx in slide_window(augmented_blocks, 2):
        if x1 + 1 != x2:
            ret.append(idx)
    return ret


def find_and_reverse_section(augmented_blocks: List[int]) -> Optional[List[int]]:
    bp_idxes = find_adjacencies_sandwiched_between_breakpoints(augmented_blocks)
    for (bp_i1, bp_i2), _ in slide_window(bp_idxes, 2):
        if augmented_blocks[bp_i1] + 1 == -augmented_blocks[bp_i2] or\
                augmented_blocks[bp_i2 + 1] == -augmented_blocks[bp_i1 + 1] + 1:
            return augmented_blocks[:bp_i1 + 1]\
                   + [-x for x in reversed(augmented_blocks[bp_i1 + 1:bp_i2 + 1])]\
                   + augmented_blocks[bp_i2 + 1:]
    return None
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        blocks = [int(i) for i in input().split(', ')]
        augmented_blocks = [0] + blocks + [len(blocks) + 1]
        print(f'Reversing on breakpoint boundaries...\n')
        print(f' * `[{", ".join(("+" if b > 0 else "") + str(b) for b in augmented_blocks)}]`')
        while (augmented_blocks := find_and_reverse_section(augmented_blocks)) is not None:
            print(f' * `[{", ".join(("+" if b > 0 else "") + str(b) for b in augmented_blocks)}]`')
        print(f'')
        print(f'No more reversals possible.')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()
