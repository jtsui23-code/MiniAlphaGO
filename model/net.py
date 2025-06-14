import torch 
import torch.nn as nn
import torch.nn.functional as F

"""
CLASS: GoNet

ATTRIBUTES:
    int self.boardSize:                                                Size of the Go board (default 9x9), determines spatial dimensions
    int self.numChannels:                                              Number of input channels (default 17) for board state representation
    
    torch.nn.modules.conv.Conv2d self.convolutional1:                  Initial convolutional layer expanding from input channels to 64 features
    torch.nn.modules.batchnorm.BatchNorm2d self.batchNormalization1:   Batch normalization for initial convolutional layer output
    
    torch.nn.modules.container.ModuleList self.residualBlocks:         List of 4 ResidualBlock instances for deep feature extraction
    
    torch.nn.modules.conv.Conv2d self.policyHead:                      Policy head convolutional layer reducing 64 channels to 2
    torch.nn.modules.batchnorm.BatchNorm2d self.policyHeadBatchNormalization: Batch normalization for policy head features
    torch.nn.modules.linear.Linear self.policyFullyConnected:          Fully connected layer mapping flattened features to move logits (81 outputs)
    
    torch.nn.modules.container.Sequential self.valueHead:             Sequential container for value head layers producing position evaluation

METHODS:
    __init__(boardSize, channels):     Constructor to initialize the GoNet neural network architecture.
    forward(x):                        Override method of nn.Module's forward method for inference and training.

PACKAGES:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F

DESCRIPTION:
    The GoNet class implements a neural network architecture designed for playing the game of Go,
    following principles similar to AlphaZero. The network uses a shared convolutional trunk with
    residual connections that feeds into two specialized heads: a policy head for move prediction
    and a value head for position evaluation.
    
    The architecture consists of:
    1. Initial convolution to expand input features from board representation to 64 channels
    2. Stack of residual blocks for deep pattern recognition while avoiding vanishing gradients
    3. Policy head that outputs probability distributions over all possible moves (81 for 9x9 board)
    4. Value head that outputs a scalar evaluation of the position (-1 to 1 range)
    
    This dual-head design allows the network to simultaneously learn move selection and position
    assessment, enabling it to play Go at a high level through self-play reinforcement learning.
    The residual connections help train deeper networks by providing gradient flow shortcuts.
"""
class GoNet(nn.Module):

    """
    METHOD: __init__
    INPUT:
        boardSize (int, optional): Size of the Go board (default=9). For a 9x9 Go board.
                                This determines the spatial dimensions of input tensors.
        channels (int, optional): Number of input channels (default=17). 
                                Includes 8 channels for recent board positions, 8 for 
                                opponent positions, and 1 for current player indicator.
    RETURN:
        None: Constructor method that initializes the GoNet neural network architecture.

    DESCRIPTION:
        Initializes a neural network designed for playing Go, following an architecture
        similar to AlphaZero. The network consists of:
        
        1. Initial convolutional layer to expand from input channels to 64 feature maps
        2. Batch normalization for training stability
        3. Stack of residual blocks for deep feature extraction
        4. Policy head that outputs move probabilities for all board positions
        5. Value head that outputs position evaluation (-1 to 1 range)
        
        The architecture uses a shared trunk (conv + residual blocks) that feeds into
        two specialized heads for move prediction and position evaluation. This design
        allows the network to learn both tactical move selection and strategic position
        assessment simultaneously.
        
    """
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
        self.policyFullyConnected = nn.Linear(2 * self.boardSize * self.boardSize, 81)

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
            nn.Flatten(),

            # 81 is fixed because of nn.Conv2d(61,1, kernel_size-1)
            # while 64 is design choice giving an extra layer for 
            # additional thinking. Its power of 2.
            nn.Linear(1 * self.boardSize * self.boardSize, 64),
            nn.ReLU(),

            # Makes the 64 features from nn.LInear(1*9*9, 64) into a 
            # scalar.
            nn.Linear(64,1),

            # Activation function that squishes the otuput to 
            # be in range of -1 to 1.
            nn.Tanh()

        )       

    """
    METHOD: forward
    INPUT:
        x (torch.Tensor): Input tensor with shape [batch_size, 17, height, width].
                        This represents the game state features where 17 is the 
                        number of input channels (likely different board states/features).
    RETURN:
        tuple: A tuple containing two elements:
            - policyLogits (torch.Tensor): Policy logits with shape [batch_size, num_actions].
                                        Raw scores for each possible action/move.
            - value (torch.Tensor): State value predictions with shape [batch_size].
                                Scalar value representing the estimated worth of the position.
    DESCRIPTION:
        Performs the forward pass of a neural network architecture. The network has two heads: a policy head
        that predicts move probabilities of possible moves on the board and a value head that estimates who is 
        currently winning.
        
        The forward pass consists of:
        1. Initial convolution to expand feature depth from 17 to 64 channels
        2. Batch normalization and ReLU activation
        3. Series of residual blocks for deep feature extraction
        4. Policy head: reduces channels to 2, flattens, and outputs action logits
        5. Value head: processes features to output a single value prediction
        

    """
    def forward(self, x):

        # Initial convolution: expands input channels from 17 to 64
        # Using nn.Conv2d(17, 64, kernel_size=3, padding=1) to maintain spatial dimensions
        x = self.convolutional1(x)

        # Apply batch normalization to stabilize training
        x = self.batchNormalization1(x)

        # Apply ReLU activation for non-linearity
        x = F.relu(x)

        # Pass through residual blocks for deep feature extraction
        # Each block learns residual mappings F(x) + x to enable deeper networks
        for block in self.residualBlocks: x = block(x)

        # Take the output of the body and pass it to the policy head's layers.
        # This reduces the feature dept while retaining the spacial information
        # about move choices.
        p = self.policyHead(x)
        p = self.policyHeadBatchNormalization(p)
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
        # Converts from [batch_size, 1] to [batch_size] if needed
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