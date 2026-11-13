# As we mentioned earlier, gene expression analysis has a wide variety of applications, including cancer studies. In
# 1999, Uri Alon analyzed gene expression data for 2,000 genes from 40 colon tumor tissues and compared them with data
# from colon tissues belonging to 21 healthy individuals, all measured at a single time point. We can represent his data
# as a 2,000 × 61 gene expression matrix, where the first 40 columns describe tumor samples and the last 21 columns
# describe normal samples.
#
# Now, suppose you performed a gene expression experiment with a colon sample from a new patient, corresponding to a
# 62nd column in an augmented gene expression matrix. Your goal is to predict whether this patient has a colon tumor.
# Since the partition of tissues into two clusters (tumor vs. healthy) is known in advance, it may seem that classifying
# the sample from a new patient is easy. Indeed, since each patient corresponds to a point in 2,000-dimensional space,
# we can compute the center of gravity of these points for the tumor sample and for the healthy sample. Afterwards, we
# can simply check which of the two centers of gravity is closer to the new tissue.
#
# Alternatively, we could perform a blind analysis, pretending that we do not already know the classification of samples
# into cancerous vs. healthy, and analyze the resulting 2,000 x 62 expression matrix to divide the 62 samples into two
# clusters. If we obtain a cluster consisting predominantly of cancer tissues, this cluster may help us diagnose colon
# cancer.
#
# Final Challenge: These approaches may seem straightforward, but it is unlikely that either of them will reliably
# diagnose the new patient. Why do you think this is? Given Alon’s 2,000 × 61 gene expression matrix and gene data from
# a new patient, derive a superior approach to evaluate whether this patient is likely to have a colon tumor.
import random
import statistics
import tarfile
from math import log2

# Load
from statistics import mean, stdev

with tarfile.open('cancer_dataset.tar.xz', 'r:xz') as t:
    with t.extractfile('colon_healthy.txt') as f:
        healthy_samples_str = f.read().decode('utf-8')
        healthy_samples = [[float(e) for e in l.split()] for l in healthy_samples_str.split('\n')]
    with t.extractfile('colon_cancer.txt') as f:
        cancer_samples_str = f.read().decode('utf-8')
        cancer_samples = [[float(e) for e in l.split()] for l in cancer_samples_str.split('\n')]
    with t.extractfile('colon_test.txt') as f:
        unknown_sample_str = f.read().decode('utf-8')
        unknown_sample = [float(e) for e in unknown_sample_str.split()]

def test(healthy_samples, cancer_samples, unknown_sample):
    # Calculate average
    healthy_sample_gene_avgs = []
    cancer_sample_gene_avgs = []
    for i in range(0, 2000):
        healthy_sample_gene_avgs.append(mean(r[i] for r in healthy_samples))
        cancer_sample_gene_avgs.append(mean(r[i] for r in cancer_samples))

    # Apply logarithms
    healthy_samples_logged = [[log2(e) for e in r] for r in healthy_samples]
    cancer_samples_logged = [[log2(e) for e in r] for r in cancer_samples]
    unknown_sample = [log2(e) for e in unknown_sample]
    healthy_sample_gene_avgs_logged = [log2(e) for e in healthy_sample_gene_avgs]
    cancer_sample_gene_avgs_logged = [log2(e) for e in cancer_sample_gene_avgs]

    # Find genes with vastly different average for healthy vs cancer, then see which mean the unknown is closer to
    genes_above_threshold = []
    healthy = 0
    cancer = 0
    for i in range(0, 2000):
        logged_healthy_i_list = [s[i] for s in healthy_samples_logged]
        logged_cancer_i_list = [s[i] for s in cancer_samples_logged]
        logged_avg_offset = abs(healthy_sample_gene_avgs_logged[i] - cancer_sample_gene_avgs_logged[i])
        if logged_avg_offset < 1.7:
            continue
        # print(f'===={i}====')
        # print(f'{min(logged_healthy_i_list)=} {max(logged_healthy_i_list)=}')
        # print(f'{min(logged_cancer_i_list)=} {max(logged_cancer_i_list)=}')
        dist_to_healthy_mean = abs(healthy_sample_gene_avgs_logged[i] - unknown_sample[i])
        dist_to_cancer_mean = abs(cancer_sample_gene_avgs_logged[i] - unknown_sample[i])
        if dist_to_cancer_mean < dist_to_healthy_mean:
            # print(f'CANCER IDENTIFIED: {dist_to_healthy_mean=} vs {dist_to_cancer_mean=}')
            cancer += 1
        else:
            # print(f'HEALTHY IDENTIFIED: {dist_to_healthy_mean=} vs {dist_to_cancer_mean=}')
            healthy += 1
        genes_above_threshold.append(i)

    # print(f'------------------------')
    # print(f'{len(genes_above_threshold)=}')
    # print(f'{healthy=}')
    # print(f'{cancer=}')
    return healthy, cancer

healthy_samples_cnts = []
for i, s in enumerate(healthy_samples):
    local_healthy_samples = healthy_samples[:]
    local_healthy_samples.pop(i)
    local_unknown_sample = s
    healthy_cnt, cancer_cnt = test(local_healthy_samples, cancer_samples, local_unknown_sample)
    healthy_samples_cnts.append((healthy_cnt, cancer_cnt))
    print(f'When healthy_samples[{i}] is removed as the unknown sample, it\'s identified as having cancer % of {(cancer_cnt / (healthy_cnt + cancer_cnt)):.2f}')

print('-----')

cancer_samples_cnts = []
for i, s in enumerate(cancer_samples):
    local_cancer_samples = cancer_samples[:]
    local_cancer_samples.pop(i)
    local_unknown_sample = s
    healthy_cnt, cancer_cnt = test(healthy_samples, local_cancer_samples, local_unknown_sample)
    cancer_samples_cnts.append((healthy_cnt, cancer_cnt))
    print(f'When cancer_samples[{i}] is removed as the unknown sample, it\'s identified as having cancer % of {(cancer_cnt / (healthy_cnt + cancer_cnt)):.2f}')

print('-----')

unknown_healthy_cnt, unknown_cancer_cnt = test(healthy_samples, cancer_samples, unknown_sample)
print(f'For the actual unknown sample, it\'s identified as having cancer % of {(unknown_cancer_cnt / (unknown_healthy_cnt + unknown_cancer_cnt)):.2f}')