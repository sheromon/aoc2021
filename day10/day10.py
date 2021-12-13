import numpy as np


def day10a(input_path):
    """Calculate and return the total syntax error score."""
    points_dict = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137,
    }
    lines = []
    with open(input_path) as file_obj:
        for line in file_obj:
            lines.append(line.strip())

    counter = {key: 0 for key in points_dict}
    for line in lines:
        corrupt_char, _ = check_line(line)
        if corrupt_char in counter:
            counter[corrupt_char] += 1
        elif corrupt_char is not None:
            raise RuntimeError(f'Unexpected corrupt character {corrupt_char}')

    return sum([points_dict[key] * val for key, val in counter.items()])


def check_line(line):
    """Check line for corrupt character or incompleteness.

    Return tuple (corrupt_char, close_list). If line is corrupt, close_list will
    be None. If line is incomplete, corrupt_char will be None.
    """
    start_to_end = {
        '[': ']',
        '{': '}',
        '(': ')',
        '<': '>',
    }

    ind = 0
    close_list = []
    while ind < len(line):
        char = line[ind]
        if char in start_to_end:
            close = start_to_end[char]
            close_list.append(close)
        else:
            close = close_list.pop()
            if char != close:
                return char, None
        ind += 1
    return None, close_list


def test10a():
    line = '{([(<{}[<>[]}>{[]{[(<()>'
    assert check_line(line)[0] == '}'
    assert 26397 == day10a('test_input.txt')


def day10b(input_path):
    """Calculate and return the middle completion score."""
    lines = []
    with open(input_path) as file_obj:
        for line in file_obj:
            lines.append(line.strip())

    incomplete_lines = []
    score_list = []
    close_list = []
    for line in lines:
        _, close_list = check_line(line)
        if close_list:
            incomplete_lines.append(line)
            close_str = ''.join(close_list[::-1])
            close_list.append(close_str)
            score = score_string(close_str)
            score_list.append(score)
    scores = np.sort(np.array(score_list))
    return scores[len(scores) // 2]


def score_string(line):
    points_dict = {
        ')': 1,
        ']': 2,
        '}': 3,
        '>': 4,
    }
    total = 0
    for char in line:
        total *= 5
        total += points_dict[char]
    return total


def test10b():
    assert score_string('])}>') == 294
    assert 288957 == day10b('test_input.txt')


if __name__ == '__main__':
    test10a()
    print('Day 10a:', day10a('day10_input.txt'))
    test10b()
    print('Day 10b:', day10b('day10_input.txt'))
