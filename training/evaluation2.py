from model.net import GoNet
from training.selfPlay2 import modelTesting
from training.train2 import createModel
import torch




"""
METHOD: evaluateModel
INPUT:
    candiateModel (GoNet)      :  The model that is being checked if it might be the best.
    championModel (GoNet)      :  The model that is the current best.
    numGames (int)             :  Number of evaluation games.
    genNum (int)               :  The generation number of the next model.
    device                     :  Determines which device the evaluation games are ran.

RETURN:
    N/A

DESCRIPTION:
    This function evaulates the candiate model to see if its maybe the new best model and if it is then 
    the model is saved.
    
"""
def evaluateModel(candidateModel, championModel, numGames=20, genNum=2, device=torch.device("cpu")):


    candidateModel .to(device)
    championModel.to(device)

    candidateModel .eval()
    championModel.eval()
    
    # Counter of all of the wins by the candiateModel.
    wins = 0
    
    # Have the 2 models compete a set number of games.
    for i in range(numGames):
        
        # Each model plays as black one after the other because playing as black gives the player/model an 
        # inherit advantage.
        if i % 2 == 0:
            
            # The championModel gets the play as black this game.
            winner = modelTesting(blackModel=championModel, whiteModel=candidateModel, device=device, dirichletAlpha=0.0,
                dirichletEpsilon=0.0, temperature=0.1, mctSim=400, explore=1.5) 

            # Checking if the winner was the candiateModel if so then increment wins.
            if winner == -1:
                wins += 1

        else:
            # The candiateModel gets the play as black this game.
            winner = modelTesting(blackModel=candidateModel, whiteModel=championModel, device=device,
                            dirichletAlpha=0.3,dirichletEpsilon=0.25, temperature=1.0, mctSim=400, explore=1.5)

            # Checking if the winner was the candiateModel if so then increment wins.
            if winner == 1:
                wins += 1

        print(f"Game {i+1}/{numGames} winner is {winner}") 

    # Calculates the win rate of the candiateModel
    # if the win rate is above 55% then the candiateModel is the new best model.
    winRate = (wins/numGames)
    print(f"Candiate model has a win rate of {winRate*100}%")

    if winRate > 0.55:
        torch.save(candidateModel.state_dict(), f"models/bestModel{genNum}.pt")
        return 1
    else:
        print("Candiate rejected")
        return -1


if __name__ == "__main__":

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Loading the both the champion and candiate model to the network to be used in the 
    # evaulation.
    currentModel = GoNet(boardSize=9, channels=17).to(device)
    candidateModel = GoNet(boardSize=9, channels=17).to(device)

    # currentModel.load_state_dict(torch.load("models/currentModel.pt"))

    currentModel.load_state_dict(torch.load("models/bestModel.pt", map_location=device))
    candidateModel.load_state_dict(torch.load("models/candidateModel.pt", map_location=device))

    currentModel.eval()
    candidateModel.eval()
    evaluateModel(candiateModel=candidateModel, championModel=currentModel, device=device)

    # Creating the new candiateModel
    # The 7th save file was rejected i.e numTrainData=8

    createModel(numTrainData=51,fileName="candidateModel")





