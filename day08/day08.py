

def load_input(input_path):
    lines = []
    with open(input_path) as file_obj:
        for line in file_obj:
            lines.append(line.strip())

    ten_patterns_list = []
    four_patterns_list = []
    ind = 0
    while ind < len(lines):
        tokens = lines[ind].partition('|')
        ten_patterns = [set(digit) for digit in tokens[0].split()]
        if tokens[-1]:
            four_patterns = [set(digit) for digit in tokens[-1].split()]
        else:
            ind += 1
            four_patterns = [set(digit) for digit in lines[ind].split()]
        ind += 1
        ten_patterns_list.append(ten_patterns)
        four_patterns_list.append(four_patterns)
    return ten_patterns_list, four_patterns_list


def day08a(input_path):
    _, four_patterns_list = load_input(input_path)

    # map from digit to number of segments for special digits that have a unique
    # number of segments
    segment_counts = {
        1: 2,
        4: 4,
        7: 3,
        8: 7,
    }
    special_counts = [segment_counts[digit] for digit in segment_counts]
    total = 0
    for four_patterns in four_patterns_list:
        total += sum((len(pattern) in special_counts for pattern in four_patterns))
    return total


def test08a():
    assert 26 == day08a('test_input.txt')


def resolve(all_patterns, four_patterns):
    digit_map = dict()

    # sort patterns by number of segments
    # sorted lengths will be 2, 3, 4, 5, 5, 5, 6, 6, 6, 7
    all_patterns = sorted(all_patterns, key=len)

    digit_map[1] = all_patterns[0]  # length 2
    digit_map[7] = all_patterns[1]  # length 3
    digit_map[4] = all_patterns[2]  # length 4
    digit_map[8] = all_patterns[-1] # length 7

    len_5_patterns = all_patterns[3:6]
    len_6_patterns = all_patterns[6:9]

    for pattern in len_6_patterns:
        if digit_map[4] < pattern:
            digit_map[9] = pattern
        elif digit_map[7] < pattern:
            digit_map[0] = pattern
        else:
            digit_map[6] = pattern

    for pattern in len_5_patterns:
        if digit_map[7] < pattern:
            digit_map[3] = pattern
        elif pattern < digit_map[9]:
            digit_map[5] = pattern
        else:
            digit_map[2] = pattern

    assert len(digit_map) == 10

    reverse_digit_map = {tuple(sorted(val)): key for key, val in digit_map.items()}
    four_digits = [reverse_digit_map[tuple(sorted(pattern))] for pattern in four_patterns]
    return sum((val * 10**ind for ind, val in enumerate(four_digits[::-1])))


def day08b(input_path):
    ten_patterns_list, four_patterns_list = load_input(input_path)
    sum = 0
    for ten_patterns, four_patterns in zip(ten_patterns_list, four_patterns_list):
        sum += resolve(ten_patterns, four_patterns)
    return sum


def test08b():
    ten_patterns_list, four_patterns_list = load_input('test_input0.txt')
    5353 == resolve(ten_patterns_list[0], four_patterns_list[0])
    assert 61229 == day08b('test_input.txt')


if __name__ == '__main__':
    test08a()
    print('Day 08a:', day08a('day08_input.txt'))
    test08b()
    print('Day 08b:', day08b('day08_input.txt'))
