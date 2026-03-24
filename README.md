# scG2P

Accociated code for the paper [Genotype-to-phenotype mapping of somatic clonal mosaicism via single-cell co-capture of DNA mutations and mRNA transcripts
](https://doi.org/10.1158/2159-8290.CD-24-0853)

![scG2P workflow](./assets/scG2P_workflow.png)

## Abstract

Somatic mosaicism is a hallmark of malignancy that is also pervasively observed in human physiological aging, with clonal expansions of cells harboring mutations in recurrently mutated driver genes. Bulk sequencing of tissue microdissection captures mutation frequencies, but cannot distinguish which mutations co-occur in the same clones to reconstruct clonal architectures, nor phenotypically profile clonal populations to delineate how driver mutations impact cellular behavior. To address these challenges, we developed single-cell Genotype-to-Phenotype sequencing (scG2P) for high-throughput, highly-multiplexed, single-cell joint capture of recurrently mutated genomic regions and mRNA phenotypic markers in cells or nuclei isolated from solid tissues. We applied scG2P to aged esophagus samples from five individuals with high alcohol and tobacco exposure and observed a clonal landscape dominated by a large number of clones with a single driver event, but only rare clones with two driver mutations. NOTCH1 mutants dominate the clonal landscape and are linked to stunted epithelial differentiation, while TP53 mutants and double-driver mutants promote clonal expansion through both differentiation biases and increased cell cycling. Thus, joint single-cell highly multiplexed capture of somatic mutations and mRNA transcripts enables high resolution reconstruction of clonal architecture and associated phenotypes in solid tissue somatic mosaicism.

## Notebooks

Data processing as described in the paper:

- [Cell Line](./notebooks/cell_line.ipynb)
- [Patient Cells](./notebooks/patient_clustering.ipynb)

We heavily rely on Mission Bio's proprietary tools to process the data, this includes their [Tapestri pipeline](https://support.missionbio.com/hc/en-us/categories/360002512933-Tapestri-Pipeline) to go from sequencing reads to a data structure for use with their [Mosaic](https://missionbio.github.io/mosaic/) package, their API may change over time, this work was done using `Mosaic` version `2.1`, check their documentation for the latest methods if you are working with a different version. Methods such as filtering cells on completeness and clustering use convenient functions of Mission Bio's data class, for example:

```python
# Filter cells on completeness (50% or greater)
sample_obj.dna.filter_barcodes(completeness=50)

# Filter varaints
sample_obj.dna.filter_variants()

# Find Clones
sample_obj.dna.find_clones()
```

When finding clones, in some pateient samples we found that it may be beneficial to run and iterative strategy to increase the quality of the clones. This is implemented this in the `iterative_clone_clustering` function found in the `utils.py` file.

## Citation

```bibtex
@article{10.1158/2159-8290.CD-24-0853,
    author = {Yuan, Dennis J. and Zinno, John and Botella, Theo and Dhingra, Dalia and Wang, Shu and Hawkins, Allegra G. and Swett, Ariel and Sotelo, Jesus and Raviram, Ramya and Hughes, Clayton and Potenski, Catherine and Godfrey, Katharine D. and Ainsworth, Kara M. and Xu, Shuzhen and Que, Jianwen and Abrams, Julian A. and Yokoyama, Akira and Kakiuchi, Nobuyuki and Ogawa, Seishi and Landau, Dan A.},
    title = {Genotype-to-Phenotype Mapping of Somatic Clonal Mosaicism via Single-Cell Co-Capture of DNA Mutations and mRNA Transcripts},
    journal = {Cancer Discovery},
    pages = {OF1-OF19},
    year = {2026},
    month = {02},
    issn = {2159-8274},
    doi = {10.1158/2159-8290.CD-24-0853},
    url = {https://doi.org/10.1158/2159-8290.CD-24-0853},
    eprint = {https://aacrjournals.org/cancerdiscovery/article-pdf/doi/10.1158/2159-8290.CD-24-0853/3738704/cd-24-0853.pdf},
}
```
