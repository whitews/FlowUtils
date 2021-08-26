"""
Various transforms for FCS data
"""

import numpy as np

# noinspection PyUnresolvedReferences
from . import logicle_c


def _logicle(y, t=262144, m=4.5, w=0.5, a=0):
    y = np.array(y, dtype='double')

    # noinspection PyUnresolvedReferences
    logicle_c.logicle_scale(t, w, m, a, y)
    return y


def _logicle_inverse(y, t=262144, m=4.5, w=0.5, a=0):
    y = np.array(y, dtype='double')

    # noinspection PyUnresolvedReferences
    logicle_c.logicle_inverse(t, w, m, a, y)
    return y


def logicle(
        data,
        channel_indices,
        t=262144,
        m=4.5,
        w=0.5,
        a=0
):
    """
    Logicle transformation, implemented as defined in the
    GatingML 2.0 specification:

    logicle(x, T, W, M, A) = root(B(y, T, W, M, A) − x)

    where B is a modified bi-exponential function defined as:

    B(y, T, W, M, A) = ae^(by) − ce^(−dy) − f

    The Logicle transformation was originally defined in the publication:

        Moore WA and Parks DR. Update for the logicle data scale including operational
        code implementations. Cytometry A., 2012:81A(4):273–277.

    :param data: NumPy array of FCS event data. If a 1-D array, channel_indices option is ignored
    :param channel_indices: channel indices to transform (other channels returned in place, untransformed).
        If None, then all events will be transformed.
    :param t: parameter for the top of the linear scale (e.g. 262144)
    :param m: parameter for the number of decades the true logarithmic scale
        approaches at the high end of the scale
    :param w: parameter for the approximate number of decades in the linear region
    :param a: parameter for the additional number of negative decades

    :return: NumPy array of transformed events
    """
    data_copy = data.copy()

    if len(data.shape) == 1:
        data_copy = _logicle(data_copy, t, m, w, a)
    else:
        # run logicle scale for each channel separately
        if channel_indices is None:
            channel_indices = range(data.shape[1])
        for i in channel_indices:
            tmp = _logicle(data_copy[:, i].T, t, m, w, a)
            data_copy.T[i] = tmp

    return data_copy


def logicle_inverse(
        data,
        channel_indices,
        t=262144,
        m=4.5,
        w=0.5,
        a=0
):
    """
    Inverse of the Logicle transformation (see `logicle()` documentation for more details)

    :param data: NumPy array of FCS event data. If a 1-D array, channel_indices option is ignored
    :param channel_indices: channel indices to transform (other channels returned in place, untransformed).
        If None, then all events will be transformed.
    :param t: parameter for the top of the linear scale (e.g. 262144)
    :param m: parameter for the number of decades the true logarithmic scale
        approaches at the high end of the scale
    :param w: parameter for the approximate number of decades in the linear region
    :param a: parameter for the additional number of negative decades

    :return: NumPy array of transformed events
    """
    data_copy = data.copy()

    if len(data.shape) == 1:
        data_copy = _logicle_inverse(data_copy, t, m, w, a)
    else:
        # run inverse logicle for each channel separately
        if channel_indices is None:
            channel_indices = range(data.shape[1])
        for i in channel_indices:
            tmp = _logicle_inverse(data_copy[:, i].T, t, m, w, a)
            data_copy.T[i] = tmp

    return data_copy


def _hyperlog(y, t=262144, m=4.5, w=0.5, a=0):
    y = np.array(y, dtype='double')

    # noinspection PyUnresolvedReferences
    logicle_c.hyperlog_scale(t, w, m, a, y)
    return y


def hyperlog(
        data,
        channel_indices,
        t=262144,
        m=4.5,
        w=0.5,
        a=0,
):
    """
    Hyperlog transformation, implemented as defined in the
    GatingML 2.0 specification:

    hyperlog(x, T, W, M, A) = root(EH(y, T, W, M, A) − x)

    where EH is defined as:

    EH(y, T, W, M, A) = ae^(by) + cy − f

    The Hyperlog transformation was originally defined in the publication:

        Bagwell CB. Hyperlog-a flexible log-like transform for negative, zero, and
        positive valued data. Cytometry A., 2005:64(1):34–42.

    :param data: NumPy array of FCS event data. If a 1-D array, channel_indices option is ignored
    :param channel_indices: channel indices to transform (other channels returned in place, untransformed).
        If None, then all events will be transformed.
    :param t: parameter for the top of the linear scale (e.g. 262144)
    :param m: parameter for desired number of decades
    :param w: parameter for the approximate number of decades in the linear region
    :param a: parameter for the additional number of negative decades

    :return: NumPy array of transformed events
    """
    data_copy = data.copy()

    if len(data.shape) == 1:
        data_copy = _hyperlog(data_copy, t, m, w, a)
    else:
        # run hyperlog scale for each channel separately
        if channel_indices is None:
            channel_indices = range(data.shape[1])
        for i in channel_indices:
            tmp = _hyperlog(data_copy[:, i].T, t, m, w, a)
            data_copy.T[i] = tmp

    return data_copy


def _hyperlog_inverse(y, t=262144, m=4.5, w=0.5, a=0):
    y = np.array(y, dtype='double')

    # noinspection PyUnresolvedReferences
    logicle_c.hyperlog_inverse(t, w, m, a, y)
    return y


def hyperlog_inverse(
        data,
        channel_indices,
        t=262144,
        m=4.5,
        w=0.5,
        a=0,
):
    """
    Inverse of the Hyperlog transformation, implemented as defined in the
    GatingML 2.0 specification (see hyperlog() documentation for more details).

    :param data: NumPy array of FCS event data. If a 1-D array, channel_indices option is ignored
    :param channel_indices: channel indices to transform (other channels returned in place, untransformed).
        If None, then all events will be transformed.
    :param t: parameter for the top of the linear scale (e.g. 262144)
    :param m: parameter for desired number of decades
    :param w: parameter for the approximate number of decades in the linear region
    :param a: parameter for the additional number of negative decades

    :return: NumPy array of transformed events
    """
    data_copy = data.copy()

    if len(data.shape) == 1:
        data_copy = _hyperlog_inverse(data_copy, t, m, w, a)
    else:
        # run hyperlog scale for each channel separately
        if channel_indices is None:
            channel_indices = range(data.shape[1])
        for i in channel_indices:
            tmp = _hyperlog_inverse(data_copy[:, i].T, t, m, w, a)
            data_copy.T[i] = tmp
    return data_copy


def asinh(data, channel_indices, t, m, a):
    """
    An implementation of the parametrized inverse hyperbolic sine function
    as defined in the GatingML 2.0 specification.

    :param data: NumPy array of FCS event data. If a 1-D array, channel_indices option is ignored
    :param channel_indices: channel indices to transform (other channels returned in place, untransformed).
        If None, then all events will be transformed.
    :param t: parameter specifying the top of the scale, (e.g. 262144)
    :param m: parameter for the number of decades
    :param a: parameter for the number of additional negative decades

    :return: NumPy array of transformed events
    """
    pre_scale = np.sinh(m * np.log(10)) / t
    transpose = a * np.log(10)
    divisor = (m + a) * np.log(10)

    data_copy = data.copy()

    if len(data.shape) == 1 or channel_indices is None:
        data_copy = (np.arcsinh(data_copy * pre_scale) + transpose) / divisor
    else:
        tmp_data = (np.arcsinh(data_copy[:, channel_indices] * pre_scale) + transpose) / divisor

        data_copy[:, channel_indices] = tmp_data

    return data_copy


def asinh_inverse(data, channel_indices, t, m, a):
    """
    Inverse of the parametrized inverse hyperbolic sine function
    as defined in the GatingML 2.0 specification.

    :param data: NumPy array of FCS event data. If a 1-D array, channel_indices option is ignored
    :param channel_indices: channel indices to transform (other channels returned in place, untransformed).
        If None, then all events will be transformed.
    :param t: parameter specifying the top of the scale, (e.g. 262144)
    :param m: parameter for the number of decades
    :param a: parameter for the number of additional negative decades

    :return: NumPy array of transformed events
    """
    pre_scale = np.sinh(m * np.log(10)) / t
    transpose = a * np.log(10)
    divisor = (m + a) * np.log(10)

    data_copy = data.copy()

    if len(data.shape) == 1 or channel_indices is None:
        data_copy = (np.sinh((data_copy * divisor) - transpose)) / pre_scale
    else:
        data_copy[:, channel_indices] = (np.sinh((data_copy[:, channel_indices] * divisor) - transpose)) / pre_scale

    return data_copy


def log(data, channel_indices, t, m):
    """
    Parametrized logarithmic transformation, implemented as defined in the
    GatingML 2.0 specification:

    flog(x, T, M) = (1 / M) * log_10(x / T) + 1

    :param data: NumPy array of FCS event data. If a 1-D array, channel_indices option is ignored
    :param channel_indices: channel indices to transform (other channels returned in place, untransformed).
        If None, then all events will be transformed.
    :param t: parameter for the top of the linear scale (e.g. 262144)
    :param m: parameter for desired number of decades

    :return: NumPy array of transformed events
    """
    data_copy = data.copy()

    if len(data.shape) == 1 or channel_indices is None:
        data_copy = (1. / m) * np.log10(data_copy / t) + 1.
    else:
        data_copy[:, channel_indices] = (1. / m) * np.log10(data_copy[:, channel_indices] / t) + 1.

    return data_copy


def log_inverse(data, channel_indices, t, m):
    """
    Inverse of logarithmic transformation

    :param data: NumPy array of FCS event data. If a 1-D array, channel_indices option is ignored
    :param channel_indices: channel indices to transform (other channels returned in place, untransformed).
        If None, then all events will be transformed.
    :param t: parameter for the top of the linear scale (e.g. 262144)
    :param m: parameter for desired number of decades

    :return: NumPy array of transformed events
    """
    data_copy = data.copy()

    if len(data.shape) == 1 or channel_indices is None:
        data_copy = t * (10 ** ((data_copy - 1) * m))
    else:
        data_copy[:, channel_indices] = t * (10 ** ((data_copy[:, channel_indices] - 1) * m))

    return data_copy
