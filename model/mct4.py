import math
import numpy as np
import torch
import torch.nn.functional as F
from utils.boardToTensor import boardToTensor

class Node:
    def __init__(self, parent=None, prior=0, board=None):
        self.parent = parent
        self.children = {}
        self.prior = prior
        self.visit_count = 0
        self.value_sum = 0
        self.board = board
        
    def expanded(self):
        return len(self.children) > 0
    
    def value(self):
        if self.visit_count == 0:
            return 0
        return self.value_sum / self.visit_count
    
    def ucb_score(self, exploration_weight):
        if self.visit_count == 0:
            return float('inf')
        
        exploitation = self.value()
        exploration = exploration_weight * self.prior * math.sqrt(self.parent.visit_count) / (1 + self.visit_count)
        return exploitation + exploration

class MCTS:
    def __init__(self, network, simulations=800, exploration_weight=1.0, device=torch.device("cpu")):
        self.network = network
        self.simulations = simulations
        self.exploration_weight = exploration_weight
        self.root = None
        self.device = device
        
    def search(self, board):
        # Reset root if board state changed
        if self.root is None or not np.array_equal(self.root.board.board, board.board):
            self.root = Node(board=board.copyBoardState())
        
        for _ in range(self.simulations):
            node = self.root
            search_path = [node]
            
            # Selection: traverse down to leaf
            while node.expanded() and not node.board.isGameOver():
                action, node = self.select_child(node)
                search_path.append(node)
            
            # Expansion and Evaluation
            leaf_node = search_path[-1]
            if not leaf_node.board.isGameOver():
                value = self.expand_node(leaf_node)
            else:
                # Terminal node evaluation
                value = self.evaluate_terminal(leaf_node)
            
            # Backup: propagate value up the tree
            self.backup(search_path, value)
        
        # Return best move and visit distribution
        return self.get_action_probs()
    
    def select_child(self, node):
        best_score = -float('inf')
        best_action = None
        best_child = None
        
        for action, child in node.children.items():
            score = child.ucb_score(self.exploration_weight)
            if score > best_score:
                best_score = score
                best_action = action
                best_child = child
                
        return best_action, best_child
    
    def expand_node(self, node):
        # Get network predictions
        board_tensor = boardToTensor(node.board).clone().detach().to(
            dtype=torch.float32, 
            device=next(self.network.parameters()).device
        )
        
        with torch.no_grad():
            policy_logits, value = self.network(board_tensor)
        
        # Convert to probabilities
        policy = F.softmax(policy_logits, dim=1).squeeze(0).cpu().numpy()
        
        # Add Dirichlet noise for exploration (only at root)
        if node.parent is None:
            noise = np.random.dirichlet([0.03] * len(policy))
            policy = 0.75 * policy + 0.25 * noise
        
        # Create children for all legal moves - FIX: Pass currentPlayer
        valid_moves = node.board.getAllValidMoves(node.board.currentPlayer)
        
        for move in valid_moves:
            if move == 'pass':
                # Handle pass move
                new_board = node.board.copyBoardState()
                if new_board.playMove(0, 0, new_board.currentPlayer, passTurn=True):
                    pass_action = len(policy) - 1
                    node.children[pass_action] = Node(
                        parent=node,
                        prior=policy[pass_action],
                        board=new_board
                    )
            else:
                x, y = move
                action = x * node.board.size + y  # FIX: Use board.size not hardcoded 9
                
                # Skip if action index is out of bounds
                if action >= len(policy) - 1:  # FIX: -1 for pass action
                    continue
                
                # Try the move - FIX: Check if move succeeded
                new_board = node.board.copyBoardState()
                if new_board.playMove(x, y, new_board.currentPlayer):
                    node.children[action] = Node(
                        parent=node,
                        prior=policy[action],
                        board=new_board
                    )
        
        return value.item()
    
    def evaluate_terminal(self, node):
        scores = node.board.score()
        current_player = node.board.currentPlayer
        opponent = -current_player
        
        if scores[current_player] > scores[opponent]:
            return 1.0
        elif scores[current_player] < scores[opponent]:
            return -1.0
        else:
            return 0.0
    
    def backup(self, search_path, value):
        for node in reversed(search_path):
            node.value_sum += value
            node.visit_count += 1
            value = -value  # Flip value for opponent
    
    def get_action_probs(self):
        if not self.root.children:
            # No legal moves, return pass move
            board_size = self.root.board.size
            total_actions = board_size * board_size + 1
            pi = np.zeros(total_actions)
            pi[-1] = 1.0  # Set pass move to 100%
            return total_actions - 1, torch.tensor(pi, device=self.device, dtype=torch.float32)
        
        # Get visit counts
        actions = list(self.root.children.keys())
        visit_counts = np.array([self.root.children[action].visit_count for action in actions])
        
        # Select move with highest visit count
        best_move = actions[np.argmax(visit_counts)]
        
        # Create full probability distribution
        board_size = self.root.board.size
        total_actions = board_size * board_size + 1  # +1 for pass
        pi = np.zeros(total_actions)
        
        if visit_counts.sum() > 0:
            for action, count in zip(actions, visit_counts):
                pi[action] = count / visit_counts.sum()
        else:
            # Fallback to uniform if no visits
            pi.fill(1.0 / total_actions)
        
        return best_move, torch.tensor(pi, device=self.device, dtype=torch.float32)
    
    def update_root(self, move):
        """Update root to move down the tree after opponent's move"""
        if self.root and move in self.root.children:
            self.root = self.root.children[move]
            self.root.parent = None
        else:
            self.root = None