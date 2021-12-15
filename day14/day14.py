import collections


def load_input(input_path):
    """Load and return the initial polymerization template and insertion rules.

    Rules are returned as a mapping from one pair to the two pairs that result
    from applying the appropriate insertion.
    """
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
            pair, _, insert_char = line.strip().split()
            # apply the insertion to make two pairs
            new_pair1 = pair[0] + insert_char
            new_pair2 = insert_char + pair[1]
            rules[pair] = [new_pair1, new_pair2]
    return template, rules


def day14(input_path, n_steps=10):
    """Return the difference between most and least common elements after n steps."""
    template, rules = load_input(input_path)
    # break the initial template into constituent pairs
    pairs = []
    for ind in range(len(template) - 1):
        pairs.append(template[ind:ind+2])
    # keep track of how many we have of each pair
    pair_counts = collections.Counter(pairs)

    # keep track of how the pairs multiply over n steps
    for _ in range(n_steps):
        pair_counts = step(pair_counts, rules)

    # count the number of each element at the end
    letter_counts = collections.defaultdict(int)
    for pair, counts in pair_counts.items():
        letter_counts[pair[0]] += counts
        letter_counts[pair[1]] += counts
    # each element is in two pairs except for the very first and last elements,
    # so add one extra for those and divide by 2 to get the actual counts.
    letter_counts[template[0]] += 1
    letter_counts[template[-1]] += 1
    for letter in letter_counts:
        letter_counts[letter] //= 2
    return max(letter_counts.values()) - min(letter_counts.values())


def step(pair_counts, rules):
    new_pair_counts = collections.defaultdict(int)
    for pair, counts in pair_counts.items():
        new_pairs = rules[pair]
        for new_pair in new_pairs:
            new_pair_counts[new_pair] += counts
    return new_pair_counts


def day14a(input_path):
    return day14(input_path, n_steps=10)


def test14a():
    assert 1588 == day14a('test_input.txt')


def day14b(input_path):
    return day14(input_path, n_steps=40)


def test14b():
    assert 2188189693529 == day14b('test_input.txt')


if __name__ == '__main__':
    test14a()
    print('Day 14a:', day14a('day14_input.txt'))
    test14b()
    print('Day 14b:', day14b('day14_input.txt'))
