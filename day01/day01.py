import numpy as np


def day01a(input_path):
    with open(input_path) as file_obj:
        depth_list = [int(line.strip()) for line in file_obj]
    prev_val = np.inf
    counter = 0
    for val in depth_list:
        if val > prev_val:
            counter += 1
        prev_val = val
    return counter


def test01a():
    assert 7 == day01a('test_input.txt')


def day01b(input_path):
    with open(input_path) as file_obj:
        depth_list = [int(line.strip()) for line in file_obj]
    prev_val = np.inf
    depth_array = np.array([
        depth_list + 2 * [0],
        [0] + depth_list + [0],
        2 * [0] + depth_list,
    ])
    sums = np.sum(depth_array, axis=0)
    counter = 0
    for val in sums[2:-2]:
        if val > prev_val:
            counter += 1
        prev_val = val
    return counter


def test01b():
    assert 5 == day01b('test_input.txt')


if __name__ == '__main__':
    test01a()
    print('Day 01a:', day01a('day01_input.txt'))
    test01b()
    print('Day 01b:', day01b('day01_input.txt'))
