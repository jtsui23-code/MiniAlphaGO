import random
import torch
from utils.boardToTensor import boardToTensor  

class ReplayBuffer:

    def __init__(self, capacity):
        self.capacity = capacity
        self.buffer = []

    def add(self, state, pi, z):

        self.buffer.append((state, pi, z))
        if len(self.buffer) > self.capacity:
            self.buffer.pop(0)

        
    def sample(self, numberOfSamples):
        batch = random.sample(self.buffer, numberOfSamples)

        # *batch splits the list of tuples into separate elements.
        # zip groups the 1st, 2nd, and 3rd element of each split tuples 
        # this creates a list of al of the states a list of all of the pi and a list
        # of all of the z. 
        states, pis, zs = zip(*batch)

        # Converting the lists into tensors to be used in the network.
        # Have to convert the board state into a tensor before using torch.stack.
        # Have to use for loop because boardToTensor expects a single board state not a list of them.
        states = [boardToTensor(s) for s in states]

        states = torch.stack(states)
        pis = torch.tensor(pis, dtype=torch.float32)
        zs = torch.tensor(zs, dtype=torch.float32)

        return states, pis, zs



    def __len__(self):
        return len(self.buffer)