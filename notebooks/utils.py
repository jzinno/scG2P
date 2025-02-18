import numpy as np
import pandas as pd

from hdbscan import HDBSCAN


def _mgt(num, detect_frac=0):
    if 0 <= num < detect_frac:
        return 0
    if num < 0:
        return -1
    if num > 0:
        return 1


def af_hdbscan(
    sc,
    min_cluster_size=30,
    min_samples=1,
    metric="euclidean",
    cluster_selection_method="leaf",
):
    """
    Add a HDBSCAN layer to the dna layer of the missionbio object inplace.
    """
    sc.dna.set_labels(
        HDBSCAN(
            min_cluster_size=min_cluster_size,
            min_samples=min_samples,
            metric=metric,
            cluster_selection_method=cluster_selection_method,
        )
        .fit_predict(
            sc.dna.get_attribute(
                "umap",
            )
        )
        .astype(str)
    )


def mgt_merge_clusters_frac(sc, similarity=0.8, remove_missing=False, detect_frac=0):
    """
    Merge similar clusters while ignoring missing data.

    Modified from the Mosaic package.

    Parameters
    ----------
    layer : str
        The layer with the VAF data.
    similarity : float [0, 1]
        The proportion of variants that must be similar
        so as to combine multiple clusters into one cluster.
    """

    mgt = sc.get_attribute(attribute="AF", constraint="row+col")
    mgt = mgt.applymap(_mgt, detect_frac=detect_frac)

    # Identifying cluster characteristics
    # i.e., mean VAF is closest to 0, 0.25, 0.5, 0.75, or 1
    mgt["label"] = sc.get_labels()

    cluster_char = pd.DataFrame(columns=mgt.columns)
    for lab, vaf_lab in mgt.groupby("label"):
        cluster_char.loc[lab, :] = np.round(vaf_lab.mean())

    cluster_char = cluster_char.drop("label", axis=1)

    clusters = np.array(cluster_char.index)
    print(f"Unique clusters found - {len(clusters)}")

    # Removing clusters caused due to missing values
    if remove_missing:
        cluster_char_pos = cluster_char.loc[:, (cluster_char >= 0).all()]
        renamed_clusters = {}

        for i in range(len(clusters)):
            if clusters[i] not in renamed_clusters:
                renamed_clusters[clusters[i]] = clusters[i]

            for j in range(i + 1, len(clusters)):
                char1 = cluster_char_pos.iloc[i, :]
                char2 = cluster_char_pos.iloc[j, :]
                simi = (char1 == char2).mean()
                if simi >= similarity:
                    renamed_clusters[clusters[j]] = renamed_clusters[clusters[i]]

        clusters = np.unique(list(renamed_clusters.values()))
    else:
        renamed_clusters = {clusters[i]: clusters[i] for i in range(len(clusters))}
    print(
        f"Clusters after removing missing data (on: {remove_missing}) - {len(clusters)}"
    )

    # Renaming labels
    newlabs = np.array([renamed_clusters[lab] for lab in sc.get_labels()])
    labels, idx, cnt = np.unique(newlabs, return_inverse=True, return_counts=True)
    labels[cnt.argsort()[::-1]] = np.arange(len(labels)) + 1
    labels = labels[idx]

    sc.set_labels(labels)
    return sc


def subcluster_small_clones(
    sc,
    min_cluster_size=10,
    min_samples=5,
    metric="euclidean",
    cluster_selection_method="leaf",
):
    small_clones = sc[
        sc.dna.barcodes(
            list(
                filter(
                    lambda x: x
                    == sc.dna.get_attribute("AF", constraint="row+col")
                    .groupby(sc.dna.get_labels())
                    .mean()
                    .max(axis=1)
                    .sort_values(ascending=True)
                    .index[0],
                    np.unique(sc.dna.get_labels()),
                )
            )
        )
    ]
    small_clones.dna.run_umap("AF")
    small_clusterer = HDBSCAN(
        min_cluster_size=min_cluster_size,
        min_samples=min_samples,
        metric=metric,
        cluster_selection_method=cluster_selection_method,
    ).fit(small_clones.dna.get_attribute("umap"))
    small_clones.dna.set_labels(
        np.array([s + "_small" for s in list(small_clusterer.labels_.astype("str"))])
    )
    small_clones = small_clones[
        small_clones.dna.barcodes(
            list(
                filter(
                    lambda x: x != "-1_small",
                    np.unique(small_clones.dna.get_labels()),
                )
            )
        )
    ]
    old_dict = dict(zip(sc.dna.barcodes(), sc.dna.get_labels()))
    new_dict = dict(zip(small_clones.dna.barcodes(), small_clones.dna.get_labels()))
    old_dict.update(new_dict)
    sc.dna.set_labels(list(old_dict.values()))


def iterative_clone_clustering(
    sc,
    macro_custer_size=25,
    micro_cluster_size=5,
    niter=5,
    similarity=0.99,
    remove_missing=True,
    detect_frac=30,
):
    """
    Performs iterative clone clustering.
    """
    af_hdbscan(sc, min_cluster_size=macro_custer_size)
    mgt_merge_clusters_frac(
        sc.dna,
        similarity=similarity,
        remove_missing=remove_missing,
        detect_frac=detect_frac,
    )
    for i in range(niter):
        subcluster_small_clones(
            sc,
            min_cluster_size=micro_cluster_size,
            min_samples=1,
        )
        mgt_merge_clusters_frac(
            sc.dna,
            similarity=similarity,
            remove_missing=remove_missing,
            detect_frac=detect_frac,
        )
