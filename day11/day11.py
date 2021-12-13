import numpy as np


def load_input(input_path):
    """Load and return 2D numpy array of octopus energy levels."""
    output = []
    with open(input_path) as file_obj:
        for line in file_obj:
            output.append([int(val) for val in line.strip()])
    return np.array(output)


def day11a(input_path):
    """Calculate and return the total number of flashes over 100 steps."""
    levels = load_input(input_path)
    total_flashes = 0
    for _ in range(100):
        # at each step, energy for each octopus increases by 1
        levels += 1
        # any octopi with energy > 9 will flash
        inds = levels > 9
        # each flash increases energy of neighboring octopi by 1, so iteratively
        # increase energy based on flashes, check which new octopi will flash,
        # etc. until no new flashes are found.
        new_inds = inds.copy()
        while np.any(new_inds):
            coords = np.where(new_inds)
            for y, x in zip(*coords):
                if y > 0:
                    levels[y-1, x] += 1
                if x > 0:
                    levels[y, x-1] += 1
                if y > 0 and x > 0:
                    levels[y-1, x-1] += 1
                if y < levels.shape[0] - 1:
                    levels[y+1, x] += 1
                if x < levels.shape[1] - 1:
                    levels[y, x+1] += 1
                if y < levels.shape[0] - 1 and x < levels.shape[1] - 1:
                    levels[y+1, x+1] += 1
                if y > 0 and x < levels.shape[1] - 1:
                    levels[y-1, x+1] += 1
                if y < levels.shape[0] - 1 and x > 0:
                    levels[y+1, x-1] += 1
            # octopi flash at most once per step, so any we've already flagged
            # don't count as new flashes
            new_inds = (levels > 9) & np.logical_not(inds)
            inds = inds | new_inds
        flashes = np.sum(inds)
        # energy resets to 0 after a flash
        levels[inds] = 0

        total_flashes += flashes

    return total_flashes


def test11a():
    assert 1656 == day11a('test_input.txt')


def day11b(input_path):
    """Return the first step at which all octopi flash."""
    levels = load_input(input_path)

    step = 0
    while True:
        step += 1
        # at each step, energy for each octopus increases by 1
        levels += 1
        # any octopi with energy > 9 will flash
        inds = levels > 9
        # each flash increases energy of neighboring octopi by 1, so iteratively
        # increase energy based on flashes, check which new octopi will flash,
        # etc. until no new flashes are found.
        new_inds = inds.copy()
        while np.any(new_inds):
            coords = np.where(new_inds)
            for y, x in zip(*coords):
                if y > 0:
                    levels[y-1, x] += 1
                if x > 0:
                    levels[y, x-1] += 1
                if y > 0 and x > 0:
                    levels[y-1, x-1] += 1
                if y < levels.shape[0] - 1:
                    levels[y+1, x] += 1
                if x < levels.shape[1] - 1:
                    levels[y, x+1] += 1
                if y < levels.shape[0] - 1 and x < levels.shape[1] - 1:
                    levels[y+1, x+1] += 1
                if y > 0 and x < levels.shape[1] - 1:
                    levels[y-1, x+1] += 1
                if y < levels.shape[0] - 1 and x > 0:
                    levels[y+1, x-1] += 1
            # octopi flash at most once per step, so any we've already flagged
            # don't count as new flashes
            new_inds = (levels > 9) & np.logical_not(inds)
            inds = inds | new_inds
        flashes = np.sum(inds)
        # energy resets to 0 after a flash
        levels[inds] = 0

        if flashes == levels.size:
            return step


def test11b():
    assert 195 == day11b('test_input.txt')


if __name__ == '__main__':
    test11a()
    print('Day 11a:', day11a('day11_input.txt'))
    test11b()
    print('Day 11b:', day11b('day11_input.txt'))
