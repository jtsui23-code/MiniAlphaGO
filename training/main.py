from board.go import Board  # adjust path if needed
from model.net import GoNet
from model.mcts import MCTS


board = Board(9)
network = GoNet(9, 17)

network.eval()
mct = MCTS(network=network, simulations=800)


while not board.isGameOver:
    print(f"The current player is " , {board.currentPlayer})
    print("------------------------------------------------------------------------------------")
    board.printBoard()
    print("------------------------------------------------------------------------------------")

    move = mct.search(board)

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

    mct.update_root(move)



