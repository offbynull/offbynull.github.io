<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

This dataset is from the NCBI gene expression omnibus (GEO): [Influenza virus H5N1 infection of U251 astrocyte cell line: time course](https://www.ncbi.nlm.nih.gov/sites/GDSbrowser?acc=GDS6010). You may be able to use other datasets from the GEO with this same code -- use the [GDS browser](https://www.ncbi.nlm.nih.gov/sites/GDSbrowser) if you want to find more.

> GDS6010
>
> Title: Influenza virus H5N1 infection of U251 astrocyte cell line: time course
>
> Summary: Analysis of U251 astrocyte cells infected with the influenza H5N1 virus for up to 24 hours. Results provide insight into the immune response of astrocytes to H5N1 infection.
>
> Organism: Homo sapiens
>
> Platform: GPL6480: Agilent-014850 Whole Human Genome Microarray 4x44K G4112F (Probe Name version)
>
> Citation: Lin X, Wang R, Zhang J, Sun X et al. Insights into Human Astrocyte Response to H5N1 Infection by Microarray Analysis. Viruses 2015 May 22;7(5):2618-40. PMID: 26008703
>
> Reference Series: GSE66597
>
> Sample count: 18
>
> Value type: transformed count
>
> Series published: 2016/01/04

There are too many genes here for the clustering algorithm (Python is slow). As such, standard deviation is used to filter out genes expression vectors that don't dramatically change during the time-course. The experiment did come with a control group: a second population of the same cell line but uninfected. Maybe instead of standard deviation, a better filtering approach would be to only include genes whose gene expression pattern is vastly different between control group vs experimental group.

The original data set was too large. I removed the replicates and only kept hour 24 of the control group.
</div>

