import random
import torch
from utils.boardToTensor import boardToTensor  
import pickle

class ReplayBuffer:

    def __init__(self, capacity):
        self.capacity = capacity
        self.buffer = []

    def add(self, state, pi, z):

        self.buffer.append((state, pi, z))
        if len(self.buffer) > self.capacity:
            self.buffer.pop(0)

    def saveToFile(self, fileName):
        # 'wb' write binary the file will be in binary not human readable format.
        with open(fileName, 'wb') as f:
            pickle.dump(self.buffer, f)

    def loadFile(self, fileName):
        # 'rb' - read buffer different from 'r' because this is binary. 
        with open(fileName, 'rb') as f:
            newData = pickle.load(f)

            # This appends all of the new data files into self.buffer 
            # This is the same thing as doing a for loop and just self.buffer.append()
            self.buffer.extend(newData)
            
            # Ensures the buffer is in range of the capacity. 
            # Gets the last number of capacity indexes preventing index overflow.
            self.buffer = self.buffer[-self.capacity:]

    def sample(self, numberOfSamples):
        batch = random.sample(self.buffer, numberOfSamples)

        # *batch splits the list of tuples into separate elements.
        # zip groups the 1st, 2nd, and 3rd element of each split tuples 
        # this creates a list of al of the states a list of all of the pi and a list
        # of all of the z. 
        states, pis, zs = zip(*batch)

       

        # states is already a tensor so doesn't need to be converted from Board State -> Tensor
        states = torch.stack(states).squeeze(1)
        pis = torch.tensor(pis, dtype=torch.float32)
        zs = torch.tensor(zs, dtype=torch.float32)

        return states, pis, zs



    def __len__(self):
        return len(self.buffer)