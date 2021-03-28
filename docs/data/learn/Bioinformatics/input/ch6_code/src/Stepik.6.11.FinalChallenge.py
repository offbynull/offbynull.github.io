import lzma
from random import randrange

import matplotlib.pyplot as plt
import matplotlib.collections as mc
import pylab as pl

with lzma.open('anchors_human_mouse.txt.xz', mode='rt', encoding='utf-8') as f:
    data = f.read()

IDX_ID = 0
IDX_H_CHR = 1
IDX_H_CHR_BEGIN_IDX = 2
IDX_H_CHR_END_IDX = 3
IDX_M_CHR = 4
IDX_M_CHR_BEGIN_IDX = 5
IDX_M_CHR_END_IDX = 6
IDX_SIGN = 7

lines = data.strip().split('\n')
lines = lines[1:]
rows = []
for line in lines:
    line = line.strip()
    row = line.split(' ')
    row[0] = int(row[0])
    row[1] = row[1]
    row[2] = int(row[2])
    row[3] = int(row[3])
    row[4] = row[4]
    row[5] = int(row[5])
    row[6] = int(row[6])
    row[7] = row[7]
    rows.append(row)
lines = []  # no longer required -- clear out memory

data = []
color = []
for x in filter(lambda r: r[IDX_M_CHR] == '2', rows):
    data.append([(x[IDX_M_CHR_BEGIN_IDX], x[IDX_H_CHR_BEGIN_IDX]), (x[IDX_M_CHR_END_IDX], x[IDX_H_CHR_END_IDX])])
    color.append((1, 0, 0, 1))
lc = mc.LineCollection(data, colors=color, linewidths=2)
fig, ax = pl.subplots()
ax.add_collection(lc)
ax.autoscale()
ax.margins(0.1)
plt.show()

# data = []
# for x in filter(lambda r: r[IDX_M_CHR] == '2', rows):
#     data += [(x[IDX_M_CHR_BEGIN_IDX], x[IDX_M_CHR_END_IDX]), (x[IDX_H_CHR_BEGIN_IDX], x[IDX_H_CHR_END_IDX]), 'r']
# plt.plot(*data)
# plt.show()

# m_chrs = {row[IDX_M_CHR] for row in rows}
# h_chrs = {row[IDX_H_CHR] for row in rows}
# points = []
# # for row in filter(lambda r: r[IDX_H_CHR] == '3', rows):
# # for row in rows:
# for row in filter(lambda r: r[IDX_M_CHR] == '2', rows):
#     h_idx = row[IDX_H_CHR_BEGIN_IDX]
#     m_idx = row[IDX_M_CHR_BEGIN_IDX]
#     m_chr = row[IDX_M_CHR]
#     points.append((m_idx, h_idx, m_chr))
#
# plt.title('All Human Chromosome (starting from 1 to n, then X and Y)')
# plt.xlabel('Mouse')
# plt.ylabel('Human')
# for m_chr in m_chrs:
#     color = f'#{randrange(0x1000000):06x}'
#     plt.scatter(
#         [m_idx for m_idx, _, _ in filter(lambda p: p[2] == m_chr, points)],
#         [h_idx for _, h_idx, _ in filter(lambda p: p[2] == m_chr, points)],
#         color=color,
#         s=1
#     )
# plt.show()
