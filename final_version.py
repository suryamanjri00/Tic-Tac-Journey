#!/usr/bin/env python3
from math import inf as infinity
from random import choice
import platform
import time
from os import system



HUMAN = -1
COMP = +1
board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]


def evaluate(state):
    """
    Function to heuristic evaluation of state.
    :param state: the state of the current board
    :return: +1 if the computer wins; -1 if the human wins; 0 draw
    """
    if wins(state, COMP):
        score = +1
    elif wins(state, HUMAN):
        score = -1
    else:
        score = 0

    return score


def wins(state, player):
    """
    This function tests if a specific player wins. Possibilities:
    * Three rows    [X X X] or [O O O]
    * Three cols    [X X X] or [O O O]
    * Two diagonals [X X X] or [O O O]
    :param state: the state of the current board
    :param player: a human or a computer
    :return: True if the player wins
    """
    win_state = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]
    if [player, player, player] in win_state:
        return True
    else:
        return False


def game_over(state):
    """
    This function test if the human or computer wins
    :param state: the state of the current board
    :return: True if the human or computer wins
    """
    return wins(state, HUMAN) or wins(state, COMP)


def empty_cells(state):
    """
    Each empty cell will be added into cells' list
    :param state: the state of the current board
    :return: a list of empty cells
    """
    cells = []

    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])

    return cells


def valid_move(x, y):
    """
    A move is valid if the chosen cell is empty
    :param x: X coordinate
    :param y: Y coordinate
    :return: True if the board[x][y] is empty
    """
    if [x, y] in empty_cells(board):
        return True
    else:
        return False


def set_move(x, y, player):
    """
    Set the move on board, if the coordinates are valid
    :param x: X coordinate
    :param y: Y coordinate
    :param player: the current player
    """
    if valid_move(x, y):
        board[x][y] = player
        return True
    else:
        return False


def minimax(state, depth, player):
    """
    AI function that choice the best move
    :param state: current state of the board
    :param depth: node index in the tree (0 <= depth <= 9),
    but never nine in this case (see iaturn() function)
    :param player: an human or a computer
    :return: a list with [the best row, best col, best score]
    """
    if player == COMP:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if depth == 0 or game_over(state):
        score = evaluate(state)
        return [-1, -1, score]

    for cell in empty_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = minimax(state, depth - 1, -player)
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == COMP:
            if score[2] > best[2]:
                best = score  # max value
        else:
            if score[2] < best[2]:
                best = score  # min value

    return best


def alphabeta(state, depth, player, alpha, beta):
    """
    AI function that choice the best move
    :param state: current state of the board
    :param depth: node index in the tree (0 <= depth <= 9),
    but never nine in this case (see iaturn() function)
    :param player: an human or a computer
    :param alpha: the best value that the maximizing player currently can guarantee at that level or above
    :param beta: the best value that the minimizing player currently can guarantee at that level or above
    :return: a list with [the best row, best col, best score]
    """
    if player == COMP:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if depth == 0 or game_over(state):
        score = evaluate(state)
        return [-1, -1, score]

    for cell in empty_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = alphabeta(state, depth - 1, -player, alpha, beta)
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == COMP:
            if score[2] > best[2]:
                best = score  # max value
            alpha = max(alpha, best[2])
            if beta <= alpha:
                break
        else:
            if score[2] < best[2]:
                best = score  # min value
            beta = min(beta, best[2])
            if beta <= alpha:
                break

    return best


def expectimax(state, depth, player):
    """
    AI function that chooses the best move using the Expectimax algorithm
    :param state: current state of the board
    :param depth: node index in the tree (0 <= depth <= 9),
    but never nine in this case (see ai_turn() function)
    :param player: a human or a computer
    :return: a list with [the best row, best col, best score]
    """
    if player == COMP:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, 0]

    if depth == 0 or game_over(state):
        score = evaluate(state)
        return [-1, -1, score]

    if player == COMP:
        for cell in empty_cells(state):
            x, y = cell[0], cell[1]
            state[x][y] = player
            score = expectimax(state, depth - 1, HUMAN)
            state[x][y] = 0
            score[0], score[1] = x, y
            if score[2] > best[2]:
                best = score  # max value
    else:  # Opponent's turn (chance node)
        scores = []
        for cell in empty_cells(state):
            x, y = cell[0], cell[1]
            state[x][y] = player
            score = expectimax(state, depth - 1, COMP)
            state[x][y] = 0
            scores.append(score[2])
        best = [-1, -1, sum(scores) / len(scores)]  # average value

    return best



def clean():
    """
    Clears the console
    """
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')


def render(state, c_choice, h_choice):
    """
    Print the board on console
    :param state: current state of the board
    """

    chars = {
        -1: h_choice,
        +1: c_choice,
        0: ' '
    }
    str_line = '---------------'

    print('\n' + str_line)
    for row in state:
        for cell in row:
            symbol = chars[cell]
            print(f'| {symbol} |', end='')
        print('\n' + str_line)


def ai_turn(c_choice, h_choice, algorithm):
    """
    It calls the minimax, alpha-beta pruning, or Expectimax function based on the provided algorithm,
    if the depth < 9, else it chooses a random coordinate.
    :param c_choice: computer's choice X or O
    :param h_choice: human's choice X or O
    :param algorithm: the algorithm to be used (minimax, alphabeta, or expectimax)
    :return:
    """
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return

    clean()
    print(f'Computer turn [{c_choice}]')
    render(board, c_choice, h_choice)

    if depth == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        if algorithm == minimax:
            move = algorithm(board, depth, COMP)
        elif algorithm == alphabeta:
            move = algorithm(board, depth, COMP, -infinity, infinity)
        elif algorithm == expectimax:
            move = algorithm(board, depth, COMP)
        else:
            raise ValueError("Invalid algorithm provided")
        x, y = move[0], move[1]

    set_move(x, y, COMP)
    time.sleep(1)






def human_turn(c_choice, h_choice):
    """
    The Human plays choosing a valid move.
    :param c_choice: computer's choice X or O
    :param h_choice: human's choice X or O
    :return:
    """
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return

    # Dictionary of valid moves
    move = -1
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    clean()
    print(f'Human turn [{h_choice}]')
    render(board, c_choice, h_choice)

    while move < 1 or move > 9:
        try:
            move = int(input('Use numpad (1..9): '))
            coord = moves[move]
            can_move = set_move(coord[0], coord[1], HUMAN)

            if not can_move:
                print('Bad move')
                move = -1
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')

def reset_board():
    """
    Reset the board to its initial state
    """
    global board
    board = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
    ]

def play_game(h_choice, c_choice, first, algorithm):
    """
    Play the Tic Tac Toe game using the specified algorithm
    """
    result = None
    clean()
    while len(empty_cells(board)) > 0 and not game_over(board):
        if first == 'N':
            ai_turn(c_choice, h_choice, algorithm)
            first = ''
        human_turn(c_choice, h_choice)
        ai_turn(c_choice, h_choice, algorithm)
    if wins(board, HUMAN):
        result = 'YOU WIN!'
    elif wins(board, COMP):
        result = 'YOU LOSE!'
    else:
        result = 'DRAW!'
    return result

def main():
    """
    Main function that calls all functions
    """
    clean()
    h_choice = ''  # X or O
    c_choice = ''  # X or O
    first = ''  # if human is the first

    # Human chooses X or O to play
    while h_choice != 'O' and h_choice != 'X':
        try:
            print('')
            h_choice = input('Choose X or O\nChosen: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')

    # Setting computer's choice
    if h_choice == 'X':
        c_choice = 'O'
    else:
        c_choice = 'X'

    # Human may start first
    clean()
    while first != 'Y' and first != 'N':
        try:
            first = input('First to start?[y/n]: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')

    # Main loop of the game with minimax algorithm
    print("\nMINIMAX ALGORITHM")
    minimax_time_start = time.time()
    minimax_result = play_game(h_choice, c_choice, first, minimax)
    minimax_time_end = time.time()
    minimax_time = minimax_time_end - minimax_time_start

    # Reset the board
    reset_board()

    # Main loop of the game with alpha-beta pruning
    print("\nALPHA-BETA PRUNING")
    alphabeta_time_start = time.time()
    alphabeta_result = play_game(h_choice, c_choice, first, alphabeta)
    alphabeta_time_end = time.time()
    alphabeta_time = alphabeta_time_end - alphabeta_time_start

    # Reset the board
    reset_board()

    # Main loop of the game with Expectimax algorithm
    print("\nEXPECTIMAX ALGORITHM")
    expectimax_time_start = time.time()
    expectimax_result = play_game(h_choice, c_choice, first, expectimax)
    expectimax_time_end = time.time()
    expectimax_time = expectimax_time_end - expectimax_time_start

    # Print results
    print("\nMINIMAX RESULT:", minimax_result)
    print("MINIMAX TIME:", minimax_time, "seconds")
    print("\nALPHA-BETA PRUNING RESULT:", alphabeta_result)
    print("ALPHA-BETA PRUNING TIME:", alphabeta_time, "seconds")
    print("\nEXPECTIMAX RESULT:", expectimax_result)
    print("EXPECTIMAX TIME:", expectimax_time, "seconds")

    exit()

if __name__ == '__main__':
    main()
    """
    Main function that calls all functions
    """
    clean()
    h_choice = ''  # X or O
    c_choice = ''  # X or O
    first = ''  # if human is the first

    # Human chooses X or O to play
    while h_choice != 'O' and h_choice != 'X':
        try:
            print('')
            h_choice = input('Choose X or O\nChosen: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')

    # Setting computer's choice
    if h_choice == 'X':
        c_choice = 'O'
    else:
        c_choice = 'X'

    # Human may start first
    clean()
    while first != 'Y' and first != 'N':
        try:
            first = input('First to start?[y/n]: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')

    # Main loop of the game with minimax algorithm
    print("\nMINIMAX ALGORITHM")
    minimax_time_start = time.time()
    minimax_result = play_game(h_choice, c_choice, first, minimax)
    minimax_time_end = time.time()
    minimax_time = minimax_time_end - minimax_time_start

    # Reset the board
    reset_board()

    # Main loop of the game with alpha-beta pruning
    print("\nALPHA-BETA PRUNING")
    alphabeta_time_start = time.time()
    alphabeta_result = play_game(h_choice, c_choice, first, alphabeta)
    alphabeta_time_end = time.time()
    alphabeta_time = alphabeta_time_end - alphabeta_time_start

    # Print results
    print("\nMINIMAX RESULT:", minimax_result)
    print("MINIMAX TIME:", minimax_time, "seconds")
    print("\nALPHA-BETA PRUNING RESULT:", alphabeta_result)
    print("ALPHA-BETA PRUNING TIME:", alphabeta_time, "seconds")

    exit()


if __name__ == '__main__':
    main()
