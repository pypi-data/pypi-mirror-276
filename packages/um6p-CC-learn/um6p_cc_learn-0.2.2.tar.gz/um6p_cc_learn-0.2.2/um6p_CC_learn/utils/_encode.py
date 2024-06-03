import numpy as np
import numbers
import math


def _unique(values, *, return_inverse=False, return_counts=False):
    """Helper function to find unique values with support for python objects."""
    if values.dtype == object:
        return _unique_python(values, return_inverse=return_inverse, return_counts=return_counts)
    # numerical
    return _unique_np(values, return_inverse=return_inverse, return_counts=return_counts)


def _unique_np(values, return_inverse=False, return_counts=False):
    """Helper function to find unique values for numpy arrays that correctly
    accounts for nans. See `_unique` documentation for details."""
    uniques = np.unique(
        values, return_inverse=return_inverse, return_counts=return_counts
    )

    inverse, counts = None, None

    if return_counts:
        *uniques, counts = uniques

    if return_inverse:
        *uniques, inverse = uniques

    if return_counts or return_inverse:
        uniques = uniques[0]

    # np.unique will have duplicate missing values at the end of `uniques`
    # here we clip the nans and remove it from uniques
    if uniques.size and is_scalar_nan(uniques[-1]):
        nan_idx = np.searchsorted(uniques, np.nan)
        uniques = uniques[: nan_idx + 1]
        if return_inverse:
            inverse[inverse > nan_idx] = nan_idx

        if return_counts:
            counts[nan_idx] = np.sum(counts[nan_idx:])
            counts = counts[: nan_idx + 1]

    ret = (uniques,)

    if return_inverse:
        ret += (inverse,)

    if return_counts:
        ret += (counts,)

    return ret[0] if len(ret) == 1 else ret


def _unique_python(values, *, return_inverse, return_counts):
    # Only used in `_uniques`, see docstring there for details
    try:
        uniques_set = set(values)
        uniques_set, missing_values = _extract_missing(uniques_set)

        uniques = sorted(uniques_set)
        uniques.extend(missing_values.to_list())
        uniques = np.array(uniques, dtype=values.dtype)
    except TypeError:
        types = sorted(t.__qualname__ for t in set(type(v) for v in values))
        raise TypeError(
            "Encoders require their input argument must be uniformly "
            f"strings or numbers. Got {types}"
        )
    ret = (uniques,)

    if return_inverse:
        ret += (_map_to_integer(values, uniques),)

    if return_counts:
        ret += (_get_counts(values, uniques),)

    return ret[0] if len(ret) == 1 else ret




def _encode(values, *, uniques, check_unknown=True):
    """Helper function to encode values into [0, n_uniques - 1].

    Uses pure python method for object dtype, and numpy method for
    all other dtypes.
    The numpy method has the limitation that the `uniques` need to
    be sorted. Importantly, this is not checked but assumed to already be
    the case. The calling method needs to ensure this for all non-object
    values.

    Parameters
    ----------
    values : ndarray
        Values to encode.
    uniques : ndarray
        The unique values in `values`. If the dtype is not object, then
        `uniques` needs to be sorted.
    check_unknown : bool, default=True
        If True, check for values in `values` that are not in `unique`
        and raise an error. This is ignored for object dtype, and treated as
        True in this case. This parameter is useful for
        _BaseEncoder._transform() to avoid calling _check_unknown()
        twice.

    Returns
    -------
    encoded : ndarray
        Encoded values
    """
    if values.dtype.kind in "OUS":
        try:
            return _map_to_integer(values, uniques)
        except KeyError as e:
            raise ValueError(f"y contains previously unseen labels: {str(e)}")
    else:
        if check_unknown:
            diff = _check_unknown(values, uniques)
            if diff:
                raise ValueError(f"y contains previously unseen labels: {str(diff)}")
        return np.searchsorted(uniques, values)


def _map_to_integer(values, uniques):
    """Map values to integers based on a set of unique values."""
    return {val: i for i, val in enumerate(uniques)}[values]


def _check_unknown(values, uniques):
    """Check for unknown values in `values`."""
    return set(values) - set(uniques)



def _get_counts(values, uniques):
    """Get the count of each unique value in values."""
    if values.dtype.kind in "OU":
        return _get_counts_object(values, uniques)
    else:
        return _get_counts_numeric(values, uniques)


def _get_counts_object(values, uniques):
    """Get the count of each unique object value in values."""
    output = np.zeros(len(uniques), dtype=np.int64)
    for i, item in enumerate(uniques):
        output[i] = np.count_nonzero(values == item)
    return output


def _get_counts_numeric(values, uniques):
    """Get the count of each unique numeric value in values."""
    unique_values, counts = np.unique(values, return_counts=True)
    index_mapping = {val: i for i, val in enumerate(unique_values)}
    output = np.zeros_like(uniques, dtype=np.int64)
    for i, item in enumerate(uniques):
        if item in index_mapping:
            output[i] = counts[index_mapping[item]]
    return output


class MissingValues:
    def __init__(self, nan=False, none=False):
        self.nan = nan
        self.none = none

def _extract_missing(values):
    """Extract missing values from a set."""
    missing_values_set = {value for value in values if value is None or is_scalar_nan(value)}

    nan_present = np.nan in missing_values_set
    none_present = None in missing_values_set

    if not missing_values_set:
        return values, MissingValues(nan=False, none=False)

    return values - missing_values_set, MissingValues(nan=nan_present, none=none_present)


def is_scalar_nan(x):
    """Test if x is NaN.

    Parameters
    ----------
    x : any type
        Any scalar value.

    Returns
    -------
    bool
        Returns true if x is NaN, and false otherwise.
    """
    return (
        not isinstance(x, numbers.Integral)
        and isinstance(x, numbers.Real)
        and math.isnan(x)
    )