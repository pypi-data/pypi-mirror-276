# PARLE: Path Analysis, Reconciliation, and Label Evaluation

This tool computes the path-label reconciliation (PLR) dissimilarity measure.

---

[TOC]

---

# Abstract

In this study, we investigate the problem of comparing gene trees reconciled with the same species tree using a novel semi-metric, called the Path-Label Reconciliation (PLR) dissimilarity measure.
This approach not only quantifies differences in the topology of reconciled gene trees, but also considers discrepancies in predicted ancestral gene-species maps and speciation/duplication events, offering a refinement of existing metrics such Robinson-Foulds (RF) and their labeled extensions LRF and ELRF. A tunable parameter $\alpha$ also allows users to adjust the balance between its species map and event labeling components. We show that PLR can be computed in linear time and that it is a semi-metric. We also discuss the diameters of reconciled gene tree measures, which are important in practice for normalization, and provide initial bounds on PLR, LRF, and ELRF.

To validate PLR, we simulate reconciliations and perform comparisons with LRF and ELRF. The results show that PLR provides a more evenly distributed range of distances, highlighting its sensitivity and effectiveness, at the same time being computationally efficient. Our findings suggest that the theoretical diameter is rarely reached in practice. The PLR measure advances phylogenetic reconciliation by combining theoretical rigor with practical applicability. Future research will refine its mathematical properties,  explore its performance on different tree types, and integrate it with existing bioinformatics tools for large-scale evolutionary analyses.

**Keywords:** Reconciliation, gene trees, species trees, evolutionary scenarios

**Reference:** Alitzel López Sánchez • José Antonio Ramírez-Rafael • Alejandro Flores Lamas • Maribel Hernandez-Rosales • Manuel Lafond (2024) **The Path-Label Reconciliation (PLR) Dissimilarity1
Measure for Gene Trees**. (currently under review at the [WABI 2004 conference](https://algo-conference.org/2024/wabi/))

---

# Installation

```bash
pip install piler
```

# Synopsis of the tool

This code is a command-line tool designed to generate and compare reconciled gene trees with a given species tree, accounting for evolutionary events. It uses a proposed semi-metric *PLR* to quantify differences between reconciled gene trees, considering discrepancies in tree topology, gene-species mapping, and speciation/duplication events.

This tool supports benchmarking and validation by simulating reconciliations and comparing results with metrics like *LRF* and *ELRF*. The tool aims to enhance phylogenetic reconciliation by providing a refined and efficient method for comparing reconciled gene trees.

The tool can be used with the following syntax:

```bash
# Compute disimilarity
python -m piler gene_trees species_tree <optional arguments>

# Compute distance
python -m piler.simulate_reconciliations species_tree n_genes n_recons <optional arguments>


```

For detailed usage information, you can access the help documentation of the modules:

```bash
python -m piler -h
python -m piler.simulate -h
```

# Tutorial

## To Generate Data

Generate a list of reconciliations with the same species tree and set of genes for all the reconciliations:

```bash
# 5 species, maximum 1 gene per species, 10 gene trees
python -m piler.simulate 5 1 10
```

Generate pairs of reconciliations with the same species tree for all the reconciliations and pair-specific sets of genes:

```bash
 5 species, maximum 1 gene per species, 10 gene trees
python -m piler.simulate 5 1 10 -m pairs
```

## To Compute Distances

Compute distances of pairs of trees sorted by rows:

```bash
python -m piler plr.random_reconciliations.list.tsv plr.species_tree.list.nhx
```

Compute distances for all possible pairs of gene trees in a list:

```bash
python -m piler plr.random_reconciliations.list.tsv plr.species_tree.list.nhx -m all_vs_all
```

# Additional Information

- The tool uses the PLR metric, which is designed to compare reconciled gene trees by taking into account all three components of reconciliations (tree topology, gene-species map, and event labeling) as well as duplication clusters.

- The metric is linear-time computable, making it suitable for large datasets.
- For more detailed documentation and examples, please refer to the project documentation within the repository.