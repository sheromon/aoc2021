import matplotlib.pyplot as plt
import numpy as np


def load_input(input_path):
    """Load and return x, y coordinates for dots and a list of instructions."""
    dots = []
    instructions = []
    with open(input_path) as file_obj:
        for line in file_obj:
            if line.startswith('fold'):
                # for the instructions, leave out the "fold along" and just
                # keep the good stuff
                instructions.append(line.strip().split(' ')[-1])
            elif line.strip():
                coords = [int(val) for val in line.strip().split(',')]
                dots.append(coords)
    dots = np.array(dots)
    return dots, instructions


def fold(dots, instruction):
    """Apply a fold instruction to a set of dots.

    The instruction should be in the format x=N or y=N, where N is an int.
    """
    if instruction[0] == 'x':
        col_ind = 0
    elif instruction[0] == 'y':
        col_ind = 1
    fold_value = int(instruction.split('=')[-1])
    flip_inds = dots[:, col_ind] > fold_value
    dots[flip_inds, col_ind] = 2 * fold_value - dots[flip_inds, col_ind]
    return np.unique(dots, axis=0)


def day13a(input_path):
    """Apply first fold instruction and retun the number of dots remaining."""
    dots, instructions = load_input(input_path)
    unique_dots = fold(dots, instructions[0])
    return len(unique_dots)


def test13a():
    assert 17 == day13a('test_input.txt')


def day13b(input_path):
    """Apply all fold instructions and save an image of the final dots."""
    dots, instructions = load_input(input_path)
    for instruction in instructions:
        dots = fold(dots, instruction)

    image_path = 'image.png'
    plt.figure()
    plt.plot(dots[:, 0], dots[:, 1], 'b*')
    plt.savefig(image_path)
    return image_path


if __name__ == '__main__':
    test13a()
    print('Day 13a:', day13a('day13_input.txt'))
    print('Day 13b:', day13b('day13_input.txt'))
