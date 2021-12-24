import collections

import numpy as np


def load_input(input_path):
    instruction_list = []
    with open(input_path) as file_obj:
        for line in file_obj:
            instruction_list.append(line.strip().split())
    return instruction_list


def day24a(input_path):
    instruction_list = load_input(input_path)
    # input_str = '13579246899999'
    # int_list = [int(char) for char in input_str[::-1]]
    while True:
        int_list = np.random.randint(1, 10, size=14)
        Alu(instruction_list, list(int_list)).run()


class Alu:

    def __init__(self, instruction_list, input_list):
        self.instruction_list = instruction_list
        self.input_list = input_list
        self.iline = 0
        self.vars = collections.defaultdict(int)
        self.log_var = None

    def run(self):
        for _ in self.instruction_list:
            self.step()
        if self.vars['z'] == 0:
            input_str = ''.join([str(val) for val in self.input_list[::-1]])
            print(input_str, 'is valid')

    def step(self):
        instruction = self.instruction_list[self.iline]
        op = instruction[0]
        name = instruction[1]
        if op == 'inp':
            self.vars[name] = int(self.input_list.pop())
        else:
            name2 = None
            try:
                val = int(instruction[2])
            except:
                name2 = instruction[2]
                val = self.vars[instruction[2]]
        if op == 'add':
            self.vars[name] += val
        elif op == 'mul':
            self.vars[name] *= val
        elif op == 'div':
            self.vars[name] = self.vars[name] // val
        elif op == 'mod':
            self.vars[name] = self.vars[name] % val
        elif op == 'eql':
            self.vars[name] = int(self.vars[name] == val)
        self.iline += 1
        if name == self.log_var:
            if op == 'inp':
                print(f'Instruction {self.iline}: {op} {name} -->', self.vars[name])
            else:
                print(f'Instruction {self.iline}: {op} {name} {name2} ({val}) -->', self.vars[name])


def test24a():
    assert run_test(['inp x', 'mul x -1'])['x'] == -15
    assert run_test(['inp z', 'inp x', 'mul z 3', 'eql z x'])['z'] == 1
    assert all(val == 1 for val in run_test('test_input.txt').values())


def run_test(input_path):
    if isinstance(input_path, str):
        instruction_list = load_input(input_path)
    else:
        instruction_list = [line.split() for line in input_path]
    input_list = [15, 45]
    input_list = input_list[::-1]
    alu = Alu(instruction_list, list(input_list))
    alu.run()
    return alu.vars


def day24b(input_path):
    pass


def test24b():
    assert 44169 == day24b('test_input.txt')


if __name__ == '__main__':
    test24a()
    print('Day 24a:', day24a('day24_input.txt'))
    # test24b()
    # print('Day 24b:', day24b('day24_input.txt'))
