import numpy as np
import re
import os
from pathlib import Path


def get_spill(text):
    """
    Extracts spillover matrix from FCS text entry.

    :param text: Text value from the $SPILL or $SPILLOVER metadata keyword in an FCS file
    :return: A tuple containing: (spillover matrix new_spill, column headers)
    """
    spill = text.split(',')
    n = int(spill[0])
    markers = spill[1:(n + 1)]
    markers = [item.strip().replace('\n', '') for item in markers]
    items = [item.strip().replace('\n', '') for item in spill[n + 1:]]
    new_spill = np.reshape(list(map(float, items)), (n, n))
    return new_spill, markers


def _parse_multiline_matrix(matrix_text, fluoro_labels):
    # first, we must find a valid header line and we will require that the matrix
    # follows on the next lines, ignoring any additional lines before or after
    # the header contains labels matching the PnN value(FCS text field)
    # and may be tab or comma delimited
    # (spaces can't be delimiters b/c they are allowed in the PnN value)
    header = None
    header_line_index = None
    for i, line in enumerate(matrix_text):
        # header may begin with a '#' and some white space
        match = re.search('^#\\s*', line)
        if match is not None:
            line = line[match.end():]
        line_values = re.split('[\t,]', line)

        label_diff = set(fluoro_labels).symmetric_difference(line_values)

        if len(label_diff) != 0:
            # if any labels are missing or extra ones found, then not a valid header row
            continue
        else:
            header = line_values
            header_line_index = i
            break

    matrix_start = header_line_index + 1
    matrix_end = matrix_start + len(fluoro_labels)

    if len(matrix_text) < matrix_end:
        raise ValueError("Too few rows in compensation")

    matrix_text = matrix_text[matrix_start:matrix_end]
    matrix_array = []

    # convert the matrix text to numpy array
    for line in matrix_text:
        line_values = re.split('[\t,]', line)
        line_values = [float(value) for value in line_values]

        if len(line_values) > len(fluoro_labels):
            raise ValueError("Too many values in line: %s" % line)
        elif len(line_values) < len(fluoro_labels):
            raise ValueError("Too few values in line: %s" % line)
        else:
            matrix_array.append(line_values)

    matrix_array = np.array(matrix_array)

    return matrix_array, header


def _convert_matrix_text_to_array(matrix_text, fluoro_labels, fluoro_indices):
    """
    Converts a compensation matrix from a CSV text string to a NumPy array

    :param matrix_text: CSV text string where header contains the fluoro labels
    :param fluoro_labels: text labels of the FCS fluorescent channels
    :param fluoro_indices: channel indices of the fluorescent channels

    :return: NumPy array of the compensation matrix values
    """
    # parse the matrix text and validate the number of params match
    # the number of fluoro params and that the matrix
    # values are numbers (can be exp notation)
    matrix_text = matrix_text.splitlines()

    if len(matrix_text) == 0:
        raise ValueError("matrix text appears to be empty")
    elif len(matrix_text) == 1:
        # probably a single-line CSV from FCS metadata
        matrix, header = get_spill(matrix_text[0])
    else:
        matrix, header = _parse_multiline_matrix(matrix_text, fluoro_labels)

    label_diff = set(fluoro_labels).symmetric_difference(header)

    # re-order matrix according to provided fluoro label order
    idx_order = [header.index(fluoro_label) for fluoro_label in fluoro_labels]
    matrix = matrix[idx_order, :][:, idx_order]

    if len(label_diff) > 0:
        in_fcs_not_comp = []
        in_comp_not_fcs = []

        for label in label_diff:
            if label in fluoro_labels:
                in_fcs_not_comp.append(label)
            else:
                in_comp_not_fcs.append(label)

        error_message = "Matrix labels do not match given fluorescent labels"

        if len(in_fcs_not_comp) > 0:
            error_message = "\n".join(
                [
                    error_message,
                    "",
                    "Labels in FCS file not found in comp matrix (null channels?):",
                    ", ".join(in_fcs_not_comp),
                    "",
                    "Null channels can be specified when creating a Sample instance"
                ]
            )

        if len(in_comp_not_fcs) > 0:
            error_message = "\n".join(
                [
                    error_message,
                    "",
                    "Labels in comp matrix not found in FCS file (wrong matrix chosen?):",
                    ", ".join(in_comp_not_fcs)
                ]
            )

        raise ValueError(error_message)

    header_channel_numbers = []

    for h in header:
        # check if label is in given fluoro labels, will raise a ValueError if missing
        # Note: this will give us the index of the given fluoro labels, which is not the
        # index of the fluoro channel in the original FCS file because of scatter channels,
        # etc. We look up the 'true' index from given fluoro_indices. Also, we increment
        # to match the original PnN numbers that index from 1 (not 0).
        # We store the channel number in the first row of the numpy array, as it is more
        # reliable to identify parameters than some concatenation of parameter attributes.
        fluoro_index = fluoro_labels.index(h)
        true_fluoro_index = fluoro_indices[fluoro_index]
        header_channel_numbers.append(true_fluoro_index + 1)

    matrix_array = np.vstack([header_channel_numbers, matrix])

    return matrix_array


def parse_compensation_matrix(compensation, channel_labels, null_channels=None):
    """
    Returns a NumPy array with the compensation matrix, where the first row contains
    the indices of the fluorescent channels

    :param compensation: Compensation matrix: may be a NumPy array, a CSV file
        path, a pathlib Path object to a CSV or TSV file or a string of CSV
        text. If a string, both multi-line, traditional CSV, and the single
        line FCS spill formats are supported. If a NumPy array, we assume the
        columns are in the same order as the channel labels
    :param channel_labels: Channel labels from the FCS file's PnN fields, must be in
        the same order as they appear in the FCS file
    :param null_channels: Specify any empty channels that were collected and
        present in the channel_labels argument. These will be ignored when
        validating and creating the compensation matrix
    :return: Compensation matrix as NumPy array where header contains the
        channel numbers (not indices!)
    """
    non_fluoro_channels = [
        'FSC-A',
        'FSC-H',
        'FSC-W',
        'SSC-A',
        'SSC-H',
        'SSC-W',
        'Time'
    ]

    fluoro_indices = []
    fluoro_labels = []

    if null_channels is not None:
        non_fluoro_channels.extend(null_channels)

    for i, label in enumerate(channel_labels):
        if label not in non_fluoro_channels:
            fluoro_indices.append(i)
            fluoro_labels.append(label)

    # Determine compensation object type
    if isinstance(compensation, str):
        # if a string, may be a file path or CSV text, we'll first test if file path exists
        # and if so try and open as CSV. If this fails, we'll test splitting the string by
        # new lines and commas. If this fails, raise a ValueError
        if os.path.isfile(compensation):
            fh = open(compensation)
            matrix_text = fh.read()
            fh.close()
        else:
            # may be a CSV string
            matrix_text = compensation

        matrix = _convert_matrix_text_to_array(matrix_text, fluoro_labels, fluoro_indices)

    elif isinstance(compensation, Path):
        fh = compensation.open('r')
        matrix_text = fh.read()
        fh.close()

        matrix = _convert_matrix_text_to_array(matrix_text, fluoro_labels, fluoro_indices)
    elif isinstance(compensation, np.ndarray):
        matrix = compensation
    else:
        raise ValueError("Compensation given is not a string or a NumPy array")

    # Make sure we have the correct number of rows (the header of matrix adds a row)
    if matrix.shape[0] > len(fluoro_labels) + 1:
        raise ValueError("Too many rows in compensation matrix")
    elif matrix.shape[0] < len(fluoro_labels) + 1:
        raise ValueError("Too few rows in compensation matrix")

    return matrix


def compensate(event_data, spill_matrix, fluoro_indices=None):
    """
    Compensate NumPy event data 'npy' given spillover matrix 'spill'
    and marker indices to compensate.

    :param event_data: NumPy array of the event data
    :param spill_matrix: Compensation matrix as a NumPy array (without headers)
    :param fluoro_indices: Optional list of indices of the fluorescent channels (only
        these will be extracted & compensated). If None (default), all columns
        will be compensated.

    :return: NumPy array of compensated event data. If fluoro_indices were given,
        the data is returned in the column order given, with the non-fluorescent
        columns unmodified.
    """
    data = event_data.copy()
    if len(fluoro_indices) > 0:
        comp_data = data[:, fluoro_indices]
    else:
        comp_data = data

    # this does the actual compensation
    comp_data = np.linalg.solve(spill_matrix.T, comp_data.T).T

    # Re-insert compensated data columns
    if len(fluoro_indices) > 0:
        data[:, fluoro_indices] = comp_data
    else:
        data = comp_data

    return data


def inverse_compensate(event_data, spill_matrix, fluoro_indices=None):
    """
    Inverse the compensation on NumPy event data 'npy' given spillover matrix 'spill'
    and marker indices to "un-compensate".

    :param event_data: NumPy array of the event data
    :param spill_matrix: Compensation matrix as a NumPy array (without headers)
    :param fluoro_indices: Optional list of indices of the fluorescent channels (only
        these will be extracted & un-compensated). If None (default), all columns
        will be un-compensated.

    :return: NumPy array of un-compensated event data. If fluoro_indices were given,
        the data is returned in the column order given, with the non-fluorescent
        columns unmodified.
    """
    data = event_data.copy()
    if len(fluoro_indices) > 0:
        inv_comp_data = data[:, fluoro_indices]
    else:
        inv_comp_data = data

    inv_comp_data = np.dot(inv_comp_data, spill_matrix)

    # Re-insert compensated data columns
    if len(fluoro_indices) > 0:
        data[:, fluoro_indices] = inv_comp_data
    else:
        data = inv_comp_data

    return data


def gen_spill_matrix(npy, stain_index):
    """
    Generates spillover matrix for one FCS file (presumably from beads)

    :param npy: the numpy array of the bead data
    :param stain_index: index of the stained channel

    :return: Compensation matrix as a NumPy array (without headers)
    """

    # get the median for all unstained columns, zero for stained index
    spill = list()
    for column, i in enumerate(npy.T):
        if i == stain_index:
            spill.append(0.0)
            continue
        else:
            spill.append(np.median(column))
        
    return spill
