import copy

import numpy as np


def load_input(input_path):
    pos_list = []
    with open(input_path) as file_obj:
        for line in file_obj:
            tokens = line.strip().split(':')
            pos_list.append(int(tokens[-1]))
    return pos_list


def day21a(input_path):
    pos_list = load_input(input_path)
    scores = [0, 0]
    done = False
    roll_ind = 1
    while not done:
        for player_ind in range(2):
            next_steps = 3 * roll_ind + 3  # sum of three consecutive ints
            pos_list[player_ind] = (pos_list[player_ind] + next_steps - 1) % 10 + 1
            scores[player_ind] += pos_list[player_ind]
            roll_ind += 3
            if scores[player_ind] >= 1000:
                done = True
                break
    return np.min(scores) * (roll_ind - 1)


def test21a():
    assert 739785 == day21a('test_input.txt')


def day21b(input_path):
    # starting state is one universe with initial positions and scores of zero
    pos_list = load_input(input_path)
    initial_scores = (0, 0)
    # track all possible game states and the number of universes with that state
    active_states = {(tuple(pos_list), initial_scores): 1}

    wins = [0, 0]
    player_ind = 0
    while active_states:
        new_active_states = dict()
        for state, n_univ in active_states.items():
            advance(wins, new_active_states, player_ind, state, n_univ)
        player_ind = (player_ind + 1) % 2
        active_states = copy.deepcopy(new_active_states)

    return np.max(wins)


def advance(wins, active_states, player_ind, current_state, n_univ):
    roll_value_to_counts = {
        3: 1,  # there is one way to get a sum of 3 (1, 1, 1)
        4: 3,  # there are three ways to get a sum of 4...
        5: 6,
        6: 7,
        7: 6,
        8: 3,
        9: 1,
    }

    positions, scores = current_state
    for steps, mult in roll_value_to_counts.items():
        # advance the current player and update their score
        new_pos = (positions[player_ind] + steps - 1) % 10 + 1
        new_score = scores[player_ind] + new_pos
        # if their score is >= 21, game is over so add to player's win total
        if new_score >= 21:
            wins[player_ind] += mult * n_univ
            continue
        # if game is not over, update the dict of active states
        if player_ind == 0:
            new_positions = (new_pos, positions[1])
            new_scores = (new_score, scores[1])
        else:
            new_positions = (positions[0], new_pos)
            new_scores = (scores[0], new_score)
        new_state = (new_positions, new_scores)
        current_count = active_states.get(new_state, 0)
        active_states[new_state] = current_count + mult * n_univ


def test21b():
    assert 444356092776315 == day21b('test_input.txt')


if __name__ == '__main__':
    test21a()
    print('Day 21a:', day21a('day21_input.txt'))
    test21b()
    print('Day 21b:', day21b('day21_input.txt'))
