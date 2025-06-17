import torch
import torch.nn as nn
import torch.optim as optim
from model.net import GoNet
from training.replayBuffer import ReplayBuffer

def train(network: GoNet, buffer: ReplayBuffer, batchSize=64, epochs=10, learningRate=1e-3):
    # Skip training if buffer doesn't have enough samples
    if len(buffer) < batchSize:
        print("Not enough samples in buffer. Skipping training.")
        return

    # Define the loss function for the policy head (classification of moves)
    policyLossFn = nn.CrossEntropyLoss()

    # Define the loss function for the value head (regression of game outcome)
    valueLossFn = nn.MSELoss()

    # Use Adam optimizer with L2 regularization (weight decay)
    optimizer = optim.Adam(network.parameters(), lr=learningRate, weight_decay=1e-4)

    # Set the network to training mode (affects things like dropout/batchnorm if used)
    network.train()

    for epoch in range(epochs):
        # Sample a batch of training data from the replay buffer
        states, pis, zs = buffer.sample(batchSize)

        # Forward pass through the network to get predictions
        pred_pis, pred_zs = network(states)

        # Compute policy loss
        # pred_pis: [batchSize, num_moves] logits from the network
        # pis: [batchSize, num_moves] target policy vectors
        # pis.argmax(dim=1): get the target move index
        loss_pi = policyLossFn(pred_pis, pis.argmax(dim=1))

        # Compute value loss
        # pred_zs: [batchSize, 1] predicted value (win/loss score)
        # zs: [batchSize] target scalar outcome
        loss_z = valueLossFn(pred_zs.squeeze(), zs)

        # Combine the two losses into total loss
        loss = loss_pi + loss_z

        # Backpropagation step
        optimizer.zero_grad()   # Clear previous gradients
        loss.backward()         # Compute new gradients
        optimizer.step()        # Apply parameter update

        # Print loss values for monitoring
        print(f"[Epoch {epoch + 1}] Total Loss: {loss.item():.4f} | Policy: {loss_pi.item():.4f} | Value: {loss_z.item():.4f}")

"""
Example usage for training the model

    # Create network instance with board size and input plane count
    network = GoNet(boardSize=9, inputPlanes=17)

    # Initialize replay buffer with a maximum capacity
    buffer = ReplayBuffer(capacity=10000)

    # Load previously saved self-play training data
    buffer.loadFile("selfPlay/selfPlayBuffer_200.pkl")

    # Train the model on the loaded data
    train(network, buffer, batchSize=64, epochs=10)

    # Save the trained model to a file
    torch.save(network.state_dict(), "models/newModel.pt")
"""
