
START_TO_END = {
    '[': ']',
    '{': '}',
    '(': ')',
    '<': '>',
}

POINTS_DICT = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}


def day10a(input_path):
    """Calculate and return the total syntax error score."""
    lines = []
    with open(input_path) as file_obj:
        for line in file_obj:
            lines.append(line.strip())

    counter = {key: 0 for key in POINTS_DICT}
    for line in lines:
        corrupt_char = check_line(line)
        if corrupt_char in counter:
            counter[corrupt_char] += 1
        elif corrupt_char is not None:
            raise RuntimeError(f'Unexpected corrupt character {corrupt_char}')

    return sum([POINTS_DICT[key] * val for key, val in counter.items()])


def check_line(line):
    """If line is corrupt, return corrupt character; otherwise, return None."""
    ind = 0
    close_list = []
    while ind < len(line):
        char = line[ind]
        if char in START_TO_END:
            close = START_TO_END[char]
            close_list.append(close)
        else:
            close = close_list.pop()
            if char != close:
                return char
        ind += 1
    return None


def test10a():
    line = '{([(<{}[<>[]}>{[]{[(<()>'
    assert check_line(line) == '}'

    score = day10a('test_input.txt')
    assert 26397 == score


def day10b(input_path):
    pass


def test10b():
    pass


if __name__ == '__main__':
    test10a()
    print('Day 10a:', day10a('day10_input.txt'))
    # test10b()
    # print('Day 10b:', day10b('day10_input.txt'))
