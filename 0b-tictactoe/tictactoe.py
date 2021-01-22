"""
Tic Tac Toe Player
"""

import math
import copy
import random

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
    move_counter = 0
    for row in board:
        for cell in row:
            if cell != EMPTY:
                move_counter += 1

    # if the move count is 9 then game over, if its' even, then it's first players turn (x), else it's (o) turn
    if move_counter == 9:
        return EMPTY
    elif move_counter % 2 == 0:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    actionList = list()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actionTuple = (i, j)
                actionList.append(actionTuple)
    random.seed()
    random.shuffle(actionList)
    return actionList


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    boardCopy = copy.deepcopy(board)
    i = action[0]
    j = action[1]
    nextMove = player(boardCopy)

    # if the action is valid (aka) than make the action
    if boardCopy[i][j] == EMPTY and nextMove != EMPTY:
        boardCopy[i][j] = nextMove
        return boardCopy
    else:
        raise RuntimeError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # check rows
    for row in board:
        if row[0] != EMPTY and row.count(row[0]) == len(row):
            return row[0]

    # check columns, transpose the array first then check
    boardTransposed = [[EMPTY, EMPTY, EMPTY],
                       [EMPTY, EMPTY, EMPTY],
                       [EMPTY, EMPTY, EMPTY]]
    for i in range(3):
        for j in range(3):
            boardTransposed[i][j] = board[j][i]
    for row in boardTransposed:
        if row[0] != EMPTY and row.count(row[0]) == len(row):
            return row[0]

    # check diagnals, only 2, so manually check
    diagnal1 = [board[0][0], board[1][1], board[2][2]]
    if diagnal1[0] != EMPTY and diagnal1.count(diagnal1[0]) == len(diagnal1):
        return diagnal1[0]
    diagnal2 = [board[0][2], board[1][1], board[2][0]]
    if diagnal2[0] != EMPTY and diagnal2.count(diagnal2[0]) == len(diagnal2):
        return diagnal2[0]

    # in the case where no winner is found, return none
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # if someone won the game, return true
    if winner(board) != None:
        return True

    # if the whole board is not filled yet (game not over), return false, else return true
    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # if someone won the game, or no winner return accordingly, this assumes the board passed in is a terminal state
    theWinner = winner(board)
    if theWinner == X:
        return 1
    elif theWinner == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # return None for boards in terminal state
    if terminal(board):
        return None

    # figure out if we are trying to min or max based on who's move it is
    if player(board) == X:
        goal = 'max'
        currBestVal = -math.inf
    else:
        goal = 'min'
        currBestVal = math.inf

    possibleActions = actions(board)
    for action in possibleActions:
        if goal == 'max':
            currActionVal = min_value(result(board, action))
            if currActionVal > currBestVal:
                currBestVal = currActionVal
                bestAction = action
        else:
            currActionVal = max_value(result(board, action))
            if currActionVal < currBestVal:
                currBestVal = currActionVal
                bestAction = action
    return bestAction


def max_value(board):
    if terminal(board):
        return utility(board)
    value = -math.inf
    for action in actions(board):
        value = max(value, min_value(result(board, action)))
    return value


def min_value(board):
    if terminal(board):
        return utility(board)
    value = math.inf
    for action in actions(board):
        value = min(value, max_value(result(board, action)))
    return value
