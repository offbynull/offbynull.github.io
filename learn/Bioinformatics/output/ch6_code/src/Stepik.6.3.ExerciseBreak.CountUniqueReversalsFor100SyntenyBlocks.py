# Poorly worded question. Here's my crack at rewording it: What's the maximum number of unique reversals possible on a
# permutation of length 100? So for example, assume you have a permutation of length 2: [+A, +B]...
#
# reverse 1:  [+A, +B] to [-A ,+B]
# reverse 2:  [+A, +B] to [+A, -B]
# reverse range 1-2: [+A, +B] to [-B, -A]
#
# That's it. Any permutation of length 2 will have a max of 3 unique reversals possible.
#
# Now apply the logic to a permutation of length 100.

total = 0
block_count = 100
for start in range(1, block_count + 1):
    # you can turn the following loop to just total += start   I left the original in because it's easier to think about
    for end in range(1, start + 1):
        total += 1
print(f'{total}')
