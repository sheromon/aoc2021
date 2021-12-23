import numpy as np

from room import Room


def load_input(input_path):
    char_list = []
    length = None
    with open(input_path) as file_obj:
        for line in file_obj:
            chars = list(line[:-1])
            if not length:
                length = len(chars)
            if len(chars) < length:
                chars += ['#'] * (length - len(chars))
            char_list.append(chars)
    return np.array(char_list)


def day23a(input_path, use_solution=False):
    array = load_input(input_path)
    array[-2:, :2] = '#'
    room = Room(array)

    min_energy = None
    if use_solution:
        run_test_case_solution(room)
        min_energy = room.energy_used
    else:
        room.print_info()
        run_room(room)
        if room.complete:
            total_energy = room.energy_used
            print(f'Total energy: {total_energy}')
            if not min_energy:
                min_energy = total_energy
            else:
                min_energy = min(min_energy, total_energy)

    return min_energy


def run_test_case_solution(room):
    """Run the example solution given in the problem.

    This set of moves gives the optimal energy for part 1.
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
    for origin, dest in moves:
        amph = room.get_amph(origin)
        success = room.move(amph, dest)
        if not success:
            room.print_info()
            raise RuntimeError('Failed move')


def run_room(room):
    any_success = True
    while any_success:
        success1 = run_hallway_movers(room)
        success2 = run_room_movers(room)
        any_success = success1 or success2


def run_hallway_movers(room):
    # attempt to move any amphs in the hallway to their home column
    any_success = True
    while any_success:
        any_success = False
        for amph in room.hallway_movers:
            if room.col_is_open(amph.home_col):
                dest_options = [(3, amph.home_col), (2, amph.home_col)]
                for dest in dest_options:
                    if room.array[dest] == '.':
                        success = room.move(amph, dest)
                        if success:
                            any_success = True
                            print(f'Moved {amph}')
                            room.print_info()
                            break
    print('No hallway movers')
    return any_success


def run_room_movers(room):
    # attempt to move an amphipod from a room to the hallway
    for amph in room.room_movers:
        for dest in room.open_coords:
            # ignore non-hallway destinations
            if dest[0] != 1:
                continue
            success = room.move(amph, dest)
            if success:
                print(f'Moved {amph}')
                room.print_info()
                return True
    return False


def test23a():
    assert 12521 == day23a('test_input.txt', use_solution=True)
    assert 12521 == day23a('test_input.txt', use_solution=False)


def day23b(input_path):
    pass


def test23b():
    assert 12521 == day23a('test_input.txt')


if __name__ == '__main__':
    test23a()
    # print('Day 23a:', day23a('day23_input.txt'))
    # test23b()
    # print('Day 23b:', day23b('day23_input.txt'))
