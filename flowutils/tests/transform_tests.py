"""
Tests for 'transform' module
"""
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
    def test_asinh_range():
        """Test a range of input values"""
        data_in = np.array([-10.0, -5.0, -1.0, 0.0, 0.3, 1.0, 3.0, 10.0, 100.0, 1000.0], dtype=float)
        data_in = data_in.reshape((-1, 1))
        correct_output = np.array(
            [[
                -0.200009,
                -0.139829,
                -0.000856,
                0.2,
                0.303776,
                0.400856,
                0.495521,
                0.600009,
                0.8,
                1.0
            ]]
        ).reshape((-1, 1))

        data_out = transforms.asinh(data_in, channel_indices=0, t=1000, m=4.0, a=1.0)

        np.testing.assert_array_almost_equal(data_out, correct_output, decimal=6)

    def test_inverse_asinh_transform(self):
        xform_data = transforms.asinh(
            self.test_data_range.reshape(-1, 1),
            [0],
            t=10000,
            m=4.5,
            a=0
        )
        x = transforms.asinh_inverse(
            xform_data,
            [0],
            t=10000,
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

    @staticmethod
    def test_log_range():
        """Test a range of input values"""
        data_in = np.array(
            [-1., 0., 0.5, 1., 10., 100., 1000., 1023., 10000., 100000, 262144],
            dtype=float
        )
        data_in = data_in.reshape((-1, 1))
        correct_output = np.array(
            [[
                np.nan,
                -np.inf,
                0.139794,
                0.2,
                0.4,
                0.6,
                0.8,
                0.801975,
                1.0,
                1.2,
                1.283708
            ]]
        ).reshape((-1, 1))

        with np.errstate(divide='ignore', invalid='ignore'):
            data_out = transforms.log(data_in, channel_indices=0, t=10000, m=5.0)

        np.testing.assert_array_almost_equal(data_out, correct_output, decimal=6)

    def test_inverse_log_transform(self):
        with np.errstate(divide='ignore'):
            xform_data = transforms.log(
                self.test_data_range.reshape(-1, 1),
                [0],
                t=10000,
                m=4.5
            )
        x = transforms.log_inverse(
            xform_data,
            [0],
            t=10000,
            m=4.5
        )

        np.testing.assert_array_almost_equal(self.test_data_range, x[:, 0], decimal=10)
