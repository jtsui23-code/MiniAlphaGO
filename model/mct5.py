import math
import numpy as np
import torch
import torch.nn.functional as F
from collections import defaultdict
from utils.boardToTensor import boardToTensor  

class Node:
    def __init__(self, parent=None, prior=0, board=None):
        self.parent = parent
        self.children = {}
        self.prior = prior
        self.visit_count = 0
        self.value_sum = 0
        self.board = board  # Always store the board state
        
    def expanded(self):
        return len(self.children) > 0
    
    def value(self):
        if self.visit_count == 0:
            return 0
        return self.value_sum / self.visit_count
    
    def ucb_score(self, exploration_weight):
        if self.visit_count == 0:
            return float('inf') if self.prior > 0 else float('-inf')
        return (self.value() + 
                exploration_weight * self.prior * 
                math.sqrt(self.parent.visit_count) / (1 + self.visit_count))

class MCTS:
    def __init__(self, network, simulations=800, exploration_weight=1.0, device=torch.device("cpu"),
                 dirichlet_alpha=0.3, dirichlet_epsilon=0.25, temperature=1.0):
        self.network = network
        self.simulations = simulations
        self.exploration_weight = exploration_weight
        self.root = None
        self.device = device
        
        # Enhanced parameters for self-play training
        self.dirichlet_alpha = dirichlet_alpha  # Controls exploration noise strength
        self.dirichlet_epsilon = dirichlet_epsilon  # Mixing ratio for Dirichlet noise
        self.temperature = temperature  # Controls move selection randomness
        
    def search(self, board, add_dirichlet_noise=True, use_temperature=True):
        """
        Enhanced search with Dirichlet noise and temperature control
        
        Args:
            board: Current board state
            add_dirichlet_noise: Whether to add Dirichlet noise to root (for self-play)
            use_temperature: Whether to use temperature in move selection
        """
        # Create new root if needed
        if self.root is None:
            self.root = Node(board=board.copyBoardState())
        # Or update root if board state changed
        elif not np.array_equal(self.root.board.board, board.board):
            self.root = Node(board=board.copyBoardState())
        
        # Expand root node first if not expanded
        if not self.root.expanded() and not self.root.board.isGameOver():
            self.expand_node(self.root, add_dirichlet_noise=add_dirichlet_noise)
        
        for _ in range(self.simulations):
            node = self.root
            search_path = [node]
            
            # Selection - traverse down the tree using UCB
            while node.expanded() and not node.board.isGameOver():
                action, node = self.select_child(node)
                search_path.append(node)
            
            # Expansion and Evaluation
            parent = search_path[-1]
            if not parent.board.isGameOver():
                value = self.expand_node(parent, add_dirichlet_noise=False)  # Only add noise to root
            else:
                # If game is over, use the actual result
                scores = parent.board.score()
                current_player_score = scores[parent.board.currentPlayer]
                opponent_score = scores[-parent.board.currentPlayer]
                
                if current_player_score > opponent_score:
                    value = 1.0
                elif current_player_score < opponent_score:
                    value = -1.0
                else:
                    value = 0.0  # Draw
            
            # Backpropagation
            for node in reversed(search_path):
                node.value_sum += value
                node.visit_count += 1
                value = -value  # Alternate for opponent
        
        # Select move based on visit counts with optional temperature
        move = self.select_move(self.root, use_temperature=use_temperature)
        
        # Create policy vector (pi) from visit counts
        visited_counts = np.zeros(82)  # 81 board positions + 1 pass move
        for action, child in self.root.children.items():
            visited_counts[action] = child.visit_count
        
        # Apply temperature to visit counts for policy
        if use_temperature and self.temperature != 1.0:
            if self.temperature == 0:
                # Greedy selection - only best move gets probability 1
                pi = np.zeros_like(visited_counts)
                best_action = np.argmax(visited_counts)
                pi[best_action] = 1.0
            else:
                # Apply temperature
                visited_counts = visited_counts ** (1.0 / self.temperature)
                pi = visited_counts / (visited_counts.sum() + 1e-8)
        else:
            # Standard normalization
            if visited_counts.sum() == 0:
                pi = np.ones(len(visited_counts)) / len(visited_counts)
            else:
                pi = visited_counts / visited_counts.sum()

        return move, torch.tensor(pi, device=self.device, dtype=torch.float32)
    
    def select_child(self, node):
        """Select child with highest UCB score"""
        best_score = -float('inf')
        best_action = -1
        best_child = None
        
        for action, child in node.children.items():
            score = child.ucb_score(self.exploration_weight)
            if score > best_score:
                best_score = score
                best_action = action
                best_child = child
                
        return best_action, best_child
    
    def expand_node(self, node, add_dirichlet_noise=False):
        """
        Expand node and optionally add Dirichlet noise to priors
        
        Args:
            node: Node to expand
            add_dirichlet_noise: Whether to add Dirichlet noise (typically only for root)
        """
        board_tensor = boardToTensor(node.board).clone().detach().to(
            dtype=torch.float32, device=next(self.network.parameters()).device
        )

        with torch.no_grad():
            policy_logits, value = self.network(board_tensor)
        
        # Convert to probabilities
        policy = F.softmax(policy_logits, dim=1).squeeze(0).cpu().numpy()
        
        # Add Dirichlet noise for exploration (typically only at root during self-play)
        if add_dirichlet_noise:
            noise = np.random.dirichlet([self.dirichlet_alpha] * len(policy))
            policy = (1 - self.dirichlet_epsilon) * policy + self.dirichlet_epsilon * noise
        
        valid_moves = node.board.getAllValidMoves()
        
        # Add all valid moves as children
        for move in valid_moves:
            if move == 'pass':
                # Pass move (action 81)
                pass_board = node.board.copyBoardState()
                pass_board.playMove(0, 0, pass_board.currentPlayer, passTurn=True)
                node.children[81] = Node(
                    parent=node,
                    prior=policy[81],
                    board=pass_board
                )
            else:
                # Regular moves
                x, y = move
                action = x * 9 + y
                if action < len(policy):
                    new_board = node.board.copyBoardState()
                    new_board.playMove(x, y, new_board.currentPlayer)
                    node.children[action] = Node(
                        parent=node,
                        prior=policy[action],
                        board=new_board
                    )
        
        return value.item()
    
    def select_move(self, node, use_temperature=True):
        """
        Select move based on visit counts, optionally using temperature
        
        Args:
            node: Root node
            use_temperature: Whether to use temperature for selection
        """
        if not node.children:
            return None
        
        if use_temperature and self.temperature > 0:
            # Temperature-based selection
            actions = list(node.children.keys())
            visit_counts = np.array([node.children[action].visit_count for action in actions])
            
            if self.temperature == float('inf'):
                # Uniform random selection
                probabilities = np.ones(len(actions)) / len(actions)
            else:
                # Apply temperature
                visit_counts_temp = visit_counts ** (1.0 / self.temperature)
                probabilities = visit_counts_temp / (visit_counts_temp.sum() + 1e-8)
            
            # Sample action based on probabilities
            selected_idx = np.random.choice(len(actions), p=probabilities)
            return actions[selected_idx]
        else:
            # Greedy selection - choose most visited
            best_move = None
            best_visit_count = -1
            
            for move, child in node.children.items():
                if child.visit_count > best_visit_count:
                    best_visit_count = child.visit_count
                    best_move = move
                    
            return best_move
    
    def update_root(self, move):
        """Update root node after a move is played"""
        if self.root and move in self.root.children:
            self.root = self.root.children[move]
            self.root.parent = None
        else:
            self.root = None
    
    def set_temperature(self, temperature):
        """Dynamically adjust temperature during training"""
        self.temperature = temperature
    
    def get_search_statistics(self):
        """Get statistics about the current search tree for debugging"""
        if not self.root:
            return {}
        
        stats = {
            'root_visits': self.root.visit_count,
            'root_value': self.root.value(),
            'children_count': len(self.root.children),
            'max_child_visits': max([child.visit_count for child in self.root.children.values()]) if self.root.children else 0
        }
        return stats