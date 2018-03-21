import unittest
import numpy as np

from flowutils import transforms


class LogicleTestCase(unittest.TestCase):
    """Tests for logicle transformation"""
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
        data_out = transforms._logicle(data_in, t=1000, m=4.0, r=None, w=1.0, a=0)

        np.testing.assert_array_almost_equal(data_out, correct_output, decimal=6)


if __name__ == '__main__':
    unittest.main()
