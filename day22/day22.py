import numpy as np


def load_input(input_path):
    axes = ['x', 'y', 'z']
    instruction_list = []
    with open(input_path) as file_obj:
        for line in file_obj:
            instruction = dict()
            instruction['on_off'], remainder = line.strip().split()
            tokens = remainder.split(',')
            for ind, axis in enumerate(axes):
                instruction[axis] = [int(val) for val in tokens[ind][2:].split('..')]
            instruction_list.append(instruction)
    return instruction_list


def day22a(input_path):
    instruction_list = load_input(input_path)
    size = 101
    offset = size // 2
    volume = np.zeros(3 * (size,), dtype=np.uint8)
    for inst in instruction_list:
        value = inst['on_off'] == 'on'
        volume[inst['x'][0]+offset:inst['x'][1]+offset+1,
               inst['y'][0]+offset:inst['y'][1]+offset+1,
               inst['z'][0]+offset:inst['z'][1]+offset+1] = value
    return np.sum(volume)


def test22a():
    assert 39 == day22a('test_input.txt')


def day22b(input_path):
    pass


def test22b():
    assert 474140 == day22a('test_input2.txt')
    assert 2758514936282235 == day22a('test_input2.txt')


if __name__ == '__main__':
    test22a()
    print('Day 22a:', day22a('day22_input.txt'))
    test22b()
    # print('Day 22b:', day22b('day22_input.txt'))
