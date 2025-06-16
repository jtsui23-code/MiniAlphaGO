from board.go import Board  
from model.net import GoNet
from model.mcts import MCTS
from training.replayBuffer import ReplayBuffer
from utils.boardToTensor import boardToTensor  


print("✅ main.py is running")

board = Board(9)
network = GoNet(9, 17)

network.eval()
mct = MCTS(network=network, simulations=100)

print("✅ Created the components")

max = 125
count = 0

buffer = ReplayBuffer(capacity=1000)
gameData = [] # Stores tuple of (state, pi, z) pi - vector of probability of all moves, 
              #                                z  - tracks all of the moves made by the winner as a +1 and -1 for 
              #                                     all the moves by the loser.

while count < max + 1:
    print("✅ Reached inside game loop")

    print(f"The current player is " , {board.currentPlayer})
    print("------------------------------------------------------------------------------------")
    board.printBoard()
    print("------------------------------------------------------------------------------------")

    move, pi = mct.search(board)
    boardState = boardToTensor(board)

    # 0 - 80 are the only valid moves on a 9x9 board. Move 81 is set to being a pass.
    if move is None or move == 81:
        print("AI passed")
        board.playMove(1,1, board.currentPlayer, passTurn=True)
    else:
        # Converting move which is a single int representation of the board position into 
        # a row and col representation of the 9x9 board.
        x, y = divmod(move, 9)
        board.playMove(x,y, board.currentPlayer)

        print(f"Player played at ", {x}, {y}, " position on the board")


    gameData.append((boardState, pi, board.currentPlayer))
    mct.update_root(move)
    count = count + 1


print(board.score())
print("------------------------------------------------------------------------------------\n Game Over ------------------------------------------------------------------------------------")

# .score() returns 1 or -1 to indicate winner.
winner = board.score()
for state, pi, player in gameData:
    z = 1 if player == winner == 1 else -1
    buffer.add(state, pi, z)

buffer.saveToFile("selfPlay/selfPlayBuffer1.pk1")

