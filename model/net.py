import torch 
import torch.nn as nn
import torch.nn.functional as F

class GoNet(nn.Module):

    def __init__(self):
        super(GoNet, self).__init__()

        # self.conv1 is a 2D convolutional layer useful for images and board games.
        # input channels  -  17
        # output channels -  64
        # kernel size     -  3
        # padding         -  1
        self.conv1 = nn.Conv2d(17, 64, kernel_size=3, padding=1)

        self.resBlocks = nn.ModuleList([
            ResidualBlock(64) for _ in range(4)

        ])

class ResidualBlock(nn.MarginRankingLoss):

    def __init__(self, channels):
        super(ResidualBlock, self). __init__()

        self.conv1 = nn.Con2d(channels, channels, kernel_size=3, padding=1)
        