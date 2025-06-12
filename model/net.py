import torch 
import torch.nn as nn
import torch.nn.functional as F

class GoNet(nn.Module):

    def __init__(self, boardSize=9, channels=17):
        super(GoNet, self).__init__()

        self.boardSize = boardSize

        # Number of input channels (17 is standard for Go)
        # - 8 channels for recent board positions
        # - 8 channels for opponent's recent positions  
        # - 1 channel for whose turn it is
        self.numChannels = channels

        # self.conv1 is a 2D convolutional layer useful for images and board games.
        # input channels  -  17
        # output channels -  64
        # kernel size     -  3 (Looks at 3x3 of the board at a time)
        # padding         -  1 (Maintains the board size of 9)
        self.convolutional1 = nn.Conv2d(self.numChannels, 64, kernel_size=3, padding=1)

        self.residualBlocks = nn.ModuleList([
            ResidualBlock(64) for _ in range(4)
        ])


"""
CLASS: ResidualBlock

ATTRIBUTES:
    torch.nn.modules.conv.Conv2d self.convulotional1:                   The first Convulotional layer with 64 channels by default
    torch.nn.modules.batchnorm.BatchNorm2d self.batchNormalization1     The first batch normalization used for the first convulotional layer

    torch.nn.modules.conv.Conv2d self.convulotional2:                   The second convulotional layer iwth 64 channels by default
    torch.nn.modules.batchnorm.BatchNorm2d self.batchNormalization2     The second batch normalization used for the second convulotional layer

METHODS:
    __init__(channels):             Constructor to initialize the Residual Block.
    foward(x):                      Overide method of nn.Module's foward method.
    


PACKAGES:
    import torch 
    import torch.nn as nn
    import torch.nn.functional as F

DESCRIPTION:
    The ResidualBlock class helps the GoNet class in learning deeper patterns. Through using
    skip connection, the ResidualBlock class prevents the vanishing gradient problem in the 
    GoNet class helping it train deeper networks.
    
"""
class ResidualBlock(nn.Module):

    def __init__(self, channels):
        super(ResidualBlock, self). __init__()

        # Creating convolutional layer
        self.convolutional1 = nn.Conv2d(channels, channels, kernel_size=3, padding=1)
        
        # Normalize the output of the self.convolutional1 to scale to have
        # mean - 0
        # standard deviation - 1
        self.batchNormalization1 = nn.BatchNorm2d(channels)


        # Second convolution layer
        self.convolutional2 = nn.Conv2d(channels, channels, kernel_size=3, padding=1)

        self.batchNormalization2 = nn.BatchNorm2d(channels)

    def foward(self, x):

        # residual is the original input which is saved.
        residual = x

        # First Convolutional layer 
        # You are using x because residual is saved input that should't be altered.
        # Meaning the first convolutional layer process the input data so you have 
        # to save the original input before it gets processed.
        output = F.relu(self.batchNormalization1(self.convolutional1(x)))

        # Uses 2nd Convolutional layer using the first layer's output as its input
        ouptut = self.batchNormalization2(self.convolutional2(output))

        # Need to account for the original input (residual) 
        # Cannot perform F.relu(output) first because you 
        # lose information since F.relu(output) removes negatives values 
        ouptut += residual

        output = F.relu(output)

        return output