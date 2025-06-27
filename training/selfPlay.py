from board.go import Board  
from model.net import GoNet
from model.mcts import MCTS
from training.replayBuffer import ReplayBuffer
from utils.boardToTensor import boardToTensor  



"""
METHOD: modelTesting
INPUT:
    blackModel (GoNet)      :  The model that is playing black this game.
    whiteModel (GoNet)      :  The model that is playing white this game.

RETURN:
    score (int)             : Returns 1 if black wins or -1 if white wins.
DESCRIPTION:
    This function has two different models play a game of against each other to 
    see who wins this match. This is used in evalateModel.py to see if a candidate model
    is the new best one.
    
"""
def modelTesting(blackModel, whiteModel):

    # Creating board, model, and mct.
    board = Board(9)
    model = None
    mct = None

    # Have a turn cap of 125 to end the game.
    count = 0
    max = 125

    while not board.isGameOver() and count < max:

        # Loads the model in respect to whose turn it is.
        if board.currentPlayer == 1:
            model = blackModel

        elif board.currentPlayer == -1:
            model = whiteModel

        # Loads the specific model into mct depending on whose turn it is.
        mct = MCTS(network=model, simulations=200)

        # Plays move using the specific model according to player's turn.
        move, pi = mct.search(board)

        x,y = divmod(move, 9)
        board.playMove(x,y, board.currentPlayer)
        

        count += 1
    
    
    # Gets the score of the game to see who won.
    score = board.score()

    return score
            


"""
METHOD: playOneGame
INPUT:
    buffer (ReplayBuffer):  Object of ReplayBuffer for saving the self-play data.
    network (GoNet)      :  Object of GoNet for play go with mct.
    mctSimulations       :  Number of simulated games by the mct.

RETURN:
    N/A
DESCRIPTION:
    This function utilizes the Go network and mct to play a single game of Go and saves the 
    result of the game for training the network.
    
"""
def playOneGame(buffer, network, mctSimulations=100, gameNumber=0):

    # Creating Board and mct
    board = Board(9)

    mct = MCTS(network=network, simulations=mctSimulations)

    print("✅ Created the components")

    # Have a counter as a hard cap so the game doesn't loop forever.
    max = 125
    count = 0

    # gameData is the data saved throughout a single game not all of them.
    gameData = [] # Stores tuple of (state, pi, z) pi - vector of probability of all moves, 
                #                                z  - tracks all of the moves made by the winner as a +1 and -1 for 
                #                                     all the moves by the loser.

    while count < max + 1:
        print("--------------- Current Game is ", gameNumber, "----------------")

        print(f"The current player is " , {board.currentPlayer})
        print("------------------------------------------------------------------------------------")
        board.printBoard()
        print("------------------------------------------------------------------------------------")

        # Gets the best move and the pi vector which is the probability of all the moves.
        move, pi = mct.search(board)

        # Converts the board into a tensor which is the expected form for saving the gameData.
        boardState = boardToTensor(board)

        # 0 - 80 are the only valid moves on a 9x9 board. Move 81 is set to being a pass.
        if move is None or move == 81:
            print("AI passed")
            # Player passes if that is the move choosen by the mct.
            board.playMove(1,1, board.currentPlayer, passTurn=True)
        else:
            # Converting move which is a single int representation of the board position into 
            # a row and col representation of the 9x9 board.
            x, y = divmod(move, 9)
            
            # Playing the move choosen by the mct.
            board.playMove(x,y, board.currentPlayer)

            print(f"Player played at ", {x}, {y}, " position on the board")


        # Saves the game data each turn. 
        gameData.append((boardState, pi, board.currentPlayer))
        mct.update_root(move)
        count = count + 1


    print(board.score())
    print("------------------------------------------------------------------------------------\n Game Over ------------------------------------------------------------------------------------")

    # .score() returns 1 or -1 to indicate winner.
    winner = board.score()

    # Loops through each turn to see which moves where good and bad. T
    # This is done through see which moves where done by the winner and the loser.
    for state, pi, player in gameData:
        z = 1 if player == winner == 1 else -1
        buffer.add(state, pi, z)



if __name__ == "__main__":

    buffer = ReplayBuffer(capacity=10000)
    network = GoNet(9, 17)
    network.eval()

    numberOfGames = 150
    saveInterval = 10

    for i in range(1, numberOfGames + 1):
        print("------------------------- Starting Game ", i , "-------------------------")
        playOneGame(buffer=buffer, network=network, gameNumber=i)

        if i % saveInterval == 0:
            buffer.saveToFile(f"selfPlay/selfPlayBuffer_{i + 350}.pkl")
            print(f"Saved replay buffer after {i} games.")





