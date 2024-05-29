import numpy as np

def indices_to_mask(indices, mask_length):
    """Convert list of indices to boolean mask.

    Parameters
    ----------
    indices : list-like
        List of integers treated as indices.
    mask_length : int
        Length of boolean mask to be generated.
        This parameter must be greater than max(indices).

    Returns
    -------
    mask : 1d boolean nd-array
        Boolean array that is True where indices are present, else False.

    Examples
    --------
    >>> from sklearn.utils import indices_to_mask
    >>> indices = [1, 2 , 3, 4]
    >>> indices_to_mask(indices, 5)
    array([False,  True,  True,  True,  True])
    """
    if mask_length <= np.max(indices):
        raise ValueError("mask_length must be greater than max(indices)")

    mask = np.zeros(mask_length, dtype=bool)
    mask[indices] = True

    return mask