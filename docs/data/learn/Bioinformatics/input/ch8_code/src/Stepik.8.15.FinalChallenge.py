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


import tarfile

with tarfile.open('cancer_dataset.tar.xz', 'r:xz') as t:
    with t.extractfile('colon_test.txt') as f:
        unknown_sample_str = f.read().decode('utf-8')
    with t.extractfile('colon_healthy.txt') as f:
        healthy_samples_str = f.read().decode('utf-8')
    with t.extractfile('colon_cancer.txt') as f:
        cancer_samples_str = f.read().decode('utf-8')

print(f'{unknown_sample_str}')

MAKE SURE TO LOG THE DATAPOINTS BEFORE WORKING ON THIS
