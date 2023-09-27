"""
Tests for 'compensate' module
"""
import unittest
import numpy as np
import pathlib
from flowutils import compensate

fcs_spill = '13,B515-A,R780-A,R710-A,R660-A,V800-A,V655-A,V585-A,V450-A,G780-A,G710-A,G660-A,G610-A,G560-A,'\
    '1,0,0,0.00008841570561316703,0.0002494559842740046,0.0006451591561972469,0.007198401782797728,0,0,'\
    '0.00013132619816952714,0.0000665251222573374,0.0005815839652764308,0.0025201730479353047,0,1,'\
    '0.07118758880093266,0.14844804153215532,0.3389031912802132,0.00971660311243448,0,0,0.3013801753249257,'\
    '0.007477611134717788,0.0123543122066652,0,0,0,0.33140488468849205,1,0.0619647566095391,0.12097867005182314,'\
    '0.004052554840959644,0,0,0.1091165124197372,0.10031383324016652,0.005831773047424356,0,0,0,'\
    '0.08862108746390694,0.38942413967608824,1,0.029758767352535288,0.06555281586224636,0,0,0.03129393154653089,'\
    '0.039305936245674286,0.09137451237674046,0.00039591122341817164,0.000056659766405160846,0,'\
    '0.13661791418865094,0.010757316236957385,0,1,0.00015647113960278087,0,0,0.48323487842103036,'\
    '0.01485813345103798,0,0,0,0,0.00012365104122837034,0.019462610460087203,0.2182062762553545,'\
    '0.004953221988365214,1,0.003582785726251024,0,0.0013106968243292993,0.029645575685206288,0.4089015923558522,'\
    '0.006505826616588717,0.00011917703878954761,0,0,0,0,0.001055595075733903,0.002287122431059274,1,0,'\
    '0.0003885172922042414,0.0001942589956485108,0,0.06255131165904257,0.13248446095817049,0,0,0,0,0,'\
    '0.008117870042687002,0.17006643956891296,1,0,0,0,0,0,0.003122390646560834,0.008525685683831916,'\
    '0.001024237027323255,0.0011626412849951272,0.12540105131097395,0.018142202256893485,0.19364562239714117,'\
    '0,1,0.06689784643460173,0.16145640353506588,0.2868231743828476,1.2380368696528024,0.002015498041918758,'\
    '0.06964529385206036,0.19471548842271394,0.0010077719457714136,0.15161117217667686,0.0012703511702660231,'\
    '0.007133491446011225,0,1.1500323358669722,1,0.016076827046672983,0.014674146885307975,0.055351746085494,'\
    '0.001685226072130514,0.05433993817875603,0.27785224557295884,0.34300826602551504,0.06175281041168121,'\
    '0.07752283973796613,0.0042628794531131406,0,0.49748791920091034,0.7439226300384197,1,0.010329232815907474,'\
    '0.03763461149817695,0,0.008713148000954844,0.04821275078920058,0.07319044343609345,0.1505631929508567,'\
    '0.3862934410767249,0.10189631814602482,0,0.3702770755789083,0.6134900271606913,1.2180240147472128,1,'\
    '0.06521131251063482,0.0016842378874079343,0,0,0.00009533732312150527,0.0034630076700367675,'\
    '0.01571183587491517,0.17412189188164517,0,0.023802192010810994,0.049474451704249904,0.13251071256825273,'\
    '0.23921555785727822,1'

fcs_spill_header = [
    'B515-A', 'R780-A', 'R710-A', 'R660-A',
    'V800-A', 'V655-A', 'V585-A', 'V450-A',
    'G780-A', 'G710-A', 'G660-A', 'G610-A',
    'G560-A'
]

test_data_npy_path = "tests/test_data/test_comp_event_data.npy"
test_comp_csv_path = "tests/test_data/test_comp_matrix.csv"
test_data_channels = [
    'FSC-A', 'FSC-W', 'SSC-A',
    'Ax488-A', 'PE-A', 'PE-TR-A',
    'PerCP-Cy55-A', 'PE-Cy7-A', 'Ax647-A',
    'Ax700-A', 'Ax750-A', 'PacBlu-A',
    'Qdot525-A', 'PacOrange-A', 'Qdot605-A',
    'Qdot655-A', 'Qdot705-A', 'Time'
]

test_data_fluoro_indices = []
for i, chan in enumerate(test_data_channels):
    if chan in ['FSC-A', 'FSC-W', 'SSC-A', 'Time']:
        continue
    test_data_fluoro_indices.append(i)

test_comp_matrix_channel_labels = [
    "Ax488-A",
    "PE-A",
    "PE-TR-A",
    "PerCP-Cy55-A",
    "PE-Cy7-A",
    "Ax647-A",
    "Ax700-A",
    "Ax750-A",
    "PacBlu-A",
    "Qdot525-A",
    "PacOrange-A",
    "Qdot605-A",
    "Qdot655-A",
    "Qdot705-A"
]


class CompensationTestCase(unittest.TestCase):
    """
    Tests for compensation related functions
    """
    def test_parse_fcs_spill_value(self):
        comp_matrix, header = compensate.get_spill(fcs_spill)

        self.assertIsInstance(comp_matrix, np.ndarray)
        self.assertTupleEqual(comp_matrix.shape, (13, 13))

    def test_parse_compensation_matrix(self):
        matrix_array = compensate.parse_compensation_matrix(fcs_spill, fcs_spill_header)

        self.assertIsInstance(matrix_array, np.ndarray)

    def test_parse_compensation_matrix_from_str(self):
        matrix_array = compensate.parse_compensation_matrix(
            test_comp_csv_path,
            test_comp_matrix_channel_labels
        )

        self.assertIsInstance(matrix_array, np.ndarray)

    def test_parse_compensation_matrix_from_path(self):
        comp_path = pathlib.Path(test_comp_csv_path)

        matrix_array = compensate.parse_compensation_matrix(
            comp_path,
            test_comp_matrix_channel_labels
        )

        self.assertIsInstance(matrix_array, np.ndarray)

    def test_parse_compensation_matrix_missing_row(self):
        comp_path = pathlib.Path("tests/test_data/test_comp_matrix_missing_row.csv")

        self.assertRaises(
            ValueError,
            compensate.parse_compensation_matrix,
            comp_path,
            test_comp_matrix_channel_labels
        )

    def test_validate_channel_label_sets_extra_header_label(self):
        header_labels = test_comp_matrix_channel_labels.copy()
        fluoro_labels = test_comp_matrix_channel_labels.copy()

        header_labels.append('extra_label')

        self.assertRaises(
            ValueError,
            compensate._validate_channel_label_sets,
            header_labels,
            fluoro_labels
        )

    def test_validate_channel_label_sets_missing_header_label(self):
        header_labels = test_comp_matrix_channel_labels.copy()
        fluoro_labels = test_comp_matrix_channel_labels.copy()

        header_labels.pop()

        self.assertRaises(
            ValueError,
            compensate._validate_channel_label_sets,
            header_labels,
            fluoro_labels
        )

    def test_parse_compensation_matrix_empty_matrix(self):
        self.assertRaises(
            ValueError,
            compensate.parse_compensation_matrix,
            "",
            test_comp_matrix_channel_labels
        )

    def test_compensate(self):
        npy_data = np.load(test_data_npy_path)
        spill = np.genfromtxt(test_comp_csv_path, delimiter=',', skip_header=True)

        comp_data = compensate.compensate(
            npy_data,
            spill,
            fluoro_indices=test_data_fluoro_indices
        )

        self.assertIsInstance(comp_data, np.ndarray)

    @staticmethod
    def test_inverse_compensate():
        npy_data = np.load(test_data_npy_path)
        spill = np.genfromtxt(test_comp_csv_path, delimiter=',', skip_header=True)

        comp_data = compensate.compensate(
            npy_data, spill, fluoro_indices=test_data_fluoro_indices
        )
        inv_comp_data = compensate.inverse_compensate(
            comp_data, spill, fluoro_indices=test_data_fluoro_indices
        )

        np.testing.assert_almost_equal(inv_comp_data, npy_data, 10)

    @staticmethod
    def test_compensate_no_indices():
        # test for compensate & inverse compensate
        npy_data = np.load(test_data_npy_path)
        spill = np.genfromtxt(test_comp_csv_path, delimiter=',', skip_header=True)

        all_fluoro_data = npy_data[:, test_data_fluoro_indices]

        # call both without fluoro_indices kwarg (defaults to None)
        comp_data = compensate.compensate(all_fluoro_data, spill)
        inv_comp_data = compensate.inverse_compensate(comp_data, spill)

        np.testing.assert_almost_equal(inv_comp_data, all_fluoro_data, 10)
