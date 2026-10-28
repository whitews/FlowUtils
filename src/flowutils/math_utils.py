import numpy as np

try:
    from . import exp10_c
except ImportError:
    # Error message if the C compilation failed or is missing
    raise ImportError(
        "The FlowUtils C extensions are not compiled or missing. "
        "Please re-install FlowUtils or build from source."
    )


def exp10(array: np.ndarray) -> np.ndarray:
    """
    Correctly rounded 10^x exponential transformation using CORE-MATH.

    Guarantees cross-platform, deterministic, bit-perfect results
    across Linux, macOS, and Windows down to 0 ULP.

    :param array: np.ndarray A numeric array (typically float64) of flow cytometry events
    :return: np.ndarray The transformed array matching the dimensions of the input.
    """

    # Map Python API call to the CORE-MATH C function
    return exp10_c.exp10_c(array)
