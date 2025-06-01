import numpy as np

class Board:
    def __init__(self, size=9):
        self.size = size

        # 0=empty, 1 = black, -1 = white
        self.board = np.zeros((size, size), dtype=int) 
        self.history = []

    # If the currentIdex is 
    # 0 that means you are checking the liberties of a stone to your right 
    # 1 that means you are checking the liberties of a stone to your left 
    # 2 that means you are checking the liberties of a stone to above 
    # 3 that means you are checking the liberties of a stone to below
    # This means the above indexes would only need 3 liberties to be captured since this is implying that a stone is being placed to capture.


    # -1 that means you are checking the liberties of a stone without considerting a capture

    def checkLiberties(self, position, stoneColor, currentIndex = -1):
        
        hasLiberties = 0

        enemyStone = -stoneColor
        
        

        key = str(currentIndex)
        ignoreThisLiberty = {
            '0': 'RIGHT',
            '1': 'LEFT',
            '2': 'UP',
            '3': 'DOWN',
        }

        surroundingStones = self.getSurroundingStones(position[0], position[1])

        for stone in surroundingStones:
            if ignoreThisLiberty[key] == 'RIGHT' and stone == 0:
                continue

            elif ignoreThisLiberty[key] == 'LEFT' and stone == 1:
                continue

            elif ignoreThisLiberty[key] == 'UP' and stone == 2:
                continue

            elif ignoreThisLiberty[key] == 'DOWN' and stone == 3:
                continue

            else:
                if self.board[stone[0], stone[1]] == stoneColor:
                    pass
                elif self.board[stone[0], stone[1]] == 0:
                    hasLiberties += 1

                elif self.board[stone[0], stone[1]] == enemyStone:
                    checkNeightLibertyCount = self.checkLiberties(stone, stoneColor)
                    hasLiberties += checkNeightLibertyCount


        
        return hasLiberties

    def getSurroundingStones(self,x,y):

        surroundStones = [[x+1, y], [x-1,y], [x,y+1], [x, y-1]]
        return surroundStones


    def isValidMove(self, x,y,player):

        

        enemyStone = -player

        # This is checking if there are any surround stones at all that fully circle the currently placed move.
        surroundingStones = self.getSurroundingStones(x,y)

        placingInEnemySurroundingStone = True

        # Now this is checkinf if the surround stones are enemy stones because this may be an illegal move.
        for stone in surroundingStones:
            if self.board[stone[0], stone[1]] != self.enemyStone:
                placingInEnemySurroundingStone = False
        

        # This is checking if the suicide move captures first, if it does then this move is legal else the move is invalid.
        captureFirst = True

        for stone in surroundingStones:
            checkLiberties = self.checkLiberties(stone, player)


        if placingInEnemySurroundingStone and captureFirst:
            pass


    
    def playMove(self, x,y, player):

        isValidMove = self.isValidMove
        # If the coordinate on the board does not equal zero, 
        # that means that position is not empty or it is out of bound.
        # Meaning that played move is illegal 
        if self.board[x,y] !=0 and isValidMove:
            return False
        
        # Player is either a -1 or a 1 meaning the player is either playing as white or black stones
        self.board[x,y] = player
        self.history.append((x,y,player))

        

        return True



