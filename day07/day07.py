import numpy as np


def day07a(input_path):
    """Calculate amount of fuel needed to align crabs at the same position.

    Distance is absolute value of delta between positions on one axis.
    """
    with open(input_path) as file_obj:
        vals = [int(val) for val in file_obj.readline().strip().split(',')]
    vals = np.array(vals, dtype=np.int32)
    # distance is the l1 distance with just one coordinate, so optimal position
    # should be the median.
    align_val = np.median(vals)
    return np.sum(np.abs(vals - align_val)).astype(int)


def test07a():
    score = day07a('test_input.txt')
    assert 37 == score


def day07b(input_path):
    """Calculate amount of fuel needed to align crabs at the same position.

    Distance is the sum of integers from 1 to absolute value of delta between
    positions on one axis.
    """
    with open(input_path) as file_obj:
        vals = [int(val) for val in file_obj.readline().strip().split(',')]
    vals = np.array(vals, dtype=np.int32)

    def calc_total_fuel(dists):
        """We could be fancy, but let's try just brute-forcing it."""
        total = 0
        for dist in dists:
            total += np.sum(np.arange(dist + 1))
        return total

    # the distance grows not quite as the square of the delta, but kind of in
    # that direction, so try taking the mean to get the optimal value.
    # the ceiling of the mean is the right value for the test case, but for the
    # real input, I had to twiddle around to find the right value. ¯\_(ツ)_/¯
    align_val = np.ceil(np.mean(vals))
    dists = np.abs(vals - align_val)
    total_fuel = calc_total_fuel(dists)
    for tweak in [-1, 1]:
        dists = np.abs(vals - (align_val + tweak))
        alt_total_fuel =  calc_total_fuel(dists)
        if alt_total_fuel < total_fuel:
            total_fuel = alt_total_fuel
    return int(total_fuel)


def test07b():
    score = day07b('test_input.txt')
    assert 168 == score


if __name__ == '__main__':
    test07a()
    print('Day 07a:', day07a('day07_input.txt'))
    test07b()
    print('Day 07b:', day07b('day07_input.txt'))
