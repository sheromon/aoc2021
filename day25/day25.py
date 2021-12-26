import numpy as np


def load_input(input_path):
    lines = []
    with open(input_path) as file_obj:
        for line in file_obj:
            lines.append(list(line.strip()))
    return np.array(lines)


def day25a(input_path):
    """Predict the sea cucumber pattern for as many steps as it takes for it to stabilize."""
    array = load_input(input_path)
    cuc_map = CucumberMap(array)
    num_moved = 1
    num_steps = 0
    while num_moved:
        num_moved = cuc_map.step_east() + cuc_map.step_south()
        num_steps += 1
    return num_steps


class CucumberMap:

    def __init__(self, array):
        self.array = array
        self.coords = {
            'east': np.stack(np.where(self.array == '>')).T,
            'south': np.stack(np.where(self.array == 'v')).T,
        }

    def __str__(self) -> str:
        return str(self.array)

    def step(self, direction, ind, char, delta):
        """Try to step all cucumbers in the given direction and return the number that moved."""
        next_coords = self.coords[direction] + delta
        next_coords[:, ind] = next_coords[:, ind] % self.array.shape[ind]
        ok_inds = self.array[tuple(next_coords.T)] == '.'
        self.array[tuple(next_coords[ok_inds, :].T)] = char
        self.array[tuple(self.coords[direction][ok_inds, :].T)] = '.'
        self.coords[direction][ok_inds, :] = next_coords[ok_inds, :]
        return sum(ok_inds)

    def step_east(self):
        """Try to step all east-facing cucumbers and return the number that moved."""
        ind = 1
        char = '>'
        delta = np.array([0, 1])
        return self.step('east', ind, char, delta)

    def step_south(self):
        """Try to step all south-facing cucumbers and return the number that moved."""
        ind = 0
        char = 'v'
        delta = np.array([1, 0])
        return self.step('south', ind, char, delta)


def test25a():
    assert 58 == day25a('test_input.txt')


if __name__ == '__main__':
    test25a()
    print('Day 25a:', day25a('day25_input.txt'))
