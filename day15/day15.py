import numpy as np


def load_input(input_path):
    array = []
    with open(input_path) as file_obj:
        for line in file_obj:
            vals = [int(val) for val in line.strip()]
            array.append(vals)
    return np.array(array)


class Cavern:

    def __init__(self, risk):
        self.risk = risk
        # initialize total risk array to a high value so that it's simple to get
        # the minimum adjacent total risk
        self.high_value = np.sum(self.risk)
        self.total_risk = self.high_value * np.ones_like(self.risk)
        # the total risk at the end postion is just the risk at that position
        self.total_risk[-1, -1] = self.risk[-1, -1]

    def explore(self):
        """Fill out the min total risk for all positions in the cavern."""
        self.calc_first_pass_risk()
        self.update_total_risk()
        self.check_total_risk()

    def calc_first_pass_risk(self):
        """Do a quick first pass of calculating min total risk for the whole cavern.

        Start at the end (bottom right) and move up and to the left, only using
        adjacent values that are below or to the right. This pass will miss any
        paths that have lowest adjacent total risk above or to the left.
        """
        n_cols, n_rows = self.risk.shape
        for irow in range(n_rows - 2, 0, -1):
            icol = n_cols - 1
            while irow < n_rows:
                self.calc_min_risk_low_right(irow, icol)
                irow += 1
                icol -= 1
        for icol in range(n_cols - 1, -1, -1):
            irow = 0
            while icol >= 0:
                self.calc_min_risk_low_right(irow, icol)
                irow += 1
                icol -= 1

    def calc_min_risk_low_right(self, irow, icol):
        """Calculate the min risk for this position considering only adjacent
        positions below and to the right.
        """
        neighbors = self.get_neighbors_low_right(irow, icol)
        adj_total_risks = self.total_risk[tuple(zip(*neighbors))]
        current_risk = self.risk[irow, icol]
        self.total_risk[irow, icol] = np.min(adj_total_risks) + current_risk

    def get_neighbors_low_right(self, irow, icol):
        deltas = []
        if irow < self.risk.shape[0] - 1:
            deltas.append([1, 0])
        if icol < self.risk.shape[1] - 1:
            deltas.append([0, 1])
        return np.array([irow, icol]) + np.array(deltas)

    def get_neighbors(self, irow, icol):
        deltas = []
        if irow < self.risk.shape[0] - 1:
            deltas.append([1, 0])
        if icol < self.risk.shape[1] - 1:
            deltas.append([0, 1])
        if irow > 0:
            deltas.append([-1, 0])
        if icol > 0:
            deltas.append([0, -1])
        return np.array([irow, icol]) + np.array(deltas)

    def update_total_risk(self):
        """The first pass total risk values will be incorrect if the path goes
        down or to the right, so check and fix values as needed.
        """
        needs_update = []
        for irow in range(self.risk.shape[0]):
            for icol in range(self.risk.shape[1]):
                needs_update.append((irow, icol))
        while needs_update:
            new_needs_update = set()
            for coords in list(needs_update):
                new_needs_update |= set(self.update_single(coords[0], coords[1]))
            needs_update = new_needs_update

    def update_single(self, irow, icol):
        """Check a single total risk value and update if needed.

        If the total risk for this position required an update, flag adjacent
        positions for checking (except the one used for the update).
        """
        needs_update = set()
        current = self.total_risk[irow, icol]
        neighbors = self.get_neighbors(irow, icol)
        adj_total_risks = self.total_risk[tuple(zip(*neighbors))]
        min_adj = np.min(adj_total_risks)
        expected = min_adj + self.risk[irow, icol]
        if current > expected:
            self.total_risk[irow, icol] = expected
            new_needs_update = neighbors[adj_total_risks > min_adj]
            needs_update |= set([tuple(coords) for coords in new_needs_update])
        return needs_update

    def check_total_risk(self):
        """Verify that there are no inconsistencies in the total risk map."""
        total_errors = 0
        for irow in range(self.risk.shape[0] - 1, 0, -1):
            for icol in range(self.risk.shape[1] - 1, 0, -1):
                current = self.total_risk[irow, icol]
                neighbors = self.get_neighbors(irow, icol)
                adj_total_risks = self.total_risk[tuple(zip(*neighbors))]
                min_ind = np.argmin(adj_total_risks)
                expected = adj_total_risks[min_ind] + self.risk[irow, icol]
                if current > expected:
                    print(f'Expected {expected} at ({irow}, {icol}) but found {current}.')
                    total_errors += 1
        print(f'Found {total_errors} errors')


def day15a(input_path):
    risk = load_input(input_path)
    cavern = Cavern(risk)
    cavern.explore()
    return cavern.total_risk[0, 0] - cavern.risk[0, 0]


def test15a():
    assert 40 == day15a('test_input.txt')


def day15b(input_path):
    risk = load_input(input_path)
    array_list = []
    for row_block in range(5):
        array_list_row = []
        for col_block in range(5):
            array_list_row.append(np.copy(risk) + row_block + col_block)
        array_list.append(np.concatenate(array_list_row, axis=1))
    risk = (np.concatenate(array_list, axis=0) - 1) % 9 + 1

    cavern = Cavern(risk)
    cavern.explore()
    return cavern.total_risk[0, 0] - cavern.risk[0, 0]


def test15b():
    assert 315 == day15b('test_input.txt')


if __name__ == '__main__':
    test15a()
    print('Day 15a:', day15a('day15_input.txt'))
    test15b()
    print('Day 15b:', day15b('day15_input.txt'))
