import math
import struct
import unittest
import numpy as np
from flowutils.math_utils import exp10


class CoreMathExp10TestCase(unittest.TestCase):
    def assert_bits(self, value, expected_hex, msg=""):
        """
        Helper function to assert exact bit-per-bit identity via raw float binary representations.
        """
        # Convert to a native Python float if it's a NumPy scalar
        result = float(value)

        # Convert float64 value to big-endian IEEE 754 double precision binary (8 bytes)
        # Then, convert to hexadecimal string
        actual_hex = struct.pack(">d", result).hex()

        # Format given expected hex string to match the above hex format:
        # Ensure lowercase, remove "0x" prefix if present, & zero pad left side to guarantee 16 chars
        expected_hex = expected_hex.lower().removeprefix("0x").zfill(16)

        self.assertEqual(
            actual_hex,
            expected_hex,
            f"{msg} Failure for input {value}. Expected bits {expected_hex}, got 0x{actual_hex}"
        )

    def test_flowio_problematic_cases(self):
        """Regression tests for inputs that previously caused 1-ULP drifts across platforms."""
        # Case 1: 1.13671875
        self.assert_bits(
            exp10(1.13671875),
            "0x402b665ee2f7005d",
            "FlowIO Drift Case 1"
        )

        # Case 2: 0.3125
        self.assert_bits(
            exp10(0.3125),
            "0x40006d9e87713534",
            "FlowIO Drift Case 2"
        )

    def test_array_and_multidimensional(self):
        """Ensures the C wrapper handles NumPy array shapes, strides, and memory layouts correctly."""
        # 1D Array verification
        inputs = np.array([1.13671875, 0.3125], dtype=np.float64)
        outputs = exp10(inputs)

        self.assertEqual(f"{outputs[0].view(np.uint64):x}", "402b665ee2f7005d")
        self.assertEqual(f"{outputs[1].view(np.uint64):x}", "40006d9e87713534")

        # Multidimensional Shape Conservation (e.g. 2D event matrices)
        matrix_in = np.array([[1.13671875], [0.3125]], dtype=np.float64)
        matrix_out = exp10(matrix_in)
        self.assertEqual(matrix_out.shape, matrix_in.shape)

    def test_scalar_bit_patterns_simple_powers_and_signed_zero(self):
        cases = [
            # Exact/simple powers and signed zero.
            (0.0, "3ff0000000000000"),
            (-0.0, "3ff0000000000000"),
            (1.0, "4024000000000000"),
            (2.0, "4059000000000000"),
            (-1.0, "3fb999999999999a")
        ]

        for value, expected_hex in cases:
            with self.subTest(value=value):
                self.assert_bits(exp10(value), expected_hex)

    def test_special_values(self):
        self.assertEqual(exp10(float("inf")), float("inf"))
        self.assertEqual(exp10(float("-inf")), 0.0)
        self.assertTrue(math.isnan(exp10(float("nan"))))

    def test_mathematical_edge_cases(self):
        """Verifies mathematical thresholds, limits, and floating point corner-cases."""
        # Zero threshold boundary rules
        self.assert_bits(exp10(0.0), "0x3ff0000000000000")  # Exactly 1.0
        self.assert_bits(exp10(-0.0), "0x3ff0000000000000")  # Exactly 1.0

        # Integer boundary powers
        self.assert_bits(exp10(1.0), "0x4024000000000000")  # Exactly 10.0
        self.assert_bits(exp10(2.0), "0x4059000000000000")  # Exactly 100.0
        self.assert_bits(exp10(-1.0), "0x3fb999999999999a")  # Exactly 0.1

        # Subnormal and Underflow Bounds (FCS files with highly compressed/scaled channels)
        # 10^-300 pushes near the absolute limits of double precision float bounds
        self.assert_bits(exp10(-300.0), "0x01a56e1fc2f8f359")  # Flirts with the minimal subnormal limit

        # Test the absolute subnormal limit edge case
        # NOTE: This is a curiosity & would be expected to fail across some machines.
        #       Leaving here but commented out for deployment.
        #self._assert_bit_perfect(-323.3062153431158, "0x0000000000000001")
