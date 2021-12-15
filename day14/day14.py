import collections


def load_input(input_path):
    template = None
    rules = dict()
    with open(input_path) as file_obj:
        first = True
        for line in file_obj:
            if first:
                template = line.strip()
                first = False
                continue
            if not line.strip():
                continue
            tokens = line.strip().split()
            rules[tokens[0]] = tokens[-1]
    return template, rules


def day14a(input_path):
    template, rules = load_input(input_path)
    for _ in range(10):
        template = step(template, rules)
    counts = collections.Counter(template)
    common = counts.most_common()
    return common[0][1] - common[-1][1]


def step(template, rules):
    ind = 0
    while ind < len(template) - 1:
        pair = template[ind:ind+2]
        new_char = rules.get(pair)
        if new_char:
            template = template[:ind+1] + new_char + template[ind+1:]
            ind += 1
        ind += 1
    return template


def test14a():
    assert 1588 == day14a('test_input.txt')


def day14b(input_path):
    pass


def test14b():
    assert 2188189693529 == day14b('test_input.txt')


if __name__ == '__main__':
    test14a()
    print('Day 14a:', day14a('day14_input.txt'))
    # test14b()
    # print('Day 14b:', day14b('day14_input.txt'))
