**Breakthrough AI Agent**
This repository contains an AI agent designed to play the strategic board game Breakthrough on a 6×6 board. The agent uses adversarial search algorithms to make intelligent, time-efficient decisions.

**Features**
- Minimax with Alpha-Beta Pruning: Optimizes decision-making by efficiently searching the game tree.
- Iterative Deepening: Dynamically adjusts search depth to ensure decisions are made within a strict 3-second time constraint.
- Zobrist Hashing for State Caching: Improves performance by storing previously evaluated board states.
- Custom Heuristic Evaluation Function: Assesses board positions based on mobility, piece advancement, center control, and piece count.
  
**Technologies Used**
- Programming Language: Python
- Algorithms: Minimax, Alpha-Beta Pruning, Iterative Deepening, Zobrist Hashing
- Data Structures: Hash Tables, Game Trees
- Game Framework: Custom utilities for move validation, board inversion, and game state evaluation
  
**How It Works**
- Reads the Board State: Parses the game board to determine available moves.
- Applies Minimax with Alpha-Beta Pruning: Searches for the best move while cutting off unproductive branches.
- Uses Iterative Deepening: Starts at depth 1 and increases depth dynamically within a 3-second time limit.
- Employs Heuristic Evaluation: Ranks board states based on game-specific criteria.
  
**Future Enhancements**
- Implement Monte Carlo Tree Search (MCTS) for probabilistic move selection.
- Experiment with Reinforcement Learning to refine heuristic functions dynamically
