import copy
import itertools
import logging

import numpy as np


def load_input(input_path):
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

    def __init__(self, scanner_id, beacon_beacon_list):
        logging.debug('Creating scanner %d', scanner_id)
        self.id = scanner_id
        self.beacon_list = beacon_beacon_list

    def __str__(self):
        return str(self.beacon_list)


class ScannerMap:

    def __init__(self, beacon_coords_set, scanner_beacon_list):
        self.beacon_coords_set = beacon_coords_set
        self.scanner_beacon_list = scanner_beacon_list


def align_scanners(scanner_list, expected_num=None):

    if expected_num is None:
        expected_num = len(scanner_list[0].beacon_list)

    remaining_scanners_list = copy.deepcopy(scanner_list)
    aligned_scanners_ids = set()
    aligned_beacon_list = []
    for scanner_0 in scanner_list:
        aligned_coords_set = set()
        for scanner_1 in remaining_scanners_list:
            if scanner_1.id == scanner_0.id:
                continue
            scanner_map = align_pair(scanner_0, scanner_1, expected_num)
            if scanner_map is None:
                logging.warning('Could not find a match for scanner %d', scanner_1.id)
                continue
            aligned_scanners_ids.add(scanner_0.id)
            aligned_scanners_ids.add(scanner_1.id)
            logging.info('Aligned scanners %d and %d', scanner_0.id, scanner_1.id)
            aligned_coords_set |= normalized_coords_set
        remaining_scanners_list = [
            scanner for scanner in remaining_scanners_list
            if scanner.id not in aligned_scanners_ids]
        if aligned_coords_set:
            aligned_beacon_list.append(aligned_coords_set)
        if not remaining_scanners_list:
            return aligned_beacon_list


def align_pair(scanner_0, scanner_1, expected_num):

    beacon_list_0 = scanner_0.beacon_list

    logging.debug('Coords 0:')
    logging.debug(beacon_list_0)

    n_dims = beacon_list_0.shape[1]
    orientations = [tuple()]
    for i in range(n_dims):
        orientations += list(itertools.combinations(range(n_dims), i+1))

    max_common = 0
    col_perms = itertools.permutations(range(n_dims))
    for col_perm in col_perms:
        swapped_cols = np.copy(scanner_1.beacon_list[:, col_perm])

        for orientation in orientations:

            reoriented = np.copy(swapped_cols)
            for axis in orientation:
                reoriented[:, axis] *= -1

            for coords_0 in beacon_list_0:
                for coords_1 in reoriented:
                    delta = coords_0 - coords_1
                    offset_beacon_list = reoriented + delta
                    logging.debug('Offset beacon_list:')
                    logging.debug(offset_beacon_list)

                    coords_0_set = set((tuple(elem) for elem in beacon_list_0.tolist()))
                    offset_coords_set = set((tuple(elem) for elem in offset_beacon_list.tolist()))

                    num_common = len(coords_0_set & offset_coords_set)
                    max_common = max(max_common, num_common)
                    logging.debug(num_common / expected_num)
                    found_match = num_common / expected_num >= 1
                    if found_match:
                        logging.info('Found match')
                        beacon_coords_set = coords_0_set | offset_coords_set
                        scanner_beacon_list =
                        ScannerMap(beacon_coords_set, scanner_beacon_list)
                        return aligned_coords_set, delta

    logging.info('Max common: %d', max_common)


def day19a(input_path):
    scanner_coords = load_input(input_path)
    logging.info('Finished loading input')
    scanner_list = []
    for scanner_id, beacon_list in scanner_coords.items():
        scanner_map = ScannerData(scanner_id, beacon_list)
        scanner_list.append(scanner_map)
    logging.info('Finished creating scanners')

    aligned_beacon_list = []
    iters = 0
    while len(aligned_beacon_list) != 1:
        if iters > 10:
            logging.warning('Could not align all scanners')
            break
        aligned_beacon_list = align_scanners(scanner_list, expected_num=12)
        iters += 1

        scanner_list = []
        for scanner_id, coords_set in enumerate(aligned_beacon_list):
            beacon_list = np.array(list(coords_set))
            scanner_map = ScannerData(scanner_id, beacon_list)
            scanner_list.append(scanner_map)

    logging.info('Number unique coords: %d', len(aligned_beacon_list[0]))

    aligned_coords_array = np.array(list(aligned_beacon_list[0]))
    np.savetxt('final_coords.txt', aligned_coords_array)

    return len(aligned_beacon_list[0])

def test19a():
    scanner_coords = load_input('test_input0.txt')
    scanner_list = []
    for scanner_id, beacon_list in scanner_coords.items():
        scanner_map = ScannerData(scanner_id, beacon_list)
        scanner_list.append(scanner_map)
    align_scanners(scanner_list)

    scanner_coords = load_input('test_input1.txt')
    scanner_list = []
    for scanner_id, beacon_list in scanner_coords.items():
        scanner_map = ScannerData(scanner_id, beacon_list)
        scanner_list.append(scanner_map)
    align_scanners(scanner_list)

    assert 79 == day19a('test_input.txt')


def day19b(input_path):
    aligned_coords_array = np.loadtxt('final_coords.txt')
    # breakpoint()
    max_dist = 0
    for coords_0, coords_1 in itertools.combinations(aligned_coords_array, 2):
        dist = np.sum(np.abs(coords_0 - coords_1))
        max_dist = max(max_dist, dist)
    breakpoint()
    return max_dist


def test19b():
    assert 3621 == day19b('test_input.txt')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    test19a()
    # print('Day 19a:', day19a('day19_input.txt'))
    # test19b()
    # print('Day 19b:', day19b('day19_input.txt'))
