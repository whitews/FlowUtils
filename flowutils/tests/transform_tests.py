import unittest
import numpy as np

from flowutils import transforms


class TransformsTestCase(unittest.TestCase):
    def setUp(self):
        self.test_data_range = np.linspace(0.0, 10.0, 101)

    def test_inverse_logicle_transform(self):
        xform_data = transforms.logicle(
            self.test_data_range.reshape(-1, 1),
            [0],
            t=10000,
            w=0.5,
            m=4.5,
            a=0
        )
        x = transforms.logicle_inverse(
            xform_data,
            [0],
            t=10000,
            w=0.5,
            m=4.5,
            a=0
        )

        np.testing.assert_array_almost_equal(self.test_data_range, x[:, 0], decimal=10)
