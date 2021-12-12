import numpy as np


def day06(input_path, n_days=80):
    """Calculate lanternfish population after n days."""
    with open(input_path) as file_obj:
        for line in file_obj:
            vals = [int(val) for val in line.strip().split(',')]
    vals = np.array(vals)

    # keep track of number of fish at each stage of reproduction
    counts = dict()
    # initial fish should have a max counter of 6 (takes 7 days to reproduce)
    assert np.sum(vals > 6) == 0
    for ind in range(7):
        counts[ind] = np.sum(vals == ind)
    # when new fish are born, they need an extra 2 days, so max counter is 8
    counts[7] = 0
    counts[8] = 0

    # each day, the fish that had n days in their countdown, then have n-1 days.
    # the fish at 0 reproduce and have their counter reset to 6, and the newly
    # born fish get their counter set to 8.
    for _ in range(n_days):
        num_new = counts[0]
        for ind in range(8):
            counts[ind] = counts[ind+1]
        counts[6] += num_new
        counts[8] = num_new
    return sum([val for val in counts.values()])


def test06a():
    score = day06('test_input.txt')
    assert 5934 == score


def test06b():
    score = day06('test_input.txt', n_days=256)
    assert 26984457539 == score


if __name__ == '__main__':
    test06a()
    print('Day 06a:', day06('day06_input.txt'))
    test06b()
    print('Day 06b:', day06('day06_input.txt', n_days=256))
