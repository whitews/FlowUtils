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
        channels,
        t=262144,
        m=4.5,
        w=0.5,
        a=0
):
    """
    return logicle transformed points for channels listed
    """
    data_copy = data.copy()

    # run logicle scale for each channel separately
    for i in channels:
        tmp = _logicle(data_copy[:, i].T, t, m, w, a)
        data_copy.T[i] = tmp
    return data_copy


def logicle_inverse(
        data,
        channels,
        t=262144,
        m=4.5,
        w=0.5,
        a=0
):
    """
    return inverse logicle transformed points for channels listed
    """
    data_copy = data.copy()

    # run logicle scale for each channel separately
    for i in channels:
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
        channels,
        t=262144,
        m=4.5,
        w=0.5,
        a=0,
):
    """
    return hyperlog transformed points for channels listed
    """
    data_copy = data.copy()

    # run hyperlog scale for each channel separately
    for i in channels:
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
        channels,
        t=262144,
        m=4.5,
        w=0.5,
        a=0,
):
    """
    return hyperlog transformed points for channels listed
    """
    data_copy = data.copy()

    # run hyperlog scale for each channel separately
    for i in channels:
        tmp = _hyperlog_inverse(data_copy[:, i].T, t, m, w, a)
        data_copy.T[i] = tmp
    return data_copy


def asinh(data, channel_indices, t, m, a):
    """
    An implementation of the parametrized inverse hyperbolic sine function
    as defined in the GatingML 2.0 specification.

    :param data: NumPy array of FCS event data
    :param channel_indices: channel indices to transform (other channels returned in place, untransformed)
    :param t: parameter specifying the top of the scale, (e.g. 262144)
    :param m: parameter for the number of decades
    :param a: parameter for the number of additional negative decades

    :return: NumPy array of transformed events
    """
    pre_scale = np.sinh(m * np.log(10)) / t
    transpose = a * np.log(10)
    divisor = (m + a) * np.log(10)

    data_copy = data.copy()

    tmp_data = (np.arcsinh(data_copy[:, channel_indices] * pre_scale) + transpose) / divisor

    data_copy[:, channel_indices] = tmp_data

    return data_copy


def asinh_inverse(data, channel_indices, t, m, a):
    """
    Inverse of the parametrized inverse hyperbolic sine function
    as defined in the GatingML 2.0 specification.

    :param data: NumPy array of FCS event data
    :param channel_indices: channel indices to transform (other channels returned in place, untransformed)
    :param t: parameter specifying the top of the scale, (e.g. 262144)
    :param m: parameter for the number of decades
    :param a: parameter for the number of additional negative decades

    :return: NumPy array of transformed events
    """
    pre_scale = np.sinh(m * np.log(10)) / t
    transpose = a * np.log(10)
    divisor = (m + a) * np.log(10)

    data_copy = data.copy()
    data_copy[:, channel_indices] = (np.sinh((data_copy[:, channel_indices] * divisor) - transpose)) / pre_scale

    return data_copy


def log(data, channel_indices, t, m):
    """
    Parametrized logarithmic transformation, implemented as defined in the
    GatingML 2.0 specification:

    flog(x, T, M) = (1 / M) * log_10(x / T) + 1

    :param data: NumPy array of FCS event data
    :param channel_indices: channel indices to transform (other channels returned in place, untransformed)
    :param t: parameter for the top of the linear scale (e.g. 262144)
    :param m: parameter for desired number of decades

    :return: NumPy array of transformed events
    """
    data_copy = data.copy()
    data_copy[:, channel_indices] = (1. / m) * np.log10(data_copy[:, channel_indices] / t) + 1.

    return data_copy


def log_inverse(data, channel_indices, t, m):
    """
    Inverse of logarithmic transformation

    :param data: NumPy array of FCS event data
    :param channel_indices: channel indices to transform (other channels returned in place, untransformed)
    :param t: parameter for the top of the linear scale (e.g. 262144)
    :param m: parameter for desired number of decades

    :return: NumPy array of transformed events
    """
    data_copy = data.copy()
    data_copy[:, channel_indices] = t * (10 ** ((data_copy[:, channel_indices] - 1) * m))

    return data_copy
