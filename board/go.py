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

        # Need to tally captured stones for scoring.
        # These are the captured stones that the player playing white has.
        self.whiteStonePrisoners = 0

        # These are the captured stones that the player black has.
        self.blackStonePrisoners = 0



    """
    METHOD: checkLiberties

    INPUT:
        position (tuple):      (x,y) coordinates of the stone whose liberties are to be checked.
        stoneColor (int):      The color of the stone/group (1 for black, -1 for white) whose liberties are being checked.
        visited (set): A set of (x,y) coordinates that have already been visited during the current liberty check (used for recursion). 
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
            
            # Keeping track of the captured stones for scoring purposes.
            if self.board[x,y] == 1:
                self.whiteStonePrisoners += 1

            elif self.board[x,y] == -1:
                self.blackStonePrisoners += 1
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
    METHOD: floodFill

    INPUT:
        x (int):      The x-coordinate where the stone is to be played.
        y (int):      The y-coordinate where the stone is to be played.
        visited (set): A set of (x,y) coordinates that have already been visited during the current liberty check (used for recursion). 


    RETURN:
        territory (set): Contains all of the empty space surrounded by groups of stone.
        borderColor (set): Contains all of the stone colors that surround the territory only want this to be one color else the territory is neutral.

    DESCRIPTION:
        This method iteratively finds adjacent groups of stones that will be return for scoring purposes. The method will be 
        called after the removal of dead groups of stones so the method does not have to account for them.
    """
    def floodFill(self, x, y, visited):

        # Set for containing all of the empty space for a territory.
        territory = set()

        # Set for keeping track of the color stone that is surround the territory.
        # If there is only one color then that means the territory belongs to that stone color.
        # Else the territory is neutral so no one gains points from it. 
        borderColor = set()

        # The queue is a means for traversing through new positions on the border for territory counting.
        queue = [(x,y)]

        while queue:    
            cx, cy = queue.pop(0)

            # Do not count the same position more than once.
            if (cx, cy) in visited:
                continue
            
            territory.add((cx,cy))
            visited.add((cx,cy))

            # Check neighboring positions if they need to be counted for territory status.
            for nx, ny in self.getSurroundingStones(cx,cy):
                if not (0<= nx < self.size and 0<= ny < self.size):
                    continue

                # If the position is empty and has not been visited yet this is for (nx,ny) not (cx, cy) above.
                # Then proceed to check its territory status and its neighboring squares too.
                if self.board[nx,ny] == 0 and (nx,ny) not in visited:
                    queue.append((nx,ny))
                
                # If the position is not empty that means a stone is occupying that space. Add the color stone to the set.
                # Since this is a set it won't have duplicates.
                elif self.board[nx,ny] != 0:

                    borderColor.add(self.board[nx,ny])

        # If there is only one stone color bordering the territory then the territory belongs to that stone.
        if len(borderColor) == 1:
            return territory, borderColor.pop()
        
        # Else the territory is neutral counting for no one.
        return territory, 0
    


   
    # def hasTwoEyes(self, group):
    #     eyes = 0

    #     # Gets all of the empty neighboring positions to the grid because some of those empty surround spaces could be an eye.
    #     for x, y in group:
    #         emptyNeighbors = [
    #             (nx,ny) for nx,ny in self.getSurroundingStones(x,y)
    #             if 0 <= nx < self.size and 0 <= ny < self.size and self.board[nx,ny] == 0
    #         ]

    #         # Now checks in reverse the surround of the empty neighboring positions to check if any of them are surround by the 
    #         # same color stone as the group because that would make the empty space a potiential eye.

    #         for ex, ey in emptyNeighbors:
    #             neighbors = self.getSurroundingStones(ex,ey)

    #             # This line checks if a single empty point (a potential "eye")
    #             # is completely surrounded by stones of the same color as the group.
    #             # If it is, we count it as a valid eye.
    #             if (0 <= nx < self.size and 0 <= ny < self.size and self.board[nx, ny] == self.board[x,y] for nx,ny in neighbors):
    #                 eyes += 1

    #     return eyes >= 2

    # def hasTwoEyes(self, group):
    #     if not group:
    #         False

    #     samplePos = next(iter(group))
    #     groupColor = self.board[samplePos[0], samplePos[1]]

    #     eyes = []

    #     checkedEyes = set()

    #     for x, y in group:
    #         for nx, ny in self.getSurroundingStones(x,y):
    #             if 0<= nx < self.size and 0<= ny < self.size and self.board[nx,ny] == 0 and (nx,ny) not in checkedEyes:

    #                 if self.isEye((nx,ny),groupColor):
    #                     eyes.append((nx,ny))
    #                     checkedEyes.add((nx,ny))


    #     return len(eyes) >= 2
    


    """
    METHOD: hasTwoEyes

    INPUT:
        group (set):      Contains a group of connect stones that are the same color.
   

    RETURN:
        Bool : Returns True if there are at 2 valid eye found in a group of stones.

    DESCRIPTION:
        This method iteratively checks for the potiential eye space that a given group of stones has and 
        counts the number of valid eyes it has. If the group has at least 2 eyes then the method returns True.

    """

    # def hasTwoEyes(self,group):
    #     if not group:
    #         return False
        
    #     samplePos = next(iter(group))

    #     groupColor = self.board[samplePos[0], samplePos[1]]

    #     pointsInEye = set()
    #     eyeCount = 0

    #     emptyNeighbors = set()

    #     for x, y in group:
    #         for nx,ny in self.getSurroundingStones(x,y):
    #             if 0 <= nx < self.size and 0 <= ny < self.size and self.board[nx, ny] == 0:
    #                 emptyNeighbors.add((nx,ny))

            
    #     for startPos in emptyNeighbors:
    #         if startPos in pointsInEye:
    #             continue

    #         region = set()
    #         borderColors = set()

    #         queue = [startPos]

    #         visitedRegion = {startPos}

    #         while queue:
    #             cx, cy = queue.pop(0)
    #             region.add((cx,cy))

    #             for nx,ny in self.getSurroundingStones(cx,cy):
    #                 if not (0 <= nx < self.size and 0 <= ny < self.size):
    #                     continue

    #                 neighborValue = self.board[nx,ny]


    #                 if neighborValue == 0:
    #                     if (nx,ny) not in visitedRegion:
                            
    #                         queue.append((nx,ny))
    #                         visitedRegion.add((nx,ny))
    #                 else:
    #                     borderColors.add(neighborValue)

    #         if borderColors == {groupColor}:

    #             isFalseEye = False
    #             if len(region) == 1:
    #                 px, py = next(iter(region))
    #                 if not self.checkSinglePointEyeDiagonals(px,py, groupColor):
    #                     isFalseEye = True

                
    #             if not isFalseEye:
    #                 eyeCount += 1
    #                 pointsInEye.update(region)

    #         if eyeCount >= 2:
    #             return True
            
    #     return eyeCount >= 2





                    


    # ------------------------------------------------------------------------------------------------------------------------------------
    # def hasTwoEyes(self, group):
    #     if not group: 
    #         return False
        
    #     samplePos = next(iter(group))
    #     groupColor = self.board[samplePos[0], samplePos[1]]

    #     eyeRegion = self.findEyeSpace(group, groupColor)

    #     validEyes = 0
        
    #     for region in eyeRegion:
    #         if self.isValidEye(region, groupColor):
    #             validEyes += 1

    #         if validEyes >= 2:
    #             return True
        
    #     return False
    # ------------------------------------------------------------------------------------------------------------------------------------






    
    # def isEye(self, pos, groupColor):
    #     x, y = pos

    #     for nx,ny in self.getSurroundingStones(x,y):
    #         if 0 <= nx < self.size and 0 <= ny < self.size:
    #             if self.board[nx,ny] != groupColor:
    #                 return False

    #     diagonals = [(x+1, y+1) ,(x+1, y-1), (x-1, y+1)(x-1, y-1)]
    #     enemyOrEmpty = 0

    #     for dx, dy in diagonals:
    #         if 0 <= dx < self.size and 0 <= dy < self.size:
    #             if self.board[dx,dy] != groupColor:
    #                 enemyOrEmpty += 1


    """
    METHOD: isValidEye

    INPUT:
        eyeRegion (set):                Contains a region of empty space that is potientially an eye.
        groupColor (int):               Color of the stones surround the empty space to know whose territory it is.
   

    RETURN:
        Bool : Returns True if the empty space is a valid eye.

    DESCRIPTION:
        This method iteratively checks for the all of the surrounding stones around a empty region if its surrounded by 
        the correct stone color to be deemed an eye along with checking for the diagonal positions of single space regions
        because they are weaker.

    """
    def isValidEye(self, eyeRegion, groupColor):

        # If there is no empty space then there is no eye.
        if not eyeRegion:
            return False
        
        # Checks the surround stone color around this empty space.
        for x, y in eyeRegion:
            if not self.isSpaceSurroundedByColor(x,y, groupColor):
                return False

        # If the empty space is only one large then have to check diagonal positions too not just adjacent ones
        # because the single space points are weaker.
        if len(eyeRegion) == 1:
            x,y = next(iter(eyeRegion))
            return self.checkSinglePointEyeDiagonals(x,y, groupColor)

        return True
    
    """
    METHOD: identifyDeadStones

    INPUT:
        N/A

    RETURN:
        deadStones (set):   Contains all of the groups of dead stones on the board.

    DESCRIPTION:
        This method iteratively checks for the all of the groups of stones on the board and detects whether or not 
        the group of stones are dead or alive and returns all of the groups of dead stones it found as a set.

    """
    def identifyDeadStones(self):

        # Creates a set for storing all of the found dead stones 
        # and visited positions on the board to prevent repeats.
        deadStones = set()
        visited = set()

        # Checks every position on the board.
        for x in range(self.size):
            for y in range(self.size):

                # If the position is not an empty space, it is occupied by a stone so check for its group if its alive or 
                # dead.
                if self.board[x,y] != 0 and (x,y) not in visited:
                    group = self.getGroup(x,y)
                    visited.update(group)

                    # Checking for the liberties of the group and its number of eyes.
                    liberties = self.checkLiberties((x,y),self.board[x,y])
                    hasTwoEyes = self.hasTwoEyes(group)

                    # A group without 2 eyes is dead. If a group of stones are in enemy territory without 2 eyes they are also 
                    # dead.
                    # if not hasTwoEyes and (liberties <= 1 or self.isInEnemyTerritory(group)):
                    #     deadStones.update(group)

                    # If a group of stones do not have at least 2 eyes then they are dead.
                    if not hasTwoEyes:
                        deadStones.update(group)




        return deadStones
    
    """
    METHOD: isInEnemyTerritory

    INPUT:
        group (set):      Contains a group of connect stones that are the same color.

    RETURN:
        Bool :            Returns True if you are in enemy territory.

    DESCRIPTION:
        This method iteratively checks for the surrounding radius of the group of stones for the ratio of 
        enemy stones there are. If there are more than 60% of enemy stones surround a group of stones then 
        they are considered to be inside of enemy territory.

    """
    def isInEnemyTerritory(self,group):

        # If there is no group then end the method.
        if not group: 
            return False
        
        # Getting the stone color of the group and the enemy.
        samplePos = next(iter(group))
        groupColor = self.board[samplePos[0], samplePos[1]]
        enemyColor = -groupColor

        # Counters for the total enemy of stones in the radius and everthing else 
        # for getting a ratio of enemies in the surrounding.
        enemyCount = 0
        totalCount = 0

        # Checks the the radius of 2 positions around each of the stones in the group for 
        # what is surrounding the group.
        for gx,gy in group:
            
            # Checking with a radius of 2 needs to include negative values for dx/dy otherwise it would only 
            # Check one direction horizontally and vertically.
            for dx in range(-2,3):
                for dy in range(-2,3):
                    
                    # Getting the radius positions to check what is there. 
                    nx, ny = gx + dx, gy + dy

                    # If there is an enemy there increment enemyCount but you always increment totalCount whether its 
                    # empty, friendly stone, or and enemy stone.
                    if 0<= nx < self.size and 0 <= ny < self.size:
                        totalCount += 1
                        
                        if self.board[nx,ny] == enemyColor:
                            enemyCount += 1

        
        # If there is more than 60% of enemy stones in the surrounding area then 
        # you are considered inside of enemy territory.
        return totalCount > 0 and (enemyCount/totalCount) > 0.6




    """
    METHOD: checkSinglePointEyeDiagonals

    INPUT:
        X (int):                        The x-coordinate of empty space.
        y (int):                        The y-coordinate of empty space.
        groupColor (int):               Color of the stones surround the empty space to know whose territory it is.
   

    RETURN:
        Bool : Returns whether or not the single space is a valid eye or not.

    DESCRIPTION:
        This method iteratively checks for the all of the diagonals of a single empty space region because 
        single space regions are weaker in that they have a limit on how many diagonals they can have occupied by an 
        enemy to invalidate them as an eye.

    """
    def checkSinglePointEyeDiagonals(self, x, y, groupColor):


        diagonals = [(x+1, y+1), (x+1, y-1), (x-1, y+1), (x-1, y-1)]
        enemyDiagonals = 0


        # Need to check the relative position of the single empty space because corner positions are 
        # weaker than center or edge positions on the board when it comes to creating a valid eye.
        onEdgeX = (x == 0 or x == self.size -1)
        onEdgeY = (y == 0 or y == self.size -1)
        onCorner = (onEdgeX and onEdgeY)

        # Checks the diagonals of the empty space and counts the number of enemy stones occupy its diagonal.
        for dx, dy in diagonals:
            if 0 <= dx < self.size and 0 <= dy < self.size:
                if self.board[dx,dy] != groupColor and self.board[dx,dy] != 0:
                    enemyDiagonals += 1

        # If the empty space is on a corner, then it cannot have any enemy stone occupying its diagonal.
        if onCorner:
            return enemyDiagonals == 0
        # Otherwise a max of 1 enemy in a diagonal is fine.
        else:
            return enemyDiagonals <= 1
     






    """
    METHOD: findEyeSpace

    INPUT:
        group (set):      Contains a group of connect stones that are the same color.
        groupColor (int):               Color of the stones surround the empty space to know whose territory it is.
   

    RETURN:
        eyeRegion (array): A list of coordinates of eye spaces this needs to be a list because some eyes are bigger than 1 space.

    DESCRIPTION:
        This method iteratively checks for the all of the neighboring empty spaces around a group of stones and then checks if
        those empty spaces have the potiential of being an eye. Then checks if the eye space is surround by the correct stone color
        for eye detection.

    """
    def findEyeSpace(self, group, groupColor):

        # If group is empty, then there is no potiential eye there.
        if not group:
            return []
        
        potientialEyeSpace = set()

        # Derives the empty neighboring spaces around the group of stones.
        for gx, gy in group:
            for nx, ny in self.getSurroundingStones(gx,gy):
                if (0 <= nx < self.size and 0 <= ny < self.size and self.board[nx, ny] == 0):
                    potientialEyeSpace.add((nx,ny))


        eyeRegion = []
        visitedSpaces = set()

        # Checks for any connected empty spaces because they are potiential eye spaces. 
        # Then checks if the eye space is surround by the correct stone color
        # for eye detection which occurs in the getConnectedEmptyRegion method.
        for x, y in potientialEyeSpace:
            if (x,y) not in visitedSpaces:
                region = self.getConnectedEmptyRegion(x,y, groupColor, visitedSpaces)

                if region:
                    eyeRegion.append(region)

        return eyeRegion
    


    """
    METHOD: getConnectedEmptyRegion

    INPUT:
        startX (int):                   The x-coordinate where the empty space region starts.
        starty (int):                   The y-coordinate where the empty space region starts.
        groupColor (int):               Color of the stones surround the empty space to know whose territory it is.
        globalVisitedSpaces (set):      Contains a coordinates of already visited spaces to prevent repeats.
   

    RETURN:
        region (set): A group empty connect spaces that may potientially be an eye.

    DESCRIPTION:
        This method iteratively checks for the all of the connected empty space in a surrounding territory this is 
        for searching for potiential eye spaces which is useful for detecting 2 eyes.

    """
    
    def getConnectedEmptyRegion(self, startX, startY, groupColor, globalVisitedSpaces):

        # Region is the conenected group os empty space.
        region = set()

        # Queue stores all of the starting position and its neighboring spaces.
        queue = [(startX, startY)]

        # localVisitedSpaces prevents the repeat of already visited spaces.
        localVisitedSpace = set()

        while queue:

            x,y = queue.pop(0)

            # Prevents repeats.
            if (x,y) in localVisitedSpace:
                continue
            
            # Prevent out of board positions.
            if not (0 <= x < self.size and 0 <= y < self.size):
                continue
            
            # Only checking empty spaces not stones.
            if self.board[x,y] != 0:
                continue
            
            # Checks if the correct color stones are surrounding this region of empty space if so 
            # then this empty space is home to an eye.
            if not (self.isSpaceSurroundedByColor(x,y, groupColor)):
                continue
            
            # If the empty space passes all of these rules then it will be marked as a connect empty region.
            localVisitedSpace.add((x,y))
            globalVisitedSpaces.add((x,y))
            region.add((x,y))

            # Searches for other empty spaces that could potientially be comprised in the same potiential eye space.
            for nx, ny in self.getSurroundingStones(x,y):
                if (nx,ny) not in localVisitedSpace:
                    queue.append((nx,ny))

        # Returns the region of the connected empty region.
        return region
    

    """
    METHOD: isSpaceSurroundedByColor

    INPUT:
        X (int):                        The x-coordinate of empty space.
        y (int):                        The y-coordinate of empty space.
        groupColor (int):               Color of the stones surround the empty space to know whose territory it is.
   

    RETURN:
        bool : Boolean of whether this specific empty space has any surround friendly stones.

    DESCRIPTION:
        This method iteratively checks for the all of the connected empty space in a surrounding territory this is 
        for searching for potiential eye spaces which is useful for detecting 2 eyes.

    """
    def isSpaceSurroundedByColor(self, x, y, groupColor):

        # If the coordinate is not of an empty, it is not valid.
        if self.board[x,y] != 0:
            return False
        
        # Check the neighbors of this empty space
        for nx, ny in self.getSurroundingStones(x,y):
            if 0 <= nx < self.size and 0 <= ny < self.size:

                # Checking if the surround stones to the empty space contains only enemy stones if so 
                # then if space cannot be an eye space.
                if self.board[nx,ny] != groupColor and self.board[nx,ny] != 0:
                    return False
                
        return True
                



    



    """
    METHOD: score

    INPUT:
        N/A

    RETURN:
        finalScore (dict): The keys are the player (-1, 1) and their respective score after considering 
        stone count, territory count and prisoner stones and captured stones..

    DESCRIPTION:
        This method is using the Chinese Scoring system which includes the stones in the score as well. The method 
        iteratively checks for dead stones to remove from the board and use for scoring. Also, the method iteratively
        checks for the stone count of alive stones and territory count for the scoring process.
    """
 
    def score(self):
        
        # Gets all of the dead stones on the board.
        deadStones = self.identifyDeadStones()


        

        # Use the scoring board.
        scoringBoard = self.board.copy()


        deadStonesType = {1:0, -1:0}

        for x, y in deadStones:
            deadStonesType[self.board[x,y]] += 1

        # Creating copy of board with the dead stones removed.
        
        # Storing prisoner stones derived from dead stones.
        prisonerStones = {
             1:0, 
            -1: 0
        }

        # Filters through the dead stones to get all of the prisoner stones. 
        for x, y in deadStones:
            
            # If the dead stone color is black, then its white's prisoner.
            if scoringBoard[x,y] == 1:
                prisonerStones[-1] += 1

            # If the dead stone is white, then its black's prisoner.
            elif scoringBoard[x,y] == -1:
                prisonerStones[1] += 1

            # # Make remove the dead stone in the temporary scoring board.
            scoringBoard[x,y] = 0

        # Saves the original board because it be needed.
        originalBoard = self.board.copy()
        self.board = scoringBoard


        visited = set()

        # Counts all of the territory.
        territoryScore = {1: 0, -1: 0}

        # Counts all of the stones surrounding the territory.
        stoneCount = {1:0, -1:0}

        # Parse through the entire board and start counting alive stones.
        for x in range(self.size):
            for y in range(self.size):

                if self.board[x,y] != 0:
                    stoneCount[self.board[x,y]] += 1
        
        # Parse through the entire board and start counting territory.
        for x in range(self.size):
            for y in range(self.size):
                
                # Checks for the area of the territory and its owner.
                if self.board[x,y] == 0 and (x,y) not in visited:

                    # floodFill returns a set representing the individual positions in territory and a 1/-1 for its owner.
                    # if the second returned value is a 0 then no one owns the territory.
                    area, owner = self.floodFill(x,y, visited)

                    if owner in territoryScore:
                        # Have to use len() for area because area is a set which stores all of the coordinates in the 
                        # territory not an int value representing the magnitude of the area.
                        territoryScore[owner] += len(area)


        # Reverts back to the original board.
        self.board = originalBoard

        # Calculates the final score for both players including stone count, territory count and prisoner stones and 
        # captured stones.
        # The difference between prisonerStones[1] and self.blackStonePrisoners is that 
        # prisonerStones[1] is from dead stones on the board when scoring while self.blackStonePrisoner is from captured stones.
        # Same thing goes for prisonerStone[-1] and self.whiteStonePrisoner.

        finalScores = {
            1: territoryScore[1] + stoneCount[1] + prisonerStones[1] + self.blackStonePrisoners,
            -1: territoryScore[-1] + stoneCount[-1] + prisonerStones[-1] + self.whiteStonePrisoners
        }

        # finalScores = {
        #     1: territoryScore[1] + stoneCount[1] + prisonerStones[1] + self.blackStonePrisoners,
        #     -1: territoryScore[-1] + stoneCount[-1] + prisonerStones[-1] + self.whiteStonePrisoners
        # }

        print("Dead Stones:", deadStones)
        print("Prisoners:", prisonerStones)
        print("Territory:", territoryScore)
        print("Stone Count:", stoneCount)

        return finalScores

                    



    """
    METHOD: getGroup

    INPUT:
        x (int):      The x-coordinate where the stone is to be played.
        y (int):      The y-coordinate where the stone is to be played.
   

    RETURN:
        group: Set of all the connect stones which will be counted as points towards a player's score.

    DESCRIPTION:
        This method iteratively finds adjacent groups of stones that will be return for scoring purposes. The method will be 
        called after the removal of dead groups of stones so the method does not have to account for them.
    """
    def getGroup(self, x,y):

        # Derives the color of stone we are getting the group of based off of coordinates
        color = self.board[x,y]

        # If the color is 0 that means its an empty space so there is no need to count the groups of 'stones'
        if color == 0:
            return set()
        

        # group is a set of all the group of stones that will be return.
        group = set()

        # This stack is the means to track which coordinate to traverse and count next.
        stack = [(x,y)]

        # This for loop will continue until there is no more connected groups of stones of the same color to include in the 
        # group set to be returned.
        while stack:
            cx, cy = stack.pop()

            # This if statement is here to prevent visiting the same position multiple times.
            if (cx, cy) not in group:
                group.add((cx,cy))

                # This for loop is searching for any other possible neighboring stones that would be in 
                for nx, ny in self.getSurroundingStones(cx, cy):
                    if (0 <= nx < self.size and 0 <= ny < self.size and self.board[nx,ny] == color):
                        stack.append((nx,ny))
                        
        return group




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

    # turnCount = 1
    # print("Turn", turnCount, "------------------------------------------------------------------------------------")
    # turnCount += 1


    # b.playMove(1, 1, 1)  
 

    # b.printBoard()


    # print("Turn", turnCount, "------------------------------------------------------------------------------------")
    # turnCount += 1


    # b.playMove(3, 4, -1)  

    # b.printBoard()



    # print("Turn", turnCount, "------------------------------------------------------------------------------------")
    # turnCount += 1

    # print("Passed turn here-----------------------")
    # b.playMove(0, 1, 1)  
 

    # b.printBoard()


    # print("Turn", turnCount, "------------------------------------------------------------------------------------")
    # turnCount += 1


    # b.playMove(1, 6, 1)  
 

    # b.printBoard()



    # Checking if scoring works -------------------------------------------------------------------------------------------------------------

    turn = 1

    def next_turn():
        global turn
        print(f"Turn {turn} --------------------------------------------")
        turn += 1
        b.printBoard()

    # # Opening - Black makes territory in upper-left
    # b.playMove(0, 0, 1); next_turn()
    # b.playMove(5, 5, -1); next_turn()
    # b.playMove(0, 1, 1); next_turn()
    # b.playMove(5, 6, -1); next_turn()
    # b.playMove(1, 0, 1); next_turn()
    # b.playMove(6, 5, -1); next_turn()
    # b.playMove(1, 1, 1); next_turn()
    # b.playMove(6, 6, -1); next_turn()

    # # Black surrounds white stone
    # b.playMove(2, 1, 1); next_turn()
    # b.playMove(2, 2, -1); next_turn()
    # b.playMove(2, 0, 1); next_turn()
    # b.playMove(4, 4, -1); next_turn()
    # b.playMove(3, 1, 1); next_turn()
    # b.playMove(4, 5, -1); next_turn()
    # b.playMove(3, 0, 1); next_turn()
    # b.playMove(7, 7, -1); next_turn()

    # # Black finishes off white stone (dead)
    # b.playMove(3, 2, 1); next_turn()

    # # Some more moves
    # b.playMove(7, 6, -1); next_turn()
    # b.playMove(4, 0, 1); next_turn()
    # b.playMove(8, 8, -1); next_turn()
    # b.playMove(4, 1, 1); next_turn()

    # # Both players pass to end game
    # b.playMove(0, 0, -1, passTurn=True); next_turn()
    # b.playMove(0, 0, 1, passTurn=True); next_turn()

    # print("Final Board:")
    # b.printBoard()

    # print("Final Score:")
    # print(b.score())

    # b.playMove(0, 0, 1); next_turn()
   

    # print("Final Board:")
    # b.printBoard()

    # print("Final Score:")
    # print(b.score())

    print("\n--- Test 1: Two-Eye Alive Group (Black should live) ---")
    # Set up black group with two eyes ---------------------------------------------------------------------------------------

    # b.playMove(1, 1, 1); next_turn()
    # b.playMove(8, 8, -1); next_turn()
    # b.playMove(1, 2, 1); next_turn()
    # b.playMove(8, 7, -1); next_turn()
    # b.playMove(2, 1, 1); next_turn()
    # b.playMove(8, 6, -1); next_turn()
    # b.playMove(2, 3, 1); next_turn()
    # b.playMove(8, 5, -1); next_turn()
    # b.playMove(3, 2, 1); next_turn()
    # print("Final Score:", b.score())

    # Set up black group with two eyes ---------------------------------------------------------------------------------------



    # Testing dead stone in enemy territory  ---------------------------------------------------------------------------------------

    # print("\n--- Test 2: Dead White Stone in Enemy Territory ---")
    # b.playMove(0, 1, 1); next_turn()
    # b.playMove(4, 4, -1); next_turn()
    # b.playMove(1, 0, 1); next_turn()
    # b.playMove(4, 5, -1); next_turn()
    # b.playMove(1, 2, 1); next_turn()
    # b.playMove(4, 6, -1); next_turn()
    # b.playMove(2, 1, 1); next_turn()
    # b.playMove(4, 7, -1); next_turn()
    # b.playMove(1, 1, -1); next_turn()  # Surrounded white stone

    # print("Final Score:", b.score())

    # Testing dead stone in enemy territory  ---------------------------------------------------------------------------------------




    # Testing 2 eyes detection variant 2  ---------------------------------------------------------------------------------------


    print("--- Test 1: Two-Eye Alive Group (Black should live) ---")

    # Black builds a wall
    b.playMove(0, 1, 1); next_turn()
    b.playMove(8, 8, -1); next_turn() # Arbitrary move for white
    b.playMove(1, 0, 1); next_turn()
    b.playMove(8, 7, -1); next_turn()
    b.playMove(2, 0, 1); next_turn()
    b.playMove(8, 6, -1); next_turn()
    b.playMove(3, 1, 1); next_turn()
    b.playMove(8, 5, -1); next_turn()
    b.playMove(3, 3, 1); next_turn()
    b.playMove(8, 4, -1); next_turn()
    b.playMove(2, 4, 1); next_turn()
    b.playMove(8, 3, -1); next_turn()
    b.playMove(1, 4, 1); next_turn()
    b.playMove(8, 2, -1); next_turn()
    b.playMove(0, 3, 1); next_turn()
    b.playMove(8, 1, -1); next_turn()

    # Black secures the eyes internally
    b.playMove(1, 2, 1); next_turn()
    b.playMove(8, 0, -1); next_turn()
    b.playMove(2, 2, 1); next_turn()

    # Checking for dead stone detection in enemy territory.
    b.playMove(1, 1, -1); next_turn()

    
    print("Final Score:", b.score())

    # Testing 2 eyes detection variant 2  ---------------------------------------------------------------------------------------


    # Testing dead stone in enemy territory variant 2 -------------------------------------------------------------------------------

    print("--- Test 4: Complex Board with Dead Group ---")

    # Black builds a large structure
    b.playMove(3, 3, 1); next_turn()
    b.playMove(0, 0, -1); next_turn()
    b.playMove(3, 4, 1); next_turn()
    b.playMove(0, 1, -1); next_turn()
    b.playMove(3, 5, 1); next_turn()
    b.playMove(0, 2, -1); next_turn()
    b.playMove(4, 2, 1); next_turn()
    b.playMove(0, 3, -1); next_turn()
    b.playMove(5, 3, 1); next_turn()
    b.playMove(0, 4, -1); next_turn()
    b.playMove(5, 6, 1); next_turn()
    b.playMove(0, 5, -1); next_turn()
    b.playMove(4, 7, 1); next_turn()
    b.playMove(0, 6, -1); next_turn()
    b.playMove(3, 6, 1); next_turn()
    b.playMove(8, 8, -1); next_turn()

    # White tries to live inside
    b.playMove(2, 4, 1); next_turn()
    b.playMove(4, 4, -1); next_turn() # White's group starts
    b.playMove(6, 4, 1); next_turn()
    b.playMove(4, 5, -1); next_turn()
    b.playMove(4, 6, 1); next_turn()
    b.playMove(5, 5, -1); next_turn()
    b.playMove(5, 4, 1); next_turn()
    b.playMove(4, 3, -1); next_turn() # White has one eye at (4,4)


    print("Final Score:", b.score())

    # Testing dead stone in enemy territory variant 2 -------------------------------------------------------------------------------
