import numpy as np


def load_array(input_path):
    with open(input_path) as file_obj:
        bits = [line.strip() for line in file_obj]
    return np.array([[int(val) for val in row] for row in bits])


def day03a(input_path):
    total_array = load_array(input_path)
    means = np.mean(total_array, axis=0)
    gamma_ints = np.round(means).astype(np.int32)
    epsilon_ints = 1 - gamma_ints
    gamma = np.sum([val * 2**ind for ind, val in enumerate(gamma_ints[::-1])])
    epsilon = np.sum([val * 2**ind for ind, val in enumerate(epsilon_ints[::-1])])
    power = gamma * epsilon
    return power


def test03a():
    assert 198 == day03a('test_input.txt')


def day03b(input_path):
    total_array = load_array(input_path)
    ints = get_value(total_array.copy(), most_common=True)
    oxygen = np.sum([val * 2**ind for ind, val in enumerate(ints[::-1])])
    ints = get_value(total_array.copy(), most_common=False)
    co2 = np.sum([val * 2**ind for ind, val in enumerate(ints[::-1])])
    return oxygen * co2


def get_value(current_array, most_common=True):
    ind = 0
    while current_array.shape[0] > 1:
        mean = np.mean(current_array[:, ind])
        # python rounds 0.5 to 0 because 0 is even, and I want it to round to 1,
        # not 0, so use a hack. add 1, get 1.5 to round to 2, then subtract 1.
        common_val = np.round(mean + 1).astype(np.int32) - 1
        keep_inds = current_array[:, ind] == common_val
        if not most_common:
            keep_inds = np.logical_not(keep_inds)
        current_array = current_array[keep_inds, :]
        ind += 1
    assert current_array.shape[0] == 1
    return np.squeeze(current_array)


def test03b():
    assert 230 == day03b('test_input.txt')


if __name__ == '__main__':
    test03a()
    print('Day 03a:', day03a('day03_input.txt'))
    test03b()
    print('Day 03b:', day03b('day03_input.txt'))
