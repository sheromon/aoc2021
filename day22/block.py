import numpy as np


class Block:

    def __init__(self, value, bounds):
        """Initialize Block.

        :param value: 1 for "on" block and 0 for "off"
        :param bounds: 3 x 2 array of block bounds; first col is min, second is max
        """
        self.value = value
        self.bounds = bounds
        self.volume = np.prod(self.bounds[:, 1] - self.bounds[:, 0])
        # store a list of blocks that fall entirely within this block and have
        # th eopposite value
        self.sub_blocks = []

    def __repr__(self):
        return str(self.__dict__)

    def intersects(self, other_bounds):
        """Return an array of booleans for blocks that do or do not intersect this one.

        :params other_bounds: 3 x 2 x n array of bounds for n blocks
        :return: n-element array of boolean values

        This was originally a method that took self and an 'other' block, but
        looping through each block individually to check the intersection status
        took too long, so I had to vectorize it. I kind of want to rework this
        class so that each object represents a list of blocks, but that would be
        too much work.
        """
        return np.logical_not(np.any(self.bounds[:, 0:1] >= other_bounds[:, 1], axis=0) | \
            np.any(self.bounds[:, 1:2] <= other_bounds[:, 0], axis=0))

    def is_in(self, other):
        """Return True if other block is entirely within this one and False otherwise."""
        return np.all(self.bounds[:, 0] >= other.bounds[:, 0]) & \
            np.all(self.bounds[:, 1] <= other.bounds[:, 1])

    def split(self, other):
        """Break up this block into one that intersects the other block and others that don't.

        :return: tuple (inner_block, outer_blocks) where inner_block is a sub-block
            that is fully inside of the other, and outer_blocks is a list of sub-blocks
            that do not intersect the other block
        """
        outer_blocks = []
        intersect_bounds = np.stack((
            np.maximum(self.bounds[:, 0], other.bounds[:, 0]),
            np.minimum(self.bounds[:, 1], other.bounds[:, 1]),
        ), axis=-1)
        inner_block = Block(self.value, bounds=intersect_bounds)
        outer_blocks += self.get_outer_blocks(other, intersect_bounds)
        return inner_block, outer_blocks

    def get_outer_blocks(self, other, intersect_bounds):
        """Calculate and return all sub-blocks of self that do not intersect with other."""
        outer_blocks = []

        # if any min bounds for this block are smaller than min bounds of the other
        # block, the deltas will be positive; otherwise they will be zero
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

        # if any max bounds for this block are larger than max bounds of the other
        # block, the deltas will be positive; otherwise they will be zero
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

        # taking the full set of min and max deltas, any non-zero pairs form
        # another sub-block; valid pairs must be for two different coordinates,
        # e.g. min x delta cannot be paired with max x delta
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

        # taking the full set of min and max deltas, any non-zero triplets form
        # another sub-block with similar restrictions as described for pairs
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
        """Calculate and return the total volume of this block and all sub-blocks."""
        final_volume = self.volume
        # all sub-blocks should have opposite sign, so subtract their volume
        for block in self.sub_blocks:
            final_volume -= block.calc_volume()
        return final_volume
