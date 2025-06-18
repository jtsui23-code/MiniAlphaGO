from model.net import GoNet
from training.selfPlay import modelTesting
from training.train import createModel
import torch






"""
METHOD: evalateModel
INPUT:
    candiateModel (GoNet)      :  The model that is being checked if it might be the best.
    championModel (GoNet)      :  The model that is the current best.

RETURN:
    N/A

DESCRIPTION:
    This function evaulates the candiate model to see if its maybe the new best model and if it is then 
    the model is saved.
    
"""
def evalateModel(candiateModel, championModel, numGames=20):

    # Counter of all of the wins by the candiateModel.
    wins = 0
    
    # Have the 2 models compete a set number of games.
    for i in range(numGames):
        
        # Each model plays as black one after the other because playing as black gives the player/model an 
        # inherit advantage.
        if i % 2 == 0:
            
            # The championModel gets the play as black this game.
            winner = modelTesting(blackModel=championModel, whiteModel=candiateModel) 

            # Checking if the winner was the candiateModel if so then increment wins.
            if winner == -1:
                wins += 1

        else:
            # The candiateModel gets the play as black this game.
            winner = modelTesting(blackModel=candiateModel, whiteModel=championModel)

            # Checking if the winner was the candiateModel if so then increment wins.
            if winner == 1:
                wins += 1

        print(f"Game {i+1}/{numGames} winner is {winner}") 

    # Calculates the win rate of the candiateModel
    # if the win rate is above 55% then the candiateModel is the new best model.
    winRate = (wins/numGames)
    print(f"Candiate model has a win rate of {winRate*100}%")

    if winRate > 0.55:
        torch.save(candiateModel.state_dict(), "models/bestModel2.pt")
    else:
        print("Candiate rejected")


if __name__ == "__main__":
    # Loading the both the champion and candiate model to the network to be used in the 
    # evaulation.
    currentModel = GoNet(boardSize=9, channels=17)
    candidateModel = GoNet(boardSize=9, channels=17)

    # currentModel.load_state_dict(torch.load("models/currentModel.pt"))

    currentModel.load_state_dict(torch.load("models/bestModel.pt"))
    candidateModel.load_state_dict(torch.load("models/candidateModel.pt"))

    currentModel.eval()
    candidateModel.eval()
    evalateModel(candiateModel=candidateModel, championModel=currentModel)

    # Creating the new candiateModel
    # The 7th save file was rejected i.e numTrainData=8

    createModel(numTrainData=51,fileName="candidateModel")





