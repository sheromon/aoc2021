import numpy as np

from block import Block


def load_input(input_path):
    """Read input and return a list of instructions in the form of a list of
    dictionaries, each with a key 'value' (1 for 'on' and 0 for 'off') and a key
    'bounds' (a 3x2 numpy array of min and max cube boundaries)."""
    axes = ['x', 'y', 'z']
    instruction_list = []
    with open(input_path) as file_obj:
        for line in file_obj:
            instruction = dict()
            on_off, remainder = line.strip().split()
            instruction['value'] = int(on_off == 'on')
            tokens = remainder.split(',')
            bounds_list = []
            for ind, _ in enumerate(axes):
                bounds_list.append([int(val) for val in tokens[ind][2:].split('..')])
                # add one to the max boundary to put it at the end of the cube
                bounds_list[-1][1] += 1
            instruction['bounds'] = np.array(bounds_list)
            instruction_list.append(instruction)
    return instruction_list


def day22a(input_path, max_steps=None):
    """Take a nice, simple, naive approach to calculating the total volume."""
    instruction_list = load_input(input_path)
    size = 101
    offset = size // 2
    volume = np.zeros(3 * (size,), dtype=np.uint8)
    if max_steps is not None:
        instruction_list = instruction_list[:max_steps]
    for inst in instruction_list:
        volume[inst['bounds'][0, 0]+offset:inst['bounds'][0, 1]+offset,
               inst['bounds'][1, 0]+offset:inst['bounds'][1, 1]+offset,
               inst['bounds'][2, 0]+offset:inst['bounds'][2, 1]+offset] = inst['value']
    return np.sum(volume)


def test22a():
    assert 39 == day22a('test_input.txt')


def append_sub_block(block, block_list, outer_value=None):
    """Add a block to a list of blocks, checking for intersections and breaking
    up the block into sub-blocks if it intersects any of the existing blocks."""
    outer_blocks = []
    # this is the set of blocks that we need to check for intersection with
    # existing blocks in block_list
    blocks_to_add = [block]
    while blocks_to_add:
        block = blocks_to_add.pop()
        appended = False
        if block_list:
            bounds = np.stack([bl.bounds for bl in block_list], axis=-1)
            intersects = block.intersects(bounds)
            first = np.argmax(intersects)
            if intersects[first]:
                other = block_list[first]
                # if block intersects but is not fully within other, break it up
                # into a sub-block that is fully within other and one or more
                # sub-blocks that do not intersect with other
                if not block.is_in(other):
                    block, outers = block.split(other)
                    # sub-blocks that don't intersect with other may intersect
                    # with some other block in the block list, so we need to
                    # add them to the list that needs to be checked
                    blocks_to_add += outers
                # the block that is fully within other goes into its sub-blocks
                append_sub_block(block, other.sub_blocks, other.value)
                appended = True
        # if the block didn't intersect any other blocks in block_list, it's
        # okay to just append, but don't want to add it until the end to avoid
        # needlessly checking it for intersections
        if not appended and block.value != outer_value:
            outer_blocks.append(block)
    block_list += outer_blocks


def day22b(input_path, max_steps=None):
    """Calculate the total volume the complicated way. Pretty slow, but it works."""
    instruction_list = load_input(input_path)
    if max_steps is not None:
        instruction_list = instruction_list[:max_steps]
    block_list = []
    for instruction in instruction_list:
        block = Block(instruction['value'], instruction['bounds'])
        append_sub_block(block, block_list, outer_value=0)
    return sum([block.value * block.calc_volume() for block in block_list])


def test22b():
    assert 474140 == day22a('test_input2.txt')
    assert 39 == day22b('test_input.txt')
    assert 2758514936282235 == day22b('test_input2.txt')


if __name__ == '__main__':
    test22a()
    print('Day 22a:', day22a('day22_input.txt'))
    test22b()
    print('Day 22b:', day22b('day22_input.txt'))
