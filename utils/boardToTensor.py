import torch 
import numpy as np

def boardToTensor(board):

    # Creates a 3D numpy array filled with zeros with each spot storing 
    # a 32 bit floating point number. Using 32 bit floating point nubmer instead of 
    # 64 bits to save memory and its faster.
    # The 17 in (17, board.size, board.size) comes from the channel size in the network being 17.
    features = np.zeros((17, board.size, board.size), dtype=np.float32)

    # This reversed(board.history[-8]) is grabbing the latest 8 moves and orders them from newest to oldest.
    # 
    for i, pastBytes in enumerate(reversed(board.history[-8])):
        
        # Converts the byte representation of the past board state back into an array size 9x9.
        pastBoard = np.frombuffer(pastBytes, dtype=int).reshape(board.size, board.size)

        # [pastBoard == 1] creates a 2D array of bools same dimension as the pastBoard matrix but sets positions True
        # if they are populated with a black stone there. 
        # Likewise [pastBoard == -1] does the same creating a 2D array of bools same dimesion as the pastBoard matrix 
        # and sets positions on the matrix True that are populated with whtie stones.

        # For white you do features i + 8 beause 
        # within the 17 features 
        # 0 - 7 are black's latest moves
        # 8 - 16 are white's latest moves 
        # and 17 is the current player turn.

        # Lastly the = 1.0 in features[i][pastBoard == 1] and features[i+8][pastBoard == -1] 
        # Sets the 9x9 grid at features[i] which are all defauted to 0.0
        # features[i] = np.array([
        #                           [0.0, 0.0, 0.0],
        #                           [0.0, 0.0, 0.0],
        #                           [0.0, 0.0, 0.0]
        #                        ])
        # Sets that specific location which is True in either [pastBoard == 1] or [pastBoard == -1]
        # To have the value of 1.0
        # so so is features[i][pastBoard == 1] = 1.0 in a sense saving the board history of just black stones 
        # and features[i+8][pastBoard == -1] = 1.0 for white
        # which will be used in the model/GoNet script.

        features[i][pastBoard == 1] = 1.0
        features[i+8][pastBoard == -1] = 1.0


