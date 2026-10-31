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

    def test_scalar_bit_patterns_normal_subnormal(self):
        cases = [
            # Normal and subnormal results.
            (-300.0, "01a56e1fc2f8f359"),
            (-307.6526555685888, "000fffffffffffe3"),  # Just below min normal.
            (-307.6526555685887, "0010000000000231"),  # Just above min normal.
            (-308.0, "000730d67819e8d2"),
            (-323.0, "0000000000000002"),
            (-323.3062153431158, "0000000000000001"),  # Min positive subnormal.
            (-324.0, "0000000000000000"),  # Rounds to zero.
            (308.0, "7fe1ccf385ebc8a0"),
            (308.2, "7fec3647f1d600b6"),
            (309.0, "7ff0000000000000"),  # Overflow to infinity.
        ]

        for value, expected_hex in cases:
            with self.subTest(value=value):
                self.assert_bits(exp10(value), expected_hex)

    def test_special_values(self):
        self.assertEqual(exp10(float("inf")), float("inf"))
        self.assertEqual(exp10(float("-inf")), 0.0)
        self.assertTrue(math.isnan(exp10(float("nan"))))
