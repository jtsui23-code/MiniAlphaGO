import numpy as np

class Board:
    def __init__(self, size=9):
        self.size = size

        # 0=empty, 1 = black, -1 = white
        self.board = np.zeros((size, size), dtype=int) 
        self.history = []





    def checkLiberties(self, position, stoneColor, visited = None):

        # If this is the fist iteration of the recursion then create the set that will store all of the 
        # positions that have had their liberties checked.
        if visited == None:
            visited = set()

        # Checking if the position is out of bound of the board.
        x, y = position

        if not( 0<= x < self.size and 0<= y < self.size):
            return 0
        
        # If you already visited this stone then don't check it again.
        if (x, y) in visited:

            return 0

        # If this is your first time visiting this stone then add it to the set. 
        visited.add((x,y))
        
        # This means that there is a liberty at this position
        if self.board[x,y] == 0:
            return 1

        # Do not count any position that has enemy stone there. 
        if self.board[x,y] != stoneColor:
            return 0

        # Creates counter for liberties
        liberties = 0

        # Recursively checking the liberties of neighboring stones because connected stones share liberties.
        for (nx, ny) in self.getSurroundingStones(x,y):
            
            liberties += self.checkLiberties((nx,ny), stoneColor, visited)
        

        return liberties

    def getSurroundingStones(self,x,y):

        surroundStones = [[x+1, y], [x-1,y], [x,y+1], [x, y-1]]
        return surroundStones


    def isValidMove(self, x,y,player):

        
        # This is checking if there are any surround stones at all that fully circle the currently placed move.
        surroundingStones = self.getSurroundingStones(x,y)

        placingInEnemySurroundingStone = True

        # Now this is checks if the surround stones are enemy stones because this may be an illegal move.
        for stone in surroundingStones:
            if self.board[stone[0], stone[1]] != self.enemyStone:
                placingInEnemySurroundingStone = False
        

        # This is checking if the suicide move captures first, if it does then this move is legal else the move is invalid.
        captureFirst = False

        # This is checking the liberties of the enemy stones. If this move removes the final liberty of the surround stone, then
        # this is a legal move else it is not.
        for stone in surroundingStones:
            checkLiberties = self.checkLiberties(stone, player)
            if checkLiberties == 0:
                captureFirst = True


        if placingInEnemySurroundingStone and captureFirst:
            return True
        elif not placingInEnemySurroundingStone:
            return True
        else: 
            return False


    
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



