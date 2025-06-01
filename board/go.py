import numpy as np

class Board:
    def __init__(self, size=9):
        self.size = size

        # 0=empty, 1 = black, -1 = white
        self.board = np.zeros((size, size), dtype=int) 
        self.history = []

    
    def play_move(self, x,y, player):

        # If the coordinate on the board does not equal zero, 
        # that means that position is not empty or it is out of bound.
        # Meaning that played move is illegal 
        if self.board[x,y] !=0:
            return False
        
        # Player is either a -1 or a 1 meaning the player is either playing as white or black stones
        self.board[x,y] = player
        self.history.append((x,y,player))

        # Complement checks the color stone of the player. 
        # If the player is playing as white, then player = -1.
        # Making complement = -1 + 1 which is 0.
        # This means that if the player is whtie then the complement must equal to 0.

        # If the player is playing as black, then player = 1.
        # Meaning that complement = 1 + 1 which is 2.
        # This means that if the player is black then the complement is not 0.
        complement = player + 1
        if complement == 0: 
            # Enemy is playing as black.
            self.enemyStone = 1
        else:
            # Enemey is playing as white.
            self.enemyStone = -1
        

        return True



