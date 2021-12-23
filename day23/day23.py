import copy

import numpy as np

from room import Room


def load_input(input_path, part2=False):
    char_list = []
    length = None
    with open(input_path) as file_obj:
        for line in file_obj:
            chars = list(line[:-1])
            char_list.append(chars)
    if part2:
        extra_lines = [
            list('  #D#C#B#A#'),
            list('  #D#B#A#C#'),
        ]
        char_list = char_list[:-2] + extra_lines + char_list[-2:]
    length = len(char_list[0])
    for chars in char_list:
        if len(chars) < length:
            chars += ['#'] * (length - len(chars))
    char_array = np.array(char_list)
    char_array[2:, :2] = '#'
    return char_array


def day23a(input_path, use_solution=False):
    """Return the minimum energy needed to get amphipods to the end state."""
    array = load_input(input_path)
    room = Room(array)
    # for testing purposes, optionally run the solution provided for the test
    # case instead of searching the solution space
    if use_solution:
        run_test_case_solution(room)
        return room.energy_used
    else:
        return run_room(room, energy_map=dict())


def run_room(room, energy_map):
    """Recursively move amphipods as allowable and fill out the energy map.

    The energy map has room states as keys and minimum energy from that state
    to the ending state as values.
    """
    if room.complete:
        return room.energy_used
    if room.to_tuple() in energy_map:
        return energy_map[room.to_tuple()] + room.energy_used
    min_energy = np.inf
    possible_moves = get_possible_moves_to_hallway(room)
    for move in possible_moves:
        room_copy = copy.deepcopy(room)
        room_copy.move(*move)
        run_hallway_movers(room_copy)
        energy = run_room(room_copy, energy_map)
        if energy:
            min_energy = min(min_energy, energy)
    energy_map[room.to_tuple()] = min_energy - room.energy_used
    return min_energy


def run_hallway_movers(room):
    """Iteratively try to move any amphipods from the hallway to their column.

    Continue until no amphipods are able to move from the hallway.
    """
    any_success = True
    while any_success:
        any_success = False
        for amph in room.hallway_movers:
            # try moving the the innermost position available
            for row in range(room.array.shape[0] - 2, 0, -1):
                dest = (row, amph.home_col)
                if room.array[dest] == '.' and room.check_move(amph, dest):
                    any_success = True
                    room.move(amph, dest)
                    break
    return any_success


def get_possible_moves_to_hallway(room):
    """Find all possible moves that move an amphipod from a room to the hallway.

    :return: tuple (amphipod coords, destination coords, number of steps)
    """
    possible_moves = []
    for amph in room.room_movers:
        for dest in room.open_coords:
            # ignore non-hallway destinations
            if dest[0] != 1:
                continue
            if room.check_move(amph, dest):
                possible_moves.append((amph.coords, dest))
    return possible_moves


def run_test_case_solution(room, max_moves=None):
    """Run the example solution given in the problem.

    This set of moves gives the optimal energy for part 1.
    If this test doesn't pass, then something is very wrong.
    """
    moves = [
        [(2, 7), (1, 4)],
        [(2, 5), (1, 6)],
        [(1, 6), (2, 7)],
        [(3, 5), (1, 6)],
        [(1, 4), (3, 5)],
        [(2, 3), (1, 4)],
        [(1, 4), (2, 5)],
        [(2, 9), (1, 8)],
        [(3, 9), (1, 10)],
        [(1, 8), (3, 9)],
        [(1, 6), (2, 9)],
        [(1, 10), (2, 3)],
    ]
    if max_moves is None:
        max_moves = len(moves)
    num_moves = 0
    for origin, dest in moves:
        amph = room.get_amph(origin)
        room.move(amph, dest)
        num_moves += 1
        if num_moves >= max_moves:
            return


def test23a():
    assert 12521 == day23a('test_input.txt', use_solution=True)
    assert 12521 == day23a('test_input.txt', use_solution=False)


def day23b(input_path):
    """Return the minimum energy needed to get amphipods to the end state.

    Larger state map for part 2.
    """
    array = load_input(input_path, part2=True)
    room = Room(array)
    min_energy = run_room(room, energy_map=dict())
    return min_energy


def test23b():
    assert 44169 == day23b('test_input.txt')


if __name__ == '__main__':
    test23a()
    print('Day 23a:', day23a('day23_input.txt'))
    test23b()
    print('Day 23b:', day23b('day23_input.txt'))
