"""Complexity metrics based on compressibility."""

# This code was created based on Michael Schartner's code.
# Author: Michael Schartner, m.schartner@sussex.ac.uk
#         Christian ferreyra, chrisferreyra13@gmail.com
# Date: 09.12.14 - 2022
# License : BSD-3-Clause

import numpy as np
from random import shuffle

from ._utils import (
    detrending_normalization,
    binary_matrix_to_string,
    binarize_matrix
)


def _lempel_ziv_welch_compression(binary_string):
    """Return the size of the dictionary of binary words after compression.

    Based on Lempel-Ziv-Welch compression.

    Parameters
    ----------
    binary_string : str
        Binary string to be compressed.

    Returns
    -------
    int
        Size of the dictionary of binary words.
    """
    if not isinstance(binary_string, str):
        raise TypeError("The input should be string.")

    dictionary = dict()
    word = ""
    for c in binary_string:
        wc = word + c
        if wc in dictionary:
            word = wc
        else:
            dictionary[wc] = wc
            word = c

    return len(dictionary)


def compute_lempel_ziv_complexity(data):
    """Compute LZc and use shuffled result as normalization.

    Parameters
    ----------
    data : ndarray, (n_channels, n_times)
        Mulidimensional time series matrix.

    Returns
    -------
    float
        Lempel-Ziv complexity value (between 0 and 1).
    """
    if not isinstance(data, np.ndarray):
        TypeError("Data matrix should be a ndarray of float values.")

    data = detrending_normalization(data)
    data = binarize_matrix(data)
    binary_str = binary_matrix_to_string(data)

    # create random string for normalization
    random_list = list(binary_str)
    shuffle(random_list)
    random_str = ""
    for c in random_list:
        random_str += c

    # compute LZc
    lzc_value = _lempel_ziv_welch_compression(binary_str)
    norm_value = float(_lempel_ziv_welch_compression(random_str))
    lzc_value_normalized = lzc_value / norm_value

    return lzc_value_normalized
