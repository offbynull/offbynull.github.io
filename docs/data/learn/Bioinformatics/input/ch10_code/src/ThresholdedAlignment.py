from typing import TypeVar

E = TypeVar('E')


class StableColumn:
    def __init__(self, elements: list[E]):
        self.elements = elements

    def missing_count(self):
        return sum(1 for e in self.elements if e is None)

    def kept_count(self):
        return sum(1 for e in self.elements if e is not None)

    def __str__(self):
        return f'{self.__class__.__name__}: {self.elements}'

    def __format__(self, format_spec):
        return str(self)

    def __repr__(self):
        return str(self)


class UnstableColumn:
    def __init__(self, elements: list[E]):
        self.elements = elements
    
    def missing_count(self):
        return sum(1 for e in self.elements if e is None)

    def kept_count(self):
        return sum(1 for e in self.elements if e is not None)
    
    def all_missing(self):
        return self.kept_count() == 0

    def __str__(self):
        return f'{self.__class__.__name__}: {self.elements}'

    def __format__(self, format_spec):
        return str(self)

    def __repr__(self):
        return str(self)


class ThresholdedAlignment:
    def __init__(self, threshold: float, sequences: list[list[E]], gap_symbol: E):
        self.col_count = len(sequences[0])
        self.row_count = len(sequences)
        columns = []
        for i in range(self.col_count):
            column_elements = [None if s[i] == gap_symbol else s[i] for s in sequences]
            gapped_count = sum(1 for e in column_elements if e is None)
            gapped_perc = gapped_count / self.row_count
            if gapped_perc >= threshold:
                columns.append(UnstableColumn(column_elements))
            else:
                columns.append(StableColumn(column_elements))
        self.threshold = threshold
        self.columns = columns

    def splice_with_unstable(self):
        last_c_type = StableColumn
        inserted_cnt = 0
        for c in self.columns:
            if last_c_type == StableColumn:
                if not isinstance(c, UnstableColumn):
                    yield UnstableColumn([None for _ in range(self.row_count)])
                yield c
                last_c_type = UnstableColumn
            elif last_c_type == UnstableColumn:
                if isinstance(c, UnstableColumn):
                    yield c
                    last_c_type = UnstableColumn
                    inserted_cnt += 1
                elif isinstance(c, StableColumn):
                    if inserted_cnt == 0:
                        yield UnstableColumn([None for _ in range(self.row_count)])
                    yield c
                    last_c_type = StableColumn
                    inserted_cnt = 0
        if last_c_type == StableColumn:
            yield UnstableColumn([None for _ in range(self.row_count)])

    def splice_with_unstable_and_group(self):
        fill = []
        for col in self.splice_with_unstable():
            if fill:
                if isinstance(col, fill[-1].__class__):
                    fill.append(col)
                    yield fill
                    fill = []
                else:
                    yield fill
                    fill = [col]
            else:
                fill.append(col)
        if fill:
            yield fill



seqs = '''
ACDEFACADF
AFDA---CCF
A--EFD-FDC
ACAEF--A-C
ADDEFAAADF
'''.strip().split()
seqs = [list(s) for s in seqs]
ta = ThresholdedAlignment(0.4, seqs, '-')

for v in ta.splice_with_unstable_and_group():
    print(f'{v}')