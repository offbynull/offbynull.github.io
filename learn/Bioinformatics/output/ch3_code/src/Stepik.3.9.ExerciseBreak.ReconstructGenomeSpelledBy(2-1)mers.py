from Kdmer import Kdmer
from ReadPair import ReadPair

# AG-AG
#  GC-GC
#   CA-CT
#    AG-TG
#     GC-GC
#      CT-CT
#       TG-TG
#        GC-GC
#         CT-CA
# AGCAGCTGCTGCA
kdmers =[
    Kdmer('AG', 'AG', 1),
    Kdmer('GC', 'GC', 1),
    Kdmer('CA', 'CT', 1),
    Kdmer('AG', 'TG', 1),
    Kdmer('GC', 'GC', 1),
    Kdmer('CT', 'CT', 1),
    Kdmer('TG', 'TG', 1),
    Kdmer('GC', 'GC', 1),
    Kdmer('CT', 'CA', 1)
]
readpairs = [ReadPair(kdmer) for kdmer in kdmers]
out = readpairs[0].stitch(readpairs)
print(f'{out}')
