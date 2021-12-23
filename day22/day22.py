import numpy as np


def load_input(input_path):
    axes = ['x', 'y', 'z']
    instruction_list = []
    with open(input_path) as file_obj:
        for line in file_obj:
            instruction = dict()
            on_off, remainder = line.strip().split()
            instruction['value'] = int(on_off == 'on')
            tokens = remainder.split(',')
            bounds_list = []
            for ind, axis in enumerate(axes):
                bounds_list.append([int(val) for val in tokens[ind][2:].split('..')])
                bounds_list[-1][1] += 1
            instruction['bounds'] = np.array(bounds_list)
            instruction_list.append(instruction)
    return instruction_list


def day22a(input_path, max_steps=None):
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


class Block:

    def __init__(self, value, bounds, block_id=99):
        self.id = block_id
        self.value = value
        self.bounds = bounds
        self.volume = np.prod(self.bounds[:, 1] - self.bounds[:, 0])
        self.sub_blocks = []

    def __repr__(self):
        return str(self.__dict__)

    def intersects(self, other_bounds):
        return np.logical_not(np.any(self.bounds[:, 0:1] >= other_bounds[:, 1], axis=0) | \
            np.any(self.bounds[:, 1:2] <= other_bounds[:, 0], axis=0))

    def is_in(self, other):
        return np.all(self.bounds[:, 0] >= other.bounds[:, 0]) & \
            np.all(self.bounds[:, 1] <= other.bounds[:, 1])

    def split(self, other):
        outer_blocks = []
        intersect_bounds = np.stack((
            np.maximum(self.bounds[:, 0], other.bounds[:, 0]),
            np.minimum(self.bounds[:, 1], other.bounds[:, 1]),
        ), axis=-1)
        inner_block = Block(self.value, bounds=intersect_bounds)
        outer_blocks += self.get_outer_blocks(other, intersect_bounds)
        return inner_block, outer_blocks

    def get_outer_blocks(self, other, intersect_bounds):
        outer_blocks = []
        max_deltas = np.maximum(self.bounds[:, 1] - other.bounds[:, 1], 0).reshape([-1, 1])
        max_bounds = np.stack([other.bounds[:, 1], self.bounds[:, 1]]).T
        deltas = max_deltas
        bounds = max_bounds
        for ind, delta in enumerate(deltas):
            if not delta:
                continue
            new_bounds = np.copy(intersect_bounds)
            new_bounds[ind] = bounds[ind]
            new_block = Block(self.value, new_bounds)
            outer_blocks.append(new_block)
            if new_block.volume <= 0:
                raise RuntimeError(f'Invalid volume {new_block.volume}')

        min_deltas = np.maximum(other.bounds[:, 0] - self.bounds[:, 0], 0).reshape([-1, 1])
        min_bounds = np.stack([self.bounds[:, 0], other.bounds[:, 0]]).T
        deltas = min_deltas
        bounds = min_bounds
        for ind, delta in enumerate(deltas):
            if not delta:
                continue
            new_bounds = np.copy(intersect_bounds)
            new_bounds[ind] = bounds[ind]
            new_block = Block(self.value, new_bounds)
            outer_blocks.append(new_block)
            if new_block.volume <= 0:
                raise RuntimeError(f'Invalid volume {new_block.volume}')

        deltas = np.concatenate([min_deltas, max_deltas])
        bounds = np.concatenate([min_bounds, max_bounds])
        pair_inds = [
            (0, 1), (1, 2), (0, 2), (3, 4), (3, 5), (4, 5),
            (0, 4), (0, 5), (1, 3), (1, 5), (2, 3), (2, 4),
        ]
        for ind1, ind2 in pair_inds:
            if deltas[ind1] != 0 and deltas[ind2] != 0:
                new_bounds = np.copy(intersect_bounds)
                new_bounds[ind1 % 3] = bounds[ind1]
                new_bounds[ind2 % 3] = bounds[ind2]
                new_block = Block(self.value, new_bounds)
                outer_blocks.append(new_block)
        trip_inds = [
            (0, 1, 2), (0, 1, 5), (0, 4, 2), (3, 1, 2),
            (0, 4, 5), (3, 1, 5), (3, 4, 2), (3, 4, 5),
        ]
        for ind1, ind2, ind3 in trip_inds:
            if deltas[ind1] != 0 and deltas[ind2] != 0 and deltas[ind3] != 0:
                new_block = Block(self.value, bounds[[ind1, ind2, ind3]])
                outer_blocks.append(new_block)

        return outer_blocks

    def calc_volume(self):
        # breakpoint()
        final_volume = self.volume
        for block in self.sub_blocks:
            sign = np.sign(int(self.value == block.value) - 0.5)
            final_volume += block.calc_volume() * sign
        return final_volume


def append_sub_block(block, block_list, outer_value=None):
    outer_blocks = []
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
                if not block.is_in(other):
                    block, outers = block.split(other)
                    blocks_to_add += outers
                append_sub_block(block, other.sub_blocks, other.value)
                appended = True
        if not appended and block.value != outer_value:
            outer_blocks.append(block)
    block_list += outer_blocks


def day22b(input_path, max_steps=None):
    instruction_list = load_input(input_path)
    if max_steps is not None:
        instruction_list = instruction_list[:max_steps]

    print('Total # instructions:', len(instruction_list))
    block_list = []
    for ind, instruction in enumerate(instruction_list):
        block = Block(instruction['value'], instruction['bounds'], block_id=ind)
        # if ind == max_steps - 1:
        #     breakpoint()
        append_sub_block(block, block_list, outer_value=0)
        print(len(block_list))
        print(f'Step {ind} volume:', sum([block.value * block.calc_volume() for block in block_list]))
    # volume = block_list[0].calc_volume()
    # print(volume)
    total_volume = sum([block.value * block.calc_volume() for block in block_list])
    print(total_volume)
    return total_volume


def test22b():
    # assert 474140 == day22a('test_input2.txt')
    # assert 20 == day22b('test_input0.txt')
    # assert 39 == day22b('test_input.txt')
    # max_steps = 2  # 248314
    # max_steps = 3  # 310956
    # max_steps = 4  # 389786
    # max_steps = 5  # 389786
    # max_steps = 6  # 421952
    # max_steps = 7  # 421700
    # max_steps = 10  # 474140 <-- OK!
    # expected = day22a('test_input3.txt', max_steps=None)
    # print('Expected:', expected)
    # assert expected == day22b('test_input3.txt', max_steps=None)
    assert 2758514936282235 == day22b('test_input2.txt')


if __name__ == '__main__':
    # test22a()
    # print('Day 22a:', day22a('day22_input.txt'))
    test22b()
    print('Day 22b:', day22b('day22_input.txt'))
