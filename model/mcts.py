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
    def __init__(self, network, simulations=800, exploration_weight=1.0):
        self.network = network
        self.simulations = simulations
        self.exploration_weight = exploration_weight
        self.root = None
        
    def search(self, board):
        # Create new root if needed
        if self.root is None:
            self.root = Node(board=board.copyBoardState())
        # Or update root if board state changed
        elif not np.array_equal(self.root.board.board, board.board):
            self.root = Node(board=board.copyBoardState())
        
        for _ in range(self.simulations):
            node = self.root
            search_path = [node]
            
            # Selection
            while node.expanded() and not node.board.isGameOver():
                action, node = self.select_child(node)
                search_path.append(node)
            
            # Expansion
            parent = search_path[-1]
            if not parent.board.isGameOver():
                value = self.expand_node(parent)
            else:
                # If game is over, use the actual result
                scores = parent.board.score()
                value = 1 if scores[parent.board.currentPlayer] > scores[-parent.board.currentPlayer] else -1
            
            # Backpropagation
            for node in reversed(search_path):
                node.value_sum += value
                node.visit_count += 1
                value = -value  # Alternate for opponent
        
        move = self.select_move(self.root)
        
        # Array to store the probabilities of all the possible moves on the board.
        # 82 because 82 represents passing. 9x9 = 81
        visited_counts = np.zeros(82)

        # Finding the visit count of all the moves on the board.
        for action, child in self.root.children.items():
            visited_counts[action] = child.visit_count
        
        # pi is a vector of the probabilities of all the moves and the board and passing.
        pi = visited_counts/ visited_counts.sum()

        # Returns the best move and the pi vector.
        return move, pi
    
    def select_child(self, node):
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
    
    def expand_node(self, node):
        board_tensor = boardToTensor(node.board)
        with torch.no_grad():
            policy_logits, value = self.network(board_tensor)
        policy = F.softmax(policy_logits, dim=1).squeeze(0).cpu().numpy()
        
        valid_moves = node.board.getAllValidMoves()
        
        # Add all valid moves as children, including pass if it's valid
        for move in valid_moves:
            if move == 'pass':
                # Pass move (assuming action 81 represents pass)
                pass_board = node.board.copyBoardState()
                pass_board.playMove(0, 0, pass_board.currentPlayer, passTurn=True)
                node.children[81] = Node(
                    parent=node,
                    prior=policy[81],  # Use network's policy for pass
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
    
    def select_move(self, node):
        best_move = None
        best_visit_count = -1
        
        for move, child in node.children.items():
            if child.visit_count > best_visit_count:
                best_visit_count = child.visit_count
                best_move = move
                
        return best_move
    
    def update_root(self, move):
        if move in self.root.children:
            self.root = self.root.children[move]
            self.root.parent = None
        else:
            self.root = None