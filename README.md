# scG2P

Accociated code for the paper [Genotype-to-phenotype mapping of somatic clonal mosaicism via single-cell co-capture of DNA mutations and mRNA transcripts
](https://www.biorxiv.org/content/10.1101/2024.05.22.595241v1)

![scG2P workflow](./assets/scG2P_workflow.png)

## Abstract

Somatic mosaicism is a hallmark of malignancy that is also pervasively observed in human physiological aging, with clonal expansions of cells harboring mutations in recurrently mutated driver genes. Bulk sequencing of tissue microdissection captures mutation frequencies, but cannot distinguish which mutations co-occur in the same clones to reconstruct clonal architectures, nor phenotypically profile clonal populations to delineate how driver mutations impact cellular behavior. To address these challenges, we developed single-cell Genotype-to-Phenotype sequencing (scG2P) for high-throughput, highly-multiplexed, single-cell joint capture of recurrently mutated genomic regions and mRNA phenotypic markers in cells or nuclei isolated from solid tissues. We applied scG2P to aged esophagus samples from five individuals with high alcohol and tobacco exposure and observed a clonal landscape dominated by a large number of clones with a single driver event, but only rare clones with two driver mutations. NOTCH1 mutants dominate the clonal landscape and are linked to stunted epithelial differentiation, while TP53 mutants and double-driver mutants promote clonal expansion through both differentiation biases and increased cell cycling. Thus, joint single-cell highly multiplexed capture of somatic mutations and mRNA transcripts enables high resolution reconstruction of clonal architecture and associated phenotypes in solid tissue somatic mosaicism.

## Notebooks

Data processing as described in the paper:

- [Cell Line](./notebooks/cell_line.ipynb)
- [Patient Cells](./notebooks/patient_clustering.ipynb)

## Citation

```bibtex
@article {Yuan2024.05.22.595241,
	author = {Yuan, Dennis J and Zinno, John and Botella, Theo and Dhingra, Dalia and Wang, Shu and Hawkins, Allegra and Swett, Ariel and Sotelo, Jesus and Raviram, Ramya and Hughes, Clayton and Potenski, Catherine and Yokoyama, Akira and Kakiuchi, Nobuyuki and Ogawa, Seishi and Landau, Dan A},
	title = {Genotype-to-phenotype mapping of somatic clonal mosaicism via single-cell co-capture of DNA mutations and mRNA transcripts},
	year = {2024},
	doi = {10.1101/2024.05.22.595241},
	journal = {bioRxiv}
}

```
