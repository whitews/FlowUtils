"""
Various transforms for FCS data
"""

import numpy

from flowutils import logicle_c


def quantile(x, n):
    """return the lower nth quantile"""
    try:
        return sorted(x)[int(n * len(x))]
    except IndexError:
        return 0


def product_log(x):
    """
    Product logarithm or LambertW function computes principal solution
    for w in f(w) = w*exp(w).
    """
    #  fast estimate with closed-form approximation
    if x <= 500:
        lxl = numpy.log(x + 1.0)
        return 0.665 * (1 + 0.0195 * lxl) * lxl + 0.04
    else:
        return numpy.log(x - 4.0) - \
               (1.0 - 1.0 / numpy.log(x)) * numpy.log(numpy.log(x))


def s(x, y, t, m, w):
    p = w / (2 * product_log(0.5 * numpy.exp(-w / 2) * w))
    sgn = numpy.sign(x - w)
    xw = sgn * (x - w)
    return sgn * t * numpy.exp(-(m - w)) * (numpy.exp(xw) - p ** 2 * numpy.exp(-xw / p) + p ** 2 - 1) - y


def _logicle(y, t=262144, m=4.5, r=None, w=0.5, a=0):
    y = numpy.array(y, dtype='double')
    if w is None:  # we need an r then...
        if r == 0:
            w = 1  # don't like this but it works... FIX!
        else:
            w = (m - numpy.log10(t / numpy.abs(r))) / 2.0

    # noinspection PyUnresolvedReferences
    logicle_c.logicle_scale(t, w, m, a, y)
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
            r = quantile(tmp[tmp < 0], 0.05)
        if r is None and w is None:
            w = 0.5
        tmp = _logicle(data_copy[:, i].T, t, m, r, w, a)
        data_copy.T[i] = tmp
    return data_copy


def asinh(data, columns, pre_scale):
    """
    return asinh transformed points (after pre-scaling) for indices listed
    """
    data_copy = data.copy()
    for c in columns:
        data_copy.T[c] = numpy.arcsinh(data_copy[:, c] * pre_scale)
    return data_copy


def log_transform(npy, channels):
    n_points = npy.copy()
    for i in channels:
        n_points[:, i] = _log_transform(n_points[:, i])
    return n_points


def _log_transform(npnts):
    return numpy.where(npnts <= 1, 0, numpy.log10(npnts))
