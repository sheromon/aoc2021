
class Amphipod:

    energy_map = {
        'A': 1,
        'B': 10,
        'C': 100,
        'D': 1000,
    }
    home_col_map = {
        'A': 3,
        'B': 5,
        'C': 7,
        'D': 9,
    }

    def __init__(self, letter, coords, energy_used=0):
        self.letter = letter
        self.energy_per_step = self.energy_map[letter]
        self.home_col = self.home_col_map[letter]
        self.coords = coords
        self.energy_used = energy_used

    def __repr__(self) -> str:
        return f'{self.letter}: {self.coords}, {self.energy_used}'

    def step(self, n_steps):
        self.energy_used += n_steps * self.energy_per_step

    @property
    def is_home(self):
        return self.coords[1] == self.home_col
