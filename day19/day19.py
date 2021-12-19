import copy
import itertools
import logging

import numpy as np


def load_input(input_path):
    """Load beacon coordinates for each scanner and store by scanner ID."""
    scanner_coords = dict()
    scanner_id = None
    beacon_list = []
    with open(input_path) as file_obj:
        for line in file_obj:
            if line.startswith('---'):
                if beacon_list:
                    scanner_coords[scanner_id] = np.array(beacon_list)
                    beacon_list = []
                scanner_id = int(line[12:].partition(' ')[0])
                continue
            if line.strip():
                beacon_list.append([int(val) for val in line.strip().split(',')])
    scanner_coords[scanner_id] = np.array(beacon_list)
    return scanner_coords


class ScannerData:
    """Store scanner ID and known coordinates for beacons and scanners.

    Initially, the only known scanner position is its own position at (0, 0).
    Two sets of aligned ScannerData can be merged to get a single map with the
    combined scanners' beacon and scanner coordinates.
    """

    def __init__(self, scanner_id=None, beacon_array=None, scanner_array=None, n_dims=3):
        logging.debug('Creating scanner %d', scanner_id)
        self.id = scanner_id
        if beacon_array is not None and not isinstance(beacon_array, np.ndarray):
            raise ValueError('Input beacon_array must be a numpy array.')
        if beacon_array is None:
            beacon_array = np.zeros((0, n_dims), dtype=np.int32)
        self.beacon_array = beacon_array
        if scanner_array is None:
            # initially, only known scanner position is own position at origin
            scanner_array = np.zeros((1, n_dims), dtype=np.int32)
        self.scanner_array = scanner_array

    def __str__(self):
        return str(self.beacon_array)

    def __len__(self):
        """Return number of known beacon positions."""
        return len(self.beacon_array)

    def merge(self, other):
        """Combine data for this scanner and another scanner."""
        new_id = self.id if self.id is not None else other.id
        new_beacon_array = np.unique(np.vstack([self.beacon_array, other.beacon_array]), axis=0)
        new_scanner_array = np.unique(np.vstack([self.scanner_array, other.scanner_array]), axis=0)
        return ScannerData(new_id, new_beacon_array, new_scanner_array)

    def translate(self, offsets):
        """Translate coordinates for known beacons and scanners."""
        self.beacon_array += offsets
        self.scanner_array += offsets


def transform(original_scanner, col_perm, orientation):
    """Return a copy of input ScannerData with specified transformations applied."""
    scanner = copy.deepcopy(original_scanner)
    scanner.beacon_array = scanner.beacon_array[:, col_perm]
    scanner.scanner_array = scanner.scanner_array[:, col_perm]
    for axis in orientation:
        scanner.beacon_array[:, axis] *= -1
        scanner.scanner_array[:, axis] *= -1
    return scanner


def align_scanners(scanner_list, expected_num=None, n_dims=3):
    """Align a list of ScannerData objects, and return the combined ScannerData.

    :param expected_num: optional, minimum number of beacons that should align
        between the data from two different scanners
    :param n_dims: optional, dimensionality of the space we're working with
    """
    if expected_num is None:
        expected_num = len(scanner_list[0].beacon_array)

    remaining_scanners_list = copy.deepcopy(scanner_list)
    aligned_scanners_ids = set()
    aligned_scanners_list = []
    for scanner_0 in scanner_list:
        aligned_scanner_data = ScannerData(n_dims=n_dims)
        for scanner_1 in remaining_scanners_list:
            if scanner_1.id == scanner_0.id:
                continue
            aligned_pair = align_pair(scanner_0, scanner_1, expected_num)
            if aligned_pair is None:
                logging.info('Could not find a match for scanner %d', scanner_1.id)
                continue
            aligned_scanners_ids.add(scanner_0.id)
            aligned_scanners_ids.add(scanner_1.id)
            logging.info('Aligned scanners %d and %d', scanner_0.id, scanner_1.id)
            aligned_scanner_data = aligned_scanner_data.merge(aligned_pair)

        remaining_scanners_list = [scanner for scanner in remaining_scanners_list
                                   if scanner.id not in aligned_scanners_ids]
        if aligned_scanner_data:
            aligned_scanners_list.append(aligned_scanner_data)
        if not remaining_scanners_list:
            return aligned_scanners_list


def align_pair(scanner_0, original_scanner_1, expected_num):
    """Attempt to align a pair of scanners.

    :param scanner_0: a ScannerData object
    :param scanner_1: a second ScannerData object to try to align with the first
    :param expected_num: optional int specifying the number of beacons that are
        expected to overlap if the scanner data is aligned
    :return: a new ScannerData object with the combined data from the two inputs
        if the alignment was successful, otherwise None
    """
    logging.debug('Coords 0:')
    logging.debug(scanner_0.beacon_array)

    n_dims = scanner_0.beacon_array.shape[1]
    orientations = [tuple()]
    for i in range(n_dims):
        orientations += list(itertools.combinations(range(n_dims), i+1))

    col_perms = itertools.permutations(range(n_dims))
    for col_perm in col_perms:
        for orientation in orientations:
            scanner_1 = transform(original_scanner_1, col_perm, orientation)
            for coords_0 in scanner_0.beacon_array:
                for coords_1 in scanner_1.beacon_array:
                    delta = coords_0 - coords_1
                    offset_beacon_array = scanner_1.beacon_array + delta
                    logging.debug('Offset beacon_list:')
                    logging.debug(offset_beacon_array)

                    coords_0_set = set((tuple(elem) for elem in scanner_0.beacon_array.tolist()))
                    offset_coords_set = set((tuple(elem) for elem in offset_beacon_array.tolist()))
                    num_common0 = len(coords_0_set & offset_coords_set)

                    combined_beacons = np.vstack([scanner_0.beacon_array, offset_beacon_array])
                    beacon_union = np.unique(combined_beacons, axis=0)
                    num_common = len(combined_beacons) - len(beacon_union)
                    if num_common0 != num_common:
                        raise RuntimeError('Incorrect calculation for num_common')

                    logging.debug(num_common / expected_num)
                    found_match = num_common / expected_num >= 1

                    if found_match:
                        scanner_1.translate(delta)
                        new_scanner = scanner_0.merge(scanner_1)
                        return new_scanner


def day19a(input_path, test=False):
    scanner_coords = load_input(input_path)
    logging.info('Finished loading input')
    scanner_list = []
    for scanner_id, beacon_list in scanner_coords.items():
        scanner_data = ScannerData(scanner_id, beacon_list)
        scanner_list.append(scanner_data)
    logging.info('Finished creating scanners')

    aligned_scanners_list = []
    iters = 0
    while len(aligned_scanners_list) != 1:
        if iters > 10:
            logging.warning('Could not align all scanners')
            break
        aligned_scanners_list = align_scanners(scanner_list, expected_num=12)
        scanner_list = aligned_scanners_list
        iters += 1

    num_beacons = len(aligned_scanners_list[0].beacon_array)
    logging.info('Number unique beacons: %d', num_beacons)

    # save beacon coordinates so we can use them for part 2
    fname = 'test_beacon_coords.txt' if test else 'beacon_coords.txt'
    np.savetxt(fname, aligned_scanners_list[0].scanner_array)
    return num_beacons


def test19a():
    scanner_coords = load_input('test_input0.txt')
    scanner_list = []
    for scanner_id, beacon_list in scanner_coords.items():
        scanner_data = ScannerData(scanner_id, beacon_list, n_dims=2)
        scanner_list.append(scanner_data)
    aligned_scanners_list = align_scanners(scanner_list, n_dims=2)
    assert len(aligned_scanners_list) == 1
    num_beacons = len(aligned_scanners_list[0].beacon_array)
    assert num_beacons == 3

    scanner_coords = load_input('test_input1.txt')
    scanner_list = []
    for scanner_id, beacon_list in scanner_coords.items():
        scanner_data = ScannerData(scanner_id, beacon_list)
        scanner_list.append(scanner_data)
    aligned_scanners_list = align_scanners(scanner_list)
    assert len(aligned_scanners_list) == 1
    num_beacons = len(aligned_scanners_list[0].beacon_array)
    assert num_beacons == 6
    assert len(aligned_scanners_list[0].scanner_array) == 1
    np.testing.assert_allclose(aligned_scanners_list[0].scanner_array,
                               np.zeros((1, 3)))

    assert 79 == day19a('test_input.txt', test=True)


def day19b(test=False):
    # cheat and use the beacon coordinates saved at the end of part 1
    fname = 'test_beacon_coords.txt' if test else 'beacon_coords.txt'
    aligned_coords_array = np.loadtxt(fname)
    max_dist = 0
    for coords_0, coords_1 in itertools.combinations(aligned_coords_array, 2):
        dist = np.sum(np.abs(coords_0 - coords_1))
        max_dist = max(max_dist, dist)
    return max_dist


def test19b():
    assert 3621 == day19b(test=True)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    test19a()
    print('Day 19a:', day19a('day19_input.txt'))
    test19b()
    print('Day 19b:', day19b('day19_input.txt'))
