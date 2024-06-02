import polars as pl
import pandas as pd
from scipy.spatial import distance
from scipy.spatial.distance import pdist, squareform

################################################################################

def Matching_dist_matrix(X):
    """
    Calculates the Matching distance matrix for a data matrix `X` using SciPy.

    Parameters (inputs)
    ----------
    X: a pandas/polars DataFrame or a NumPy array. It represents a data matrix.

    Returns (outputs)
    -------
    M: the Matching distance matrix between the rows of X.
    """

    if isinstance(X, pl.DataFrame):
        X = X.to_numpy()
    if isinstance(X, pd.DataFrame):
        X = X.to_numpy()    
            
    # Compute the pairwise distances using pdist and convert to a square form.
    M = squareform(pdist(X, metric='matching'))
    
    return M

################################################################################

def Matching_dist(xi, xr) :
    """
    Calculates the Matching distance between a pair of vectors.

    Parameters (inputs)
    ----------
    xi, xr: a pair of quantitative vectors. They represent a couple of statistical observations.

    Returns (outputs)
    -------
    The Matching distance between the observations `xi` and `xr`.
    """
    return distance.hamming(xi, xr)

################################################################################