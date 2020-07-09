"""
Tic Tac Toe Player
"""
import copy
import math
import numpy as np

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
    X = 0
    O = 0
    for row in board:
        for square in row:
            if (square == "X"):
                X += 1
            elif (square == "O"):
                O += 1

    if (X <= O or (X == 0 and O == 0)):
        player = "X"
    else: 
        player = "O"


    return player 



def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = []

    for i in range(0,3):
        for j in range(0,3):
            if (board[i][j] == EMPTY):
                actions.append((i, j))

    return actions



def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if (action not in actions(board)):
        raise Exception('Invalid action')

    copiedBoard = copy.deepcopy(board)

    copiedBoard[action[0]][action[1]] = player(board)
        
    return copiedBoard



def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    winner = None

    if((board[0][0] == board[1][1]) and (board[1][1] == board[2][2])):
        """ Case in that wins with diagonal completed """
        winner = board[0][0]

    elif((board[2][0] == board[1][1]) and (board[1][1] == board[0][2])):
        """ Case in that wins with second diagonal row completed """
        winner = board[2][0]


    transposeBoard = np.transpose(board)

    for i in range(0,3):

        if (len(set(board[i])) == 1 and (board[i][0] is not None)):
            winner = board[i][0]
        elif (len(set(transposeBoard[i])) == 1 and (transposeBoard[i][0] is not None)):
            winner = transposeBoard[i][0]



    return winner



def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    terminated = False
    count = 0

    for i in range(0,3):
        for j in range(0,3):
            if (board[i][j] != EMPTY):
                count += 1

    """ Return True if everything is filled or if there is already a winner """
    if ((winner(board) != None) or count == 9):
        terminated = True
    

    return terminated



def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    output = 0

    if (winner(board) == X):
        output = 1
    elif (winner(board) == O):
        output = -1


    return output



def max_value(board):
    """
    Returns the highest value on the possible options given the current state
    """

    if (terminal(board)):
        return (utility(board), None)

    """ All the possible actions for the player in that situation """
    v = float("-inf")
    possibleActions = actions(board)

    for action in possibleActions:
        minimizer = min_value(result(board, action))

        if (v < minimizer[0]):
            v = minimizer[0]
            chosenAction = action


    return (v, chosenAction)



def min_value(board):
    """
    Returns the lowest value on the possible options given the current state
    """

    if (terminal(board)):
        return (utility(board), None)

    """ All the possible actions for the player in that situation """
    v = float("inf")
    possibleActions = actions(board)

    for action in possibleActions:
        maximizer = max_value(result(board, action))

        if (v > maximizer[0]):
            v = maximizer[0]
            chosenAction = action


    return (v, chosenAction)



def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if (terminal(board)):
        return None

    if (player(board) == X):
        xPlayer = max_value(board)
        action = xPlayer[1]
    else:
        oPlayer = min_value(board)
        action = oPlayer[1]

    return action
