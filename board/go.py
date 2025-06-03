import numpy as np

"""
CLASS: Board

ATTRIBUTES:
    int size:             Stores the dimension of the Go board (e.g., 9 for a 9x9 board).
    numpy.ndarray board:  A 2D array representing the Go board. 
                          0 indicates an empty intersection, 
                          1 indicates a black stone, and 
                          -1 indicates a white stone.
    list history:         Stores a history of moves made on the board. Each entry is a tuple (x, y, player).

METHODS:
    __init__(size=9):                       Constructor to initialize the board.
    checkLiberties(position, stoneColor, visited=None): Calculates the number of liberties for a stone or group of stones.
    removeStones(position, color):          Removes a stone and any connected stones of the same color that have no liberties.
    getSurroundingStones(x, y):             Returns a list of coordinates for positions adjacent to (x,y).
    isValidMove(x, y, player):              Checks if placing a stone by 'player' at (x,y) is a valid move according to Go rules.
    playMove(x, y, player):                 Attempts to place a stone for 'player' at (x,y) and updates the board state.
    printBoard():                           Prints a text-based representation of the current board state.

PACKAGES:
    import numpy as np: Used for efficient numerical operations, especially for the board representation as a 2D array.

DESCRIPTION:
    The Board class encapsulates the logic and state of a Go game board. 
    It handles the placement of stones, checks for valid moves (including suicide and ko - though ko is not explicitly implemented here but isValidMove structure allows for it), 
    calculates liberties, captures opponent stones, and maintains the history of moves.
    The board is represented as a 2D numpy array where 0 signifies an empty point, 1 signifies a black stone, and -1 signifies a white stone.
"""
class Board:

    """
    METHOD: __init__

    INPUT:
        size (int, optional): The dimension of one side of the square Go board. Defaults to 9.

    RETURN:
        N/A

    DESCRIPTION:
        Constructor for the Board class. Initializes an empty Go board of the specified size.
        The board is represented by a 2D numpy array filled with zeros.
        It also initializes an empty list to store the history of moves.
    """
    def __init__(self, size=9):
        self.size = size

        # 0=empty, 1 = black, -1 = white
        self.board = np.zeros((size, size), dtype=int) 

        # Stores the board states as bytes to make them hashable with easy look up for detecting ko violations.
        self.history = []
        
        # This is a flag to prevent player from performing multiple moves a turn.
        # It will store a -1 - white or 1 - black
        # Black plays first so it self.currentPlayer is default to black.
        self.currentPlayer = 1

        # Need to count the number of consecutive passes because if there are 2 consecutive passes then the game ends.
        self.passCount = 0


    """
    METHOD: checkLiberties

    INPUT:
        position (tuple):      (x,y) coordinates of the stone whose liberties are to be checked.
        stoneColor (int):      The color of the stone/group (1 for black, -1 for white) whose liberties are being checked.
        visited (set, optional): A set of (x,y) coordinates that have already been visited during the current liberty check (used for recursion). 
                               Defaults to None and is initialized as an empty set in the first call.
        board           :      The temporary board from the isValidMove method is passed in to reduce the actual recquired liberty if capture is possible.

    RETURN:
        int: The total number of unique liberties for the stone or group of stones connected to the initial 'position'.

    DESCRIPTION:
        This method recursively counts the number of empty adjacent intersections (liberties) for a given stone
        and all connected stones of the same color (a group).
        It uses a 'visited' set to avoid recounting liberties or getting into infinite loops with circular groups.
        - If the position is off-board, it contributes 0 liberties.
        - If the position has already been visited in the current check, it contributes 0 liberties to avoid double counting.
        - If the position is an empty intersection (self.board[x,y] == 0), it's a liberty, returning 1.
        - If the position contains an opponent's stone, it's not a liberty for 'stoneColor', returning 0.
        - If the position contains a stone of 'stoneColor', it recursively calls checkLiberties for its unvisited neighbors.
    """
    def checkLiberties(self, position, stoneColor, visited = None, board=None):
        
        if board is None:
            board = self.board
        # If this is the fist iteration of the recursion then create the set that will store all of the 
        # positions that have had their liberties checked.
        if visited == None:
            visited = set()

        # Checking if the position is out of bound of the board.
        x, y = position


        if not(0 <= x < self.size and 0 <= y < self.size):
            return 0
        
        # If you already visited this stone then don't check it again.
        if (x, y) in visited:

            return 0

        # If this is your first time visiting this stone then add it to the set. 
        visited.add((x,y))
        
        # This means that there is a liberty at this position
        if board[x,y] == 0:
            return 1

        # Do not count any position that has enemy stone there. 
        if board[x,y] != stoneColor:
            return 0

        # Creates counter for liberties
        liberties = 0

        # Recursively checking the liberties of neighboring stones because connected stones share liberties.
        for (nx, ny) in self.getSurroundingStones(x,y):
            
            liberties += self.checkLiberties((nx,ny), stoneColor, visited, board)
        

        return liberties
    
    """
    METHOD: removeStones
    
    INPUT: 
        position (tuple): (x,y) pair for the coordinate of which stone to start the removal check from.
        color (int):      The stone color (1 for black, -1 for white) of the stones to be removed. 
    
    RETURN: 
        N/A
    
    DESCRIPTION:
        This method removes a group of stones of the specified 'color' starting from 'position' if they have no liberties.
        It uses a Depth First Search (DFS) to find all connected stones of the given 'color'.
        All stones identified as part of the group to be removed are set to 0 (empty) on the board.
        This method is typically called after a check (like checkLiberties) has determined that the group at 'position'
        is indeed captured (has zero liberties).
    """
    def removeStones(self, position, color):
        

        toRemove = set()
        visited = set()

        #   """
        #   SUB-METHOD: dfs (nested function)
        #
        #   INPUT:
        #       pos (tuple): (x,y) coordinate of the current stone being visited.
        #
        #   RETURN:
        #       N/A
        #
        #   DESCRIPTION:
        #       Performs a Depth First Search to find all connected stones of the specified 'color'
        #       starting from the initial 'pos'. Adds stones to be removed to the 'toRemove' set.
        #   """
        def dfs(pos):
            x, y = pos

            # Do not traverse through stones that already have been visited.
            if (x, y) in visited: 
                return 
            
            visited.add((x,y))

            # Do not traverse through 'stones' that are outside of the board.
            if not (0 <= x < self.size and 0 <= y < self.size):
                return

            # If the stone is not the same color stone as the one you are trying to 
            # remove then ignore it.
            if self.board[x,y] != color:
                return
            
            if self.checkLiberties((x,y), color, visited=set(), board=self.board) > 0:
                return
            
            toRemove.add((x,y))

            # This recurisvely checks if there are any connected stones that need to be removed as well.
            for nx, ny in self.getSurroundingStones(x,y):
                dfs((nx,ny))

        
        dfs(position)

        # Removes all of the stones that were select for removal.
        for x, y in toRemove:
            self.board[x,y] = 0

    

    """
    METHOD: getSurroundingStones

    INPUT:
        x (int): The x-coordinate of the central stone.
        y (int): The y-coordinate of the central stone.

    RETURN:
        list: A list of [x,y] coordinate pairs representing the positions immediately adjacent (up, down, left, right)
              to the input (x,y) coordinate. Does not check if these coordinates are within board boundaries.

    DESCRIPTION:
        A helper method that returns the four orthogonal neighboring coordinates of a given point (x,y) on the board.
    """
    def getSurroundingStones(self,x,y):

        surroundStones = [[x+1, y], [x-1,y], [x,y+1], [x, y-1]]
        return surroundStones



    """
    METHOD: isValidMove

    INPUT:
        x (int):      The x-coordinate of the proposed move.
        y (int):      The y-coordinate of the proposed move.
        player (int): The color of the player making the move (1 for black, -1 for white).

    RETURN:
        bool: True if the move is valid according to Go rules, False otherwise.

    DESCRIPTION:
        Checks if placing a stone for 'player' at (x,y) is a legal move.
        A move is invalid if:
        1. It is outside the board boundaries.
        2. The position is already occupied (handled in playMove, but good to be aware).
        3. It is a "suicide" move: placing the stone results in the newly placed stone (or its group) having zero liberties,
           UNLESS placing this stone captures one or more opponent stones, thereby giving the new stone/group liberties.
        This method simulates the move on a temporary board to check for captures and self-capture (suicide) conditions.






        Note: Ko rule is not explicitly implemented here but this is where it would be checked.









    """
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
                if self.checkLiberties((nx,ny), enemyStone, visited=set(), board=tempBoard) == 0:
                    captured = True
                    # Simluates capturing the stone for checking for suicides captures or ko.
                    self.simulatedCapture(tempBoard, (nx,ny), enemyStone)



        # Checking for ko violations.
        # Turning the simulationed board into bytes to efficiently check if there is any repeating board states
        # that would cause a ko. self.history[1] is the last board state.
        if len(self.history) > 0:
            if tempBoard.tobytes() == self.history[-1]:
                return False


        # This checks the player's own group of stones if this move removes the final liberty of the group which is a suicide move.
        # If the player's move doesn't remove the final liberty of the group then its fine and is a valid move. 
        if self.checkLiberties((x,y), player, visited=set(), board=tempBoard) > 0:
            return True
        
        # If it is the case where the move is a suicide move BUT captures the enemy stone then its is valid.
        elif captured:
            
            return True
        
        # However, if the move is a suicide move and doesn't capture then its an illegal move.
        else: 
            return False



    """
    METHOD: playMove

    INPUT:
        x (int):      The x-coordinate where the stone is to be played.
        y (int):      The y-coordinate where the stone is to be played.
        player (int): The color of the player making the move (1 for black, -1 for white).
        passTurn (bool): Checks if the player wants to pass this turn.

    RETURN:
        bool: True if the move was successfully played, False if the move was illegal.

    DESCRIPTION:
        Attempts to play a stone for the given 'player' at coordinates (x,y).
        1. Checks if the target intersection (x,y) is empty.
        2. Validates the move using `isValidMove` (checks for out-of-bounds, suicide).
        3. If valid, places the stone on the board and adds the move to history.
        4. Checks adjacent enemy stones/groups. If any are captured (no liberties), they are removed using `removeStones`.
        This method updates the actual game board.
    """
    def playMove(self, x,y, player, passTurn=False):

        # If the player is passing, switch turns and increment the self.passCount.
        # Need to keep track of consecutive passes because if there is 2 consecutive passes then 
        # the game ends.
        if passTurn:
            self.currentPlayer *= -1
            self.passCount += 1
            return
        else: 
            # Resets self.passCount back to zero because only keeping track of consecutive passes not total.
            self.passCount = 0


        # If the coordinate on the board does not equal zero, 
        # that means that position is not empty or it is out of bound.
        # Meaning that played move is illegal 
        if self.board[x,y] !=0:
            return False
        
        # Players playing on not their turn is not valid.
        # This prevents players from playing multiple moves per turn.
        if self.currentPlayer != player:
            return False
        
        if not self.isValidMove(x,y, player):
            return False

        # Player is either a -1 or a 1 meaning the player is either playing as white or black stones
        self.board[x,y] = player
        # Storing the board states as bytes to make them hashable with easy look up for detecting ko violations.
        self.history.append(self.board.copy().tobytes())

        enemy = -player

        # This checks to remove any possible dead stones around where the player placed their move
        for nx, ny in self.getSurroundingStones(x,y):
            if (0 <= nx < self.size and 0 <= ny < self.size and self.board[nx,ny] == enemy):
                self.removeStones((nx,ny), enemy)


        # Switches to the next player's turn.
        self.currentPlayer *= -1
            
        
        
    """
    METHOD: printBoard

    INPUT:
        N/A

    RETURN:
        N/A

    DESCRIPTION:
        Prints a simple text-based representation of the current Go board state to the console.
        '●' represents a black stone.
        '○' represents a white stone.
        '+' represents an empty intersection.
    """
    def printBoard(self):
        symbols = {1: 'b', -1: 'w', 0: '+'}
        for row in self.board:
            print(' '.join(symbols[val] for val in row))
        print()

    """
    METHOD: simulatedCapture
    
    INPUT: 
        board           : The temporary board that is simulating the capture of a stone. 
        position (tuple): (x,y) pair for the coordinate of which stone to start the removal check from.
        color (int):      The stone color (1 for black, -1 for white) of the stones to be removed. 
    
    RETURN: 
        N/A
    
    DESCRIPTION:
        This method simulates removing a group of stones of the specified 'color' starting from 'position' if they have no liberties.
        It uses a Depth First Search (DFS) to find all connected stones of the given 'color'.
        All stones identified as part of the group to be removed are set to 0 (empty) on the board.
        This method is typically called after a check (like checkLiberties) has determined that the group at 'position'
        is indeed captured (has zero liberties).
    """
    def simulatedCapture(self, board, position, color):
        toRemove = set()
        visited = set()

        def dfs(pos):
            x, y = pos 
            if (x,y) in visited:
                return

            visited.add((x,y)) 

            if not (0 <= x < self.size and 0 <= y < self.size):
                return

            if board[x,y] != color:
                return 
            
            # Don't check liberties again, we already know this group is captured
            toRemove.add((x,y))

            for (nx, ny) in self.getSurroundingStones(x,y):
                dfs((nx,ny))
            
            dfs(position)

            # Remove captured stones from the temporary board
            for x,y in toRemove:
                board[x,y] = 0


        
        
if __name__ == "__main__":
    b = Board(size=9)


    # Check for ko -----------------------------------------------------------------------------------------------------------------------------------------------------
    # Example: surround a white stone and capture it
    # b.playMove(1, 2, 1)  
    # b.playMove(3, 2, 1)  
    # b.playMove(2, 3, 1)  

    # b.playMove(2, 0, -1)  
    # b.playMove(1, 1, -1)  
    # b.playMove(3, 1, -1)  
    # b.playMove(2, 2, -1)  





    # print("Before:")

    # # print("Before capture:")
    # b.printBoard()

    # b.playMove(2, 1, 1)  # white goes in the middle



    # print("After:")
    # # print("After capture:")

    # b.printBoard()

    # print("Ko Check:")
    # # print("After capture:")

    # b.playMove(2, 2, -1)  # white goes in the middle

    # b.printBoard()

    # print("Ko Redo:")
    # # print("After capture:")

    # b.playMove(2, 5, -1)  # white goes in the middle

    # b.printBoard()


    # print("Ko again:")
    # # print("After capture:")

    # b.playMove(2, 2, -1)  # white goes in the middle

    # b.printBoard()

    # Check for ko -----------------------------------------------------------------------------------------------------------------------------------------------------







    # Check for Turn Manager -----------------------------------------------------------------------------------------------------------------------------------------------------

    # turnCount = 1
    # print("Turn", turnCount, "------------------------------------------------------------------------------------")
    # turnCount += 1


    # b.playMove(1, 4, 1)  
    # b.playMove(3, 4, 1)  
    # b.playMove(2, 4, 1)  

    # b.printBoard()

    # print("Turn", turnCount, "------------------------------------------------------------------------------------")
    # turnCount += 1
    # # print("Before capture:")




    # b.playMove(1, 1, -1)  
    # b.playMove(3, 1, -1)  
    # b.playMove(2, 2, -1)  

    # b.printBoard()



    # print("Turn", turnCount, "------------------------------------------------------------------------------------")
    # turnCount += 1

    # b.playMove(3, 4, 1)  

    # # print("Before capture:")
    # b.printBoard()



    # print("Turn", turnCount, "------------------------------------------------------------------------------------")
    # turnCount += 1

    # b.playMove(3, 5, 1)  

    # # print("Before capture:")
    # b.printBoard()


    # print("Turn", turnCount, "------------------------------------------------------------------------------------")
    # turnCount += 1

    # b.playMove(3, 7, -1)  

    # # print("Before capture:")
    # b.printBoard()


    # print("Turn", turnCount, "------------------------------------------------------------------------------------")
    # turnCount += 1

    # b.playMove(3, 7, 1)  

    # # print("Before capture:")
    # b.printBoard()

    # Check for Turn Manager -----------------------------------------------------------------------------------------------------------------------------------------------------







    # Check for Passing  -----------------------------------------------------------------------------------------------------------------------------------------------------

    turnCount = 1
    print("Turn", turnCount, "------------------------------------------------------------------------------------")
    turnCount += 1


    b.playMove(1, 4, 1)  
 

    b.printBoard()


    print("Turn", turnCount, "------------------------------------------------------------------------------------")
    turnCount += 1


    b.playMove(3, 4, -1)  

    b.printBoard()



    print("Turn", turnCount, "------------------------------------------------------------------------------------")
    turnCount += 1

    print("Passed turn here-----------------------")
    b.playMove(1, 4, 1, passTurn=True)  
 

    b.printBoard()


    print("Turn", turnCount, "------------------------------------------------------------------------------------")
    turnCount += 1


    b.playMove(1, 6, 1)  
 

    b.printBoard()


    print("Turn", turnCount, "------------------------------------------------------------------------------------")
    turnCount += 1


    b.playMove(1, 6, -1)  
 

    b.printBoard()


    # Check for Passing  -----------------------------------------------------------------------------------------------------------------------------------------------------




