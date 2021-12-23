import copy

import numpy as np


def load_input(input_path):
    array = []
    with open(input_path) as file_obj:
        for line in file_obj:
            vals = [int(val) for val in line.strip()]
            array.append(vals)
    return np.array(array)


class Cavern:

    def __init__(self, risk_array):
        self.risk_array = risk_array
        self.high_value = np.sum(self.risk_array)
        self.total_risk_array = self.high_value * np.ones_like(self.risk_array)
        self.total_risk_array[-1, -1] = self.risk_array[-1, -1]


    def explore(self):
        n_cols, n_rows = self.risk_array.shape
        for irow in range(n_rows - 2, 0, -1):
            icol = n_cols - 1
            while irow < n_rows:
                self.total_risk_array[irow, icol] = self.calc_min_risk(irow, icol, self.high_value, set())
                irow += 1
                icol -= 1
        for icol in range(n_cols - 1, -1, -1):
            irow = 0
            while icol >= 0:
                self.total_risk_array[irow, icol] = self.calc_min_risk(irow, icol, self.high_value, set())
                irow += 1
                icol -= 1

    def calc_min_risk(self, irow, icol, max_risk, visited):
        if self.total_risk_array[irow, icol] < self.high_value:
            return self.total_risk_array[irow, icol]

        neighbors = self.get_neighbor_coords(irow, icol)
        adj_total_risks = self.total_risk_array[tuple(zip(*neighbors))]
        min_total = np.min(adj_total_risks)

        next_visited = copy.deepcopy(visited)
        next_visited.add((irow, icol))

        for coords in neighbors[adj_total_risks < self.high_value]:
            if tuple(coords) in visited:
                continue
            next_risk = self.risk_array[tuple(coords)]
            if next_risk >= min(max_risk, min_total):
                continue
            min_total = min(
                min_total,
                self.calc_min_risk(
                    *tuple(coords),
                    min(max_risk, min_total) - next_risk,
                    next_visited,
                ),
            )
        new_total = min_total + self.risk_array[irow, icol]
        return new_total

    def get_neighbor_coords(self, irow, icol):
        deltas = []
        if irow < self.risk_array.shape[0] - 1:
            deltas.append([1, 0])
        if icol < self.risk_array.shape[1] - 1:
            deltas.append([0, 1])
        if irow > 0:
            deltas.append([-1, 0])
        if icol > 0:
            deltas.append([0, -1])
        return np.array([irow, icol]) + np.array(deltas)


def day15a(input_path):
    risk_array = load_input(input_path)
    cavern = Cavern(risk_array)
    cavern.explore()
    return cavern.total_risk_array[0, 0] - cavern.risk_array[0, 0]


def test15a():
    assert 40 == day15a('test_input.txt')


def day15b(input_path):
    risk_array = load_input(input_path)
    array_list = []
    for row_block in range(5):
        array_list_row = []
        for col_block in range(5):
            array_list_row.append(np.copy(risk_array) + row_block + col_block)
        array_list.append(np.concatenate(array_list_row, axis=1))
    risk_array = (np.concatenate(array_list, axis=0) - 1) % 9 + 1

    cavern = Cavern(risk_array)
    cavern.explore()
    return cavern.total_risk_array[0, 0] - cavern.risk_array[0, 0]


def test15b():
    assert 315 == day15b('test_input.txt')


if __name__ == '__main__':
    test15a()
    print('Day 15a:', day15a('day15_input.txt'))
    test15b()
    print('Day 15b:', day15b('day15_input.txt'))
