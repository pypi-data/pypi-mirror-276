from typing import Union
import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from scipy.spatial.distance import pdist, squareform


def show_clustering(data_traces, links, condensed_distances):
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(8, 8))
    gs = fig.add_gridspec(5, 5)
    ax1 = plt.subplot(gs[1:, 1:])

    ax0 = plt.subplot(gs[0, 1:], sharex=ax1)
    ax2 = plt.subplot(gs[1:, 0], sharey=ax1)

    ddg = dendrogram(
        links, ax=ax0,
        count_sort=False, distance_sort=True, show_leaf_counts=True,
        no_plot=False, no_labels=True)
    ddg = dendrogram(
        links, ax=ax2, orientation="left",
        count_sort=False, distance_sort=True, show_leaf_counts=True,
        no_plot=False, no_labels=True)

    index = ddg['leaves']
    condensed_distances = squareform(condensed_distances)[index, :][:, index]

    ax1.pcolormesh(
        np.arange(data_traces.shape[0] + 1) * 10 + 0.5,
        np.arange(data_traces.shape[0] + 1) * 10 + 0.5,
        condensed_distances)
    plt.setp(ax1.get_xticklabels(), visible=False)
    plt.setp(ax1.get_yticklabels(), visible=False)
    ax2.invert_yaxis()
    plt.show()



def waveform_corr_coeff(data_traces: np.ndarray, force_symmetry: bool=True) -> np.ndarray:
    """
    :param data_traces: 1 row = 1 trace, 1 col = 1 trace sample
    :return rho: the correlation coefficient matrix
    """
    correlation_matrix = np.corrcoef(data_traces)
    if force_symmetry:
        # force exact symmetry
        correlation_matrix = (correlation_matrix + correlation_matrix.T) / 2.
        # force autocorr to 1
        np.fill_diagonal(correlation_matrix, 1.0)
    return correlation_matrix
    #
    # # 1 row = 1 trace,
    # # the number of samples in each trace is the dimension of the data space
    # n_traces, n_dim = data_traces.shape
    # # compute the correlation between the traces
    # # xi = random variable describing the amplitudes of trace number i, we have n_dim realizations
    # # compute the deviation : xi - E(xi) for all xi
    # dev = data_traces - np.mean(data_traces, axis=1)[:, np.newaxis]
    # # compute the covariance for all pairs of traces
    # # E( (xi - E(xi)) * (xj - E(xj)) )
    # cov = dev.dot(dev.T) / float(n_dim)
    # # compute the inverse std
    # invstd = (dev ** 2.).mean(axis=1) ** -.5
    # # intersect these products and multiply by cov to get the correlation coeff
    # correlation_matrix = cov * (invstd[:, np.newaxis] * invstd)
    #
    # if force_symmetry:
    #     # force exact symmetry
    #     correlation_matrix = (correlation_matrix + correlation_matrix.T) / 2.
    #     # force autocorr to 1
    #     np.fill_diagonal(correlation_matrix, 1.0)
    #
    # return correlation_matrix


def waveform_distances(correlation_matrix: np.ndarray, power: float = 1.0) -> np.ndarray:
    """
    get distance from corr coeff, move to condensed distance matrix
    :param correlation_matrix: correlation coefficient matrix from waveform_corr_coeff
    :param power:
    :return:
    """
    condensed_distances = squareform((0.5 * (1. - correlation_matrix)) ** power)
    return condensed_distances


def waveform_clustering(
    data_traces: np.ndarray,
    condensed_distances: np.ndarray,
    n_clusters: int = 10,
    sort_by: str="distance",
    master: str="average"):

    # 1 row = 1 trace,
    n_traces, n_dim = data_traces.shape
    assert len(condensed_distances) == (n_traces * (n_traces - 1)) // 2

    links = linkage(condensed_distances, method="ward")

    cluster_affiliations = fcluster(links, t=n_clusters, criterion='maxclust') - 1

    _, cluster_counts = np.unique(cluster_affiliations, return_counts=True)

    cluster_masters = np.zeros((n_clusters, n_dim), data_traces.dtype)

    for n_cluster in range(n_clusters):
        cluster_mask = cluster_affiliations == n_cluster
        if master == "average":
            cluster_masters[n_cluster, :] = data_traces[cluster_mask, :].mean(axis=0)

        elif master == "median":
            cluster_masters[n_cluster, :] = np.median(data_traces[cluster_mask, :], axis=0)

        else:
            raise ValueError(master)

    # sort_by seems to have no effect
    clustering_index = dendrogram(links, no_plot=True, count_sort=False, distance_sort=True)['leaves']
#   # clustering_index = dendrogram(links, no_plot=True, count_sort=True, distance_sort=False)['leaves']
    if False:
        # QC
        # from scipy.cluster.hierarchy import optimal_leaf_ordering
        # links = optimal_leaf_ordering(links, condensed_distances) # takes a while and has no effect
        show_clustering(data_traces, links, condensed_distances)

    return cluster_masters, cluster_affiliations, cluster_counts, clustering_index


if __name__ == '__main__':
    npts = 1024

    data_traces = []
    for _ in range(100):
        data_traces.append(
            np.sin(2. * np.pi * np.arange(npts) / 200.) + 0.9 * np.random.randn(npts))

    for _ in range(50):
        data_traces.append(
            np.sin(2. * np.pi * np.arange(npts) / 130.) + 0.9 * np.random.randn(npts))

    for _ in range(25):
        data_traces.append(
            np.sin(2. * np.pi * np.arange(npts) / 100.) + 0.9 * np.random.randn(npts))

    data_traces = np.asarray(data_traces)
    i = np.argsort(np.random.rand(data_traces.shape[0]))
    data_traces = data_traces[i, :]

    rho = waveform_corr_coeff(data_traces)
    condensed_distance = waveform_distances(rho, power=1)

    cluster_centroids, cluster_affiliations, \
        cluster_counts, sort_index = \
            waveform_clustering(
                data_traces=data_traces,
                condensed_distances=condensed_distance,
                n_clusters=3,
                sort_by="distance",
                master="median")

    dist = squareform(condensed_distance)
    import matplotlib.pyplot as plt
    plt.figure()
    ax1 = plt.subplot(221)
    plt.colorbar(ax1.pcolormesh(rho))
    ax2 = plt.subplot(222, sharex=ax1, sharey=ax1)
    plt.colorbar(ax2.pcolormesh(rho[sort_index, :][:, sort_index]))
    ax3 = plt.subplot(223, sharex=ax1)
    plt.colorbar(ax3.pcolormesh(data_traces.T))
    ax4 = plt.subplot(224, sharex=ax1, sharey=ax3)
    plt.colorbar(ax4.pcolormesh(data_traces.T[:, sort_index]))

    plt.figure()
    for n in range(cluster_centroids.shape[0]):
        plt.plot(0.1 * cluster_centroids[n, :] / cluster_centroids[n, :].std() + n)

    plt.show()
