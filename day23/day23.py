import numpy as np


def load_input(input_path):
    char_list = []
    length = None
    with open(input_path) as file_obj:
        for line in file_obj:
            chars = list(line[:-1])
            if not length:
                length = len(chars)
            if len(chars) < length:
                chars += ['#'] * (length - len(chars))
            char_list.append(chars)
    return np.array(char_list)


def day23a(input_path):
    array = load_input(input_path)
    array[-2:, :2] = '#'
    room = Room(array)
    # array[1, 3:10:2] = '#'
    print(array)

    amph = room.amphs[2]
    breakpoint()
    result = room.move(amph, (1, 2))
    print(room.array)
    breakpoint()

    min_energy = None
    return min_energy


class Amphipod:

    energy_map = {
        'A': 1,
        'B': 10,
        'C': 100,
        'D': 1000,
    }
    col_map = {
        'A': 3,
        'B': 5,
        'C': 7,
        'D': 9,
    }

    def __init__(self, letter, coords):
        self.letter = letter
        self.energy_per_step = self.energy_map[letter]
        self.home_col = self.col_map[letter]
        self.coords = coords
        self.energy_used = 0

    def __repr__(self) -> str:
        return f'{self.letter}: {self.coords}, {self.energy_used}'

    def step(self, n_steps):
        self.energy_used += n_steps * self.energy_per_step


class Room:

    def __init__(self, array):
        self.array = array
        self.open_coords = set(zip(*np.where(array == '.')))
        self.open_coords -= set([(1, 3), (1, 5), (1, 7), (1, 9)])

        self.amphs = []
        for letter in Amphipod.energy_map:
            inds = np.where(array == letter)
            for coords in zip(*inds):
                amph = Amphipod(letter, coords)
                self.amphs.append(amph)

    def move(self, amph, coords):
        """Try to move an amphipod from its current position to a new position.

        If the move is not successful, False will be returned.
        """
        if coords not in self.open_coords:
            return False
        coords = np.array(coords)
        next_coords = np.zeros_like(coords)
        steps = 0
        orig_coords = amph.coords
        while not np.all(next_coords == coords):
            signs = np.sign(np.array(coords) - np.array(amph.coords))
            stepped = False
            for ind, sign in enumerate(signs):
                if not sign:
                    continue
                direction = np.zeros(2, dtype=np.int32)
                direction[ind] = sign
                next_coords = np.array(amph.coords) + direction
                if self.array[tuple(next_coords)] == '.':
                    amph.coords = tuple(next_coords)
                    steps += 1
                    stepped = True
                    break
            if not stepped:
                amph.coords = orig_coords
                return False
        self.open_coords.remove(tuple(coords))
        self.open_coords.add(orig_coords)
        self.array[amph.coords] = amph.letter
        self.array[orig_coords] = '.'
        amph.step(steps)
        return True


def test23a():
    assert 12521 == day23a('test_input.txt')


def day23b(input_path):
    pass


def test23b():
    assert 12521 == day23a('test_input.txt')


if __name__ == '__main__':
    test23a()
    print('Day 23a:', day23a('day23_input.txt'))
    # test23b()
    # print('Day 23b:', day23b('day23_input.txt'))
