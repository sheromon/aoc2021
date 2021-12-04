import numpy as np


class BingoBoard:

    def __init__(self, board_values):
        self.numbers = np.array(board_values)
        assert self.numbers.shape[0] == self.numbers.shape[1]
        self.size = self.numbers.shape[0]
        self.hits = np.zeros_like(self.numbers, dtype=np.bool)
        self.last_number = None
        self.done = False

    def has_bingo(self):
        """Check for bingo. Diagonals don't count!"""
        return np.any(self.hits.sum(axis=0) == self.size) or \
            np.any(self.hits.sum(axis=1) == self.size)

    def check_number(self, val):
        """Check if new number is on the board (if board is still in play).

        If we have bingo, return the score. If we don't have bingo, return None.
        """
        if self.done:
            return self.score
        match_inds = self.numbers == val
        assert match_inds[:].sum() <= 1
        self.hits[match_inds] = True
        self.last_number = val
        if self.has_bingo():
            self.done = True
            return self.score
        return None

    @property
    def score(self):
        """Return the score (the sum of unmarked numbers times the last number)."""
        return self.numbers[~self.hits][:].sum() * self.last_number


def day04a(input_path):
    """Return the score for the first board to get bingo."""
    number_list, board_list = load_input(input_path)
    for val in number_list:
        for board in board_list:
            score = board.check_number(val)
            if score is not None:
                return score


def test04a():
    score = day04a('test_input.txt')
    assert 4512 == score


def day04b(input_path):
    """Return the score for the last board to get bingo."""
    number_list, board_list = load_input(input_path)
    for val in number_list:
        for board in board_list:
            score = board.check_number(val)
            # this assumes there will be one last board (no ties), but the
            # problem seems to indicate that this will be the case, so we trust.
            if (score is not None) and (len(board_list) == 1):
                return score
        # remove boards that have already gotten bingo
        board_list = [board for board in board_list if not board.done]


def test04b():
    score = day04b('test_input.txt')
    assert 1924 == score


def load_input(input_path):
    with open(input_path) as file_obj:
        number_list = [int(val) for val in file_obj.readline().strip().split(',')]
        lines = [line.strip() for line in file_obj]
    board_list = []
    count = 0
    board_input = []
    for line in lines:
        if not line:
            continue
        board_input.append([int(val) for val in line.split()])
        count += 1
        if count == 5:
            board_list.append(BingoBoard(board_input))
            count = 0
            board_input = []
    return number_list, board_list


if __name__ == '__main__':
    test04a()
    print('Day 04a:', day04a('day04_input.txt'))
    test04b()
    print('Day 04b:', day04b('day04_input.txt'))
