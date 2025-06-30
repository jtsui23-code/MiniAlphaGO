from model.net import GoNet
import os
from training.evaluation import evalateModel
from training.train import createModel
from training.selfPlay import playOneGame
from training.replayBuffer import ReplayBuffer
import torch
import re # For pattern recognition in strings




"""
METHOD: startPipline
INPUT:
    numGames (int)      :  How many new games you want to add to the self-play game data set.
    genNum   (int)      :  Generation number so older best models are not overrided for having varying bot difficulties. 

RETURN:
    N/A
DESCRIPTION:
    This function generates more self-play game data that is used by the new model along with the original data set.
    The new model is then evaluated to see if its the new best model.
    
"""
def startPipline(numGames=50, genNum=2):
    print("Entered function")
    # Gets all of the self-play game files and appends them into an array. 
    # This is to prevent override when saving replay buffer and correctly naming the replay buffer as well.
    existingBufferfiles = [f for f in os.listdir("selfPlay") if f.startswith("selfPlayBuffer_") and f.endswith(".pkl")]

    # int(f.split("_")[1] 
    # splits the name of the self-play files from 
    # ["selfPlayerBuffer_200.pkl"] -> ["selfPlayerBuffer_", "200.pkl"]
    # The [1] in int(f.split("_")[1] selects "200.pkl" in ["selfPlayerBuffer_", "200.pkl"]
    # because that the part of the string we care about the file number.
    # Then .split(".")[0] 
    # splits ["200.pkl"] -> ["200", ".pkl"]
    # and [0] in .split(".")[0] selects first element because that is the number
    # and all of this is within an int() converting the string to an integer.
    # This is applied to all of the existing buffer files in selfPlay/
    bufferNumber = [int(f.split("_")[1].split(".")[0]) for f in existingBufferfiles]
    highestBufferNumber = max(bufferNumber, default=0)
    print("Passed the buffer counting")


    # Loading the current best model.
    currentModel = GoNet(boardSize=9, channels=17)
    currentModel.load_state_dict(torch.load(f"models/bestModel{genNum-1}.pt"))

    currentModel.eval()

    # Creating buffer object to save self-play games.
    buffer = ReplayBuffer(capacity=1000)


    print("Creating components")

    numGames = numGames
    saveInterval = 10

    print("Right before the for loop")


    # Playing a set amount of self-play games and saving them.
    for i in range(1, numGames + 1):
        print(f"-------------------------------------------- Generating self-play game data --------------------------------------------")
        playOneGame(buffer=buffer, network=currentModel, mctSimulations=200, gameNumber=i)

        if i % saveInterval == 0:
            buffer.saveToFile(f"selfPlay/selfPlayBuffer_{i + highestBufferNumber}.pkl")
        



    # numTrainData = len(existingBufferfiles)
    # numBuffers = numTrainData + numGames/10
    numtTrainData = [f for f in os.listdir("selfPlay") if f.startswith("selfPlayBuffer_") and f.endswith(".pkl")]
    numBuffers = len(numtTrainData)

    createModel(numTrainData=int(numBuffers), fileName="candidateModel.pt")


    # Creating candiateModel that uses the newly self-play games as well as the orignal data set.
    candidateModel = GoNet(boardSize=9, channels=17)
    candidateModel.load_state_dict(torch.load("models/candidateModel.pt"))
    candidateModel.eval()

    print(f"-------------------------------------------- Evaluating the new model --------------------------------------------")

    # Evaluating whether the new model is better than the current one or not.
    return evalateModel(candiateModel=candidateModel, championModel=currentModel, numGames=50, genNum=genNum)


def extractFileNum(fileName):

    # r"" is a raw string
    # (\d+)\ is the number we want in the file that starts with selfPlayBuffer_ and ends with .pkl
    match = re.search(r"selfPlayBuffer_(\d+)\.pkl", fileName)

    # match.group(1) would be the file number so if fileName is selfPlayBuffer_510.pkl
    # match.group(1) is 510
    return int(match.group(1)) if match else -1



"""
METHOD: evaludateModel
INPUT:
    genNum   (int)      :  Generation number so older best models are not overrided for having varying bot difficulties. 

RETURN:
    N/A
DESCRIPTION:
    This function evaluates the candidate model compared to the current best model its purpose is to be used separately 
    whenever the pipline cannot be fully ran because of time contraint.
    
"""
def evaludateModel(genNum=3):

    # Loading the current best model.
    currentModel = GoNet(boardSize=9, channels=17)
    currentModel.load_state_dict(torch.load(f"models/bestModel{genNum-1}.pt"))

    currentModel.eval()


    # numTrainData = len(existingBufferfiles)
    # numBuffers = numTrainData + numGames/10
    allDataFiles = [f for f in os.listdir("selfPlay") if f.startswith("selfPlayBuffer_") and f.endswith(".pkl")]

    # key=extractFileNum means each file name in allDataFiels will be passed into extractFileNum function.
    sortedFiles = sorted(allDataFiles, key=extractFileNum)
    
    latestFiles = sortedFiles[-50]

    createModel(numTrainData=latestFiles, fileName="candidateModel.pt")


    # Creating candiateModel that uses the newly self-play games as well as the orignal data set.
    candidateModel = GoNet(boardSize=9, channels=17)
    candidateModel.load_state_dict(torch.load("models/candidateModel.pt"))
    candidateModel.eval()
    evalateModel(candiateModel=candidateModel, championModel=currentModel, numGames=50, genNum=genNum)

counter = 5
while counter < 11:

    evalResult = startPipline(numGames=100, genNum=counter)
    if evalResult == 1:
        counter+= 1

# evaludateModel(genNum=4)




