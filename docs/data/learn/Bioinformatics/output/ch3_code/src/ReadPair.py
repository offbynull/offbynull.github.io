from __future__ import annotations

from collections import Counter
from random import Random
from typing import List, Tuple, Optional, Callable

from Kdmer import Kdmer
from Read import Read
from Utils import slide_window, slide_window_kd


class ReadPair:
    def __init__(self: ReadPair, data: Kdmer, instance: int = 0, source: Optional[Tuple[str, List[ReadPair]]] = None) -> None:
        self.source = source
        self.data = data
        self.instance = instance
        self.source = source
        self._hash_cache = hash((self.data, self.instance))  # this is an immutable class, so caching hash is okay

    # If instantize is true, each duplicate kdmer in text will be given a unique instance number, meaning that it'll be
    # distinct from its duplicates.
    @staticmethod
    def from_string(text: str, k: int, d: int, instantize: bool = False):
        counter = Counter()
        ret = []
        for kdmer, _ in slide_window_kd(text, k, d):
            instance = counter[kdmer] if instantize else 0
            ret.append(ReadPair(kdmer, instance=instance))
            counter[kdmer] += 1
        return ret

    @property
    def k(self: ReadPair) -> int:
        return self.data.k

    @property
    def d(self: ReadPair) -> int:
        return self.data.d

    def prefix(self: ReadPair, skip: int = 1) -> ReadPair:
        return ReadPair(
            Kdmer(
                self.data.head[:-skip],
                self.data.tail[:-skip],
                self.data.d
            ),
            source=('prefix', [self])
        )

    def suffix(self: ReadPair, skip: int = 1) -> ReadPair:
        return ReadPair(
            Kdmer(
                self.data.head[skip:],
                self.data.tail[skip:],
                self.data.d
            ),
            source=('suffix', [self])
        )

    def reverse_complement(self: ReadPair) -> ReadPair:
        def complement(ch):
            if ch == 'A':
                return 'T'
            elif ch == 'T':
                return 'A'
            elif ch == 'C':
                return 'G'
            elif ch == 'G':
                return 'C'
            else:
                return '?'

        new_head = ''
        for ch in self.data.head[::-1]:
            new_head += complement(ch)
        new_tail = ''
        for ch in self.data.tail[::-1]:
            new_tail += complement(ch)
        return ReadPair(Kdmer(new_head, new_tail, self.d))

    # MARKDOWN_MERGE_OVERLAPPING
    def append_overlap(self: ReadPair, other: ReadPair, skip: int = 1) -> ReadPair:
        self_head = Read(self.data.head)
        other_head = Read(other.data.head)
        new_head = self_head.append_overlap(other_head)
        new_head = new_head.data

        self_tail = Read(self.data.tail)
        other_tail = Read(other.data.tail)
        new_tail = self_tail.append_overlap(other_tail)
        new_tail = new_tail.data

        # WARNING: new_d may go negative -- In the event of a negative d, it means that rather than there being a gap
        # in between the head and tail, there's an OVERLAP in between the head and tail. To get rid of the overlap, you
        # need to remove either the last d chars from head or first d chars from tail.
        new_d = self.d - skip
        kdmer = Kdmer(new_head, new_tail, new_d)

        return ReadPair(kdmer, source=('overlap', [self, other]))

    @staticmethod
    def stitch(items: List[ReadPair], skip: int = 1) -> str:
        assert len(items) > 0
        ret = items[0]
        for other in items[1:]:
            ret = ret.append_overlap(other, skip)
        assert ret.d <= 0, "Gap still exists -- not enough to stitch"
        overlap_count = -ret.d
        return ret.data.head + ret.data.tail[overlap_count:]
    # MARKDOWN_MERGE_OVERLAPPING

    # MARKDOWN_BREAK
    # This is read breaking -- why not just call it break? because break is a reserved keyword.
    def shatter(self: ReadPair, k: int) -> List[ReadPair]:
        ret = []
        d = (self.k - k) + self.d
        for window_head, window_tail in zip(slide_window(self.data.head, k), slide_window(self.data.tail, k)):
            kmer_head, _ = window_head
            kmer_tail, _ = window_tail
            kdmer = Kdmer(kmer_head, kmer_tail, d)
            rp = ReadPair(kdmer, source=('shatter', [self]))
            ret.append(rp)
        return ret
    # MARKDOWN_BREAK

    @staticmethod
    def collapse(items: List[ReadPair]) -> List[ReadPair]:
        collector = dict()
        for item in items:
            collector.setdefault(item.data, []).append(item)
        ret = []
        for data, matches in collector.items():
            collapsed = ReadPair(data, source=('collapse', matches))
            ret.append(collapsed)
        return ret

    def __eq__(self, x: ReadPair) -> bool:
        return type(self) is type(x) and self.data == x.data and self.instance == x.instance

    def __hash__(self: ReadPair) -> int:
        return self._hash_cache

    def __repr__(self: ReadPair) -> str:
        return str(self.data)

    def __str__(self: ReadPair) -> str:
        return str(self.data)

    @staticmethod
    def random_fragment(data: str, k: int, d: int, read_count: int, r: Optional[Random] = None) -> List[ReadPair]:
        if r is None:
            r = Random()
        total_kmers = len(data) - (k*2 + d) + 1
        ret = []
        for i in range(read_count):
            offset = r.randint(0, total_kmers)
            kdmer_head = data[offset:offset+k]
            kdmer_tail = data[offset+k+d:offset+k+d+k]
            kdmer = Kdmer(kdmer_head, kdmer_tail, d)
            read = ReadPair(kdmer)
            ret.append(read)
        return ret

    def introduce_random_errors(self: ReadPair, count: int, include_source: bool = False, r: Optional[Random] = None) -> ReadPair:
        if r is None:
            r = Random()
        data = self.data.head + self.data.tail
        offsets = list(range(len(data)))
        for i in range(count):
            offset = r.choice(offsets)
            offsets.remove(offset)
            choices = ['A', 'C', 'T', 'G']
            choices.remove(data[offset])
            data = data[:offset] + r.choice(choices) + data[offset+1:]
        source = ('introduce_error', [self]) if include_source else None
        return ReadPair(Kdmer(data[:self.k], data[self.k:], self.d), source=source)

    def to_sources(self: ReadPair, stop_func: Callable[[str, List[ReadPair]], bool] = lambda x: False) -> List[List[ReadPair]]:
        def walk_up(item: ReadPair, path: List[ReadPair]) -> List[List[ReadPair]]:
            if item.source is None:
                return [path]
            source_name, source_list = item.source
            if stop_func(source_name, source_list):
                return [path]
            ret = []
            for new_source in source_list:
                new_path = path.copy() + [new_source]
                new_paths = walk_up(new_source, new_path)
                ret.extend(new_paths)
            return ret
        return walk_up(self, [self])




def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        lines = []
        while True:
            try:
                line = input().strip()
                if len(line) > 0:
                    lines.append(line)
            except EOFError:
                break

        command = lines[0]
        lines = lines[1:]
        if command == 'stitch':
            read_pairs = [ReadPair(Kdmer(l.split('|')[0], l.split('|')[2], int(l.split('|')[1]))) for l in lines]
            genome = read_pairs[0].stitch(read_pairs)
            print(f'Stitched {read_pairs} to {genome}\n\n')
        elif command == 'shatter':
            new_k = int(lines[0])
            read = ReadPair(Kdmer(lines[1].split('|')[0], lines[1].split('|')[2], int(lines[1].split('|')[1])))
            shattered = read.shatter(new_k)
            print(f'Broke {read} to {shattered}\n\n')
        else:
            raise
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()