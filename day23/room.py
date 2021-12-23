import numpy as np

from amphipod import Amphipod


class Room:

    def __init__(self, array):
        self.array = array
        self.open_coords = set(zip(*np.where(array == '.')))
        self.open_coords -= set([(1, 3), (1, 5), (1, 7), (1, 9)])
        self.amphs = []
        self._init_amphs()

    def _init_amphs(self):
        """Create all amphipods based on the input array."""
        for letter in Amphipod.energy_map:
            inds = np.where(self.array == letter)
            for coords in zip(*inds):
                amph = Amphipod(letter, coords)
                self.amphs.append(amph)

    def print_info(self):
        print(self.array)
        print('Hallway movers:', self.hallway_movers)
        print('Room movers:', self.room_movers)
        for col in [3, 5, 7, 9]:
            if self.col_is_open(col):
                print(f'Col {col} is open')


    def get_amph(self, coords):
        for amph in self.amphs:
            if amph.coords == coords:
                return amph

    @property
    def complete(self):
        for amph in self.amphs:
            if not amph.is_home:
                return False
        return True

    @property
    def energy_used(self):
        return sum([amph.energy_used for amph in self.amphs])

    @property
    def room_movers(self):
        """Identify amphipods that are in rooms and can move."""
        amph_list = []
        for amph in self.amphs:
            # amphipods in the room but closest to the exit
            if amph.coords[0] == 2:
                if amph.is_home:
                    coords_below = np.array(amph.coords) + np.array([1, 0])
                    if self.array[tuple(coords_below)] == amph.letter:
                        continue
                amph_list.append(amph)
                continue
            coords_above = np.array(amph.coords) + np.array([-1, 0])
            if self.array[tuple(coords_above)] == '.' and not amph.is_home:
                amph_list.append(amph)
        return amph_list

    @property
    def hallway_movers(self):
        """Identify amphipods that are in the hallway."""
        amph_list = []
        for amph in self.amphs:
            if amph.coords[0] == 1:
                amph_list.append(amph)
        return amph_list

    def col_is_open(self, col):
        """Return True if col is available for an amphipod to end there."""
        if np.all(self.array[2:4, col] == '.'):
            return True
        if not np.any(self.array[2:4, col] == '.'):
            return False
        if self.array[2, col] == '.':
            amph_letter = self.array[3, col]
            return col == Amphipod.home_col_map[amph_letter]

    def move(self, amph, coords):
        """Try to move an amphipod from its current position to a new position.

        If the move is not successful, False will be returned.
        """
        if coords not in self.open_coords:
            return False
        # an amphipod on the hallway can only move to its home column
        if amph.coords[0] == 1 and coords[1] != amph.home_col:
            return False
        coords = np.array(coords)
        next_coords = np.zeros_like(coords)
        steps = 0
        orig_coords = amph.coords
        while not np.all(next_coords == coords):
            signs = np.sign(np.array(coords) - np.array(amph.coords))
            stepped = False
            for ind in [1, 0]:
                sign = signs[ind]
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
