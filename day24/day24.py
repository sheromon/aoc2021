import itertools

import numpy as np

from alu import Alu


def load_input(input_path):
    instructs = []
    with open(input_path) as file_obj:
        for line in file_obj:
            instructs.append(line.strip().split())
    return instructs


def day24(input_path):
    instructs = load_input(input_path)

    # by stepping through the calculations, I'd figured out that there are a
    # bunch of equality statements that are important, so start by finding those
    eql_inds = np.array([ind for ind, line in enumerate(instructs) if line == ['eql', 'x',  'w'] ])

    # I'd also figured out that some of the statements depend on the inputs and
    # some don't, so let's run the ALU a bunch of times on random inputs to see
    # which results are always the same and which vary
    constants = run_random_trials(instructs, num_trials=500)

    eql_check_outputs = constants[eql_inds]
    variable_check_inds = eql_check_outputs == -1
    print('All check outputs:', eql_check_outputs)
    print('# constant check outputs:', np.sum(~variable_check_inds))
    print('# variable check outputs:', np.sum(variable_check_inds))

    # for the equality check outputs that vary based on the input, try running
    # the ALU with those bits hardcoded to all combinations of True/False.
    # there are only 7 that vary, so the search space is 2^7.
    search_test_bit_space(instructs, np.copy(constants), eql_inds[variable_check_inds])

    # based on the previous step, I know that I want all 7 checks to evaluate to
    # True in order to get z to be 0, so generate the string expressions for w
    # and x at each of the 7 important equality checks.
    prev_num_steps = None
    # doesn't matter what input is used for this step, so use the example input
    input_str = '13579246899999'
    for num_steps in eql_inds[variable_check_inds]:
        # after calculating the first expression, hardcode the previous results
        # as if each one had the condition met because we already know we need
        # to satisfy the condition, and it makes the expression much simpler
        if prev_num_steps is not None:
            constants[prev_num_steps] = 1
            constants[prev_num_steps + 1] = 0
        alu = Alu(instructs, input_str, constants=constants, gen_expressions=True)
        alu.run(max_steps=num_steps)
        print('    Instruction', num_steps)
        print('w:', alu.exprs['w'])
        print('x:', alu.exprs['x'])
        prev_num_steps = num_steps

    # the printouts from this step give inreasingly complicated expressions, but
    # they aren't too complicated to simplify by hand and come up with the
    # following rules:
    #   ints[2] = ints[3]
    #   ints[4] = ints[5] - 2
    #   ints[1] = ints[6] - 6
    #   ints[10] = ints[9] - 3
    #   ints[8] = ints[11] - 7
    #   ints[12] = ints[7] - 8
    #   ints[13] = ints[0] - 7
    # then I can apply the rules to come up with the largest and smallest
    # valid model numbers
    input_str = '93997999296912'  # max valid model number
    input_str = '81111379141811'  # min valid model number
    alu = Alu(instructs, input_str, constants=constants).run()
    print(alu.vals)


def run_random_trials(instructs, num_trials=500):
    """Run the ALU with random inputs and bunch of times and check which
    intermediate results are always the same and which vary.
    """
    all_inputs = np.random.randint(1, 9, size=(num_trials, 14))
    # keep track of all intermediate values across multiple trials
    all_intermeds = []
    for ints in all_inputs:
        alu = Alu(instructs, list(ints)).run()
        all_intermeds.append(alu.intermeds)

    # determine which intermediate results are the same regardless of the input
    all_intermeds = np.array(all_intermeds)
    max_val = np.max(all_intermeds, axis=0)
    is_constant = np.all(all_intermeds == max_val, axis=0)
    print('Num constants:', np.sum(is_constant))
    # make a list of all intermediate results with -1 for non-constant values
    # and the value filled in for constants
    constants = -1 * np.ones_like(is_constant)
    constants[is_constant] = all_intermeds[0, is_constant]

    return constants


def search_test_bit_space(instructs, constants, variable_check_inds):
    """Force the ALU calculation to use hardcoded values at certain steps.

    Using this cheat, figure out which conditions should be True or False to
    get z to be 0 at the end.
    """
    input_str = '13579246899999'
    int_list = [int(char) for char in input_str]
    for test_bits in itertools.product(range(2), repeat=7):
        constants[variable_check_inds] = np.array(test_bits)
        alu = Alu(instructs, int_list, constants=constants).run()
        if alu.vals['z'] == 0:
            print('Found valid test bit sequence:', test_bits)


def test24():
    assert run_test(['inp x', 'mul x -1'])['x'] == -15
    assert run_test(['inp z', 'inp x', 'mul z 3', 'eql z x'])['z'] == 1
    assert all(val == 1 for val in run_test('test_input.txt').values())


def run_test(input_path):
    if isinstance(input_path, str):
        instructs = load_input(input_path)
    else:
        instructs = [line.split() for line in input_path]
    input_list = [15, 45]
    alu = Alu(instructs, list(input_list))
    alu.run()
    return alu.vals


if __name__ == '__main__':
    test24()
    day24('day24_input.txt')
