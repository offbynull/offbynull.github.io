from GCSkew import gc_skew

skew = gc_skew('GAGCCACCGCGATA')

print(f'{" ".join([str(f) for f in skew])}')