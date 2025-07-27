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
        self.board = board
        
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
    def __init__(self, network, simulations=800, exploration_weight=1.0, device=torch.device("cpu")):
        self.network = network
        self.simulations = simulations
        self.exploration_weight = exploration_weight
        self.root = None
        self.device = device
        
    def search(self, board):
        if self.root is None or not np.array_equal(self.root.board.board, board.board):
            self.root = Node(board=board.copyBoardState())
        
        for _ in range(self.simulations):
            node = self.root
            search_path = [node]
            
            while node.expanded() and not node.board.isGameOver():
                action, node = self.select_child(node)
                search_path.append(node)
            
            parent = search_path[-1]
            if not parent.board.isGameOver():
                value = self.expand_node(parent)
            else:
                scores = parent.board.score()
                value = 1 if scores[parent.board.currentPlayer] > scores[-parent.board.currentPlayer] else -1
            
            for node in reversed(search_path):
                node.value_sum += value
                node.visit_count += 1
                value = -value
        
        move = self.select_move(self.root)
        visited_counts = np.zeros(82)

        for action, child in self.root.children.items():
            visited_counts[action] = child.visit_count
        
        if visited_counts.sum() == 0:
            pi = np.ones(len(visited_counts)) / len(visited_counts)
        else:
            pi = visited_counts / visited_counts.sum()

        return move, torch.tensor(pi, device=self.device, dtype=torch.float32)
    
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
        board_tensor = boardToTensor(node.board).clone().detach().to(dtype=torch.float32, device=next(self.network.parameters()).device)

        with torch.no_grad():
            policy_logits, value = self.network(board_tensor)

        policy = F.softmax(policy_logits, dim=1).squeeze(0).cpu().numpy()
        valid_moves = node.board.getAllValidMoves()

        for move in valid_moves:
            if move == 'pass':
                pass_board = node.board.copyBoardState()
                pass_board.playMove(0, 0, pass_board.currentPlayer, passTurn=True)
                node.children[81] = Node(
                    parent=node,
                    prior=policy[81],
                    board=pass_board
                )
            else:
                x, y = move
                action = x * 9 + y
                if action >= len(policy):
                    continue

                # ADDED: Skip suicidal moves
                if node.board.isSuicidal(x, y, node.board.currentPlayer):
                    continue

                # ADDED: Discourage filling own eyes by reducing prior
                if node.board.isFillingOwnEye(x, y, node.board.currentPlayer):
                    policy[action] *= 0.1  # Downweight

                new_board = node.board.copyBoardState()
                success = new_board.playMove(x, y, new_board.currentPlayer)
                if not success:
                    continue

                # ADDED: Skip moves that result in 0 liberties (redundant if playMove fails on suicide)
                if new_board.countLiberties(x, y) == 0:
                    continue

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
