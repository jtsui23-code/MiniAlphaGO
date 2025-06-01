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
        
        # Checks if the move in in the board if its not then the move is invalid
        if not (0 <= x < self.size and 0 <= y < self.size):
            return False
        
        # Making a simulated board where the player's move has already occured to check if the move will capture first beofre a suicide move.
        tempBoard = self.board.copy()
        tempBoard[x,y] = player


        enemyStone = -player

        # This is checking if the suicide move captures first, if it does then this move is legal else the move is invalid.
        captured = False


        # This is checking the liberties of the enemy stones. If this move removes the final liberty of the surround stone, then
        # this is a legal move else it is not.
        for (nx,ny) in self.getSurroundingStones(x,y):

            # This checks if the surrounding possible stones are in the board are enemy stones.
            if 0 <= nx < self.size and 0 <= ny < self.size and tempBoard[nx,ny] == enemyStone:

                # If a surrounding enemy stone can be captured from this suicide move then its valid and simulate the capture.
                if self.checkLiberties((nx,ny), enemyStone, visited=set()) == 0:
                    captured = True
                    tempBoard[nx, ny] = 0

        # This checks the player's own group of stones if this move removes the final liberty of the group which is a suicide move.
        # If the player's move doesn't remove the final liberty of the group then its fine and is a valid move. 
        if self.checkLiberties((x,y), player, visited=set()) > 0:
            return True
        
        # If it is the case where the move is a suicide move BUT captures the enemy stone then its is valid.
        elif captured:
            return True
        
        # However, if the move is a suicide move and doesn't capture then its an illegal move.
        else: 
            return False



    
    def playMove(self, x,y, player):

        isValidMove = self.isValidMove(x,y,player)


        # If the coordinate on the board does not equal zero, 
        # that means that position is not empty or it is out of bound.
        # Meaning that played move is illegal 
        if self.board[x,y] !=0:
            return False
        
        # Player is either a -1 or a 1 meaning the player is either playing as white or black stones
        self.board[x,y] = player
        self.history.append((x,y,player))

        if isValidMove:
            return True
        else:
            return False



