import numpy as np




"""
METHOD: generateSymmetries
INPUT:
    board     (Board)     :  Current board state.
    pi        (list)      :  Probablity of all moves on the board.

RETURN:
    boardSym (list)       : List of board symmetries.
    piSym    (list)       : List of pi vector symmetries.
DESCRIPTION:
    This function rotates the current board state 8 times to exploits the symmetry 
    properties of the Go board to dramatically increase training efficiency and reduce bias 
    and return the rotated symmetries of the board and pi vector.
    
"""
def generateSymmetries(board, pi):
    boardSym = []
    piSym = []

    piMatrix = pi.reshape(9,9)  

    # Using k because k is a parameter in np.rot90 meaning how many 90% rotations to perform.
    for k in range(4):

        # np.rot90() has 3 parameters (m, k, axes=()) 
        # m - matrix
        # k - number of 90% rotations
        # axes - 2 axes which is rotated 
        # (-2, -1) is used here because it uses the last 2 dimesnion as the axes of rotation. 
        rotatedBoard = np.rot90(board, k, axes=(-2,-1))
        rotatedPi = np.rot90(piMatrix, k)

        boardSym.append(rotatedBoard)

        # Have to .flatten() because earlier made the pi vector into a matrix
        piSym.append(rotatedPi.flatten())

        flippedBoard = np.flip(rotatedBoard, axis=-1) # flips board horizontally
        flippedPi = np.flip(rotatedPi, axis=1)

        boardSym.append(flippedBoard)
        piSym.append(flippedPi)

    return boardSym, piSym