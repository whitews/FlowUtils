from typing import overload
import numpy as np

try:
    from . import exp10_c
except ImportError:
    # Error message if the C compilation failed or is missing
    raise ImportError(
        "The FlowUtils C extensions are not compiled or missing. "
        "Please re-install FlowUtils or build from source."
    )

__all__ = ['exp10']

@overload
def exp10(x: np.ndarray) -> np.ndarray: ...

@overload
def exp10(x: float) -> float: ...

@overload
def exp10(x: int) -> float: ...

def exp10(x):
    """
    Correctly rounded 10^x exponential transformation using CORE-MATH.

    Guarantees cross-platform, deterministic, bit-perfect results
    across Linux, macOS, and Windows down to 0 ULP.

    Parameters
    ----------
    x : ndarray, float, or int
        The exponent value(s) to process. Typically, a float64 array of flow
        cytometry events or a single numeric scalar. Regular Python lists are
        not accepted.

    Returns
    -------
    ndarray or float
        The transformed result. Returns a ndarray matching the dimensions of
        the input, or native Python float if given an int or float.
    """

    # Map Python API call to the CORE-MATH C function
    return exp10_c.exp10_c(x)
