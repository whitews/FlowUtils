import unittest

from .transform_tests import TransformsTestCase
from .compensation_tests import CompensationTestCase, SpectralCompensationTestCase
from .gating_tests import GatingTestCase
from .exp10_tests import CoreMathExp10TestCase

if __name__ == "__main__":
    unittest.main()
