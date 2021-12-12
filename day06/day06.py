import numpy as np


def day06a(input_path):
    """Calculate lanternfish population after 80 days (computationally bad)."""
    with open(input_path) as file_obj:
        for line in file_obj:
            vals = [int(val) for val in line.strip().split(',')]
    vals = np.array(vals)
    for _ in range(80):
        vals = advance(vals)
    return len(vals)


def advance(vals):
    """Go forward one day in countdown to new births, and create new fish."""
    zero_inds = vals == 0
    vals[~zero_inds] -= 1
    vals[zero_inds] = 6
    num_new = np.sum(zero_inds)
    new_vals = 8 * np.ones(num_new)
    vals = np.concatenate([vals, new_vals])
    return vals


def test06a():
    score = day06a('test_input.txt')
    assert 5934 == score


if __name__ == '__main__':
    test06a()
    print('Day 06a:', day06a('day06_input.txt'))
    # test06b()
    # print('Day 06b:', day06b('day06_input.txt'))
