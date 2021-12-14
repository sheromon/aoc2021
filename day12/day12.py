from collections import defaultdict
import copy


def construct_cave_map(input_path):
    """Load cave connections and return dictionary of all valid connections."""
    cave_map = defaultdict(list)
    with open(input_path) as file_obj:
        for line in file_obj:
            tokens = line.strip().split('-')
            # each connection can go both ways, except that going from "end" or
            # to "start" doesn't make sense, so leave out those connections
            cave_map[tokens[0]].append(tokens[1])
            if tokens[0] != 'start' and tokens[1] != 'end':
                cave_map[tokens[1]].append(tokens[0])
    return cave_map


def day12a(input_path):
    """Return the number of valid paths that go from start to end of the caves."""
    cave_map = construct_cave_map(input_path)
    return explore(cave_map, 'start', visited=set())


def explore(cave_map, node, visited):
    """Return the number of valid paths starting at node and ending at 'end'.

    Small caves cannot be visited more than once.
    """
    if node == 'end':
        return 1
    # paths that return to start or small (lowercase) caves are invalid
    if (node == 'start') or (ord(node[0]) >= 97):
        if node in visited:
            return 0
        visited = copy.deepcopy(visited)
        visited.add(node)

    valid_paths = 0
    next_nodes = cave_map[node]
    for next_node in next_nodes:
        valid_paths += explore(cave_map, next_node, visited)

    return valid_paths


def test12a():
    assert 10 == day12a('test_input.txt')


def day12b(input_path):
    """Return the number of valid paths that go from start to end of the caves."""
    cave_map = construct_cave_map(input_path)
    return explore2(cave_map, 'start', defaultdict(int))


def explore2(cave_map, node, visited):
    """Return the number of valid paths starting at node and ending at 'end'.

    At most, one small cave can be visited twice, and other small caves cannot
    be visited more than once.
    """
    if node == 'end':
        return 1
    if (node == 'start') and (visited[node] >= 1):
        return 0
    if ord(node[0]) >= 97:
        if visited[node] >= 2:
            return 0
        visited[node] += 1
        if sum([val == 2 for val in visited.values()]) > 1:
            return 0

    valid_paths = 0
    next_nodes = cave_map[node]
    for next_node in next_nodes:
        valid_paths += explore2(cave_map, next_node, copy.deepcopy(visited))

    return valid_paths


def test12b():
    assert 36 == day12b('test_input.txt')


if __name__ == '__main__':
    test12a()
    print('Day 12a:', day12a('day12_input.txt'))
    test12b()
    print('Day 12b:', day12b('day12_input.txt'))
