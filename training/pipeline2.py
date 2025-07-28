from model.net import GoNet
import os
from training.evaluation2 import evalateModel
from training.train2 import createModel
from training.selfPlay2 import playOneGame
from training.replayBuffer2 import ReplayBuffer
import torch
import re # For pattern recognition in strings

# Detects GPU is possible
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")


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
def startPipline(numGames=50, genNum=2, mct=100):
    # print("Entered function")
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
    # print("Passed the buffer counting")


    # Loading the current best model.
    currentModel = GoNet(boardSize=9, channels=17)
    currentModel.load_state_dict(torch.load(f"models/bestModel{genNum-1}.pt", map_location=device))

    currentModel.to(device)
    currentModel.eval()

    # Creating buffer object to save self-play games.
    buffer = ReplayBuffer(capacity=1000)


    # print("Creating components")

    numGames = numGames
    saveInterval = 10

    # print("Right before the for loop")


    # Playing a set amount of self-play games and saving them.
    for i in range(1, numGames + 1):
        # print(f"-------------------------------------------- Generating self-play game data --------------------------------------------")
        playOneGame(buffer=buffer, network=currentModel, mctSimulations=mct, gameNumber=i, device=device)

        if i % saveInterval == 0:
            buffer.saveToFile(f"selfPlay/selfPlayBuffer_{i + highestBufferNumber}.pkl")
            print(f"Finished {i}th batch of games")
        


    # numTrainData = len(existingBufferfiles)
    # numBuffers = numTrainData + numGames/10
    allDataFiles = [f for f in os.listdir("selfPlay") if f.startswith("selfPlayBuffer_") and f.endswith(".pkl")]

    # key=extractFileNum means each file name in allDataFiels will be passed into extractFileNum function.
    sortedFiles = sorted(allDataFiles, key=extractFileNum)
    
    latestFiles = sortedFiles[-100:]

    createModel(fileLIst=latestFiles, fileName="candidateModel.pt", device=device)



    # Using GPU instead of CPU for pipline for faster runtime.
    # device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    

    # Creating candiateModel that uses the newly self-play games as well as the orignal data set.
    candidateModel = GoNet(boardSize=9, channels=17)
    candidateModel.load_state_dict(torch.load("models/candidateModel.pt", map_location=device))
    candidateModel.to(device)
    candidateModel.eval()

    print(f"-------------------------------------------- Evaluating the new model --------------------------------------------")

    # Evaluating whether the new model is better than the current one or not.
    return evalateModel(candiateModel=candidateModel, championModel=currentModel, numGames=50, genNum=genNum, device=device)


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
    
    latestFiles = sortedFiles[-100:]

    createModel(fileLIst=latestFiles, fileName="candidateModel.pt", device=device)


    # Creating candiateModel that uses the newly self-play games as well as the orignal data set.
    candidateModel = GoNet(boardSize=9, channels=17)
    candidateModel.load_state_dict(torch.load("models/candidateModel.pt"))
    candidateModel.eval()
    evalateModel(candiateModel=candidateModel, championModel=currentModel, numGames=50, genNum=genNum, device=device)


"""
METHOD: freshStart
INPUT:
    N/A

RETURN:
    N/A

DESCRIPTION:
    This function creates a model from scratch without any previous training data.
    
"""
def freshStart(mct=0, games=500):
    # Create initial random model
    initial_model = GoNet(boardSize=9, channels=17)
    torch.save(initial_model.state_dict(), "models/bestModel0.pt")

    allDataFiles = [f for f in os.listdir("selfPlay") if f.startswith("selfPlayBuffer_") and f.endswith(".pkl")]
    # print(len(allDataFiles))

    # Generate initial self-play data with random model
    buffer = ReplayBuffer(capacity=1000)
    for i in range(1, games + 1):  # Generate some initial games

        fileNum = i + (len(allDataFiles) * 10)
        playOneGame(buffer=buffer, network=initial_model, mctSimulations=mct, gameNumber=i, device=device)
        if i % 10 == 0:
            buffer.saveToFile(f"selfPlay/selfPlayBuffer_{fileNum}.pkl")
            print(f"Finished {i}th batch of games")



gen = 1
count = 0

freshStart(mct=300, games=1000)
freshStart(mct=800, games=200)



while count < 2000:
    mct = 300


    numGames = 1000

    if count == 0:
        mct = 100

    freshStart(mct=mct, games=numGames)

    mct = 300

    evalResult = startPipline(numGames=numGames, genNum=gen, mct=mct)
    
    if evalResult == 1:
        gen += 1



# while counter < 2000:

#     evalResult = startPipline(numGames=100, genNum=counter)
#     if evalResult == 1:
#         counter+= 1











