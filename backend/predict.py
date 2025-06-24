import torch
from model.net import GoNet
from utils import boardToTensor


# Leaving the loading of the model outside fo the function because this will only 
# be called once when backend/predict.py is imported into backend/main.py which saves 
# memory and is more efficient than having this inside of the getBestMove() function.
model = GoNet(boardSize=9, channels=17)

# map_location=torch.device('cpu') allows the model that was trained on the GPU to be ran on CPU
# which is useful for laptops without GPU or running the model on a server.
model.load_state_dict(torch.load(f"models/bestModel{2}.pt", map_location=torch.device('cpu')))

# Switches the network from training mode to inference mode.
model.eval()


"""
METHOD: getBestMove
INPUT:
    boardState (Board)      :  Current board state that is passed in for the model to predict the best mvove.

RETURN:
    tuple: x, y position on the board for the model's prediction on the best move.

DESCRIPTION:
    This function evaulates the candiate model to see if its maybe the new best model and if it is then 
    the model is saved.
    
"""
def getBestMove(boardState):

    # Converting the current board state into a tensor which the network can handle.
    boardTensor = boardToTensor(boardState)

    
    # Stops calculating the gradient during prediction normaly does during training. 
    # This is because its faster, saves memory and safer to perform predictions without calculating 
    # gradients.
    with torch.no_grad():

        # Using the foward method in the GoNet to get the policy value which has the probablities of all of the possible
        # moves on the board.
        # using , _ because do not need the 'value' 
        policy, _ = model(boardTensor)

        # This finds the move on the board with the highest probablity and sets that as the best move.
        bestMove  = torch.argmax(policy).item()
        x,y = divmod(bestMove, 9)
        
    return x,y



