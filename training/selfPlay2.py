from board.go import Board  
from model.net import GoNet
from model.mct5 import MCTS
from training.replayBuffer2 import ReplayBuffer
from utils.boardToTensor import boardToTensor  
import torch
from utils.symmetries import generateSymmetries

# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")



"""
METHOD: modelTesting
INPUT:
    blackModel (GoNet)      :  The model that is playing black this game.
    whiteModel (GoNet)      :  The model that is playing white this game.
    device                  :  The device which the model testing is being done on.
RETURN:
    score (int)             : Returns 1 if black wins or -1 if white wins.
DESCRIPTION:
    This function has two different models play a game of against each other to 
    see who wins this match. This is used in evalateModel.py to see if a candidate model
    is the new best one.
    
"""
def modelTesting(blackModel, whiteModel, device=torch.device("cpu"),dirichletAlpha=0.3,
                dirichletEpsilon=0.25, temperature=1.0, mct=400, explore=1.5):

    # Creating board, model, and mct.
    board = Board(9)
    model = None
    mct = None

    # Have a turn cap of 125 to end the game.
    count = 0
    max = 100
    hardCap = False

    # Include max move count of 300 as an 
    # alternative to end games for evaluation games. 
    # For self-play game generation just use double pass 
    # for end game condition.
    while not board.isGameOver():
        if count >= max:
            hardCap = True
            break

    # while not board.isGameOver():

        # Loads the model in respect to whose turn it is.
        if board.currentPlayer == 1:
            model = blackModel

        elif board.currentPlayer == -1:
            model = whiteModel

        # Loads the specific model into mct depending on whose turn it is.
        mct = MCTS(network=model, simulations=mct, dirichlet_alpha=dirichletAlpha, 
               dirichlet_epsilon=dirichletEpsilon, temperature=temperature, exploration_weight=explore)

        # Plays move using the specific model according to player's turn.
        move, pi = mct.search(board)

        if move is not None:
            x,y = divmod(move, 9)
            board.playMove(x,y, board.currentPlayer)

        else:
            board.playMove(1,1, board.currentPlayer, passTurn=True)

        
        count += 1
    
    
    # Gets the score of the game to see who won.
    score = board.score(hardCap=hardCap)

    return score
            


"""
METHOD: playOneGame
INPUT:
    buffer (ReplayBuffer):  Object of ReplayBuffer for saving the self-play data.
    network (GoNet)      :  Object of GoNet for play go with mct.
    mctSimulations       :  Number of simulated games by the mct.
    device                  :  The device which the model game is being played on.


RETURN:
    N/A
DESCRIPTION:
    This function utilizes the Go network and mct to play a single game of Go and saves the 
    result of the game for training the network.
    
"""
def playOneGame(buffer, network, mctSimulations=100, gameNumber=0, device=torch.device("cpu"), dirichletAlpha=0.3,
                dirichletEpsilon=0.25, temperature=1.0, explore=1.5):

    # Creating Board and mct
    board = Board(9)

    mct = MCTS(network=network, simulations=mctSimulations, dirichlet_alpha=dirichletAlpha, 
               dirichlet_epsilon=dirichletEpsilon, temperature=temperature, exploration_weight=explore)

    # print("✅ Created the components")

    # Have a counter as a hard cap so the game doesn't loop forever.
    max = 100
    count = 0
    hardCap = False

    # gameData is the data saved throughout a single game not all of them.
    gameData = [] # Stores tuple of (state, pi, z) pi - vector of probability of all moves, 
                #                                z  - tracks all of the moves made by the winner as a +1 and -1 for 
                #                                     all the moves by the loser.

    while not board.isGameOver():
        if count >= max:
            hardCap = True
            break
        # print("Current Game is ", gameNumber, "")

        # print(f"The current player is " , {board.currentPlayer})
        # print("------------------------------------------------------------------------------------")
        # board.printBoard()
        # print("------------------------------------------------------------------------------------")

        # Gets the best move and the pi vector which is the probability of all the moves.
        move, pi = mct.search(board)

        # Converts the board into a tensor which is the expected form for saving the gameData.
        # boardState = boardToTensor(board).to(device)

        boardState = boardToTensor(board).to(device)

        # 0 - 80 are the only valid moves on a 9x9 board. Move 81 is set to being a pass.
        if move is None or move == 81:
            # print("AI passed")
            # Player passes if that is the move choosen by the mct.
            board.playMove(1,1, board.currentPlayer, passTurn=True)
        else:
            # Converting move which is a single int representation of the board position into 
            # a row and col representation of the 9x9 board.
            x, y = divmod(move, 9)
            
            # Playing the move choosen by the mct.
            board.playMove(x,y, board.currentPlayer)

            # print(f"Player played at ", {x}, {y}, " position on the board")


        # Saves the game data each turn. 
        gameData.append((boardState, pi, board.currentPlayer))
        mct.update_root(move)
        count = count + 1


    # print(board.score())
    # print("------------------------------------------------------------------------------------\n Game Over ------------------------------------------------------------------------------------")

    # .score() returns 1 or -1 to indicate winner.
    winner = board.score(hardCap=hardCap)

    # Loops through each turn to see which moves where good and bad. T
    # This is done through see which moves where done by the winner and the loser.
    for state, pi, player in gameData:
        z = 1 if player == winner == 1 else -1


        # Generate symmetries of the current board state and pi vector to 
        # take advantage of the fact that the go board has dihedral symmetry.
        boardSymmetries, piSymmetries = generateSymmetries(state, pi)

        for b, p in zip(boardSymmetries, piSymmetries):
            buffer.add(b, p, z)



# if __name__ == "__main__":


#     device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#     print(f"Running on {device}")


#     buffer = ReplayBuffer(capacity=10000)
#     # network = GoNet(9, 17).to(device)

#     network = GoNet(9, 17).to(device)
    
#     network.eval()

#     numberOfGames = 150
#     saveInterval = 10

#     for i in range(1, numberOfGames + 1):
# #         print("------------------------- Starting Game ", i , "-------------------------")
#         playOneGame(buffer=buffer, network=network, gameNumber=i)

#         if i % saveInterval == 0:
#             buffer.saveToFile(f"selfPlay/selfPlayBuffer_{i + 350}.pkl")
#             print(f"Saved replay buffer after {i} games.")





