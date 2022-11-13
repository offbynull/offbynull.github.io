def hanoi_towers(n, from_peg, to_peg):
    if n == 1:
        print(f'Move disk from peg {from_peg} to peg {to_peg}')
        return
    unused_peg = 6 - from_peg - to_peg
    hanoi_towers(n-1, from_peg, unused_peg)
    print(f'Move disk from peg {from_peg} to peg {to_peg}')
    hanoi_towers(n-1, unused_peg, to_peg)

hanoi_towers(6, 1, 3)