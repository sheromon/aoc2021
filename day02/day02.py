

def day02a(input_path):
    """Ummm... parse the strings, I guess."""
    depth = 0
    pos = 0
    with open(input_path) as file_obj:
        for line in file_obj:
            direction, distance = line.strip().split()
            distance = int(distance)
            if direction == 'forward':
                pos += distance
            elif direction == 'up':
                depth -= distance
            elif direction == 'down':
                depth += distance
            else:
                raise RuntimeError('Bad direction')
    return depth * pos


def test02a():
    assert 150 == day02a('test_input.txt')


def day02b(input_path):
    """Apply weird arbitrary formula to... figure out the submarine's course?"""
    depth = 0
    pos = 0
    aim = 0
    with open(input_path) as file_obj:
        for line in file_obj:
            direction, distance = line.strip().split()
            distance = int(distance)
            if direction == 'forward':
                pos += distance
                depth += aim * distance
            elif direction == 'up':
                aim -= distance
            elif direction == 'down':
                aim += distance
            else:
                raise RuntimeError('Bad direction')
    return depth * pos


def test02b():
    assert 900 == day02b('test_input.txt')


if __name__ == '__main__':
    test02a()
    print('Day 02a:', day02a('day02_input.txt'))
    test02b()
    print('Day 02b:', day02b('day02_input.txt'))
