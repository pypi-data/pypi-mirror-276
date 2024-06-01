import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import BisectingKMeans


def slow_bisecting_kmeans(coords):
    """Slow brute force initial clustering using bisecting kmeans

    This uses a 'perfect' even distribution of cluster members to estimate
    the initial number of target clusters, and then iterates upwards from
    there until the termination condition is met. Will be replaced."""

    nclust = (len(coords)//50) + 1
    kmean = BisectingKMeans(n_clusters=nclust, init='k-means++',n_init = 50,algorithm='elkan', max_iter=8000, bisecting_strategy='largest_cluster')
    kmean.fit(coords)

    sizes = []

    for i in np.unique(kmean.labels_):
        sizes.append(np.sum(kmean.labels_ == i))

    minsize = np.array(sizes).min()
    maxsize = np.array(sizes).max()

    while (maxsize > 24) and (minsize > 3):
        nclust +=1
        kmean = BisectingKMeans(n_clusters=nclust, init='k-means++',n_init = 50,algorithm='elkan', max_iter=8000, bisecting_strategy='largest_cluster')
        kmean.fit(coords)

        sizes = []

        for i in np.unique(kmean.labels_):
            sizes.append(np.sum(kmean.labels_ == i))

        #msize = np.array(sizes).min()
        minsize = np.array(sizes).min()
        maxsize = np.array(sizes).max()

    kmean = BisectingKMeans(n_clusters=nclust-1,init='k-means++',n_init = 50,algorithm='elkan', max_iter=8000, bisecting_strategy='largest_cluster')
    kmean.fit(coords)
    return kmean

    # For debugging / plotting
    #
    # sizes = []
    # for i in np.unique(kmean.labels_):
    #    sizes.append(np.sum(kmean.labels_ == i))


def select_central_point(labels, coordinates, centroids, 
                         metric='euclidean'):
    """Select the nearest central point in a given nieghborhood

    Note this code explicitly assumes that centroids are passed from an
    sklearn clustering result (i.e., kmeans, or bisecting kmeans); those
    centroids are ordered as monotonically increasing labels. In other words,
    the output indices will match the labeling order of the input centroids.
    """
    nbrs = NearestNeighbors(n_neighbors=1, algorithm='ball_tree', 
                            metric=metric).fit(coordinates)
    I = nbrs.kneighbors(centroids, return_distance=False)
    return I.squeeze()
    #return labels[I], I #coordinates[I].squeeze()       


def over_cluster(labels, coordinates, metric='haversine', neighborhood=5,
                 overlap_points=2,  method='edge', include_centroid=False,
                 rejection_threshold=None, centriod_labels=None):
    """Expand cluster membership to include edge points of neighbor clusters

    Expands an existing clustering to create overlapping membership between 
    clusters. Existing clusters are processed sequentially by removing
    the current cluster, and looking up nearest neighbors from adjacent
    clusters. Once the `overlapping_points` for the first neighbor have
    been determined and added to current cluster, the first neighbor is
    removed and distance query is rerun, repeating the process N times as
    set by the `neighborhood` parameter. For stability, only original points
    are included for subsequent neighborhood searches. Nearest neighbor
    distances are either from the most central point of the current cluster,
    or the shortest distance of all original members of the current cluster.
    
    Function requires an initial vector of cluster labels from a prior
    clustering, and coordinates in an ordering that matches the labels. This
    function also assumes that all points have been assigned a label (i.e.,
    there are no unlabeled points, or points labeled as 'noise').

    For method 'center', the algorithm will build a reachability graph using
    the corresponding OPTICS method, select point with the shortest
    reachability value as the central point for distance queries; this
    approximates the densest portion of the cluster, rather than the
    geometric center. For method 'user', a vector of indices corresponding
    to central cluster points will be used. The `include_centroid` flag
    will add the central most point of a neighbor cluster to output
    groupings, and uses the previously mentioned OPTICS logic to determine
    centrality, unless `method` is set to 'user'.
    
    Parameters
    ----------

    labels : ndarray of type int, and shape (n_samples,)
        Cluster labels for each point in the dataset from prior clustering.
    coordinates : ndarray of shape (n_samples, n_features)
        Coordinates do not need to match what was used for the prior
        clustering; i.e., if 'Euclidean' was used to calculate the prior
        clustering in an X,Y,Z projection, those coordinates can be provided
        in spherical coordinates, provided that 'haversine' is selected for
        the `metric` parameter.
    metric : str or callable, default='haversine'
        Metric to use for distance computation. Any metric from scikit-learn
        or scipy.spatial.distance can be used. Note that latitude and
        longitude values will need to be converted to radians if using 
        the default 'haversine' distance metric.

        If metric is a callable function, it is called on each
        pair of instances (rows) and the resulting value recorded. The callable
        should take two arrays as input and return one value indicating the
        distance between them. This works for Scipy's metrics, but is less
        efficient than passing the metric name as a string. 

        Use of "precomputed", i.e., a N-by-N distance matrix, has not been
        tested, nor have sparse matrices. These may or may not work, but
        are likely to break if OPTICS is being used to calculate centrality
        of either the source or neighbor cluster.

        Valid values for metric are:

        - from scikit-learn: ['cityblock', 'cosine', 'euclidean', 'l1', 'l2',
          'manhattan']

        - from scipy.spatial.distance: ['braycurtis', 'canberra', 'chebyshev',
          'correlation', 'dice', 'hamming', 'jaccard', 'kulsinski',
          'mahalanobis', 'minkowski', 'rogerstanimoto', 'russellrao',
          'seuclidean', 'sokalmichener', 'sokalsneath', 'sqeuclidean',
          'yule']

        Sparse matrices are only supported by scikit-learn metrics.
        See the documentation for scipy.spatial.distance for details on these
        metrics.

        .. note::
           `'kulsinski'` is deprecated from SciPy 1.9 and will removed in SciPy 1.11.

    neighborhood : int greater than or equal to 1, default=3
        Number of adjacent clusters to include when adding cluster membership
        overlap. Should be less than the number of unique cluster labels - 1.

    overlap_points : int greater than or equal to 1, default=2
        Should not exceed the size of the smallest cluster in `labels`, or
        one less than that when `include_centroid` is set to 'True'.

    method : {'edge', 'center', 'user'}, str, default='edge'
        The method used to determine distance when selecting nearest points
        of overlap. The default 'edge' will use the shortest distance
        considering all points in the source cluster; 'center' will determine
        the point in source cluster occupying the densest area of the cluster,
        and select the shortest distance from that point to any point outside
        of the source cluster. If selecting 'user', `centroid_labels` must be
        provided, and will be used for minimizing distances.

    include_centroids : bool, default=False
        Whether or not the most central point of adjacent clusters should be
        added as overlap points. If this option is set to 'True', returned
        cluster membership will be original cluster sizes + `overlap_points`
        + 1. Centroid points will be determined by OPTICS unless `method` is
        set to 'user' .

    rejection_threshold : float, default=None
        Determines if any potential overlapping points should be rejected for
        being too far (from source centroid or nearest source edge point).
        Default of 'None' is equivalent to setting the threshold to infinity.
        Note that if value other than 'None' is used, there is no guarantee
        that all clusters will have overlap points added.

    centroid_labels : ndarray of type int, shape (n_clusters,), default=None
        The indices corresponding to centroid points of each labeled cluster.
        Used only when ``method='user'``.

    Returns
    -------
    expanded_clusters : bool array of shape (n_clusters, n_coordinates)
        The updated labels, one-hot encoded. Each row is a boolean index to
        extract cluster membership for a given label. If labels are
        continuous integers starting at 0, then the row number will match the
        cluster label; if not, rows are ordered to monotonically increase
        from the smallest cluster label.
"""
    
    # Returns already sorted
    clusters = np.unique(labels)
    n_clusters = len(clusters)

    # reference index for reverse lookups
    ridx = np.array(list(range(len(labels))))
    output = np.zeros((n_clusters, len(labels)), dtype=np.bool_)

    for cluster in clusters:
        # Define current cluster membership (and non-membership)
        members = labels == cluster
        output[cluster, members] = True
        nonmembers = ~members

        if method == 'edge':
            # Build index tree on members
            nbrs = NearestNeighbors(n_neighbors=1, algorithm='ball_tree', 
                                    metric=metric).fit(coordinates[members])
            # Could be set to '1', but using same check from while loop for consistency
            coverage = len(np.unique(labels[output[cluster, :]]))
            while coverage <= neighborhood:
                # intersect search tree with non-members
                D, I = nbrs.kneighbors(coordinates[nonmembers, :])
                # Rejection threshold is lightly tested...
                if rejection_threshold:
                    if np.min(D) > rejection_threshold:
                        break
                # Select closest external point to add to member cluster
                new_member = ridx[nonmembers][np.argmin(D)]
                # Remove point from future coordinate distance queries
                nonmembers[new_member] = 0
                # Add to member label array
                output[cluster, new_member] = 1
                # Update current count of over-clustered nieghbors
                coverage = len(np.unique(labels[output[cluster, :]]))
                # Grab label of new member for overlap check
                nm_label = labels[new_member]
                # Check if we've exceeded our overlap allotment...
                if sum(labels[output[cluster, :]] == nm_label) >= overlap_points:
                    # ...if so, remove entire nieghboring cluster
                    remove = nm_label == labels
                    nonmembers[remove] = False
    return output
