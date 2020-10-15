import unittest
import numpy as np

from flowutils import transforms


class TransformsTestCase(unittest.TestCase):
    def setUp(self):
        self.test_data_range = np.linspace(0.0, 1000.0, 10001)

    @staticmethod
    def test_logicle_range():
        """Test a range of input values"""
        data_in = np.array([-10, -5, -1, 0, 0.3, 1, 3, 10, 100, 1000])
        correct_output = np.array(
            [
                0.067574,
                0.147986,
                0.228752,
                0.25,
                0.256384,
                0.271248,
                0.312897,
                0.432426,
                0.739548,
                1.0
            ]
        )

        # noinspection PyProtectedMember
        data_out = transforms._logicle(data_in, t=1000, m=4.0, w=1.0, a=0)

        np.testing.assert_array_almost_equal(data_out, correct_output, decimal=6)

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

    @staticmethod
    def test_hyperlog_range():
        """Test a range of input values"""
        data_in = np.array([-10, -5, -1, 0, 0.3, 1, 3, 10, 100, 1000])
        correct_output = np.array(
            [
                0.08355406,
                0.15586819,
                0.2294768,
                0.25,
                0.25623887,
                0.2705232,
                0.30909185,
                0.41644594,
                0.73187469,
                1.
            ]
        )

        # noinspection PyProtectedMember
        data_out = transforms._hyperlog(data_in, t=1000, m=4.0, w=1.0, a=0)

        np.testing.assert_array_almost_equal(data_out, correct_output, decimal=6)

    def test_inverse_hyperlog_transform(self):
        xform_data = transforms.hyperlog(
            self.test_data_range.reshape(-1, 1),
            [0],
            t=10000,
            w=0.5,
            m=4.5,
            a=0
        )
        x = transforms.hyperlog_inverse(
            xform_data,
            [0],
            t=10000,
            w=0.5,
            m=4.5,
            a=0
        )

        np.testing.assert_array_almost_equal(self.test_data_range, x[:, 0], decimal=10)

