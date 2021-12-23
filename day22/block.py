import numpy as np


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
