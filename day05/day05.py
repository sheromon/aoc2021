import numpy as np


def day05(input_path, part_a=True):
    """Count the overlappint points for all valid lines.

    For part a, only horizontal and vertical lines are valid. For part b,
    45-degree diagonal lines are valid as well.
    """
    points1, points2 = load_input(input_path)
    max_vals = np.max(np.vstack([points1, points2]), axis=0)
    grid = np.zeros((max_vals + 1), dtype=np.int)

    for p1, p2 in zip(points1, points2):
        if (p1[0] != p2[0]) and (p1[1] != p2[1]) and part_a:
            continue
        # we should probably check to verify that any diagonal lines are
        # 45-degree diagonal lines, but I guess they all are, because I got the
        # right answer without checking.
        delta = p2 - p1
        for ind in range(np.max(np.abs(delta)) + 1):
            x_ind = p1[0] + ind * np.sign(delta[0])
            y_ind = p1[1] + ind * np.sign(delta[1])
            grid[y_ind, x_ind] += 1
    return np.sum(grid >= 2)


def load_input(input_path):
    points1 = []
    points2 = []
    with open(input_path) as file_obj:
        for line in file_obj:
            tokens = line.strip().split()
            p1 = [int(val) for val in tokens[0].split(',')]
            p2 = [int(val) for val in tokens[-1].split(',')]
            points1.append(p1)
            points2.append(p2)
    return np.array(points1), np.array(points2)


def day05a(input_path):
    return day05(input_path)


def test05a():
    score = day05a('test_input.txt')
    assert 5 == score


def day05b(input_path):
    return day05(input_path, part_a=False)


def test05b():
    score = day05b('test_input.txt')
    assert 12 == score


if __name__ == '__main__':
    test05a()
    print('Day 05a:', day05a('day05_input.txt'))
    test05b()
    print('Day 05b:', day05b('day05_input.txt'))
