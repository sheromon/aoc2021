import numpy as np


def load_input(input_path):
    pos_list = []
    with open(input_path) as file_obj:
        for line in file_obj:
            tokens = line.strip().split(':')
            pos_list.append(int(tokens[-1]))
    return pos_list


def day20a(input_path):
    pos_list = load_input(input_path)
    scores = [0, 0]
    done = False
    roll_ind = 1
    while not done:
        for player_ind in range(2):
            next_steps = 3 * roll_ind + 3  # sum of three consecutive ints
            pos_list[player_ind] = (pos_list[player_ind] + next_steps - 1) % 10 + 1
            scores[player_ind] += pos_list[player_ind]
            # print(f'Player {player_ind+1} score: {scores[player_ind]}')
            roll_ind += 3
            if scores[player_ind] >= 1000:
                done = True
                break
    return np.min(scores) * (roll_ind - 1)


def test20a():
    assert 739785 == day20a('test_input.txt')


def day20b(input_path):
    pass


def test20b():
    assert 3351 == day20b('test_input.txt')


if __name__ == '__main__':
    test20a()
    print('Day 20a:', day20a('day21_input.txt'))
    # test20b()
    # print('Day 20b:', day20b('day20_input.txt'))
