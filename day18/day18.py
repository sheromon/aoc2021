import ast
import copy
import itertools
import logging


def load_input(input_path):
    """Load and return a list of snailfish numbers."""
    input_list = []
    with open(input_path) as file_obj:
        for line in file_obj:
            input_list.append(ast.literal_eval(line.strip()))
    return input_list


class SnailfishNum:
    """Each snailfish number is a pair, an each element can be a scalar or a pair."""

    def __init__(self, pair):
        self.pair = copy.deepcopy(pair)
        self.pair_map = dict()
        self.scalar_map = dict()
        assert len(pair) == 2, 'Input pair should have length 2'
        self.decompose(pair, ())

    def decompose(self, pair, pre_inds):
        """Break down a snailfish number into its elemental pairs and scalars.

        pair_map tracks the indices (a, b, ...) for all pairs of scalars such
        that snailfish_num[a][b] is the index of a pair two levels deep, and
        snailfish_num[a][b][c] is the index of a pair three levels deep.

        scalar_map similarly tracks the indices for all scalars.

        Each pair is made of two scalars, so in a sense, each pair of scalars
        has one entry in the pair map and two entries in the scalar map.
        """
        for ind in range(2):
            key = pre_inds + (ind,)
            value = pair[ind]
            if isinstance(value, int):
                self.scalar_map[key] = value
            elif all(isinstance(elem, int) for elem in value):
                self.pair_map[key] = value
                self.scalar_map[key + (0,)] = value[0]
                self.scalar_map[key + (1,)] = value[1]
            else:
                self.decompose(value, key)

    def __str__(self):
        return str(self.pair)

    def __add__(self, other):
        new = SnailfishNum([self.pair, other.pair])
        new.reduce()
        return new

    @property
    def magnitude(self):
        """Magnitude is 3 times the first element plus 2 times the second element."""
        def _magnitude(value):
            if isinstance(value, int):
                return value
            return 3 * _magnitude(value[0]) + 2 * _magnitude(value[1])
        return _magnitude(self.pair)

    def reduce(self):
        while self.can_explode() or self.can_split():
            self.explode()
            self.split()

    def can_explode(self):
        """If any pair is nested inside four pairs, the leftmost such pair explodes."""
        for pair_inds in self.pair_map.keys():
            if len(pair_inds) == 4:
                return True
        return False

    def can_split(self):
        """If any regular number is 10 or greater, the leftmost such regular number splits."""
        return any(val > 9 for val in self.scalar_map.values())

    def explode(self, once=False):
        """This is too much to explain."""
        pair_inds_list = sorted(self.pair_map.keys())
        for pair_inds in pair_inds_list:
            if len(pair_inds) < 4:
                continue

            pair_to_explode = self.pair[pair_inds[0]][pair_inds[1]][pair_inds[2]][pair_inds[3]]

            scalar_inds_list = sorted(self.scalar_map.keys())
            last_scalar_before = ()
            first_scalar_after = ()
            for inds in scalar_inds_list:
                if inds < pair_inds:
                    last_scalar_before = inds
                elif inds > pair_inds + (1,):
                    first_scalar_after = inds
                    break

            if last_scalar_before:
                pair = self.pair
                for ind in last_scalar_before[:-1]:
                    pair = pair[ind]
                pair[last_scalar_before[-1]] += pair_to_explode[0]
                self.scalar_map[last_scalar_before] = pair[last_scalar_before[-1]]

            if first_scalar_after:
                pair = self.pair
                for ind in first_scalar_after[:-1]:
                    pair = pair[ind]
                pair[first_scalar_after[-1]] += pair_to_explode[1]
                self.scalar_map[first_scalar_after] = pair[first_scalar_after[-1]]

            self.pair[pair_inds[0]][pair_inds[1]][pair_inds[2]][pair_inds[3]] = 0
            del self.pair_map[pair_inds]
            del self.scalar_map[pair_inds + (0,)]
            del self.scalar_map[pair_inds + (1,)]

            self.scalar_map[pair_inds] = 0
            logging.debug('After explode: %s', self.pair)
            if once:
                return

    def split(self):
        for scalar_inds in sorted(self.scalar_map.keys()):
            value = self.scalar_map[scalar_inds]
            if value < 10:
                continue

            first = value // 2
            second = value - first
            del self.scalar_map[scalar_inds]
            self.pair_map[scalar_inds] = [first, second]
            self.scalar_map[scalar_inds + (0,)] = first
            self.scalar_map[scalar_inds + (1,)] = second

            pair = self.pair
            for ind in scalar_inds[:-1]:
                pair = pair[ind]
            pair[scalar_inds[-1]] = [first, second]
            logging.debug('After split: %s', self.pair)
            return


def sum_list(input_list):
    snailfish_num = SnailfishNum(input_list[0])
    for elem in input_list[1:]:
        snailfish_num = snailfish_num + SnailfishNum(elem)
    return snailfish_num


def day18a(input_path):
    input_list = load_input(input_path)
    snailfish_num = sum_list(input_list)
    return snailfish_num.magnitude


def test18a():
    explode_test_cases = [
        {'input': [[[[[9,8],1],2],3],4], 'expected': [[[[0,9],2],3],4]},
        {'input': [7,[6,[5,[4,[3,2]]]]], 'expected': [7,[6,[5,[7,0]]]]},
        {'input': [[6,[5,[4,[3,2]]]],1], 'expected': [[6,[5,[7,0]]],3]},
        {'input': [[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]], 'expected': [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]},
        {'input': [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]], 'expected': [[3,[2,[8,0]]],[9,[5,[7,0]]]]},
    ]
    for test_case in explode_test_cases:
        logging.debug(test_case['input'])
        snailfish_num = SnailfishNum(test_case['input'])
        snailfish_num.explode(once=True)
        assert snailfish_num.pair == test_case['expected']
        logging.debug('')

    snailfish_num = SnailfishNum([[[[4,3],4],4],[7,[[8,4],9]]]) + SnailfishNum([1,1])
    assert snailfish_num.pair == [[[[0,7],4],[[7,8],[6,0]]],[8,1]]

    sum_test_cases = [
        {
            'input': [
                [1,1],
                [2,2],
                [3,3],
                [4,4],
            ],
            'expected': [[[[1,1],[2,2]],[3,3]],[4,4]],
        },
        {
            'input': [
                [1,1],
                [2,2],
                [3,3],
                [4,4],
                [5,5],
            ],
            'expected': [[[[3,0],[5,3]],[4,4]],[5,5]],
        },
        {
            'input': [
                [1,1],
                [2,2],
                [3,3],
                [4,4],
                [5,5],
                [6,6],
            ],
            'expected': [[[[5,0],[7,4]],[5,5]],[6,6]],
        },
    ]
    for test_case in sum_test_cases:
        snailfish_num = sum_list(test_case['input'])
        assert snailfish_num.pair == test_case['expected']

    assert SnailfishNum([[1,2],[[3,4],5]]).magnitude == 143
    assert SnailfishNum([[[[0,7],4],[[7,8],[6,0]]],[8,1]]).magnitude == 1384
    assert SnailfishNum([[[[1,1],[2,2]],[3,3]],[4,4]]).magnitude == 445
    assert SnailfishNum([[[[3,0],[5,3]],[4,4]],[5,5]]).magnitude == 791

    assert 4140 == day18a('test_input.txt')


def day18b(input_path):
    max_mag = 0
    input_list = load_input(input_path)
    for comb in itertools.combinations(input_list, 2):
        mag = (SnailfishNum(comb[0]) + SnailfishNum(comb[1])).magnitude
        max_mag = max(mag, max_mag)
        mag = (SnailfishNum(comb[1]) + SnailfishNum(comb[0])).magnitude
        max_mag = max(mag, max_mag)
    return max_mag


def test18b():
    assert 3993 == day18b('test_input.txt')


if __name__ == '__main__':
    test18a()
    print('Day 18a:', day18a('day18_input.txt'))
    test18b()
    print('Day 18b:', day18b('day18_input.txt'))
