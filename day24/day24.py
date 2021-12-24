import collections
import itertools

import numpy as np


def load_input(input_path):
    instruction_list = []
    with open(input_path) as file_obj:
        for line in file_obj:
            instruction_list.append(line.strip().split())
    return instruction_list


def day24a(input_path):
    instruction_list = load_input(input_path)
    input_str = '13579246899999'
    # input_str = 14 * '3'
    int_list = [int(char) for char in input_str[::-1]]
    # for input_vals in itertools.combinations_with_replacement(range(1, 10), 14):
    while True:
        int_list = np.random.randint(1, 10, size=14)
        # print(int_list)
        run_monad(instruction_list, list(int_list))


def run_monad(instruction_list, input_list):
    # print('input:', input_str)
    # input_list = [int(char) for char in input_str[::-1]]
    vars = collections.defaultdict(int)
    for iline, instruction in enumerate(instruction_list):
        process(instruction, vars, input_list, iline)
    if vars['z'] == 0:
        input_str = ''.join([str(val) for val in input_list[::-1]])
        print(input_str, 'is valid')


def process(instruction, vars, input_list, iline=None):
    log_var = None
    op = instruction[0]
    name = instruction[1]
    if op == 'inp':
        vars[name] = int(input_list.pop())
        if name == log_var:
            print(f'input {name}:', vars[name])
        return
    else:
        name2 = None
        try:
            val = int(instruction[2])
        except:
            name2 = instruction[2]
            val = vars[instruction[2]]
    # if iline == 6:
    #     breakpoint()
    if op == 'add':
        vars[name] += val
    elif op == 'mul':
        vars[name] *= val
    elif op == 'div':
        vars[name] = vars[name] // val
    elif op == 'mod':
        vars[name] = vars[name] % val
    elif op == 'eql':
        vars[name] = int(vars[name] == val)
        # if name == 'x' and name2 == 'w':
        #     breakpoint()
    if name == log_var:
        print(f'Instruction {iline}: {op} {name} {val} ({name2}) -->', vars[name])


def test24a():
    assert run_test(['inp x', 'mul x -1'])['x'] == -15
    assert run_test(['inp z', 'inp x', 'mul z 3', 'eql z x'])['z'] == 1
    assert all(val == 1 for val in run_test('test_input.txt').values())


def run_test(input_path):
    if isinstance(input_path, str):
        instruction_list = load_input(input_path)
    else:
        instruction_list = [line.split() for line in input_path]
    vars = collections.defaultdict(int)
    input_list = [15, 45]
    input_list = input_list[::-1]
    for instruction in instruction_list:
        process(instruction, vars, input_list)
    return vars


def day24b(input_path):
    pass


def test24b():
    assert 44169 == day24b('test_input.txt')


if __name__ == '__main__':
    # test24a()
    print('Day 24a:', day24a('day24_input.txt'))
    # test24b()
    # print('Day 24b:', day24b('day24_input.txt'))
