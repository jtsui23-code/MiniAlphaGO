# Monte Carlo Tree Search with Neural Networks - Detailed Explanation

## Node Selection (Tree Traversal)

The algorithm begins at the **root node** (current game state) and navigates the tree using the UCT formula:

```
UCT = Q(s,a) + c * P(s,a) * √(N(s))/(1 + N(s,a))
```

**Components:**
- `Q`: Average value (how successful moves have been historically)
- `P`: Neural network's prior probability for the move
- `N`: Visit count for the node
- `c`: Exploration parameter (typically between 0.5-2.0)

**Balance achieved:**
1. **Exploration**: Tries moves the network suggests (high P)
2. **Exploitation**: Uses moves that worked well (high Q)
3. **Discovery**: Investigates less-tried options (low N)

## Expansion Phase

When reaching an unexplored **leaf node**:
1. Network's policy head outputs move probabilities
2. Creates child nodes for all legal moves
3. Stores in each child:
   - Resulting game state
   - Move that created it
   - Network's probability estimate (P)

*Key benefit:* Focuses search only on plausible moves, ignoring bad options.

## Simulation (Value Estimation)

**Unlike random playouts in classic MCTS:**
- Uses value network for instant evaluation
- Outputs score between -1 (certain loss) and 1 (certain win)

**Advantages:**
- 100-1000x faster than random playouts
- More accurate evaluations
- Consistent with policy head's understanding

## Backpropagation

After evaluation:
1. Increments visit counters (`N`) for all nodes in path
2. Accumulates value through tree (with sign alternation)
   - *Why sign flip?* Good for me = bad for opponent
3. Root node value represents overall position evaluation
4. Visit counts show which moves were explored most

## Why This Hybrid Approach Works

**Neural Network Provides:**
- Smart move suggestions (policy head)
- Instant position evaluations (value head)

**MCTS Provides:**
- Deep lookahead capability
- Adaptive exploration based on actual results

**Synergy Benefits:**
- Focuses computation on promising variations
- Verifies network's intuition with concrete analysis
- Discovers non-obvious tactical sequences

## Search Tree Characteristics

**Structure:**
- Nodes = game states
- Edges = possible moves

**Node Data:**
- `N`: Visit count
- Total value: Cumulative results
- `P`: Network's initial probability

*Growth Pattern:* Develops asymmetrically with deeper exploration of promising lines

## Performance Considerations

**Per Simulation:**
1. One neural network evaluation (policy + value)
2. Tree traversal operations (scales with depth)

**Total Time Depends On:**
- Number of simulations
- Network evaluation speed
- Average search depth

**Memory Requirements:**
- Grows with nodes created and state size
- Typical 9x9 Go with 800 simulations: Several thousand nodes (easily manageable)
```

This version:
1. Uses proper Markdown formatting for readability
2. Maintains all technical details
3. Organizes information logically
4. Highlights key concepts clearly
5. Presents formulas and components cleanly