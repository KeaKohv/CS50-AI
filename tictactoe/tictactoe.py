"""
Tic Tac Toe Player
"""

import math
import copy
import sys

sys.setrecursionlimit(10000)

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    # Initializes helper variables to keep track of the number of X-s and O-s on the board
    nrX = 0
    nrO = 0

    # Counts how many X-s and O-s are on the board
    for row in board:
        for cell in row:
            if cell == X:
                nrX += 1
            elif cell == O:
                nrO += 1
    
    # Returns whose turn it is. Does not take into account if it is a terminal state.
    if nrX <= nrO:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    # Initializes an empty set of actions
    actions = set()

    # Goes through the cells to see which are empty.
    # If empty, adds the cell to the set of actions.
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions.add((i, j))

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    # Checks if the action is valid. i and j must be either 0, 1 or 2.
    i = action[0]
    j = action[1]
    if not i in (0, 1, 2) or not j in (0, 1, 2):
        raise Exception

    # Another check if the action is valid. Action must be one of the available actions.
    if not action in actions(board):
        raise Exception

    # See whose turn it is, make a deepcopy of the board, insert their move and return the new board.
    whose_turn = player(board)
    new_board = copy.deepcopy(board)
    new_board[i][j] = whose_turn
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Check if there are 3 X or O in a row horizontally.
    for row in board:
        if row[0] != EMPTY and row.count(row[0]) == len(row):
            return row[0]

    # Check if there are 3 X or O in a row vertically.
    i = 0
    for _ in range(3):
        list = []
        for row in board:
            list.append(row[i])
        if list[0] != EMPTY and list.count(list[0]) == len(list):
            return list[0]
        i += 1


    # Check if there are 3 x or O in a row diagonally.
    # First diagonal
    i = 0
    list = []
    for row in board:
        list.append(row[i])
        i += 1
    if list[0] != EMPTY and list.count(list[0]) == len(list):
        return list[0]

    # The other diagonal
    i = 2
    list = []
    for row in board:
        list.append(row[i])
        i -= 1
    if list[0] != EMPTY and list.count(list[0]) == len(list):
        return list[0]

    # No winner, it is a tie
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # First check if there is a winner. Return true, if there is.
    winner_check = winner(board)
    if winner_check != None:
        return True

    # If there is no winner, check if there are any empty cells.
    # Return false, if an empty cell is found.
    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False

    # If no empty cells are found, return true as this means the game is over, it is a tie.
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # Get the information on the winner from the winner function
    who_won = winner(board)

    if who_won == O:
        return -1
    elif who_won == X:
        return 1
    else:
        # This means no one won, it is a tie.
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # Check if the board is a terminal board.
    game_ended = terminal(board)
    if game_ended == True:
        return None
    
    # See whose turn it is
    whose_turn = player(board)

    # Find the optimal action
    if whose_turn == X:
        # Aiming to maximise
        return max_value(board)[1] # This returns the best move.
    else:
        # Player is O, aiming to minimise
        return min_value(board)[1] # This returns the best move.

# Function that calculates the maximum available value of the current board
# based on available actions.
# Functions max_value and min_value call each other recursively.
def max_value(board):

    # If the game is over, return the utility of the board (1 for X, -1 for O, 0 for tie).
    if terminal(board):
        return utility(board), None

    # Variable that will hold the max value. At first set to negative infinity.
    v = -math.inf
    # Variable that will hold the best move.
    move = None

    # Update the variable v to hold the maximum among min values for available actions.
    for action in actions(board):
        value = min_value(result(board, action))[0]
        if value > v:
            v = value
            move = action
            if v == 1: # This would be a winning move, so return it.
                return v, move

    return v, move

# Similar to the function max value except that it calculates the minimum available value
# of the current board based on available actions.
def min_value(board):

    # If the game is over, return the utility of the board (1 for X, -1 for O, 0 for tie).
    if terminal(board):
        return utility(board), None

    # Variable that will hold min max value. At first set to infinity.
    v = math.inf
    move = None

    # Update the variable v to hold the minimum among max values for available actions.
    for action in actions(board):
        value = max_value(result(board, action))[0]
        if value < v:
            v = value
            move = action
            if v == -1: # This would be a winning move, so return it.
                return v, move
    
    return v, move
