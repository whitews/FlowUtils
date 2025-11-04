"""
Tests for 'gating' module
"""
import unittest
import numpy as np

from flowutils import gating


class GatingTestCase(unittest.TestCase):
    @staticmethod
    def test_points_in_ellipse():
        cov_mat = [[62.5, 37.5], [37.5, 62.5]]
        coords = [12.99701, 16.22941]
        distance_square = 1.0

        npy_file_path = "tests/test_data/event_data_for_ellipse_test.npy"
        event_data = np.load(npy_file_path)

        truth_path = 'tests/test_data/truth/Results_Ellipse1.txt'
        truth = np.genfromtxt(truth_path, delimiter=',').astype('bool')

        result = gating.points_in_ellipsoid(
            cov_mat,
            coords,
            distance_square,
            event_data
        )

        np.testing.assert_array_equal(truth, result)

    @staticmethod
    def test_points_in_polygon1():
        poly_vertices = np.array(
            [
                [5., 5.],
                [500., 5.],
                [500., 500.]
            ]
        )

        # npy_file_path = "tests/test_data/poly1/poly1_events.npy"
        # event_data = np.load(npy_file_path)

        # These are the 3 "trouble" events incorrectly marked as outside gate
        # Keep these but comment out to revisit in case of future issues.
        event_data = np.array(
            [
                [ 5.88208437619687,  5.88208437619687],
                [ 8.659643233600654,  8.659643233600654],
                [13.455698580999508, 13.455698580999508]
            ]
        )

        # this file was exported from linux to evaluate if
        # the discrepancies originate from differences in
        # reading / parsing FCS event data.
        # npy_linux_file_path = "tests/test_data/poly1/poly1_events_linux.npy"
        # event_data_linux = np.load(npy_linux_file_path)

        # truth_path = 'tests/test_data/poly1/poly1_truth.npy'
        # truth = np.load(truth_path)

        truth = [True, True, True]

        result = gating.points_in_polygon(poly_vertices, event_data)
        # result_linux = gating.points_in_polygon(poly_vertices, event_data_linux)

        np.testing.assert_array_equal(truth, result)
        # np.testing.assert_array_equal(truth, result_linux)

    @staticmethod
    def test_points_in_polygon4():
        poly_vertices = np.array(
            [
                [5., 5.],
                [500., 5.],
                [500., 500.]
            ]
        )

        npy_file_path = "tests/test_data/event_data_for_poly_test.npy"
        event_data = np.load(npy_file_path)

        truth_path = 'tests/test_data/truth/Results_Polygon4.txt'
        truth = np.genfromtxt(truth_path, delimiter=',').astype('bool')

        result = gating.points_in_polygon(poly_vertices, event_data)

        np.testing.assert_array_equal(truth, result)
