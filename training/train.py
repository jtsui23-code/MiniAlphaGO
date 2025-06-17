import torch
import torch.nn as nn
import torch.optim as optim
from model.net import GoNet
from training.replayBuffer import ReplayBuffer

def train(network: GoNet, buffer: ReplayBuffer, batchSize=64, epochs=10, learningRate=1e-3):
    if len(buffer) < batchSize:
        print("Not enough samples in buffer. Skipping training.")
        return

    # Loss functions
    policyLossFn = nn.CrossEntropyLoss()
    valueLossFn = nn.MSELoss()

    # Optimizer
    optimizer = optim.Adam(network.parameters(), lr=learningRate, weight_decay=1e-4)

    network.train()

    for epoch in range(epochs):
        # Sample training data
        states, pis, zs = buffer.sample(batchSize)

        # Forward pass
        pred_pis, pred_zs = network(states)

        # Policy loss: softmax over logits vs pi targets
        loss_pi = policyLossFn(pred_pis, pis.argmax(dim=1))

        # Value loss: scalar win/loss prediction
        loss_z = valueLossFn(pred_zs.squeeze(), zs)

        # Total loss
        loss = loss_pi + loss_z

        # Backward and update
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        print(f"[Epoch {epoch + 1}] Total Loss: {loss.item():.4f} | Policy: {loss_pi.item():.4f} | Value: {loss_z.item():.4f}")
"""
Jack, here is some example usage for you


    network = GoNet(boardSize=9, inputPlanes=17)
    buffer = ReplayBuffer(capacity=10000)
    buffer.loadFile("selfPlay/selfPlayBuffer_200.pkl")

    train(network, buffer, batchSize=64, epochs=10)

    torch.save(network.state_dict(), "models/newModel.pt")

"""