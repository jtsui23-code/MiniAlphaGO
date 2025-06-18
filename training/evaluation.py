from model.net import GoNet
from training.selfPlay import modelTesting
import torch

currentNetwork = GoNet(boardSize=9, channels=17)
candidateModel = GoNet(boardSize=9, channels=17)

currentNetwork.load_state_dict(torch.load("models/currentModel.pt"))
candidateModel.load_state_dict(torch.load("models/candidateModel.pt"))

currentNetwork.eval()
candidateModel.eval()

def evaulateModel(candiateModel, championModel, numGames=20):

    wins = 0

    for i in range(numGames):

        if i % 2 == 0:
            winner = modelTesting(blackModel=championModel, whiteModel=candiateModel) 
            if winner == -1:
                wins += 1

        elif i % 2 != 0:
            winner = modelTesting(blackModel=candiateModel, whiteModel=championModel)
            if winner == 1:
                wins += 1

        print(f"Game {i+1}/{numGames} winner is {winner}") 

    winRate = (wins/numGames)
    print(f"Candiate model has a win rate of {winRate*100}%")

    if winRate > 0.55:
        torch.save(candiateModel.state_dict(), "models/bestModel.pt")
    else:
        print("Candiate rejected")

evaulateModel(candiateModel=candidateModel, championModel=currentNetwork)



