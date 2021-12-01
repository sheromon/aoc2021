

def day01a(input_path):
    """Find the number of times the value increases."""
    with open(input_path) as file_obj:
        depth_list = [int(line.strip()) for line in file_obj]
    counter = 0
    for ind in range(0, len(depth_list) - 1):
        if depth_list[ind + 1] > depth_list[ind]:
            counter += 1
    return counter


def test01a():
    assert 7 == day01a('test_input.txt')


def day01b(input_path):
    """Find the number of times the sum of three consecutive values increases."""
    with open(input_path) as file_obj:
        depth_list = [int(line.strip()) for line in file_obj]
    counter = 0
    for ind in range(0, len(depth_list) - 3):
        # the sum of three consecutive values increases when the newest value to
        # enter the sliding window is more than the one that is leaving, so we
        # don't actually need to sum, I think
        if depth_list[ind + 3] > depth_list[ind]:
            counter += 1
    return counter


def test01b():
    assert 5 == day01b('test_input.txt')


if __name__ == '__main__':
    test01a()
    print('Day 01a:', day01a('day01_input.txt'))
    test01b()
    print('Day 01b:', day01b('day01_input.txt'))
