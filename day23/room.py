import numpy as np

import amphipod


class Room:

    def __init__(self, array):
        self.array = array
        self.open_coords = set(zip(*np.where(array == '.')))
        self.open_coords -= set([(1, 3), (1, 5), (1, 7), (1, 9)])
        self.amphs = []
        self._init_amphs()

    def _init_amphs(self):
        """Create all amphipods based on the input array."""
        for letter in amphipod.Amphipod.energy_map:
            inds = np.where(self.array == letter)
            for coords in zip(*inds):
                amph = amphipod.Amphipod(letter, coords)
                self.amphs.append(amph)

    def to_tuple(self):
        """Return a hashable representation of the room state."""
        return tuple([tuple(row) for row in self.array.tolist()[1:-1]])

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
        """Return list of amphipods that are in rooms and can move."""
        amph_list = []
        for amph in self.amphs:
            if amph.coords[0] == 1:
                continue
            # check if the way out is empty
            if np.all(self.array[1:amph.coords[0], amph.coords[1]] == '.'):
                # but skip this one if it's already at its end position
                if amph.is_home and np.all(self.array[amph.coords[0]:-1, amph.coords[1]] == amph.letter):
                    continue
                amph_list.append(amph)
        return amph_list

    @property
    def hallway_movers(self):
        """Return list of amphipods that are in the hallway and can move."""
        amph_list = []
        for amph in self.amphs:
            if amph.coords[0] == 1 and self.col_is_open(amph.home_col):
                amph_list.append(amph)
        return amph_list

    def col_is_open(self, col):
        """Return True if col is available for an amphipod to end there."""
        letter = amphipod.HOME_COL_REVERSE_MAP[col]
        return np.all((self.array[2:-1, col] == '.') | (self.array[2:-1, col] == letter))

    def check_move(self, amph, coords):
        """Check if amphipod can move to the given position.

        If the move is possible, return True. Otherwise, return False.

        This is just a check, so the amphipod will be in its original position
        at the end of this method.
        """
        # can't move there if the position is occupied
        if coords not in self.open_coords:
            return False
        # an amphipod in the hallway can only move to its home column, so if
        # the destination column isn't its home column, the move is invalid
        if amph.coords[0] == 1 and coords[1] != amph.home_col:
            return False

        can_move = False
        # check if there is a clear path between the origin and destination
        coords = np.array(coords)
        min_coords = np.minimum(coords, np.array(amph.coords))
        max_coords = np.maximum(coords, np.array(amph.coords))
        # temporarily make the current space vacant to make the check easier
        self.array[amph.coords] = '.'
        col_move_first = np.all(self.array[amph.coords[0], min_coords[1]:max_coords[1]+1] == '.')
        row_move_second = np.all(self.array[min_coords[0]:max_coords[0]+1, coords[1]] == '.')
        row_move_first = np.all(self.array[min_coords[0]:max_coords[0]+1, amph.coords[1]] == '.')
        col_move_second = np.all(self.array[coords[0], min_coords[1]:max_coords[1]+1] == '.')
        if (col_move_first and row_move_second) or (row_move_first and col_move_second):
            can_move = True
        # undo the temp change
        self.array[amph.coords] = amph.letter
        return can_move

    def move(self, amph, coords):
        """Move an amphipod to the given position.

        :param amph: either an Amphipod or a tuple of coordinates corresponding
            to the location of an Amphipod
        :param coords: destination coordinates tuple
        """
        if not isinstance(amph, amphipod.Amphipod):
            amph = self.get_amph(amph)
        self.open_coords.remove(coords)
        self.open_coords.add(amph.coords)
        self.array[amph.coords] = '.'
        self.array[coords] = amph.letter
        num_steps = np.abs(np.array(coords) - np.array(amph.coords)).sum()
        amph.step(num_steps)
        amph.coords = coords
