# Connect Four AI Algorithm

This document explains the complete algorithm used in the project, implemented in `connect4.py`.

---

## 1. Problem Statement

The game is played on a 6x7 board, with two players taking turns placing discs. One player is the human and the other is the AI. A player wins when they connect four discs in a straight line horizontally, vertically, or diagonally.

The AI must choose the best possible move at each turn. Since this is a two-player zero-sum game with perfect information, the most suitable solution is the Minimax algorithm, improved with alpha-beta pruning.

---

## 2. Game Representation

| Component | Representation |
| --- | --- |
| Board | 6 rows x 7 columns matrix |
| Empty cell | 0 |
| Human disc | 1 |
| AI disc | 2 |
| Move | Choosing a column (0 to 6) |
| Terminal state | One player wins or the board is full |
| Utility value | AI win = very high positive, Human win = very high negative, draw = 0 |

The board is stored as a 2D list where each entry is either empty, human, or AI.

---

## 3. Game Flow Overview

```text
START
  |
  v
Create an empty board and select difficulty
  |
  v
If it is the human turn:
    click a column -> drop disc
If it is the AI turn:
    select best move using minimax
  |
  v
Check for a win or draw
  |
  +--> If win/draw: show result and stop
  |
  +--> Otherwise: switch turns
```

---

## 4. Main AI Algorithm: Minimax with Alpha-Beta Pruning

### 4.1 Core Idea

- The AI is the maximizing player.
- The human is the minimizing player.
- The AI assumes the human will also play optimally.
- The search explores all possible moves up to a limited depth.
- At the leaf node, the board is evaluated using a heuristic function.
- The evaluation score is propagated upward through the search tree.

### 4.2 Alpha-Beta Pruning

Alpha-beta pruning is used to reduce unnecessary search.

- `alpha` stores the best value found so far for the maximizing player.
- `beta` stores the best value found so far for the minimizing player.
- If `alpha >= beta`, the remaining branches of that node cannot improve the current decision, so they are pruned.

### 4.3 Pseudocode

```text
function minimax(board, depth, alpha, beta, isMax):

    if AI has won:
        return (None, WIN_SCORE + depth)

    if Human has won:
        return (None, -WIN_SCORE - depth)

    if no valid moves remain:
        return (None, 0)            // draw

    if depth == 0:
        return (None, evaluate(board))

    bestCol = first legal column

    if isMax:                       // AI's turn
        value = -infinity
        for col in legal columns ordered from center outward:
            make AI move in col
            score = minimax(board, depth - 1, alpha, beta, False).score
            undo move

            if score > value:
                value = score
                bestCol = col

            alpha = max(alpha, value)

            if alpha >= beta:
                break               // prune

        return (bestCol, value)

    else:                           // Human's turn
        value = +infinity
        for col in legal columns ordered from center outward:
            make Human move in col
            score = minimax(board, depth - 1, alpha, beta, True).score
            undo move

            if score < value:
                value = score
                bestCol = col

            beta = min(beta, value)

            if alpha >= beta:
                break               // prune

        return (bestCol, value)
```

The first call is:

```text
minimax(board, depth, -infinity, +infinity, True)
```

---

## 5. Move Ordering

Columns are explored in this order:

```text
3, 2, 4, 1, 5, 0, 6
```

This means the AI tries the center columns first. Center columns are usually stronger, and ordering them early helps alpha-beta pruning cut more branches quickly.

---

## 6. Heuristic Evaluation Function

When the search reaches a leaf node and the position is not terminal, the board is scored using a heuristic evaluation.

### 6.1 Scoring Rules

The AI evaluates all possible windows of four cells, including:

- horizontal windows
- vertical windows
- diagonal windows (both directions)
- center column advantage

```text
function evaluate(board):
    score = 0

    // Prefer center control
    for each cell in the center column:
        if cell == AI:
            score += 3

    for each 4-cell window in the board:
        score += score_window(window)

    return score
```

### 6.2 Window Scoring

```text
function score_window(window):
    my_pieces = count of AI discs in the window
    opp_pieces = count of Human discs in the window
    empty_cells = count of empty cells in the window

    if my_pieces == 4:
        return +100
    if my_pieces == 3 and empty_cells == 1:
        return +5
    if my_pieces == 2 and empty_cells == 2:
        return +2
    if opp_pieces == 3 and empty_cells == 1:
        return -4      // opponent is close to winning, block it

    return 0
```

This heuristic favors:
- immediate wins
- strong threats
- central control
- blocking the opponent's near-winning moves

---

## 7. Winning Check

The board is checked for a winner after every move. A win exists when four discs of the same color lie in a contiguous line.

```text
function winning_cells(board, piece):
    for each cell in board:
        if cell == piece:
            for each direction in [right, down, down-right, down-left]:
                check next 3 cells in that direction
                if all 4 cells contain the same piece:
                    return those 4 cells
    return None
```

This checks all four possible directions of a connect-four line.

---

## 8. Difficulty Levels

The project supports three difficulty levels:

| Level | Search depth | Behavior |
| --- | ---: | --- |
| Easy | 2 | 30% chance of making a random move |
| Medium | 4 | Standard minimax search |
| Hard | 6 | Deeper minimax search |

Higher depth gives the AI more foresight, making it stronger.

---

## 9. Time and Space Complexity

Let:

- `b` = branching factor (maximum 7 legal moves)
- `d` = search depth

### Time Complexity

- Standard minimax: `O(b^d)`
- With alpha-beta pruning: often much smaller in practice, especially with good move ordering

### Space Complexity

- `O(d)` recursion depth
- Board is modified in-place and then restored (undo move), so memory usage stays low

---

## 10. Why This Works Well

This approach performs well for Connect Four because:

- the game tree is large but finite
- alpha-beta pruning removes many useless branches
- center-first move ordering improves pruning efficiency
- heuristic evaluation helps approximate positions when full depth search is not feasible

This gives a strong AI without requiring enormous computation.

---

## 11. Example of AI Decision Making

Suppose the human is one move away from winning. The AI search will examine the possible next moves and detect that allowing the human to complete four in a row would lead to a very bad score. The minimax search will therefore choose a move that blocks the threat or creates a stronger position.

In other words, the AI is not just playing greedily. It is analyzing future positions and choosing the move that maximizes its chance of winning while minimizing the opponent's chances.

---

## 12. Future Improvements

Possible improvements for this project include:

- transposition table for caching board states
- iterative deepening with a time limit
- stronger heuristic weighting
- Monte Carlo Tree Search (MCTS) comparison

These enhancements would improve both speed and strength of play.

---

## 13. Summary

The AI in this project uses:

1. a board state representation
2. legal move generation
3. win detection
4. minimax search
5. alpha-beta pruning
6. heuristic evaluation at depth limits
7. difficulty-based depth selection

This makes the AI capable of playing Connect Four at a strong level while remaining fast enough for a browser or desktop application.
