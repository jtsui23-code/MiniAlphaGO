"""
MCTS Implementation for Mini AlphaGo (9x9)

(Line 256 for example usage)

This module implements Monte Carlo Tree Search with Neural Network guidance for Go,
following AlphaGo Zero's approach with simplifications for 9x9 boards.

CLASSES:
    MCTSNode: Represents game states in the search tree
    MCTS: Main search algorithm using neural network for policy/value estimation

USAGE EXAMPLE:
    1. Initialize with trained GoNet:
       mcts = MCTS(network, exploration_weight=1.0, simulations=800)
    2. Perform search:
       best_move = mcts.search(current_board_state)
    3. For subsequent moves:
       mcts.update_root(played_move)
       best_move = mcts.search(new_board_state)
"""

import math
import numpy as np
import torch
from collections import defaultdict

class MCTSNode:
    """
    A node in the Monte Carlo search tree representing a game state.

    ATTRIBUTES:
        state: Current game state (GoBoard object)
        parent: Parent node (None if root)
        move: Move that led to this node (None if root)
        children: List of child nodes
        visits: Number of times node was visited
        total_value: Cumulative value from all simulations
        prior: Prior probability from policy network

    METHODS:
        __init__: Initialize new node
        value: Calculate average value (Q(s,a))
        is_fully_expanded: Check if node has all children expanded
        select_child: Choose child using UCT formula
        expand: Create child nodes from policy probabilities
        backpropagate: Update statistics with simulation result
    """

    def __init__(self, state, parent=None, move=None):
        """
        METHOD: __init__
        INPUT:
            state: GoBoard object representing game state
            parent: Parent MCTSNode (None for root)
            move: Move that led to this node (None for root)
        RETURN:
            None: Initializes new MCTSNode instance
        """
        self.state = state
        self.parent = parent
        self.move = move
        self.children = []
        self.visits = 0
        self.total_value = 0.0
        self.prior = 0.0

    @property
    def value(self):
        """
        METHOD: value
        INPUT: None
        RETURN: float
            Average value of the node (Q(s,a))
            Returns 0 if node hasn't been visited
        """
        if self.visits == 0:
            return 0
        return self.total_value / self.visits

    def is_fully_expanded(self):
        """
        METHOD: is_fully_expanded
        INPUT: None
        RETURN: bool
            True if node has all legal moves expanded as children
            False otherwise
        """
        return len(self.children) > 0

    def select_child(self, exploration_weight=1.0):
        """
        METHOD: select_child
        INPUT:
            exploration_weight: float (default=1.0)
                Controls exploration vs exploitation tradeoff
        RETURN: MCTSNode
            Child node with highest UCT score:
            UCT = Q(s,a) + c * P(s,a) * √(N(s))/(1 + N(s,a))
        """
        total_visits = sum(child.visits for child in self.children)
        log_total = math.log(total_visits + 1)

        best_score = -float('inf')
        best_child = None
        
        for child in self.children:
            exploitation = child.value
            exploration = child.prior * (math.sqrt(log_total) / (child.visits + 1))
            uct_score = exploitation + exploration_weight * exploration
            
            if uct_score > best_score:
                best_score = uct_score
                best_child = child
                
        return best_child

    def expand(self, policy_probs):
        """
        METHOD: expand
        INPUT:
            policy_probs: np.ndarray
                Move probabilities from policy network
                Shape: (82,) for 9x9 (81 moves + pass)
        RETURN: None
            Creates child nodes for all legal moves with prior probabilities
        """
        for move, prob in enumerate(policy_probs):
            if prob > 1e-6:  # Threshold for valid moves
                new_state = self.state.make_move(move)
                if new_state is not None:  # Legal move check
                    child = MCTSNode(new_state, self, move)
                    child.prior = prob
                    self.children.append(child)

    def backpropagate(self, value):
        """
        METHOD: backpropagate
        INPUT:
            value: float (-1 to 1)
                Value estimate from simulation
        RETURN: None
            Updates visit count and total value for this node and all ancestors
            Alternates value sign for opponent nodes
        """
        self.visits += 1
        self.total_value += value
        if self.parent:
            self.parent.backpropagate(-value)  # Flip for opponent


class MCTS:
    """
    Monte Carlo Tree Search with Neural Network guidance.

    ATTRIBUTES:
        network: GoNet instance for policy/value predictions
        exploration_weight: float controlling exploration vs exploitation
        simulations: int number of MCTS simulations per move
        root: MCTSNode root of search tree

    METHODS:
        __init__: Initialize MCTS searcher
        search: Perform MCTS from given game state
        get_best_move: Return most visited move
        update_root: Advance root after move for successive searches
    """

    def __init__(self, network, exploration_weight=1.0, simulations=800):
        """
        METHOD: __init__
        INPUT:
            network: GoNet
                Trained neural network for policy/value predictions
            exploration_weight: float (default=1.0)
                Controls exploration vs exploitation tradeoff
            simulations: int (default=800)
                Number of MCTS simulations per move
        RETURN:
            None: Initializes MCTS instance
        """
        self.network = network
        self.exploration_weight = exploration_weight
        self.simulations = simulations
        self.root = None

    def search(self, initial_state):
        """
        METHOD: search
        INPUT:
            initial_state: GoBoard
                Current game state to search from
        RETURN: int
            Best move found by search (0-80 for board, 81 for pass)
            Returns None if no legal moves
        """
        self.root = MCTSNode(initial_state)
        
        for _ in range(self.simulations):
            node = self.root
            
            # Selection phase
            while node.is_fully_expanded():
                node = node.select_child(self.exploration_weight)
            
            # Expansion phase
            if not node.state.is_game_over():
                with torch.no_grad():
                    state_tensor = node.state.get_state().unsqueeze(0)
                    policy_logits, _ = self.network(state_tensor)
                    policy_probs = torch.softmax(policy_logits, dim=1).numpy()[0]
                node.expand(policy_probs)
            
            # Simulation phase
            with torch.no_grad():
                state_tensor = node.state.get_state().unsqueeze(0)
                _, value = self.network(state_tensor)
                value = value.item()
            
            # Backpropagation phase
            node.backpropagate(value)
        
        return self.get_best_move()

    def get_best_move(self):
        """
        METHOD: get_best_move
        INPUT: None
        RETURN: int or None
            Move with highest visit count (0-80 for board, 81 for pass)
            Returns None if no legal moves exist
        """
        if not self.root.children:
            return None
            
        visits = [child.visits for child in self.root.children]
        best_child = self.root.children[np.argmax(visits)]
        return best_child.move

    def update_root(self, move):
        """
        METHOD: update_root
        INPUT:
            move: int
                Move that was played (0-80 for board, 81 for pass)
        RETURN: None
            Advances root to child node corresponding to played move
            Creates new root if move not found in children
        """
        for child in self.root.children:
            if child.move == move:
                self.root = child
                self.root.parent = None
                return
        new_state = self.root.state.make_move(move)
        self.root = MCTSNode(new_state)

"""
# Example Usage
if __name__ == "__main__":

    EXAMPLE USAGE:
    1. Initialize components:
       network = GoNet()
       mcts = MCTS(network)
    2. Perform search:
       best_move = mcts.search(current_board)
    3. Make move and update:
       board.make_move(best_move)
       mcts.update_root(best_move)

    from net import GoNet
    from go_board import GoBoard  # Your Go board implementation

    # Initialize
    network = GoNet()
    network.eval()
    mcts = MCTS(network)
    board = GoBoard()

    # First move
    best_move = mcts.search(board)
    print(f"Best move: {best_move}")

    # Subsequent moves would use:
    # board.make_move(best_move)
    # mcts.update_root(best_move)
    # best_move = mcts.search(board)
"""