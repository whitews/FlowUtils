"""
Various transforms for FCS data
"""

import numpy as np

# noinspection PyUnresolvedReferences
from . import logicle_c


def _quantile(x, n):
    """return the lower nth _quantile"""
    try:
        return sorted(x)[int(n * len(x))]
    except IndexError:
        return 0


def _logicle(y, t=262144, m=4.5, r=None, w=0.5, a=0):
    y = np.array(y, dtype='double')
    if w is None:  # we need an r then...
        if r == 0:
            w = 1  # don't like this but it works... FIX!
        else:
            w = (m - np.log10(t / np.abs(r))) / 2.0

    # noinspection PyUnresolvedReferences
    logicle_c.logicle_scale(t, w, m, a, y)
    return y


def _logicle_inverse(y, t=262144, m=4.5, r=None, w=0.5, a=0):
    y = np.array(y, dtype='double')
    if w is None:  # we need an r then...
        if r == 0:
            w = 1  # don't like this but it works... FIX!
        else:
            w = (m - np.log10(t / np.abs(r))) / 2.0

    # noinspection PyUnresolvedReferences
    logicle_c.logicle_inverse(t, w, m, a, y)
    return y


def logicle(
        data,
        channels,
        t=262144,
        m=4.5,
        r=None,
        w=0.5,
        a=0,
        r_quant=None):
    """
    return logicle transformed points for channels listed
    """
    data_copy = data.copy()

    # run logicle scale for each channel separately
    for i in channels:
        if r_quant:
            w = None
            tmp = data_copy[:, i]
            r = _quantile(tmp[tmp < 0], 0.05)
        if r is None and w is None:
            w = 0.5
        tmp = _logicle(data_copy[:, i].T, t, m, r, w, a)
        data_copy.T[i] = tmp
    return data_copy


def logicle_inverse(
        data,
        channels,
        t=262144,
        m=4.5,
        r=None,
        w=0.5,
        a=0,
        r_quant=None):
    """
    return inverse logicle transformed points for channels listed
    """
    data_copy = data.copy()

    # run logicle scale for each channel separately
    for i in channels:
        if r_quant:
            w = None
            tmp = data_copy[:, i]
            r = _quantile(tmp[tmp < 0], 0.05)
        if r is None and w is None:
            w = 0.5
        tmp = _logicle_inverse(data_copy[:, i].T, t, m, r, w, a)
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


def asinh(data, columns, pre_scale):
    """
    return asinh transformed points (after pre-scaling) for indices listed
    """
    data_copy = data.copy()
    for c in columns:
        data_copy.T[c] = np.arcsinh(data_copy[:, c] * pre_scale)
    return data_copy


def log_transform(npy, channels):
    n_points = npy.copy()
    for i in channels:
        n_points[:, i] = _log_transform(n_points[:, i])
    return n_points


def _log_transform(npnts):
    return np.where(npnts <= 1, 0, np.log10(npnts))
