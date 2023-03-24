"""
Tic Tac Toe Player
"""

import math
import sys
import copy

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

    Logic:  If the number of empty slots % 2 == 1, it is player X's turn
            If the number of empty slots % 2 == 0, it is player O's turn
    """
    emptySlots = countEmptySlots(board)

    if emptySlots % 2 == 0:
        return O

    return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    Logic: If the slot is EMPTY, it is a possible action
    """

    possibleActions = []
    i = 0
    j = 0

    while i < 3:
        while j < 3:
            if board[i][j] == EMPTY:
                possibleActions.append((i, j))
            j += 1
        i += 1
        j = 0

    return possibleActions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    boardCopy = copy.deepcopy(board)

    if board[action[0]][action[1]] != EMPTY:
        sys.exit("Invalid move! Slot already filled.")

    boardCopy[action[0]][action[1]] = player(board)
    return boardCopy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    slots = []
    # Find horizontal winning states
    for row in board:
        if (row[0] == row[1] == row[2]) and row[0] != EMPTY:
            return row[0]

    # Find vertical winning states
    c = 0
    while c < 3:
        if (board[0][c] == board[1][c] == board[2][c]) and board[0][c] != EMPTY:
            return board[0][c]
        c += 1

    diag_one = [(0, 0), (1, 1), (2, 2)]
    diag_two = [(0, 2), (1, 1), (2, 0)]

    diag_one_slots = [board[slot[0]][slot[1]] for slot in diag_one]
    diag_two_slots = [board[slot[0]][slot[1]] for slot in diag_two]

    if (diag_one_slots[0] == diag_one_slots[1] == diag_one_slots[2]
            and diag_one_slots[0] != EMPTY):
        return diag_one_slots[0]

    if (diag_two_slots[0] == diag_two_slots[1] == diag_two_slots[2]
            and diag_two_slots[0] != EMPTY):
        return diag_two_slots[0]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    True if 1) There is a WINNER (will have to call winner function) or
            2) The board is full
    """

    if winner(board) is not None:
        return True

    if countEmptySlots(board) == 0:
        return True

    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1

    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    currentPlayer = player(board)
    possibleActions = actions(board)

    if terminal(board):
        return None

    if currentPlayer == X:
        return maxValue(board)[0]

    return minValue(board)[0]


def printBoard(board):
    for row in board:
        print(row)


def countEmptySlots(board):
    emptySlots = 0
    for row in board:
        for item in row:
            if item == EMPTY:
                emptySlots += 1

    return emptySlots


def maxValue(board):
    # X aims to maximize score
    if terminal(board):
        return (None, utility(board))

    v = -1 * math.inf
    bestAction = ()

    for action in actions(board):
        maxVal = minValue(result(board, action))[1]
        if maxVal > v:
            v = maxVal
            bestAction = action

    return (bestAction, v)


def minValue(board):
    # O aims to minimize score
    if terminal(board):
        return (None, utility(board))

    v = math.inf
    bestAction = ()

    for action in actions(board):
        minVal = maxValue(result(board, action))[1]
        if minVal < v:
            v = minVal
            bestAction = action

    return (bestAction, v)
