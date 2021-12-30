import copy
import itertools
import re

import numpy as np

from alu import Alu


def load_input(input_path):
    steps = []
    with open(input_path) as file_obj:
        for line in file_obj:
            steps.append(line.strip().split())
    return steps


def day24(input_path):
    steps = load_input(input_path)

    # after stepping through the calculations, I know that there are a bunch of
    # equality checks that are important, so start by finding all of those
    eql_inds = np.array([ind for ind, line in enumerate(steps) if line == ['eql', 'x',  'w'] ])

    # I'd also figured out that some of the statements depend on the inputs and
    # some don't, so let's run the ALU a bunch of times on random inputs to see
    # which results are always the same and which vary
    constants = run_random_trials(steps, num_trials=500)
    eql_check_outputs = constants[eql_inds]
    variable_check_inds = eql_check_outputs == -1
    print('All check outputs (-1 means non-constant):', eql_check_outputs)
    print('# constant check outputs:', np.sum(~variable_check_inds))
    print('# variable check outputs:', np.sum(variable_check_inds))

    # for the equality check outputs that vary based on the input, try running
    # the ALU with those bits hardcoded to all combinations of True/False. from
    # the previous step, there are only 7 that vary, so the search space is 2^7.
    search_test_bit_space(steps, np.copy(constants), eql_inds[variable_check_inds])

    # from the previous step, I know that I want all of the checks that can
    # result in either 0 or 1 o be 1 (True). also from doing some calculations
    # by hand, I know that each check depends on a pair of inputs (well, they
    # also depend on previous check results, but we know we want all to be True,
    # so given that constraint, it's a specific pair per check). so try all
    # combinations of two integers in [1, 9] to get the right relationship, then
    # either maximize values for part 1 or minimize for part 2.
    find_model_number(steps, eql_inds[variable_check_inds], mode='max')
    find_model_number(steps, eql_inds[variable_check_inds], mode='min')


def run_random_trials(steps, num_trials=500):
    """Run the ALU with random inputs and bunch of times and check which
    intermediate results are always the same and which vary.
    """
    all_inputs = np.random.randint(1, 9, size=(num_trials, 14))
    # keep track of all intermediate values across multiple trials
    all_intermeds = []
    for ints in all_inputs:
        alu = Alu(steps, list(ints)).run()
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


def search_test_bit_space(steps, constants, variable_check_inds):
    """Force the ALU calculation to use hardcoded values at certain steps.

    Using this cheat, figure out which conditions should be True or False to
    get z to be 0 at the end.
    """
    input_str = '13579246899999'
    int_list = [int(char) for char in input_str]
    for test_bits in itertools.product(range(2), repeat=7):
        constants[variable_check_inds] = np.array(test_bits)
        alu = Alu(steps, int_list, constants=constants).run()
        if alu.vals['z'] == 0:
            print('Found valid test bit sequence:', test_bits)


def find_model_number(steps, variable_check_inds, mode='max'):
    """Solve for the optimal value of each model number digit."""
    # this will eventually hold the desired model number, but initilize it with
    # whatever for now
    good_values = 14 * [9]
    # iterate through each point where an important condition check happens
    for ind, num_steps in enumerate(variable_check_inds):
        # generate string expressions for the contents of w and x at the step
        # where the check we care about takes place, then parse out which input
        # indices are used in the expressions (input variables are 'inp #')
        alu = Alu(steps, good_values, gen_expressions=True)
        alu.run(max_steps=num_steps)
        # w is always 'inp #', so it's straightforward
        w_ind = int(alu.exprs['w'].rpartition(' ')[-1])
        # x is an expression that depends on one or more inputs, so find all of
        # the input indices in the expression
        search_pattern = re.compile('inp (\d+)')
        x_inds = [int(val) for val in search_pattern.findall(alu.exprs['x'])]

        # for each input value that could potentially determine the value of x,
        # try out different values in relation to w
        solved_digit = False
        for x_ind in x_inds:
            int_list = copy.deepcopy(good_values)
            for ints in itertools.product(range(1, 10), repeat=2):
                int_list[w_ind] = ints[0]
                int_list[x_ind] = ints[1]
                alu = Alu(steps, int_list).run()
                # if the check failed, stop processing and try the next values
                if not alu.intermeds[num_steps]:
                    continue
                # increment both inputs by 1 to verify that this x input is the
                # correct one to pair with this w, and it's not a coincidence.
                # this may result in an invalid value (10) if one was 9, but
                # that's okay because we'll fix it later.
                int_list[w_ind] = ints[0] + 1
                int_list[x_ind] = ints[1] + 1
                alu = Alu(steps, int_list).run()
                if not alu.intermeds[num_steps]:
                    continue
                # we don't actually need to know the conditions, but why not
                delta = int_list[w_ind] - int_list[x_ind]
                print(f'Condition {ind + 1}: inp {w_ind} == inp {x_ind} + {delta}')
                #
                if mode == 'max':
                    max_val = max(int_list[w_ind], int_list[x_ind])
                    int_list[w_ind] += 9 - max_val
                    int_list[x_ind] += 9 - max_val
                else:
                    min_val = min(int_list[w_ind], int_list[x_ind])
                    int_list[w_ind] -= min_val - 1
                    int_list[x_ind] -= min_val - 1
                good_values = int_list
                solved_digit = True
                break
            if solved_digit:
                break
    print(f'{mode} model number:', ''.join([str(val) for val in good_values]))
    return


def test24():
    assert run_test(['inp x', 'mul x -1'])['x'] == -15
    assert run_test(['inp z', 'inp x', 'mul z 3', 'eql z x'])['z'] == 1
    assert all(val == 1 for val in run_test('test_input.txt').values())


def run_test(input_path):
    if isinstance(input_path, str):
        steps = load_input(input_path)
    else:
        steps = [line.split() for line in input_path]
    input_list = [15, 45]
    alu = Alu(steps, list(input_list))
    alu.run()
    return alu.vals


if __name__ == '__main__':
    test24()
    day24('day24_input.txt')
