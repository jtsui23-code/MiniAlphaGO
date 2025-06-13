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

        # Normalize the output of self.convolutional1 
        # to have a mean of 0 
        # a standard deviation of 1
        self.batchNormalization1 = nn.BatchNorm2d(64)

        # Creating a list of Residual Blocks. nnModuleList is special list 
        # that notifies Pytorch these residual blocks are apart of GoNet.
        # Stacking the 4 Residual Blocks ontop of each other to process the 
        # board deeply.
        self.residualBlocks = nn.ModuleList([
            ResidualBlock(64) for _ in range(4)
        ])

        # Outputs the probabliy of each possible move on the board (81)
        # A 1x1 convolution reduces the 64 feature maps into just 2.
        self.policyHead = nn.Conv2d(64, 2, 1)

        self.policyHeadBatchNormalization = nn.BatchNorm2d(2)

        # There is a 2 in (2 * 9 * 9) because that is the size of 
        # the feature map from self.policyHead.
        # The 9 * 9 in (2 * 9 * 9) is the board size
        # This reduces the feature of 2 * 81 = 162 to 81 possible moves 
        # because that is the max number of possible moves on the 
        # board.
        self.policyFullyConnected = nn.Linear(2 * 9 * 9, 81)

        # Want an output of -1 to 1 to indicate which player is winning.
        # This is using Sequential object from Pytorch which is a in order 
        # container of neural network layers.
        self.valueHead = nn.Sequential(
            nn.Conv2d(64, 1, kernel_size=1),
            nn.BatchNorm2d(1),

            # Using nn.ReLU for improviing training speed and gradient flow
            # because it introduces complexity and makes non-linearity 
            # from the removal of negative values becoming zero.
            nn.ReLU(),

            # Makes 1x9x9 feature map into a vector size 81.
            nn.Flatten,

            # 81 is fixed because of nn.Conv2d(61,1, kernel_size-1)
            # while 64 is design choice giving an extra layer for 
            # additional thinking. Its power of 2.
            nn.Linear(1*9*9, 64),
            nn.ReLU(),

            # Makes the 64 features from nn.LInear(1*9*9, 64) into a 
            # scalar.
            nn.Linear(64,1),

            # Activation function that squishes the otuput to 
            # be in range of -1 to 1.
            nn.Tanh()

        )       

    def forward(self, x):

        # This is using the foward method of nn.Conv2d(17, 64, kernel_size=3, padding=1 )
        x = self.convolutional1(x)


        x = self.batchNormalization1(x)

        x = F.relu(x)

        # Takes the output and pass it to the residual blocks.
        for block in self.residualBlocks: x = block(x)

        # Take the output of the body and pass it to the policy head's layers.
        # This reduces the feature dept while retaining the spacial information
        # about move choices.
        p = self.policyHead(x)
        p = self.policyHeadBatchNormalization(x)
        p = F.relu(p)

        # .vew - reshapes tensors
        # Flattens the tensor to become a vector.
        # Flattens [B, 2, 9, 9] to [B, 162]
        # 162 is from 2 * 9 * 9
        p = p.view(p.size(0), -1 )

        # Get the final policy logits 
        policyLogits = self.policyFullyConnected(p)

        value = self.valueHead(x)

        # torch.squeeze(value, dim=-1) Removes redundant dimensions making the 
        # tensor easier to work with
        return policyLogits, torch.squeeze(value, dim=-1)

        



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


    """
    METHOD: __init__

    INPUT:
        channels (int): The number of inputs/outputs for the convolutional layers.

    RETURN:
        N/A

    DESCRIPTION:
        Constructor for the ResidualBlock class. Initializes two convolutional layers
        and two batch normalization layers. Both conv layers maintain the same number
        of channels (no dimension change) and use 3x3 kernels with padding=1 to 
        preserve spatial dimensions. Each conv layer has a corresponding batch 
        normalization layer to stabilize training.
    """
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


    """
    METHOD: forward

    INPUT:
        x (torch.Tensor): Input tensor with shape [batch_size, channels, height, width].
                          This is the feature map from the previous layer.

    RETURN:
        torch.Tensor: Output tensor with same shape as input. Contains the result
                      of the residual computation: F(x) + x, where F(x) is the 
                      transformation learned by the two convolutional layers.

    DESCRIPTION:
        Performs the forward pass of the residual block. Applies two convolutional
        layers with batch normalization and ReLU activation, then adds the original
        input (skip connection) to create the residual connection. This allows the
        network to learn identity mappings and helps with gradient flow in deep networks.
        The sequence is: conv1->batchnorm1->relu->conv2->batchnorm2->add_residual->relu.
    """
    def forward(self, x):

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