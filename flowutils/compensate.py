from numpy import reshape, max, median
from numpy.linalg import solve, inv


def get_spill(text):
    """Extracts spillover matrix from FCS text entry.

    Returns (spillover matrix new_spill, column headers)
    """
    spill = text.split(',')
    n = int(spill[0])
    markers = spill[1:(n + 1)]
    markers = [item.strip().replace('\n', '') for item in markers]
    items = [item.strip().replace('\n', '') for item in spill[n + 1:]]
    new_spill = reshape(map(float, items), (n, n))
    return new_spill, markers


def compensate(npy, spill, indices=None, comp=False, scale=False):
    """
    Compensate numpy data 'npy' given spillover matrix 'spill'
    and markers to compensate
    If markers are not given, will look for fcm.annotate.text['SPILL']
    """
    data = npy.copy()
    if indices:
        data = data[:, indices]

    if scale and not comp:
        spill = spill / max(spill)
    if comp:
        spill = inv(spill)

    return solve(spill.T, data.T).T


def gen_spill_matrix(npy, stain_index):
    """
    Generates spillover matrix for one FCS file (presumably from beads)
    npy: the numpy array of the bead data
    stain_index: index of the stained channel
    """

    # get the median for all unstained columns, zero for stained index
    spill = list()
    for column, i in enumerate(npy.T):
        if i == stain_index:
            spill.append(0.0)
            continue
        else:
            spill.append(median(column))
        
    return spill