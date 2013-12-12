"""
Various transforms for FCS data
"""

from scipy.optimize import brentq
from scipy import interpolate
import numpy

import logicle as clogicle


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
        return numpy.log(x - 4.0) - (1.0 - 1.0 / numpy.log(x)) * numpy.log(numpy.log(x))


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

    clogicle.logicle_scale(t, w, m, a, y)
    return y


def logicle(
        npy,
        channels,
        t,
        m,
        r=None,
        scale_max=1e5,
        w=0.5,
        a=0,
        r_quant=None):
    """
    return logicle transformed points for channels listed
    """
    npnts = npy.copy()
    for i in channels:
        if r_quant:
            w = None
            tmp = npnts[:, i]
            r = quantile(tmp[tmp < 0], 0.05)
        if r is None and w is None:
            w = 0.5
        tmp = scale_max * _logicle(npnts[:, i].T, t, m, r, w, a)
        npnts.T[i] = tmp
    return npnts


def eh(x, y, b, d, r):
    e = float(d) / r
    sgn = numpy.sign(x)
    return sgn * 10 ** (sgn * e * x) + b * e * x - sgn - y


def hyperlog0(y, b, d, r):
    return brentq(eh, -10 ** 6, 10 ** 6, (y, b, d, r))

hyperlog0 = numpy.vectorize(hyperlog0)


def _hyperlog(y, b, d, r, order=2, intervals=1000.0):
    ub = numpy.log(numpy.max(y) + 1 - numpy.min(y))
    xx = numpy.exp(numpy.arange(0, ub[0], ub / intervals)) - 1 + numpy.min(y)
    yy = hyperlog0(xx, b, d, r)
    t = interpolate.splrep(xx, yy, k=order)
    return interpolate.splev(y, t)


def hyperlog(npy, channels, b, d, r):
    npnts = npy.copy()
    for i in channels:
        npnts.T[i] = _hyperlog(
            npnts[:, i].T,
            b,
            d,
            r,
            order=2,
            intervals=1000.0)
    return npy


def log_transform(npy, channels):
    npnts = npy.copy()
    for i in channels:
        npnts[:, i] = _log_transform(npnts[:, i])
    return npnts


def _log_transform(npnts):
    return numpy.where(npnts <= 1, 0, numpy.log10(npnts))