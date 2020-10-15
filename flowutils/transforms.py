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


def asinh(data, columns, pre_scale):
    """
    return asinh transformed points (after pre-scaling) for indices listed
    """
    data_copy = data.copy()
    for c in columns:
        data_copy.T[c] = np.arcsinh(data_copy[:, c] * pre_scale)
    return data_copy


def log_transform(data, channels):
    n_points = data.copy()
    for i in channels:
        n_points[:, i] = _log_transform(n_points[:, i])
    return n_points


def _log_transform(npnts):
    return np.where(npnts <= 1, 0, np.log10(npnts))
