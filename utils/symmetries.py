import numpy as np
import torch




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

    # boardNp = board.cpu().numpy()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Convert pi to tensor on GPU
    # Need 2 variables because the 82th element in the list is pass which would not fit in a 
    # 9x9 matrix.
    # piBoard = torch.tensor(pi[:81], device=device, dtype=torch.float32).reshape(9, 9)
    # piPass = torch.tensor([pi[81]], device=device, dtype=torch.float32)  # Keep as tensor

    piBoard = pi[:81].to(device).reshape(9, 9)
    piPass = pi[81:82].to(device)


    # piBoard = torch.tensor(pi[:81], device=device).reshape(9,9)

    # piPass = pi[81]

    # Using k because k is a parameter in np.rot90 meaning how many 90% rotations to perform.
    for k in range(4):

        # torch.rot90() has 3 parameters (m, k, dims=()) 
        # m - matrix
        # k - number of 90% rotations
        # axes - 2 axes which is rotated 
        # (-2, -1) is used here because it uses the last 2 dimesnion as the dims of rotation. 
        rotatedBoard = torch.rot90(board, k, dims=(-2, -1))
        rotatedPi = torch.rot90(piBoard, k, dims=(-2, -1))

        boardSym.append(rotatedBoard)


        # Concatenates the pi tesnors as one on the GPU.
        piSym.append(torch.cat([rotatedPi.flatten(), piPass]))

        # Flips board and pi horizontally
        flippedBoard = torch.flip(rotatedBoard, dims=[-1]) 
        flippedPi = torch.flip(rotatedPi, dims=[-1])

        
        boardSym.append(flippedBoard)
        piSym.append(torch.cat([flippedPi.flatten(), piPass]))

    return boardSym, piSym